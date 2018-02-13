################################################################################
###############################################################################
# Copyright (C) 2013-2018 Jacob Barhak
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
###############################################################################

###############################################################################                                                                              #
# This file contains a form to define a Model                                 #
###############################################################################

import DataDef as DB
import CDMLib as cdml

import wx
import copy



class RowPanel(cdml.CDMPanel):
    def __init__(self, *args, **kwds):
        """ Constructor of RowPanel class """

        # Create instance of the CDMPanel class.
        kwdsnew = copy.copy(kwds)
        kwdsnew['style'] = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL          # Set the style of this RowPanel class
        cdml.CDMPanel.__init__(self, is_row = True, *args, **kwdsnew) # Second argument should be True always

        # Create variables using StudyModel class and initialize those variables
        # using initial values defined in StudyModel Class
        self.record = cdml.GetInstanceAttr(DB.StudyModel)

        # Create controls for each field in database
        # All controls are derived from controls in wxPython for CDM Project
        # Naming convention :
        # self.btn_ : Button or BitmapButton
        # self.cc_  : Combo control
        # self.lc_  : List control
        # self.tc_  : Text control
        # self.st_  : Static Text
        # self.cb_  : Checkbox

        # Button and hidden StaticText to display panel status
        self.btn_del = cdml.Button(self, wx.ID_DELETE, "x") # Second argument should be wx.ID_DELETE
        self.st_status = wx.StaticText(self, -1, " ")


        # Create controls to enter/display the variables in StudyModel object
        # For controls include text area set wx.TE_NOHIDESEL always.
        # This style need for the Find function
        # wx.TE_MULTILINE means multi line text control
        self.tc_name = cdml.Text(self, -1, "", style=wx.TE_MULTILINE|wx.TE_NOHIDESEL)

        # Add validator to prevent certain type of keyboard input
        # Following line shows how to prevent string input (i.e. only allow numbers in this control)

        self.cc_main_proc = cdml.Combo(self, style=wx.TE_NOHIDESEL, validator=cdml.KeyValidator(cdml.NO_EDIT))

        # Following two lines show how to prevent keyboard input
        self.tc_created = cdml.Text(self, -1, "", validator=cdml.KeyValidator(cdml.NO_INPUT))
        self.tc_modified = cdml.Text(self, -1, "", validator=cdml.KeyValidator(cdml.NO_INPUT))

        self.DerivedFrom = 0
        self.tc_from = cdml.Text(self, -1, style=wx.TE_NOHIDESEL, validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.tc_notes = cdml.Text(self, -1, "", style=wx.TE_MULTILINE|wx.TE_NOHIDESEL)

        self.btn_trans = cdml.Button(self, cdml.IDP_BUTTON1, "Transitions")
        #self.btn_copy = cdml.Button(self, cdml.IDP_BUTTON2, "Copy")

        # To modify the MainProcess, assign event handles for the combo control
        # Because modification will be done in the 'States' form (i.e. don't need to check the focus change ),
        # event handlers are assigned directly to the controls instead of the FrameEventHandler method in CDMFrame class
        self.cc_main_proc.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDblClick)


        self.__set_properties()
        self.__do_layout()


    def __set_properties(self):
        """ Set properties of panel and controls """

        self.btn_del.SetMinSize((20, 20))
        # Deactivate delete button of a panel, Not used in current version
        #if self.GetTopLevelParent().openMode == cdml.ID_MODE_SINGL:
        #    self.btn_del.Enable(False)

        self.st_status.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.tc_name.SetMinSize((125, -1))

        columns = (('Name', 150), ('Notes', 332))
        self.cc_main_proc.SetMinSize((120, -1)) # Set minimum size of a control.
                                                 # Thus, the size can't be shrunk smaller than this size
        self.cc_main_proc.SetColumns(columns)
        self.tc_from.SetMinSize((130, 20))
        self.tc_notes.SetMinSize((190,-1))

        # Set Sort Id and Data Type of a control
        # The sortId should be matched to the sortId of field title in the title section
        # If sortId is not set, no action occurs when user click the field title
        self.tc_name.sortId = 0

        # Each editable control has default dataType
        # GetValue method return proper value according to the data type --> See CDMLib
        self.cc_main_proc.sortId = 1

        self.tc_created.sortId = 2
        self.tc_created.dataType = cdml.ID_TYPE_NONE
        self.tc_created.SetMinSize((100,-1))

        self.tc_modified.sortId = 3
        self.tc_modified.dataType = cdml.ID_TYPE_NONE
        self.tc_modified.SetMinSize((100,-1))

        # Assign event handler that need to respond after checking the focus change
        # Syntax : tuple, (EventType, ActionID, Event Handler)
        # ventType should be None always( Not used in current version)
        # Valid value of EventId are ID_EVT_OWN and ID_EVT_SORT
        # If EventID is ID_EVT_OWN, third argument (i.e. name of event handler) should be defined
        # If EventID is ID_EVT_SORT, FrameEventHandler deals that event. Thus, event handler need not to be defined
        self.btn_trans.SetEvent((None, cdml.ID_EVT_OWN, self.OnButtonClick))
        self.btn_trans.chkFocus = True

    def __do_layout(self):
        """ Set position of each control """

        gb_sizer = wx.GridBagSizer(hgap=0, vgap=0)
        gb_sizer.Add(self.btn_del, (0,0), flag=wx.ALL, border=1)
        gb_sizer.Add(self.st_status, (1,0), flag = wx.ALL, border=1)

        gb_sizer.Add(self.tc_name, (0,1),(2,1), flag=wx.EXPAND|wx.ALL, border=1)
        gb_sizer.Add(self.cc_main_proc, (0,2),(2,1), flag = wx.ALL, border=1)

        gb_sizer.Add(self.tc_created, (0,3), flag = wx.ALL, border=1)
        gb_sizer.Add(self.tc_modified, (1,3), flag = wx.ALL, border=1)

        gb_sizer.Add(self.tc_from, (0,4), span=(2,1), flag = wx.EXPAND|wx.ALL, border=1)
        gb_sizer.Add(self.tc_notes, (0,5), span=(2,1), flag=wx.EXPAND|wx.ALL, border=1)

        gb_sizer.Add(self.btn_trans, (0,6), flag = wx.ALL, border=1)
        #gb_sizer.Add(self.btn_copy, (1,6), flag = wx.ALL, border=1)

        self.SetSizer(gb_sizer)

        # After invoking Layout() method,
        # wxSizer arranges the controls using above layout rules and properties
        self.Layout()


    def GetValues(self):
        """
        Retrieve current values in a row panel.
        RowPanel class must implement this method.
        """

        record = copy.copy(self.record)

        record.ID = self.Key # key
        record.Name = str(self.tc_name.GetValue())
        record.CreatedOn = self.tc_created.GetValue()
        record.LastModified = self.tc_modified.GetValue()
        record.MainProcess = self.cc_main_proc.GetValue()
        record.DerivedFrom = self.DerivedFrom
        record.Notes =  str(self.tc_notes.GetValue())

        return record


    def SetValues(self, record, init=False):
        """
        Write current data in controls on a row panel
        RowPanel class must implement this method.
        """
        # Since there are combo items in use, first populate their list
        self.SetComboItem()

        self.Key = record.ID        
        self.tc_name.SetValue(str(record.Name))
        self.tc_created.SetValue(record.CreatedOn)
        self.tc_modified.SetValue(record.LastModified)
        self.tc_notes.SetValue(str(record.Notes))

        from_model = cdml.GetRecordByKey(DB.StudyModels, record.DerivedFrom)
        if from_model:
            self.tc_from.SetValue(str(from_model.Name))
        self.DerivedFrom = record.DerivedFrom
        if record.MainProcess :
            self.cc_main_proc.SetValue(record.MainProcess)


    def SaveRecord(self, record):
        """
        Save/Modify the data of StudyModel object
        This method is called by CheckFocus mehtod in CDMLib
        RowPanel class must implement this method.
        """

        # Create new StudyModel object
        entry = DB.StudyModel( ID = 0,
                                Name = str(record.Name),
                                Notes = str(record.Notes),
                                DerivedFrom = record.DerivedFrom,
                                MainProcess = record.MainProcess )


        # Check the relevance of the new state,

        frame = self.GetTopLevelParent()

        if self.Id == 0:    # if previous panel is new, create new object
            entry = DB.StudyModels.AddNew(entry, ProjectBypassID = frame.idPrj)

        elif self.Id > 0:   # if previous panel is existing one, replace record
            entry = DB.StudyModels.Modify(self.Key, entry, ProjectBypassID = frame.idPrj)

        return entry


    def TextRecordID(self):
        """ Returns the identity of the record as text """
        if self.Id == 0:
            Result = 'New Model'
            RecordName = None
        else:
            RecordName = str(self.record.Name)
            Result = 'Model saved as "' + str(RecordName) + '"'
        DisplayName = self.tc_name.GetValue()
        if DisplayName != RecordName:
           Result = Result + ' currently edited to "' + str(DisplayName) + '"'
        return Result


    def SetComboItem(self):
        """
        Set items of ComboCtrl in RowPanel class when focus is moved in current RowPanel instance
        The items are removed when lost focus --> Implemented in CDMFrame class
        RowPanel class that have combo controls must implement this method.
        """
        main_process = [(str(state.Name), str(state.Notes), state.ID)
                            for state in DB.States.values() if state.IsSubProcess() ]

        self.cc_main_proc.SetItems(main_process)


    # Following methods are dedicated to the StudyModel form
    def OnButtonClick(self, event):
        """
        Event handler to respond to the button click event.
        Open Transition Form or create a copy of current Model
        New control mechanism may need to make more general method to open and manage child form
        """

        id = event.GetId()
        if id == cdml.IDP_BUTTON1: # open transition form
            if self.Id == 0 :
                cdml.dlgSimpleMsg('ERROR', "This model is Empty. Please enter data before transitions", Parent = self)
                return

            frame = self.GetTopLevelParent()
            cdml.OpenForm('Transitions', self, cdml.ID_MODE_MULTI, self.Key, None, frame.idPrj)

        elif id == cdml.IDP_BUTTON2:
            cdml.dlgNotPrepared()


    def OnLeftDblClick(self, event):
        """  Event handler to open 'State' form"""
        cc = event.GetEventObject().GetParent()
        id = cc.GetValue()
        frame = self.GetTopLevelParent()
        if id not in DB.States.keys():
            # If this is a listed subprocess - there may be a problem
            # Therefore, add the assertion check for this
            if id != 0:
                cdml.dlgSimpleMsg('Error', "ASSERTION ERROR: Can't find Main Process:" , Parent = self)
                return
            cdml.OpenForm('States', self, cdml.ID_MODE_SINGL, -1, 'process', frame.idPrj)
        else:
            cdml.OpenForm('States', self, cdml.ID_MODE_SINGL, id, 'process', frame.idPrj)


