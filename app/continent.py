from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter()

@router.post('/create-continent', status_code=status.HTTP_201_CREATED)
def create_country(payload : schemas.ContinentCreate, db: Session = Depends(get_db)):
    existing_continent = db.query(models.Continent).filter(models.Continent.continent_id == payload.continent_id).first()
    if existing_continent:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Continent already exists.")

    new_continent = models.Continent(**payload.dict())
    try:
        db.add(new_continent)
        db.commit()
        db.refresh(new_continent)
        return {"status": "success", "message": "Continent created successfully!", "data": new_continent}
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


@router.get('/continent/{country_name}')
def get_country_by_id(continent_name: str, db: Session = Depends(get_db)):
    continent = db.query(models.Country).filter(models.Continent.continent_name == continent_name).first()
    if not continent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    return {"status": "success", "message": "Continent found successfully!", "data": continent}

@router.get('/continents')
def get_countries(db: Session = Depends(get_db)):
    continents = db.query(models.Continent).all()
    if not continents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No countries found")
    return {"status": "success", "message": "Countries found successfully!", "data": continents}