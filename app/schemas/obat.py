from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

class ObatBase(BaseModel):
    nama_obat: str
    jenis_obat: str
    harga: float
    jumlah_stok: int
    # tanggal_kadaluwarsa: date

class ObatCreate(ObatBase):
    pass

class ObatUpdate(BaseModel):
    nama_obat: Optional[str] = None
    jenis_obat: Optional[str] = None
    harga: Optional[float] = None
    jumlah_stok: Optional[int] = None
    # tanggal_kadaluwarsa: Optional[date] = None

class Obat(ObatBase):
    id_obat: int
    class Config:
        from_attributes = True