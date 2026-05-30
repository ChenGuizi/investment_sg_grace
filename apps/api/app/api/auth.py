from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from app.core.security import create_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    investment_style: str = "balanced"
    risk_appetite: str = "moderate"
    horizon: str = "long-term"
    country_preference: str = "both"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterRequest) -> TokenResponse:
    # Production flow should persist the user and enforce unique email.
    password_hash = hash_password(payload.password)
    token = create_access_token(
        payload.email,
        {
            "name": payload.name,
            "investment_style": payload.investment_style,
            "risk_appetite": payload.risk_appetite,
            "horizon": payload.horizon,
            "country_preference": payload.country_preference,
            "password_configured": bool(password_hash),
        },
    )
    return TokenResponse(access_token=token)
