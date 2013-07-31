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
# This file contains a form to define structure and value of a PopulationSet   #
################################################################################

import DataDef as DB
import CDMLib as cdml
import os
import wx, wx.grid
import copy


class MainFrame(wx.Frame):
    """ MainFrame class for PopulationData form"""

    def __init__(self, mode=None, data=None, type=None, id_prj=0, *args, **kwds):
        self.idPrj = id_prj

        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwdsnew)

        self.grid_1 = None
        
        self.pset_id = data # save the ID of parent RowPanel instance(i.e the ID of current PopulationSet)

        
        if self.pset_id == None: # If current PopulationSet is new one and wasn't saved
            title = 'Population Set : No Name'

        else: # Else display name of the PopulationSet
            CurrentName = DB.PopulationSets[self.pset_id].Name
            if mode != None and CurrentName != mode:
                CurrentName = mode +' {Edited from:' + CurrentName +'}'
            title = 'Population Set : ' + CurrentName

        # define lists for temporary Columns / Data list
        self.DataColumns = []
        self.Data = []
        self.HasDistribution = None

        self.idPrj = 0
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
        self.pup_menus = (  ["Undo", self.OnMenuSelected, wx.ID_UNDO ],
                            ["-" , None, -1],
                            ["Add Row" , self.OnMenuSelected, cdml.IDF_BUTTON1],
                            ["Delete Row" , self.OnMenuSelected, cdml.IDF_BUTTON2] )

        cdml.GenerateStandardMenu(self, SkipItems = [cdml.ID_MENU_REPORT_THIS, cdml.ID_MENU_REPORT_ALL])

        self.panel_1 = wx.Panel(self, -1)
        self.st_name = wx.StaticText(self.panel_1, -1, title)

        # Create Tab control for DataCulumns and Data
        self.nb = wx.Notebook(self.panel_1, -1, style=0)
        self.nb_pane_1 = wx.Panel(self.nb, 0)

        self.nb.AddPage(self.nb_pane_1, "Columns")


        self.lc_parm = cdml.List(self.nb_pane_1, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.lc_dist_text = cdml.Text(self.nb_pane_1, -1, "", style=wx.TE_NOHIDESEL)
        self.lc_dist = cdml.List(self.nb_pane_1, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)


        arrow_up = cdml.getSmallUpArrowBitmap() # arrow bitmap for buttons
        arrow_dn = cdml.getSmallDnArrowBitmap()

        self.btn_del = wx.BitmapButton(self.nb_pane_1, wx.ID_DELETE, arrow_dn)
        self.btn_add = wx.BitmapButton(self.nb_pane_1, wx.ID_ADD, arrow_up)
        self.lc_column = cdml.List(self.nb_pane_1, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)

        self.btn_import = wx.Button(self.panel_1, cdml.IDF_BUTTON2, "Import")
        self.btn_export = wx.Button(self.panel_1, cdml.IDF_BUTTON3, "Export")
        self.btn_undo = wx.Button(self.panel_1, cdml.IDF_BUTTON4, "Undo")
        self.btn_ok = wx.Button(self.panel_1, cdml.IDF_BUTTON5, "Ok")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CONTEXT_MENU, self.OnPopupMenu)    # Bind event handler for right mouse click. Open Popup menu
        self.Bind(wx.EVT_CLOSE, self.OnButtonClick)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, id=cdml.IDF_BUTTON2, id2=cdml.IDF_BUTTON6)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.btn_add)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.btn_del)
        # The next line fixes the bug of the parent window scrolling because
        # of a click in this window - focus is captured here and not
        # propagated to the parent window
        self.Bind(wx.EVT_CHILD_FOCUS, lambda Event: None)


        # closing the child parameter form triggers this
        self.Bind(wx.EVT_END_PROCESS, self.OnRefresh)

        self.lc_parm.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnLeftDblClick)
        self.lc_parm.Bind(wx.EVT_LIST_COL_CLICK, self.OnLeftDblClick)

        self.lc_dist.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnSelectDistribution)
        self.lc_dist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectDistribution)

        self.Initialize()


    def __set_properties(self):

        self.SetTitle("POPULATION DATA")
        self.HelpContext = 'PopulationData'

        self.SetSize((640, 400))
        self.MakeModal(True)

        self.st_name.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

        self.btn_add.SetSize(self.btn_add.GetBestSize())
        self.btn_del.SetSize(self.btn_del.GetBestSize())

        # build and assign the list of parameters
        self.lc_parm.SetMinSize((310,135))
        self.lc_parm.CreateColumns((('Parameter', 100), ('Notes', 205)))
        self.lc_parm.AllowBlank = False


        self.lc_dist_text.SetMinSize((310,-1))
        
        # build and assign the list of distribution
        self.lc_dist.SetMinSize((310,135))
        self.lc_dist.CreateColumns((('Expression', 100), ('Notes', 205)))

        # Set the column and column header of list control for DataColumn
        self.lc_column.SetMinSize((580,150))
        self.lc_column.CreateColumns((('Parameter', 250), ('Expression', 250)))
        self.lc_column.AllowBlank = False

        # Now actually assign the values
        self.SetListItems()


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_2.Add(self.st_name, 0, wx.EXPAND|wx.ALL, 10)

        gb_sizer = wx.GridBagSizer(0,0)

        gb_sizer.Add(self.lc_column, (0,0),(5,10), wx.EXPAND, 0)
        gb_sizer.Add(self.btn_add, (5,4), (1,1), wx.ALL|wx.ALIGN_CENTER, 3)
        gb_sizer.Add(self.btn_del, (5,5), (1,1), wx.ALL|wx.ALIGN_CENTER, 3)
        gb_sizer.Add(self.lc_parm, (6,0), (4,5), wx.EXPAND, 0)
        gb_sizer.Add(self.lc_dist_text, (6,5), (1,5), wx.EXPAND, 0)
        gb_sizer.Add(self.lc_dist, (7,5), (3,5), wx.EXPAND, 0)
        
        self.nb_pane_1.SetSizer(gb_sizer)

        if self.grid_1 != None:
            sizer_3 = wx.BoxSizer(wx.VERTICAL)
            sizer_3.Add(self.grid_1, 1, wx.EXPAND|wx.ALL, 0)
            if self.nb_pane_2 != None:
                self.nb_pane_2.SetSizer(sizer_3)
            else:
                raise ValueError, 'ASSERTION ERROR, Grid created without notebook pane - can not poperly layout the form'

        sizer_2.Add(self.nb, 0, wx.EXPAND, 0)

        sizer_4.Add(self.btn_export, 1, wx.ALL, 3)
        sizer_4.Add(self.btn_import, 1, wx.ALL, 3)
        sizer_4.Add(self.btn_undo, 1, wx.ALL, 3)
        sizer_4.Add(self.btn_ok, 1, wx.ALL, 3)
        sizer_2.Add(sizer_4, 0, wx.EXPAND, 0)

        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()


    def Initialize(self):
        """ Display initial data for DataColumn and/or Data if any"""
        # create temporary copy of DataColumns and Data
        parent = self.GetParent()
        if parent != None:
            self.DataColumns.extend(parent.DataColumns)
            self.Data.extend(parent.Data)
            if self.DataColumns == []:
                self.HasDistribution = None
                self.lc_dist.Enable(True)
                self.lc_dist_text.Enable(True)
            else:
                (parm,dist) = self.DataColumns[0]
                self.HasDistribution = (dist != '')
                self.lc_dist.Enable(self.HasDistribution)
                self.lc_dist_text.Enable(self.HasDistribution)

        # If data columns are not defined, simply display blank form
        if self.DataColumns == []:
            self.HasDistribution = None
            self.ShowTabData()
            return

        self.ShowData(self.DataColumns, self.Data)


    def SetListItems(self):
        """
        Build list for the controls
        """
        # build and assign the list of parameters
        parm = [ (str(p), p.Notes) for p in DB.Params.values() if p.ParameterType in ['Number','Integer', 'State Indicator']]
        self.lc_parm.SetItems(parm)
        # build and assign the list of distribution
        dist = [ (str(p), p.Notes) for p in DB.Params.values() if p.ParameterType == 'Expression']
        self.lc_dist.SetItems(dist)


    def OnRefresh(self, event):
        """ Refresh data after closing child form """
        self.SetListItems()

    def ShowTabData(self):
        """ Show/Hide 'Data' tab in the tab control """
        # Check the first distribution
        show = not self.HasDistribution
        if not show: # If distribution is defined
            # 'Data' tab doesn't exist, return
            if self.nb.GetPageCount() == 1 : return

            # If 'Data' tab exists, delete it
            self.nb.DeletePage(1)
            self.grid_1 = None
            self.nb_pane_2 = None

        else:
            # 'Data' tab exists, return
            if self.nb.GetPageCount() == 2 : return

            # Else create new panel and grid controls for 'Data' tab
            self.nb_pane_2 = wx.Panel(self.nb, 1)
            self.grid_1 = wx.grid.Grid(self.nb_pane_2, -1)
            self.grid_1.CreateGrid(1,1) # create minimum number of grid. grid size will be decided when the data is displayed
            self.grid_1.DeleteCols(0,1) # delete row and column to initialize the grid control

            # Add new panel to tab control
            self.nb.AddPage(self.nb_pane_2, "Data")

            w,h = self.grid_1.GetParent().GetSizeTuple()
            self.grid_1.SetSize((w-2, h-2))
        # Set up event handler
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnPopupMenu)    # Bind event handler for right mouse click. Open Popup menu
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnPopupMenu)    # Bind event handler for right mouse click. Open Popup menu
        self.__do_layout()




    def ShowData(self, Columns, Data):
        """ Display DataColums/Data in the List Controls and Grid control if necessary"""

        self.lc_column.SetItems(Columns, do_sort=False)     # Clear and add new Column names

        self.ShowTabData()                        # Create or delete 'Data' tab

        if Data == []:
            if self.HasDistribution:
                # if this is distribution based, make sure the grid is clear
                # do nothing 
                return
        # Display Data on the grid control
        no_col = len(Columns)
        no_row = len(Data)

        no_grid_col = self.grid_1.GetNumberCols()
        no_grid_row = self.grid_1.GetNumberRows()

        # Adjust grid size according to the size of Data
        if no_col > no_grid_col:
            self.grid_1.AppendCols(no_col - no_grid_col)

        elif no_col < no_grid_col :
            self.grid_1.DeleteCols(no_col, no_grid_col - no_col)

        if no_row > no_grid_row:
            self.grid_1.AppendRows(no_row - no_grid_row)

        elif no_row < no_grid_row :
            self.grid_1.DeleteRows(no_row, no_grid_row - no_row)

        self.grid_1.ClearGrid()             # Delete existing data in grid control

        # Set the column header of grid control
        for i, column in enumerate(Columns):
            self.grid_1.SetColLabelValue(i, column[0])

        # Write Data in each cell
        for i, row in enumerate(Data):
            for j, col in enumerate(row):
                value = cdml.iif(row[j] == None, '', str(row[j]))
                self.grid_1.SetCellValue(i,j, value)
        self.__do_layout()



    def Undo(self):
        """ Cancel current actions and display original data in the 'PopulationData' form"""
        # Clear temporary variable for DataColumns and Data
        self.DataColumns = []
        self.Data = []
        # copy DataColumns and Data from parent RowPanel instance
        parent = self.GetParent()
        if parent != None:
            self.DataColumns.extend(parent.DataColumns)
            self.Data.extend(parent.Data)
        # deduce if undoing causes distributions
        if self.DataColumns == []:
            self.HasDistribution = None
            self.lc_dist.Enable(True)
            self.lc_dist_text.Enable(True)
        else:
            (parm,dist) = self.DataColumns[0]
            self.HasDistribution = (dist != '')
            self.lc_dist.Enable(self.HasDistribution)
            self.lc_dist_text.Enable(self.HasDistribution)
        self.ShowData(self.DataColumns, self.Data) # Display data


    def OnLeftDblClick(self, event):
        """  Event handler to open parameters form"""
        cdml.OpenForm('Parameters', self, cdml.ID_MODE_SINGL, '', ['Number','Integer','State Indicator'], self.idPrj)


    def OnSelectDistribution(self, event):
        """  Event handler to copy the list value to the text box"""
        eventType = event.GetEventType()
        if eventType in [wx.EVT_LIST_ITEM_ACTIVATED.typeId, wx.EVT_LIST_ITEM_SELECTED.typeId]:
            index = self.lc_dist.GetFirstSelected()
            DistName = self.lc_dist.GetItem(index,0).GetText()
            self.lc_dist_text.SetValue(DistName)


    def AddColumn(self):
        """ Add Column name and distribution to list control"""

        idx = self.lc_parm.GetFirstSelected()
        if idx == -1:
            cdml.dlgSimpleMsg('ERROR', 'Please select a parameter', wx.OK, wx.ICON_ERROR, Parent = self)
            return
        parm = str(self.lc_parm.GetItem(idx,0).GetText())
        dist = str(self.lc_dist_text.GetValue())

        # Validate that this is a valid expression
        try:
            DB.Expr(dist)
        except:
            cdml.dlgErrorMsg(Parent = self)
            return

        no_page = self.nb.GetPageCount()
        no_column = self.lc_column.GetItemCount()
        if no_column == 0 : # if first item being added to column listbox
            self.HasDistribution = (dist != '')
            self.ShowTabData()
            self.lc_dist.Enable(self.HasDistribution)
            self.lc_dist_text.Enable(self.HasDistribution)

        else : # add more columns
            if no_page == 1 and dist == '':
                cdml.dlgSimpleMsg('ERROR', 'Please select a distribution', wx.OK, wx.ICON_ERROR, Parent = self)
                return

        # If this point was reached, then the distribution is ok
        # Add new column name (and distribution) to list control
        idx = self.lc_column.GetFirstSelected()
        if idx == -1 : idx = self.lc_column.GetItemCount()
        ItemToAdd = (parm,dist)
        # add to display
        self.lc_column.AddItem(ItemToAdd, idx, False)
        # update the data columns - this duality is needed for windows systems
        # that store only 512 characters in a listbox
        self.DataColumns.insert(idx, ItemToAdd)

        if self.nb.GetPageCount() == 1 : return

        if idx == self.lc_column.GetItemCount():    # Append New Column
            self.grid_1.AppendCols(1)

        else:                                       # insert new column
            self.grid_1.InsertCols(idx, 1, True)

        self.grid_1.SetColLabelValue(idx, parm)


    def DeleteColumn(self):
        """ Delete Column Name from list control"""

        idx = self.lc_column.GetFirstSelected()
        if idx == -1 :
            cdml.dlgSimpleMsg('ERROR', 'Please select an item to remove', Parent = self)
            return

        # generate a warning message only if data is about to be deleted
        if self.nb.GetPageCount() > 1:
            msg = 'This column may include data. The data will be deleted also. Do you want to continue?'
            ans = cdml.dlgSimpleMsg('WARNING', msg, wx.YES_NO, wx.ICON_WARNING, Parent = self)
            if ans == wx.ID_NO: return

        # Remove from list
        (parm,dist) = self.DataColumns.pop(idx)
        # remove from list control display
        self.lc_column.DeleteItem(idx)

        self.lc_column.Select(idx, True)

        oldidx = self.lc_parm.GetFirstSelected()
        self.lc_parm.Select(oldidx, False)

        idx2 = self.lc_parm.FindItem(-1, parm)

        if idx2 != wx.NOT_FOUND:
            self.lc_parm.Select(idx2,True)

        self.lc_dist_text.SetValue(dist)

        if self.nb.GetPageCount() > 1:
            self.grid_1.DeleteCols(idx,1, False)

            # refresh Column Labels
            for i in range(idx, self.lc_column.GetItemCount()):
                label = str(self.lc_column.GetItem(idx,0).GetText())
                self.grid_1.SetColLabelValue(i, label)

        if self.lc_column.GetItemCount() == 0:
            if self.nb.GetPageCount() > 1:
                self.grid_1.ClearGrid()
            self.HasDistribution = None
            self.ShowTabData()
            self.lc_dist.Enable(not self.HasDistribution)
            self.lc_dist_text.Enable(not self.HasDistribution)


     


    def SaveData(self):
        """ Gather current DataColumns/Data and then save it to list of parent panel"""
        no_column = self.lc_column.GetItemCount()

        DataColumns = self.DataColumns
        Data = []

        if self.nb.GetPageCount() > 1:
            if no_column != self.grid_1.GetNumberCols():
                raise ValueError, 'The number of columns is different from the columns in the data tab'

            for i in range(self.grid_1.GetNumberRows()):
                row = []
                for j in range(no_column):
                    value = self.grid_1.GetCellValue(i,j)
                    if value == '':
                        value = None
                    else:
                        value = float(value)

                    row.append(value)

                Data.append(row)

        self.Data = Data

        parent = self.GetParent()
        if parent != None:
            parent.DataColumns = DataColumns
            parent.Data = Data


    def ImportCSV(self):
        """ Import Population Data from a CSV file"""

        wildcard = "CSV File (*.csv)|*.csv| All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            try:
                (DataColumns, Data) = DB.ImportDataFromCSV(dialog.GetPath())
                # Make sure that DataColumns is composed of strings
                # alone and not numbers or other data types
                # this is a minimal precaution - no other validity checks
                # are made other than what made in ImportDataFromCSV
                AllStrings = all(map(lambda (ColumnName,Distribution): DB.IsStr(ColumnName), DataColumns))
                if not AllStrings:
                    raise ValueError, 'Error Loading CSV file - headers are not all strings'
            except:
                cdml.dlgErrorMsg(Parent = self)
            else:
                # set the HasDistribution flag to False since loading
                # a distribution is not currently supported.
                self.HasDistribution = False
                self.lc_dist.Enable(not self.HasDistribution)
                self.lc_dist_text.Enable(not self.HasDistribution)
                # also load this data to the object
                self.ShowTabData()
                self.DataColumns = DataColumns
                self.Data = Data
                self.ShowData(DataColumns, Data)

        self.Raise()
        dialog.Destroy() # Destroy file selection dialog


    def ExportCSV(self, DataColumns, Data ):
        """ Export Population Data from a CSV file"""

        wildcard = "CSV File (*.csv)|*.csv| All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a file name to save the data", os.getcwd(), "", wildcard, wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dialog.ShowModal() == wx.ID_OK:
            try:
                # convert the columns from tuples to strings
                ColumnHeadersToUse = map(lambda (ColumnName , Distribution) : ColumnName, DataColumns)
                DB.ExportDataToCSV(dialog.GetPath(), Data, ColumnHeadersToUse)
            except:
                cdml.dlgErrorMsg(Parent = self)

            else:
                # successfully saved the exported data
                cdml.dlgSimpleMsg('INFO', 'The data has been successfully saved to file', wx.OK, wx.ICON_INFORMATION, Parent = self)

        self.Raise()
        dialog.Destroy() # Destroy file selection dialog


    def OnButtonClick(self, event):
        """ Event handler for buttons """

        btn_id = event.GetId()

        try:
            if btn_id == cdml.IDF_BUTTON2:  # Import
                self.ImportCSV()

            if btn_id == cdml.IDF_BUTTON3:  # Export
                try:
                    self.SaveData()
                    self.ShowData(self.DataColumns, self.Data)
                except :
                    cdml.dlgErrorMsg(Parent = self)
                else:
                    if self.Data == []:
                        cdml.dlgSimpleMsg('INFO', 'No data has been defined so exporting makes no sense', wx.OK, wx.ICON_INFORMATION, Parent = self)
                    else:
                        self.ExportCSV(self.DataColumns, self.Data)

            elif btn_id == cdml.IDF_BUTTON4 :   # Undo
                self.Undo()

            elif btn_id == cdml.IDF_BUTTON5 or \
                event.GetEventType() == wx.wxEVT_CLOSE_WINDOW : # Ok or Close
                try:
                    self.SaveData()

                except :
                    cdml.dlgErrorMsg(Parent = self)

                else :
                    cdml.CloseForm(self, False)

            elif btn_id == wx.ID_ADD:           # Up Arrow : Add new State/Distribution
                self.AddColumn()

            elif btn_id == wx.ID_DELETE:        # Down Arrow : Delete State/Distribution
                self.DeleteColumn()

        except:
            cdml.dlgErrorMsg(Parent = self)


    def OnMenuSelected(self, event):
        """ Event handler for Popup menu"""

        # Use the default handler first and if no more processing needed return
        if cdml.OnMenuSelected(self, event):
            return

        menuId = event.GetId()
        if menuId == cdml.IDF_BUTTON1:  # ADD ROW
            self.grid_1.AppendRows(1)

        elif menuId == cdml.IDF_BUTTON2:    # Delete Row

            row = self.grid_1.GetGridCursorRow()
            if row == -1 : return

            self.grid_1.DeleteRows(row)

        elif menuId == wx.ID_UNDO:      # Undo
            self.Undo()



    def OnPopupMenu(self, event):
        """ Event handler to open Popup menu """

        if not hasattr(self, 'pup_menus'): return

        menu = cdml.setupMenu(self, self.pup_menus, False)  # crate popup menu and assign event handler

        page = self.nb.GetCurrentPage()
        menu_enable = cdml.iif( page.Id == 0, False, True )

        item_add = menu.FindItemById(cdml.IDF_BUTTON1)
        item_del = menu.FindItemById(cdml.IDF_BUTTON2)

        item_add.Enable(menu_enable)
        item_del.Enable(menu_enable)

        self.PopupMenu(menu)                            # open popup menu
        menu.Destroy()                                  # remove from memory to show just once when right button is clicked

# end of class MainFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()

    DB.LoadAllData('Testing.zip')
    frame_1 = MainFrame(mode=None, data=1090, type=None, id_prj=None, parent = None)

    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
