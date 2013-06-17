################################################################################
###############################################################################
# Copyright (C) 2013 Jacob Barhak
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
# This file contains a form to define Project                                  #
################################################################################

import DataDef as DB
import CDMLib as cdml
import wx
import wx.grid
import sys
import copy

import Wizard

class MainFrame(wx.Frame):
    """ Main frame for project form"""

    def __init__(self, mode=None, data=None, type=None, id_prj=0, *args, **kwds):

        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwdsnew)

        self.Collection = 'Projects'

        self.idPrj = data     # Current project id.
        self.typePrj = type # Current project type.

        self.HelpContext = self.typePrj

        # List to save simulation rules at each stage
        # stage 2 doesn't have rule, but added here for indexing
        # This list is used to maintain temporary rule data before saving
        self.SimRule = [[], [], [], []]

        # Create empty class to save initial value(s) of project variables
        self.record = cdml.GetInstanceAttr(DB.Project)

        self.curCtrl = None # Current control which is selected for opening of a form
        self.curPage = 0     # Variable to save current page(i.e. tab) number
        self.openMode = mode

        # reset the override population
        self.TempOverridePopulationSet = None

        # Deine Popup menu items
        # Format : tuple of list --> ([Label, Event handler, Id] , [], [], ... )
        #           Label : label of an item
        #           Evet handler : name of event handler
        #           Id : Id of current menu item
        # Special label : '-'--> seperator, '+' --> submenu items
        #           First item after last '+' marked items is the title of the submenu
        # If an item doesn't have event handler, the second parameter should be 'None'
        # If an item doesn't have Id, the third item should be -1
        # In Project form dedicated event handler(OnMenuSelected) is being used
        # to deal with the button press event and focus change.
        self.pup_menus = (  ["Undo", self.OnUndo, wx.ID_UNDO ],
                            ["Copy Record" , self.OnMenuSelected, cdml.ID_MENU_COPY_RECORD],
                            ["Save" , self.OnMenuSelected, wx.ID_SAVE],
                            ["-" , None, -1],
                            ["Run Simulation" , self.OnMenuSelected, wx.ID_APPLY],
                            ["View Result" , self.OnMenuSelected, wx.ID_VIEW_DETAILS])

        # Define the window menus 
        cdml.GenerateStandardMenu(self, SkipItems = [cdml.ID_MENU_REPORT_ALL])

        self.panel_main = wx.Panel(self, -1)
        self.panel_common = wx.Panel(self.panel_main, -1)
        self.notebook = wx.Notebook(self.panel_main, -1, style=0)

        # title
        self.st_title = wx.StaticText(self.panel_main, -1, "Project Definition")

        # Common simulation information
        self.st_name = wx.StaticText(self.panel_common, -1, "Name : ")
        self.tc_name = cdml.Text(self.panel_common, -1, "")
        self.st_from = wx.StaticText(self.panel_common, -1, "Derived From : ")
        self.tc_from = cdml.Text(self.panel_common, -1, "", validator=cdml.KeyValidator(cdml.NO_EDIT))

        self.st_created = wx.StaticText(self.panel_common, -1, "Created On : ")
        self.tc_created = cdml.Text(self.panel_common, -1, "", validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.st_modified = wx.StaticText(self.panel_common, -1, "Last Modified : ")
        self.tc_modified = cdml.Text(self.panel_common, -1, "", validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.st_notes = wx.StaticText(self.panel_common, -1, "Notes : ")
        self.tc_notes = cdml.Text(self.panel_common, -1, "", style = wx.TE_MULTILINE)

        # reserved for future extension

        arrow_up = cdml.getSmallUpArrowBitmap() # arrow bitmap for buttons
        arrow_dn = cdml.getSmallDnArrowBitmap()

        self.btn_save = wx.Button(self.panel_main, wx.ID_SAVE)
        self.btn_copy = wx.Button(self.panel_main, cdml.ID_MENU_COPY_RECORD, "Copy")
        self.btn_undo = wx.Button(self.panel_main, wx.ID_UNDO)

        # simulation conditions
        self.panel_sim = wx.Panel(self.panel_main, -1)
        self.st_pset = wx.StaticText(self.panel_sim, -1, "Population Set : ")
        self.cc_pset = cdml.Combo(self.panel_sim, cdml.IDF_BUTTON1, validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.st_simsteps = wx.StaticText(self.panel_sim, -1, "No. of Simulation Steps : ")
        self.tc_simsteps = cdml.Text(self.panel_sim, -1, "")
        self.st_model = wx.StaticText(self.panel_sim, -1, "Primary Model : ")
        self.cc_model = cdml.Combo(self.panel_sim, cdml.IDF_BUTTON2, validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.st_repet = wx.StaticText(self.panel_sim, -1, "No. of Repetitions : ")
        self.tc_repet = cdml.Text(self.panel_sim, -1, "")

        self.btn_ed_pset = wx.Button(self.panel_sim, cdml.IDF_BUTTON3, "...")
        self.btn_ed_model = wx.Button(self.panel_sim, cdml.IDF_BUTTON4, "...")

        self.btn_run = wx.Button(self.panel_sim, wx.ID_APPLY, "Run Simulation")
        self.btn_result = wx.Button(self.panel_sim, wx.ID_VIEW_DETAILS, "View Result")
        self.btn_delete = wx.Button(self.panel_sim, wx.ID_CLEAR, "Delete Results")


        # create tabs for simulation stage
        self.nb_pane_0 = wx.Panel(self.notebook, 0)
        self.nb_pane_1 = wx.Panel(self.notebook, 1)
        self.nb_pane_2 = wx.Panel(self.notebook, 2)
        self.nb_pane_3 = wx.Panel(self.notebook, 3)

        
        # simulation stage 0 : initialization
        self.tab0_label = wx.StaticText(self.nb_pane_0, -1, "Initialize the simulation")
        self.tab0_list = cdml.List(self.nb_pane_0, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        # simulation stage 1 - Pre state transition
        self.tab1_label = wx.StaticText(self.nb_pane_1, -1, "Pre-State Transition Rules")
        self.tab1_list = cdml.List(self.nb_pane_1, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        # simulation stage 2
        self.tab2_label = wx.StaticText(self.nb_pane_2, -1, "Execute state transitions according to the primary model:", style=wx.ALIGN_CENTRE)
        self.tab2_st_model = wx.StaticText(self.nb_pane_2, -1, "")
        self.tab2_st_TraceBack = wx.StaticText(self.nb_pane_2, -1, "Pickled TraceBack Information for Reproducing simulation")
        self.tab2_tc_TraceBack = cdml.Text(self.nb_pane_2, -1, "", style = wx.TE_MULTILINE)
     
        # show the TraceBack fields only in Admin mode
        TraceBackIsVisible = cdml.GetAdminMode()
        self.tab2_st_TraceBack.Show(TraceBackIsVisible)
        self.tab2_tc_TraceBack.Show(TraceBackIsVisible)


        # simulation stage 3 - Post state transition
        self.tab3_label = wx.StaticText(self.nb_pane_3, -1, "Post-State Transition Rules")
        self.tab3_list = cdml.List(self.nb_pane_3, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)


        # combo boxes
        self.panel_combo = wx.Panel(self.panel_main, -1)
        self.label_1 = wx.StaticText(self.panel_combo, -1, "Covariate")
        self.label_2 = wx.StaticText(self.panel_combo, -1, "Occurrence Probability")
        self.label_3 = wx.StaticText(self.panel_combo, -1, "Function")
        self.label_4 = wx.StaticText(self.panel_combo, -1, "Notes")

        self.combo_box_1 = cdml.Combo(self.panel_combo, cdml.IDP_BUTTON1)
        self.combo_box_2 = cdml.Combo(self.panel_combo, cdml.IDP_BUTTON2)
        self.combo_box_2.AllowInput = True
        self.combo_box_3 = cdml.Combo(self.panel_combo, cdml.IDP_BUTTON3)
        self.combo_box_3.AllowInput = True
        self.tc_notes_rule = cdml.Text(self.panel_combo, cdml.IDP_BUTTON4)


        # Up/Down arrow button, Cost and QoL Wizard button
        self.btn_up = wx.BitmapButton(self.panel_combo, wx.ID_ADD, arrow_up)
        self.btn_dn = wx.BitmapButton(self.panel_combo, wx.ID_DELETE, arrow_dn)


        # Bind common event handler for Project form
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnPopupMenu) # Dedicated event handler for popup menu
        self.Bind(wx.EVT_CLOSE, self.OnMenuSelected)
        self.Bind(wx.EVT_END_PROCESS, self.OnRefresh)

        self.btn_save.Bind(wx.EVT_BUTTON, self.OnMenuSelected)
        self.btn_copy.Bind(wx.EVT_BUTTON, self.OnMenuSelected)
        self.btn_undo.Bind(wx.EVT_BUTTON, self.OnUndo)

        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

        self.btn_up.Bind(wx.EVT_BUTTON, self.ChangeSimulaionRules)
        self.btn_dn.Bind(wx.EVT_BUTTON, self.ChangeSimulaionRules)

        self.btn_run.Bind(wx.EVT_BUTTON, self.OnMenuSelected)
        self.btn_result.Bind(wx.EVT_BUTTON, self.OnMenuSelected)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.OnMenuSelected)

        self.btn_ed_pset.Bind(wx.EVT_BUTTON, self.OnLeftDblClick)
        self.btn_ed_model.Bind(wx.EVT_BUTTON, self.OnLeftDblClick)

        self.cc_pset.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDblClick)
        self.cc_model.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDblClick)

        self.combo_box_1.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDblClick)
        self.combo_box_2.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDblClick)
        self.combo_box_3.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDblClick)
        self.tc_notes_rule.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDblClick)

        self.__set_properties()
        self.__do_layout()

        # This method is different from the Initialize method of CDMFrame class
        # It is implemented in this module
        self.Initialize()



    def __set_properties(self):
        """ Define properties of frame and controls """

        self.SetTitle("PROJECT DEFINITION")
        self.SetSize((850, 730))
        self.MakeModal(True)

        f = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "")
        self.st_title.SetFont(f)

        self.tc_name.SetMinSize((150, -1))
        self.tc_from.SetMinSize((150, -1))
        self.tc_notes.SetMinSize((200, 45))
        self.tc_created.SetMinSize((150, -1))
        self.tc_modified.SetMinSize((150, -1))

        self.tc_created.dataType = cdml.ID_TYPE_NONE
        self.tc_modified.dataType = cdml.ID_TYPE_NONE

        columns = ( ['Affected Parameter', 205], 
                    ['Occurrence Probability', 205], 
                    ['Function', 205],
                    ['Notes', 215] )

        self.cc_pset.SetMinSize((200, 21))
        self.cc_pset.SetColumns((('Name', 150),('Type', 70),('Notes', 332)))
        self.cc_pset.InRow = False

        self.cc_model.SetMinSize((200, 21))
        self.cc_model.SetColumns((('Name', 150), ('Notes', 332)))
        self.cc_model.InRow = False

        self.btn_ed_pset.SetMinSize((20,20))
        self.btn_ed_model.SetMinSize((20,20))

        self.tc_simsteps.dataType = cdml.ID_TYPE_INTEG
        self.tc_repet.dataType = cdml.ID_TYPE_INTEG

        self.st_simsteps.SetToolTipString("Simulation Stop Criterion")

        self.btn_up.SetMinSize((30, 30))
        self.btn_dn.SetMinSize((30, 30))

        f = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "")
        for i in [3,1,0]:
            list = getattr(self, 'tab%d_list' % i)
            list.SetMinSize((825,250))
            list.CreateColumns(columns)
            list.AllowBlank = False

            getattr(self, 'tab%d_label' % i).SetFont(f)


        self.tab2_label.SetFont(f)
        self.tab2_st_model.SetFont(f)
        self.tab2_tc_TraceBack.SetMinSize((200, 200))

        self.combo_box_1.SetMinSize((200, -1))
        self.combo_box_1.SetColumns((('Name', 200), ('Notes', 332)))
        self.combo_box_1.InRow = False

        self.combo_box_2.SetMinSize((200, -1))
        self.combo_box_2.SetColumns((('Name', 200), ('Formula', 150), ('Notes', 150)))
        self.combo_box_2.InRow = False

        self.combo_box_3.SetMinSize((200, -1))
        self.combo_box_3.SetColumns((('Name', 200), ('Formula', 150), ('Notes', 150)))
        self.combo_box_3.InRow = False

        self.tc_notes_rule.SetMinSize((200,-1))

        self.SetComboItems(None, 0)




    def __do_layout(self):
        """ Arrange panels and controls in this frame """
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_v = wx.BoxSizer(wx.VERTICAL)

        # title
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(self.st_title, 0, flag=wx.ALL, border=10)
        sizer_h.Add((355,0), 0)
        sizer_h.Add(self.btn_save, 0, flag=wx.ALIGN_BOTTOM|wx.ALL, border=1)
        sizer_h.Add(self.btn_copy, 0, flag=wx.ALIGN_BOTTOM|wx.ALL, border=1)
        sizer_h.Add(self.btn_undo, 0, flag=wx.ALIGN_BOTTOM|wx.ALL, border=1)
        sizer_v.Add(sizer_h, 0, wx.EXPAND, 0)
        sizer_v.Add(wx.StaticLine(self.panel_main, -1, (0,0), (self.GetSizeTuple()[0],1)))

        # common information
        gb_sizer_1 = wx.GridBagSizer(0, 0)
        gb_sizer_1.Add((40,0), (0,0))
        gb_sizer_1.Add(self.st_name, (0,1), flag=wx.ALL|wx.ALIGN_RIGHT, border=1)
        gb_sizer_1.Add(self.st_from, (1,1), flag=wx.ALL|wx.ALIGN_RIGHT, border=1)

        gb_sizer_1.Add(self.tc_name, (0,2), flag=wx.ALL, border=1)
        gb_sizer_1.Add(self.tc_from, (1,2), flag=wx.ALL, border=1)

        gb_sizer_1.Add(self.st_created, (0,4), flag=wx.ALL|wx.ALIGN_RIGHT, border=1)
        gb_sizer_1.Add(self.st_modified, (1,4), flag=wx.ALL|wx.ALIGN_RIGHT, border=1)
        gb_sizer_1.Add(self.tc_created, (0,5), flag=wx.ALL, border=1)
        gb_sizer_1.Add(self.tc_modified, (1,5), flag=wx.ALL, border=1)
        gb_sizer_1.Add((40,0), (0,6))
        gb_sizer_1.Add(self.st_notes, (0,7), flag=wx.ALL|wx.ALIGN_RIGHT, border=1)
        gb_sizer_1.Add(self.tc_notes, (0,8), (2,2), flag=wx.ALL , border=1)

        self.panel_common.SetSizer(gb_sizer_1)
        sizer_v.Add(self.panel_common, 0, wx.EXPAND|wx.ALL, 5)

        space = int((self.GetSizeTuple()[0] - 80)*.5) # space from left edge of form to up arrow button

        # Remove the pages
        while self.notebook.GetPageCount()>0:
            self.notebook.RemovePage(0)

        self.panel_sim.Show(True)
        self.panel_combo.Show(True)
        self.nb_pane_0.Show(True)
        self.nb_pane_1.Show(True)
        self.nb_pane_2.Show(True)
        self.nb_pane_3.Show(True)

        # simulation information
        gb_sizer_2 = wx.GridBagSizer(0, 0)
        gb_sizer_2.Add((35,0), (0,0))
        gb_sizer_2.Add((30,0), (0,4))
        gb_sizer_2.Add((20,0), (0,7))
        gb_sizer_2.Add(self.st_model,(0,1), flag=wx.ALL|wx.ALIGN_RIGHT, border=1)
        gb_sizer_2.Add(self.cc_model,(0,2), flag=wx.ALL, border=1)
        gb_sizer_2.Add(self.btn_ed_model,(0,3), flag=wx.ALL, border=1)

        gb_sizer_2.Add(self.st_simsteps, (0,5), flag=wx.ALL|wx.ALIGN_RIGHT, border=1)
        gb_sizer_2.Add(self.tc_simsteps, (0,6), flag=wx.ALL, border=1)
        gb_sizer_2.Add(self.btn_run, (0,8), (1,2), flag=wx.EXPAND|wx.ALL, border=1)

        gb_sizer_2.Add(self.st_pset, (1,1), flag=wx.ALL|wx.ALIGN_RIGHT, border=1)
        gb_sizer_2.Add(self.cc_pset, (1,2), flag=wx.ALL, border=1)
        gb_sizer_2.Add(self.btn_ed_pset, (1,3), flag=wx.ALL, border=1)
        gb_sizer_2.Add(self.st_repet,(1,5), flag=wx.ALL|wx.ALIGN_RIGHT, border=1)
        gb_sizer_2.Add(self.tc_repet,(1,6), flag=wx.ALL, border=1)
        gb_sizer_2.Add(self.btn_result, (1,8), (1,1), flag=wx.EXPAND|wx.ALL, border=1)
        gb_sizer_2.Add(self.btn_delete, (1,9), (1,1), flag=wx.EXPAND|wx.ALL, border=1)

        self.panel_sim.SetSizer(gb_sizer_2)
        sizer_v.Add(self.panel_sim, 0, wx.EXPAND|wx.ALL, 5)

        # tab 0
        sizer_v0 = wx.BoxSizer(wx.VERTICAL)
        sizer_v0.Add(self.tab0_label, 0, wx.EXPAND|wx.ALL, 3)
        sizer_v0.Add(self.tab0_list, 0, wx.EXPAND|wx.ALL, 3)
        self.nb_pane_0.SetSizer(sizer_v0)

        # tab 1
        sizer_v1 = wx.BoxSizer(wx.VERTICAL)
        sizer_v1.Add(self.tab1_label, 0, wx.EXPAND|wx.ALL, 3)
        sizer_v1.Add(self.tab1_list, 0, wx.EXPAND|wx.ALL, 3)
        self.nb_pane_1.SetSizer(sizer_v1)

        # tab 2

        sizer_v2 = wx.BoxSizer(wx.VERTICAL)
        sizer_v2.Add((0,20),0,0,0)
        sizer_v2.Add(self.tab2_label, 0, wx.TOP, 10)
        sizer_v2.Add(self.tab2_st_model, 0, wx.TOP, 10)
        sizer_v2.Add((0,20),0,0,0)
        sizer_v2.Add(self.tab2_st_TraceBack, 0, wx.TOP, 10)
        sizer_v2.Add(self.tab2_tc_TraceBack, 0, wx.EXPAND|wx.ALL, 10)
        
        self.nb_pane_2.SetSizer(sizer_v2)


        # tab 3
        sizer_v3 = wx.BoxSizer(wx.VERTICAL)
        sizer_v3.Add(self.tab3_label, 0, wx.EXPAND|wx.ALL, 3)
        sizer_v3.Add(self.tab3_list, 0, wx.EXPAND|wx.ALL, 3)
        self.nb_pane_3.SetSizer(sizer_v3)

        # add each panel to notebook control as pages
        self.notebook.AddPage(self.nb_pane_0, "Stage 0 - Initialization")
        self.notebook.AddPage(self.nb_pane_1, "Stage 1 - Pre-State Transition Rules")
        self.notebook.AddPage(self.nb_pane_2, "Stage 2 - Execute State Transitions")
        self.notebook.AddPage(self.nb_pane_3, "Stage 3 - Post-State Transition Rules")

        sizer_v.Add(self.notebook, 0, wx.EXPAND, 0)

        sizer_v5 = wx.BoxSizer(wx.VERTICAL)
        sizer_h1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h1.Add((space,0), 0, 0, 0)
        sizer_h1.Add(self.btn_up, 0, wx.ALL, 3)
        sizer_h1.Add(self.btn_dn, 0, wx.ALL, 3)
        sizer_v5.Add(sizer_h1, 0, 0, 0)

        # combo boxes
        gb_sizer_6 = wx.GridBagSizer(0,0)
        gb_sizer_6.Add(self.label_1, (0,1), (1,1), wx.ALL, 3)
        gb_sizer_6.Add(self.label_2, (0,2), (1,1), wx.ALL, 3)
        gb_sizer_6.Add(self.label_3, (0,3), (1,1), wx.ALL, 3)
        gb_sizer_6.Add(self.label_4, (0,4), (1,1),  wx.ALL, 3)
        gb_sizer_6.Add(self.combo_box_1, (1,1), (1,1), wx.LEFT|wx.BOTTOM, 3)
        gb_sizer_6.Add(self.combo_box_2, (1,2), (1,1), wx.LEFT|wx.BOTTOM, 3)
        gb_sizer_6.Add(self.combo_box_3, (1,3), (1,1), wx.LEFT|wx.BOTTOM, 3)
        gb_sizer_6.Add(self.tc_notes_rule, (1,4), (1,1), wx.LEFT|wx.BOTTOM, 3)
        sizer_v5.Add(gb_sizer_6, 0, 0, 0)
        self.panel_combo.SetSizer(sizer_v5)

        sizer_v.Add(self.panel_combo, 0, wx.EXPAND, 0)

        self.panel_main.SetSizer(sizer_v)
        sizer_1.Add(self.panel_main, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_1)
        self.Layout()
        self.Fit()

        


    def Initialize(self):
        """ Assign initial values to the controls """
        self.record.ID = self.idPrj
        project = cdml.GetRecordByKey(DB.Projects, self.idPrj)
        if cdml.Exist(project): # if project != None, create temporary copy of the project data
            self.record.Name = str(project.Name)
            self.record.Notes = str(project.Notes)
            self.record.PrimaryModelID = project.PrimaryModelID
            self.record.DerivedFrom = project.DerivedFrom
            self.record.PrimaryPopulationSetID = project.PrimaryPopulationSetID
            self.record.NumberOfSimulationSteps = project.NumberOfSimulationSteps
            self.record.NumberOfRepetitions = project.NumberOfRepetitions
            self.record.CreatedOn = project.CreatedOn
            self.record.LastModified = project.LastModified
            self.record.SimulationRules = project.SimulationRules

            self.SimRule = [[], [], [], []]
            for rule in self.record.SimulationRules: 
                self.SimRule[rule.SimulationPhase].append(rule)

        self.ShowProjectData()
        


    def CopyProject(self):
        """ Copies project and refreshes the form accordingly with the copied Data """
        # It is assumed that the data is saved
        # Eclose the copying in a try statement just in case of an error
        copy_ok = False
        try:
            new_record = DB.Projects.Copy(self.idPrj)
            copy_ok = True
        except:
            cdml.dlgErrorMsg(Parent = self)
       
        if copy_ok:
            self.idPrj = new_record.ID
            self.Initialize()

        return copy_ok
       
              

    def SetComboItems(self, ctrl=None, page=-1):
        """
        Build list for the combo controls for a simulation  project
        """

        if ctrl == None :
            id_ctrl = None
        else:
            id_ctrl = ctrl.Id


        if ctrl is None or id_ctrl in [ cdml.IDF_BUTTON1, cdml.IDF_BUTTON3 ]:
            # distribution population sets are now allowed, the next commented
            pset = [ (str(ps.Name), DB.Iif(ps.IsDistributionBased(),'Distribution','Data'), str(ps.Notes), ps.ID) for ps in DB.PopulationSets.values() ]
            self.cc_pset.SetItems(pset)

        if ctrl is None or id_ctrl in [ cdml.IDF_BUTTON2, cdml.IDF_BUTTON4 ]:
            model = [(str(sm.Name), str(sm.Notes), sm.ID)
                        for sm in DB.StudyModels.values() ]
            self.cc_model.SetItems(model)


        parameters = DB.Params.values()
        if ctrl is None or id_ctrl == cdml.IDP_BUTTON1:
            if page in [0,1,3]:
                items = [ (str(parm), parm.Notes, -1)
                          for parm in parameters if parm.ParameterType in (['System Option']*(page==0) + ['Number','Integer','State Indicator'])]
            self.combo_box_1.SetItems(items)


        if ctrl is None or id_ctrl == cdml.IDP_BUTTON2:
            function = [ (str(parm), str(parm.Formula), str(parm.Notes), -1)
                         for parm in parameters if parm.ParameterType == 'Expression']
            self.combo_box_2.SetItems(function)

        if ctrl is None or id_ctrl == cdml.IDP_BUTTON3:
            function = [ (str(parm), str(parm.Formula), str(parm.Notes), -1)
                         for parm in parameters if parm.ParameterType == 'Expression']
            self.combo_box_3.SetItems(function)





    def ShowProjectData(self):
        """ Display data for current project
            If current project is new one, do nothing """

        self.tc_name.SetValue(str(self.record.Name))

        from_prj = cdml.GetRecordByKey(DB.Projects, self.record.DerivedFrom)
        if from_prj:
            self.tc_from.SetValue(str(from_prj.Name))
        self.tc_created.SetValue(self.record.CreatedOn)
        self.tc_modified.SetValue(self.record.LastModified)
        self.tc_notes.SetValue(str(self.record.Notes))

        self.cc_pset.SetValue(self.record.PrimaryPopulationSetID)
        self.cc_model.SetValue(self.record.PrimaryModelID)
        self.tc_simsteps.SetValue(self.record.NumberOfSimulationSteps)
        self.tc_repet.SetValue(self.record.NumberOfRepetitions)

        self.tab0_list.DeleteAllItems()
        self.tab1_list.DeleteAllItems()
        self.tab3_list.DeleteAllItems()

        for rule in self.record.SimulationRules:

            item = (str(rule.AffectedParam), str(rule.OccurrenceProbability), str(rule.AppliedFormula), str(rule.Notes), -1)
            list = getattr(self, 'tab' + str(rule.SimulationPhase) + '_list')
            list.AddItem(item, list.GetItemCount())

        self.ClearPanel(self.panel_combo)
        self.tc_name.SetFocus()
        self.tc_name.SetInsertionPoint(0)


    def ShowControls(self, targets, show):
        """ Show/Hide controls in a list"""
        for item in targets:
            item.Show(show)


    def OnLeftDblClick(self, event):
        """ Event handler to open child form"""

        ctrl = event.GetEventObject()

        type = ''
        if ctrl.Id == cdml.IDF_BUTTON3: # Population Set
            cc = self.cc_pset
            id_obj = cc.GetValue()
            form = 'PopulationSets'

        elif ctrl.Id == cdml.IDF_BUTTON4 : # Primary Model
            cc = self.cc_model
            id_obj = cc.GetValue()
            form = 'StudyModels'

        elif ctrl.Id == cdml.IDP_BUTTON4:
            # The notes rule text
            cc = ctrl
            TheTextControl = cc
            id_obj = cc.GetValue()
            DefaultText = id_obj
            form = ''

        else:

            cc = ctrl.GetParent()
            TheTextControl = cc.GetTextCtrl()
            if cc.Id == cdml.IDF_BUTTON1:
                id_obj = cc.GetValue()
                form = 'PopulationSets'

            elif cc.Id == cdml.IDF_BUTTON2:
                id_obj = cc.GetValue()
                form = 'StudyModels'

           
            else:
                id_obj = str(cc.GetValueString())
                DefaultText = id_obj

                if cc.Id == cdml.IDP_BUTTON1:
                    form = 'Parameters'
                    type = ['System Option']*(self.curPage==0) + ['Number','Integer','State Indicator']


                elif cc.Id == cdml.IDP_BUTTON2:
                    form = ''
                    type = 'Expression'

                elif cc.Id == cdml.IDP_BUTTON3:
                    form = ''
                    type = 'Expression'
                    if ('CostWizard' in DefaultText):
                        form = 'WIZARD'

        self.curCtrl = cc

        if form == 'WIZARD':
            try:
                Sequence = DB.CostWizardParserForGUI(DefaultText, True)
                dlg_wizard = Wizard.WizardDialog(data=Sequence, parent=self)
                dlg_wizard.CenterOnScreen()

                dlg_wizard.Show()
                dlg_wizard.MakeModal()
    
            except:
                cdml.dlgErrorMsg(Parent = self)

        elif form == '':
            TheText = cdml.dlgTextEntry(Message = 'Modify Text and Press OK, or Press Cancel to ignore changes', Caption = type, DefaultValue = DefaultText, Parent = self)
            TheTextControl.SetValue(str(TheText))
            # make sure focus returne properly to this form
            self.MakeModal()  
            self.Raise()
            
        else:
            if id_obj == 0 or id_obj == '' : id_obj = -1
            cdml.OpenForm(form, self, cdml.ID_MODE_SINGL, id_obj, type, self.idPrj)


    def OnPageChanged(self, event):
        """ Display controls according to selected tab"""

        cpage = self.curPage = event.GetSelection()


        if cpage == 2 : # simulation stage 2
            self.tab2_st_model.SetLabel(str(self.cc_model.GetValueString()))

        else:
             # Build the item for combo_box_1 according to the page of tab control
            self.label_1.SetLabel('Parameter')
            self.combo_box_1.SetColumns((('Name', 200), ('Notes', 332)))
            self.SetComboItems(self.combo_box_1, cpage)
            self.ClearPanel(self.panel_combo)


        self.ShowControls([self.btn_up, self.btn_dn, self.panel_combo], cpage != 2)

        x, y = self.btn_dn.GetPositionTuple()
        w, h = self.btn_dn.GetSizeTuple()

        self.Refresh()
        event.Skip()


    def OnRefresh(self, event):
        """ Refresh data after closing child form """

        # This line wa previously:
        # self.SetComboItems(self.curCtrl, self.curPage)
        # Yet o allow the user to create new paameters for all
        # combo boxes it was decided to update all combo boxes
        # if the is inefficient, then the previous approach should be rerolled
        if self.curCtrl == self.combo_box_1:
            self.SetComboItems(self.combo_box_1, self.curPage)
            self.SetComboItems(self.combo_box_2, self.curPage)
            self.SetComboItems(self.combo_box_3, self.curPage)
        else:
            self.SetComboItems(None, self.curPage)
            
        record = cdml.GetRefreshInfo()

        if record == None:
            id_record = 0
        elif type(record)==str or not hasattr(record,'ID'):
            # For cost wizard and parameters that their id is their name
            id_record = record

        else:
            id_record = record.ID

        if self.curCtrl != None: # on return from result viewer this can be 0
            if self.curCtrl.Id == cdml.IDF_BUTTON1:
                self.cc_pset.SetValue(id_record)

            elif self.curCtrl.Id == cdml.IDF_BUTTON2:
                if record == None :
                    self.cc_model.GetTextCtrl().SetValue('')
                else:
                    self.cc_model.SetValue(id_record)

            else:

                if self.curCtrl.Id in [ cdml.IDP_BUTTON1, cdml.IDP_BUTTON2, cdml.IDP_BUTTON3, cdml.IDP_BUTTON4]:
                    if record == None :
                        self.curCtrl.SetValue(0)
                    else:                
                        self.curCtrl.GetTextCtrl().SetValue(id_record)
            self.curCtrl.SetFocus()
        self.curCtrl = None


    def ChangeSimulaionRules(self, event):
        """ Add/Remove simulation rules when user click up/down button"""
        id_btn = event.GetId()

        lc = getattr( self, 'tab' + str(self.curPage) + '_list' )
        index = lc.GetFirstSelected()

        try :
            list_rules = getattr(self, 'SimRule')[self.curPage]
            if id_btn == wx.ID_ADD: # UP ARROW - Add/Insert a rule
                if index == -1 : index = lc.GetItemCount()

                rule = []
                no_blank = 0
                for i in range(3):
                    cc = getattr(self, 'combo_box_'+str(i+1))
                    rule.append( str(cc.GetValueString()) )
                    if rule[i] == '' : no_blank += 1

                if no_blank == 3 : return  # no rules are set in the combo boxes

                notes = str(self.tc_notes_rule.GetValue())
                new_rule = DB.SimulationRule(rule[0], self.curPage, rule[1], rule[2], notes)


                list_rules.insert(index, new_rule)
                lc.AddItem((rule[0], rule[1], rule[2], notes, -1), index)
                # Do not clear panel so that it can be used as a clipboard
                # for copy operations. 
                #self.ClearPanel(self.panel_combo)

            else: # DOWN ARROW - Remove a rule
                if index == -1 : return

                # the new implementation is:
                # get the information from the list_rules buffer rather than
                # from the listbox in the screen. 
                cur_rule = [str(list_rules[index].AffectedParam), str(list_rules[index].OccurrenceProbability), str(list_rules[index].AppliedFormula), str(list_rules[index].Notes) ]
                for i in range(3):
                    cc = getattr(self, 'combo_box_' + str(i+1))
                    cc.GetTextCtrl().SetValue(cur_rule[i])
                self.tc_notes_rule.SetValue(cur_rule[-1])

                list_rules.pop(index)
                lc.DeleteItem(index)
                lc.Select(index, True)
        except:
            cdml.dlgErrorMsg(Parent = self)



    def OnPopupMenu(self, event):
        """ Open Popup menu """

        if not hasattr(self, 'pup_menus'): return

        menu = cdml.setupMenu(self, self.pup_menus, False)  # crate popup menu and assign event handler


        self.PopupMenu(menu)    # open popup menu
        menu.Destroy()          # remove from memory to show just once when right button is clicked


    def OnUndo(self, event):
        """ Method for Undo function. Restore recent values which wasn't saved """

        self.ShowProjectData() # display initial data

        # Reset Rules list and StudyModel list with initial values
        self.SimRule = [[], [], [], []]
        for rule in self.record.SimulationRules:
            getattr(self, 'SimRule')[self.curPage].append(rule)


    def CheckData(self):
        """ Check the value of controls and if changed save/modify current project"""
        # Create temporary record to get current data
        cur_record = copy.copy(self.record)

        cur_record.Name = str(self.tc_name.GetValue())
        cur_record.Notes = str(self.tc_notes.GetValue())
        cur_record.DerivedFrom = self.record.DerivedFrom


        # reset all other parameters by default, then rebuild them
        # according to project type
        cur_record.PrimaryModelID = 0
        cur_record.PrimaryPopulationSetID = 0
        cur_record.NumberOfSimulationSteps = 0
        cur_record.NumberOfRepetitions = 0
        cur_record.SimulationRules = []

        cur_record.PrimaryModelID = self.cc_model.GetValue()
        cur_record.PrimaryPopulationSetID = self.cc_pset.GetValue()
        cur_record.NumberOfSimulationSteps = self.tc_simsteps.GetValue()
        cur_record.NumberOfRepetitions = self.tc_repet.GetValue()

        cur_record.SimulationRules = self.SimRule[0] + \
                                     self.SimRule[1] + \
                                     self.SimRule[3]

        save_ok = False

        if not DB.IsEqualDetailed(cur_record, self.record): # if any data has been changed
            # create new project object
            new_prj = DB.Project(   0,
                                    str(cur_record.Name),
                                    str(cur_record.Notes),
                                    cur_record.PrimaryModelID,
                                    cur_record.PrimaryPopulationSetID,
                                    cur_record.NumberOfSimulationSteps,
                                    cur_record.NumberOfRepetitions,
                                    cur_record.SimulationRules,
                                    cur_record.DerivedFrom )

            if  self.idPrj in DB.Projects.keys() : # If current project exists in DB, modify it
                new_prj = DB.Projects.Modify(self.idPrj, new_prj)

            else:   # Else save it --> New Project
                new_prj = DB.Projects.AddNew(new_prj)

            # save current record for next changes
            self.idPrj = new_prj.ID
            self.record = cur_record
            self.record.ID = self.idPrj
            self.record.CreatedOn = new_prj.CreatedOn
            self.record.LastModified = new_prj.LastModified

            # refresh time stamp
            self.tc_created.SetValue(self.record.CreatedOn)
            self.tc_modified.SetValue(self.record.LastModified)

            save_ok = True

        return save_ok


    def OnMenuSelected(self, event):
        """ Do something when action buttons are clicked.
            Action buttons are Save, Run Simulation, View Result and Close"""
        menuId = event.GetId()
        evtType = event.GetEventType()

        if evtType==wx.wxEVT_COMMAND_MENU_SELECTED:
            if menuId not in [cdml.ID_MENU_REPORT_ALL]:
                # Use the default handler first and if no more processing needed return
                if cdml.OnMenuSelected(self, event):
                    return

        try:
            # In any case, if a button - Save, Run, View Result - is clicked, data will be save
            save_ok = self.CheckData()

            if evtType == wx.wxEVT_CLOSE_WINDOW:    # Close Window Event
                #cdml.CloseForm(self, True, self.Collection, self.idPrj)
                cdml.CloseForm(self, True)
                return

            elif menuId == cdml.ID_MENU_COPY_RECORD:
                copy_ok = self.CopyProject()
                if not copy_ok: return
                cdml.dlgSimpleMsg('INFO', 'The project has been successfully copied - you are now working on the new copy', wx.OK, wx.ICON_INFORMATION, Parent = self)
            elif menuId == wx.ID_SAVE :
                if not save_ok: return
                cdml.dlgSimpleMsg('INFO', 'The project data has been saved successfully', wx.OK, wx.ICON_INFORMATION, Parent = self)

            elif menuId == wx.ID_APPLY:             # Run Simulation
                self.RunSimulation()

            elif menuId == wx.ID_VIEW_DETAILS:  # View Results / Extract PopulationSets
                self.ShowSimResult()

            elif menuId == wx.ID_CLEAR:

                result_ids = [ result.ID for result in DB.SimulationResults.values()
                                if result.ProjectID == self.idPrj ]

                if result_ids == [] :
                    cdml.dlgSimpleMsg('ERROR', "There are no simulation results for this project", Parent = self)
                else:
                    ans = cdml.dlgSimpleMsg('WARNING', 'Simulation results will be deleted permanently.\nDo you want to continue with deletion?', wx.YES_NO, wx.ICON_WARNING, Parent = self)
                    if ans == wx.ID_NO: return

                    for id in result_ids:
                        DB.SimulationResults.Delete(id, ProjectBypassID = self.idPrj)

                    cdml.dlgSimpleMsg('INFO', 'All simulation results were deleted', wx.OK, wx.ICON_INFORMATION, Parent = self)

        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            need_ans = cdml.iif(evtType == wx.wxEVT_CLOSE_WINDOW, True, False)
            if cdml.dlgErrorMsg(yesno=need_ans, Parent = self) == wx.ID_NO:
                cdml.CloseForm(self, False)


    def RunSimulation(self):
        """ Simulation control routine. Check user response to begin simulation and display messages"""

        ans = cdml.dlgSimpleMsg('INFO', 'Running a simulation may take some time. Do you want to continue?', wx.YES_NO, wx.ICON_INFORMATION, Parent = self)
        if ans == wx.ID_NO: return

        TheProgressDialog = None
        try:
            def ExtractTraceBack():
                try:
                    # Extract Traceback if exists
                    TraceBackText = self.tab2_tc_TraceBack.GetValue()
                    if TraceBackText == '':
                        SimulationTraceBack = None
                    else:
                        SimulationTraceBack = DB.pickle.loads(TraceBackText)
                except:
                    raise ValueError, 'TraceBack Error: Could not properly extract TraceBack - please make sure a proper TraceBack was entered'
                    SimulationTraceBack = None
                return SimulationTraceBack
                            
            # version 2.5 does not support canceling simulation
            TheProgressDialog = cdml.ProgressDialogTimeElapsed(Parent = self, StartTimerUponCreation = False, AllowCancel = DB.SystemSupportsProcesses)
            # Define the Function to run on a thread/process
            def GenerationStartMiniScript():
                "Compile and execute the generation"
                prj = DB.Projects[self.idPrj]
                PopID = prj.PrimaryPopulationSetID
                NumberOfRepetitions = prj.NumberOfRepetitions
                Pop = DB.PopulationSets[PopID]
                
                if Pop.IsDistributionBased():
                    SimulationTraceBack = ExtractTraceBack()
                    if SimulationTraceBack == None:
                        PopulationTraceBack = None
                    else:
                        PopulationTraceBack = SimulationTraceBack[-1]
                    # if the population is distribution based, then 
                    # Compile the generation script with default options
                    ScriptFileNameFullPath = Pop.CompilePopulationGeneration(GeneratedPopulationSize = NumberOfRepetitions, GenerationFileNamePrefix = None, OutputFileNamePrefix = None , RandomStateFileNamePrefix = None, GenerationOptions = None , RecreateFromTraceBack = PopulationTraceBack)
                    # run the generation script
                    (ProcessList, PipeList) = Pop.RunPopulationGeneration(GenerationFileName = ScriptFileNameFullPath, NumberOfProcessesToRun = -1)
                else:
                    # otherwise don't run anything                    
                    (ProcessList, PipeList) = (None,None)
                return (ProcessList, PipeList)
            
            def GenerationEndMiniScript(ProcessList, PipeList):
                "Complete Generation by collecting results"
                prj = DB.Projects[self.idPrj]
                PopID = prj.PrimaryPopulationSetID
                Pop = DB.PopulationSets[PopID]
                if (ProcessList, PipeList) == (None,None):
                    # if nothing was run, then return no replacement population
                    RetVal = None
                else:
                    # If a process was run, return the replacement population
                    RetVal = Pop.CollectResults(ProcessList, PipeList)
                # Collect the results
                return RetVal

            def SimulationStartMiniScript():
                "Compile and execute the simulation"
                SimulationTraceBack = ExtractTraceBack()
                prj = DB.Projects[self.idPrj]
                # if an override population is defined, this means it was
                # generated from distributions and therefore repetitions should
                # be 1 as the number of repetitions defined the population size
                if self.TempOverridePopulationSet == None:
                    OverrideRepetitionCount = None
                else:
                    OverrideRepetitionCount = 1
                ScriptFileName = prj.CompileSimulation(OverrideRepetitionCount = OverrideRepetitionCount, OverridePopulationSet = self.TempOverridePopulationSet, RecreateFromTraceBack = SimulationTraceBack)
                # run the simulation once without collecting results
                (ProcessList, PipeList) = prj.RunSimulation(ScriptFileName, NumberOfProcessesToRun = -1)
                return (ProcessList, PipeList)

            def SimulationEndMiniScript(ProcessList, PipeList):
                "Complete Simulation by collecting results"
                prj = DB.Projects[self.idPrj]
                RetVal = prj.CollectResults(ProcessList, PipeList)
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
            # Figure out if cancel was pressed:
            WasCanceled = TheProgressDialog.WasCanceled
            if not WasCanceled:
                # set the override population to the result - None means no override
                self.TempOverridePopulationSet = Info
                # Now actually run the simulation
                ThreadObject = cdml.WorkerThread(SimulationStartMiniScript,SimulationEndMiniScript)
                # Tell the dialog box what to do when cancel is pressed
                TheProgressDialog.FunctionToRunUponCancel = ThreadObject.StopProcess
                # wait until thread/process exits
                Info = ThreadObject.WaitForJob()
                # Cancel through the dialog box is no longer possible
                TheProgressDialog.FunctionToRunUponCancel = None
                # Properly destroy the dialog 
                WasCanceled = TheProgressDialog.WasCanceled
            # Properly destroy the dialog 
            TheProgressDialog.Destroy()
            TheProgressDialog = None
                
            if WasCanceled:
                cdml.dlgSimpleMsg('INFO', 'The simulation was canceled by request!', wx.OK, wx.ICON_INFORMATION, Parent = self)
            elif Info.ProjectID == self.idPrj:
                cdml.dlgSimpleMsg('INFO', 'The simulation has finished successfully!', wx.OK, wx.ICON_INFORMATION, Parent = self)
            else:
                raise ValueError, 'ASSERTION ERROR: wrong project ID returned'
        except:
            cdml.dlgErrorMsg(Parent = self)
        # Release the override population if set
        self.TempOverridePopulationSet = None

        # Properly destroy the progress dialog box if not done before
        if TheProgressDialog != None:
            TheProgressDialog.Destroy()


    def ShowSimResult(self):
        """ Get user response to select simulation result file and open EXCEL to display CSV file"""
        RelevantSimulations = [ result.ID for result in DB.SimulationResults.values() if result.ProjectID == self.idPrj ]
        if RelevantSimulations != [] :
            cdml.OpenForm("ResultViewer", key=self.idPrj, parent=self, id_prj=self.idPrj)
        else:
            cdml.dlgSimpleMsg('INFO', 'No results exist for this project, run the simulation successfully to create results for this project', wx.OK, wx.ICON_INFORMATION, Parent = self)
        return
        

    def ClearPanel(self, panel):
        """ Clear all controls in a panel"""

        for ctrl in panel.GetChildren():
            type_ctrl = type(ctrl)
            if type_ctrl in [wx.TextCtrl, cdml.Text]:
                ctrl.SetValue('')
            elif type_ctrl == cdml.Combo:
                ctrl.GetTextCtrl().SetValue('')
            elif type_ctrl in [cdml.Checkbox, wx.CheckBox]:
                ctrl.SetValue(False)

    Exit = cdml.CloseForm


    def GetCurrTarget(self, type='obj', what='both'):
        """ Dummy method to return the Project ID """
        # ignore any input as this just imitates the cdml function
        id = self.idPrj
        if id == '':
            return None
        # Just create a dummy structure with enough information to allow
        # processing it by the general menu handler function
        DummyStructToReturn = cdml.Struct()
        DummyStructToReturn.Id = 1
        DummyStructToReturn.Key = id
        return DummyStructToReturn


# end of class MainFrame


if __name__ == "__main__":
    DB.LoadAllData('Testing.zip')
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MainFrame(cdml.ID_MODE_SINGL, 1150, None, 0 ,None )
    app.SetTopWindow(frame_1)
    frame_1.Center()
    frame_1.Show()
    app.MainLoop()
