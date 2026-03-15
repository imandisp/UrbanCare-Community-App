from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class ComplaintImage(Base):
    __tablename__ = "complaint_images"

    # Primary key
    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key to complaints table
    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.complaint_id"), nullable=False)

    # Type of image (complaint, verification, repair)
    image_type = Column(String(20), nullable=False, default="complaint")

    # Firebase / cloud URL
    image_url = Column(String(500), nullable=False)
