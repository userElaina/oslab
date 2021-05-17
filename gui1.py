import os
import random
import tkinter as tk
from time import sleep as slp
from copy import deepcopy as dcp
import downs

rd=lambda x:(random.choice(list(range(100)))<x)

def u(js:dict,k:str,v:all,t:type=int)->None:
	if k not in js:
		js[k]=v
	js[k]=t(js[k])

def Fbt(
	where,
	px:int,
	py:int,
	x:int,
	y:int,
	command=None,
	text:str='',
	font:tuple=('黑体',16,),
	bg:str='#ffffff',
	abg:str=None,
	bd=0,
):
	if not abg:
		abg=bg
	fa=tk.Frame(
		where,
		width=px,
		height=py,
		bg=bg,
	)
	fa.propagate(False)
	fa.place(x=x,y=y)

	a=tk.Button(
		fa,
		command=command,
		text=text,
		font=font,
		bg=bg,
		bd=bd,
		activebackground=abg,
	)
	a.pack(expand=True,fill=tk.BOTH)
	return a

NT='NEXIST'
RD='READY'
RUN='RUNNING'
IO='WAITING'
END='DONE'
BG='begin'

col={
	BG:'#ffffff',
	NT:'#7f7f7f',
	RD:'#00ff00',
	RUN:'#00ffff',
	IO:'#ff0000',
	END:'#7f7f7f',
}

_process_example={
	'name':'EXIT',
	'id':0,
	'total':0,
	'wait':0,
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
			'wait':(i+1)*20,
		}
		_process.append(_a)
	for i in range(10,15):
		_a={
			'name':'p'+str(i+1),
			'id':300+i+1,
			'total':40,
		}
		_process.append(_a)
	return _process

_l=process_maker()
s_time=[2,4,8,16,999999]
_q=[list() for i in s_time]
_len=len(_l)


dpix,dpiy=1440,900
psquare=50
pd=2
ptitle=25
_len_title=[100,150,150,150,160,200,100]

nx=(dpix-psquare*2)//(psquare+pd)
ny=(_len-1)//nx+1

t=tk.Tk()
t.geometry(str(dpix)+'x'+str(dpiy)+'+0+0')
t.title('Feed-Back')
# t.iconbitmap('1.png')
tt=tk.Frame(
	t,
	width=dpix,
	height=dpiy,
	bg=col[BG],
)
tt.place(x=0,y=0)
# tt.pack(expand=True,fill=tk.BOTH)

fbts=list()
bts=list()
bt_clk=None
bt_auto=None
bt_cpu=None

nwx,nwy=pd,pd

a=Fbt(
	tt,
	px=_len_title[0],
	py=ptitle,
	x=pd,
	y=pd,
	text='所有进程:',
	bg=col[BG],
)
nwy+=ptitle+pd

for j in range(ny):
	yy=nwy+(psquare+pd)*j
	for i in range(nx):
		n=j*nx+i
		xx=nwx+(psquare+pd)*i
		a=Fbt(
			tt,
			px=psquare,
			py=psquare,
			x=xx,
			y=yy,
			text=(_l[n]['name']+'\n(0)') if n<_len else '',
			bg=col[NT] if n<_len else col[BG],
		)
		bts.append(a)

for k in range(len(s_time)+1):
	nwx,nwy=pd,pd+(ptitle+pd+psquare+ptitle)*(k+1)

	a=Fbt(
		tt,
		px=_len_title[k+1],
		py=ptitle,
		x=nwx,
		y=nwy,
		text=('等待队列:')
			if k==len(s_time) else 
				('进程队列'+str(k+1)+'('+str(s_time[k])+'):'),
		bg=col[BG],
	)
	nwy+=ptitle+pd

	for j in range(ny):
		yy=nwy+(psquare+pd)*j
		for i in range(nx):
			xx=nwx+(psquare+pd)*i
			a=Fbt(
				tt,
				px=psquare,
				py=psquare,
				x=xx,
				y=yy,
				text='',
				bg=col[BG],
			)
			bts.append(a)

flg_wait=True
def f():
	global flg_wait
	flg_wait=False

def run():
	if not [None for i in _l if i['state']!=END]:
		clk()
		return False
	p=chose()
	if not p:
		clk()
		return True
	
	lv=p['state']
	for i in range(s_time[lv]):
		if not isinstance(p['state'],int):
			break
		clk(p,lv)
	
	if isinstance(p['state'],int):
		p['state']+=1
		_q[p['state']].append(p)

	return True

def th_1():
	while True:
		run()

flg_auto=False
def th_2():
	while True:
		slp(0.01)
		if flg_auto:
			f()

def h():
	global flg_auto
	if flg_auto:
		bt_auto['bg']=col[IO]
		bt_auto['activebackground']=col[RUN]
	else:
		bt_auto['bg']=col[RUN]
		bt_auto['activebackground']=col[IO]
	flg_auto=~flg_auto


