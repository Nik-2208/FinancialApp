from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="pending")
    description = Column(String(255), nullable=False)

    # Relationship with the User model
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, timestamp={self.timestamp}, status={self.status}, description={self.description})>"
