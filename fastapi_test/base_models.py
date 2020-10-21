from pydantic import BaseModel, Field


class PostIn(BaseModel):
    inp: str = Field(...,
                     description="Enter description here")


class PostOut(BaseModel):
    out: str = Field(..., description="Enter description here")
