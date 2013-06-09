ceasered="Esp qtcde nzyqpcpynp zy esp ezatn zq Lcetqtntlw Tyepwwtrpynp hld spwo le Olcexzfes Nzwwprp ty estd jplc."
shredded=[
['de','  ',' f','Cl','nf','ed','au',' i','ti','  ','ma','ha','or','nn','ou',' S','on','nd','on'], 
['ry','  ','is','th','is',' b','eo','as','  ','  ','f ','wh',' o','ic',' t',', ','  ','he','h '],
['ab','  ','la','pr','od','ge','ob',' m','an','  ','s ','is','el','ti','ng','il','d ','ua','c '],
['he','  ','ea','of','ho',' m',' t','et','ha','  ',' t','od','ds','e ','ki',' c','t ','ng','br'],
['wo','m,','to','yo','hi','ve','u ',' t','ob','  ','pr','d ','s ','us',' s','ul','le','ol','e '],
[' t','ca',' t','wi',' M','d ','th','"A','ma','l ','he',' p','at','ap','it','he','ti','le','er'],
['ry','d ','un','Th','" ','io','eo','n,','is','  ','bl','f ','pu','Co','ic',' o','he','at','mm'],
['hi','  ','  ','in','  ','  ',' t','  ','  ','  ','  ','ye','  ','ar','  ','s ','  ','  ','. '],
]
import collections
# wikipedia letter frequency in percent
lf ={'a': 8.167,'b': 1.492,'c': 2.782,'d': 4.253,'e': 12.702,'f': 2.228,'g': 2.015,'h': 6.094,'i': 6.966,'j': 0.153,'k': 0.772,'l': 4.025,'m': 2.406,'n': 6.749,'o': 7.507,'p': 1.929,'q': 0.095,'r': 5.987,'s': 6.327,'t': 9.056,'u': 2.758,'v': 0.978,'w': 2.360,'x': 0.150,'y': 1.974,'z': 0.074}
lf = collections.defaultdict(float,lf);

# wikipedia frequency for first letter of words
flf = {'a': 11.602, 'b': 4.702, 'c': 3.511, 'd': 2.670, 'e': 2.000, 'f': 3.779, 'g': 1.950, 'h': 7.232, 'i': 6.286, 'j': 0.631, 'k': 0.690, 'l': 2.705, 'm': 4.374, 'n': 2.365, 'o': 6.264, 'p': 2.545, 'q': 0.173, 'r': 1.653, 's': 7.755, 't': 16.671, 'u': 1.487, 'v': 0.619, 'w': 6.661, 'x': 0.005, 'y': 1.620, 'z': 0.050}

d = collections.defaultdict(float)
N_all=len(ceasered);
N=0;
N_nonletter = 0;
for c in ceasered:
	if 'A'<=c<='z':
		d[c.lower()] += 1
		N += 1;
	else:
		N_nonletter += 1

for c,n in d.items():
	d[c] = 100.0*d[c]/N;

print str(d)
print str(lf)

for delta in range(26):
	lc = list(ceasered);
	for i,c in enumerate(lc):
		if 'A'<=c<='Z':
			lc[i] = chr(((ord(c)-ord('A')+delta) % 26)+ord('A'))
		elif 'a'<=c<='z':
			lc[i] = chr(((ord(c)-ord('a')+delta) % 26)+ord('a'))
	print ''.join(lc)
	
# It took about 9 hand-iterations to find the right order
order = [3,6,0,15,11,13,18,2,14,17,5,7,4,12,10,8,16,1,9]
line = ['']*len(shredded)
for l,row in enumerate(shredded):
	for c,col in enumerate(row):
		line[l] += row[order[c]]
	print line[l]

