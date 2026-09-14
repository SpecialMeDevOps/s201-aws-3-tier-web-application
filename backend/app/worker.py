import logging
import os
import requests
from . import create_app, db
from .models import Job, Result
from .validation import InvalidTarget, validate_target_url

log = logging.getLogger(__name__)

def process_job(job):
    app = create_app()
    with app.app_context():
        job = db.session.get(Job, job.id)
        if not job or job.status != "queued":
            return False
        job.status = "running"
        db.session.commit()
        try:
            validate_target_url(job.target_url)
            response = requests.get(job.target_url, timeout=app.config["REQUEST_TIMEOUT_SECONDS"],
                                    allow_redirects=False, stream=True,
                                    headers={"User-Agent": "s201-fetcher/1.0"})
            max_bytes = app.config["MAX_RESPONSE_BYTES"]
            data = b""
            for chunk in response.iter_content(8192):
                data += chunk
                if len(data) > max_bytes:
                    break
            truncated = len(data) > max_bytes
            body = data[:max_bytes].decode(response.encoding or "utf-8", errors="replace")
            job.result = Result(status_code=response.status_code, content_type=response.headers.get("Content-Type"),
                                body=body, truncated=truncated)
            job.status = "completed"
        except (requests.RequestException, InvalidTarget, UnicodeError) as exc:
            job.status, job.error = "failed", str(exc)[:1000]
        db.session.commit()
        return True

def run_once():
    app = create_app()
    with app.app_context():
        job = Job.query.filter_by(status="queued").order_by(Job.created_at).first()
        if job:
            return process_job(job)
    return False

if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("BACKEND_LOG_LEVEL", "INFO"))
    while run_once():
        pass
