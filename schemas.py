from pydantic import BaseModel


class Country(BaseModel):
    id: int
    label: str

    class Config:
        orm_mode = True
