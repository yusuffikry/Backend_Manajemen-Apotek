from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# Base models for user management
class UserBase(BaseModel):
    nama_user: str
    role: int
    email: str
    alamat: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id_user: int
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    nama_user: Optional[str] = None
    role: Optional[int] = None
    email: Optional[str] = None
    alamat: Optional[str] = None
    password: Optional[str] = None

# Authentication models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

class UserLogin(BaseModel):
    username: str
    password: str
    
class TokenVerify(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    valid: bool

# Models for managing "Obat" (Medicine)
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
        orm_mode = True

# Models for managing "Pelanggan" (Customer)
class PelangganBase(BaseModel):
    nama_pelanggan: str
    alamat: str
    nomor_telepon: str

class PelangganCreate(PelangganBase):
    pass

class PelangganUpdate(BaseModel):
    nama_pelanggan: Optional[str] = None
    alamat: Optional[str] = None
    nomor_telepon: Optional[str] = None

class Pelanggan(PelangganBase):
    id_pelanggan: int
    class Config:
        orm_mode = True

# Models for managing "Pemasok" (Supplier)
class PemasokBase(BaseModel):
    nama_pemasok: str
    alamat: str
    telepon: str

class PemasokCreate(PemasokBase):
    pass

class Pemasok(PemasokBase):
    id_pemasok: int
    class Config:
        orm_mode = True

class PemasokUpdate(BaseModel):
    nama_pemasok: Optional[str] = None
    alamat: Optional[str] = None
    telepon: Optional[str] = None

# Models for managing sales transactions
class TransaksiPenjualanBase(BaseModel):
    tanggal_transaksi: date
    total_pembayaran: float

class TransaksiPenjualanCreate(TransaksiPenjualanBase):
    pass

class TransaksiPenjualan(TransaksiPenjualanBase):
    id_transaksi_penjualan: int
    class Config:
        orm_mode = True

class TransaksiPenjualanUpdate(BaseModel):
    tanggal_transaksi: Optional[date] = None
    total_pembayaran: Optional[float] = None

class DetailTransaksiPenjualanBase(BaseModel):
    id_transaksi_penjualan: int
    id_obat: int
    jumlah_beli: int
    harga_satuan: float

class DetailTransaksiPenjualanCreate(DetailTransaksiPenjualanBase):
    pass

class DetailTransaksiPenjualan(DetailTransaksiPenjualanBase):
    id_detail_transaksi: int
    class Config:
        orm_mode = True

class DetailTransaksiPenjualanUpdate(BaseModel):
    id_transaksi_penjualan: Optional[int] = None
    id_obat: Optional[int] = None
    jumlah_beli: Optional[int] = None
    harga_satuan: Optional[float] = None
    harga_satuan: Optional[float] = None