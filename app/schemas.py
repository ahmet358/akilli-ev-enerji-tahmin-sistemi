from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        normalized = " ".join(value.strip().split())
        if len(normalized) < 2:
            raise ValueError("Ad soyad alanı en az iki karakter olmalıdır.")
        return normalized


class EnergyPredictionInput(BaseModel):
    temperature: float = Field(..., ge=-20, le=55)
    humidity: float = Field(..., ge=0, le=100)
    hour: int = Field(..., ge=0, le=23)
    day_of_week: int = Field(..., ge=0, le=6)
    month: int = Field(..., ge=1, le=12)
    active_appliances: int = Field(..., ge=0, le=40)
    lights_usage: int = Field(..., ge=0, le=20)
    heating_status: bool
    cooling_status: bool
    household_size: int = Field(..., ge=1, le=12)
    weather_condition: str = Field(..., min_length=3, max_length=40)

    @field_validator("weather_condition")
    @classmethod
    def validate_weather_condition(cls, value: str) -> str:
        allowed_values = {"gunesli", "bulutlu", "yagmurlu", "karli", "ruzgarli"}
        normalized = value.strip().lower()
        if normalized not in allowed_values:
            raise ValueError("Hava durumu seçimi geçerli değil.")
        return normalized

    def to_feature_dict(self) -> dict:
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "hour": self.hour,
            "day_of_week": self.day_of_week,
            "month": self.month,
            "active_appliances": self.active_appliances,
            "lights_usage": self.lights_usage,
            "heating_status": int(self.heating_status),
            "cooling_status": int(self.cooling_status),
            "household_size": self.household_size,
            "weather_condition": self.weather_condition,
        }

