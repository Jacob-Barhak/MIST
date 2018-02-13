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
# Initially developed by Deanna Isaman, Jacob Barhak
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
# This file contains a form to view reports                                    #
################################################################################


import DataDef as DB
import CDMLib as cdml
import wx, copy
import wx.stc as stc
import os
import datetime
import sys

class MainFrame(cdml.CDMWindow, wx.Frame):
    
    def __init__(self, mode=None, data=None, type=None, id_prj=0, *args, **kwds):
        """ Constructor of the MainFrame class """
        self.idPrj = id_prj
        # Note that key stands for the text to display rather than a record key
        # The name has not been changed to conform with the existing terminology
        # of the system.
        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwdsnew)
        # Default path is the report
        t = datetime.datetime.now().isoformat()
        time_stamp = t.replace(':', '').replace('.', '').replace('T', '').replace('-','')
        self.Path = os.path.join(os.getcwd(),'Report'+'_' + time_stamp + '.txt')

        self.ReportObject, self.FormatOptions = data
        

        # Create the tabs
        self.NoteBook = wx.Notebook(self, -1, style=0)
        self.ReportPane = wx.Panel(self.NoteBook, 0)
        self.OptionsPane = wx.Panel(self.NoteBook, 1)
        
        self.tc_ReportDisplay = stc.StyledTextCtrl(self.ReportPane, wx.ID_ANY )
        self.tc_ReportDisplay.StyleSetFaceName(stc.STC_STYLE_DEFAULT,'Courier')
        self.tc_ReportDisplay.StyleClearAll()
        self.DisplayText()
        # Now add the filter controls:
        self.st_DetailLevel = wx.StaticText(self.OptionsPane, -1, 'Detail Level:')
        self.cc_DetailLevel = cdml.Combo(self.OptionsPane, cdml.IDF_BUTTON1)
        self.st_ShowDependency = wx.StaticText(self.OptionsPane, -1, 'Show Dependency:')
        self.cc_ShowDependency = cdml.Combo(self.OptionsPane, cdml.IDF_BUTTON2, validator=cdml.KeyValidator(cdml.NO_EDIT))
        self.st_SummaryIntevals = wx.StaticText(self.OptionsPane, -1, 'Summary Intervals:')
        self.tc_SummaryIntevals = cdml.Text(self.OptionsPane, -1, "")
        self.st_ColumnNumberFormatFloat = wx.StaticText(self.OptionsPane, -1, 'Float Column Number Format:')
        self.tc_ColumnNumberFormatFloat = cdml.Text(self.OptionsPane, -1, "")
        self.st_ColumnNumberFormatInteger = wx.StaticText(self.OptionsPane, -1, 'Integer Column Number Format:')
        self.tc_ColumnNumberFormatInteger = cdml.Text(self.OptionsPane, -1, "")
        self.st_ColumnSeparator = wx.StaticText(self.OptionsPane, -1, 'Column Separator:')
        self.tc_ColumnSeparator = cdml.Text(self.OptionsPane, -1, "")
        self.st_ShowHidden = wx.StaticText(self.OptionsPane, -1, 'Show Hidden:')
        self.cc_ShowHidden = cdml.Combo(self.OptionsPane, cdml.IDF_BUTTON2, validator=cdml.KeyValidator(cdml.NO_EDIT))

        # allow showing Hidden parameters only in Admin mode
        IsVisible = cdml.GetAdminMode()
        self.st_ShowHidden.Show(IsVisible)
        self.cc_ShowHidden.Show(IsVisible)

        self.st_CandidateColumns = wx.StaticText(self.OptionsPane, -1, 'Candidate Columns:')
        self.lc_CandidateColumns = cdml.List(self.OptionsPane, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)
        self.st_ColumnTitle = wx.StaticText(self.OptionsPane, -1, 'Column Title:')
        self.tc_ColumnTitle = cdml.Text(self.OptionsPane, -1, "")
        self.st_CalculationMethod = wx.StaticText(self.OptionsPane, -1, 'Calculation Method:')
        self.cc_CalculationMethod = cdml.Combo(self.OptionsPane, cdml.IDF_BUTTON3, validator=cdml.KeyValidator(cdml.NO_EDIT))

        self.st_StratificationTable = wx.StaticText(self.OptionsPane, -1, 'Stratification Table:')
        self.tc_StratificationTable = cdml.Text(self.OptionsPane, -1, "", style = wx.TE_MULTILINE)

        self.btn_LoadReportOptions = wx.Button(self.OptionsPane, cdml.IDP_BUTTON1, "Load Report Options")
        self.btn_SaveReportOptions = wx.Button(self.OptionsPane, cdml.IDP_BUTTON2, "Save Report Options")

        self.btn_Add = wx.Button(self.OptionsPane, wx.ID_ADD, ">")
        self.btn_Del = wx.Button(self.OptionsPane, wx.ID_DELETE, "X")
        self.st_SelectedColumns = wx.StaticText(self.OptionsPane, -1, 'Selected Columns:')
        self.lc_SelectedColumns = cdml.List(self.OptionsPane, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)
        self.btn_Regenerate = wx.Button(self.OptionsPane, wx.ID_APPLY, "Regenerate Report")
        
        # Add Standard menu while skipping a few options
        cdml.GenerateStandardMenu(self, SkipItems = [cdml.ID_MENU_REPORT_THIS, cdml.ID_MENU_REPORT_ALL])
        # Add a SaveAs option to the menu
        self.MenuItemSave = wx.MenuItem(self.MenuBarFile, wx.ID_SAVE, "&Save", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemSave)
        self.MenuItemSaveAs = wx.MenuItem(self.MenuBarFile, wx.ID_SAVEAS, "Save &As", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemSaveAs)
        # 
        self.Bind(wx.EVT_MENU, self.OnMenuSelected, self.MenuItemSave)
        self.Bind(wx.EVT_MENU, self.OnMenuSelected, self.MenuItemSaveAs)
        self.Bind(wx.EVT_BUTTON, self.FrameEventHandler)
        self.Bind(wx.EVT_CLOSE, self.FrameEventHandler) 

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        
        self.HelpContext = 'ReportViewer'

        self.SetTitle("Report Viewer")
        self.SetSize((900, 700))
        self.MyMakeModal(True)

        self.st_DetailLevel.SetMinSize((-1, -1))
        self.st_ShowDependency.SetMinSize((-1, -1))
        self.st_ColumnNumberFormatFloat.SetMinSize((-1, -1))
        self.st_ColumnNumberFormatInteger.SetMinSize((-1, -1))
        self.st_CandidateColumns.SetMinSize((-1, -1))
        self.st_SelectedColumns.SetMinSize((-1, -1))
        self.st_ColumnSeparator.SetMinSize((-1, -1))
        self.st_ShowHidden.SetMinSize((-1, -1))
        self.st_ColumnTitle.SetMinSize((-1, -1))
        self.st_CalculationMethod.SetMinSize((-1, -1))
        self.st_StratificationTable.SetMinSize((-1, -1))

        self.cc_DetailLevel.SetMinSize((80, 21))
        self.cc_DetailLevel.SetColumns([('Detail Level', 100)])
        self.cc_DetailLevel.InRow = False
        self.cc_DetailLevel.AllowInput = True
        self.cc_DetailLevel.SetItems([(str(Entry),-1) for Entry in range(10)], allowBlank = True, do_sort = False)

        self.cc_ShowDependency.SetMinSize((80, 21))
        self.cc_ShowDependency.SetColumns([('Show Dependency', 100)])
        self.cc_ShowDependency.InRow = False
        self.cc_ShowDependency.SetItems([('No',-1),('Yes',-1)], allowBlank = True, do_sort = False)

        self.cc_ShowHidden.SetMinSize((80, 21))
        self.cc_ShowHidden.SetColumns([('Show Dependency', 100)])
        self.cc_ShowHidden.InRow = False
        self.cc_ShowHidden.SetItems([('No',-1),('Yes',-1)], allowBlank = True, do_sort = False)

        self.tc_SummaryIntevals.SetMinSize((80, -1))

        self.tc_ColumnNumberFormatFloat.SetMinSize((80, -1))

        self.tc_ColumnNumberFormatInteger.SetMinSize((80, -1))

        self.tc_ColumnSeparator.SetMinSize((80, -1))

        self.tc_StratificationTable.SetMinSize((320, -1))

        self.lc_CandidateColumns.SetMinSize((320,140))
        self.lc_CandidateColumns.AllowBlank = False

        # add column information only if there are columns
        if self.ReportObject.__class__.__name__ in  ['SimulationResult','SimulationResults']:
            self.lc_CandidateColumns.CreateColumns([('Column Name/Group',300)])
            DetailedStateIndicatorList = []
            for Ending1 in [',State', ',Sub-Process' ]:
                for Ending2 in ['', '_Actual'] + DB.ParamNameExtensitons[1:] :
                    DetailedStateIndicatorList.append('<State Indicator'+ Ending1 + Ending2 +'>')
            ColumnGroupsToAdd = ['<Header>','<Number>','<Integer>','<State Indicator>','<System Option>'] +  DetailedStateIndicatorList
            
            self.lc_CandidateColumns.SetItems([(Entry,Num) for (Num,Entry) in enumerate(ColumnGroupsToAdd + self.ReportObject.DataColumns)], do_sort=False)

        self.tc_ColumnTitle.SetMinSize((320, -1))

        self.cc_CalculationMethod.SetColumns([('Calculation Method', 290)])
        self.cc_CalculationMethod.SetItems([(Entry,-1) for Entry in DB.ReportCalculationMethods], allowBlank = False, do_sort = False)
        self.cc_CalculationMethod.InRow = False
        self.cc_CalculationMethod.SetMinSize((320, -1))
        self.cc_CalculationMethod.GetTextCtrl().SetValue(DB.ReportCalculationMethods[0])

        self.btn_Add.SetMinSize((50,50))
        self.btn_Add.SetToolTipString("Add column to the selected column list")

        self.btn_Del.SetMinSize((50,50))
        self.btn_Del.SetToolTipString("Delete column From the selected column list")

        self.btn_LoadReportOptions.SetMinSize((200,-1))
        self.btn_LoadReportOptions.SetToolTipString("Load report options from file")
        self.btn_SaveReportOptions.SetMinSize((200,-1))
        self.btn_SaveReportOptions.SetToolTipString("Save report options to file")

        self.lc_SelectedColumns.SetMinSize((455,280))
        self.lc_SelectedColumns.CreateColumns([('Column Name/Group',220),('Calculation Method',150),('Title',80)])

        self.btn_Regenerate.SetMinSize((150,50))

        self.tc_ReportDisplay.SetMinSize((850,650))


    def __do_layout(self):

        OptionsSizer = wx.GridBagSizer(0,0)

        OptionsSizer.Add(self.st_DetailLevel, (0,0), (1,1), wx.ALIGN_RIGHT, 1)
        OptionsSizer.Add(self.cc_DetailLevel, (0,1), (1,1), wx.ALL, 1)

        OptionsSizer.Add(self.st_StratificationTable, (0,2), (1,1), wx.ALIGN_CENTER, 1)
        OptionsSizer.Add(self.tc_StratificationTable, (1,2), (2,1), wx.EXPAND | wx.ALL, 1)

        OptionsSizer.Add(self.btn_LoadReportOptions, (4,2), (1,1), wx.ALIGN_CENTER, 1)
        OptionsSizer.Add(self.btn_SaveReportOptions, (5,2), (1,1), wx.ALIGN_CENTER, 1)

        OptionsSizer.Add(self.st_ShowDependency, (1,0), (1,1), wx.ALIGN_RIGHT, 1)
        OptionsSizer.Add(self.cc_ShowDependency, (1,1), (1,1), wx.ALL, 1)
        OptionsSizer.Add(self.st_SummaryIntevals, (2,0), (1,1), wx.ALIGN_RIGHT, 1)
        OptionsSizer.Add(self.tc_SummaryIntevals, (2,1), (1,1), wx.ALL, 1)
        OptionsSizer.Add(self.st_ColumnNumberFormatFloat, (3,0), (1,1), wx.ALIGN_RIGHT, 1)
        OptionsSizer.Add(self.tc_ColumnNumberFormatFloat, (3,1), (1,1), wx.ALL, 1)
        OptionsSizer.Add(self.st_ColumnNumberFormatInteger, (4,0), (1,1), wx.ALIGN_RIGHT, 1)
        OptionsSizer.Add(self.tc_ColumnNumberFormatInteger, (4,1), (1,1), wx.ALL, 1)
        OptionsSizer.Add(self.st_ColumnSeparator, (5,0), (1,1), wx.ALIGN_RIGHT, 1)
        OptionsSizer.Add(self.tc_ColumnSeparator, (5,1), (1,1), wx.ALL, 1)

        OptionsSizer.Add(self.st_ShowHidden, (6,0), (1,1), wx.ALIGN_RIGHT, 1)
        OptionsSizer.Add(self.cc_ShowHidden, (6,1), (1,1), wx.ALL, 1)



        OptionsSizer.Add(self.st_CandidateColumns, (7,0), (1,1), wx.ALL, 1)
        OptionsSizer.Add(self.lc_CandidateColumns, (8,0), (5,1), wx.ALL, 1)
        OptionsSizer.Add(self.st_CalculationMethod, (13,0), (1,1), wx.ALIGN_BOTTOM | wx.ALL, 1)
        OptionsSizer.Add(self.cc_CalculationMethod, (14,0), (1,1), wx.ALIGN_TOP |wx.ALL, 1)
        OptionsSizer.Add(self.st_ColumnTitle, (15,0), (1,1), wx.ALIGN_BOTTOM | wx.ALL , 1)
        OptionsSizer.Add(self.tc_ColumnTitle, (16,0), (1,1), wx.ALIGN_TOP | wx.ALL , 1)

        OptionsSizer.Add(self.btn_Add, (8,1), (1,1), wx.ALIGN_CENTER, 1)
        OptionsSizer.Add(self.btn_Del, (9,1), (1,1), wx.ALIGN_CENTER, 1)

        OptionsSizer.Add(self.st_SelectedColumns, (7,2), (1,1), wx.ALL, 1)
        OptionsSizer.Add(self.lc_SelectedColumns, (8,2), (10,1), wx.ALL, 1)
        OptionsSizer.Add(self.btn_Regenerate, (18,0), (1,3), wx.ALL|wx.EXPAND, 1)

        self.OptionsPane.SetSizer(OptionsSizer)

        ReportSizer = wx.BoxSizer(wx.HORIZONTAL)
        ReportSizer.Add(self.tc_ReportDisplay, flag = wx.ALL|wx.EXPAND)
        self.ReportPane.SetSizer(ReportSizer)

        # add each panel to notebook control as pages
        self.NoteBook.AddPage(self.ReportPane, "Report Text")
        self.NoteBook.AddPage(self.OptionsPane, "Report Options")

        self.Layout()



    def AddColumnHandler(self):
        " Add a column to the report "
        # Get text from the list box
        Index = self.lc_CandidateColumns.GetFirstSelected()
        if Index != -1:
            ColumnText = str(self.lc_CandidateColumns.GetItemText(Index))
            CalculationMethod = str(self.cc_CalculationMethod.GetTextCtrl().GetValue())
            ColumnTitle = str(self.tc_ColumnTitle.GetValue())
            Item = (ColumnText,CalculationMethod,ColumnTitle)
            ToIndex = self.lc_SelectedColumns.GetFirstSelected()
            if ToIndex == -1:
                ToIndex = self.lc_SelectedColumns.GetItemCount()
            self.lc_SelectedColumns.AddItem(Item, ToIndex, False)
            # Reset the title to an empty string for the next add
            self.tc_ColumnTitle.SetValue('')
        return
    
    
    def DelColumnHandler(self):
        " Delete a column from the report "
        Index = self.lc_SelectedColumns.GetFirstSelected()
        if Index != -1:
            self.lc_SelectedColumns.DeleteItem(Index)
        return


    def ExtractReportOptions(self):
        " Extract the options from the screen "
        FormatOptions = self.FormatOptions
        # Detail level
        DetailLevelStr = str(self.cc_DetailLevel.GetTextCtrl().GetValue())
        if DetailLevelStr != '':
            try:
                DetailLevel = int (DetailLevelStr)
            except:
                cdml.dlgSimpleMsg('Report Parameter Error', 'The text in the detail level box is not a number, please enter a positive number in the detail level box or leave it blank for the default' , wx.OK, wx.ICON_ERROR, Parent = self)
                return
            if DetailLevel < 0:
                cdml.dlgSimpleMsg('Report Parameter Error', 'The number in the detail level box is negative, please enter a positive number in the detail level box or leave it blank for the default' , wx.OK, wx.ICON_ERROR, Parent = self)
                return
            FormatOptions = DB.HandleOption('DetailLevel', FormatOptions, DetailLevel, True)
        else:
            # Handle the defualt case by removing the option form the list
            NewFormatOptions = DB.HandleOption('DetailLevel', FormatOptions, None, False, True)
            if NewFormatOptions != None:
                FormatOptions = NewFormatOptions
        
        # Show Dependency
        ShowDependencyStr = str(self.cc_ShowDependency.GetTextCtrl().GetValue())
        if ShowDependencyStr != '':
            FormatOptions = DB.HandleOption('ShowDependency', FormatOptions, ShowDependencyStr == 'Yes', True)
        else:
            # Handle the defualt case by removing the option form the list
            NewFormatOptions = DB.HandleOption('ShowDependency', FormatOptions, None, False, True)
            if NewFormatOptions != None:
                FormatOptions = NewFormatOptions
        # Summary Intervals
        SummaryIntevalStr = str(self.tc_SummaryIntevals.GetValue())
        if SummaryIntevalStr != '':
            # Analyze the Summary Interval and make sure there
            # are only numbers there and valid punctuations there
            for Char in SummaryIntevalStr:
                if Char not in (DB.NumericCharacters + '[], '):
                    raise ValueError, 'Summary Interval may contain only numeric characters, brackets, commas, and spaces'
            try:
                # Transform this to a number
                SummaryInterval = eval(SummaryIntevalStr , DB.EmptyEvalDict)
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                cdml.dlgSimpleMsg('Report Parameter Error', 'Summary Interval does not evaluate to a valid expression. Here are Additional Details: '+ str(ExceptValue), wx.OK, wx.ICON_ERROR, Parent = self)
                return
            if not DB.IsList(SummaryInterval):
                # Handle the case that the user asked for only one
                # Summary Interval
                if DB.IsInt(SummaryInterval):
                    # Convert integer to list
                    SummaryInterval = [SummaryInterval]
                elif DB.IsTuple(SummaryInterval):
                    # Convert Tuple to list
                    SummaryInterval = list(SummaryInterval)
                else:
                    cdml.dlgSimpleMsg('Report Parameter Error', 'Invalid Summary Interval format', wx.OK, wx.ICON_ERROR, Parent = self)
                    return
            # Now verify that each member of the list is valid:
            for Member in SummaryInterval:
                if not (DB.IsInt(Member) or (DB.IsList(Member) and len(Member)==2 and all(map(lambda Entry: DB.IsInt(Entry), Member)))):
                    cdml.dlgSimpleMsg('Report Parameter Error', 'A member of the Summary interval list is not valid, i.e. not an integer or a list of two integers. The offending member is: ' + str(Member), wx.OK, wx.ICON_ERROR, Parent = self)
                    return
            FormatOptions = DB.HandleOption('SummaryIntervals', FormatOptions, SummaryInterval, True)
        else:
            # Handle the defualt case by removing the option form the list
            NewFormatOptions = DB.HandleOption('SummaryIntervals', FormatOptions, None, False, True)
            if NewFormatOptions != None:
                FormatOptions = NewFormatOptions
        # Number Formats
        ColumnNumberFormatFloatStr = str(self.tc_ColumnNumberFormatFloat.GetValue())
        ColumnNumberFormatIntegerStr = str(self.tc_ColumnNumberFormatInteger.GetValue())
        if ColumnNumberFormatFloatStr != '' or ColumnNumberFormatIntegerStr != '':
            if ColumnNumberFormatFloatStr == '' or ColumnNumberFormatIntegerStr == '':
                cdml.dlgSimpleMsg('Report Parameter Error', 'If a number format is defined, it should be defined both for floats and for integers', wx.OK, wx.ICON_ERROR, Parent = self)
                return
            ColumnNumberFormatFloatTest = ColumnNumberFormatFloatStr
            # Test that the float format is valid
            try:
                ColumnNumberFormatFloatTest % 123.456
            except:
                cdml.dlgSimpleMsg('Report Parameter Error', 'Float format is invalid - format should correspond to python string formatting conventions', wx.OK, wx.ICON_ERROR, Parent = self)
                return
            # Test that the Integer format is valid
            try:
                ColumnNumberFormatIntegerStr % 123456
            except:
                cdml.dlgSimpleMsg('Report Parameter Error', 'Integer format is invalid - format should correspond to python string formatting conventions', wx.OK, wx.ICON_ERROR, Parent = self)
                return
            # If reached here, format options can be specified
            FormatOptions = DB.HandleOption('ColumnNumberFormat', FormatOptions, (ColumnNumberFormatFloatStr,ColumnNumberFormatIntegerStr), True)
        else:
            # Handle the defualt case by removing the option form the list
            NewFormatOptions = DB.HandleOption('ColumnNumberFormat', FormatOptions, None, False, True)
            if NewFormatOptions != None:
                FormatOptions = NewFormatOptions
        # Column Separator
        ColumnSeparatorStr = str(self.tc_ColumnSeparator.GetValue())
        if ColumnSeparatorStr != '':
            FormatOptions = DB.HandleOption('ColumnSpacing', FormatOptions , ColumnSeparatorStr, True)
        else:
            # Handle the defualt case by removing the option form the list
            NewFormatOptions = DB.HandleOption('ColumnSpacing', FormatOptions, None, False, True)
            if NewFormatOptions != None:
                FormatOptions = NewFormatOptions
        # Show Hidden
        ShowHiddenStr = str(self.cc_ShowHidden.GetTextCtrl().GetValue())
        if ShowHiddenStr != '':
            FormatOptions = DB.HandleOption('ShowHidden', FormatOptions, ShowHiddenStr == 'Yes', True)
        else:
            # Handle the defualt case by removing the option form the list
            NewFormatOptions = DB.HandleOption('ShowHidden', FormatOptions, None, False, True)
            if NewFormatOptions != None:
                FormatOptions = NewFormatOptions

        # Column Selections
        NumberOfSelectedColumns = self.lc_SelectedColumns.GetItemCount()
        if NumberOfSelectedColumns > 0:
            ColumnList = []
            for Index in range(NumberOfSelectedColumns):
                ColumnText = str(self.lc_SelectedColumns.GetItem(Index,0).Text)
                CalculationMethod = str(self.lc_SelectedColumns.GetItem(Index,1).Text)
                ColumnTitle = str(self.lc_SelectedColumns.GetItem(Index,2).Text)
                ColumnList.append((ColumnText,CalculationMethod,ColumnTitle))
            FormatOptions = DB.HandleOption('ColumnFilter', FormatOptions, ColumnList, True)
        else:
            # Handle the defualt case by removing the option form the list
            NewFormatOptions = DB.HandleOption('ColumnFilter', FormatOptions, None, False, True)
            if NewFormatOptions != None:
                FormatOptions = NewFormatOptions

        # Stratification table
        StratificationTableStr = str(self.tc_StratificationTable.GetValue()).strip()
        if StratificationTableStr != '':
            try:
                #first verify that this is a valid expression
                DB.Expr(StratificationTableStr)
                #then verify that this is a valid expression
                DB.TableClass(StratificationTableStr)
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                cdml.dlgSimpleMsg('Report Parameter Error', 'The text in the Stratification Table box is not a valid table, please enter a valid table in the box or leave it blank for the default of no stratification. Here are Additional Details: '+ str(ExceptValue) , wx.OK, wx.ICON_ERROR, Parent = self)
                return
            FormatOptions = DB.HandleOption('StratifyBy', FormatOptions, StratificationTableStr, True)
        else:
            # Handle the defualt case by removing the option form the list
            NewFormatOptions = DB.HandleOption('StratifyBy', FormatOptions, None, False, True)
            if NewFormatOptions != None:
                FormatOptions = NewFormatOptions
                
        return FormatOptions


    def PopulateOptionsOnScreen(self,FormatOptions):
        """ updates controls with values from an option list """
        # Detail level
        DetailLevelStr = str(DB.HandleOption('DetailLevel', FormatOptions, ''))
        self.cc_DetailLevel.GetTextCtrl().SetValue(DetailLevelStr)
        # Show Dependency
        ShowDependency = str(DB.HandleOption('ShowDependency', FormatOptions, ''))
        ShowDependencyStr = DB.Iif(ShowDependency == '','',DB.Iif(ShowDependency,'Yes','No'))
        self.cc_ShowDependency.GetTextCtrl().SetValue(ShowDependencyStr)
        # Summary Intervals
        SummaryIntevalStr = str(DB.HandleOption('SummaryIntervals', FormatOptions, ''))
        self.tc_SummaryIntevals.SetValue(SummaryIntevalStr)
        # Number Formats
        (ColumnNumberFormatFloatStr,ColumnNumberFormatIntegerStr) = DB.HandleOption('ColumnNumberFormat', FormatOptions, ('',''))
        self.tc_ColumnNumberFormatFloat.SetValue(ColumnNumberFormatFloatStr)
        self.tc_ColumnNumberFormatInteger.SetValue(ColumnNumberFormatIntegerStr)
        # Column Separator
        ColumnSeparatorStr = str(DB.HandleOption('ColumnSpacing', FormatOptions , ''))
        self.tc_ColumnSeparator.SetValue(ColumnSeparatorStr)
        # Show Hidden
        ShowHidden = str(DB.HandleOption('ShowHidden', FormatOptions, ''))
        ShowHiddenStr = DB.Iif(ShowHidden == '','',DB.Iif(ShowHidden,'Yes','No'))
        self.cc_ShowHidden.GetTextCtrl().SetValue(ShowHiddenStr)
        # Column Selections
        ColumnList = DB.HandleOption('ColumnFilter', FormatOptions, [])
        # first delete all items to allow rebuilding the list
        self.lc_SelectedColumns.DeleteAllItems()
        # add to column list
        for Item in reversed(ColumnList):
            # each item is of the following format
            #Item = (ColumnText,CalculationMethod,ColumnTitle)
            self.lc_SelectedColumns.AddItem(Item, 0, False)
        # Stratification table
        StratificationTableStr = str(DB.HandleOption('StratifyBy', FormatOptions, ''))
        self.tc_StratificationTable.SetValue(StratificationTableStr)
        return                



    def RegenerateHandler(self):
        " Regenerates the Report Text according to the new options"
        # Extract report options
        FormatOptions = self.ExtractReportOptions()
        if FormatOptions != None:
            # Actually display the text
            ReportGenerationSuccess = self.DisplayText(FormatOptions)
            if ReportGenerationSuccess:
                # change the pane to see the text
                self.NoteBook.ChangeSelection(0)
        return


    def FrameEventHandler(self, evt):
        "The frame handling routine"
        # if current event is close window, call CloseForm function
        evtType = evt.GetEventType()
        evtId = evt.GetId()
        if evtType == wx.wxEVT_CLOSE_WINDOW:
            cdml.CloseForm(self,False)
            return
        elif evtType == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            if evtId == wx.ID_ADD:
                self.AddColumnHandler()
            if evtId == wx.ID_DELETE:
                self.DelColumnHandler()
            if evtId == wx.ID_APPLY:
                self.RegenerateHandler()
            if evtId == cdml.IDP_BUTTON1:
                self.LoadReportOptions()
            if evtId == cdml.IDP_BUTTON2:
                self.SaveReportOptions()
        return                

    def GetReportOptionsFileName(self, style_part):
        """ Open file selection window and get a report name"""
        NewPath = None
        wildcard =  "Options file (*.opt)|*.opt|All files (*.*)|*.*"
        dlg = wx.FileDialog(
                self, message="Choose a file for report options",
                defaultDir=os.getcwd(),
                defaultFile='RepOpt.opt',
                wildcard=wildcard,
                style= style_part)

        if dlg.ShowModal() == wx.ID_OK:
            NewPath = str(dlg.GetPath())
        return NewPath



    def SaveReportOptions(self):
        """ Save report options to file"""
        FormatOptions = self.ExtractReportOptions()
        if FormatOptions != None:
            # filter out the KeyFilter options since it is internal to the system
            # and should not be loaded or saved
            FormatOptionModified = DB.HandleOption('KeyFilter', FormatOptions, Value = None, UseNewValue = False, DeleteThisOption = True)
            if FormatOptionModified == None:
                # if KeyFilter did not exist, then use the original OptionList
                FormatOptionModified = FormatOptions
            # get path name
            path = self.GetReportOptionsFileName(wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if path != None:
                try:
                    DB.SaveOptionList(path,FormatOptionModified)
                except:
                    cdml.dlgErrorMsg(Parent = self)
        return

    
    def LoadReportOptions(self):
        """ Load report options from file"""
        path = self.GetReportOptionsFileName(wx.FD_OPEN)
        if path != None:
            try:
                BackupFormatOptions = copy.deepcopy(self.FormatOptions)
                FormatOptions = DB.LoadOptionList(path)
                KeyFilterOptionValue = DB.HandleOption('KeyFilter', self.FormatOptions, Value = None, UseNewValue = False, DeleteThisOption = False)
                if KeyFilterOptionValue != None:
                    DB.HandleOption('KeyFilter', FormatOptions, Value = KeyFilterOptionValue, UseNewValue = True, DeleteThisOption = False)
                # now load the data to the controls to reflect the newly loaded data
                # note that not validity checks are made, so if the file loaded
                # properly and had bad data this may be reflected as bad text in
                # the control or even raise an error that can be caught. Since this
                # is not disruptive to data stored in the system no additional
                # checks are made beyond what the system will allow in the controls
                self.PopulateOptionsOnScreen(FormatOptions)
                # now after data was updated update self with the new options
                self.FormatOptions = FormatOptions
                # Everything went fine - no need for backup anymore
                BackupFormatOptions = None
            except:
                cdml.dlgErrorMsg(Parent = self)
            if BackupFormatOptions != None:
                try:
                    # in case of a bad file or an error, restore blank values
                    self.PopulateOptionsOnScreen(BackupFormatOptions)
                except:
                    answer = cdml.dlgErrorMsg(msg_prefix='ASSERTION ERROR: Unable to recover from Error. Here are additional details: ',yesno=True, Parent = self)
                    if answer == wx.ID_YES :
                        return
                    else:
                        cdml.CloseForm(self, False)
        return



    def OnMenuSelected(self, event):
        """ Handles Menu selection """
        MenuID = event.GetId()
        if MenuID in [ wx.ID_SAVE, wx.ID_SAVEAS ]: # save or save as menu
            self.SaveReport(MenuID)
        else:
            cdml.OnMenuSelected (self, event)


    def SaveReport(self, menuId=wx.ID_SAVE):
        """ Save current report"""
        if '*' in self.Path or menuId == wx.ID_SAVEAS:
            NewPath = self.GetReportFileName()
            if NewPath == None: 
                return False
            else:
                self.Path = NewPath # replace previous path with current path
        try:
            OutputFileName = open(self.Path,'w')
            OutputFileName.write(self.ReportText)
            OutputFileName.close()        
        except:
            msg = 'Could not complete saving into the selected file, check if the file is not in use or otherwise locked'
            cdml.dlgSimpleMsg('ERROR', msg, wx.OK, wx.ICON_ERROR, Parent = self)
            return False
        return True
        
        
    def GetReportFileName(self):
        """ Open file selection window and get a report name"""
        NewPath = None
        wildcard =  "Text file (*.txt)|*.txt|All files (*.*)|*.*"
        [Head,Tail]=os.path.split(self.Path)
        dlg = wx.FileDialog(
                self, message="Choose a file name to save the report",
                defaultDir=Head,
                defaultFile=Tail,
                wildcard=wildcard,
                style= wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            NewPath = str(dlg.GetPath())
        return NewPath
        
    def DisplayText(self, FormatOptions=None):
        """ displays the text """
        if FormatOptions==None:
            FormatOptions = self.FormatOptions

        TheProgressDialog = None
        try:
            # version 2.5 does not support canceling simulation
            TheProgressDialog = cdml.ProgressDialogTimeElapsed(Parent = self, StartTimerUponCreation = False, AllowCancel = DB.SystemSupportsProcesses)

            # Define the Function to run on a thread
            def ReportGenerationStartMiniScript():
                "Generate the report and copy the text"
                # Define an encapsulating function so no arguments will be needed
                def FunctionToRunAsProcess():
                    ReturnVal = self.ReportObject.GenerateReport(FormatOptions)
                    return ReturnVal
                # Now run this function as a process - if possible
                (ProcessList, PipeList)=DB.RunFunctionAsProcess(FunctionToRunAsProcess)                
                return (ProcessList, PipeList)

            def ReportGenerationEndMiniScript(ProcessList, PipeList):
                "Copy the text"
                ReturnVal = PipeList[0].recv()
                return ReturnVal
            
            ThreadObject = cdml.WorkerThread(ReportGenerationStartMiniScript,ReportGenerationEndMiniScript)

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
                self.ReportText = 'The report generation operation was canceled by user request!'
            else:
                self.ReportText = Info
            
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            self.ReportText = 'Report Generation Error : The report could not be generated due to an error during generation. Here are Additional Details: '+ str(ExceptValue)

        # Properly destroy the progress dialog box if not done before
        if TheProgressDialog != None:
            TheProgressDialog.Destroy()

        # Clear previous text
        self.tc_ReportDisplay.SetReadOnly(False)
        self.tc_ReportDisplay.ClearAll()
        # Actually display the text
        self.tc_ReportDisplay.AddText(str(self.ReportText))
        self.tc_ReportDisplay.SetReadOnly(True)
        # Calculate the horizontal scroll width. Default is the number reported
        # by the system that should be 2000 pixels
        MaxPixelWidth = self.tc_ReportDisplay.GetScrollWidth()
        # Split the text lines to allow counting their length
        TextLines = self.ReportText.split('\n')
        for TextLine in TextLines:
            PixelLineWidth = self.tc_ReportDisplay.TextWidth(stc.STC_STYLE_DEFAULT,TextLine)
            MaxPixelWidth = max(MaxPixelWidth,PixelLineWidth)
        self.tc_ReportDisplay.SetScrollWidth(MaxPixelWidth)
        self.tc_ReportDisplay.ScrollToLine(0)
        self.tc_ReportDisplay.ScrollToColumn(0)
        return True       
            
       
        

# end of class MainFrame


if __name__ == "__main__":
    app = wx.App(0)
    #wx.InitAllImageHandlers() Deprecated
    DB.LoadAllData('InData' + DB.os.sep + 'Testing.zip')
    ScriptFileNameFullPath = DB.Projects[1010].CompileSimulation()
    ResultInfo = DB.Projects[1010].RunSimulationAndCollectResults(ScriptFileNameFullPath)
    frame_1 = MainFrame(mode=None, data=(ResultInfo, None), type=None, id_prj=0, parent=None )
    app.SetTopWindow(frame_1)
    frame_1.CenterOnScreen()
    frame_1.Show()
    app.MainLoop()
