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
# This file contains a form to define Transition(s) for a Study/Mode           #
################################################################################

import DataDef as DB
import CDMLib as cdml
import wx, copy


class RowPanel(cdml.CDMPanel):
    """ RowPanel class for Transitions """

    def __init__(self, id_model, *args, **kwds):
        """ Constructor of RowPanel class """


        kwdsnew = copy.copy(kwds)
        kwdsnew['style'] = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL # Set the style of RowPanel class
        cdml.CDMPanel.__init__(self, True, *args, **kwdsnew) # Second parameter should be True always for any RowPanel class

        # Use userData to save ID of Study/Model
        self.userData = id_model

        # Create variables using Transition class and initialize those variables
        # using initial values defined in Transition Class
        self.record = cdml.GetInstanceAttr(DB.Transition)
        self.record.StudyModelID = self.userData

        # Button and hidden StaticText to display panel status
        self.btn_del = cdml.Button(self, wx.ID_DELETE, "x", style=wx.BU_EXACTFIT)
        self.st_status = wx.StaticText(self, -1, " ")

        # Create controls to enter/display the variables in Transition object
        # For controls include text area set wx.TE_NOHIDESEL always.
        # This style need for the Find function
        self.cc_state_from = cdml.Combo(self, cdml.IDP_BUTTON1, style=wx.TE_NOHIDESEL, validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.cc_state_to = cdml.Combo(self, cdml.IDP_BUTTON2, style=wx.TE_NOHIDESEL, validator=cdml.KeyValidator(cdml.NO_EDIT))

        self.tc_probability = cdml.Text(self, cdml.IDP_BUTTON3, '', style=wx.TE_NOHIDESEL|wx.TE_MULTILINE)

        self.tc_notes = cdml.Text(self, -1, "", style=wx.TE_NOHIDESEL|wx.TE_MULTILINE)

        self.__set_properties()
        self.__do_layout()

        # Bind an event handler to check/display formulae for the parameters
        # self.Bind(wx.EVT_IDLE, self.CheckFormula)

        # To modify the state and parameters, assign event handles for some controls
        # Because focus management isn't need for the modification,
        # event handlers are assigned directly to the controls instead of the FrameEventHandler method in CDMFrame class
        #self.cc_state_from.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnButtonDblClick )
        #self.cc_state_to.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnButtonDblClick )
        self.tc_probability.Bind(wx.EVT_LEFT_DCLICK, self.OnButtonDblClick )


    def __set_properties(self):
        """ Set properties of panel and controls """

        self.SetSize((960,-1))

        self.btn_del.SetMinSize((20, 20))
        self.st_status.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

        # Define number of columns, column title and width
        # It's tuple of tupels
        # Syntax : ((Column Name, width), Column Name, width), ...)
        # Column number is calculated automatically.
        columns = (('Name', 150), ('Notes', 332))

        StandardSize = (150, -1)
        self.cc_state_from.SetMinSize(StandardSize) 
        self.cc_state_from.SetColumns(columns)

        # Set Sort Id and Data Type of a control
        # The sortId should be matched to the sortId of field title in the title section
        # If sortId is not set, no action occurs when user click the field title
        self.cc_state_from.sortId = 0

        self.cc_state_to.SetMinSize(StandardSize)
        self.cc_state_to.SetColumns(columns)
        self.cc_state_to.sortId = 1


        self.tc_probability.SetMinSize(StandardSize)
        self.tc_probability.sortId = 2

        self.tc_notes.SetMinSize(StandardSize)
        self.tc_notes.sortId = 3


    def __do_layout(self):
        """ Set position of each control """

        grid_sizer_1 = wx.GridBagSizer(0, 0)

        grid_sizer_1.Add(self.btn_del, (0,0), (1,1), wx.ALL, 1)                 # 'x' button
        grid_sizer_1.Add(self.st_status, (2,0), (1,1), wx.ALL, 1)                   #  hidden text for status display

        grid_sizer_1.Add(self.cc_state_from, (0,1), (1,1), wx.ALL, 1)               # From State
        grid_sizer_1.Add(self.cc_state_to, (1,1), (1,1), wx.ALL, 1)             # To State

        grid_sizer_1.Add(self.tc_probability, (0,2), (3,1), wx.ALL|wx.EXPAND, 1)          # Probability

        grid_sizer_1.Add(self.tc_notes, (0,4), (3,1), wx.ALL|wx.EXPAND, 1)

        self.SetSizer(grid_sizer_1)
        grid_sizer_1.Fit(self)


    def GetValues(self):
        """
        Retrieve current values in a row panel.
        RowPanel class must implement this method.
        """

        # create a copy of field variables
        record = copy.copy(self.record)

        record.StudyModelID = (self.userData)
        record.FromState = (self.cc_state_from.GetValue())
        record.ToState = (self.cc_state_to.GetValue())
        record.Probability = str(self.tc_probability.GetValue())
        record.Notes = str(self.tc_notes.GetValue())

        return record


    def SetValues(self, record, init=False):
        """
        Write current data in controls on a row panel
        RowPanel class must implement this method.
        """

        # Since there are combo items in use, first populate their list
        self.SetComboItem()
        
        self.userData = (record.StudyModelID)
        self.Key = (record.StudyModelID, record.FromState, record.ToState)

        self.cc_state_from.SetValue((record.FromState))
        self.cc_state_to.SetValue((record.ToState))

        self.tc_probability.SetValue(str(record.Probability))
        self.tc_notes.SetValue(str(record.Notes))



    def SaveRecord(self, record):
        """
        Save/Modify the data of StudyModel object
        This method is called by CheckFocus method in CDMLib
        RowPanel class must implement this method.
        """

        # create new Transition object
        entry = DB.Transition(  StudyModelID = record.StudyModelID,
                                FromState = record.FromState,
                                ToState = record.ToState,
                                Probability = str(record.Probability),
                                Notes = str(record.Notes) )

        frame = self.GetTopLevelParent()
        if self.Id == 0:    # if previous panel is new, create new object
            entry = DB.Transitions.AddNew(entry, ProjectBypassID = frame.idPrj)

        elif self.Id > 0:   # if previous panel is existing one, replace record
            entry = DB.Transitions.Modify(self.Key, entry, ProjectBypassID = frame.idPrj)

        return entry


    def TextRecordID(self):
        """ Returns the identity of the record as text """
        if self.Id == 0:
            Result = 'New Transition'
            FromState = None
            ToState = None
        else:            
            Result = 'Transition saved as "'
            FromState = self.record.FromState
            ToState = self.record.ToState            
            if DB.States.has_key(FromState):
                Result = Result + ' From-State ' + str(DB.States[FromState].Name)
            if DB.States.has_key(ToState):
                Result = Result + ' To-State ' + str(DB.States[ToState].Name)
            if DB.States.has_key(self.record.StudyModelID):
                Result = Result + ' For Model ' + str(DB.StudyModels[self.record.StudyModelID].Name)
            Result = Result + '"'
        FromStateEdited = self.cc_state_from.GetValue()
        ToStateEdited = self.cc_state_to.GetValue() 
        if FromState != FromStateEdited or ToState != ToStateEdited:
            Result = Result + ' Currently changed to'
            if DB.States.has_key(FromStateEdited):
                Result = Result + ' From-State ' + str(DB.States[FromStateEdited].Name)
            else:
                Result = Result + ' From-State is blank'
            
            if DB.States.has_key(ToStateEdited):
                Result = Result + ' To-State ' + str(DB.States[ToStateEdited].Name)
            else:
                Result = Result + ' To-State is blank'
        return Result        


    def SetComboItem(self):
        """
        Set items of ComboCtrl in RowPanel class when focus is moved in current RowPanel instance
        The items are removed when lost focus --> Implemented in CDMFrame class
        RowPanel class that have combo controls must implement this method.
        """

        if self.userData != None:
            StatesInStudyModel = DB.StudyModels[self.userData].FindStatesInStudyModel()
            states = [ (str(state.Name), str(state.Notes), state.ID)
                    for state in DB.States.values() if state.ID in StatesInStudyModel ]

            self.cc_state_from.SetItems(states)
            self.cc_state_to.SetItems(states)


    # Following methods are dedicated to the instance of RowPanel class for Transitions form


    def OnButtonDblClick(self, event):
        """
        Event handler to open child form
        """
        tc = event.GetEventObject()
        cc = tc.GetParent()

        if cc.Id in [ cdml.IDP_BUTTON1, cdml.IDP_BUTTON2 ]:
            collection = DB.States
            key = cc.GetValue()
            form = 'States'
            type_parm = ''

        elif tc.Id == cdml.IDP_BUTTON3:
            collection = DB.Params
            key = tc.GetValue()
            form = 'Parameters'
            if tc.Id == cdml.IDP_BUTTON3:
                type_parm = [ 'Number', 'Integer', 'Epression']
        else:
            raise ValueError, "Assertion Error: Button does not exist"

        if key == '' or key == 0:
            msg = 'This ' + form[:-1] + ' is not defined yet.\n'
            msg += "Do you want to create a new " + form[:-1] + '?'
            ans = cdml.dlgSimpleMsg('ERROR', msg, wx.YES_NO, wx.ICON_ERROR, Parent = self)

            if ans == wx.ID_NO : return
            cdml.OpenForm(form, self, cdml.ID_MODE_SINGL, key, type_parm)

        elif not cdml.GetRecordByKey(collection, key) :
            msg = 'The entry "' + str(key) + '" does not exist in ' + form + '.'
            ans = cdml.dlgSimpleMsg('ERROR', msg, wx.OK, wx.ICON_ERROR, Parent = self)
            return

        else:
            frame = self.GetTopLevelParent()
            cdml.OpenForm(form, self, cdml.ID_MODE_SINGL, key, type_parm, frame.idPrj)


class MainFrame(cdml.CDMFrame):
    """  MainFrame class for the Transitions """

    def __init__(self, mode=None, data=None, type=None, id_prj=0, *args, **kwds):
        """ Constructor of the MainFrame class """
        self.idPrj = id_prj

        cdml.CDMFrame.__init__(self, mode, data, type, *args, **kwds)

        # Deine Popup menu items
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
                            ["Delete" , self.FrameEventHandler, wx.ID_DELETE],
                            ["-" , None, -1 ],
                            ["Find" , self.FrameEventHandler, wx.ID_FIND],
                            ["-" , None, -1 ],
                            ["+From State" , self.FrameEventHandler, cdml.IDF_BUTTON4],
                            ["+To State" , self.FrameEventHandler, cdml.IDF_BUTTON5],
                            ["+Probability" , self.FrameEventHandler, cdml.IDF_BUTTON6],
                            ["Sort By", None, -1])

        # Define the window menus 
        cdml.GenerateStandardMenu(self)

        # create panel for field titles
        # IMPORTANT NOTE:
        #   In current version, name of a panel for the title section should be "pn_title"
        #   And should be an instance of CDMPanel class with False as a first argument
        self.pn_title = cdml.CDMPanel(False, self, -1)
        self.st_title = wx.StaticText(self.pn_title, -1, "Transitions Between States in a Model")

        # Create text and combo control to display the list of studies and models
        # Due to this controls, two step initialization need to be implemented for Transition form
        # --> transition list could be set up after selecting a study or model using this combo control
        self.st_study_model = wx.StaticText(self.pn_title, -1, "Model")
        self.cc_study_model = cdml.Combo(self.pn_title, validator = cdml.KeyValidator(cdml.NO_EDIT))

        # Create bitmap buttons to display title of each field
        # Syntax : cdml.BitmapButton( parent, id, bitmap, label )
        # Don't need to set bitmap here. It will be assigned in the event handler when pressed
        # For the sort function, the labels need to be same with the variable name in database object
        self.button_1 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON1, None, "From State")
        self.button_2 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON2, None, "To State")
        self.button_3 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON3, None, "Probability")
        self.button_4 = cdml.BitmapButton(self.pn_title, cdml.IDF_BUTTON8, None, "Notes")

        # Create Add/Find buttons
        # Syntax : cdml.Button( parent, ID )
        # ID should be wx.ID_ADD for add button and wx.ID_FIND for find button in all forms
        self.btn_add = cdml.Button(self.pn_title, wx.ID_ADD)
        self.btn_find = cdml.Button(self.pn_title, wx.ID_FIND)
        self.btn_copy_from_model = cdml.Button(self.pn_title, cdml.IDF_BUTTON11, 'Copy From Model')

        # Scroll window that the RowPanel objects will be placed
        # IMPORTANT NOTE:
        #   In current version, all forms that need to manage the instance(s) of RowPanel class
        #       should have an instance of wx.ScrolledWindow class.
        #   Also the name of the panel should be "pn_view"
        self.pn_view = wx.ScrolledWindow(self, -1, style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)

        self.__set_properties()
        self.__do_layout()

        # Assign event handler for the buttons in title section -- to check the focus change
        self.pn_title.Bind(wx.EVT_BUTTON, self.FrameEventHandler, id=cdml.IDF_BUTTON1, id2=cdml.IDF_BUTTON8)
        self.btn_add.Bind(wx.EVT_BUTTON, self.FrameEventHandler)
        self.btn_find.Bind(wx.EVT_BUTTON, self.FrameEventHandler)
        self.btn_copy_from_model.Bind(wx.EVT_BUTTON, self.CopyTransitionsFromAnotherStudyModel)

        self.cc_study_model.Bind(wx.EVT_LEFT_UP, self.FrameEventHandler)
        self.cc_study_model.GetTextCtrl().Bind(wx.EVT_LEFT_UP, self.FrameEventHandler)
        # The next line was commented since it worked fine on windows yet did
        # not work on a Linux system. Therefore instead of handling the mouse 
        # click we are looking at the selection of the item form the list. For 
        # some reason this forces repainting of the screen. Yet since it works
        # on both Linux and Windows, this solution was a compromise
        # self.cc_study_model.Bind(wx.EVT_COMMAND_LEFT_CLICK, self.FrameEventHandler)
        self.cc_study_model.Bind(wx.EVT_LIST_ITEM_SELECTED, self.InitTransitions)

        self.InitTransitions() # display existing data


    # Define the default method to handle the menu selections
    OnMenuSelected = cdml.OnMenuSelected



    def __set_properties(self):
        """ Set properties of frame and controls """

        self.SetTitle("TRANSITIONS")
        self.SetSize((960, 600))
        self.SetCollection('Transitions') # or self.Collection = 'Transitions'
        self.HelpContext = 'Transitions'

        self.st_title.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

        self.cc_study_model.SetColumns( (('Name', 150), ('Notes', 332)) )
        self.cc_study_model.SetEvent((None, cdml.ID_EVT_OWN, self.InitTransitions))
        self.cc_study_model.typeData = cdml.ID_TYPE_COMBO

        self.pn_title.isRow = False
        self.pn_view.SetScrollRate(10, 10)

        StandardSize = (150, -1)

        # set sort id and event id for field titles
        for i in range(1,5):
            btn = getattr(self, 'button_' + str(i))
            btn.SetMinSize(StandardSize)
            btn.sortId = i-1
            btn.evtID = cdml.ID_EVT_SORT

        # Build and assign study/model list for the combo control in title section
        study_models = [(sm.Name, sm.Notes, sm.ID) for sm in DB.StudyModels.values() ]
        self.cc_study_model.SetItems(study_models, allowBlank = False)

        # Set default study or model according to the opening mode
        init_id = cdml.iif( self.openData == None, DB.StudyModels.keys()[0], self.openData)
        self.cc_study_model.SetValue(init_id)

        # If specific Study/Model ID was given, disable the Combo control
        self.cc_study_model.Enable(self.openData==None)


    def __do_layout(self):
        """ Set the position of controls """
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)

        grid_sizer_1 = wx.GridBagSizer(0, 0)

        grid_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2.Add(self.st_study_model, 1, wx.ALL|wx.ALIGN_RIGHT)
        grid_sizer_2.Add(self.cc_study_model, 4, wx.ALL|wx.EXPAND)
        grid_sizer_2.Add((1,1),1)
        grid_sizer_2.Add(self.btn_add, 1)
        grid_sizer_2.Add(self.btn_copy_from_model, 2)
        grid_sizer_2.Add(self.btn_find, 1)

        grid_sizer_1.Add(self.st_title, (0,1), (1,5), wx.ALIGN_LEFT, 10)
        grid_sizer_1.Add(grid_sizer_2, (1,1), (1,6), wx.ALL|wx.EXPAND, 0) # 

        grid_sizer_1.Add((28,0), (2,0))
        grid_sizer_1.Add(self.button_1, (2,1), (1,1), wx.ALL, 1) # From
        grid_sizer_1.Add(self.button_2, (3,1), (1,1), wx.ALL, 1) # To
        grid_sizer_1.Add(self.button_3, (2,2), (3,1), wx.ALL|wx.EXPAND, 1) # Probability
        grid_sizer_1.Add(self.button_4, (2,3), (2,1), wx.ALL|wx.EXPAND, 1) # Notes title


        self.pn_title.SetSizer(grid_sizer_1)

        sizer_1.Add(self.pn_title, 2, wx.EXPAND, 1)
        sizer_1.Add(self.pn_view, 10, wx.EXPAND, 1)
        self.pn_view.SetSizer(sizer_3)
        self.SetSizer(sizer_1)
        self.Layout()


    # Actual routine to add new panel
    # Create an instance of RowPanel object
    # this method is called by AddPanel and Initialize method
    # Most form may not need this method. However, Transitions could be changed according to the value of Study/Model combo control
    # two stage initialization need to be implemented for Transition form and Parameter form
    def SetupPanel(self, py=0):
        """ Addtional code of AddPanel method defined in CDMLib.py """

        # Get an ID of study or model from combo control in the title section
        id = self.cc_study_model.GetValue()
        new_panel = RowPanel(id, self.pn_view, 0, pos=(0,py))

        # If the item selected, change the label of a field title.

        self.button_3.SetLabel("Probability")
        self.button_4.SetLabel("Notes")

        self.button_4.Refresh()

        # Same as above, according to the type of item(Study or Model)
        # 4 titles will be shown or hidden.

        return new_panel


    def CopyTransitionsFromAnotherStudyModel(self, event=None):
        """
        Allow the user to copy all the transitions from an existing study/model
        This will bring a dialog box for the user and allow choosing the study
        to copy transitions from.
        """

        DestinationStudyModelID = self.openData
        if DestinationStudyModelID == None or DestinationStudyModelID not in DB.StudyModels.keys():
            raise ValueError, "ASSERTION ERROR: invalid destination study model while copying"
            return

        SortedByNameStudyModelKeys = sorted(DB.StudyModels.keys(), key = lambda Entry: ( DB.StudyModels[Entry].Name , Entry))
        # For a study show studies to copy from, for a model show models.
        SourceStudyModelNames = map (lambda Entry: str(DB.StudyModels[Entry].Name), SortedByNameStudyModelKeys)
        
        dlg = wx.SingleChoiceDialog(self, 'Please select a Model to copy transitions from', 'Copy all Transitions From a Model', SourceStudyModelNames, wx.CHOICEDLG_STYLE )
        
        if dlg.ShowModal() == wx.ID_OK: # then open blank project form
            SelectionIndex = dlg.GetSelection()
            if 0 <= SelectionIndex <= (len(SourceStudyModelNames)-1):
                SourceStudyModelID = SortedByNameStudyModelKeys[SelectionIndex]
                frame = self.GetTopLevelParent()
                (RecordsCopied,RecordsToCopy) = DB.StudyModels[DestinationStudyModelID].CopyTransitionsFromAnotherStudyModel(SourceStudyModelID, ProjectBypassID = frame.idPrj)
                cdml.dlgSimpleMsg('Completed transition copying from another model', str(RecordsCopied) +' out of ' + str(RecordsToCopy) +' transitions were copied. ', wx.OK, wx.ICON_INFORMATION, Parent = self)
                self.InitTransitions()
                


    def InitTransitions(self, event=None):
        """
        Display Transitions for selected Study/Model
        According to the value of combo control and opening mode, this method build the list of object
        then call the Initialize method
        """

            
        if self.openMode == None:
            self.openData = self.cc_study_model.GetValue()

        StudyModel = DB.StudyModels[self.openData]
        SortedTransitionKeys = StudyModel.FindTransitions(SortOption = 'SortByOrderInSubProcess')
        objects = map (lambda TransKey: DB.Transitions[TransKey], SortedTransitionKeys )

        # decide if study or model
        self.Initialize(objects)


if __name__ == "__main__":

    app = wx.App(0)
    #wx.InitAllImageHandlers() Deprecated
    DB.LoadAllData('InData' + DB.os.sep + 'Testing.zip')
    frame_1 = MainFrame(mode=None, data=None, type=None, id_prj=0, parent=None)
    app.SetTopWindow(frame_1)
    frame_1.CenterOnScreen()
    frame_1.Show()
    app.MainLoop()
