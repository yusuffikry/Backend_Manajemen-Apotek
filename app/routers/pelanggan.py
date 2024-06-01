from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.Pelanggan)
def create_pelanggan(pelanggan: schemas.PelangganCreate, db: Session = Depends(database.get_db)):
    return crud.create_pelanggan(db=db, pelanggan=pelanggan)

@router.get("/{pelanggan_id}", response_model=schemas.Pelanggan)
def read_pelanggan(pelanggan_id: int, db: Session = Depends(database.get_db)):
    db_pelanggan = crud.get_pelanggan(db, pelanggan_id=pelanggan_id)
    if db_pelanggan is None:
        raise HTTPException(status_code=404, detail="Pelanggan not found")
    return db_pelanggan

@router.put("/{pelanggan_id}", response_model=schemas.Pelanggan)
def update_pelanggan(pelanggan_id: int, pelanggan: schemas.PelangganUpdate, db: Session = Depends(database.get_db)):
    db_pelanggan = crud.get_pelanggan(db, pelanggan_id=pelanggan_id)
    if db_pelanggan is None:
        raise HTTPException(status_code=404, detail="Pelanggan not found")
    return crud.update_pelanggan(db=db, pelanggan_id=pelanggan_id, pelanggan=pelanggan)

@router.delete("/{pelanggan_id}", response_model=schemas.Pelanggan)
def delete_pelanggan(pelanggan_id: int, db: Session = Depends(database.get_db)):
    db_pelanggan = crud.get_pelanggan(db, pelanggan_id=pelanggan_id)
    if db_pelanggan is None:
        raise HTTPException(status_code=404, detail="Pelanggan not found")
    return crud.delete_pelanggan(db=db, pelanggan_id=pelanggan_id)

@router.get("/", response_model=List[schemas.Pelanggan])
def read_pelanggan_list(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_pelanggan_list(db, skip=skip, limit=limit)
