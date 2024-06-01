from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import database
from ..models import Pemasok as PemasokModel
from ..schemas.pemasok import *
from ..schemas.user import User
from ..deps import get_current_user

router = APIRouter()

@router.post("/", response_model=Pemasok, status_code=status.HTTP_201_CREATED)
def create_pemasok(pemasok: PemasokCreate, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    db_pemasok = PemasokModel(**pemasok.dict())
    db.add(db_pemasok)
    db.commit()
    db.refresh(db_pemasok)
    return db_pemasok

@router.get("/", response_model=List[Pemasok],status_code=status.HTTP_200_OK)
def read_pemasok(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    pemasok = db.query(PemasokModel).offset(skip).limit(limit).all()
    return pemasok

@router.get("/{pemasok_id}", response_model=Pemasok,status_code=status.HTTP_200_OK)
def read_pemasok_by_id(pemasok_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    pemasok = db.query(PemasokModel).filter(PemasokModel.id_pemasok == pemasok_id).first()
    if pemasok is None:
        raise HTTPException(status_code=404, detail="Pemasok not found")
    return pemasok

@router.put("/{pemasok_id}", response_model=Pemasok,status_code=status.HTTP_200_OK)
def update_pemasok(pemasok_id: int, pemasok: PemasokUpdate, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    db_pemasok = db.query(PemasokModel).filter(PemasokModel.id_pemasok == pemasok_id).first()
    if db_pemasok is None:
        raise HTTPException(status_code=404, detail="Pemasok not found")
    for var, value in vars(pemasok).items():
        setattr(db_pemasok, var, value) if value else None
    db.commit()
    return db_pemasok

@router.delete("/{pemasok_id}", response_model=Pemasok,status_code=status.HTTP_200_OK)
def delete_pemasok(pemasok_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    db_pemasok = db.query(PemasokModel).filter(PemasokModel.id_pemasok == pemasok_id).first()
    if db_pemasok is None:
        raise HTTPException(status_code=404, detail="Pemasok not found")
    db.delete(db_pemasok)
    db.commit()
    return db_pemasok