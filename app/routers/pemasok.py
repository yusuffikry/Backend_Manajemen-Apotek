from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database
from .auth import get_current_user  # Assuming this is the function to get the current user

router = APIRouter()

@router.post("/pemasok/", response_model=schemas.Pemasok, status_code=status.HTTP_201_CREATED)
def create_pemasok(pemasok: schemas.PemasokCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_pemasok = models.Pemasok(**pemasok.dict())
    db.add(db_pemasok)
    db.commit()
    db.refresh(db_pemasok)
    return db_pemasok

@router.get("/pemasok/", response_model=List[schemas.Pemasok])
def read_pemasok(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    pemasok = db.query(models.Pemasok).offset(skip).limit(limit).all()
    return pemasok

@router.get("/pemasok/{pemasok_id}", response_model=schemas.Pemasok)
def read_pemasok_by_id(pemasok_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    pemasok = db.query(models.Pemasok).filter(models.Pemasok.id_pemasok == pemasok_id).first()
    if pemasok is None:
        raise HTTPException(status_code=404, detail="Pemasok not found")
    return pemasok

@router.put("/pemasok/{pemasok_id}", response_model=schemas.Pemasok)
def update_pemasok(pemasok_id: int, pemasok: schemas.PemasokUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_pemasok = db.query(models.Pemasok).filter(models.Pemasok.id_pemasok == pemasok_id).first()
    if db_pemasok is None:
        raise HTTPException(status_code=404, detail="Pemasok not found")
    for var, value in vars(pemasok).items():
        setattr(db_pemasok, var, value) if value else None
    db.commit()
    return db_pemasok

@router.delete("/pemasok/{pemasok_id}", response_model=schemas.Pemasok)
def delete_pemasok(pemasok_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_pemasok = db.query(models.Pemasok).filter(models.Pemasok.id_pemasok == pemasok_id).first()
    if db_pemasok is None:
        raise HTTPException(status_code=404, detail="Pemasok not found")
    db.delete(db_pemasok)
    db.commit()
    return db_pemasok