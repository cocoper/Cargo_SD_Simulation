import os
import wx
import json
import wx.adv


image_path = os.getcwd()+"\\src\\Images\\"


class SimplePage(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id,size=(1600,1200))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.Add(wx.StaticText(self,-1,"test"))
        # self.sizer.Add(wx.TextCtrl(self,-1,style=wx.TE_PROCESS_ENTER))
        data={'a':'123'}
        self.validator = DataXferValidator(data, "name")
        self.SetSizer(self.sizer)

    def InputBox(self,parent,labels, names):
        """
        Create "label:text ctrl "style widgets
        """
        rows = len(labels)
        cols = 2
        fgs = wx.FlexGridSizer(rows=rows, cols=cols, hgap=10, vgap=20)
        for label, name in zip(labels, names):
            fgs.Add(wx.StaticText(parent, -1, label),
                    wx.ALL | wx.ALIGN_LEFT, 0)
            inputText = wx.TextCtrl(parent,
                        style=wx.TE_PROCESS_ENTER,
                        validator=self.validator)
            inputText.SetInsertionPoint(0)
            fgs.Add(inputText)

        return fgs

    def _GetValueFromSizer(self, sizeritems):
        value = {}
        for child in sizeritems:
            sub_sizer = child.GetSizer()
            if sub_sizer:
                for child in sub_sizer:
                    widget = child.GetWindow()
                    if isinstance(widget, wx.TextCtrl):
                        try:
                            value[widget.GetName()] = float(widget.GetValue())
                        except:
                            value[widget.GetName()] = widget.GetValue()

    def _GetValueByName(self,name): #按照name获取单个文本控件的值并实施类型转换
        
        ctrl = wx.FindWindowByName(name,self)
        #TODO :这里有逻辑问题,只会返回None
        if isinstance(ctrl,wx.TextCtrl): #判断是否是文本控件
            try:
                value = float(ctrl.GetValue()) #尝试强制将string类型转换成float类型
                return value
            except:
                value = ctrl.GetValue()  #如果不能转换成float,返回string类型
                if value == "":   #如果是空值,返回0,否则返回应该有的值
                    return 0
                else:
                    return value
        else:
            return None #如果不是文本控件,返回None

    def GetPageValueByName(self,names): #获取整个页面的数据by name
        values = {}
        for name in names:
            values[name] = self._GetValueByName(name)
        return values

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
    
    def ChangeSizer(self,sizer):
        self.sizer = sizer
        self.SetSizer(self.sizer)


class DataXferValidator(wx.Validator):
    def __init__(self, data, key):
        wx.Validator.__init__(self)
        self.data = data
        self.key = key

    def Clone(self):
        return DataXferValidator(self.data, self.key)

    def Validate(self, win):
        pass

    def TransferToWindow(self):
        textctrl = self.GetWindow()
        textctrl.SetValue(self.data.get(self.key, ""))
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        self.data[self.key] = textCtrl.GetValue()
        return True
