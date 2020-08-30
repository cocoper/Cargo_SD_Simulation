import streamlit as st
from PIL import Image
import json
import predictor
from multiprocessing import Queue,Process

process_message = ''  #一个全局变量，用来接收从主程序中传递出的信息字符串

#定义所有需要输入的函数
def number(title,mv,v,s):
    setting = st.sidebar.number_input(title,min_value=mv,value=v,step=s)
    return setting

def radio(title,choice):
    setting=st.sidebar.radio(title,choice)
    return setting

# def parameter():
#     P = st.sidebar.radio('货舱烟雾探测器设备参数定义方式选择：', ('默认（C919的烟雾探测参数）', '自定义'))
#     return P

def slider(title,min,max,v,s):
    Sen = st.sidebar.slider(title,min_value=min,max_value=max,value=v,step=s)
    return Sen

def text(title,input):
    setting = st.sidebar.text_input(title,input)
    return setting

def get_msg_main(msg_queue): #读取主程序进程数据
    while True:
        process_message = msg_queue.get(True)
        # print('this is from GUI')
        process_message += 'this is from GUI\n'
    


#生成网页界面，调用输入函数
st.title('货舱烟雾探测系统设计平台')
show_fig = Image.open('1.1.png')
if show_fig.mode == "P":
    show_fig = show_fig.convert('RGB')
st.image(show_fig, width=530)
st.sidebar.title('参数设置')
st.sidebar.header('1.设置货舱尺寸')
if st.sidebar.button('货舱尺寸示意图'):
    st.header('货舱尺寸')
    bay_fig=Image.open('bay_fig.bmp')
    st.image(bay_fig,width=512)
l=number('货舱长度（>100mm）：',100,100,1)
w=number('货舱宽度（>100mm）：',100,100,1)
h=number('货舱高度（>100mm）：',100,100,1)

st.sidebar.header('2.设置货舱烟雾探测器布置参数')
if st.sidebar.button('布置方式示意图'):
    st.header('货舱烟雾探测器布置参数')
    center = Image.open('center.jpg')
    st.image(center, width=512)
    side = Image.open('side.jpg')
    st.image(side, width=512)
m=radio('典型布置方式：',('居中布置','交错布置'))
q=number('货舱烟雾探测器数量（>1个）',1,8,1)
G1=number('Gap1（>0mm）：',0,0,1)
G2=number('Gap2（>0mm）：',0,0,1)
d=number('Displacement（>0mm）：',0,0,1)


st.sidebar.header('3.设置货舱烟雾探测器设备参数')
# parameter('C919')
S=slider('货舱烟雾探测器灵敏度（0.1~1.0）', 0.1, 1.0, 0.5, 0.1)
F=slider('货舱烟雾探测器虚警率（0.0~1.0）', 0.0, 1.0, 0.5, 0.1)
Sl=number('货舱烟雾探测器的长度（>10mm）：',10,10,1)
Sw=number('货舱烟雾探测器的宽度（>10mm）：',10,10,1)

st.sidebar.header('4.设置仿真环境参数')
c=number('货舱烟雾探测系统的响应时间要求（>1s）',1,60,1)
T=text('本次仿真分析的飞机型号为', '请输入')
x=number('烟雾源移动步长间隔（X向）（>1mm）',1,1,1)
y=number('烟雾源移动步长间隔（Y向）（>1mm）',1,1,1)

#把输入的数值保存在Dic中
if st.sidebar.button('设置完成'):
    dic={
        "bay_length": l,
        "bay_width": w,
        "bay_height": h,
        'criteria':c,
        'Type':T,
        'SD_qty':q,
        'Sen':S,
        'FAR':F,
        "SD_len": Sl,
        "SD_width": Sw,
        "method": m,
        "Gap1": G1,
        "Gap2": G2,
        "displace": d,
        "x_interval": x,
        "y_iterval": y
    }
    st.write('您设置的所有参数如下：\n',
             '\n1.货舱尺寸\n',
             '\n货舱长度：',l,'mm\n',
             '\n货舱宽度：', w, 'mm\n',
             '\n货舱高度：', h, 'mm\n',
             '\n2.布置参数\n',
             '\n布置方式：',m, '\n',
             '\n烟雾探测器数量：',q, '个\n',
             '\nGap1：', G1, 'mm\n',
             '\nGap2：', G2, 'mm\n',
             '\nDisplacement：', d, 'mm\n',
             '\n3.货舱烟雾探测器设备参数\n',
             '\n烟雾探测器灵敏度：', S, '\n',
             '\n烟雾探测器虚警率：', F, '\n',
             '\n烟雾探测器长度：', Sl, 'mm\n',
             '\n烟雾探测器宽度：', Sw, 'mm\n',
             '\n4.仿真环境参数\n',
             '\n系统响应时间要求：', c, 's\n',
             '\n飞机型号：',T, '\n',
             '\n烟雾源移动步长X向间隔：', x, 'mm\n',
             '\n烟雾源移动步长Y向间隔：', y, 'mm\n'
             )

    json_string=json.dumps(dic,ensure_ascii=False,indent=4)
    #ensure_ascii=False(输出中文)， indent=4(缩进为4)
    with open('test.json','w',encoding='utf-8') as f:
        f.write(json_string)
    
if st.button('开始预测'):

#创建两个进程，一个用于运行预测器，一个读取预测器中每步输出的信息
    msg_queue = Queue()
    msg_put = Process(target=predictor.RunMain,args=(msg_queue,))
    msg_get = Process(target=get_msg_main,args=(msg_queue,))
    # predictor.RunMain()
#启动后台主程序
    msg_get.start()
    msg_put.start()
    msg_put.join() #处理队列中所有的数据
    st.write(process_message)
    msg_get.terminate()  #手动终止读取进程，结束程序