def bg():
	l=['Clock','Queue','CPU','NewIO?']+[i['name'] for i in _l]
	print(fil(l))
	for _i in range(_len):
		i=_l[_i]
		i['state']=NT
		u(i,'surplus',i['total'])
		u(i,'total',20)
		u(i,'wait',0)
		u(i,'+io',0)
		u(i,'-io',50)
		if i['wait']:
			continue
		i['state']=0

		bts[_i]['bg']=col[RD if isinstance(i['state'],int) else i['state']]
		bts[_i]['activebackground']=bts[_i]['bg']
		bts[_i+nx]['bg']=bts[_i]['bg']
		bts[_i+nx]['activebackground']=bts[_i]['bg']
		bts[_i+nx]['text']=i['name']

		_q[0].append(i)

	downs.throws(th_1)
	downs.throws(th_2)
	bt_clk['text']='Clock'
	bt_clk['command']=f

	bt_auto['command']=h
	bt_auto['text']='Auto'
	bt_auto['bg']=col[IO]
	bt_auto['activebackground']=col[RD]


def chose():
	for i in _q:
		if i:
			return i.pop(0)

def fil(l:list,x:int=8)->str:
	return ''.join([str(i)+' '*(x-len(str(i))) for i in l])

def ckio(p:dict):
	_ans=list()
	for i in _l:
		if i==p:
			continue
		if i['state']==IO:
			if rd(i['-io']):
				i['state']=0
				_q[0].append(i)
			else:
				_ans.append(i['name'])
	return _ans



_clk=1
def clk(p:dict=None,lv:int=0):
	global _clk,flg_wait

	while flg_wait:None
	# print(clk)

	if p:
		if rd(p['+io']):
			p['state']=IO
		if p['surplus']==1:
			p['state']=END
		l=[
			_clk,
			lv,
			p['name']+'_'+str(p['total']-p['surplus']+1),
			'True' if p['state']==IO else ''
		]+[
			RUN if i==p else (
				RD if isinstance(i['state'],int) else i['state']
			) for i in _l
		]
		bt_cpu['text']=p['name']
		bt_cpu['bg']=col[RUN]
		bt_cpu['activebackground']=col[RUN]
	else:
		p=_process_example
		l=[_clk,'','WAITING','']+[
			RD if isinstance(i['state'],int) else i['state']
				for i in _l
		]
		bt_cpu['text']='WAIT\nING'
		bt_cpu['bg']=col[END]
		bt_cpu['activebackground']=col[END]

	print(fil(l))

	_waits=ckio(p)
	for i in _l:
		if i['wait']==_clk:
			i['state']=0
			_q[0].append(i)
	
	for _i in range(_len):
		i=_l[_i]
		bts[_i]['bg']=col[RUN if i==p else (
				RD if isinstance(i['state'],int) else i['state']
		)]
		bts[_i]['activebackground']=bts[_i]['bg']
		bts[_i]['text']=i['name']+'\n('+str(i['total']-i['surplus'])+')'
	
	for _i in range(len(_q)):
		i=dcp(_q[_i])
		for _j in range(nx):
			_k=(_i+1)*nx+_j
			if _j<len(i):
				bts[_k]['text']=i[_j]['name']
				bts[_k]['bg']=col[RD]
				bts[_k]['activebackground']=col[RD]
			else:
				bts[_k]['text']=''
				bts[_k]['bg']=col[BG]
				bts[_k]['activebackground']=col[BG]
	
	for _j in range(nx):
		_k=(len(s_time)+1)*nx+_j
		if _j<len(_waits):
			bts[_k]['text']=_waits[_j]
			bts[_k]['bg']=col[IO]
			bts[_k]['activebackground']=col[IO]
		else:
			bts[_k]['text']=''
			bts[_k]['bg']=col[BG]
			bts[_k]['activebackground']=col[BG]
	
	bt_tm['text']=str(_clk)

	p['surplus']-=1
	flg_wait=True
	_clk+=1



bt_clk=Fbt(
	tt,
	px=psquare,
	py=psquare,
	x=dpix-int(psquare*1.5),
	y=psquare,
	text='Begin',
	bg=col[IO],
	abg=col[RUN],
	command=bg,
	font=('黑体',12,''),
)

bt_auto=Fbt(
	tt,
	px=psquare,
	py=psquare,
	x=dpix-int(psquare*1.5),
	y=int(psquare*2.5),
	text='',
	bg=col[BG],
	abg=col[BG],
)

Fbt(
	tt,
	px=psquare,
	py=psquare//2,
	x=dpix-int(psquare*1.5),
	y=psquare*5,
	text='CPU',
	bg=col[BG],
	abg=col[BG],
)

bt_cpu=Fbt(
	tt,
	px=psquare,
	py=psquare,
	x=dpix-int(psquare*1.5),
	y=pd+int(psquare*5.5),
	text='WAIT\nING',
	bg=col[END],
	abg=col[END],
)

Fbt(
	tt,
	px=psquare,
	py=psquare//2,
	x=dpix-int(psquare*1.5),
	y=psquare*7,
	text='Clock',
	bg=col[BG],
	abg=col[BG],
)

bt_tm=Fbt(
	tt,
	px=psquare,
	py=psquare,
	x=dpix-int(psquare*1.5),
	y=pd+int(psquare*7.5),
	text='0',
	bg=col[RUN],
	abg=col[RUN],
)

t.mainloop()


