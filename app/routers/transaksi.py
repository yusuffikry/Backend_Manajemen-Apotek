import logging
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
# from .. import schemas, models, database
from ..schemas.transaksi import *
from ..schemas.user import User

from ..models import TransaksiPenjualan as TransaksiPenjualanModel,DetailTransaksiPenjualan as DetailTransaksiPenjualanModel,Obat as ObatModel
from sqlalchemy.orm import Session
from ..deps import get_current_user
from ..database import get_db
from icecream import ic
# from loguru import logger

router = APIRouter()

# TransaksiPenjualan Routes
@router.post("/",  status_code=status.HTTP_201_CREATED)
def create_transaksi(transaksi: TransaksiPenjualanCreate,details :List[DetailTransaksiPenjualanCreate], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_transaksi = TransaksiPenjualanModel(**transaksi.dict())
    db.add(db_transaksi)
    db.flush()
    for detail in details:
        obat = db.query(ObatModel).filter(ObatModel.id_obat == detail.id_obat).first()
        if not obat:
            raise HTTPException(status_code=404, detail="Obat not found")
        if obat.jumlah_stok < detail.jumlah_beli:
            raise HTTPException(status_code=400, detail="Jumlah stok tidak cukup")
        
        obat.jumlah_stok -= detail.jumlah_beli
        detail.id_transaksi_penjualan = db_transaksi.id_transaksi_penjualan
        # logging.error(detail)
        db_detail = DetailTransaksiPenjualanModel(**detail.dict())
        # return db_detail
        db.add(db_detail)
        ic(db_detail)
    db.commit()
    db.refresh(db_detail)
    return StructTransaksi(transaksi=db_transaksi, details=[db_detail])
    
    # transaksi = TransaksiPenjualanModel.create_or_get(**transaksi.dict())
    # details = [DetailTransaksiPenjualanModel.create_or_get(**detail.dict()) for detail in details]
    
    # return StructTransaksi(
    #     transaksi=TransaksiPenjualanRead.from_orm(transaksi),
    #     details=[DetailTransaksiPenjualanRead.from_orm(detail) for detail in details]
    # )


@router.get("/details", response_model=List[StructTransaksi],status_code=status.HTTP_200_OK)
def read_transaksi_with_detail(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Query the database for TransaksiPenjualanModel objects
    transaksis = db.query(TransaksiPenjualanModel).offset(skip).limit(limit).all()
    
    # Log the result before processing
    logging.info(f"Before Pydantic: {transaksis}")
    
    # Create a list of details for each transaksi
    details_list = []
    for transaksi in transaksis:
        # Query the database for DetailTransaksiPenjualanModel objects related to the current transaksi
        details = db.query(DetailTransaksiPenjualanModel).filter(DetailTransaksiPenjualanModel.id_transaksi_penjualan == transaksi.id_transaksi_penjualan).all()
        
        # Add the details to the list
        details_list.append({"transaksi": transaksi, "details": details})
    
    # Return the list of dictionaries
    return details_list

@router.get("/", response_model=List[TransaksiPenjualanRead],status_code=status.HTTP_200_OK)
def read_transaksi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaksi = db.query(TransaksiPenjualanModel).offset(skip).limit(limit).all()
    return transaksi

@router.get("/{transaksi_id}", response_model=TransaksiPenjualanRead)
def read_transaksi_by_id(transaksi_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaksi = db.query(TransaksiPenjualanModel).filter(TransaksiPenjualanModel.id_transaksi_penjualan == transaksi_id).first()
    if transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    transaksi.details = db.query(DetailTransaksiPenjualanModel).filter(DetailTransaksiPenjualanModel.id_transaksi_penjualan == transaksi.id_transaksi_penjualan).all()
    return transaksi

@router.put("/{transaksi_id}", response_model=StructTransaksi,status_code=status.HTTP_200_OK)
def update_transaksi(transaksi_id: int, transaksi: TransaksiPenjualanUpdate, details: List[DetailTransaksiPenjualanUpdate], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_transaksi = db.query(TransaksiPenjualanModel).filter(TransaksiPenjualanModel.id_transaksi_penjualan == transaksi_id).first()
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")

    # Update the transaksi
    for field, value in vars(transaksi).items():
        setattr(db_transaksi, field, value) if value else None

    # Update the details
    for detail in details:
        db_detail = db.query(DetailTransaksiPenjualanModel).filter(DetailTransaksiPenjualanModel.id_transaksi_penjualan == db_transaksi.id_transaksi_penjualan).filter(DetailTransaksiPenjualanModel.id_detail_transaksi == detail.id_detail_transaksi).first()
        if db_detail is None:
            raise HTTPException(status_code=404, detail="Detail Transaksi not found")

        # Update the detail
        for field, value in vars(detail).items():
            setattr(db_detail, field, value) if value else None

    db.commit()
    return StructTransaksi(transaksi=db_transaksi, details=[db_detail],status_code=status.HTTP_200_OK)

@router.delete("/{transaksi_id}", response_model=TransaksiPenjualanRead)
def delete_transaksi(transaksi_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_transaksi = db.query(TransaksiPenjualanModel).filter(TransaksiPenjualanModel.id_transaksi_penjualan == transaksi_id).first()
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    db_detail = db.query(DetailTransaksiPenjualanModel).filter(DetailTransaksiPenjualanModel.id_transaksi_penjualan == db_transaksi.id_transaksi_penjualan).all()
    for detail in db_detail:
        db.delete(detail)
    db.delete(db_transaksi)
    
    db.commit()
    return db_transaksi

# # DetailTransaksiPenjualan Routes
# @router.post("/detail-", response_model=DetailTransaksiPenjualan, status_code=status.HTTP_201_CREATED)
# def create_detail_transaksi(detail: DetailTransaksiPenjualanCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     db_detail = DetailTransaksiPenjualan(**detail.dict())
#     db.add(db_detail)
#     db.commit()
#     db.refresh(db_detail)
#     return db_detail

# @router.get("/detail-", response_model=List[DetailTransaksiPenjualan])
# def read_detail_transaksi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     details = db.query(DetailTransaksiPenjualan).offset(skip).limit(limit).all()
#     return details

# @router.get("/detail-{detail_id}", response_model=DetailTransaksiPenjualan)
# def read_detail_transaksi_by_id(detail_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     detail = db.query(DetailTransaksiPenjualan).filter(DetailTransaksiPenjualan.id_detail_transaksi == detail_id).first()
#     if detail is None:
#         raise HTTPException(status_code=404, detail="Detail Transaksi not found")
#     return detail

# @router.put("/detail-{detail_id}", response_model=DetailTransaksiPenjualan)
# def update_detail_transaksi(detail_id: int, detail: DetailTransaksiPenjualanUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     db_detail = db.query(DetailTransaksiPenjualan).filter(DetailTransaksiPenjualan.id_detail_transaksi == detail_id).first()
#     if db_detail is None:
#         raise HTTPException(status_code=404, detail="Detail Transaksi not found")
#     for var, value in vars(detail).items():
#         setattr(db_detail, var, value) if value else None
#     db.commit()
#     return db_detail

# @router.delete("/detail-{detail_id}", response_model=DetailTransaksiPenjualan)
# def delete_detail_transaksi(detail_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     db_detail = db.query(DetailTransaksiPenjualan).filter(DetailTransaksiPenjualan.id_detail_transaksi == detail_id).first()
#     if db_detail is None:
#         raise HTTPException(status_code=404, detail="Detail Transaksi not found")
#     db.delete(db_detail)
#     db.commit()
#     return db_detail