# -*- coding:utf-8 -*-

import os
import wx
import GenericPanel
import wx.lib.agw.aui as aui
from core import SimulatorModel
image_path = os.getcwd()+"\\src\\Images\\"


class MainAUI(wx.Frame):
    def __init__(self, parent, id=-1, title="Smoke Detection System Simulator",
                 size=(1248, 1024), style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent=parent, id=id, title=title,
                          size=size, style=style)
        self.core_model = SimulatorModel  # 创建底层模型
        self._mgr = aui.AuiManager()

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)

        # create text controls
        # text1 = wx.TextCtrl(self,-1,"System Structure",
        #                     wx.DefaultPosition,wx.Size(200,150),
        #                     wx.NO_BORDER|wx.TE_MULTILINE)

        self.text2 = wx.TextCtrl(self, -1, "Main Window",
                            wx.DefaultPosition, wx.Size(200, 150),
                            wx.NO_BORDER | wx.TE_MULTILINE)

        self.text3 = wx.TextCtrl(self, -1, "Log Window",
                            wx.DefaultPosition, wx.Size(200, 150),
                            wx.NO_BORDER | wx.TE_MULTILINE)

        # panel1 = wx.Panel(self,-1,size=wx.Size(200,150))
        self.treepnl = TreeCtrlPanel(self, wx.Size(200, 150))
        # Set pane 1 parameters

        paneinfo1 = aui.AuiPaneInfo()
        paneinfo1.Dock()
        paneinfo1.Left()
        paneinfo1.Floatable(False)
        paneinfo1.Caption("System Structure")
        paneinfo1.CloseButton(False)

        # Set pane 2 parameters
        paneinfo2 = aui.AuiPaneInfo()
        paneinfo2.Dock()
        paneinfo2.Center()
        paneinfo2.Floatable(False)
        paneinfo2.Caption("Main Window")
        paneinfo2.CloseButton(False)

        # Set pane 3 parameters
        paneinfo3 = aui.AuiPaneInfo()
        paneinfo3.Dock()
        paneinfo3.Bottom()
        paneinfo3.Floatable(False)
        paneinfo3.Caption("Log Window")
        paneinfo3.CloseButton(False)

        # add the panes to the manager

        self._mgr.AddPane(self.treepnl, paneinfo1)
        self._mgr.AddPane(self.text2, paneinfo2)
        self._mgr.AddPane(self.text3, paneinfo3)

        self._mgr.Update()

        self.CreateMenuBar()  # create menu

    def OnClose(self, evt):
        self._mgr.UnInit()
        evt.Skip()

    def OnExit(self, e):
        self.Close(True)

    def OnSetEnv(self, evt):
        frm = wx.Frame(self, -1, title="环境设置", size=(790, 600))
        pnl = wx.Panel(frm, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.nb = SystemSettingPage(pnl, -1)
        sizer.Add(self.nb, 1)
        OkBtn = wx.Button(pnl,label='OK')
        CancelBtn = wx.Button(pnl,label='Cancel')
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddMany([OkBtn,CancelBtn])
        sizer.Add(hbs,0,wx.ALIGN_RIGHT)

        pnl.SetSizer(sizer)
        frm.Show()
        self.Bind(wx.EVT_BUTTON,self.OnConfirmBtn,OkBtn)
        
    def OnSetSD(self, evt):
        pass

    def OnSetModel(self, evt):
        pass

    def OnAbout(self, e):
        description = """ This is a generic aircraft smoke detection system simulator
        by machine learning

        Under developing

        """

        licence = """
        TBD
        """
        icon_path = os.path.join(image_path, 'icon_about.png')

        info = wx.adv.AboutDialogInfo()

        info.SetIcon(wx.Icon(icon_path, wx.BITMAP_TYPE_PNG))
        info.SetName('Smoke Detection System Simulator')
        info.SetVersion('0.1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2018 Xuan Yang. All rights reserved')
        info.SetWebSite('')
        info.SetLicence(licence)
        info.AddDeveloper('Xuan Yang')
        info.AddDocWriter('Xuan Yang')

        wx.adv.AboutBox(info)

    def OnConfirmBtn(self, evt):
        print("ok pressed")
        values = self.nb.GetValues()
        self.text3.AppendText(str(values))
        
        


    def CreateMenuBar(self):

        # create menu
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)

        file_menu = wx.Menu()
        menuOpen = file_menu.Append(wx.ID_OPEN, "&Open", "打开数据文件")
        menuExit = file_menu.Append(wx.ID_EXIT, "E&xit", "退出")
        menubar.Append(file_menu, "文件")
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        model_menu = wx.Menu()
        menuEnv = model_menu.Append(wx.ID_ANY, "设置环境参数", "设置预测模型的环境参数")
        menuSD = model_menu.Append(wx.ID_ANY, "设置烟雾探测器", "设置烟雾探测器")
        menuload = model_menu.Append(wx.ID_ANY, "读取模型", "读取预测模型")
        menubar.Append(model_menu, "创建模型")
        # self.Bind(wx.EVT_MENU, self.OnSetSmokeDetector, menuSD)

        run_menu = wx.Menu()
        menurun = run_menu.Append(wx.ID_ANY, "运行", "开始模拟")
        # self.Bind(wx.EVT_MENU, self.OnRun, menurun)

        about_menu = wx.Menu()
        menuabt = about_menu.Append(wx.ID_ABOUT, "关于", "关于本软件的信息")
        menubar.Append(about_menu, "关于")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuabt)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_MENU, self.OnSetEnv, menuEnv)


