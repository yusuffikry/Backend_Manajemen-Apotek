# coding: utf-8
from sqlalchemy import Column, Date, Float, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AkunToken(Base):
    __tablename__ = 'akun_token'

    Id = Column(INTEGER(11), primary_key=True)
    Email = Column(String(50), nullable=False)
    Password = Column(Text, nullable=False)


class Obat(Base):
    __tablename__ = 'obat'

    id_obat = Column(INTEGER(11), primary_key=True)
    nama_obat = Column(String(255))
    jenis_obat = Column(String(255))
    harga = Column(Float(asdecimal=True))
    jumlah_stok = Column(INTEGER(11))
    tanggal_kadaluwarsa = Column(Date)


class Pelanggan(Base):
    __tablename__ = 'pelanggan'

    id_pelanggan = Column(INTEGER(11), primary_key=True)
    nama_pelanggan = Column(String(255))
    alamat = Column(String(255))
    nomor_telepon = Column(String(255))


class Pemasok(Base):
    __tablename__ = 'pemasok'

    id_pemasok = Column(INTEGER(11), primary_key=True)
    nama_perusahaan = Column(String(255))
    nomor_telepon = Column(String(255))


class TransaksiPenjualan(Base):
    __tablename__ = 'transaksi_penjualan'

    id_transaksi_penjualan = Column(INTEGER(11), primary_key=True)
    tanggal_transaksi = Column(Date)
    total_pembayaran = Column(Float(asdecimal=True))
    status = Column(INTEGER(11), nullable=False)


class User(Base):
    __tablename__ = 'user'

    id_user = Column(INTEGER(11), primary_key=True)
    nama_user = Column(String(255))
    role = Column(INTEGER(11))
    email = Column(String(255))
    password = Column(String(255), nullable=False)
    alamat = Column(String(255))


class DetailTransaksiPenjualan(Base):
    __tablename__ = 'detail_transaksi_penjualan'

    id_detail_transaksi = Column(INTEGER(11), primary_key=True)
    id_transaksi_penjualan = Column(ForeignKey('transaksi_penjualan.id_transaksi_penjualan'), index=True)
    id_obat = Column(ForeignKey('obat.id_obat'), index=True)
    jumlah_beli = Column(INTEGER(11))
    harga_satuan = Column(Float(asdecimal=True))

    obat = relationship('Obat')
    transaksi_penjualan = relationship('TransaksiPenjualan')


class ResepDokter(Base):
    __tablename__ = 'resep_dokter'

    id_resep = Column(INTEGER(11), primary_key=True)
    id_pelanggan = Column(ForeignKey('pelanggan.id_pelanggan'), index=True)
    tanggal_resep = Column(String(255))
    catatan_dokter = Column(Text)

    pelanggan = relationship('Pelanggan')
