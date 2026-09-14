from datetime import datetime, timezone
from . import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_url = db.Column(db.String(2048), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="queued", index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    error = db.Column(db.String(1000))
    result = db.relationship("Result", backref="job", uselist=False, cascade="all, delete-orphan")

    def as_dict(self):
        return {"id": self.id, "target_url": self.target_url, "status": self.status,
                "error": self.error, "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat(),
                "result": self.result.as_dict() if self.result else None}

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False, unique=True)
    status_code = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String(255))
    body = db.Column(db.Text, nullable=False)
    truncated = db.Column(db.Boolean, default=False, nullable=False)
    fetched_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def as_dict(self):
        return {"status_code": self.status_code, "content_type": self.content_type,
                "body": self.body, "truncated": self.truncated,
                "fetched_at": self.fetched_at.isoformat()}
