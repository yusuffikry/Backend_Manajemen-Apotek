from sqlalchemy.orm import Session
from . import models, schemas

def get_obat(db: Session, obat_id: int):
    return db.query(models.Obat).filter(models.Obat.id_obat == obat_id).first()

def create_obat(db: Session, obat: schemas.ObatCreate):
    db_obat = models.Obat(**obat.dict())
    db.add(db_obat)
    db.commit()
    db.refresh(db_obat)
    return db_obat

def update_obat(db: Session, obat_id: int, obat: schemas.ObatUpdate):
    db_obat = db.query(models.Obat).filter(models.Obat.id_obat == obat_id).first()
    if db_obat:
        for key, value in obat.dict(exclude_unset=True).items():
            setattr(db_obat, key, value)
        db.commit()
        db.refresh(db_obat)
    return db_obat

def delete_obat(db: Session, obat_id: int):
    db_obat = db.query(models.Obat).filter(models.Obat.id_obat == obat_id).first()
    if db_obat:
        db.delete(db_obat)
        db.commit()
    return db_obat

def get_obat_list(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Obat).offset(skip).limit(limit).all()



def get_pelanggan(db: Session, pelanggan_id: int):
    return db.query(models.Pelanggan).filter(models.Pelanggan.id_pelanggan == pelanggan_id).first()

def create_pelanggan(db: Session, pelanggan: schemas.PelangganCreate):
    db_pelanggan = models.Pelanggan(**pelanggan.dict())
    db.add(db_pelanggan)
    db.commit()
    db.refresh(db_pelanggan)
    return db_pelanggan

def update_pelanggan(db: Session, pelanggan_id: int, pelanggan: schemas.PelangganUpdate):
    db_pelanggan = db.query(models.Pelanggan).filter(models.Pelanggan.id_pelanggan == pelanggan_id).first()
    if db_pelanggan:
        for key, value in pelanggan.dict(exclude_unset=True).items():
            setattr(db_pelanggan, key, value)
        db.commit()
        db.refresh(db_pelanggan)
    return db_pelanggan

def delete_pelanggan(db: Session, pelanggan_id: int):
    db_pelanggan = db.query(models.Pelanggan).filter(models.Pelanggan.id_pelanggan == pelanggan_id).first()
    if db_pelanggan:
        db.delete(db_pelanggan)
        db.commit()
    return db_pelanggan

def get_pelanggan_list(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Pelanggan).offset(skip).limit(limit).all()
