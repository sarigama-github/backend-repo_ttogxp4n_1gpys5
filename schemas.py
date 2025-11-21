"""
Database Schemas for Kolegium Dermatologi, Venereologi & Estetika

Each Pydantic model represents a MongoDB collection.
Collection name is the lowercase of the class name, e.g. Event -> "event".
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List, Literal
from datetime import date as Date

# Core domain schemas

class Event(BaseModel):
    title: str = Field(..., description="Judul kegiatan/konferensi/seminar")
    dateStart: Date = Field(..., description="Tanggal mulai")
    dateEnd: Optional[Date] = Field(None, description="Tanggal selesai (opsional)")
    location: Optional[str] = Field(None, description="Lokasi acara")
    mode: Literal["online", "offline", "hybrid"] = Field("offline", description="Mode acara")
    category: Optional[str] = Field(None, description="Kategori acara (konferensi, seminar, workshop)")
    speakers: Optional[List[str]] = Field(default_factory=list, description="Daftar pembicara")
    description: Optional[str] = Field(None, description="Deskripsi singkat")
    registrationUrl: Optional[HttpUrl] = Field(None, description="URL pendaftaran")
    coverImage: Optional[HttpUrl] = Field(None, description="Gambar sampul")

class Publication(BaseModel):
    title: str = Field(..., description="Judul publikasi atau pedoman klinis")
    year: int = Field(..., ge=1900, le=2100, description="Tahun publikasi")
    authors: Optional[List[str]] = Field(default_factory=list, description="Daftar penulis")
    category: Optional[str] = Field(None, description="Kategori (panduan, laporan penelitian, konsensus)")
    abstract: Optional[str] = Field(None, description="Abstrak ringkas")
    pdfUrl: Optional[HttpUrl] = Field(None, description="Tautan PDF")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tag/kata kunci")
    citation: Optional[str] = Field(None, description="Sitasi")

class BlogPost(BaseModel):
    title: str = Field(..., description="Judul artikel")
    slug: str = Field(..., description="Slug URL unik")
    author: Optional[str] = Field(None, description="Nama penulis")
    # Hindari nama field 'date' agar tidak bentrok dengan tipe, gunakan publishedAt
    publishedAt: Date = Field(default_factory=Date.today, description="Tanggal publikasi")
    category: Optional[str] = Field(None, description="Kategori artikel")
    excerpt: Optional[str] = Field(None, description="Ringkasan 1–3 kalimat")
    content: Optional[str] = Field(None, description="Konten HTML/Markdown")
    coverImage: Optional[HttpUrl] = Field(None, description="Gambar sampul")

class Commission(BaseModel):
    name: str = Field(..., description="Nama komisi/divisi")
    slug: str = Field(..., description="Slug URL unik")
    chair: Optional[str] = Field(None, description="Ketua")
    secretary: Optional[str] = Field(None, description="Sekretaris")
    description: Optional[str] = Field(None, description="Deskripsi")
    programs: Optional[List[str]] = Field(default_factory=list, description="Program kerja")
    contacts: Optional[str] = Field(None, description="Kontak PIC")
    relatedDocs: Optional[List[HttpUrl]] = Field(default_factory=list, description="Dokumen terkait")

class Center(BaseModel):
    institutionName: str = Field(..., description="Nama institusi/senter pendidikan")
    address: Optional[str] = Field(None, description="Alamat")
    city: Optional[str] = Field(None, description="Kota")
    province: Optional[str] = Field(None, description="Provinsi")
    website: Optional[HttpUrl] = Field(None, description="Website")
    pic_name: Optional[str] = Field(None, description="Nama PIC")
    pic_role: Optional[str] = Field(None, description="Jabatan PIC")
    pic_email: Optional[EmailStr] = Field(None, description="Email PIC")
    pic_phone: Optional[str] = Field(None, description="Telepon PIC")
    capacity: Optional[int] = Field(None, ge=0, description="Kapasitas")
    facilities: Optional[List[str]] = Field(default_factory=list, description="Daftar fasilitas")
    accreditationStatus: Optional[Literal["A", "B", "C", "Belum"]] = Field(None, description="Status akreditasi")
    accreditationYear: Optional[int] = Field(None, ge=1900, le=2100, description="Tahun akreditasi")
    documents: Optional[List[HttpUrl]] = Field(default_factory=list, description="Tautan dokumen pendukung")

class Member(BaseModel):
    fullName: str = Field(..., description="Nama lengkap")
    email: EmailStr = Field(..., description="Email")
    phone: Optional[str] = Field(None, description="Nomor telepon")
    institution: Optional[str] = Field(None, description="Institusi")
    city: Optional[str] = Field(None, description="Kota")
    province: Optional[str] = Field(None, description="Provinsi")
    role: Optional[str] = Field(None, description="Residen/Spesialis/ dll")
    strNumber: Optional[str] = Field(None, description="Nomor STR")
    interests: Optional[List[str]] = Field(default_factory=list, description="Bidang minat")

class ContactMessage(BaseModel):
    name: str = Field(..., description="Nama pengirim")
    email: EmailStr = Field(..., description="Email pengirim")
    subject: str = Field(..., description="Subjek")
    message: str = Field(..., description="Isi pesan")
