#!/usr/bin/python3

#
# SQLAlchemy creates an object heirarchy that adapts python code classes
# to DB tables.  By subclassing all these adapter objects from a declariative
# base table, code can traverse the object tree to detect the structure of 
# the object heirarchy, and create schema DDL so that the database can be created
# from the derived SQL
#
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

#
# The classes represent tables, and they contain members for the columns
# and constraints of the table.  These are instances of classes that are available 
# in the main sqlalchemy module
from sqlalchemy import Table, Index, Column, Boolean, Integer, String, Float, Unicode, DateTime, ForeignKey, func
import string

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import ForeignKeyConstraint

class Usage(Base):
	__tablename__ = "usages"
	theorem_id = Column(String, ForeignKey("theorems.id"),primary_key="True")
	support_id = Column(String, ForeignKey("theorems.id"),primary_key="True")
	text=Column(String)
	
	def __repr__(self):
		return f"Usage({self.theorem_id!r}-{self.theorem.title},{self.support_id}-{self.support.title}, {self.text})" 


class Theorem(Base):
	__tablename__ = "theorems"
	id = Column(String, primary_key=True)
	type=Column(String)
	title=Column(String)
	chapter=Column(String)
	text=Column(String)
	def __repr__(self):
		return f"Theorem({self.id!r},{self.title!r})" 

Usage.theorem=relationship("Theorem", uselist=False, foreign_keys=[Usage.theorem_id],  backref="arguments")
Usage.support=relationship("Theorem", uselist=False, foreign_keys=[Usage.support_id],  backref="usages")
#Theorem.usages=relationship("Usage", foreign_keys=[Usage.theorem_id], backref="theorem")

#Usage.proof=relationship("Theorem", foreign_keys=[Usage.support_id])
#Usage.supports=relationship("Theorem", foreign_keys=[Usage.theorem_id])

if False:
	Theorem.proves=relationship("Theorem", 
		secondary=Usage.__table__,
		primaryjoin="Theorem.id==Usage.theorem_id",
		secondaryjoin="Theorem.id==Usage.support_id",
		backref="supports"
	)

#Theorem.supports=relationship("Usage", primaryjoin="Theorem.id==Usage.support_id")

#Usage.theorem=relationship("Theorem", foreign_keys=[theorem_id], backref="usages")

#Theorem.proofs=relationship("Theorem", secondary="Usage",backref="proofs")

from sqlalchemy import create_engine, not_
engine=create_engine("sqlite:///analysis.sqlite")
Base.metadata.create_all(engine)

#from sqlalchemy.orm import Session
#Session=sessionmaker(engine)
Session=sessionmaker(engine, autoflush=False)

session=Session()
_quiet=False

if __name__ == "__main__":
	from argparse import ArgumentParser as ap
	parser=ap()
	parser.add_argument("--list","-l", action="store_true", help="List Database")
	args=parser.parse_args()



