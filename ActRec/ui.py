import wx 
import wx.grid 
import os 
import time 
import controller 

ID_BUTTON=100
ID_EXIT=200
ID_SPLITTER=300

ID_ADD_FLUENTS = 401
ID_ADD_ACTIONS = 402
ID_ADD_RULE = 403

ID_SET_INIT_STATE = 410
ID_SET_FINAL_STATE = 411




class ActRec(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size=(800,600))

        filemenu= wx.Menu()
        filemenu.Append(ID_ADD_FLUENTS, "Add &Fluents", "Add fluents")
        filemenu.Append(ID_ADD_ACTIONS, "Add &Actions", "Add actions")
        filemenu.Append(ID_ADD_RULE, "Add &Rules", "Add new rules")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")
        
        editmenu = wx.Menu()

        activitymenu = wx.Menu()
        activitymenu.Append(ID_SET_INIT_STATE, "Set &Initial State", "Set initial state")
        activitymenu.Append(ID_SET_FINAL_STATE, "Set &Final state", "Set final State")

        # showmenu = wx.Menu()
        # configmenu = wx.Menu()
        # helpmenu = wx.Menu()

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(activitymenu, "&Activity")
        # menuBar.Append(netmenu, "&Net")
        # menuBar.Append(showmenu, "&Show")
        # menuBar.Append(configmenu, "&Config")
        # menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAddFluents, id=ID_ADD_FLUENTS)
        self.Bind(wx.EVT_MENU, self.OnAddActions, id=ID_ADD_ACTIONS)
        # to be implemented
        self.Bind(wx.EVT_MENU, self.OnAddRule, id=ID_ADD_RULE)
        self.Bind(wx.EVT_MENU, self.OnSetInitState, id=ID_SET_INIT_STATE)
        self.Bind(wx.EVT_MENU, self.OnSetFinalState, id=ID_SET_FINAL_STATE)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # size = wx.DisplaySize()
        # self.SetSize(size)

        self.sb = self.CreateStatusBar()
        self.sb.SetStatusText(os.getcwd())
        self.Center()
        self.Show(True)


    def OnExit(self, e):
        self.Close(True)

    def OnAddFluents(self, e): 
        addf = AddFluentDialog(None, 
            title="Add Fluents")
        addf.ShowModal() 
        addf.Destroy()

    def OnAddActions(self, e): 
        addc = AddFluentDialog(None, 
            title="Add Actions")
        addc.ShowModal() 
        addc.Destroy()

    def OnAddRule(self, e): 
        pass 

    def OnSetInitState(self, e): 
        pass 

    def OnSetFinalState(self, e):
        pass 

class AddFluentDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(AddFluentDialog, self).__init__(*args, **kw) 
            
        self.InitUI()
        self.SetSize((300, 400))
        self.SetTitle("Add Fluents")
    
    def InitUI(self):

        panel = wx.Panel(self)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)


        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Fluents separated by comma:')
        st2.SetFont(font)
        hbox2.Add(st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(self.tc2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, 
            border=10)

        vbox.Add((-1, 25))


        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        addButton = wx.Button(panel, label='Ok', size=(70, 30))
        hbox5.Add(addButton)
        clearButton = wx.Button(panel, label='Reset DB', size=(70, 30))
        hbox5.Add(clearButton)
        closeButton = wx.Button(panel, label='Close', size=(70, 30))
        hbox5.Add(closeButton, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)


        addButton.Bind(wx.EVT_BUTTON, self.OnAddFluents)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        clearButton.Bind(wx.EVT_BUTTON, self.OnClearTable)
        
        
    def OnClose(self, e):
        self.Destroy()

    def OnAddFluents(self, e):
        txt = self.tc2.GetValue()
        controller.add_fluent_string(txt)
        dial = wx.MessageDialog(None, 'Fluents added.', 'Info', wx.OK)
        dial.ShowModal()

    def OnClearTable(self, e):
        controller.clear_table('Fluent')

# class AddActionDialog(wx.Dialog):
#     def __init__(self, *args, **kw):
#         super(AddActionDialog, self).__init__(*args, **kw) 
            
#         self.InitUI()
#         self.SetSize((300, 400))
#         self.SetTitle("Add Actions")
    
#     def InitUI(self):

#         panel = wx.Panel(self)

#         font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
#         font.SetPointSize(9)

#         vbox = wx.BoxSizer(wx.VERTICAL)


#         hbox2 = wx.BoxSizer(wx.HORIZONTAL)
#         st2 = wx.StaticText(panel, label='Actions separated by comma:')
#         st2.SetFont(font)
#         hbox2.Add(st2)
#         vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

#         vbox.Add((-1, 10))

#         hbox3 = wx.BoxSizer(wx.HORIZONTAL)
#         self.tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
#         hbox3.Add(self.tc2, proportion=1, flag=wx.EXPAND)
#         vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, 
#             border=10)

#         vbox.Add((-1, 25))


#         hbox5 = wx.BoxSizer(wx.HORIZONTAL)
#         addButton = wx.Button(panel, label='Add', size=(70, 30))
#         hbox5.Add(addButton)
#         closeButton = wx.Button(panel, label='Close', size=(70, 30))
#         hbox5.Add(closeButton, flag=wx.LEFT|wx.BOTTOM, border=5)
#         vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

#         panel.SetSizer(vbox)


#         addButton.Bind(wx.EVT_BUTTON, self.OnAddActions)
#         closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        
        
#     def OnClose(self, e):
        
#         self.Destroy()

#     def OnAddActions(self, e):
#         txt = self.tc2.GetValue()
#         print txt
#         dial = wx.MessageDialog(None, 'Actions added', 'Info', wx.OK)
#         dial.ShowModal()

app = wx.App(0)
ActRec(None, -1, 'ActRec ')
app.MainLoop()