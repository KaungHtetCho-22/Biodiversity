from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class RpiDevices(Base):
    __tablename__ = 'RpiDevices'
    id = Column(Integer, primary_key=True)
    pi_id = Column(String(50), nullable=False, unique=True)
    pi_type = Column(Integer, nullable=False, default=1, doc='0: Mobile, 1: Station')  
    audio_files = relationship("AudioFiles", back_populates="device", cascade="all, delete-orphan")

class AudioFiles(Base):
    __tablename__ = 'AudioFiles'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('RpiDevices.id'), nullable=False)
    recording_date = Column(Date, nullable=False)
    file_key = Column(String(255), nullable=False)

    # Ensure uniqueness based on (device_id, recording_date, file_key)
    __table_args__ = (
        UniqueConstraint('device_id', 'recording_date', 'file_key', name='uq_audio_file_per_day'),
    )

    detections = relationship("SpeciesDetections", back_populates="audio_file", cascade="all, delete-orphan")
    device = relationship("RpiDevices", back_populates="audio_files")

class SpeciesDetections(Base):
    __tablename__ = 'SpeciesDetections'
    id = Column(Integer, primary_key=True)
    audio_file_id = Column(Integer, ForeignKey('AudioFiles.id'), nullable=False)
    species_class = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
    time_segment_id = Column(String, nullable=False, doc="Time segment ID within the audio file where detection occurred")
    audio_file = relationship("AudioFiles", back_populates="detections")


engine = None

def init_database(database_url) -> sessionmaker:
    global engine
    engine = create_engine(database_url)
    create_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables (modify schema only if new DB)
    Base.metadata.create_all(bind=engine)

    return create_session
