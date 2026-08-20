from pydantic import BaseModel, ConfigDict

class BookBaseSchema(BaseModel):
    title: str
    description: str
    author: str

class BookUpdateSchema(BaseModel):
    title: str | None
    description: str | None
    author: str | None

class BookCreateSchema(BookBaseSchema):
    pass

    model_config = ConfigDict(from_attributes=True)

class BookResponseSchema(BookBaseSchema):
    id: int