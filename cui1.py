import os
import random

rd=lambda x:(random.choice(list(range(100)))<x)

s_time=[2,4,8,16,999999]
_q=[list(),]*len(s_time)

NT='NEXIST'
RD='READY'
RUN='RUNNING'
IO='WAITING'
END='DONE'
BG='begin'

_process_example={
	'name':'EXIT',
	'id':0,
	'total':0,
	'wait':0,
	'err':0,
	'+io':0,
	'-io':50,
	'surplus':0,
	'state':END,
}

def process_maker()->list:
	_process=list()
	for i in range(5):
		_a={
			'name':'p'+str(i+1),
			'id':100+i+1,
			'total':20,
			'+io':40,
			'-io':10,
		}
		_process.append(_a)
	for i in range(5,10):
		_a={
			'name':'p'+str(i+1),
			'id':200+i+1,
			'total':10,
			'wait':(i+1)*10,
		}
		_process.append(_a)
	for i in range(10,15):
		_a={
			'name':'p'+str(i+1),
			'id':300+i+1,
			'total':40,
			'err':3,
		}
		_process.append(_a)
	return _process


def u(js:dict,k:str,v:all,t:type=int)->None:
	if k not in js:
		js[k]=v
	js[k]=t(js[k])

_l=process_maker()
for i in _l:
	i['state']=NT
	u(i,'surplus',i['total'])
	u(i,'total',20)
	u(i,'wait',0)
	u(i,'err',0)
	u(i,'+io',0)
	u(i,'-io',50)
	if i['wait']:
		continue
	i['state']=0
	_q[0].append(i)


def chose():
	for i in _q:
		if i:
			return i.pop(0)

def fil(l:list,x:int=8)->str:
	return ''.join([str(i)+' '*(x-len(str(i))) for i in l])

def bg()->None:
	l=['Clock','Queue','CPU','NewIO?']+[i['name'] for i in _l]
	print(fil(l))

def ckio(p:dict):
	for i in _l:
		if i==p:
			continue
		if i['state']==IO:
			if rd(i['-io']):
				i['state']=0
				# print('push',i)
				_q[0].append(i)

_clk=1
def clk(p:dict=None,lv:int=0):
	global _clk
	if p:
		if rd(p['+io']):
			p['state']=IO
		if p['surplus']==1 or rd(p['err']):
			p['state']=END

		l=[_clk,lv,p['name']+'_'+str(p['total']-p['surplus']+1),'True' if p['state']==IO else '']+[RUN if i==p else (RD if isinstance(i['state'],int) else i['state']) for i in _l]
	else:
		p=_process_example
		l=[_clk,'','WAITING','']+[RD if isinstance(i['state'],int) else i['state'] for i in _l]


	print(fil(l))

	ckio(p)
	for i in _l:
		if i['wait']==_clk:
			i['state']=0
			_q[0].append(i)
	p['surplus']-=1
	_clk+=1
	


def run():
	if not [None for i in _l if i['state']!=END]:
		return
	p=chose()
	if not p:
		clk()
		return True
	
	lv=p['state']
	# print('pop',p)
	for i in range(s_time[lv]):
		if not isinstance(p['state'],int):
			break
		clk(p,lv)
	
	if isinstance(p['state'],int):
		p['state']+=1
		# print('push',p)
		_q[p['state']].append(p)

	return True

bg()
while run():None
clk()
clk()
clk()




		

