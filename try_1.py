import tkinter as tk
from tkinter import messagebox
import os

root = tk.Tk()#创建窗口
root.title("登录界面")#创建窗口标题
image_1 = tk.PhotoImage(file='image\\tupian.gif')#准备图片
root.iconphoto(True,image_1)#将图片设为图标
width,height = 400,200
screen_width,screen_height = root.maxsize()#这里用maxsize方法获取电脑屏幕大小
root.resizable(width=False,height=False)#决定窗口能否被拉伸
root.maxsize(1200,750)#窗口最大大小
root.minsize(100,100)#窗口最小大小
root.geometry(f'{width}x{height}+{int(screen_width/2-width/2)}+{int(screen_height/2-height/2)}')#这样能居中
#前面的500x600是窗口大小,+x表离屏幕左边的距离,-x表离屏幕右边的距离,+y表离屏幕上面的距离,-y表离屏幕下面的距离
#用int是为了将浮点数转为整数
l1_text = tk.StringVar()
l1_text.set('用户名')
l1 = tk.Label(root,textvariable=l1_text,bg='white',fg='black',font=('宋体',20))
l1.place(x=0,y=28)
l2 = tk.Label(root,text='密  码',bg='white',fg='black',font=('宋体',20))
l2.place(x=0,y=68)
e_name = tk.Entry(root,width=28)
e_name.place(x=110,y=31)
secert = '*'
e_pd = tk.Entry(root,width=28,show=secert)
e_pd.place(x=110,y=75)
e_name.insert(0,'李涛')#如果要用这行代码,place方法或pack方法或grid方法与实例本体要分开放,要把实例放在前面
#Entry组件与Label组件操作基本相同,但没那么多参数ps:没有height参数,只有width参数

def get_password():
	e_pd_text = tk.StringVar()
	e_pd_text.set(f'密码是{e_pd.get()}')
	e_pd_show = tk.Label(root,textvariable=e_pd_text)
	e_pd_show.place(x=140,y=145)
	e_pd_show.after(5000,e_pd_show.destroy)#在这里destroy后不要加括号

def login():
	if e_name.get() == '李涛' and e_pd.get() == '123456':
		successful = tk.Label(root,text='登录成功',fg='green')
		successful.place(x=170,y=3)
		global zhuangtai
		zhuangtai = True
		root.after(1000,root.destroy)
	elif e_name.get() == '张睿' and e_pd.get() == '654321':
		successful = tk.Label(root,text='登录成功',fg='green')
		successful.place(x=170,y=3)
		zhuangtai = True
		root.after(1000,root.destroy)
	elif e_name.get() == '荆垒' and e_pd.get() == '654123':
		successful = tk.Label(root,text='登录成功',fg='green')
		successful.place(x=170,y=3)
		zhuangtai = True
		root.after(1000,root.destroy)
	else:
		unsuccessful = tk.Label(root,text='登录失败',fg='red')
		unsuccessful.place(x=170,y=3)
		unsuccessful.after(1000,unsuccessful.destroy)

def del_all():
	e_name.delete(0,'end')
	e_pd.delete(0,'end')

def check_color():
	os.startfile("image\\color.png")

def secert_on():
	global e_pd#在函数内调用或定义函数外的变量时,要用global声明为全局变量
	message = e_pd.get()
	e_pd.destroy()
	secert = '*'
	e_pd = tk.Entry(root,width=28,show=secert)
	e_pd.place(x=110,y=75)
	e_pd.insert(0,message)
	e_pd.focus_set()#使光标始终集中在密码输入框里
	button_secert_on.destroy()
	button_secert_off = tk.Button(root,text='密码可见',width=7,height=1,bg='Tan',command=secert_off)
	button_secert_off.place(x=320,y=72)

def secert_off():
	global e_pd#在函数内调用或定义函数外的变量时,要用global声明为全局变量
	message = e_pd.get()
	e_pd.destroy()
	secert = ''
	e_pd = tk.Entry(root,width=28,show=secert)
	e_pd.place(x=110,y=75)
	e_pd.insert(0,message)
	e_pd.focus_set()#使光标始终集中在密码输入框里
	global button_secert_on#在这里将button_secert_on设为全局变量,为上面的引用作准备	
	button_secert_off.destroy()
	button_secert_on = tk.Button(root,text='密码不可见',width=7,height=1,bg='Tan',command=secert_on)
	button_secert_on.place(x=320,y=72)

def tuichu_event():
	if messagebox.askquestion(title='退出/回来',message='你要退出吗？',icon='warning') == 'yes':
		root.destroy()#icon表示弹窗的图标,有error，info，question或warning等参数可选

#Label组件第一个填在哪个窗口写文字,第二个text或textvariable填要写入的文字,
#第三个bg填背景颜色,第四个fg填字体颜色,第五个font填用什么字体和字体大小
#第五个font可填可不填,填的话要输入一个元组,第六个anchor填字体的位置,用N,S,W,E,CENTER来表达位置

#当你需要改变Label显示的文本内容时,需要创建一个StringVar对象如:变量名 = tk.StringVar()
#然后再用变量名.set('内容')设置内容,可以用变量名.get()来获取StringVar此时的内容
#如用此方式,就不能用text=''而要用textvariable=变量名

#最后用pack决定把文本放在哪ps:不加pack文本会显示不出来,fill代表往上或下延伸,expand代表是否填满分配给他的所有空间
#还可以用width,height来决定字体的宽度和高度ps:可加可不加
#也可以用place来决定把文本放在哪,直接输入x轴和y轴的坐标就行

#Label还可以加载图片格式为tk.Label(窗口名,image=tupian).pack()ps:只支持.gif等格式的图片
#ps:tupian = tk.PhotoImage(flie='文件名')ps:这一句必须放外面或用global设成全局变量
#如果想放其他格式的图片可以用 变量名 = ImageTk.PhotoImage(file='文件名')ps:PIL库要单独下载
#窗口名.iconphoto(True,文件名)设置图标,True代表以后新开的窗口都用该图标,False代表只用当前窗口用该图标

button_secert_off = tk.Button(root,text='密码可见',width=7,height=1,bg='Tan',command=secert_off)
button_secert_off.place(x=320,y=72)
button_color = tk.Button(root,text='获取图片',width=7,height=1,bg='Tan',command=check_color)
button_color.place(x=280,y=115)
button_pd = tk.Button(root,text='获取密码',width=7,height=1,bg='Tan',command=get_password)
button_pd.place(x=50,y=115)
button_login = tk.Button(root,text='登录',width=7,height=1,bg='Tan',command=login)
button_login.place(x=200,y=115)
button_del = tk.Button(root,text='删除所有',width=7,height=1,bg='Tan',command=del_all)
button_del.place(x=125,y=115)

#Button组件操作与Label组件操作基本相同,但多了一个command用来指定按按钮后的命令
#如果要用图片做按钮就要去掉text或textvariable参数,换成image=变量名
#bg参数也要去掉

#l2 = tk.Label(root,image=image_1).pack() ps:如果要用去掉#号
root.protocol('WM_DELETE_WINDOW',tuichu_event)#WM_DELETE_WINDOW是事件监测不可删掉
root.mainloop()#使窗口保持循环