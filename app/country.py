from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter()

@router.post('/create-country', status_code=status.HTTP_201_CREATED)
def create_country(payload : schemas.CountryCreate, db: Session = Depends(get_db)):
    existing_country = db.query(models.Country).filter(models.Country.country_id == payload.country_id).first()
    if existing_country:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Country already exists.")

    new_country = models.Country(**payload.dict())
    try:
        db.add(new_country)
        db.commit()
        db.refresh(new_country)
        return {"status": "success", "message": "Country created successfully!", "data": new_country}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A database integrity error occurred. Please verify your data."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )



@router.get('/country/{country_name}')
def get_country_by_id(country_name: str, db: Session = Depends(get_db)):
    country = db.query(models.Country).filter(models.Country.country_name == country_name).first()
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    return {"status": "success", "message": "Country found successfully!", "data": country}


@router.get('/countries')
def get_countries(continent_name: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Country)
    if continent_name:
        query = query.join(models.Continent).filter(models.Continent.continent_name == continent_name)
    countries = query.all()

    if not countries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No countries found")
    return {"status": "success", "data": countries}


@router.get('/countries/{continent_name}')
def get_countries_by_continent(continent_name: str, db: Session = Depends(get_db)):
    countries = (
        db.query(models.Country)
        .join(models.Continent, models.Country.continent == models.Continent.continent_id)
        .filter(models.Continent.continent_name == continent_name)
        .all()
    )

    if not countries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No countries found for the given continent")

    return {
        "status": "success",
        "message": f"Countries found successfully for continent {continent_name}!",
        "data": countries
    }
