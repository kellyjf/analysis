#!/usr/bin/python3


import signal
import csv
from argparse import ArgumentParser as ap

from schema import Theorem, Usage, session

def load(filename="db.csv"):
	with open(filename, "r", encoding="utf-8-sig") as f:
		rdr=csv.DictReader(f)
		for line in rdr:
			t=Theorem(id=line['ID'],
				type=line['Type'], title=line['Title'],
				chapter=line['Chapter'])
			if line['ID']:
				session.add(t)
				print(line)
				session.commit()
def choose(pattern, indent=""):
	thms=session.query(Theorem).filter(Theorem.id.like(f"{pattern}"))
	thms=thms.all()

	if len(thms)==0:	
		thms=session.query(Theorem).filter(Theorem.title.like(f"{pattern}")).all()
	if len(thms)==0:	
		thms=session.query(Theorem).filter(Theorem.title.like(f"%{pattern}%")).all()

	for ndx,thm in enumerate(thms):
		print(f"{indent}{ndx:3d} {thm.id:>9} {thm.title}")

	if thms:
		choice=input(f"{indent}Select a theorem to edit: ")
		try:
			choice=int(choice)
			return thms[choice]
		except:
			pass

def editthm(thm):
	choice=""
	while choice != 'Q':
		print(f"{thm.chapter:<18} {thm.type:<12} {thm.id:>10}  {thm.title}")
		for ndx,u in enumerate(thm.arguments):
			athm=u.support
			print(f"{ndx:3d} {athm.chapter:<18} {athm.type:<12} {athm.id:>10}  {athm.title:<30.30} {u.text}")

		action=input("[A]dd, [D]elete, [E]dit, [S]ave or [Cancel]? ")
		choice=action[0].upper()

		if choice=='S':
			session.commit()
			choice='Q'
		elif choice=='C':
			session.rollback()
			choice='Q'
		elif choice=='D':
			if len(action)>1:
				udx=int(action[1:].strip())
				print("DELETE",udx,thm.arguments[udx])
				#thm.arguments.remove(thm.arguments[udx])
				#session.add(thm)
				session.delete(thm.arguments[udx])
				session.refresh(thm)
		elif choice=='A':
			uthm=choose(action[1:].strip(), "\t")
			text=input("Notes: ")
			if uthm:
				usage=Usage(theorem=thm, support=uthm, text=text)
				session.add(usage)
	

def edit(pattern):
	thm=choose(pattern)
	editthm(thm)




if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	parser=ap()
	parser.add_argument("--load", action="store", help="Load from CSV")
	parser.add_argument("--edit", action="store", help="Load from CSV")

	args=parser.parse_args()

	if args.load:
		load(args.load)
	if args.edit:
		edit(args.edit)

