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
# This file contains a form to define States                                   #
################################################################################


import DataDef as DB
import CDMLib as cdml
import wx, copy




class RowPanel(cdml.CDMPanel):

    def __init__(self, *args, **kwds):

        # Create instance of the CDMPanel class.
        kwdsnew = copy.copy(kwds)
        kwdsnew['style'] = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL              # Set the style of this RowPanel class
        cdml.CDMPanel.__init__(self, is_row = True, *args, **kwdsnew) # Second argument should be 'True' always

        # Create variables using State class and initialize those variables
        # using initial values defined in State Class
        self.record = cdml.GetInstanceAttr(DB.State)

        # create controls
        self.btn_del = cdml.Button(self, wx.ID_DELETE, "x") # Second argument should be wx.ID_DELETE
        self.st_status = wx.StaticText(self, -1, "")

        # Create controls to enter/display the variables in State object
        # For controls include text area set wx.TE_NOHIDESEL always.
        # This style need for the Find function
        self.tc_name = cdml.Text(self, -1, "", style=wx.TE_NOHIDESEL)
        self.cb_isSplit = cdml.Checkbox(self, -1, "")
        self.cb_isEvent = cdml.Checkbox(self, -1, "")
        self.cb_isTerminal = cdml.Checkbox(self, -1, "")
        self.cc_joiner_split = cdml.Combo(self, -1, validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.tc_notes = cdml.Text(self, -1, "", style=wx.TE_MULTILINE|wx.TE_NOHIDESEL)
        self.lc_states = cdml.List(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.cc_states = cdml.Combo(self, -1, validator=cdml.KeyValidator(cdml.NO_EDIT))

        arrow_up = cdml.getSmallUpArrowBitmap() # arrow bitmap for buttons
        arrow_dn = cdml.getSmallDnArrowBitmap()

        # add buttons for child States
        self.btn_add_state = cdml.BitmapButton(self, -1, arrow_up)
        self.btn_del_state = cdml.BitmapButton(self, -1, arrow_dn)

        self.__set_properties()
        self.__do_layout()

        # Opening another instance of the form is currently disabled since
        # recursive opening of this form and updating a parent form according
        # to a modification performed with a child is not supported. However,
        # doing this from the list box is ok since the record is saved and
        # changing the data is not possible in the child form
        # self.cc_states.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDblClick)
        self.lc_states.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnLeftDblClick)

    def __set_properties(self):

        self.btn_del.SetMinSize((20, 20))

        self.btn_add_state.SetMinSize((20, 20))
        self.btn_add_state.evtID = cdml.ID_EVT_OWN
        self.btn_add_state.evtData = self.AddChildState
        self.btn_add_state.SetToolTipString("Add Child States to the list")

        self.btn_del_state.SetMinSize((20, 20))
        self.btn_del_state.evtID = cdml.ID_EVT_OWN
        self.btn_del_state.evtData = self.DelChildState

        self.btn_del_state.SetToolTipString("Delete Child States from the list")

        self.tc_name.SetMinSize((120,-1))

        columns = (('Name', 150), ('Notes', 332))
        self.cc_joiner_split.SetColumns(columns)

        self.cb_isSplit.SetMinSize((66,-1))
        self.cb_isEvent.SetMinSize((66,-1))
        self.cb_isTerminal.SetMinSize((66,-1))
        self.tc_notes.SetMinSize((200,-1))

        self.lc_states.SetMinSize((300,90))
        self.lc_states.CreateColumns((('Included States', 250 ),))

        self.cc_states.SetMinSize((200,-1))

        self.cc_states.SetColumns((('Name', 200), ('Notes', 332)))

        self.tc_name.sortId = 0
        self.cb_isSplit.sortId = 1
        self.cb_isEvent.sortId = 2
        self.cb_isTerminal.sortId = 3
        self.cc_joiner_split.sortId = 4
        self.tc_notes.sortId = 5


    def __do_layout(self):
        """ Set the position of controls """
        sizer = wx.GridBagSizer(0,0)

        sizer.Add(self.btn_del, (0,0), (1,1), wx.ALL, 1)
        sizer.Add(self.st_status, (1,0), (1,1), wx.ALL, 1)
        sizer.Add(self.tc_name, (0,1), (1,1), wx.ALL, 1)
        sizer.Add(self.cb_isSplit, (0,2), (1,1), wx.ALIGN_CENTER,1)
        sizer.Add(self.cb_isEvent, (0,3), (1,1), wx.ALIGN_CENTER,1)
        sizer.Add(self.cb_isTerminal, (0,4), (1,1), wx.ALIGN_CENTER,1)
        sizer.Add(self.cc_joiner_split, (1,1),(1,1), wx.ALL, 1)
        sizer.Add(self.tc_notes, (1,2), (2,3), wx.ALL|wx.EXPAND, 1)
        sizer.Add(self.lc_states, (0,5), (2,4),wx.EXPAND|wx.ALL, 1)
        sizer.Add(self.cc_states, (2,5), (1,2), wx.ALL, 1 )
        sizer.Add(self.btn_add_state, (2,7), (1,1), wx.ALL, 1)
        sizer.Add(self.btn_del_state, (2,8), (1,1), wx.ALL, 1)
        self.SetSizer(sizer)


    def GetValues(self):
        """
        Retrieve current values in a row panel.
        RowPanel class must implement this method.
        """

        # create a copy of field variables
        record = copy.copy(self.record)

        record.ID = self.Key
        record.Name = str(self.tc_name.GetValue())
        record.IsSplit = self.cb_isSplit.GetValue()
        record.IsEvent = self.cb_isEvent.GetValue()
        record.IsTerminal = self.cb_isTerminal.GetValue()
        record.JoinerOfSplitter = self.cc_joiner_split.GetValue()
        record.Notes = str(self.tc_notes.GetValue())

        states = []
        for i in range(self.lc_states.GetItemCount()):
            key = self.lc_states.GetItemData(i)
            states.append(key)

        record.ChildStates = states

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
        self.cb_isEvent.SetValue(record.IsEvent)
        self.cb_isSplit.SetValue(record.IsSplit)
        self.cb_isTerminal.SetValue(record.IsTerminal)
        self.tc_notes.SetValue(str(record.Notes))

        if record.JoinerOfSplitter != 0:
            self.cc_joiner_split.SetValue(record.JoinerOfSplitter)

        # Display Child States
        self.lc_states.DeleteAllItems()
        for item in record.ChildStates:
            state = DB.States[item]
            self.lc_states.AddItem((str(state.Name), state.ID), self.lc_states.GetItemCount())


    def SaveRecord(self, record):
        """
        Save/Modify the data of StudyModel object
        This method is called by CheckFocus method in CDMLib
        RowPanel class must implement this method.
        """

        # create new State instance
        entry = DB.State( ID = 0,
                            Name = record.Name,
                            Notes = record.Notes,
                            IsSplit = record.IsSplit,
                            JoinerOfSplitter = record.JoinerOfSplitter,
                            IsEvent = record.IsEvent,
                            IsTerminal = record.IsTerminal,
                            ChildStates = record.ChildStates )

        frame = self.GetTopLevelParent()

        if self.Id == 0:    # if previous panel is new, create new object
            entry = DB.States.AddNew(entry, ProjectBypassID = frame.idPrj)

        elif self.Id > 0:   # if previous panel is existing one, replace record
            entry = DB.States.Modify(self.Key, entry, ProjectBypassID = frame.idPrj)

        return entry


    def TextRecordID(self):
        """ Returns the identity of the record as text """
        if self.Id == 0:
            Result = 'New State'
            RecordName = None
        else:
            RecordName = self.record.Name
            Result = 'State saved as "' + str(RecordName) + '"'
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

        splitter = [ (str(state.Name), str(state.Notes), state.ID)
                        for state in DB.States.values() if state.IsSplit ]
        states = [(str(state.Name), str(state.Notes), state.ID) for state in DB.States.values()]


        self.cc_joiner_split.SetItems(splitter)
        self.cc_states.SetItems(states)


    # Following methods are dedicated to the instance of RowPanel class for States form
    def AddChildState(self, event):
        """ Add Child States to ListCtrl """

        index = self.lc_states.GetFirstSelected()
        if index == -1 : index = self.lc_states.GetItemCount()

        key = self.cc_states.GetValue()
        state = str(self.cc_states.GetValueString())
        if state == '': return

        self.lc_states.AddItem((state, key), index)

        self.cc_states.SetValue(0)


    def DelChildState(self, event):
        """ Remove Child States from ListCtrl """

        index = self.lc_states.GetFirstSelected()
        if index == -1 : return

        state = self.lc_states.GetItemData(index)
        self.cc_states.SetValue(state)

        self.lc_states.DeleteItem(index)
        self.lc_states.Select(index, True)


    def OnLeftDblClick(self, event):
        """  Event handler to open 'State' form"""
        eventType = event.GetEventType()
        if eventType == wx.EVT_LEFT_DCLICK.typeId:
            id = self.cc_states.GetValue()
        elif eventType == wx.EVT_LIST_ITEM_ACTIVATED.typeId:
            index = self.lc_states.GetFirstSelected()
            id = self.lc_states.GetItemData(index)
        frame = self.GetTopLevelParent()
        if id not in DB.States.keys():
            # This code will never be reached since an empty list box
            # will not trigger this function. However, it is left here
            # since in the future this function may be called from another
            # control without properly defining a state.
            msg = "No state was selected" 
            msg += "\nDo you want to create new state?"
            ans = cdml.dlgSimpleMsg('ERROR', msg, wx.YES_NO , Parent = self)
            if ans == wx.ID_NO : return
            id =-1
        NoError = frame.ForceRecordSaveAttempt()
        if NoError:
            cdml.OpenForm('States', self, cdml.ID_MODE_SINGL, id, '', frame.idPrj)




# end of class RowPanel


class MainFrame(cdml.CDMFrame):
    def __init__(self, mode=None, data=None, type=None, id_prj=0, *args, **kwds):
        """ Constructor of the MainFrame class """
        self.idPrj = id_prj
        cdml.CDMFrame.__init__(self, mode, data, type, *args, **kwds)

        # Define Popup menu items
        # Format : tuple of list --> ([Label, Event handler, Id] , [], [], ... )
        #                       Label : label of an item
        #                       Event handler : name of event handler
        #                       Id : Id of current menu item
        # Special label : '-'--> separator, '+' --> submenu items
        #                       First item after last '+' marked items is the title of the submenu
        # If an item doesn't have event handler, the second parameter should be 'None'
        # If an item doesn't have Id, the third item should be -1
        # If a form need to manage instances of RowPanel class,
        #       the event handler should be 'self.FrameEventHandler'
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
                            ["+IsSplit" , self.FrameEventHandler, cdml.IDF_BUTTON2],
                            ["+IsEvent" , self.FrameEventHandler, cdml.IDF_BUTTON3],
                            ["+IsTemplate" , self.FrameEventHandler, cdml.IDF_BUTTON4],
                            ["+Joiner Of Splitter" , self.FrameEventHandler, cdml.IDF_BUTTON5],
                            ["+Notes" , self.FrameEventHandler, cdml.IDF_BUTTON6],
                            ["Sort By", None, -1])

        # Define the window menus 
        cdml.GenerateStandardMenu(self)

        # create panels for title section. First argument should be False
        self.pn_title = cdml.CDMPanel(False, self, -1)

        # Create bitmap buttons to display title of each field
        # Syntax : cdml.BitmapButton( parent, id, bitmap, label )
        # Don't need to set bitmap here. It will be assigned in the event handler when pressed
        # For the sort function, the labels need to be same with the variable name in database object
        self.st_title = wx.StaticText(self.pn_title, -1, "State Definition")
        self.st_name = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON1, None, "Name  ")
        self.st_isSplit = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON2, None, "Is Split")
        self.st_isEvent = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON3, None, "Is Event")
        self.st_isTerminal = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON4, None, "Is Terminal")
        self.st_joins_split = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON5, None, "Joiner Of Splitter")
        self.st_notes = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON6, None, "Notes")
        self.st_child_state = cdml.BitmapButton(self.pn_title, -1, None, "Child State/ Subprocess")

        # Create Add/Find buttons
        # Syntax : cdml.Button( parent, ID )
        # ID should be wx.ID_ADD for add button and wx.ID_FIND for find button in all forms
        self.btn_add = cdml.Button(self.pn_title, wx.ID_ADD)
        self.btn_find = cdml.Button(self.pn_title, wx.ID_FIND)

        # Scroll window that the RowPanel objects will be placed
        # IMPORTANT NOTE:
        #       In current version, all forms that need to manage the instance(s) of RowPanel class
        #               should have an instance of wx.ScrolledWindow class.
        #       Also the name of the panel should be "pn_view"
        self.pn_view = wx.ScrolledWindow(self, -1, style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)

        self.__set_properties()
        self.__do_layout()

        # Assign event handler for the buttons in title section -- to check the focus change
        self.pn_title.Bind(wx.EVT_BUTTON, self.FrameEventHandler, id=cdml.IDF_BUTTON1, id2=cdml.IDF_BUTTON6)
        self.btn_add.Bind(wx.EVT_BUTTON, self.FrameEventHandler)
        self.btn_find.Bind(wx.EVT_BUTTON, self.FrameEventHandler)

        # Call Initialize method to create row panels and display data
        self.Initialize()


    # Define the default method to handle the menu selections
    OnMenuSelected = cdml.OnMenuSelected


    def __set_properties(self):
        self.SetTitle("STATE DEFINITION")
        self.Collection = 'States' # name of global variable for States
        self.HelpContext = 'States'

        self.st_title.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

        self.pn_view.SetScrollRate(10, 10)

        self.SetSize((800, 600))

        self.st_title.SetMinSize((440, -1))
        
        self.st_name.sortId = 0
        self.st_name.evtID = cdml.ID_EVT_SORT
        self.st_name.SetMinSize((120,-1))

        self.st_isSplit.sortId = 1
        self.st_isSplit.evtID = cdml.ID_EVT_SORT
        self.st_isSplit.SetMinSize((66,-1))

        self.st_isEvent.sortId = 2
        self.st_isEvent.evtID = cdml.ID_EVT_SORT
        self.st_isEvent.SetMinSize((66,-1))

        self.st_isTerminal.sortId = 3
        self.st_isTerminal.evtID = cdml.ID_EVT_SORT
        self.st_isTerminal.SetMinSize((66,-1))

        self.st_joins_split.sortId = 4
        self.st_joins_split.evtID = cdml.ID_EVT_SORT
        self.st_joins_split.SetMinSize((120,-1))
        
        self.st_notes.sortId = 5
        self.st_notes.evtID = cdml.ID_EVT_SORT
        self.st_notes.SetMinSize((200,-1))

        self.st_child_state.SetMinSize((300,-1))
        

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.GridBagSizer(0,0)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        
        gb_sizer = wx.GridBagSizer(0, 0)
        gb_sizer1 = wx.GridBagSizer(0,0)

        gb_sizer1.Add((28,0), (0,0))
        gb_sizer1.Add(self.st_title, (0,1), (1,5), wx.ALL, 1)
        gb_sizer1.Add(self.btn_add, (0,8), (1,1), wx.ALL, 1)
        gb_sizer1.Add(self.btn_find, (0,9), (1,1), wx.ALL, 1)
       
        gb_sizer.Add((28,0), (0,0))
        gb_sizer.Add(self.st_name, (0,1), (1,1), wx.ALL, 1)

        gb_sizer.Add(self.st_isSplit, (0,2), (1,1), wx.ALL)
        gb_sizer.Add(self.st_isEvent, (0,3), (1,1), wx.ALL)
        gb_sizer.Add(self.st_isTerminal, (0,4), (1,1), wx.ALL)

        gb_sizer.Add(self.st_joins_split, (1,1), (1,1), wx.ALL, 1)
        gb_sizer.Add(self.st_notes, (1,2), (2,3), wx.ALL|wx.EXPAND, 1)

        gb_sizer.Add(self.st_child_state, (0,5), (2,3), wx.ALL|wx.EXPAND)
        
        sizer_2.Add(gb_sizer1, (0,0), (1,1), wx.EXPAND)
        sizer_2.Add(gb_sizer, (1,0), (1,2), wx.EXPAND)
        self.pn_title.SetSizer(sizer_2)

        sizer_1.Add(self.pn_title, 1, wx.EXPAND)
        sizer_1.Add(self.pn_view, 5, wx.EXPAND)

        self.pn_view.SetSizer(sizer_3)
        self.SetSizer(sizer_1)
        self.Layout()

    def CheckBeforeClose ( self, Key ):
        """ Override the Check before closing the form """
        if Key != None:
            if self.openMode == cdml.ID_MODE_SINGL :
                if  self.openType == 'process' and not DB.States[Key].IsSubProcess():
                    return True
        return False

# end of class MainFrame





if __name__ == "__main__":
    app = wx.App(0)
    #wx.InitAllImageHandlers() Deprecated
    DB.LoadAllData('InData' + DB.os.sep + 'Testing.zip')
    frame_1 = MainFrame(mode=None, data=None, type=None, id_prj=0, parent=None)
    app.SetTopWindow(frame_1)
    frame_1.CenterOnScreen()
    frame_1.Show()
    app.MainLoop()
