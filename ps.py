#!/usr/bin/python3
from argparse import ArgumentParser as ap
import signal
import itertools

def powerset(ain):
	a=[x for x in ain]
	if len(a)==1:
		yield list()
		yield a 
	else:
		head=a.pop(0)
		for item in powerset(a):
			yield item 
			yield [head]+item


def closure(base, n):

	bs=[set(x) for x in base]
	pairs=itertools.combinations(base,2)
	for x,y in pairs:
		sx=set(x)
		sy=set(y)
		if sx&sy not in bs or sx|sy not in bs:
			if sx&sy not in bs:
				why="inter"
			else:
				why="union"
			#print (sx,sy,sx|sy,sx&sy,bs,sx|sy in bs, sx&sy in bs)
			print (f"{n:3d} FAIL {len(bs):3d} {str(bs):<55},{why:5} {str(sx):<10},{str(sy):<10}")
			return False
	return True

if __name__ == "__main__":
	signal.signal(signal.SIGINT,signal.SIG_DFL)
	parser=ap()
	parser.add_argument("--count","-c", action="store", type=int, default=3,  help="Order of target set")
	args=parser.parse_args()



	baseset=list(range(1,1+args.count))
	ps=list(powerset(baseset))
	print([set(x) for x in ps])
	ppfs=list(powerset(ps))
	ppas=[x for x in ppfs if [] in x ]
	pps=[x for x in ppas if baseset in x ]
	print(len(pps))

	res=[]
	for n,b in enumerate(pps):
		if closure(b,n):
			bset=[set(x) for x in b]
			res.append(bset)
			print(f"{n:3d} GOOD {len(bset):3d} {str(bset):<55}")

	print(len(res))

