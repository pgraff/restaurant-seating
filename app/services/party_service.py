"""
Party service layer
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.database import Party
from app.models.schemas import PartyCreate, PartyUpdate


class PartyService:
    """Service for party operations"""

    def __init__(self, db: Session):
        self.db = db

    def create_party(self, party_data: PartyCreate) -> Party:
        """Create a new party"""
        party = Party(
            id=str(uuid.uuid4()),
            name=party_data.name,
            size=party_data.size,
            phone=party_data.phone,
            email=party_data.email,
            status=party_data.status,
            arrival_time=party_data.arrival_time or datetime.utcnow()
        )
        self.db.add(party)
        self.db.commit()
        self.db.refresh(party)
        return party

    def get_party(self, party_id: str) -> Optional[Party]:
        """Get party by ID"""
        return self.db.query(Party).filter(Party.id == party_id).first()

    def get_parties(self, status: Optional[str] = None) -> List[Party]:
        """Get all parties, optionally filtered by status"""
        query = self.db.query(Party)
        if status:
            query = query.filter(Party.status == status)
        return query.all()

    def update_party(self, party_id: str, party_data: PartyUpdate) -> Optional[Party]:
        """Update party"""
        party = self.get_party(party_id)
        if not party:
            return None

        update_data = party_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(party, field, value)

        self.db.commit()
        self.db.refresh(party)
        return party

    def delete_party(self, party_id: str) -> bool:
        """Delete party"""
        party = self.get_party(party_id)
        if not party:
            return False

        self.db.delete(party)
        self.db.commit()
        return True
