from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    content = Column(Text)
    answers = relationship("Answer", back_populates="document")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(Text)
    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("Document", back_populates="answers")
