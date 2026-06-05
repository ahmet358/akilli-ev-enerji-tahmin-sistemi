from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(180), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    predictions = relationship("PredictionRecord", back_populates="user", cascade="all, delete-orphan")
    actions = relationship("UserAction", back_populates="user", cascade="all, delete-orphan")


class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    hour = Column(Integer, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    active_appliances = Column(Integer, nullable=False)
    lights_usage = Column(Integer, nullable=False)
    heating_status = Column(Boolean, nullable=False)
    cooling_status = Column(Boolean, nullable=False)
    household_size = Column(Integer, nullable=False)
    weather_condition = Column(String(40), nullable=False)
    predicted_energy_consumption = Column(Float, nullable=False)
    model_used = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    user = relationship("User", back_populates="predictions")


class UserAction(Base):
    __tablename__ = "user_actions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    action_type = Column(String(80), nullable=False)
    action_description = Column(String(260), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    user = relationship("User", back_populates="actions")