class TreeCtrlPanel(wx.Panel):
    def __init__(self, parent, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, id=-1, size=size,
                          style=wx.WANTS_CHARS | wx.EXPAND | wx.ALL)
        self.tree = wx.TreeCtrl(self, -1, wx.DefaultPosition, size=size,
                                style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS)

        self.root = self.tree.AddRoot("Fwd cargo bay")
        self.tree.SetItemData(self.root, None)

        for x in range(10):
            child = self.tree.AppendItem(
                self.root, "smoke detector {}".format(str(x)))
            # self.tree.SetItemData(child, None)

        self.tree.Expand(self.root)

        treesizer = wx.BoxSizer(wx.VERTICAL)
        treesizer.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(treesizer)


class SystemSettingPage(wx.Notebook):
    def __init__(self, parent, id):
        wx.Notebook.__init__(self, parent, id, size=(1600, 1200),
                             style=wx.BK_DEFAULT)

        self.param ={}

        # Create tab pages
        self.page_env = GenericPanel.SimplePage(self, -1)
        self.page_sys = GenericPanel.SimplePage(self, -1)
        self.page_det = GenericPanel.SimplePage(self, -1)
        self.page_sim = GenericPanel.SimplePage(self, -1)

        # Layout page

        self.CreatePageEnv(self.page_env)
        self.CreatePageSys(self.page_sys)
        self.CreatePageDet(self.page_det)
        self.CreatePageSim(self.page_sim)

        self.AddPage(self.page_env, "货舱设置")
        self.AddPage(self.page_sys, "系统布置")
        self.AddPage(self.page_det, "探测器设置")
        self.AddPage(self.page_sim, "仿真参数")
        #TODO: 用循环优化这段代码

    def CreatePageEnv(self, parent):  # 创建货舱环境设置页面

        labels = ['长(mm)', '宽(mm)', '高(mm)']
        ctrlnames = ['bay_length', 'bay_width', 'bay_height']

        # layout page
        # parent.ChangeSizer(wx.BoxSizer(wx.HORIZONTAL))  # 调整sizer方向
        box1 = wx.StaticBox(parent, -1, "货舱尺寸设置")
        bsizer1 = wx.BoxSizer()
        bsizer1.Add(parent.InputBox(
            box1, labels, ctrlnames), 0, wx.ALL, 50)
        box1.SetSizer(bsizer1)
        parent.sizer.Add(box1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        # parent.sizer.Add(wx.StaticLine(parent, -1), 0, wx.EXPAND)

        parent.sizer.Add(self.GenerateScaledBitmap(
            parent, image_path+"bay_fig.bmp", 2), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 50)

    def CreatePageSys(self, parent):  # 创建探测系统设置页面

        labels = ['探测器数量(个)', 'Gap1(mm)', 'Gap2(mm)', '偏移(mm)']
        ctrlnames = ['SD_qty', 'Gap1', 'Gap2', 'displace']
        radiolabels = ['居中布置', '交错布置']
        imgs = ["center.jpg", "side.jpg"]

        # layout page

        # layout left side widgets
        box1 = wx.RadioBox(parent, -1, "烟雾探测器布置形式", wx.DefaultPosition,
                           wx.Size(300, 100), radiolabels, 1, wx.RA_SPECIFY_COLS)

        imgsizer = wx.BoxSizer(wx.VERTICAL)

        for img in imgs:
            imgsizer.Add(self.GenerateScaledBitmap(
                parent, image_path+img, 10), 0, wx.ALL, 20)

        lsizer = wx.BoxSizer(wx.VERTICAL)
        lsizer.Add(imgsizer)
        lsizer.Add(box1, 0, wx.ALL, 10)

        # layout right side widgets
        rsizer = wx.BoxSizer(wx.HORIZONTAL)
        box2 = wx.StaticBox(parent, -1, "布置参数")
        bsizer = wx.BoxSizer(wx.VERTICAL)
        bsizer.Add(parent.InputBox(box2, labels, ctrlnames), 0, wx.ALL, 50)
        box2.SetSizer(bsizer)
        rsizer.Add(box2, 0, wx.LEFT, 30)

        # layout whole page
        parent.ChangeSizer(wx.BoxSizer(wx.HORIZONTAL))
        parent.sizer.Add(lsizer)
        parent.sizer.Add(wx.StaticLine(
            parent, -1, style=wx.LI_VERTICAL), 0, wx.EXPAND)
        parent.sizer.Add(rsizer)

        self.Bind(wx.EVT_RADIOBOX, self.OnRadioBoxSys, box1)  # 响应radiobox事件


    def CreatePageDet(self, parent):  # 创建探测器设置页面
        labels = ['灵敏度(0.1~1)', '虚警率(0~1)', '探测器-长(mm)', '探测器-宽(mm)']
        ctrlnames = ['Sen', 'FAR', 'SD_len', 'SD_width']

        radiobox = wx.RadioBox(parent, -1, "参数输入模式", choices=['默认', '自定义'])

        box = wx.StaticBox(parent, -1, "探测器参数")
        bsizer = wx.BoxSizer(wx.VERTICAL)
        bsizer.Add(parent.InputBox(box, labels, ctrlnames), 0, wx.ALL, 50)
        box.SetSizer(bsizer)

        parent.sizer.Add(radiobox, 0, wx.ALIGN_CENTER | wx.TOP, 50)
        parent.sizer.Add(wx.Size(0, 50))
        parent.sizer.Add(box, 0, wx.ALIGN_CENTER)

    def CreatePageSim(self, parent):  # 创建模拟参数页面
        labels = ['响应时间标准(秒)', '型号', '烟雾移动间隔(X向)', '烟雾移动间隔(Y向)']
        ctrlnames = ['criteria', 'Type', 'x_interval', 'y_interval']

        radiobox = wx.RadioBox(parent, -1, "选择预测模型", choices=['默认模型', '自定义模型'])

        box = wx.StaticBox(parent, -1, "模拟参数")
        bsizer1 = wx.BoxSizer(wx.VERTICAL)
        bsizer1.Add(parent.InputBox(box, labels, ctrlnames), 0, wx.ALL, 50)
        box.SetSizer(bsizer1)

        bsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        bsizer2.Add(box, 0, wx.ALIGN_LEFT | wx.RIGHT, 50)
        bsizer2.Add(self.GenerateScaledBitmap(
            parent, image_path+'smoke_src.jpg', 1))
        parent.sizer.Add(radiobox, 0, wx.ALIGN_CENTER | wx.TOP, 50)
        parent.sizer.Add(wx.Size(0, 50))
        parent.sizer.Add(bsizer2)

    def GetValues(self):
        ctrlnames = ['bay_length', 'bay_width', 'bay_height']
        values = self.page_env.GetPageValueByName(ctrlnames)
        print(values)
        


    # Event Handler
    def OnRadioBoxSys(self, evt):
        # print(evt.GetInt())
        method = "center" if evt.GetInt() == 0 else "side"

        self.param['method']=method


    def GenerateScaledBitmap(self, parent, imagepath, scale=2):
        img = self._ScaleBitmap(imagepath, scale)
        img_sb = wx.StaticBitmap(parent, -1, img)
        # parent.sizer.Add(img_sb)
        return img_sb

    def _ScaleBitmap(self, bitmap, scale=2):
        '''
        bitmap: bitmap name in wx.ImageFromBitmap
        scale: scale factor
        '''
        image = wx.Image(bitmap, wx.BITMAP_TYPE_ANY)
        w = image.GetWidth()
        h = image.GetHeight()
        image = image.Scale(w/scale, h/scale, wx.IMAGE_QUALITY_HIGH)
        img = wx.Bitmap(image)
        return img

#TODO:读取每个页面的参数 目前读不出来
#TODO: 添加各个事件响应函数
#TODO: 处理设置界面关闭时候的数据
# TODO: 创建一个接口,向log window里面输出参数设置完毕的信息
#TODO: 优化MCV模型
