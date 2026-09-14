from flask import Blueprint, jsonify, request
from . import db
from .models import Job
from .validation import InvalidTarget, validate_target_url

api = Blueprint("api", __name__)

@api.post("/jobs")
def create_job():
    payload = request.get_json(silent=True) or {}
    try:
        target = validate_target_url(payload.get("target_url"))
    except InvalidTarget as exc:
        return jsonify({"error": str(exc)}), 400
    job = Job(target_url=target)
    db.session.add(job)
    db.session.commit()
    return jsonify(job.as_dict()), 202

@api.get("/jobs")
def list_jobs():
    limit = min(max(request.args.get("limit", 25, type=int), 1), 100)
    jobs = Job.query.order_by(Job.created_at.desc()).limit(limit).all()
    return jsonify({"items": [job.as_dict() for job in jobs]})

@api.get("/jobs/<int:job_id>")
def get_job(job_id):
    job = db.session.get(Job, job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404
    return jsonify(job.as_dict())
