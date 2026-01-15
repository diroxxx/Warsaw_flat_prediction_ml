"""
Pydantic schema for input data validation and serialization.
"""

from enum import Enum
from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


class District(str, Enum):
    """Warsaw districts"""
    BEMOWO = "Bemowo"
    BIALOLEKA = "Białołęka"
    BIELANY = "Bielany"
    MOKOTOW = "Mokotów"
    OCHOTA = "Ochota"
    PRAGA = "Praga"
    PRAGA_POLUDNIE = "Praga-Południe"
    PRAGA_POLNOC = "Praga-Północ"
    TARGOWEK = "Targówek"
    URSUS = "Ursus"
    URSYNOW = "Ursynów"
    WAWER = "Wawer"
    WILANOW = "Wilanów"
    WOLA = "Wola"
    WLOCHY = "Włochy"
    SRODMIESCIE = "Śródmieście"
    ZOLIBORZ = "Żoliborz"


class ConstructionStatus(str, Enum):
    """Construction status options"""
    READY = "do zamieszkania"
    DEVELOPER = "do wykończenia"
    RENOVATION = "do remontu"


class Market(str, Enum):
    """Market type options"""
    PRIMARY = "pierwotny"
    SECONDARY = "wtórny"

class PredictionInput(BaseModel):
    """Schema for input data used in price prediction."""
    district: District = Field(..., json_schema_extra={"example": District.MOKOTOW.value})
    surface: float = Field(..., ge=14, le=102, json_schema_extra={"example": 60.5})
    rooms_num: int = Field(..., ge=1, le=6, json_schema_extra={"example": 3})
    construction_status: ConstructionStatus = (
        Field(..., json_schema_extra={"example": ConstructionStatus.READY.value}))
    market: Market = Field(..., json_schema_extra={"example": Market.SECONDARY.value})
    build_year: int = Field(..., ge=1900, le=2025, json_schema_extra={"example": 2005})
    floor_no: int = Field(..., ge=0, le=10, json_schema_extra={"example": 2})
    building_floors_num: int = Field(..., ge=1, le=50, json_schema_extra={"example": 5})
    transit_dur_m: float = Field(..., ge=4.9, le=230, json_schema_extra={"example": 30.0})

    @field_validator("building_floors_num")
    def validate_floors(cls, v, info: ValidationInfo):
        """Ensure total_floors is greater than or equal to floor."""
        if "floor_no" in info.data and v < info.data["floor_no"]:
            raise ValueError("building_floors_num must be >= floor")
        return v
