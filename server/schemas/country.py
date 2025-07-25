from pydantic import BaseModel


class CountryBase(BaseModel):
    name: str
    iso_code: str


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: str | None = None
    iso_code: str | None = None


class CountryResponse(CountryBase):
    id: int

    class Config:
        from_attributes = True 