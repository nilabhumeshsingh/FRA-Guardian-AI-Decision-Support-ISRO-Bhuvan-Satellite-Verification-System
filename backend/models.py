from sqlalchemy import Column, Integer, String, Float, Text, Date, JSON
from database import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    claimant_name = Column(String, nullable=False)
    village = Column(String, nullable=False)
    district = Column(String, nullable=False)
    state = Column(String, default="Chhattisgarh")
    officer_id = Column(String, nullable=False)
    officer_name = Column(String, nullable=False)
    status = Column(String, nullable=False)           # Approved / Rejected / Pending
    filed_date = Column(String, nullable=False)       # ISO string
    decision_date = Column(String, nullable=True)
    area_ha = Column(Float, nullable=False)
    geojson = Column(Text, nullable=False)            # JSON string of GeoJSON polygon
    documents_submitted = Column(JSON, nullable=False) # list of doc names
    health_score = Column(Float, default=0.0)
    anomaly_flags = Column(JSON, default=list)        # list of flag strings
    satellite_match_pct = Column(Float, default=0.0)  # 0–100
    land_use_claimed = Column(String, default="Agricultural")
    satellite_land_use = Column(String, default="Forest")
