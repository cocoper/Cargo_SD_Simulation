# 3.0版本：界面共两栏；
# 输入框显示在左边栏，把图片显示在右边栏，点击标题可以查看图片；
# 删除了每个输入的显示反馈；
# 可以存储生成json文件，且可以根据输入实时更新json文件中的内容
# 优化了按钮
import streamlit as st
from PIL import Image
import json

#定义所有需要输入的函数
def bay_length(bay_length):
    bay_length = st.sidebar.number_input('货舱长度（>100mm）：',min_value=100,step=1)
    return bay_length

def bay_width(bay_width):
    bay_width = st.sidebar.number_input('货舱宽度（>100mm）：',min_value=100,step=1)
    return bay_width

def bay_height(bay_height):
    bay_height = st.sidebar.number_input('货舱高度（>100mm）：',min_value=100,step=1)
    return bay_height

def method(method):
    method=st.sidebar.radio('典型布置方式：',('居中布置','交错布置'))
    return method

def SD_qty(SD_qty):
    SD_qty = st.sidebar.number_input('货舱烟雾探测器数量（>1个）', min_value=1, value=8, step=1)
    return SD_qty

def Gap1(Gap1):
    Gap1 = st.sidebar.number_input('Gap1（>0mm）：',min_value=0,value=0,step=1)
    return Gap1

def Gap2(Gap2):
    Gap2 = st.sidebar.number_input('Gap2（>0mm）：',min_value=0,value=0,step=1)
    return Gap2

def displacement(displacement):
    displacement = st.sidebar.number_input(' Displacement（>0mm）：',min_value=0,value=0,step=1)
    return displacement

def parameter(P):
    P = st.sidebar.radio('货舱烟雾探测器设备参数定义方式选择：', ('默认（C919的烟雾探测参数）', '自定义'))
    return P

def Sen(Sen):
    Sen = st.sidebar.slider('货舱烟雾探测器灵敏度（0.1~1.0）', min_value=0.1, max_value=1.0, value=0.5, step=0.1)
    return Sen

def FAR(FAR):
    FAR = st.sidebar.slider('货舱烟雾探测器虚警率（0.0~1.0）', min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    return FAR

def SD_len(SD_len):
    SD_len = st.sidebar.number_input('货舱烟雾探测器的长度（>10mm）：', min_value=10, step=1)
    return SD_len

def SD_width(SD_width):
    SD_width = st.sidebar.number_input('货舱烟雾探测器的宽度（>10mm）：', min_value=10, step=1)
    return SD_width

def criteria(criteria):
    criteria = st.sidebar.number_input('货舱烟雾探测系统的响应时间要求（>1s）', min_value=1,value=60, step=1)
    return criteria

def Type(Type):
    Type = st.sidebar.text_input('本次仿真分析的飞机型号为', '请输入')
    return Type

def x_interval(x_interval):
    x_interval = st.sidebar.number_input('烟雾源移动步长间隔（X向）（>1mm）', min_value=1, value=1, step=1)
    return x_interval

def y_interval(y_interval):
    y_interval = st.sidebar.number_input('烟雾源移动步长间隔（Y向）（>1mm）', min_value=1, value=1, step=1)
    return y_interval

#生成网页界面，调用输入函数
st.sidebar.title('参数设置')
st.title('货舱烟雾探测系统设计平台')
st.sidebar.header('1.设置货舱尺寸')
if st.sidebar.button('货舱尺寸示意图'):
    st.header('货舱尺寸')
    bay_fig=Image.open('bay_fig.bmp')
    st.image(bay_fig,width=512)
l=bay_length(1)
w=bay_width(1)
h=bay_height(1)

st.sidebar.header('2.设置货舱烟雾探测器布置参数')
if st.sidebar.button('布置方式示意图'):
    st.header('货舱烟雾探测器布置参数')
    center = Image.open('center.jpg')
    st.image(center, width=512)
    side = Image.open('side.jpg')
    st.image(side, width=512)
m=method(0)
q=SD_qty(8)
G1=Gap1(0)
G2=Gap2(0)
d=displacement(0)


st.sidebar.header('3.设置货舱烟雾探测器设备参数')
# parameter('C919')
S=Sen(0)
F=FAR(0)
Sl=SD_len(0)
Sw=SD_width(0)

st.sidebar.header('4.设置仿真环境参数')
c=criteria(0)
T=Type(0)
x=x_interval(0)
y=y_interval(0)

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