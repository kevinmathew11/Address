from pydantic import BaseModel, validator
from typing import Optional, List
from fastapi import status, HTTPException


# Create AddressBook Schema (Pydantic Model)
class AddressCreate(BaseModel):
    name: str
    city: str
    state: str
    latitude: float
    longitude: float

    @validator('latitude')
    def validate_latitude(cls, v):
        if (v > 90.0) or (v < -90.0):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="latitude should be between 90 and -90.")
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if (v > 180.0) or (v < -180.0):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="longitude should be between -180 and 180.")
        return v
class AddressView(BaseModel):
    id: int
    name: str
    city: str
    state: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True