# end of class RowPanel


class MainFrame(cdml.CDMFrame):
    """ MainFrame for StudyModel object """

    def __init__(self, mode=None, data=None, type=None, id_prj=0, *args, **kwds):
        """ Constructor of the MainFrame class """
        self.idPrj = id_prj

        #create frame instance
        cdml.CDMFrame.__init__(self, mode, data, type, *args, **kwds)

        # Define Popup menu items
        # Format : tuple of list --> ([Label, Event handler, Id] , [], [], ... )
        #           Label : label of an item
        #           Event handler : name of event handler
        #           Id : Id of current menu item
        # Special label : '-'--> separator, '+' --> submenu items
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
                            ["-" , None, -1 ],
                            ["Find" , self.FrameEventHandler, wx.ID_FIND],
                            ["-" , None, -1 ],
                            ["+Name" , self.FrameEventHandler, cdml.IDF_BUTTON1],
                            ["+Main Process" , self.FrameEventHandler, cdml.IDF_BUTTON2],
                            ["+Created On" , self.FrameEventHandler, cdml.IDF_BUTTON3],
                            ["+Last Modified" , self.FrameEventHandler, cdml.IDF_BUTTON4],
                            ["+User Modified" , self.FrameEventHandler, cdml.IDF_BUTTON5],
                            ["+Derived From Model" , self.FrameEventHandler, cdml.IDF_BUTTON6],
                            ["+Created By Project" , self.FrameEventHandler, cdml.IDF_BUTTON7],
                            ["+Notes", self.FrameEventHandler, cdml.IDF_BUTTON8],
                            ["Sort By", None, -1])

        # Define the window menus 
        cdml.GenerateStandardMenu(self)

        # create panel for field titles
        # IMPORTANT NOTE:
        #   In current version, name of a panel for the title section should be "pn_title"
        #   And should be an instance of CDMPanel class with False as a first argument
        self.pn_title = cdml.CDMPanel(False, self, -1)
        self.st_title = wx.StaticText(self.pn_title, -1, "Define Model")

        # Create bitmap buttons to display title of each field
        # Syntax : cdml.BitmapButton( parent, id, bitmap, label )
        # Don't need to set bitmap here. It will be assigned in the event handler when pressed
        # For the sort function, the labels need to be same with the variable name in database object
        self.button_1 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON1, None, "Name")
        self.button_2 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON2, None, "Main Process")
        self.button_3 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON3, None, "Created On")
        self.button_4 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON4, None, "Last Modified")
        self.button_5 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON5, None, "Derived From")
        self.button_6 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON6, None, "Notes")


        # Create buttons to open State form. This button is only used for StudyModels form
        self.btn_states = cdml.Button(self.pn_title, wx.ID_OPEN, "States")

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

        # Test code for the usage of StatusBar - Not used
        # self.sb = cdml.StatusBar(self)
        # self.SetStatusBar(self.sb)

        # Assign event handler for the buttons in title section -- to check the focus change
        self.pn_title.Bind(wx.EVT_BUTTON, self.FrameEventHandler, id=cdml.IDF_BUTTON1, id2=cdml.IDF_BUTTON9)
        self.btn_states.Bind(wx.EVT_BUTTON, self.FrameEventHandler) # States
        self.btn_add.Bind(wx.EVT_BUTTON, self.FrameEventHandler)    # ADD
        self.btn_find.Bind(wx.EVT_BUTTON, self.FrameEventHandler)   # FIND

        self.__set_properties() # set properties of controls
        self.__do_layout()      # Set position of controls/panels

        # Initialze this form : Create RowPanles and display data for each field in DB
        # Implemented in CDMLib -> CDMFrame class -> Initialize
        self.Initialize()


    # Define the default method to handle the menu selections
    OnMenuSelected = cdml.OnMenuSelected


    def __set_properties(self):
        """ Set properties of frame and controls """

        self.SetTitle("Define Model")   # title on title bar
        self.SetSize((825,600))
        self.SetCollection('StudyModels')   # Set Variable name related to this form -- Always required
        self.HelpContext = 'StudyModels'

        self.button_1.SetMinSize((125, -1))
        self.button_2.SetMinSize((120, -1))
        self.button_3.SetMinSize((100, -1))
        self.button_4.SetMinSize((100, -1))
        self.button_5.SetMinSize((130, -1))
        self.button_6.SetMinSize((190, -1))

        self.st_title.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.st_title.SetMinSize((340, -1))
        
        self.pn_view.SetScrollRate(10, 10)      # Set scroll rate of scrolled window

        # Define control specific event data - tuple
        # Syntax : (Event Type, ID , Event Handler)
        # Event handler is called by FrameEventHandler after processing focus change
        # See CDMLib.py --> CDMFrame class --> FrameEventHandler method
        self.btn_states.SetEvent(( None, cdml.ID_EVT_OWN, self.OpenFormStates))

        # Set sort id and event action id for each field title
        # If a user click title of a field, SorPanels function uses this id to match
        # the title and control in a RowPanel
        # See SortPanels function in CDMLib.py
        for i in range(6):
            btn = getattr(self, 'button_' + str(i+1))
            btn.sortId = i
            btn.evtID = cdml.ID_EVT_SORT


    def __do_layout(self):
        """ Set position of each control """

        # For basic concept of sizer, see http://neume.sourceforge.net/sizerdemo/
        sizer_1 = wx.BoxSizer(wx.VERTICAL)  # define BoxSizers <-- most common sizer in wxPython
        sizer_2 = wx.GridBagSizer(0,0)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)

        gb_sizer = wx.GridBagSizer(0,0)
        gb_sizer1 = wx.GridBagSizer(0,0)

        gb_sizer1.Add((28,0), (0,0))
        gb_sizer1.Add(self.st_title, (0,1), (1,5), flag=wx.EXPAND|wx.ALL, border=1)

        gb_sizer1.Add(self.btn_states, (0,7), flag=wx.EXPAND|wx.ALL)
        gb_sizer1.Add((150,0), (0,8), flag=wx.EXPAND|wx.ALL)
        gb_sizer1.Add(self.btn_add, (0,9), flag=wx.EXPAND|wx.ALL)
        gb_sizer1.Add(self.btn_find, (0,10), flag=wx.EXPAND|wx.ALL)
 
        gb_sizer.Add((28,0), (0,0))
        gb_sizer.Add(self.button_1, (0,1), (2,1), flag=wx.EXPAND|wx.ALL)

        gb_sizer.Add(self.button_2, (0,2), (2,1), flag=wx.EXPAND|wx.ALL)
        gb_sizer.Add(self.button_3, (0,3), flag=wx.EXPAND|wx.ALL)
        gb_sizer.Add(self.button_4, (1,3), flag=wx.EXPAND|wx.ALL)
        gb_sizer.Add(self.button_5, (0,4), (2,1), flag=wx.EXPAND|wx.ALL)
        gb_sizer.Add(self.button_6, (0,5), (2,1), flag=wx.EXPAND|wx.ALL)

        sizer_2.Add(gb_sizer1, (0,0), (1,1), wx.EXPAND, 0)
        sizer_2.Add(gb_sizer, (1,0), (1,2), wx.EXPAND, 0)
        self.pn_title.SetSizer(sizer_2)

        sizer_1.Add(self.pn_title, 1, wx.EXPAND, 0)
        sizer_1.Add(self.pn_view, 5, wx.EXPAND, 0)
        self.pn_view.SetSizer(sizer_3)
        self.SetSizer(sizer_1)
 
        self.Layout()                   # Trigger for layout
                                        # After invoking this method, the sizer arrange the controls using above rules


    # Additional method for StudyModel form to open 'States' form
    def OpenFormStates(self, event):
        """ Event handler for the 'States' button in the title section """
        cdml.OpenForm('States', self, None, None)


# this code was generated by wxGlade for standalone mode
if __name__ == "__main__":

    app = wx.App(0)
    #wx.InitAllImageHandlers() Deprecated

    DB.LoadAllData('InData' + DB.os.sep + 'Testing.zip')
    frame_1 = MainFrame(mode=None, data=None, type=None, id_prj=0, parent=None)
    app.SetTopWindow(frame_1)
    frame_1.Center()
    frame_1.Show()
    app.MainLoop()
