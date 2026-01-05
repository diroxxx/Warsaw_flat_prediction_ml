from pydantic import BaseModel

class TrainInput(BaseModel):
    district: str
    price: float
    surface: float
    rooms_num: int
    construction_status: str
    market: str
    build_year: int
    floor: int
    total_floors: int
    transit_dur_s: float