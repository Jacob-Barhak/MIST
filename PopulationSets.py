################################################################################
###############################################################################
# Copyright (C) 2013-2014 Jacob Barhak
# Copyright (C) 2009-2012 The Regents of the University of Michigan
# 
# This file is part of the MIcroSimulation Tool (MIST).
# The MIcroSimulation Tool (MIST) is free software: you
# can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
# 
# The MIcroSimulation Tool (MIST) is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
###############################################################################
# 
# ADDITIONAL CLARIFICATION
# 
# The MIcroSimulation Tool (MIST) is distributed in the 
# hope that it will be useful, but "as is" and WITHOUT ANY WARRANTY of any 
# kind, including any warranty that it will not infringe on any property 
# rights of another party or the IMPLIED WARRANTIES OF MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. THE AUTHORS assume no responsibilities 
# with respect to the use of the MIcroSimulation Tool (MIST).  
# 
# The MIcroSimulation Tool (MIST) was derived from the Indirect Estimation  
# and Simulation Tool (IEST) and uses code distributed under the IEST name.
# The change of the name signifies a split from the original design that 
# focuses on microsimulation. For the sake of completeness, the copyright 
# statement from the original tool developed by the University of Michigan
# is provided below and is also mentioned above.
# 
###############################################################################
############################ Original Copyright ###############################
###############################################################################
# Copyright (C) 2009-2012 The Regents of the University of Michigan
# Initially developed by Deanna Isaman, Jacob Barhak, Donghee Lee
#
# This file is part of the Indirect Estimation and Simulation Tool (IEST).
# The Indirect Estimation and Simulation Tool (IEST) is free software: you
# can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# The Indirect Estimation and Simulation Tool (IEST) is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
################################################################################
#                                                                              #
# This file contains a form to define PopulationSet                            #
################################################################################




import DataDef as DB
import CDMLib as cdml
import wx, wx.grid
import copy


