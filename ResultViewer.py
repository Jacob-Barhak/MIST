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
# This file contains a form to define the project result viewer                #
################################################################################


import DataDef as DB
import CDMLib as cdml
import datetime
import wx
import wx.grid
import os
import copy

class MainFrame(cdml.CDMWindow, wx.Frame):
    """ Form class to display the simulation result"""

    def __init__(self, mode=None, data=None, type=None, id_prj=0, *args, **kwds):
        """ MainFrame class for PopulationSets """

        self.idPrj = id_prj     # Backup ID of current project

        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwdsnew)


        # Find SimulationResult objects for current project
        sim_ids = [ str(sim.ID) for sim in DB.SimulationResults.values()
                        if sim.ProjectID == self.idPrj ]
        sim_ids.reverse() # Reverse the order. So, latest simulation result is shown on top of the combo box
        name = 'Results for Project : ' + DB.Projects[self.idPrj].Name

        # Default path is the report
        t = datetime.datetime.now().isoformat()
        time_stamp = t.replace(':', '').replace('.', '').replace('T', '').replace('-','')
        self.Path = os.path.join(os.getcwd(),'ResultExport'+'_' + time_stamp + '.csv')

        self.panel = wx.Panel(self, -1)
        self.st_id_sim = wx.StaticText(self.panel, -1, "Simulation ID : ")
        self.btn_export = wx.Button(self.panel, cdml.IDF_BUTTON1, 'Export To File')
        self.cc_id_sim = wx.ComboBox(self.panel, -1, choices=sim_ids, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.btn_del = wx.Button(self.panel, wx.ID_DELETE)
        self.btn_del_all = wx.Button(self.panel, wx.ID_CLEAR, 'Delete All')
        self.st_prj = wx.StaticText(self.panel, -1, name)
        self.grid = wx.grid.Grid(self.panel, -1, size=(1, 1))

        # Set the collection name        
        self.Collection = 'SimulationResults'
        self.HelpContext = 'SimulationResults'

        cdml.GenerateStandardMenu(self, SkipItems = [cdml.ID_MENU_REPORT_ALL])

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CONTEXT_MENU, self.OnPopupMenu) # Disable popup
        self.Bind(wx.EVT_CLOSE, self.FrameEventHandler) # Bind event handler for close window event

        self.cc_id_sim.Bind(wx.EVT_COMBOBOX, self.ShowSimResult)
        self.btn_del.Bind(wx.EVT_BUTTON, self.DelSimResult)
        self.btn_export.Bind(wx.EVT_BUTTON, self.ExportSimResult)
        self.btn_del_all.Bind(wx.EVT_BUTTON, self.DelSimResult)
        self.grid.CreateGrid(10,10) # create grid

        self.cc_id_sim.SetSelection(0)
        self.ShowSimResult()


    def __set_properties(self):
        self.SetTitle("SIMULATION RESULT")
        self.SetMinSize((800, 600))


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_3.Add(self.st_prj, 0, wx.ALL, 3)
        sizer_3.Add((100,0), 0, wx.ALL, 3)      # space b/w project name and simulation ID combo box
        sizer_3.Add(self.st_id_sim, 0, wx.ALL, 3)
        sizer_3.Add(self.cc_id_sim, 0, wx.ALL, 3)
        sizer_3.Add(self.btn_export, 0, wx.ALL, 3)
        sizer_3.Add(self.btn_del, 0, wx.ALL, 3)
        sizer_3.Add(self.btn_del_all, 0, wx.ALL, 3)
        sizer_2.Add(sizer_3, 0, wx.ALL, 1)

        sizer_2.Add(self.grid, 1, wx.ALL|wx.EXPAND, 1)
        self.panel.SetSizer(sizer_2)

        sizer_1.Add(self.panel, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def OnPopupMenu(self, event):
        """ Open Popup menu """
        # Do nothing in this form
        return
    
    def ShowSimResult(self, event=None):
        """
        Display simulation results in the grid control
        """

        id = self.cc_id_sim.GetValue()  # Retrieve simulation ID from combo box
        if id == '': return
        id = int(id)

        # Find simulation results object related to current project
        cur_result = None
        for result in DB.SimulationResults.values():
            if result.ID == id and result.ProjectID == self.idPrj :
                cur_result = result
                break

        no_col = len(cur_result.DataColumns)
        no_row = len(cur_result.Data)

        no_grid_col = self.grid.GetNumberCols()
        no_grid_row = self.grid.GetNumberRows()

        # If there are too many records, allow the user to decide how many
        # to load to the system to reduce the load. It is impractical to show
        # very large simulation results.
        if no_col * no_row > 50000:
            dlg = wx.NumberEntryDialog(self, 'Define number or records to show', 'The result grid is very large (' + str(no_row) + ' rows x ' + str(no_col) + ' columns) \nand it is probably not practical to show it on the screen. \nPlease decide how many rows you wish to view. \nNote that you can later export the results to view them in full in another application. \nPressing Cancel will show all rows and in some cases may overwhelm the system.', 'Rows to show', 1000, 0, 100000)
            dlg.CenterOnScreen()
            if dlg.ShowModal() == wx.ID_OK:
                no_row = min(dlg.GetValue(),no_row)             

        # adjust the number of rows and columns of the grid congtrol
        if no_col > no_grid_col:
            self.grid.AppendCols(no_col - no_grid_col)

        elif no_col < no_grid_col :
            self.grid.DeleteCols(no_col, no_grid_col - no_col)

        if no_row > no_grid_row:
            self.grid.AppendRows(no_row - no_grid_row)

        elif no_row < no_grid_row :
            self.grid.DeleteRows(no_row, no_grid_row - no_row)

        self.grid.ClearGrid()           # Clear current values in grid control


        dlg = wx.GenericProgressDialog("Load Data",
                                "Loading Data. Please wait......",
                                maximum = no_col + no_row,
                                parent=self,
                                style = wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME )
        dlg.CenterOnScreen()

        for i, column in enumerate(cur_result.DataColumns): # write column header on grid control
            self.grid.SetColLabelValue(i, column)
            dlg.Update(i)                                       # update length of gauge in progress dialog

        for i, row in enumerate(cur_result.Data[0:no_row]):   # write data in each cell in the range
            for j, col in enumerate(row):
                value = cdml.iif(row[j] == None, '', str(row[j]))
                self.grid.SetCellValue(i,j, value)

            dlg.Update(i+no_col)

        dlg.Destroy()


    def ExportSimResult(self, event):
        evt_id = event.GetId()

        if evt_id == cdml.IDF_BUTTON1:
        
            id_sim = self.cc_id_sim.GetValue()  # Retrieve simulation ID from combo box
            if id_sim == '': return
            id_sim = int(id_sim)
            target_id = [ result.ID for result in DB.SimulationResults.values()
                            if result.ID == id_sim and result.ProjectID == self.idPrj ]
            if len(target_id) != 1:
                return None

            NewPath = self.GetExportFileName()
            if NewPath == None: 
                return 
            else:
                self.Path = NewPath # replace previous path with current path
            try:
                DB.SimulationResults[id_sim].ExportAsCSV(self.Path)
            except:
                msg = 'Could not complete saving into the selected file, check if the file is not in use or otherwise locked'
                cdml.dlgSimpleMsg('ERROR', msg, wx.OK, wx.ICON_ERROR, Parent = self)
                return False
        return True


    def GetExportFileName(self):
        """ Open file selection window and get a file name"""
        NewPath = None
        wildcard =  "Text file (*.csv)|*.csv|All files (*.*)|*.*"
        [Head,Tail]=os.path.split(self.Path)
        dlg = wx.FileDialog(
                self, message="Choose a filename to save the export file",
                defaultDir=Head,
                defaultFile=Tail,
                wildcard=wildcard,
                style= wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            NewPath = str(dlg.GetPath())
        return NewPath

            

    def DelSimResult(self, event):
        id = event.GetId()

        try:
            if id == wx.ID_DELETE:
                id = self.cc_id_sim.GetValue()  # Retrieve simulation ID from combo box
                if id == '':
                    cdml.dlgSimpleMsg('ERROR', 'No Result ID was selected', Parent = self)
                    return

                if self.cc_id_sim.GetCount() == 1:
                    msg = 'This is the last simulation result. '
                    msg += 'After deleting this result, the form will be closed automatically.'
                    msg += '\nDo you want to continue?'
                    ans = cdml.dlgSimpleMsg('WARNING', msg, wx.YES_NO, wx.ICON_WARNING, Parent = self)
                    if ans == wx.ID_NO: return

                id_sim = int(id)
                target_id = [ result.ID for result in DB.SimulationResults.values()
                                if result.ID == id_sim and result.ProjectID == self.idPrj ]

                if target_id == []: return

                DB.SimulationResults.Delete(target_id[0], ProjectBypassID = self.idPrj)

                self.cc_id_sim.Delete(self.cc_id_sim.GetSelection())
                self.grid.ClearGrid()

                if self.cc_id_sim.GetCount() == 0:
                    self.cc_id_sim.Clear()
                    self.cc_id_sim.SetValue('')
                else:
                    self.cc_id_sim.SetSelection(0)
                self.ShowSimResult()

            else:

                for result in DB.SimulationResults.values():
                    if result.ProjectID != self.idPrj : continue
                    DB.SimulationResults.Delete(result.ID, ProjectBypassID = self.idPrj)

                self.cc_id_sim.Clear()
                self.cc_id_sim.SetValue('')
                self.grid.ClearGrid()           # Clear current values in grid control

        except:
            cdml.dlgErrorMsg()

    def GetCurrTarget(self, type='obj', what='both'):
        """ Dummy method to return the selected ID """
        # ignore any input as this just imitates the cdml function
        id = self.cc_id_sim.GetValue()  # Retrieve simulation ID from combo box
        if id == '':
            return None
        id_sim = int(id)
        target_id = [ result.ID for result in DB.SimulationResults.values()
                        if result.ID == id_sim and result.ProjectID == self.idPrj ]
        if len(target_id) != 1:
            return None
        # Just create a dummy structure with enough information to allow
        # processing it by the general menu handler function
        DummyStructToReturn = cdml.Struct()
        DummyStructToReturn.Id = 1
        DummyStructToReturn.Key = target_id[0]
        return DummyStructToReturn

    def FrameEventHandler(self, evt):
        """ Frame Event Handler """

        evtType = evt.GetEventType()
        # if current event is close window, call CloseForm function
        if evtType == wx.wxEVT_CLOSE_WINDOW:
            cdml.CloseForm(self)
            return

    # Define the default method to handle the menu selections
    OnMenuSelected = cdml.OnMenuSelected



if __name__ == "__main__":
    DB.LoadAllData('InData' + DB.os.sep + 'Testing.zip')
    ProjectKeyToShow = min(DB.Projects.keys())
    SimulationScriptFullPath = DB.Projects[ProjectKeyToShow].CompileSimulation()
    ResultInfo = DB.Projects[ProjectKeyToShow].RunSimulationAndCollectResults(SimulationScriptFullPath)
    app = wx.App(0)
    #wx.InitAllImageHandlers() Deprecated
    frame_1 = MainFrame(id_prj=ProjectKeyToShow, parent=None)
    app.SetTopWindow(frame_1)
    frame_1.Center()
    frame_1.Show()
    app.MainLoop()

