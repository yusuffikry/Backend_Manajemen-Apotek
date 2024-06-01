from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from .. import schemas, models, database
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter()

# TransaksiPenjualan Routes
@router.post("/transaksi/", response_model=schemas.TransaksiPenjualan, status_code=status.HTTP_201_CREATED)
def create_transaksi(transaksi: schemas.TransaksiPenjualanCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_transaksi = models.TransaksiPenjualan(**transaksi.dict())
    db.add(db_transaksi)
    db.commit()
    db.refresh(db_transaksi)
    return db_transaksi

@router.get("/transaksi/", response_model=List[schemas.TransaksiPenjualan])
def read_transaksi(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    transaksi = db.query(models.TransaksiPenjualan).offset(skip).limit(limit).all()
    return transaksi

@router.get("/transaksi/{transaksi_id}", response_model=schemas.TransaksiPenjualan)
def read_transaksi_by_id(transaksi_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    transaksi = db.query(models.TransaksiPenjualan).filter(models.TransaksiPenjualan.id_transaksi_penjualan == transaksi_id).first()
    if transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    return transaksi

@router.put("/transaksi/{transaksi_id}", response_model=schemas.TransaksiPenjualan)
def update_transaksi(transaksi_id: int, transaksi: schemas.TransaksiPenjualanUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_transaksi = db.query(models.TransaksiPenjualan).filter(models.TransaksiPenjualan.id_transaksi_penjualan == transaksi_id).first()
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    for var, value in vars(transaksi).items():
        setattr(db_transaksi, var, value) if value else None
    db.commit()
    return db_transaksi

@router.delete("/transaksi/{transaksi_id}", response_model=schemas.TransaksiPenjualan)
def delete_transaksi(transaksi_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_transaksi = db.query(models.TransaksiPenjualan).filter(models.TransaksiPenjualan.id_transaksi_penjualan == transaksi_id).first()
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    db.delete(db_transaksi)
    db.commit()
    return db_transaksi

# DetailTransaksiPenjualan Routes
@router.post("/detail-transaksi/", response_model=schemas.DetailTransaksiPenjualan, status_code=status.HTTP_201_CREATED)
def create_detail_transaksi(detail: schemas.DetailTransaksiPenjualanCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_detail = models.DetailTransaksiPenjualan(**detail.dict())
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail

@router.get("/detail-transaksi/", response_model=List[schemas.DetailTransaksiPenjualan])
def read_detail_transaksi(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    details = db.query(models.DetailTransaksiPenjualan).offset(skip).limit(limit).all()
    return details

@router.get("/detail-transaksi/{detail_id}", response_model=schemas.DetailTransaksiPenjualan)
def read_detail_transaksi_by_id(detail_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    detail = db.query(models.DetailTransaksiPenjualan).filter(models.DetailTransaksiPenjualan.id_detail_transaksi == detail_id).first()
    if detail is None:
        raise HTTPException(status_code=404, detail="Detail Transaksi not found")
    return detail

@router.put("/detail-transaksi/{detail_id}", response_model=schemas.DetailTransaksiPenjualan)
def update_detail_transaksi(detail_id: int, detail: schemas.DetailTransaksiPenjualanUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_detail = db.query(models.DetailTransaksiPenjualan).filter(models.DetailTransaksiPenjualan.id_detail_transaksi == detail_id).first()
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Detail Transaksi not found")
    for var, value in vars(detail).items():
        setattr(db_detail, var, value) if value else None
    db.commit()
    return db_detail

@router.delete("/detail-transaksi/{detail_id}", response_model=schemas.DetailTransaksiPenjualan)
def delete_detail_transaksi(detail_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_detail = db.query(models.DetailTransaksiPenjualan).filter(models.DetailTransaksiPenjualan.id_detail_transaksi == detail_id).first()
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Detail Transaksi not found")
    db.delete(db_detail)
    db.commit()
    return db_detail