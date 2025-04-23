from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    name: str = Field(max_length=15)