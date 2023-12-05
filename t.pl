#!/usr/bin/python3


import signal
import csv
from schema import Theorem, session

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	with open("db.csv", "r", encoding="utf-8-sig") as f:
		rdr=csv.DictReader(f)
		for line in rdr:
			t=Theorem(id=line['ID'],
				type=line['Type'], title=line['Title'],
				chapter=line['Chapter'])
			if line['ID']:
				session.add(t)
				print(line)
				session.commit()
