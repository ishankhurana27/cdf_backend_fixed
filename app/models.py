import uuid
from sqlalchemy import UUID, Column, DateTime, Integer, String, Float, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from app.database import Base
from sqlalchemy.orm import relationship

class Source(Base):
    __tablename__ = "source"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class SubSource(Base):
    __tablename__ = "sub_source"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    source_id = Column(Integer, ForeignKey("source.id"))

class MaritimeDataCDF(Base):
    __tablename__ = "cdf_data"
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    bearing = Column(Float)
    course = Column(Float)
    sys_trk_no = Column(Integer,nullable=True)
    source_id = Column(Integer, ForeignKey("source.id"))
    sub_source_id = Column(Integer, ForeignKey("sub_source.id"))
    location = Column(Geometry("POINT"),nullable=True)
    raw_data = Column(JSONB)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    logged_timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    vessel_name = Column(String, nullable=True)
    imo = Column(String(50), nullable=True)
    mmsi = Column(String(50), nullable=True)
    file_uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)    
    



class UploadMetadata(Base):
    __tablename__ = "upload_metadata"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=True)
    source_id = Column(Integer, ForeignKey("source.id"))
    sub_source_id = Column(Integer, ForeignKey("sub_source.id"))
    format = Column(String, nullable=True)  # e.g., 'NDJSON', 'CSV', 'Excel'
    record_count = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    source = relationship("Source")
    sub_source = relationship("SubSource")


class MmsiWarehouse(Base):
    __tablename__ = "mmsi_warehouse"

    id = Column(Integer, primary_key=True, index=True)
    nav_status = Column(String)
    rot = Column(Float)
    sog = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    cog = Column(Float)
    true_heading = Column(Integer)
    imo = Column(Integer)
    ship_name = Column(String)
    call_sign = Column(String)
    ship_type = Column(String)
    draught = Column(Float)
    destination = Column(String)
    dimbow = Column(Integer)
    dimstern = Column(Integer)
    dimport = Column(Integer)
    dimstarboard = Column(Integer)
    eta = Column(DateTime)  # <-- FIXED
    beam = Column(Integer)
    length = Column(Integer)
    rec_time = Column(DateTime)  # <-- FIXED
    source = Column(String)
    country = Column(String)
    flag_name = Column(String)
    file_uuid = Column(UUID(as_uuid=True), nullable=False, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, index=True)