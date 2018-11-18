"""Model definition(s)"""
from sqlalchemy import Column, DateTime, Integer, Sequence, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class Definition(Base):
    """Blah"""
    __tablename__ = 'definitions'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    word = Column(String)
    long_definition = Column(Text)
    short_definition = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        word = self.word
        definition = self.short_definition
        return f'<{word}: {definition}>'
