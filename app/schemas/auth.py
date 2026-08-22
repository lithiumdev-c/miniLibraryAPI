from pydantic import AwareDatetime, BaseModel, EmailStr, ConfigDict
from datetime import datetime

class CreateUserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr

    created_at: AwareDatetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
