from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class TransaksiPenjualanBase(BaseModel):
    tanggal_transaksi: date
    total_pembayaran: float

class TransaksiPenjualanCreate(TransaksiPenjualanBase):
    pass

class TransaksiPenjualanRead(TransaksiPenjualanBase):
    id_transaksi_penjualan: int

    class Config:
        from_attributes = True

class TransaksiPenjualanUpdate(BaseModel):
    tanggal_transaksi: Optional[date] = None
    total_pembayaran: Optional[float] = None

class DetailTransaksiPenjualanBase(BaseModel):
    id_obat: int
    jumlah_beli: int
    harga_satuan: float

class DetailTransaksiPenjualanCreate(DetailTransaksiPenjualanBase):
    id_transaksi_penjualan: Optional[int] = None
    pass

class DetailTransaksiPenjualanRead(DetailTransaksiPenjualanBase):
    id_detail_transaksi: int

    class Config:
        from_attributes = True

class DetailTransaksiPenjualanUpdate(DetailTransaksiPenjualanBase):
    id_detail_transaksi: Optional[int] = None
    id_obat: Optional[int] = None
    jumlah_beli: Optional[int] = None
    harga_satuan: Optional[float] = None

class StructTransaksi(BaseModel):
    transaksi: TransaksiPenjualanRead
    details: List[DetailTransaksiPenjualanRead]
    # details: List[DetailTransaksiPenjualan]