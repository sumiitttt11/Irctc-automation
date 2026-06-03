import json
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, field_validator, model_validator


# ─── Pydantic models ──────────────────────────────────────────────────────────

class TrainOption(BaseModel):
    number: str
    classes: List[str]

    @field_validator("classes")
    @classmethod
    def valid_classes(cls, v):
        allowed = {"SL", "3A", "2A", "1A", "CC", "EC"}
        for c in v:
            if c not in allowed:
                raise ValueError(f"Unknown class '{c}'. Allowed: {allowed}")
        return v


class PaymentConfig(BaseModel):
    method: str = "UPI"
    saved_upi_id: str = ""

    @field_validator("method")
    @classmethod
    def valid_method(cls, v):
        if v not in ("UPI","EWALLET", "CARD", "NETBANKING", "MANUAL"):
            raise ValueError(f"Unknown payment method '{v}'")
        return v


class RouteConfig(BaseModel):
    from_station: str
    to_station: str
    journey_date: str
    fire_time: str
    quota: str = "TATKAL"
    trains: List[TrainOption]
    payment: PaymentConfig = PaymentConfig()

    @field_validator("journey_date")
    @classmethod
    def valid_date(cls, v):
        import re
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", v):
            raise ValueError(f"journey_date must be DD/MM/YYYY, got: '{v}'")
        return v

    @field_validator("fire_time")
    @classmethod
    def valid_time(cls, v):
        import re
        if not re.match(r"^\d{2}:\d{2}:\d{2}$", v):
            raise ValueError(f"fire_time must be HH:MM:SS, got: '{v}'")
        return v

    @model_validator(mode="after")
    def at_least_one_train(self):
        if not self.trains:
            raise ValueError("routes.json must have at least one train in 'trains' list")
        return self


class PassengerEntry(BaseModel):
    name: str
    age: int
    gender: str
    berth_preference: str = "NO PREFERENCE"

    @field_validator("gender")
    @classmethod
    def valid_gender(cls, v):
        if v.upper() not in ("M", "F", "T"):
            raise ValueError(f"gender must be M/F/T, got: '{v}'")
        return v.upper()

    @field_validator("age")
    @classmethod
    def valid_age(cls, v):
        if not (1 <= v <= 125):
            raise ValueError(f"age out of range: {v}")
        return v


class PassengersConfig(BaseModel):
    auto_upgrade: bool = True
    passengers: List[PassengerEntry]

    @model_validator(mode="after")
    def at_least_one_passenger(self):
        if not self.passengers:
            raise ValueError("passengers.json must contain at least one passenger")
        if len(self.passengers) > 6:
            raise ValueError("IRCTC max 6 passengers per booking")
        return self


# ─── Loader ───────────────────────────────────────────────────────────────────

def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_and_validate_route(path: str = "config/routes.json") -> RouteConfig:
    data = load_json(path)
    try:
        return RouteConfig(**data)
    except Exception as e:
        raise SystemExit(f"\n❌ Config error in {path}:\n{e}\n")


def load_and_validate_passengers(path: str = "config/passengers.json") -> PassengersConfig:
    data = load_json(path)
    try:
        return PassengersConfig(**data)
    except Exception as e:
        raise SystemExit(f"\n❌ Config error in {path}:\n{e}\n")
