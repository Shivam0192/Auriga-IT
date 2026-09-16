from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


def utc_now():
    return datetime.now(timezone.utc)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    target_amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="INR")
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)
    participants = db.relationship("Participant", backref="pool", cascade="all, delete-orphan", lazy=True)


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    contributions = db.relationship("Contribution", backref="participant", cascade="all, delete-orphan", lazy=True)


class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participant.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)


class SettlementPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"), nullable=False, unique=True)
    transfers = db.Column(db.Text, nullable=False, default="[]")
    updated_at = db.Column(db.DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)


class PoolRefund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participant.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)