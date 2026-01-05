from pydantic import BaseModel


class PredictionInput(BaseModel):
    district: str
    surface: float
    rooms_num: int
    construction_status: str
    market: str
    build_year: int
    floor: int
    total_floors: int
    transit_dur_s: float