"""database table models"""
from app import db

class Temps(db.Model):
    """Data model for sensor reading data point."""

    __tablename__ = 'datapoint'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    pm = db.Column(
        db.Float,
        unique=False,
        nullable=False
    )
    time = db.Column(
        db.DateTime,
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return f'temp:{self.temperature}, time:{self.time}'
