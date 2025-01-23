from pydantic import BaseModel
from typing import List

class CountryResponse(BaseModel):
    country_id: int | None = None
    country_name: str
    capital: str
    area: float
    population: int
    language: str
    continent : int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class ListCountryResponse(BaseModel):
    status: str
    result: int
    countries : List[CountryResponse]


class CountryCreate(BaseModel):
    country_id : int
    country_name: str
    capital: str
    area: float
    population: int
    language: str
    continent: int

    class Config:
        orm_mode = True

class ContinentResponse(BaseModel):
    continent_id: int | None = None
    continent_name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class ContinentListResponse(BaseModel):
    status: str
    result: int
    continents : List[ContinentResponse]

class ContinentCreate(BaseModel):
    continent_id : int
    continent_name: str

    class Config:
        orm_mode = True


