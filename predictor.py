# -*- coding:utf-8  -*-

import os
import json
from time import time
import pickle
import pandas as pd
import SimpleGUI
import wx
import myAUI
from Detector import Detector
from cargobay import CargoBay
from Environment import Environment
from multiprocessing import Process,Queue

LOAD_DEF = True
process_msg = '' #需传递给GUI的过程信息

def load_model(model_file):  # load model
    with open(model_file, 'rb') as f:
        predictor = pickle.load(f)
    return predictor


def ReadInputs(inputs_file):
    with open(inputs_file, 'r', encoding='utf-8')as read_file:
        inputs = json.load(read_file)

    return inputs


def check_status(parameter_list):  # 检查所有输入数据是否正确
    pass


def read_sd(data_path):
    pass


def print_results(summary, data_path='test_result.csv'):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df_res = pd.read_csv(data_path)

        print('\n\n\n------------Test Summary--------------\n\n\n')
        print('Type:{:>10}\n\n'.format(summary['Type']))
        print('Time elapsed:{:.2f} seconds\n\n'.format(summary['Time']))
        print('Fail Test counts:{:d}\n\n'.format(
            len(df_res[df_res.Alarm == False])))
        print(df_res.to_string())

def message_get(msg_queue):
    global process_msg
    while True:
        process_msg = msg_queue.get(True)
        # print ('this msg is from main')
        print('internal'+ process_msg)

    # return msg

# def message_output(msg_queue):
#     msg_queue.put(process_msg)

def RunMain(msg_pipe):
    # 输入cargobay几何数据
    # 输入SD几何数据
    # 初始化仿真数据
    # 初始化各种参数

    if LOAD_DEF:
        inputs = ReadInputs('default.json')  # load inputs
    else:
        inputs = ReadInputs('inputs.json')
    airplaneType = inputs['Type']
    SD_qty = int(inputs['SD_qty'])
    bay_width = inputs['bay_width']
    bay_length = inputs['bay_length']
    bay_height = inputs['bay_height']
    Time_Crit = inputs['criteria']
    arrange_method = inputs['method']
    SD_len = inputs['SD_len']
    SD_width = inputs['SD_width']
    SD_FAR = inputs['FAR']
    arrange = {
        'method': inputs['method'],
        'fwd_gap': inputs['Gap1'],
        'aft_gap': inputs['Gap2'],
        'displace': inputs['displace']
    }
    move_interval = [inputs['x_interval'],inputs['y_interval']]

    SD_predictor = load_model(os.getcwd()+'\\rf_model_all_new.model')
    FWD_cargobay = CargoBay(
        width=bay_width, length=bay_length, height=bay_height)
    dets = [Detector(SD_predictor, (SD_width, SD_len), name='SD' +
                     str(i+1), FalseAlarmRate=SD_FAR) for i in range(SD_qty)]

    Env1 = Environment(
        cargobay_obj=FWD_cargobay,
        detector_series=dets,
        detector_qty=SD_qty,
        arrange=arrange,
        time_criteria=Time_Crit,
        move_interval=move_interval
    )

#创建两个进程，一个用于运行预测器，一个读取预测器中每步输出的信息

    # msg_queue = Queue() #Env->main 传输数据

    # msg_put = Process(target= Env1.run,args=(msg_queue,'all',))
    # msg_get = Process(target=message_get,args=(msg_queue,))

# 启动预测器
    Start_T = time()
    Env1.run(msg_pipe = msg_pipe,mode='all')
    # Env1.run(mode='all')
    # msg_put.start()
    # msg_get.start()

    print('external++++++++++++++++++++\n')
    # print(process_msg)
    # msg_put.join()  #阻塞操作，一道队列所有的任务都处理
    msg_pipe.put(Env1.process_message) #向GUI传输数据，main->GUI
#------------------------------------------

    End_T = time()

    # msg_get.terminate()

    runs_summary = {
        'Type': airplaneType,
        'Date': 'tbd',
        'Time': End_T-Start_T
    }

    print_results(runs_summary)


if __name__ == "__main__":
    # main()
    # app = SimpleGUI.MyGUIApp(redirect=False,useBestVisual=True)
    app = wx.App()

    AUIfrm = myAUI.MainAUI(None)
    app.SetTopWindow(AUIfrm)
    AUIfrm.Show()
    app.MainLoop()
