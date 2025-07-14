from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Index(Base):
    __tablename__ = "index"
    id = Column(Integer, primary_key=True, index=True)
    document = Column(String, unique = True)

class Info(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True, index=True)
    nb_doc = Column(Integer)
    nb_mot_distincts = Column(Integer)
    nb_mot_total = Column(Integer)
    nb_doc_file = Column(Integer)


class Répertoire(Base):
    __tablename__ = 'répertoire'
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(String)
    word_freq = Column(Integer)


class Index_inverse(Base):
    __tablename__ = "Index_inverse"
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(String, ForeignKey('répertoire.id'))
    document = Column(String)
    word_freq = Column(Integer)

class File(Base):
    __tablename__ = "File"
    id = Column(Integer, primary_key=True, index = True)
    titre = Column(String)