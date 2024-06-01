from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud,schemas,database,models
from .auth import get_current_user
# from app.main import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Obat)
def create_obat(obat: schemas.ObatCreate, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    db_obat = models.Obat(**obat.dict())
    db.add(db_obat)
    db.commit()
    db.refresh(db_obat)
    return db_obat

@router.get("/{obat_id}", response_model=schemas.Obat)
def read_obat(obat_id: int, db: Session = Depends(database.get_db),current_user: str = Depends(get_current_user)):
    return db.query(models.Obat).filter(models.Obat.id_obat == obat_id).first()



@router.put("/{obat_id}", response_model=schemas.Obat)
def update_obat(obat_id: int, obat: schemas.ObatUpdate, db: Session = Depends(database.get_db),current_user: str = Depends(get_current_user)):
    db_obat = db.query(models.Obat).filter(models.Obat.id_obat == obat_id).first()
    if db_obat is None:
        raise HTTPException(status_code=404, detail="Obat not found")
    for key, value in obat.dict(exclude_unset=True).items():
        setattr(db_obat, key, value)
    db.commit()
    db.refresh(db_obat)
    return db_obat

@router.delete("/{obat_id}", response_model=schemas.Obat)
def delete_obat(obat_id: int, db: Session = Depends(database.get_db),current_user: str = Depends(get_current_user)):
    db_obat = db.query(models.Obat).filter(models.Obat.id_obat == obat_id).first()
    if db_obat is None:
        raise HTTPException(status_code=404, detail="Obat not found")
    db.delete(db_obat)
    db.commit()
    return db_obat

@router.get("/", response_model=List[schemas.Obat])
def read_obat_list(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db),current_user: str = Depends(get_current_user)):
    return db.query(models.Obat).offset(skip).limit(limit).all()