class RowPanel(cdml.CDMPanel):
    """ RowPanel class for PopulationSets"""

    def __init__(self, *args, **kwds):
        """ Constructor of RowPanel class"""

        kwdsnew = copy.copy(kwds)
        kwdsnew['style'] = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL
        cdml.CDMPanel.__init__(self, True, *args, **kwdsnew) # initialize

        # Create variables using PopulationSet class and initialize those variables
        # using initial values defined in PopulationSet Class
        self.record = cdml.GetInstanceAttr(DB.PopulationSet)

        # Create temporary variable to keep input for DataColumns and Data
        self.DataColumns = []
        self.Data = []
        self.Objectives = []
        
        # Add Button and StaticText for deletion and status display
        self.btn_del = cdml.Button(self, wx.ID_DELETE, "x", style=wx.BU_EXACTFIT)
        self.st_status = wx.StaticText(self, -1, " ")

        # Create controls to enter/display the variables in Transition object
        # For controls include text area set wx.TE_NOHIDESEL always.
        # This style need for the Find function
        self.tc_name = cdml.Text(self, -1, "", style=wx.TE_NOHIDESEL)
        self.tc_definitiontype = cdml.Text(self, -1, "", style=wx.TE_NOHIDESEL, validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.tc_source = cdml.Text(self, -1, "", style=wx.TE_NOHIDESEL)
        # keep the derived from status in addition to the text box
        self.DerivedFrom = 0
        self.tc_derived = cdml.Text(self, -1, "", style=wx.TE_NOHIDESEL, validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.tc_created = cdml.Text(self, -1, "", validator=cdml.KeyValidator(cdml.NO_INPUT))
        self.tc_modified = cdml.Text(self, -1, "", validator=cdml.KeyValidator(cdml.NO_INPUT))
        self.tc_notes = cdml.Text(self, -1, "", style=wx.TE_MULTILINE|wx.TE_NOHIDESEL)

        #self.btn_copy = cdml.Button(self, cdml.IDP_BUTTON1, "Copy")
        self.btn_data = cdml.Button(self, cdml.IDP_BUTTON3, "Data")

        self.__set_properties()
        self.__do_layout()


    def __set_properties(self):
        """ Set properties of panel and controls """

        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))

        self.btn_del.SetMinSize((20, 20))

        self.st_status.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.tc_name.SetMinSize((150, -1))
        self.tc_definitiontype.SetMinSize((150, -1))
        self.tc_derived.SetMinSize((150, -1))
        self.tc_source.SetMinSize((150, -1))
        self.tc_created.SetMinSize((120, -1))
        self.tc_modified.SetMinSize((120, -1))
        self.tc_notes.SetMinSize((215, -1))


        # Set Sort Id and Data Type of a control
        # The sortId should be matched to the sortId of field title in the 
        # title section. If sortId is not set, no action occurs when user click
        # the field title
        self.tc_name.sortId = 1
        self.tc_source.sortId = 2
        self.tc_definitiontype.sortId = 3

        #self.cb_read_only.sortId = 5

        self.tc_created.sortId = 6
        self.tc_created.dataType = cdml.ID_TYPE_NONE

        self.tc_modified.sortId = 7
        self.tc_modified.dataType = cdml.ID_TYPE_NONE

        self.tc_notes.sortId = 8

        # Assign event handler that need to respond after checking the focus 
        # change
        # Syntax : tuple, (EventType, ActionID, Event Handler)
        # ventType should be None always( Not used in current version)
        # Valid value of EventId are ID_EVT_OWN and ID_EVT_SORT
        # If EventID is ID_EVT_OWN, third argument (i.e name of event handler) 
        # should be defined
        # If EventID is ID_EVT_SORT, FrameEventHandler deals that event. Thus, 
        # event handler need not to be defined
        btn_evt = ( None, cdml.ID_EVT_OWN, self.OnButtonClick)

        self.btn_data.SetEvent(btn_evt)


    def __do_layout(self):
        """ Set position of controls """

        sizer = wx.GridBagSizer(0,0)

        sizer.Add(self.btn_del,     (0, 0),         flag = wx.ALL, border = 1)
        sizer.Add(self.st_status,   (1, 0),         flag = wx.ALL, border = 1)

        sizer.Add(self.tc_name, (0, 1),             flag = wx.ALL, border = 1)
        sizer.Add(self.tc_source,   (1, 1),         flag = wx.ALL, border = 1)

        sizer.Add(self.tc_definitiontype,  (0, 2),    flag = wx.wx.ALL, border = 1)
        sizer.Add(self.tc_derived,  (1, 2), (1,2),  flag = wx.ALL, border = 1)

        sizer.Add((10,0), (0, 3),        flag = wx.ALIGN_CENTER|wx.ALL, border = 1)
        sizer.Add(self.tc_created,  (0, 4),         flag = wx.ALL, border = 1)
        sizer.Add(self.tc_modified, (1, 4),         flag = wx.ALL, border = 1)

        sizer.Add(self.tc_notes,    (0, 5), (2,1), flag = wx.EXPAND|wx.ALL, border = 1 )

        sizer.Add(self.btn_data,    (0, 6), (1,1),  flag = wx.EXPAND|wx.ALL, border = 1)

        self.SetSizer(sizer)


    def GetValues(self):
        """
        Retrieve current values in a row panel.
        RowPanel class must implement this method.
        """

        # create a copy of field variables
        record = copy.copy(self.record)

        record.ID = self.Key
        record.Name =  str(self.tc_name.GetValue())

        record.Source = str(self.tc_source.GetValue())
        record.Notes =  str(self.tc_notes.GetValue())
        record.DerivedFrom = self.DerivedFrom

        record.DataColumns = copy.copy(self.DataColumns)
        record.Data = copy.copy(self.Data)
        record.Objectives = copy.copy(self.Objectives)

        return record


    def SetValues(self, record, init=False):
        """
        Write current data in controls on a row panel
        RowPanel class must implement this method.
        """

        self.Key = record.ID

        self.tc_name.SetValue(str(record.Name))
        self.tc_source.SetValue(str(record.Source))
        self.tc_created.SetValue(record.CreatedOn)
        self.tc_modified.SetValue(record.LastModified)
        self.tc_notes.SetValue(str(record.Notes))
        # Special treatment needed to discover if a record is distribution 
        # based
        if record.IsDistributionBased():
            self.tc_definitiontype.SetValue('Distribution based')
        else:
            self.tc_definitiontype.SetValue('Data based')
        
        from_pset = cdml.GetRecordByKey( DB.PopulationSets, record.DerivedFrom)
        if from_pset:
            self.tc_derived.SetValue(str(from_pset.Name))
        self.DerivedFrom = record.DerivedFrom
        
        self.DataColumns = record.DataColumns
        self.Data = record.Data
        self.Objectives = record.Objectives
        


    def SaveRecord(self, record):
        """
        Save/Modify the data of StudyModel object
        This method is called by CheckFocus mehtod in CDMLib
        RowPanel class must implement this method.
        """

        # create new PopulationSet instance
        entry = DB.PopulationSet(   ID = 0,
                                    Name = str(record.Name),
                                    Notes = str(record.Notes),
                                    Source = str(record.Source),
                                    DerivedFrom = record.DerivedFrom,
                                    DataColumns = record.DataColumns,
                                    Data = record.Data,
                                    Objectives = record.Objectives)


        frame = self.GetTopLevelParent()
        if self.Id == 0:    # if previous panel is new, create new object
            entry = DB.PopulationSets.AddNew(entry, ProjectBypassID = frame.idPrj)

        elif self.Id > 0:   # if previous panel is existing one, replace record
            entry = DB.PopulationSets.Modify(self.Key, entry, ProjectBypassID = frame.idPrj)

        return entry



    def TextRecordID(self):
        """ Returns the identity of the record as text """
        if self.Id == 0:
            Result = 'New Population Set'
            RecordName = None
        else:
            RecordName = self.record.Name
            Result = 'Population Set saved as "' + str(RecordName) + '"'
        DisplayName = self.tc_name.GetValue()
        if DisplayName != RecordName:
           Result = Result + ' currently edited to "' + str(DisplayName) + '"'
        return Result        


    # Following methods are dedicated to the instance of RowPanel class for States form
    def OnButtonClick(self, event):
        """ Method to respond the action taken by user"""

        id = event.GetId()

        if id == cdml.IDP_BUTTON1:  # Copy this set
            cdml.dlgNotPrepared()

        elif id == cdml.IDP_BUTTON2:    # PopulationStructure
            cdml.dlgNotPrepared()

        elif id == cdml.IDP_BUTTON3:    # PopulationData
            frame = self.GetTopLevelParent()

            if self.Id == 0:
                PopulationID = None
            else:
                PopulationID = self.Key

            CurrentName = str(self.tc_name.GetValue())
            
            cdml.OpenForm('PopulationData', self, CurrentName, PopulationID, None, frame.idPrj )





