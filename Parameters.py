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
################################################################################
#                                                                              #
# This file contains a form to define Parameters                               #
################################################################################

import DataDef as DB
import CDMLib as cdml
import wx, copy



class RowPanel(cdml.CDMPanel):

    def __init__(self, *args, **kwds):
        """ Constructor of RowPanel class """

        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL # Set the style of RowPanel class
        cdml.CDMPanel.__init__(self, True, *args, **kwdsnew) # Second parameter should be True always for any RowPanel class

        # Create variables using Param class and initialize those variables
        # using initial values defined in Param Class
        self.record = cdml.GetInstanceAttr(DB.Param)
        self.record.Name = ''

        # Button and hidden StaticText to display panel status
        self.btn_del = cdml.Button(self, wx.ID_DELETE, "x", style=wx.BU_EXACTFIT)
        self.st_status = wx.StaticText(self, -1, " ")

        # Create controls to enter/display the variables in Transition object
        # For controls include text area set wx.TE_NOHIDESEL always.
        # This style need for the Find function
        self.tc_name = cdml.Text(self, -1, "", style=wx.TE_NOHIDESEL)
        self.tc_formula = cdml.Text(self, -1, "", style=wx.TE_MULTILINE|wx.TE_NOHIDESEL)
        self.cc_type = cdml.Combo(self, -1, style=wx.TE_NOHIDESEL, validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.tc_rule_parm = cdml.Text(self, -1, "", style=wx.TE_NOHIDESEL)
        self.tc_notes = cdml.Text(self, -1, "", style=wx.TE_MULTILINE|wx.TE_NOHIDESEL)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        """ Set properties of panel and controls """

        self.btn_del.SetMinSize((20, 20))
        # Deactivate delete button of a panel, Not used in current version
        #if self.GetTopLevelParent().openMode == cdml.ID_MODE_SINGL:
        #    self.btn_del.Enable(False)

        self.st_status.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

        # Define number of columns, column title and width
        # It's tuple of tuples
        # Syntax : ((Column Name, width), Column Name, width), ...)
        # Colunm number is calculated automatically.
        columns = (('Type', 150),)
        self.cc_type.SetMinSize((100, -1))
        self.cc_type.SetColumns(columns)


        self.tc_name.SetMinSize((150,-1))
        self.tc_formula.SetMinSize((150,-1))
        self.tc_rule_parm.SetMinSize((150,-1))

        self.tc_notes.SetMinSize((200,-1))

        # Set Sort Id and Data Type of a control
        # The sortId should be matched to the sortId of field title in the title section
        # If sortId is not set, no action occurs when user click the field title
        self.tc_name.sortId = 0
        self.tc_formula.sortId = 1
        self.cc_type.sortId = 2
        self.cc_type.dataType = cdml.ID_TYPE_ALPHA
        self.tc_rule_parm.sortId = 3
        self.tc_notes.sortId = 4


    def __do_layout(self):
        sizer = wx.GridBagSizer(0,0)

        sizer.Add(self.btn_del, (0,0), (1,1), wx.ALL, 2)
        sizer.Add(self.st_status, (1,0), (1,1), wx.ALL, 2)

        sizer.Add(self.tc_name, (0,1), (1,1), wx.ALL, 2)
        sizer.Add(self.cc_type, (1,1), (1,1), wx.ALL, 2)
        sizer.Add(self.tc_formula, (0,2), (2,1), wx.EXPAND|wx.ALL, 2)
        sizer.Add(self.tc_rule_parm, (0,3), (1,1), wx.EXPAND|wx.ALL, 2)
        sizer.Add(self.tc_notes, (0,4), (2,1), wx.EXPAND|wx.ALL, 2)

        self.SetSizer(sizer)
        sizer.Fit(self)


    def GetValues(self):
        """
        Retrieve current values in a row panel.
        RowPanel class must implement this method.
        """

        # create a copy of field variables
        record = copy.copy(self.record)

        record.Name = str(self.tc_name.GetValue())
        record.Formula = str(self.tc_formula.GetValue())
        record.ParameterType = str(self.cc_type.GetValue())
        record.ValidationRuleParams = str(self.tc_rule_parm.GetValue())
        record.Notes = str(self.tc_notes.GetValue())

        return record


    def SetValues(self, record, init=False):
        """
        Write current data in controls on a row panel
        RowPanel class must implement this method.
        """

        self.Key = str(record)

        self.tc_name.SetValue(str(record))
        self.tc_formula.SetValue(str(record.Formula))

        self.cc_type.SetValue(str(record.ParameterType))

        self.tc_rule_parm.SetValue(str(record.ValidationRuleParams))
        self.tc_notes.SetValue(str(record.Notes))


    def SaveRecord(self, record):
        """
        Save/Modify the data of StudyModel object
        This method is called by CheckFocus mehtod in CDMLib
        RowPanel class must implement this method.
        """

        # create new Param object
        entry = DB.Param(   Name = str(record.Name),
                            Formula = str(record.Formula),
                            ParameterType = str(record.ParameterType),
                            ValidationRuleParams = str(record.ValidationRuleParams),
                            Notes = str(record.Notes) )


        if self.Id == 0:    # if previous panel is new, create new object
            entry = DB.Params.AddNew(entry)

        else:               # if previous panel is existing one, replace record
            entry = DB.Params.Modify(self.Key, entry)

        return entry


    def TextRecordID(self):
        """ Returns the identity of the record as text """
        if self.Id == 0:
            Result = 'New Parameter'
            RecordName = None
        else:
            RecordName = str(self.record.Name)
            Result = 'Parameter saved as "' + str(RecordName) + '"'
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
        parm_type = [ (str(Type), -1) for Type in DB.ParameterTypes if (cdml.GetAdminMode() or Type not in ['State Indicator','System Reserved'])]
        self.cc_type.SetItems(parm_type)



class MainFrame(cdml.CDMFrame):
    """ MainFrame class for Parameters form"""
    def __init__(self, mode=None, data=None, type=None, id_prj=0, *args, **kwds):
        """ Constructor of the MainFrame class """
        self.idPrj = id_prj

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
        # In Project form dedicated event handler in that class (ex. see Project or PopulationData form)
        self.pup_menus = (  ["Undo", self.FrameEventHandler, wx.ID_UNDO ],
                            ["-" , None, -1],
                            ["Add" , self.FrameEventHandler, wx.ID_ADD],
                            ["Copy Record" , self.FrameEventHandler, cdml.ID_MENU_COPY_RECORD],
                            ["Delete" , self.FrameEventHandler, wx.ID_DELETE],
                            ["-" , None, -1 ],
                            ["Find" , self.FrameEventHandler, wx.ID_FIND],
                            ["-" , None, -1 ],
                            ["+Param" , self.FrameEventHandler, cdml.IDF_BUTTON1],
                            ["+Formula" , self.FrameEventHandler, cdml.IDF_BUTTON2],
                            ["+Parameter Type" , self.FrameEventHandler, cdml.IDF_BUTTON3],
                            ["+Validation Rule Params" , self.FrameEventHandler, cdml.IDF_BUTTON5],
                            ["+Notes" , self.FrameEventHandler, cdml.IDF_BUTTON6],
                            ["Sort By", None, -1])

        # Define the window menus 
        cdml.GenerateStandardMenu(self)


        # create panel for field titles
        # IMPORTANT NOTE:
        #   In current version, name of a panel for the title section should be "pn_title"
        #   And should be an instance of CDMPanel class with False as a first argument
        self.pn_title = cdml.CDMPanel(False, self, -1)
        self.st_title = wx.StaticText(self.pn_title, -1, "Define Parameters")

        # Create bitmap buttons to display title of each field
        # Syntax : cdml.BitmapButton( parent, id, bitmap, label )
        # Don't need to set bitmap here. It will be assigned in the event handler when pressed
        # For the sort function, the labels need to be same with the variable name in database object
        self.button_1 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON1, None, "Param")
        self.button_2 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON2, None, "Formula")
        self.button_3 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON3, None, "Parameter Type")
        self.button_4 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON5, None, "Validation Rule Params")
        self.button_5 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON6, None, "Notes")

        # Create Add/Find buttons
        # Syntax : cdml.Button( parent, ID )
        # ID should be wx.ID_ADD for add button and wx.ID_FIND for find button in all forms
        self.button_6 = cdml.Button(self.pn_title, wx.ID_ADD)
        self.button_7 = cdml.Button(self.pn_title, wx.ID_FIND)

        # Create a button to open the dialog for display option
        self.button_8 = cdml.Button(self.pn_title, wx.ID_OPEN, "Select")

        # Scroll window that the RowPanel objects will be placed
        # IMPORTANT NOTE:
        #   In current version, all forms that need to manage the instance(s) of RowPanel class
        #       should have an instance of wx.ScrolledWindow class.
        #   Also the name of the panel should be "pn_view"
        self.pn_view = wx.ScrolledWindow(self, -1, style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)

        self.__set_properties()
        self.__do_layout()

        # Assign event handler for the buttons in title section -- to check the focus change
        self.pn_title.Bind(wx.EVT_BUTTON, self.FrameEventHandler, id=cdml.IDF_BUTTON1, id2=cdml.IDF_BUTTON6)
        self.button_6.Bind(wx.EVT_BUTTON, self.FrameEventHandler)
        self.button_7.Bind(wx.EVT_BUTTON, self.FrameEventHandler)
        self.button_8.Bind(wx.EVT_BUTTON, self.FrameEventHandler)

        self.InitParameters()

    # Define the default method to handle the menu selections
    OnMenuSelected = cdml.OnMenuSelected

    def __set_properties(self):
        self.SetTitle("PARAMETERS")
        self.SetSize((800, 600))
        self.Collection = 'Params'
        self.HelpContext = 'Params'


        self.button_1.SetMinSize((150, -1))
        self.button_2.SetMinSize((150, -1))
        self.button_3.SetMinSize((150, -1))
        self.button_4.SetMinSize((150, -1))
        self.button_5.SetMinSize((200, -1))
        self.button_6.SetMinSize((100, -1))
        self.button_7.SetMinSize((100, -1))
        self.button_8.SetMinSize((100, -1))

        self.st_title.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.st_title.SetMinSize((340, -1))
        
        self.pn_view.SetScrollRate(10, 10)

        self.button_8.evtID = cdml.ID_EVT_OWN
        self.button_8.evtData = self.InitParameters

        for i in range(1,6):
            btn = getattr(self, 'button_'+str(i))
            btn.sortId = i-1
            btn.evtID = cdml.ID_EVT_SORT




    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.GridBagSizer(0,0)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)

        gb_sizer = wx.GridBagSizer(0,0)
        gb_sizer1 = wx.GridBagSizer(0,0)

        gb_sizer1.Add((28,0), (0,0))
        gb_sizer1.Add(self.st_title, (0,1), (1,3), wx.ALL, 2)

        gb_sizer1.Add(self.button_8, (0,5), (1,1), wx.ALL|wx.EXPAND, 2)
        gb_sizer1.Add(self.button_6, (0,6), (1,1), wx.ALL|wx.EXPAND, 2)
        gb_sizer1.Add(self.button_7, (0,7), (1,1), wx.ALL|wx.EXPAND, 2)

        gb_sizer.Add((28,0), (0,0))
        gb_sizer.Add(self.button_1, (0,1), (1,1), wx.ALL, 2)
        gb_sizer.Add(self.button_3, (1,1), (1,1), wx.ALL, 2)
        gb_sizer.Add(self.button_2, (0,2), (2,1), wx.EXPAND|wx.ALL, 2)
        gb_sizer.Add(self.button_4, (0,3), (1,1), wx.EXPAND|wx.ALL, 2)
        gb_sizer.Add(self.button_5, (0,4), (2,1), wx.EXPAND|wx.ALL, 2)

        sizer_2.Add(gb_sizer1, (0,0), (1,1), wx.EXPAND, 0)
        sizer_2.Add(gb_sizer, (1,0), (1,2), wx.EXPAND, 0)
        self.pn_title.SetSizer(sizer_2)

        sizer_1.Add(self.pn_title, 1, wx.EXPAND, 0)
        sizer_1.Add(self.pn_view, 5, wx.EXPAND, 0)
        self.pn_view.SetSizer(sizer_3)
        self.SetSizer(sizer_1)
        self.Layout()


    def InitParameters(self, event=None):
        """
        Create list of parameter then call Initialize method to display the selected parameters
        """
        params = self.GetParameterList()
        # Create RowPanels and Display selected parameters
        self.Initialize(params)     


    def GetParameterList(self):
        """ Open a dialog and get parameter list to display """

        types = [ 'ALL User Accessible' ]
        types.extend(DB.ParameterTypes)
        # Decide if to include system reserve parameters according to if
        # admin mode was set
        if not cdml.GetAdminMode():
            types.remove('State Indicator')
            types.remove('System Reserved')
        else:
            types.append('ALL')

        if self.openData == None:
            # if no specific parameter was requested show a dialog box
            dlg = wx.MultiChoiceDialog(self, 'Please select parameter type you want to see.\n Some parameter types may take long time to display.', 'Select Parameter',
                            types, wx.CHOICEDLG_STYLE )

            dlg.SetSelections([0]) # set default selection
            dlg.CenterOnScreen()

            if dlg.ShowModal() != wx.ID_OK:
                return [] # If 'Cancel' button is clicked

            indexes = dlg.GetSelections() # Get selection index
            dlg.Destroy()

            selections = [types[i] for i in indexes]    # extract selected parameter types
            if selections == []:
                params = []
            elif selections[0] == 'ALL User Accessible':
                # Sort the entries according to key and filter
                params = [ Entry for (Key,Entry) in sorted(DB.Params.iteritems()) if Entry.ParameterType not in ['State Indicator', 'System Reserved'] ]

            elif selections[-1] == 'ALL':
                # Sort the entries according to key
                params = [ Entry for (Key,Entry) in sorted(DB.Params.iteritems())]

            else:
                # Sort the entries according to key and filter
                params = [ Entry for (Key,Entry) in sorted(DB.Params.iteritems()) if Entry.ParameterType in selections ]
        else:
            # The form was called with a particular parameter in mind
            parm = cdml.GetRecordByKey(getattr(DB, self.Collection), self.openData)
            if parm == None or parm.ParameterType not in types:
                params = []
            else:
                params = [parm]            
        return params


    def CheckBeforeClose ( self, Key ):
        """ Override the Check before closing the form """
        if Key != None:
            if self.openMode == cdml.ID_MODE_SINGL:
                if DB.Params[Key].ParameterType not in self.openType :
                    return True
        return False


if __name__ == "__main__":

    app = wx.App(0)
    #wx.InitAllImageHandlers() Deprecated
    DB.LoadAllData('InData' + DB.os.sep + 'Testing.zip')
    frame_1 = MainFrame(mode=None, data=None, type=None, id_prj=0, parent = None)
    app.SetTopWindow(frame_1)
    frame_1.CenterOnScreen()
    frame_1.Show()
    app.MainLoop()
