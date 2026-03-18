from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any


class HarvestSession(BaseModel):

    userId: str

    threeInOneTotalPieces: int
    fourInOneTotalPieces: int
    fiveInOneTotalPieces: int
    sardinesTotalPieces: int

    totalPiecesOfHarvest: int
    totalWeightOfHarvest: float

    timestamp: datetime

    geminiForecastRemarks: str | None = None
    geminiForecastedData: Dict[str, Any] | None = None