class MainFrame(cdml.CDMFrame):
    """ MainFrame class for PopulationSets """
    def __init__(self, mode=None, data=None, type=None, id_prj=0, *args, **kwds):
        """ Constructor of the MainFrame class """
        self.idPrj = id_prj

        cdml.CDMFrame.__init__(self, mode, data, type, *args, **kwds)

        # Deine Popup menu items
        # Format : tuple of list --> ([Label, Event handler, Id] , [], [], ... )
        #           Label : label of an item
        #           Evet handler : name of event handler
        #           Id : Id of current menu item
        # Special label : '-'--> seperator, '+' --> submenu items
        #           First item after last '+' marked items is the title of the submenu
        # If an item doesn't have event handler, the second parameter should be 'None'
        # If an item doesn't have Id, the third item should be -1
        # If a form need to manage instances of RowPanel class,
        #   the event handler should be 'self.FrameEventHandler'
        # Otherwise, dedicated event handler should be implemented in that class (ex. see Project or PopulationData form)
        self.pup_menus = (  ["Undo", self.FrameEventHandler, wx.ID_UNDO ],
                            ["-" , None, -1],
                            ["Add" , self.FrameEventHandler, wx.ID_ADD],
                            ["Copy Record" , self.FrameEventHandler, cdml.ID_MENU_COPY_RECORD],
                            ["Delete" , self.FrameEventHandler, wx.ID_DELETE],
                            ["Regenerate New Population Data from a Distribution" , self.FrameEventHandler, cdml.ID_SPECIAL_RECORD_ADD],
                            ["-" , None, -1 ],
                            ["Find" , self.FrameEventHandler, wx.ID_FIND],
                            ["-" , None, -1 ],
                            ["+ID" , self.FrameEventHandler, cdml.IDF_BUTTON1],
                            ["+Name" , self.FrameEventHandler, cdml.IDF_BUTTON2],
                            ["+Source" , self.FrameEventHandler, cdml.IDF_BUTTON3],
                            ["+Definition Type" , self.FrameEventHandler, cdml.IDF_BUTTON4],
                            ["+Derived From" , self.FrameEventHandler, cdml.IDF_BUTTON5],
                            ["+Read Only" , self.FrameEventHandler, cdml.IDF_BUTTON6],
                            ["+Created On" , self.FrameEventHandler, cdml.IDF_BUTTON7],
                            ["+Last Modified" , self.FrameEventHandler, cdml.IDF_BUTTON8],
                            ["+Notes", self.FrameEventHandler, cdml.IDF_BUTTON9],
                            ["Sort By", None, -1])

        # Define the window menus 
        cdml.GenerateStandardMenu(self)

        # create panel for field titles
        # IMPORTANT NOTE:
        #   In current version, name of a panel for the title section should be "pn_title"
        #   And should be an instance of CDMPanel class with False as a first argument
        self.pn_title = cdml.CDMPanel(False, self, -1, style = wx.TAB_TRAVERSAL)
        self.st_title = wx.StaticText(self.pn_title, -1, "Population Sets")

        # Create bitmap buttons to display title of each field
        # Syntax : cdml.BitmapButton( parent, id, bitmap, label )
        # Don't need to set bitmap here. It will be assigned in the event handler when pressed
        # For the sort function, the labels need to be same with the variable name in database object
        self.button_2 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON2, None, "Name")
        self.button_3 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON3, None, "Source")
        self.button_4 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON4, None, "Definition Type")
        self.button_5 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON5, None, "Derived From")
        self.button_6 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON7, None, "Created On")
        self.button_7 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON10, None, "Last Modified")
        self.button_8 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON11, None, "Notes")

        # Create Add/Find buttons
        # Syntax : cdml.Button( parent, ID )
        # ID should be wx.ID_ADD for add button and wx.ID_FIND for find button in all forms
        self.btn_add = cdml.Button(self.pn_title, wx.ID_ADD)
        self.btn_find = cdml.Button(self.pn_title, wx.ID_FIND)

        # Scroll window that the RowPanel objects will be placed
        # IMPORTANT NOTE:
        #   In current version, all forms that need to manage the instance(s) of RowPanel class
        #       should have an instance of wx.ScrolledWindow class.
        #   Also the name of the panel should be "pn_view"
        self.pn_view = wx.ScrolledWindow(self, -1, style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)

        self.__set_properties()
        self.__do_layout()

        # Assign event handler for the buttons in title section -- to check the focus change
        self.pn_title.Bind(wx.EVT_BUTTON, self.FrameEventHandler, id=cdml.IDF_BUTTON2, id2=cdml.IDF_BUTTON9)
        self.btn_add.Bind(wx.EVT_BUTTON, self.FrameEventHandler)
        self.btn_find.Bind(wx.EVT_BUTTON, self.FrameEventHandler)

        self.Initialize()


    # Define the default method to handle the menu selections
    OnMenuSelected = cdml.OnMenuSelected
    

    def SpecialRecordAdd(self, ClickedPanel):
        """ Add a special record - In this case this means a new population set
            Generated from a distribution population set """
        if ClickedPanel != None:
            RecordID = ClickedPanel.Key
            if (RecordID == 0 or RecordID == None) or not DB.PopulationSets.has_key(RecordID):
                ReturnRecord = None
            else:
                if not DB.PopulationSets[RecordID].IsDistributionBased():
                    # This is a data population set
                    cdml.dlgSimpleMsg('ERROR', 'This population set is not based on distribution and therefore cannot be used to generate new population data', Parent = self)
                    ReturnRecord = None
                else:
                    # This means this population set is defined by distributions
                    dlg = wx.NumberEntryDialog(self, 'Define population size', 'Please enter the size of the population to generate ', 'Population Size', 1000, 0, 100000)
                    dlg.CenterOnScreen() 
                    if dlg.ShowModal() != wx.ID_OK:
                        # If 'Cancel' button is clicked
                        ReturnRecord = None
                    else:
                        NumberOfIndividuals = dlg.GetValue() # Get selection index
                        dlg.Destroy()
                        PopulationTraceBack = None
                        # When in admin mode, also ask for traceback info
                        AskForTraceBack = cdml.GetAdminMode()                     
                        if AskForTraceBack:
                            TraceBackText = cdml.dlgTextEntry(Message = 'Please enter the Pickled TraceBack information as appear in the hidden report of the population you are trying to reconstruct ', Caption = 'Enter Pickled TraceBack Info', DefaultValue = '', Parent = self)
                            if TraceBackText == '':
                                PopulationTraceBack = None
                            else:
                                try:
                                    PopulationTraceBack = DB.pickle.loads(TraceBackText)
                                except:
                                    raise ValueError, 'TraceBack Error: Could not properly extract TraceBack - please make sure a proper TraceBack was entered'
                                    PopulationTraceBack = None
                           
                        TheProgressDialog = None
                        try:
                            # version 2.5 does not support canceling simulation
                            TheProgressDialog = cdml.ProgressDialogTimeElapsed(Parent = self, StartTimerUponCreation = False, AllowCancel = DB.SystemSupportsProcesses)                            
                            # Define the Function to run on a thread/process
                            def GenerationStartMiniScript():
                                "Compile and execute the generation"
                                Pop = DB.PopulationSets[RecordID]
                                # Compile the generation script with default options
                                ScriptFileNameFullPath = Pop.CompilePopulationGeneration(GeneratedPopulationSize = NumberOfIndividuals, GenerationFileNamePrefix = None, OutputFileNamePrefix = None , RandomStateFileNamePrefix = None, GenerationOptions = None, RecreateFromTraceBack = PopulationTraceBack)
                                # run the generation script
                                DeleteScriptFileAfterRun = not cdml.GetAdminMode()
                                (ProcessList, PipeList) = Pop.RunPopulationGeneration(GenerationFileName = ScriptFileNameFullPath, NumberOfProcessesToRun = -1, DeleteScriptFileAfterRun = DeleteScriptFileAfterRun)
                                return (ProcessList, PipeList)
                            
                            def GenerationEndMiniScript(ProcessList, PipeList):
                                "Complete Generation by collecting results"
                                Pop = DB.PopulationSets[RecordID]
                                # Collect the results
                                RetVal = Pop.CollectResults(ProcessList, PipeList)
                                return RetVal
                            
                            ThreadObject = cdml.WorkerThread(GenerationStartMiniScript,GenerationEndMiniScript)
                            # Tell the dialog box what to do when cancel is pressed
                            TheProgressDialog.FunctionToRunUponCancel = ThreadObject.StopProcess
                            # Now start the timer for the progress dialog box
                            TheProgressDialog.StartTimer()
                            # wait until thread/process exits
                            Info = ThreadObject.WaitForJob() 
                            # Cancel through the dialog box is no longer possible
                            TheProgressDialog.FunctionToRunUponCancel = None
                            # Properly destroy the dialog 
                            
                            WasCanceled = TheProgressDialog.WasCanceled
                            TheProgressDialog.Destroy()
                            TheProgressDialog = None
                            
                            if WasCanceled:
                                cdml.dlgSimpleMsg('INFO', 'The Population generation was canceled by request!', wx.OK, wx.ICON_INFORMATION, Parent = self)
                                ReturnRecord = None
                            else:
                                cdml.dlgSimpleMsg('INFO', 'The Population generation has finished successfully! After you press OK your cursor will be focused on the new population set.', wx.OK, wx.ICON_INFORMATION, Parent = self)
                                ReturnRecord = Info
                        except:         
                            cdml.dlgErrorMsg()
                            ReturnRecord = None

                        # Properly destroy the progress dialog box if not done before
                        if TheProgressDialog != None:
                            TheProgressDialog.Destroy()

        return ReturnRecord

    def __set_properties(self):
        """ Set properties of panel and controls """

        self.SetTitle("Population Sets")
        self.SetSize((800, 600))
        self.SetCollection('PopulationSets')    # same as self.Collection = 'PopulationSets'
        self.HelpContext = 'PopulationSets'

        self.button_2.SetMinSize((150, -1))
        self.button_3.SetMinSize((150, -1))
        self.button_4.SetMinSize((150, -1))
        self.button_5.SetMinSize((150, -1))
        self.button_6.SetMinSize((120, -1))
        self.button_7.SetMinSize((120, -1))
        self.button_8.SetMinSize((225, -1))

        self.st_title.SetMinSize((500, -1))

        self.st_title.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

        bgcolor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE)
        self.pn_title.SetBackgroundColour(bgcolor)
        self.pn_view.SetScrollRate(10, 10)
        self.pn_view.SetMinSize((800, -1))

        # set sort id and event id for field titles
        for i in range(2,9):
            btn = getattr(self, 'button_' + str(i))
            btn.sortId = i-1
            btn.evtID = cdml.ID_EVT_SORT


    def __do_layout(self):
        """ Set position of controls """

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.GridBagSizer(0,0)

        gb_sizer = wx.GridBagSizer(0,0)
        gb_sizer1 = wx.GridBagSizer(0,0)

        gb_sizer1.Add((28,0), (0,0))

        gb_sizer1.Add(self.st_title, (0, 1), span=(1,5), flag = wx.ALL, border = 1)

        gb_sizer1.Add(self.btn_add, (0,9), flag = wx.ALL, border = 1)
        gb_sizer1.Add(self.btn_find, (0,10), flag = wx.ALL, border = 1)

        gb_sizer.Add((28,0), (0,0))

        gb_sizer.Add(self.button_2, (0,1), flag = wx.ALL, border = 1)
        gb_sizer.Add(self.button_3, (1,1), flag = wx.ALL, border = 1)

        gb_sizer.Add(self.button_4, (0,2), flag = wx.ALL, border = 1)
        gb_sizer.Add(self.button_5, (1,2), (1,2), flag = wx.ALL, border = 1)

        gb_sizer.Add((10,0), (0, 3), flag = wx.ALIGN_CENTER|wx.ALL, border = 1)
        gb_sizer.Add(self.button_6, (0,4), flag = wx.ALL, border = 1)

        gb_sizer.Add(self.button_7, (1,4), flag = wx.ALL, border = 1)

        gb_sizer.Add(self.button_8, (0,5), (2,1), flag = wx.EXPAND|wx.ALL, border = 1)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)

        sizer_2.Add(gb_sizer1, (0,0), (1,1), wx.EXPAND, 0)
        sizer_2.Add(gb_sizer, (1,0), (1,2), wx.EXPAND, 0)
        self.pn_title.SetSizer(sizer_2)
        
        sizer_1.Add(self.pn_title, 1, wx.EXPAND, 0)
        sizer_1.Add(self.pn_view, 5, wx.EXPAND, 0)
        self.pn_view.SetSizer(sizer_3)
        self.SetSizer(sizer_1)
        self.Layout()


if __name__ == "__main__":

    app = wx.App(0)
    #wx.InitAllImageHandlers() Deprecated

    DB.LoadAllData('InData' + DB.os.sep + 'Testing.zip')
    frame_1 = MainFrame(mode=None, data=None, type=None, id_prj=0, parent=None)

    app.SetTopWindow(frame_1)
    frame_1.CenterOnScreen()
    frame_1.Show()
    app.MainLoop()
