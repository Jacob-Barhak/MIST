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
# This file contains a form to define Cost/Life of quality wizard              #
################################################################################

import DataDef as DB
import CDMLib as cdml
import sys
import wx
import copy

AllowedParameterTypesThatCanBeUsed = ['Integer','Number', 'State Indicator','System Option']

class WizardDialog(wx.Frame):
    def __init__(self, mode=None, data=None, type=None, id_prj=0, *args, **kwds):
        """ Constructor of the MainFrame class """
        self.idPrj = id_prj

        self.ParsedStruct = data

        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwdsnew)

        self.pn_main = wx.Panel(self, -1)
        self.label_1 = wx.StaticText(self.pn_main, -1, "Function Type : ")
        self.cb_type = wx.ComboBox(self.pn_main, -1, choices=["Cost Wizard = Init * 10**Sum(Coefficient*Value)", "Quality of Life Wizard = Init + Sum(Coefficient*Value)"], style=wx.CB_DROPDOWN)
        self.label_2 = wx.StaticText(self.pn_main, -1, "Initial Value : ")
        self.ed_ival = wx.TextCtrl(self.pn_main, -1, "")
        self.lc_vector = cdml.List(self.pn_main, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)

        # Up/Down arrow button
        arrow_up = cdml.getSmallUpArrowBitmap() # arrow bitmap for buttons
        arrow_dn = cdml.getSmallDnArrowBitmap()
        self.btn_up = wx.BitmapButton(self.pn_main, wx.ID_ADD, arrow_up)
        self.btn_dn = wx.BitmapButton(self.pn_main, wx.ID_DELETE, arrow_dn)

        self.cc_coef = cdml.Combo(self.pn_main, -1)
        self.tc_valu = cdml.Text(self.pn_main, -1)

        self.btn_undo = wx.Button(self.pn_main, wx.ID_UNDO, "Undo")
        self.btn_ok = wx.Button(self.pn_main, wx.ID_OK, "Ok")
        self.btn_cancel = wx.Button(self.pn_main, wx.ID_CANCEL, "Cancel")

        cdml.GenerateStandardMenu(self, SkipItems = [cdml.ID_MENU_REPORT_THIS, cdml.ID_MENU_REPORT_ALL])

        self.__set_properties()
        self.__do_layout()

        

        self.btn_ok.Bind(wx.EVT_BUTTON, self.OnClose)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.OnClose)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.cc_coef.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnListDblClick)
        self.Bind(wx.EVT_END_PROCESS, self.OnRefresh)

        self.btn_up.Bind(wx.EVT_BUTTON, self.OnEdit)
        self.btn_dn.Bind(wx.EVT_BUTTON, self.OnEdit)
        self.btn_undo.Bind(wx.EVT_BUTTON, self.OnEdit)

        self.InitData()

    # Define the default method to handle the menu selections
    OnMenuSelected = cdml.OnMenuSelected

    def __set_properties(self):
        self.SetTitle("Cost/QoL Wizard")
        self.HelpContext = 'Wizard'
        self.cb_type.SetSelection(0)
        self.cc_coef.SetColumns((('Name', 200),('Type', 82), ('Notes', 200)))
        self.cc_coef.InRow = False

        columns = ( ['Coefficients', 150], ['Values', 140])
        self.lc_vector.CreateColumns(columns)
        self.lc_vector.AllowBlank = False


    def __do_layout(self):
        sizer_0 = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_0.Add(self.pn_main, 0, 0, 0)
        sizer_2.Add(self.label_1, 0, wx.ALL, 3)
        sizer_2.Add(self.cb_type, 0, wx.ALL, 3)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        sizer_4.Add(self.label_2, 0, wx.ALL, 3)
        sizer_4.Add(self.ed_ival, 0, wx.ALL, 3)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)

        sizer_1.Add(self.lc_vector, 10, wx.EXPAND, 0)

        sizer_5.Add(self.cc_coef, 0, wx.ALL, 3)
        sizer_5.Add(self.tc_valu, 0, wx.ALL, 3)
        sizer_5.Add(self.btn_up, 0, wx.ALL, 3)
        sizer_5.Add(self.btn_dn, 0, wx.ALL, 3)
        sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)

        sizer_3.Add((50,0), 0, wx.ALL, 3 )
        sizer_3.Add(self.btn_undo, 0, wx.ALL, 3)
        sizer_3.Add(self.btn_ok, 0, wx.ALL, 3)
        sizer_3.Add(self.btn_cancel, 0, wx.ALL, 3)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

        self.pn_main.SetSizer(sizer_1)
        self.SetSizer(sizer_0)
        sizer_0.Fit(self)
        self.Layout()


    def OnEdit(self, event):
        action = event.GetId()

        index = self.lc_vector.GetFirstSelected()
        if action == wx.ID_ADD:
            if index == -1 : index = self.lc_vector.GetItemCount()

            coef = str(self.cc_coef.GetValueString())
            valu = str(self.tc_valu.GetValue())

            self.lc_vector.InsertStringItem(index, coef)
            self.lc_vector.SetStringItem(index, 1, valu)

            self.cc_coef.SetValue("")
            self.tc_valu.SetValue("")

        elif action == wx.ID_DELETE:
            if index == -1: return

            coef = str(self.lc_vector.GetItem(index,0).GetText())
            valu = str(self.lc_vector.GetItem(index,1).GetText())

            self.cc_coef.SetValueString(coef)
            self.tc_valu.SetValue(valu)

            self.lc_vector.DeleteItem(index)
            self.lc_vector.Select(index, True)

        elif action == wx.ID_UNDO:
            self.lc_vector.DeleteAllItems()
            self.InitData()


    def OnClose(self, event):
        """ Event handler activated when this dialog is closed"""

        if event.GetId() == wx.ID_OK:
            type_wizard = cdml.iif( 'Cost' in self.cb_type.GetValue(), 0, 1)
            ival = self.ed_ival.GetValue()

            coef, val = [], []
            item_num = self.lc_vector.GetItemCount()
            for i in range(item_num):
                coef.append(str(self.lc_vector.GetItem(i,0).GetText()))
                val.append(str(self.lc_vector.GetItem(i,1).GetText()))

            wizard_output = [ type_wizard, ival, coef, val ]
            try :
                CostWizardOutput = DB.ConstructCostWizardString(wizard_output)
                cdml.SetRefreshInfo(self, '', CostWizardOutput)

            except:
                CostWizardOutput = None
                ans = cdml.dlgErrorMsg(0, True, Parent = self)
                if ans == wx.ID_YES : return
            cdml.CloseForm(self, True, '', CostWizardOutput)

        else:
            cdml.CloseForm(self, False)


    def SetComboItem(self):
        """ sets the combo list items """
        items = [ (str(p), p.ParameterType, p.Notes, -1)
                    for p in DB.Params.values() if p.ParameterType in AllowedParameterTypesThatCanBeUsed ]
        self.cc_coef.SetItems(items)


    def InitData(self):
        """ Display given wizard data on each control """

        self.cb_type.SetSelection(self.ParsedStruct[0])
        self.ed_ival.SetValue(str(self.ParsedStruct[1]))
        for coef, val in zip(self.ParsedStruct[2], self.ParsedStruct[3]):
            index = self.lc_vector.InsertStringItem(sys.maxint, str(coef))
            self.lc_vector.SetStringItem(index, 1, str(val))
        self.SetComboItem()


    def OnListDblClick(self, event):
        """Open Parameter form when the text control is clicked twice"""

        item = str(event.GetEventObject().GetValue())
        if item not in DB.Params.keys():
            if item != "":
                cdml.dlgSimpleMsg('ERROR', "Can not find a parameter named " + item, Parent = self)
                self.OnRefresh(None)
                return

        types = AllowedParameterTypesThatCanBeUsed
        cdml.OpenForm("Parameters", self, cdml.ID_MODE_SINGL, item, types)


    def OnRefresh(self, event):
        """ Reopen text editor at previous position after closing Parameter form
            This method has been added because the TextEditMixin close the text box
            whenever user click of double-click a cell in the list control"""
        parm = cdml.GetRefreshInfo()
        # update the list of parameters in the combo box
        self.SetComboItem()
        if parm != None:
            self.cc_coef.GetTextCtrl().SetValue(str(parm))



if __name__ == "__main__":
    app = wx.App(0)
    #wx.InitAllImageHandlers() Deprecated

    DB.LoadAllData('InData' + DB.os.sep + 'Testing.zip')

    # Add a few parameters
    DB.Params.AddNew(DB.Param(Name = 'TestCovariate1', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Testing'))
    DB.Params.AddNew(DB.Param(Name = 'TestCovariate2', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Testing'))
    DB.Params.AddNew(DB.Param(Name = 'TestCovariate3', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Testing'))

    CostWizardStr = 'CostWizard (0, 100.12, [TestCovariate1,TestCovariate2, TestCovariate3], [ 1, 2, 3.0] )'
    ParsedStruct = DB.CostWizardParserForGUI(CostWizardStr)

    dialog_1 = WizardDialog(data=ParsedStruct, parent=None)
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
