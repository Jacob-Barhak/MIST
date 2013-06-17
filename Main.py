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
# This file contains a Main form of the GUI for CDM Project                    #
################################################################################

import DataDef as DB
import CDMLib as cdml
import os
import wx
import wx.lib.mixins.listctrl as listmix
import sys
import copy


class Main(wx.Frame, listmix.ColumnSorterMixin):
    """ Main class for main form """

    def __init__(self, *args, **kwds):

        self._db_opened = False # state variables to check
        self._path = None          # path that database(zip file) exists
        self.curPrj = None      # variable to maintain opened project form

        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwdsnew)  # In Main form, wx.Frame class is used
                                                # because this form don't need to check the focus change

        self.HelpContext = 'Main'

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
        self.pup_menus = (  ["Delete Record" , self.OnMenuSelected, cdml.ID_MENU_DELETE_RECORD],
                            ["-" , None, -1],
                            ["Copy Record" , self.OnMenuSelected, cdml.ID_MENU_COPY_RECORD] )




        
        # Menu Bar
        self.menubar = wx.MenuBar()
        self.SetMenuBar(self.menubar)

        # File Menu
        self.MenuBarFile = wx.Menu()# Create 'File' menu

        # Add File menu items
        self.MenuItemNew = wx.MenuItem(self.MenuBarFile, wx.ID_NEW, "&New", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemNew)
        self.MenuItemOpen = wx.MenuItem(self.MenuBarFile, wx.ID_OPEN, "&Open", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemOpen)
        self.MenuItemSave = wx.MenuItem(self.MenuBarFile, wx.ID_SAVE, "&Save", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemSave)
        self.MenuItemSaveAs = wx.MenuItem(self.MenuBarFile, wx.ID_SAVEAS, "Save &As", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemSaveAs)
        self.MenuBarFile.AppendSeparator()
        self.MenuItemReportThis = wx.MenuItem(self.MenuBarFile, cdml.ID_MENU_REPORT_THIS, "Sing&le Report", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemReportThis)
        self.MenuItemReportAll = wx.MenuItem(self.MenuBarFile, cdml.ID_MENU_REPORT_ALL, "&Report All", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemReportAll)
        self.MenuBarFile.AppendSeparator()
        self.MenuItemExit = wx.MenuItem(self.MenuBarFile, wx.ID_EXIT, "E&xit", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemExit)
        self.menubar.Append(self.MenuBarFile, "&File")


        # Data Menu
        self.MenuBarForms = wx.Menu()

        # Add Data menu items
        self.MenuItemStates = wx.MenuItem(self.MenuBarForms, cdml.IDF_BUTTON1, "States", "", wx.ITEM_NORMAL)
        self.MenuBarForms.AppendItem(self.MenuItemStates)
        self.MenuItemStudy = wx.MenuItem(self.MenuBarForms, cdml.IDF_BUTTON4, "Model", "", wx.ITEM_NORMAL)
        self.MenuBarForms.AppendItem(self.MenuItemStudy)
        self.MenuItemTransition = wx.MenuItem(self.MenuBarForms, cdml.IDF_BUTTON3, "Transitions / Probabilities", "", wx.ITEM_NORMAL)
        self.MenuBarForms.AppendItem(self.MenuItemTransition)
        self.MenuItemPopulation = wx.MenuItem(self.MenuBarForms, cdml.IDF_BUTTON5, "Populations", "", wx.ITEM_NORMAL)
        self.MenuBarForms.AppendItem(self.MenuItemPopulation)
        self.MenuItemParameters = wx.MenuItem(self.MenuBarForms, cdml.IDF_BUTTON6, "Parameters", "", wx.ITEM_NORMAL)
        self.MenuBarForms.AppendItem(self.MenuItemParameters)
        self.menubar.Append(self.MenuBarForms, "F&orms")

        #  Menu
        self.MenuBarHelp = wx.Menu()

        # Add Help menu items
        self.MenuItemHelp = wx.MenuItem(self.MenuBarHelp, cdml.ID_MENU_HELP, "&Help", "", wx.ITEM_NORMAL)
        self.MenuBarHelp.AppendItem(self.MenuItemHelp)
        self.MenuItemHelpGeneral = wx.MenuItem(self.MenuBarHelp, cdml.ID_MENU_HELP_GENERAL, "&General Help", "", wx.ITEM_NORMAL)
        self.MenuBarHelp.AppendItem(self.MenuItemHelpGeneral)
        self.MenuBarFile.AppendSeparator()
        self.MenuItemAbout = wx.MenuItem(self.MenuBarHelp, cdml.ID_MENU_ABOUT, "&About", "", wx.ITEM_NORMAL)
        self.MenuBarHelp.AppendItem(self.MenuItemAbout)
        self.menubar.Append(self.MenuBarHelp, "&Help")
        # Menu Bar end

        self.st_title = wx.StaticText(self, -1, ' '*50+"MIcroSimulation Tool (MIST)")
        self.btn_state = cdml.Button(self, cdml.IDF_BUTTON1, "States")
        self.btn_study_model = cdml.Button(self, cdml.IDF_BUTTON4, "Models")
        self.btn_trans = cdml.Button(self, cdml.IDF_BUTTON3, "Transitions / Probabilities")
        self.btn_pset = cdml.Button(self, cdml.IDF_BUTTON5, "Populations")
        self.btn_params = cdml.Button(self, cdml.IDF_BUTTON6, "Parameters")


        self.lc_project = cdml.List(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)
        
        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        self.itemDataMap = {}
        self.IndexToPID = {}
        listmix.ColumnSorterMixin.__init__(self, 4)

        # assign event handlers
        #self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemNew)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemOpen)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemSave)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemSaveAs)
        self.Bind(wx.EVT_MENU,  self.OnExit, self.MenuItemExit)        
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemReportThis)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemReportAll)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemHelp)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemHelpGeneral)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemAbout)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, id = cdml.IDF_BUTTON1, id2=cdml.IDF_BUTTON6)
        self.Bind(wx.EVT_BUTTON,  self.OnMenuSelected, id = cdml.IDF_BUTTON1, id2=cdml.IDF_BUTTON6)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnPopupMenu) # Dedicated event handler for popup menu
        self.lc_project.Bind(wx.EVT_KEY_DOWN, self.OnKeyUp )
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListDClick, self.lc_project)

        # Bind special event to refresh project refresh
        # This event handler is called by Project form
        self.Bind(wx.EVT_END_PROCESS, self.RefreshEvent)

        self.__set_properties()
        self.__do_layout()


    # Used by the ColumnSorterMixin
    def GetListCtrl(self):
        return self.lc_project


    def __set_properties(self):
        """ Set the properties of frame and controls """

        self.SetTitle("MIST : MIcroSimulation Tool")
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))

        self.st_title.SetFont(wx.Font(16, wx.DEFAULT, wx.SLANT, wx.BOLD, 0, ""))

        self.lc_project.AllowBlank = False  # set this property, if you don't want to add a blank line at the top of a list control
        self.lc_project.SetMinSize(wx.DLG_SZE(self.lc_project, (320,200)))

        # Create columns and assign column titles
        # Symtax : tuple of tuples ((Column Name, width), (Column Name, width). ... )
        self.lc_project.CreateColumns((('#', 0 ),
                                       ('Project Name', 250 ),
                                        ('Notes', 350 )))

        self.btn_state.SetMinSize((200,-1))

        # Assign form names as UserData of each button
        # Module name is same as form name in current version
        self.btn_state.userData = 'States'
        self.btn_trans.userData = 'Transitions'
        self.btn_study_model.userData = 'StudyModels'
        self.btn_pset.userData = 'PopulationSets'
        self.btn_params.userData = 'Parameters'


    def __do_layout(self):
        """ Set the position of controls """

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)

        sizer_1.Add(self.st_title, 0, wx.ALL, 10)
        sizer_3.Add(self.btn_state, 1, wx.ALL|wx.EXPAND, 3)
        sizer_3.Add(self.btn_study_model, 1, wx.ALL|wx.EXPAND, 3)
        sizer_3.Add(self.btn_trans, 1, wx.ALL|wx.EXPAND, 3)
        sizer_3.Add(self.btn_pset, 1, wx.ALL|wx.EXPAND, 3)
        sizer_3.Add(self.btn_params, 1, wx.ALL|wx.EXPAND, 3)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)

        sizer_2.Add(self.lc_project, 0, wx.ALL|wx.EXPAND, 5)

        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()


    def GetNameDB(self, style_part):
        """ Open file selection window and get a database name"""

        path = None
        wildcard =  "ZIP file (*.zip)|*.zip|All files (*.*)|*.*"
        dlg = wx.FileDialog(
                self, message="Choose a file",
                defaultDir=os.getcwd(),
                defaultFile="",
                wildcard=wildcard,
                style=style_part | wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

        return path


    def SaveDB(self, menuId=wx.ID_SAVE):
        """ Save current database. If current database is new one, remove asterisk(*) from title"""

        if not self._db_opened : return

        if menuId == wx.ID_SAVEAS or (self._path == (os.getcwd() + os.sep + 'new_file.zip')):
            path = self.GetNameDB(wx.SAVE)
            if path == None: return False
            self._path = path # replace previous path with current path

        try:
            DB.SaveAllData(FileName = self._path, Overwrite = True, CompressFile = True, CreateBackupBeforeSave = True)
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            cdml.dlgErrorMsg(Parent = self)

        self.SetTitle('MIST - ' + self._path)
        return True


    def OpenDB(self, menuId):
        if DB.AccessDirtyStatus():
            ans = cdml.dlgSimpleMsg('WARNING', "The data is not saved in a file. Do you want to save it?", wx.YES_NO|wx.CANCEL, wx.ICON_WARNING, Parent = self)
            if ans == wx.ID_YES :
                if not self.SaveDB(wx.ID_SAVE): return
            if ans == wx.ID_CANCEL:
                return

        if menuId == wx.ID_NEW:                     # if New menu selected,
            path = os.getcwd() + os.sep + 'new_file.zip'        #   set dummy path
        else:
            path = self.GetNameDB(wx.OPEN)          # else get database name

            if path == None : return

            if not os.path.isfile(path):
                cdml.dlgSimpleMsg('ERROR', 'The file does not exist, please make sure the path is valid', Parent = self)
                return
            
        wx.BeginBusyCursor()
        reload(DB)
        try:
            if os.path.isfile(path):
                # test the version of the file:
                (FileVersion, IsCompatible, IsUpgradable, DidLoad, HasResults) = DB.ReconstructDataFileAndCheckCompatibility(InputFileName = path, JustCheckCompatibility = True, RegenerationScriptName = None, ConvertResults = False, KnownNumberOfErrors = 0, CatchError = True)
                if IsCompatible:
                    # If versions are compatible, just load the file
                    DB.LoadAllData(path)   # If Open menu, load data
                elif IsUpgradable:
                    if HasResults:
                        wx.EndBusyCursor()
                        AnswerForConvertResults = cdml.dlgSimpleMsg('Data Conversion', 'This file was generated with an older version of data definitions.: ' + str(FileVersion) +  '. It was converted to the new version ' + str (DB.Version) + ' . Converting simulation results may take a long time and such results may not be reproducible with the current version. Even if simulation results are not loaded, the parameters, states, models, Population sets and projects will be loaded.\nDo you wish to convert simulation results from this file? ', wx.YES_NO, wx.ICON_QUESTION, Parent = self)
                        AnswerForConvertResultsBoolean = AnswerForConvertResults == wx.ID_YES
                        wx.BeginBusyCursor()
                    else:
                        AnswerForConvertResultsBoolean = False
                        print '*** Converting file to the new version. Please wait - this may take a while ***'
                    # if a version upgrade is needed, convert the data
                    (FileVersion, IsCompatible, IsUpgradable, DidLoad, HasResults) = DB.ReconstructDataFileAndCheckCompatibility(InputFileName = path, JustCheckCompatibility = False, RegenerationScriptName = None, ConvertResults = AnswerForConvertResultsBoolean, KnownNumberOfErrors = 0, CatchError = True)
                
            self.ShowProjectList(None)
            self.SetTitle("MIST - " + path)
            self._db_opened = True
            self._path = path

        except:
            cdml.dlgErrorMsg(Parent = self)
        wx.EndBusyCursor()



    def RefreshEvent(self, event):
        """ Function to handle a return from a child form """
        # Just clear the stack from the last return
        cdml.GetRefreshInfo()
        # Update the project list
        self.ShowProjectList(event)
        

    def ShowProjectList(self, event=None):
        """ Display project list on the list control """
        ProjectIDs = sorted(DB.Projects.keys())
        ProjectRecords = map (lambda Entry: DB.Projects[Entry], ProjectIDs)
        ProjectColumnData = [ (Num+1, prj.Name, prj.Notes, Num+1 )
                            for (Num,prj) in enumerate(ProjectRecords) ]
        # sort projects by ID, in the future this may change to allow users
        # to change the column sorting
        ProjectColumnData.insert(0, ('', ' Add New Project', '', 0))
        ProjectIDs.insert(0, 0)
        self.itemDataMap = dict(enumerate(ProjectColumnData))
        self.IndexToPID = dict(enumerate(ProjectIDs))
        self.lc_project.SetItems(ProjectColumnData, False)


    def OpenProject(self, id_prj):
        """ Open a project or Create new project """
        self.curPrj = cdml.OpenForm( 'Project', self, cdml.ID_MODE_SINGL, id_prj)



    def DeleteProjectRecord(self):
        """ Delete the Project record pointed on in the list"""
        index = self.lc_project.GetFirstSelected()
        if index in [ -1, 0 ]: # -1 : nothing selected, 0 : or selected 'New Project'
            return

        msg = 'Selected project will be deleted permanently.\n'
        msg += 'Are you sure you want to delete the selected project?'
        ans = cdml.dlgSimpleMsg('WARNING', msg, wx.YES_NO, wx.ICON_WARNING, Parent = self)

        if ans == wx.ID_NO: return

        ProjectIndex = self.lc_project.GetItemData(index)

        pid = self.IndexToPID[ProjectIndex]

        if pid not in DB.Projects.keys(): return

        try:
            DB.Projects.Delete(pid)                     # delete database object
            self.ShowProjectList()
            # set the focus on the next record after the deleted one
            self.lc_project.Select(index)
        except:
            cdml.dlgErrorMsg(Parent = self)


    def CopyProjectRecord(self):
        """ Delete the Project record pointed on in the list"""
        index = self.lc_project.GetFirstSelected()
        if index in [ -1, 0 ]: # -1 : nothing selected, 0 : or selected 'New Project'
            return

        ProjectIndex = self.lc_project.GetItemData(index)

        pid = self.IndexToPID[ProjectIndex]

        if pid not in DB.Projects.keys(): return

        try:
            DB.Projects.Copy(pid)
            self.ShowProjectList()
        except:
            cdml.dlgErrorMsg(Parent = self)



    def OnPopupMenu(self, event):
        """ Open Popup menu """

        if not hasattr(self, 'pup_menus'): return

        menu = cdml.setupMenu(self, self.pup_menus, False)  # crate popup menu and assign event handler

        self.PopupMenu(menu)    # open popup menu
        menu.Destroy()          # remove from memory to show just once when right button is clicked


    def OnMenuSelected(self, event):
        """ Event handler for buttons and menu items in main form"""

        menuId = event.GetId()
        if menuId in [ wx.ID_NEW, wx.ID_OPEN ]:     # New and Open menu
            self.OpenDB(menuId)                     # open dialog to select database file


        elif menuId == cdml.ID_MENU_COPY_RECORD:
            self.CopyProjectRecord()        

        elif menuId == cdml.ID_MENU_DELETE_RECORD:
            self.DeleteProjectRecord()        

        elif menuId in [ wx.ID_SAVE, wx.ID_SAVEAS ]: # save or save as menu
            self.SaveDB(menuId)

        elif menuId in range(cdml.IDF_BUTTON1, cdml.IDF_BUTTON10): # Items in Data Menu and buttons
            # check database was loaded
            if not self._db_opened:
                cdml.dlgSimpleMsg('WARNING', "No data is loaded to the system. Please select 'New' or 'Open' in File menu", wx.OK, wx.ICON_WARNING, Parent = self)
                return

            btn = self.FindWindowById(menuId)   # synchronize selected menu to a button
            if btn.userData == None : return  # target for should be assigned to each button
                                                # as user data to avoid import statement.
                                                # See __set_properties method


            if btn.userData == 'Transitions' and len(DB.StudyModels) == 0:
                cdml.dlgSimpleMsg('ERROR', 'A Model should be defined', Parent = self)
                return

            cdml.OpenForm(btn.userData, self)   # open a form as default mode(=None)

        elif menuId in [cdml.ID_MENU_ABOUT, cdml.ID_MENU_HELP, cdml.ID_MENU_HELP_GENERAL]:
            cdml.OnMenuSelected(self, event)

        elif menuId == cdml.ID_MENU_REPORT_THIS: # Create a report for a specific project
            index = self.lc_project.GetFirstSelected()
            if index in [ -1, 0 ]: # -1 : nothing selected, 0 'New Project' selected
                return
            ProjectCode = self.IndexToPID[index]
            if ProjectCode in DB.Projects.keys():
                cdml.OpenForm("ReportViewer",self, key=(DB.Projects[ProjectCode],None) )

        elif menuId == cdml.ID_MENU_REPORT_ALL: # Create a report for all projects
            CollectionObject = DB.Projects
            if CollectionObject != None:
                cdml.OpenForm("ReportViewer",self,key=(CollectionObject,None) )


    def OnExit(self, event):
        """ Event handler for Exit menu or CLOSE_WINDOW event"""

        if DB.AccessDirtyStatus(): # If there is unsaved data
            ans = cdml.dlgSimpleMsg('WARNING', "The data was not saved to a file. Do you want to save it?", wx.YES_NO|wx.CANCEL, wx.ICON_WARNING, Parent = self)
            if ans == wx.ID_YES:
                if not self.SaveDB(wx.ID_CLOSE) : return

            elif ans == wx.ID_CANCEL: return

        self.MakeModal(False)
        self.Destroy()


    def OnListDClick(self, event):
        """ Open project form when user double click the project list"""
        IdToOpen = event.GetData()
        ProjectCode = self.IndexToPID[IdToOpen]
        self.OpenProject(ProjectCode)



    def OnKeyUp(self, event):
        """ Event handler to track key input on project list"""

        key_code = event.GetKeyCode()
        if key_code in [ wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE ]: # DEL --> Delete Project
            self.DeleteProjectRecord()
        elif key_code == wx.WXK_EXECUTE: # Enter -> Open a project form. same as double click
            IdToOpen = event.GetData()
            ProjectCode = self.IndexToPID[IdToOpen]
            self.OpenProject(ProjectCode)
        elif key_code == wx.WXK_UP: # Up button 
            index = self.lc_project.GetFirstSelected()
            self.lc_project.Select(index-1)
        elif key_code == wx.WXK_DOWN: # Down button 
            index = self.lc_project.GetFirstSelected()
            self.lc_project.Select(index+1)


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()

   
    if len(sys.argv)>1 and str(sys.argv[1]).lower() in ['admin', 'administrator']:
        print "Running Application in Admin Mode"
        cdml.SetAdminMode(True)
    else:
        cdml.SetAdminMode(False)

    w, h = wx.GetDisplaySize()
    if w<1024 or h<768:
        msg = 'Minimum resolution for this program is 1024x768.\n'
        msg += 'Some forms may not be displayed properly. Do you want to continue?'
        ans = cdml.dlgSimpleMsg('WARNING', msg, wx.YES_NO, wx.ICON_WARNING)
        if ans == wx.ID_NO : wx.Exit()

    frame_1 = Main(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.MakeModal(True)
    frame_1.CenterOnScreen()
    frame_1.Show()
    app.MainLoop()
