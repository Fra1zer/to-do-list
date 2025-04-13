from pydantic import BaseModel, Field


class CreateTask(BaseModel):
    name: str = Field(max_length=25)
    description: str | None = Field(max_length=50, default=None)
    status: bool = False
