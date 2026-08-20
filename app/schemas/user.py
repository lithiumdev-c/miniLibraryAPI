from pydantic import BaseModel, EmailStr

class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr

class UserResponseSchema(BaseModel):
    id: int