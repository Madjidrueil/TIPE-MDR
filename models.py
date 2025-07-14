from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Index(Base):
    __tablename__ = "index"
    id = Column(Integer, primary_key=True, index=True)
    document = Column(String, unique = True)

class Mots_distincs(Base):
    __tablename__ = 'mots_distincs'
    id = Column(Integer, primary_key=True, index=True)
    mot = Column(String, unique = True)


class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String)
    word_freq = Column(Integer)
    document_id = Column(String, ForeignKey("documents.id"))


class Index_inverse(Base):
    __tablename__ = "Index_inverse"
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(String, ForeignKey('mots_distincs.id'))
    document = Column(String)
    word_freq = Column(Integer)