from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Market = Literal["US", "SG"]
Recommendation = Literal["BUY", "HOLD", "SELL"]
Impact = Literal["Positive", "Neutral", "Negative"]
RiskLevel = Literal["Low", "Medium", "High"]


class Citation(BaseModel):
    title: str
    url: str
    publisher: str
    published_at: datetime | None = None


class Evidence(BaseModel):
    claim: str
    citations: list[Citation] = Field(default_factory=list)


class Score(BaseModel):
    value: float = Field(ge=0, le=100)
    label: str
    explanation: str
