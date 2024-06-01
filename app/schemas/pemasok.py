from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class PemasokBase(BaseModel):
    nama_perusahaan: str
    nomor_telepon: str

class PemasokCreate(PemasokBase):
    pass

class Pemasok(PemasokBase):
    id_pemasok: int
    class Config:
        from_attributes = True

class PemasokUpdate(BaseModel):
    nama_perusahaan: Optional[str] = None
    nomor_telepon: Optional[str] = None
