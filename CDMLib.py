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
# This file contains all common constants, classes and functions for GUI       #
################################################################################


import os
# There is an issue with overlay scroll bars on Ubuntu Linux that breaks 
# combo controls. This line disables these scroll bars in favor of old style
# scroll bars that are more comppatible. 
os.environ['LIBOVERLAY_SCROLLBAR']='0'

import wxversion
# This line ensures that all wx imports will have a proper version
# therefore it is important that this file is always imported before wx
wxversion.ensureMinimal("3.0")
import wx
import wx.combo
import wx.lib.buttons
from wx.lib.wordwrap import wordwrap

import sys
import string
import types
import cStringIO

import thread

import DataDef as DB
import HelpInterface
import copy

# Define the GUI version
Version = (0,92,1,0,'MIST')
CompatibleWithDataDefVersion = (0,92,0,0,'MIST')

# Check that the Data Version and the GUI version are compatible
# Currently the Last text identifier in the version is ignored in
# comparison - this may change in the future.
if not hasattr(DB, 'Version'):
    VersionOfDB = None
else:
    VersionOfDB = DB.Version
    
if VersionOfDB == None or VersionOfDB[0:4] != CompatibleWithDataDefVersion[0:4]:
    raise ValueError, ' GUI version ' + str(Version) + ' is compatible only with DataDef version: ' + str (CompatibleWithDataDefVersion) + ' or higher, while attempting to load DataDef version: ' + str(VersionOfDB)


# CONSTANTS used in Project

# Ids used in menus
ID_MENU_ABOUT = wx.NewId()
ID_MENU_HELP = wx.NewId()
ID_MENU_HELP_GENERAL = wx.NewId()
ID_MENU_REPORT_THIS = wx.NewId()
ID_MENU_REPORT_ALL = wx.NewId()

# This is used by a popup menu
ID_MENU_COPY_RECORD = wx.NewId()
ID_SPECIAL_RECORD_ADD = wx.NewId()
ID_MENU_DELETE_RECORD = wx.NewId()

# Button ids used in frame
IDF_BUTTON1 = wx.NewId()
IDF_BUTTON2 = wx.NewId()
IDF_BUTTON3 = wx.NewId()
IDF_BUTTON4 = wx.NewId()
IDF_BUTTON5 = wx.NewId()
IDF_BUTTON6 = wx.NewId()
IDF_BUTTON7 = wx.NewId()
IDF_BUTTON8 = wx.NewId()
IDF_BUTTON9 = wx.NewId()
IDF_BUTTON10 = wx.NewId()
IDF_BUTTON11 = wx.NewId()
IDF_BUTTON12 = wx.NewId()
IDF_BUTTON13 = wx.NewId()
IDF_BUTTON14 = wx.NewId()
IDF_BUTTON15 = wx.NewId()
IDF_BUTTON16 = wx.NewId()
IDF_BUTTON17 = wx.NewId()
IDF_BUTTON18 = wx.NewId()
IDF_BUTTON19 = wx.NewId()
IDF_BUTTON20 = wx.NewId()

# Button ids used in panel
# Actually following constants are defined for convenience.
IDP_BUTTON1 = wx.NewId()
IDP_BUTTON2 = wx.NewId()
IDP_BUTTON3 = wx.NewId()
IDP_BUTTON4 = wx.NewId()
IDP_BUTTON5 = wx.NewId()
IDP_BUTTON6 = wx.NewId()
IDP_BUTTON7 = wx.NewId()
IDP_BUTTON8 = wx.NewId()
IDP_BUTTON9 = wx.NewId()
IDP_BUTTON10 = wx.NewId()

# Data type definition for Control class
ID_TYPE_NONE = -1
ID_TYPE_ALPHA = 0
ID_TYPE_INTEG = 1
ID_TYPE_FLOAT = 2
ID_TYPE_COMBO = 3

# Constants for event
ID_EVT_SORT = wx.NewId()    # dedicated id for sort.
                            # If this flag is set, default event handler call SortPanel function
ID_EVT_OWN = wx.NewId()     # indicat this control has own event handler.
                            # it is called by FrameEventHandler in CDMFrame class
ID_EVT_OPEN_WINDOW = wx.NewId() # Not used currently


# Ids for KeyValidator class
ALPHA_ONLY = 1 # only allow characters
DIGIT_ONLY = 2 # only allow numbers, including +/- sign
NO_INPUT   = 0 # not allow any keyboard input
NO_EDIT    = 3 # Not allow del or backspace key

## Id for Project Type
#ID_PRJ_SIMULATION = 'Simulation'
#ID_PRJ_ESTIMATION = 'Estimation'

# Id for open mode of a form
# NONE : no specific mode. Thus, all objects will be displaced in the scrolled window
# multi : in other word, 'filtered' mode. need only for 'Transition' form in current version
# single : Display single object to edit/create new object in any collection except Transition
ID_MODE_NONE = None
ID_MODE_MULTI = 'multi'
ID_MODE_SINGL = 'single'




# define supported commands for focus switch
SUPPORTED_COMMANDS = [ wx.wxEVT_COMMAND_BUTTON_CLICKED,
                            wx.wxEVT_COMMAND_LEFT_CLICK,
                            wx.wxEVT_COMMAND_MENU_SELECTED,
                            wx.wxEVT_COMMAND_LIST_ITEM_SELECTED ]


# common functions used in the CDM library and forms
def iif(condition, true_value, false_value):
    """Immediate if: if statement is true return TruePart otherwise FalsePart
        This function is copied from DataDef.py
    """
    if condition:   return true_value
    else:           return false_value


def xproperty(fget, fset, fdel=None, doc=None):
    """ Map set/get method to a property.
        Thus, 'form.SetProperty(PropertyA = value)' is same as 'form.PropertyA = value'
    """
    if isinstance(fget, str):
        attr_name = fget
        def fget(obj): return getattr(obj, attr_name)

    if isinstance(fset, str):
        attr_name = fset
        def fset(obj, val): setattr(obj, attr_name, val)


    return property(fget, fset, fdel, doc)


def Exist(obj):
    """ Simple function to check if an object is None or not """
    return obj != None


def OpenPopupMenu(self, event=None):
    """ Open Popup menu. To use this function, a frame should have a menu list named 'pup_menus' """

    if not hasattr(self, 'pup_menus'): return

    menu = setupMenu(self, self.pup_menus, False)   # crate popup menu and assign event handler
    self.PopupMenu(menu)                            # open popup menu
    menu.Destroy()                                  # remove from memory to show just once when right button is clicked




def CloseForm(self, refresh=True, collection=None, key=None):
    """ Common function to close new form """

    # check if current form has parent form
    parent = self.GetParent()
    self.MyMakeModal(False)
    self.Destroy()

    # If entered data is ok, throw event to refresh to parent row panel
    if refresh :
        SetRefreshInfo(self, collection, key) # save data(i.e. collection, key) to refresh field

        parent = self.GetParent()
        if parent!=None:
            event = wx.PyEvent()    # create new event
            event.SetEventType(wx.wxEVT_END_PROCESS)
            wx.PostEvent(parent, event) # throw the event to the parent of current frame


    if parent is None : return

    if not parent.IsTopLevel(): parent = parent.GetTopLevelParent()

    # if current form has parent form, raise it to the top of the screen
    parent.MyMakeModal()  # MakeModal(False) command makes all forms as Non-modal forms
                        # Thus, before raising the parent, MakeModal method should be called once more
    parent.Raise()


def OpenForm(name_module, parent, mode=None, key=None, type=None, id_prj=0):
    """ Common function to open a form
        arguments
            name_module : module name that includes the form
            parent : parent of new form, should be an instance of wx.Window class
            mode : Set the initial mode of new form.Default mode is None that displays all the data in a collection
            key : key(usually ID) of the record that is used in new form
            type : Specific type of record if needed. Additional data for initialization. Type of the target is changed according to mode
                    See Initialization method in CDMFrame class
            id_prj : ID of a project. It is used to prevent data change.
    """

    module = __import__(name_module)                # import form module
    form = module.MainFrame(mode, key, type, id_prj, parent)# create an instance of the form

    form.MyMakeModal()                                # Make this frame as modal window

    # Adjust the position of new form according to the screen size
    # If the size of form is smaller than screen size, open new form on the center of screen
    # Otherwise, set top left corner of the form at the corner of the screen
    sw, sh = wx.GetDisplaySize()
    fx, fy, fw, fh = form.GetRect()

    ox = iif( sw < fw, 0, 0.5 * (sw-fw) )
    oy = iif( sh < fh, 0, 0.5 * (sh-fh) )
    wid = iif( sw < fw, sw, fw )
    hgt = iif( sh < fh, sh, fh )

    form.SetRect((ox,oy, wid, hgt))
    form.Show()

    return form


# Define Administrator mode by using a global list
AdminMode = [False]

def GetAdminMode():
    """ Returns True if AdminMode set set """
    return AdminMode[0]

def SetAdminMode(NewValue = False):
    """ Set AdminMode to specified value """
    AdminMode[0] = NewValue


# global variable to save/retrieve refresh data
_com_stack = []

def GetRefreshInfo():
    """ Retrieve a database object using data in the clipboard
        This function is used to refresh information after closing child form
    """

    global _com_stack

    object = None

    if len(_com_stack) == 0 :
        return None

    info = _com_stack.pop()
    if info[0] == '':
        object = info[1] # In current version, this line is used only for Cost/QoL Wizard

    elif info[1] is None:
        object = info[1]

    else:
        object = GetRecordByKey(getattr(DB, info[0]), info[1])

    return object


def SetRefreshInfo(self, Collection=None, Key=None):
    """ Set target information for refreshing in the clipboard"""

    global _com_stack

    success = not (Collection == None and Key == None)

    if success:
        _com_stack.append((Collection, Key))

    return success


class Struct:
    """ Dummy class to create structure-like data
        It is used to replicate the variables in each database object
        See 'GetInstanceAttr' function
    """
    pass


def OpenAbout(self):
    """ Display information about Chronic Disease Model"""

    info = wx.AboutDialogInfo()
    info.Name = "MIcro Simulation Tool (MIST)\n"
    info.Version = 'Data Definitions Version: ' + str(DB.Version) + '\n GUI Version: '+ str(Version) 
    info.Copyright = " Copyright (C) 2013-2014 Jacob Barhak\n Copyright (C) 2009-2012 The Regents of the University of Michigan (IEST)"
    info.Description = wordwrap(
        "The Micro-simulation tools is a Monte-Carlo simulation compiler" 
        "It has been initially designed to help model Chronic Diseases."
        "MIST is a split branch from the GPL code of the "
        "Indirect Estimation and Simulation Tool (IEST). "
        "More information is available on the web site of the developer. ",
        350, wx.ClientDC(self))
    info.WebSite = ("http://sites.google.com/site/jacobbarhak/",
                    "")
    info.Developers = [ "\n Jacob Barhak - MIST system design and implementation"
                        "\n see IEST documentation for additional developers"]
    info.License = wordwrap(" The MIcroSimulation Tool (MIST) is free software: you"
                            " can redistribute it and/or modify it under the terms of the GNU General"
                            " Public License as published by the Free Software Foundation, either"
                            " version 3 of the License, or (at your option) any later version."
                            " \n"
                            " The MIcroSimulation Tool (MIST) is distributed in the"
                            " hope that it will be useful, but WITHOUT ANY WARRANTY; without even the"
                            " implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."
                            " See the GNU General Public License for more details."
                            ,350, wx.ClientDC(self) )

    wx.AboutBox(info)



#-----------------------------------------------------------------------#
#   Base class for all window class used in GUI                         #
#   Event and blank properties are defined                              #
#-----------------------------------------------------------------------#

class CDMWindow(wx.Window):
    """ Base Window class for CDM project. Derived from wx.Window class
        Base properties of a CDMWindow class are defined here
        See FrameEventHandler method in CDMFrame class for the usage of the event properties"""

    def __init__(self):
        self._isEmpty = False  # flag to check empty panel
        self._evtType = None    # event type : reserved for future extension
        self._evtID = None      # event ID : define specific action
        self._evtData = None    # data for event : depends on the event ID
        self._user_data = None  # user(programmer) definable data,

    # setters for above variables
    def SetEvtType(self, evt_type):
        """ Setter Method for Event Type of a CDMWindow Instance"""
        self._evtType = evt_type

    def SetEvtData(self, evt_data):
        """ Setter Method for Event Data of a CDMWindow Instance"""
        self._evtData = evt_data

    def SetEvtID(self, evt_id):
        """ Setter Method for Event Id of a CDMWindow Instance"""
        self._evtID = evt_id


    def SetEvent(self, evt):
        """ Setter Method for Event Related Properties (Type, Id, Data) of a CDMWindow Instance"""
        self._evtType = evt[0]
        self._evtID = evt[1]
        self._evtData = evt[2]


    def SetUserData(self, user_data):
        """ Setter Method for User Data of a CDMWindow Instance"""
        if type(self._user_data) == list:       # if type of user data is list
            self._user_data.append(user_data)

        else: # otherwise
            self._user_data = user_data


    def SetBackgroundColor(self, bgcolor=None):
        """ Setter Method for Background Color of a CDMWindow Instance"""
        if bgcolor == None:
            bgcolor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE)

        self.SetBackgroundColour(bgcolor)

    # Map the setter methods to a property
    # Using  'xproperty' function,
    # Getter/Setter methods can be used as same form
    # Ex : win.evtData = data is same as win.SetEvtData(data)
    # evtType is not used in the version. It is reserved for the future extension.
    evtType = xproperty( '_evtType', SetEvtType )
    evtData = xproperty( '_evtData', SetEvtData )
    evtID = xproperty( '_evtID', SetEvtID )
    userData = xproperty( '_user_data', SetUserData )

    def MyMakeModal(self, modal=True):
         if self.IsTopLevel():
             for w in wx.GetTopLevelWindows():
                 if w is not self and 'Inspection' not in str(w):
                     w.Enable(not modal)


#-----------------------------------------------------------------------#
#   Base class for a frame.                                             #
#   Common properties and methods are defined                           #
#-----------------------------------------------------------------------#

class CDMFrame(CDMWindow, wx.Dialog, wx.Frame):
#class CDMFrame(CDMWindow, wx.Frame):
    """
        Base Frame class for CDM project. It is derived from CDMWindow and wx.Frame class
        Common properties, methods and event handler are defined in this class
    """

    def __init__(self, mode=None, data=None, type=None, *args, **kwds):
        """ Initialization method for CDMFrame class
            Arguments
                - mode : open mode (single, multi, None)
                - data : used if mode is ID_MODE_SINGL. Usually, ID of a record
                - type : used for data checking.
        """

        CDMWindow.__init__(self)    # Initialize super class

        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN # set window style
        wx.Frame.__init__(self, *args, **kwdsnew)

        self._id_prev_panel = -1    # define ids to target panels and controls

        self._id_prev_ctrl = -1     # used to check the movement of focus
        self._id_this_panel = -1
        self._id_this_ctrl = -1

        self._no_row = 1         # initialize no. of RowPanel instances in the scrolled window
        self._collection = None # target collection(==name of global variables) in database related to this frame(or form)
        self._open_mode = mode  # Open mode of a form. It decides the number of RowPanel objects in ScrolledWindow
        self._open_data = data  # Data for opening mode(i.e. ID of a record)
        self._open_type = type  #

        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))

        # Bind common event handlers for the instances of CDMFrame class
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel) # Bind event handler for mouse wheel -> need to fix
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)  # Bind event handler for right mouse click. Open Popup menu
        self.Bind(wx.EVT_CLOSE, self.FrameEventHandler) # Bind event handler for close window event


    # create new panel and assign event hander
    def AddPanel(self , data = None):
        """ Method to add new RowPanel instance.
            Create and Set the position of new RowPanel instance"""

        # First, check if there is a RowPanel which is being focused( open or new )
        panel = self.FindRowPanelByStatus([wx.ID_OPEN, wx.ID_NEW])
        if panel :
            panel.SetStatus(wx.ID_NONE)


        new_panel = self.GetBlankPanel()

        if new_panel==None:
            # get position and size of last RowPanel
            # to calculate the position of new row panel
            x, y, w, h = 0, 0, 0, 0
            panels = list(self.pn_view.GetChildren())
            if panels:
                x, y, w, h = panels[-1].GetRect()

            # add new RowPanel defined in module
            if hasattr(self, 'SetupPanel'):
                new_panel = self.SetupPanel(py=y+h)     # Dedicated Setup method for each form
                                                        # Need to be implemented in each module
            else:
                module = __import__(self.__module__)
                new_panel = module.RowPanel(parent=self.pn_view, id=0, pos=(0,y+h))

            self.pn_view.GetSizer().Add(new_panel, 0, wx.ALL, 1)

            # Assign default event handler to controls in new RowPanel
            self.BindDefaultEvent(new_panel)
            # Find first editable control - Textbox, combobox or checkbox
            # Then set focus in that control
            new_ctrl = new_panel.GetDefaultFocus()
            new_ctrl.SetFocus()

            wx.CallAfter(adjustScrollBar, self, self.pn_view)  # Resize the length of scroll bar according to the number of RowPanel instances
            wx.CallAfter(scrollPanel, self.pn_view, new_panel) # Display new RowPanel instance

        else:
            # Find first editable control - Textbox, combobox or checkbox
            # Then set focus in that control
            new_ctrl = new_panel.GetDefaultFocus()
            new_ctrl.SetFocus()


        # If current RowPanel intance include Combo Control(s), it should have 'SetComboItem' method
        if hasattr(new_panel, 'SetComboItem'):
            new_panel.SetComboItem()            # check items in a combobox  and set items if necessary

        if data == None:
            # Set status of new RowPanel. Display asterisk(*) at the left side of the panel
            new_panel.SetStatus(wx.ID_NEW)
        else:            
            # In case data exists for the record, initialize the fields         
            new_panel.SetValues(data) # display current record data
            new_panel.SetId(self.NextRowID)
            self.IncrNextRowID()                # increase row no for indexing
            new_panel.SetStatus(wx.ID_OPEN)
            new_panel.SaveValues()          # copy panel data to record
            # Reset target information again to reflect changes

        # Reset target information
        self.SetPrevTarget( new_panel, new_ctrl )
        self.SetCurrTarget( new_panel, new_ctrl )

    # bind event for all controls in the new panel
    # ALL EVT_LEFT_UP evnts are for focus check
    def BindDefaultEvent(self, new_panel):
        """ Assign Event Handler to controls in a row panel """

        for ctrl in new_panel.GetChildren(): # for all controls in new panel

            type_ctrl = type(ctrl)

            # Static text doesn't need event handler
            if type_ctrl == wx._controls.StaticText or not ctrl.IsShown() :
                continue

            if type_ctrl in [ Button, BitmapButton, wx.Button ]:
                ctrl.Bind(wx.EVT_BUTTON, self.FrameEventHandler)

            elif type_ctrl == List:
                ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.FrameEventHandler)
                ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.FrameEventHandler)

            else:
                ctrl.Bind(wx.EVT_LEFT_UP, self.FrameEventHandler)   # for focus check

            # if curren control is ComboBox, Bind the Text Control to check the focus change
            if type_ctrl == Combo:
                ctrl.GetTextCtrl().Bind(wx.EVT_LEFT_UP, self.FrameEventHandler)

            # If a control has specific event type, bind this control to event handler for the event
            # This code reserved for evtType property in CDMWindow. Not used currently
            if Exist(ctrl.evtType):
                ctrl.Bind(ctrl.evtType, self.FrameEventHandler)


        # Bind this panel to Default Event Hanlder to check the focus change
        new_panel.Bind(wx.EVT_LEFT_DOWN, self.FrameEventHandler)


    def ForceRecordSaveAttempt(self):
        """ Tries to force a record save to be performed if needed """
        # Find current/previous panel and control
        # The function returns False if an Error occurred and True otherwise
        this_panel, this_ctrl = self.GetCurrTarget('obj')
        try:
            self.CheckFocus(this_panel, this_ctrl, this_panel, this_ctrl, None, True)
            return True
        except:
            dlgErrorMsg(Parent = self)
            return False

    # check the focus change
    def CheckFocus(self, prev_panel, prev_ctrl, this_panel, this_ctrl, typeEvt, ForceSaveAttempt = False):
        """ Method to process focus change in an Instance of CDMFrame class"""

        type_this_panel = iif( this_panel == None, this_panel, type(this_panel))
        type_prev_panel = iif( prev_panel == None, prev_panel, type(prev_panel))

        # check the focus moves from the title section to frame
        if type_this_panel == type_prev_panel and type_this_panel == None : return

        save_data = ForceSaveAttempt
        if type_this_panel == type_prev_panel: # row panel <-> row panel or row panel <-> title
            if this_panel.Id == prev_panel.Id :# if focus was moved in same panel
                if hasattr(this_ctrl, 'chkFocus') and this_ctrl.chkFocus :      # and current control needs to be checked
                    save_data = True

            elif prev_panel.isRow :
                save_data = True

        else: # row panel <-> frame
            if hasattr(prev_panel, 'isRow') and prev_panel.isRow:
                save_data = True

        if save_data :
            record = prev_panel.GetValues()         # read current values in previous panel

            if not DB.IsEqualDetailed(record, prev_panel.record):

                # Create new instance and save it to a collection
                # *** Need to be implemented in each row panel ***
                entry = prev_panel.SaveRecord(record)

                # display relevant message according to the entry.
                # If there is an error, current field won't be refreshed
                if entry is None:
                    if type(self.openType) in [ tuple, list ]:
                        str_type = str(self.openType)
                    else:
                        str_type = self.openType

                    raise ValueError, 'INVALID type. Type of current record should be (or should be one of): "' + string.upper(str_type) + '"'

                # if saved successfully and prev_panel is new, assign new Id
                if prev_panel.Id == 0:
                    prev_panel.SetId(self.NextRowID)
                    self.IncrNextRowID()                # increase row no for indexing

                # Refresh screen using new entry
                prev_panel.SetValues(entry)         # *** Need to be implemented in each row panel ***
                prev_panel.SaveValues()            # saves the new data in the record info - this is used if the panel is not exited since a button is pressed    
                prev_panel.ClearComboItem()         # release memory for ComboCtrls in prev_panel


        if this_panel != None:
            if this_panel.isRow:
                # check items in a combobox  and set items if necessary
                if hasattr(this_panel, 'SetComboItem'):
                    this_panel.SetComboItem()   # *** Need to be implemented in each row panel if necessary ***

                # If focus is moved from title section or frame or dialog,
                # save current values
                if  prev_panel is None or \
                    ( prev_panel and prev_panel.Id != this_panel.Id ):
                    this_panel.SaveValues()     # Copy current value to record property.
                                                # *** Need to be implemented in each row panel if necessary ***
                if type_prev_panel:     # If previous panel is row panel
                    prev_panel.SetStatus( wx.ID_NONE )

                else: # or check the panels in the scrolled window
                    panels = self.pn_view.GetChildren()
                    for panel in panels:
                        if panel.Id == this_panel.Id or panel.Status != wx.ID_OPEN: continue
                        panel.SetStatus( wx.ID_NONE )
                        break

                if this_panel.isRow :
                    this_panel.SetStatus(this_panel.Id, False) # set status of current RowPanel

        self.SetCurrTarget(this_panel, this_ctrl) # set current panel/control as previous objects
        self.SetPrevTarget(this_panel, this_ctrl)



    # Default event handler for a frame
    # Basic functions - add, delete, focus change, undo, find - are done here
    # Specific event defined for each control also can be done here
    # ALL METHOD MARKED WITH STARS(***) SHOULD BE IMPLEMENTED IN EACH RowPanel Class
    def FrameEventHandler(self, evt):
        """ Default Event Handler of CDMFrame class """

        evtType = evt.GetEventType()
        this_ctrl = evt.GetEventObject()
        menuId = evt.GetId()

        try:
            panels = list(self.pn_view.GetChildren())

            # Find current/previous panel and control
            this_panel, this_ctrl = self.InitCurrTarget(this_ctrl)
            prev_panel, prev_ctrl = self.GetPrevTarget('obj')

            # First check event(s) which doesn't require focus check such as Undo
            # Undo function always use previous panel as target panel
            # because if there was no error, prev_panel is same as this_panel
            if menuId == wx.ID_UNDO:
                prev_panel.Undo(getattr(DB, self.Collection))
                return

            # If row panels exist in the scrolled window, check focus
            if panels != []:
                self.CheckFocus(prev_panel, prev_ctrl, this_panel, this_ctrl, evtType)

            # if current event is close window, call CloseForm function
            if evtType == wx.wxEVT_CLOSE_WINDOW:
                if not this_panel:
                    panel = prev_panel
                else:
                    panel = this_panel
                if not panel or panel.IsBlank():
                    Collection = None
                    Key = None
                else:
                    Collection = self.Collection
                    Key = panel.Key
                IsInfoPassingBackInvalid = self.CheckBeforeClose(Key) 
                if IsInfoPassingBackInvalid:
                    msg = "The information passed by this form to the parent form is not the correct type. If you continue closing with form, the record will be saved. However, it will not be passed back to the parent. Do you wish to continue?"
                    ans = dlgSimpleMsg('ERROR', msg, wx.YES_NO, wx.ICON_ERROR, Parent = self)
                    if ans == wx.ID_NO :
                        return
                    else:
                        Collection = None
                        Key = None
                    
                CloseForm(self, refresh=True, collection=Collection, key=Key)
                return

            # if current control is Combo, now open the popup window
            if type(this_ctrl) in [ Combo, wx._controls.ComboBox ] and \
                evtType == wx.wxEVT_LEFT_UP:
                this_ctrl.OpenPopup()

            # process control specific event
         
            
            if evtType in SUPPORTED_COMMANDS:
                # if there are nothing in the scroll window and action is not ADD
                if panels == [] and menuId not in [wx.ID_ADD, wx.ID_OPEN]:
                    dlgSimpleMsg('ERROR', "Fields are not defined in this form. Please add a field first", wx.OK, wx.ICON_ERROR, Parent = self)
                    return

                # First check pre-defined actions
                if menuId == wx.ID_FIND : # open search dialog
                    row_panel = self.GetFocusedPanel()
                    dlgFind(self.pn_view, row_panel.GetDefaultFocus(), self, -1, "").Show()

                elif menuId in [wx.ID_ADD, ID_MENU_COPY_RECORD, ID_SPECIAL_RECORD_ADD] : # ADD a new row panel
                    if Exist(prev_panel) and prev_panel.Id == 0 :   # if there is new panel which is not saved
                        dlgSimpleMsg('GUI ERROR', "Can't add new panel. Please enter data first", wx.OK, wx.ICON_ERROR, Parent = self)
                        prev_ctrl.SetFocus()
                    else:
                        if menuId == ID_MENU_COPY_RECORD:
                            # Get the data by copying the current record
                            frm = prev_panel.GetTopLevelParent()
                            Collection = getattr(DB, frm.Collection)
                            # Note that this actually changes the DB
                            RecordData = Collection.Copy(prev_panel.Key)
                            self.AddPanel(data=RecordData)
                        elif menuId == ID_SPECIAL_RECORD_ADD:
                            # Get the data by calling the frame window function
                            # with the current record key
                            frm = prev_panel.GetTopLevelParent()
                            if hasattr(frm,'SpecialRecordAdd'):
                                RecordData = frm.SpecialRecordAdd(prev_panel)
                                self.AddPanel(data=RecordData)
                        else:
                            # No data for a new record
                            self.AddPanel()


                elif menuId == wx.ID_DELETE : # Delete row panel and record in database
                        self.DeletePanel(this_panel)
                        return

                else: # Then, look for control specific actions
                    # handle the case of the sort sub menu
                    if evtType == wx.wxEVT_COMMAND_MENU_SELECTED:
                        EventID = ID_EVT_SORT
                        btn = self.FindWindowById(menuId)
                    else:
                        btn = this_panel.FindWindowById(menuId)
                        if type(btn) == ListCtrlComboPopup :    # if current control is list control in popup window
                            btn = btn.GetParent().GetParent()   # find Combo Control to retrieve event action id
                        EventID = btn.evtID

                    if EventID == ID_EVT_SORT:           # sort
                        SortPanels( self.pn_view, btn)

                        # If there is a panel which is focused or new scroll window to the panel
                        cur_panel = self.FindRowPanelByStatus([wx.ID_OPEN, wx.ID_NEW])
                        if cur_panel:
                            scrollPanel(self.pn_view, cur_panel)

                    elif EventID == ID_EVT_OWN:
                        btn.evtData(evt)                    # call own event handler

        except:
            # If an exception occur, display error message and move the focus to previous control

            if evtType == wx.wxEVT_CLOSE_WINDOW :
                ans = dlgErrorMsg(yesno=True, Parent = self)
                if ans == wx.ID_YES : return

                CloseForm(self, False)
                return

            else:
                dlgErrorMsg(Parent = self)

            if Exist(this_panel) and this_panel.isRow:
                this_panel.SetStatus(wx.ID_NONE)

            if type(this_ctrl) == Checkbox:
                this_ctrl.SetValue(not this_ctrl.GetValue())

            if Exist(prev_panel) :
                prev_panel.SetStatus(prev_panel.Id, False)
                prev_ctrl.SetFocus()
                self.SetPrevTarget(prev_panel, prev_ctrl)
                self.SetCurrTarget(prev_panel, prev_ctrl)


        # If the event is activated by button clicking or menu selection,
        # the event should not be propagated.
        # For the event propagation, refer wxPython manual

        if evtType not in SUPPORTED_COMMANDS:
            evt.Skip()


    def CheckBeforeClose(self, Key):
        """ Dummy method to be overridden when inherited """
        # This method should raise an error if closing the form will pass
        # an invalid type record to the previous form. This function serves
        # as default and does nothing and should be overridden by a derived
        # class to take effect of this feature.
        # The function returns False if problem is encountered. A True should
        # Trigger a message to the user.
        return False

    # delete panel and record by clicking 'x' button or selecting 'delete' menu
    def DeletePanel(self, this_panel=None):
        """ Method to delete row panel and object in database"""

        # If target panel is not set, check current target
        if this_panel == None:
            this_panel = self.GetCurrTarget('obj', 'panel')

        # If can't find target panel, display error message
        if self.GetCurrTarget('id', 'panel') < 0:
            dlgSimpleMsg('GUI ERROR', "Please select a panel", wx.OK, wx.ICON_ERROR, Parent = self)
            return

        # If target panel is in database or data was entered for new row panel
        # check user's response
        if this_panel.Id > 0 or not this_panel.isEmpty:
            RecordName =  this_panel.TextRecordID()
            msg = "Do you really want to delete this record? \n"
            msg += "The " + RecordName + " will be deleted permanently"
            answer = dlgSimpleMsg('WARNING', msg, wx.YES_NO, wx.ICON_QUESTION, Parent = self)

            if (answer == wx.ID_NO): return


        # delete record in database
        if this_panel.Id > 0:
            CollectionInstance = getattr(DB, self.Collection)
            CollectionInstance.Delete(this_panel.Key, ProjectBypassID = self.idPrj)
            
        sizer = this_panel.GetContainingSizer()     # get sizer that contains this panel
        sizer.Detach(this_panel)                    # detach this panel from containing sizer
        wx.CallAfter(this_panel.Destroy)            # remove panel
        self.Layout()                               # re-arrange panels

        # set the status of the previous panel as NONE --> delete arrow mark
        prev_panel = self.GetPrevTarget('obj', 'panel')
        if Exist(prev_panel):
            prev_panel.SetStatus(wx.ID_NONE)

        self.ResetTargetInfo()                      # initialize target(panel, control) ids

        if len(self.pn_view.GetChildren()) == 0: return # if all row panel have been deleted, return
            
        adjustScrollBar(self, self.pn_view)         # change the length of the scroll bar
        self.SetDefaultTarget(0)                    # set current target


    # Find new panel
    def FindRowPanelById(self, pid):
        """Find RowPanel object in a frame and return it using Panel Id"""

        for panel in self.pn_view.GetChildren():
            if panel.Id == pid : return panel


        return None


    # Find new panel


    def FindRowPanelByStatus(self, status):
        """Find RowPanel object in a frame and return it using Panel Status"""

        if type(status) not in [list, tuple]:
            status = [status]

        for panel in self.pn_view.GetChildren():
            if panel.Status in status :
                return panel

        return None


    def GetBlankPanel(self):
        """ Method to fine newly added row panel """
        return self.FindWindowById(0)


    def ReturnDisplayedRecordKeys(self):
        """Return all the record ID's in the form"""
        
        Result = []
        # Note that a new record will not have a Key parameter
        for panel in self.pn_view.GetChildren():
            if 'Key' in dir(panel):
                Result.append(panel.Key)
        return Result



    # retrieve current target information : id/object of panel/control
    def GetCurrTarget(self, type='obj', what='both'):
        """ Mehtod to retrieve current targets(panel/control) information(id or object)"""
        if type == 'id':
            if what == 'panel':
                return self._id_this_panel

            elif what == 'ctrl':
                return self._id_this_ctrl

            else:
                return self._id_this_panel, self._id_this_ctrl

        elif type == 'obj':
            if what == 'panel':
                return self.FindRowPanelById(self._id_this_panel)

            elif what == 'ctrl':
                return self.FindWindowById(self._id_this_ctrl)

            else:
                return self.FindRowPanelById(self._id_this_panel), \
                        self.FindWindowById(self._id_this_ctrl)


    def GetFocusedPanel(self):
        """ Find a panel whose status is OPEN or NEW """
        panels = self.pn_view.GetChildren()
        status = [ panel.Status for panel in panels ]
        id_panel = [ panel.Id for panel in panels ]

        if wx.ID_OPEN in status:
            id = id_panel[status.index(wx.ID_OPEN)]
            return self.FindRowPanelById(id)

        elif wx.ID_NEW in status:
            id = id_panel[status.index(wx.ID_NEW)]
            return self.FindRowPanelById(id)

        return None


    def GetPrevTarget(self, type='obj', what='both'):
        """ Retrieve previous target information : id/object of panel/control """
        if type == 'id':
            if what == 'panel':
                RetVal = self._id_prev_panel

            elif what == 'ctrl':
                RetVal = self._id_prev_ctrl

            else:
                RetVal = self._id_prev_panel, self._id_prev_ctrl

        elif type == 'obj':
            if what == 'panel':
                RetVal = self.FindRowPanelById(self._id_prev_panel)

            elif what == 'ctrl':
                RetVal = self.FindWindowById(self._id_prev_ctrl)

            else:
                RetVal = self.FindRowPanelById(self._id_prev_panel), \
                        self.FindWindowById(self._id_prev_ctrl)

            return RetVal



    def IncrNextRowID(self, incr_no=None):
        """ Increase row no after adding new row panel """

        self._next_row_id += iif( incr_no != None, incr_no, 1 )

    def ResetNextRowID(self):
        """ Reset the number of row panel """
        self._next_row_id = 1

    # set getter/setter method as property
    NextRowID = xproperty('_next_row_id', IncrNextRowID)

    def ResetTargetInfo(self):
        """ Reset target panel/control id """
        self._id_prev_panel = -1
        self._id_prev_ctrl = -1
        self._id_this_panel = -1
        self._id_this_ctrl = -1

    def InitCurrTarget(self, ctrl):
        """ Determine where the cursor is """

        if isinstance(ctrl, CDMPanel): # button down on a panel
            this_panel = ctrl
            this_ctrl = this_panel.GetDefaultFocus()

        # if current event object is Frame (CloseWindow event)
        # or item in popup menu selected
        elif isinstance(ctrl, CDMFrame) or type(ctrl) == wx._core.Menu:
            this_panel, this_ctrl = None, None

        # now assume all clicks on controls, find CDMPanel object
        else:
            this_ctrl = ctrl
            this_panel = ctrl.GetParent()
            while not isinstance(this_panel, CDMPanel):
                this_panel = this_panel.GetParent()

        return this_panel, this_ctrl

    # Initialize data and panels programmatically when the form activated
    def Initialize(self, data=None):
        """
            Data initialization for a frame
            Main function :
            - build list for the combo boxes from Database : MainProcess, Model, Project etc.
            - write values of each field on the controls in a row panel
        """

        if data != None : # If data(object) list is given, use that list
            objects = data

        # else if open mode isn't specified, use all data in a collection
        elif self.openMode == ID_MODE_NONE :
            # Retrieve the values in a list sorted by the ID. Therefore the
            # natural order in the GUI will be by the ID of the object
            objects = [Entry for (Key,Entry) in sorted(getattr(DB, self.Collection).iteritems())]

        # else if this method is called to edit single object,
        #           find the target object using openData
        elif self.openMode == ID_MODE_SINGL:
            object_get = GetRecordByKey(getattr(DB, self.Collection), self.openData)
            objects = iif( object_get == None, [], [object_get] )

        no_panel = len(objects)
        # If object list is empty, prepare blank RowPanel instance
        if no_panel == 0 : no_panel = 1

        # Clear scroll window
        self.pn_view.DestroyChildren()
        self.ResetTargetInfo()  # reset target panel/control information(id) for focus checking
        self.ResetNextRowID()       # reset index of row panel

        # If object list is empty, return
        if no_panel == 0 : return

        # If this method is called to edit single object,
        # delete control(i.e 'x' button), 'Open' and 'Find' buttons are disabled.
        if self.openMode == ID_MODE_SINGL:
            for ctrl in self.pn_title.GetChildren():
                if type(ctrl) not in [Button, wx._controls.Button] : continue
                # Do not disable add buttons as there are allowed in single mode
                if ctrl.Id == wx.ID_ADD : continue
                ctrl.Enable(False)

        # Create progress dialog, if panel no. is greater than 20 <-- set by manual test
        dlg = None
        if no_panel > 20:
            dlg = wx.GenericProgressDialog("Loading Data",
                                    "Please wait......",
                                    maximum = no_panel,
                                    parent=self,
                                    style = wx.PD_CAN_ABORT
                                            | wx.PD_APP_MODAL
                                            | wx.PD_ELAPSED_TIME
                                            | wx.PD_REMAINING_TIME )
            dlg.CenterOnScreen()
            keepGoing = True

        y = 0
        sizer = self.pn_view.GetSizer()
        module = __import__(self.__module__)
        for i in range(no_panel):
            if hasattr(self, 'SetupPanel'): # if current form has dedicated SetupPanel method, call it
                panel = self.SetupPanel(y)

            else: # Else simply create  an instance of RowPanel class
                panel = module.RowPanel(parent=self.pn_view, id=0, pos=(0,y))

            sizer.Add(panel, 0, wx.ALL, 1)              # add new panel to the sizer
            self.BindDefaultEvent(panel)                # bind event handler

            if objects != []:   # If found an database object
                panel.SetValues(objects[i], init=True) # display current record data
                panel.SetId(self.NextRowID)                     # assign panel Id : sequential order

            panel.SetStatus(wx.ID_NONE)

            self.IncrNextRowID()                            # increase row no = panel Id + 1

            if dlg != None:
                (keepGoing, skip) = dlg.Update(i)
                if not keepGoing : break

            w, h = panel.GetSizeTuple()
            y += ( h + 1 )

        if dlg != None: dlg.Destroy()

        adjustScrollBar(self, self.pn_view) # change the size of scroll bar

        if hasattr(panel, 'SetComboItem'): # If this panel have combo controls, assign items
            list(self.pn_view.GetChildren())[0].SetComboItem()

        self.SetDefaultTarget(0) # set first panel as default, '0' is index of first row panel instance


    # Map OpenPopupMenu to OnContextMenu method
    OnContextMenu = OpenPopupMenu


    # Not implemented yet
    def OnMouseWheel(self, event):
        """ Default event handlers to manage mouse wheel scroll """
        rot = event.GetWheelRotation()
        delta = event.GetWheelDelta()
        mx, my = event.GetPositionTuple()

        xunit, yunit = self.pn_view.GetScrollPixelsPerUnit()
        hx,hy=self.pn_view.GetSizeTuple()
        cx,cy=self.pn_view.GetClientSizeTuple()
        sx,sy=self.pn_view.GetViewStart()

        if rot!=0:
            self.pn_view.Scroll(0,delta/rot)

        event.Skip()


    def OpenDebugMsg(self, (type, value, traceback), debug=False, popup=True):
        """ Open error message for try ~ except statements """

        if debug: # pull out information about the exception
            frame = traceback.tb_frame
            code = traceback.tb_frame.f_code
            msg = '%s : %s\n\nFile : %s\nMethod name : %s\nLine No : %s' %  \
                (type.__name__, value, code.co_filename, code.co_name, frame.f_lineno )
        else:
            msg = '%s : %s' % (type.__name__, value )

        if popup: # set the method how to display the error message
            dlgSimpleMsg('ERROR', msg, wx.OK, wx.ICON_ERROR, Parent = self)
        else:
            self.sb.Notify(msg)


    def SetCollection(self, collection):
        """ Set collection related to this frame """
        self._collection = collection

    Collection = xproperty('_collection', SetCollection)


    def SetCurrTarget(self, panel=None, ctrl=None):
        """ Save current target information(ID) """
        if panel != None:
            self._id_this_panel = iif( type(panel) == int, panel, panel.Id )

        if ctrl != None:
            self._id_this_ctrl = iif( type(panel) == int, ctrl, ctrl.Id)


    def SetPrevTarget(self, panel=None, ctrl=None):
        """ Save previous target information(ID) """
        if panel != None:
            self._id_prev_panel = iif( type(panel) == int, panel, panel.Id )

        if ctrl != None:
            self._id_prev_ctrl = iif( type(ctrl) == int, ctrl, ctrl.Id )


    def SetDefaultTarget(self, idx):
        """ Set default panel and control using given index value
            If there is new panel, it is selected as default target """

        tmp_panel = self.GetBlankPanel()
        if not Exist(tmp_panel):    # If can't find new row panel, set focus on the given panel in scrolledwindow
            tmp_panel = list(self.pn_view.GetChildren())[idx]

        tmp_panel.SaveValues()
        tmp_ctrl = tmp_panel.GetDefaultFocus()
        tmp_panel.SetStatus(tmp_panel.Id, False)

        self.SetPrevTarget(tmp_panel, tmp_ctrl)
        self.SetCurrTarget(tmp_panel, tmp_ctrl)

        scrollPanel(self.pn_view, tmp_panel)
        tmp_ctrl.SetFocus()


    def SetOpenMode(self, mode):
        """ Set mode of a form"""
        self._open_mode = mode

    def SetOpenData(self, data):
        """ Set opening data for a form"""
        self._open_data = data

    def SetOpenType(self, type):
        """ Set required type of record for a form"""
        self._open_type = type

    def SetPrjId(self, id_prj):
        self._id_prj = id_prj

    openMode = xproperty('_open_mode', SetOpenMode)
    openData = xproperty('_open_data', SetOpenData)
    openType = xproperty('_open_type', SetOpenType)

    idPrj = xproperty('_id_prj', SetPrjId)



#---------------------------------------------------------------#
#    BASE Panel Class                                           #
#---------------------------------------------------------------#

class CDMPanel(CDMWindow, wx.Panel):
    """
        Base Panel class for CDM project. Derived from CDMWindow and wx.Panel class
        Common properties, methods are defined
    """
    def __init__(self, is_row=True, *args, **kwds):
        """ Initialize CDMPanel class """

        CDMWindow.__init__(self)    # initialize super class
        wx.Panel.__init__(self, *args, **kwds)

        self._is_full = True        # Full panel or short
        self._status = wx.ID_NEW    # Indicate the status of this panel. Default is NEW
        self._is_row = is_row       # Indicate that this panel is used for title section if this property is False
        self._key = None            # variable to save key value for an instance
        self._user_data = None      # varialbe to save additional data

        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))

        if self._is_row:
            self.Bind(wx.EVT_END_PROCESS, self.OnRefresh)


    def ClearComboItem(self):
        """ Remove the items of a ComboCtrl in CDMPanel instance"""
        for ctrl in self.GetChildren():
            if type(ctrl) not in [ Combo, wx.combo.ComboCtrl ]: continue
            ctrl.GetListCtrl().DeleteAllItems()


    def GetDefaultFocus(self):
        """ Find first editable control(Text, Combo or Checkbox) in a row panel """
        for ctrl in self.GetChildren():
            if type(ctrl) in [Text, Combo, Checkbox]:
                return ctrl

        return None


    def GetProjectId(self):
        """ Get project id of parent frame"""

        frm = self.GetTopLevelParent()

        return frm.idPrj


    def IsBlank(self):
        """ Check a row panel whether it is blank or not """

        no_ctrl, no_blank = 0, 0
        for ctrl in self.GetChildren():
            if type(ctrl) not in [Combo, Text, Checkbox]: continue
            type_ctrl = type(ctrl)
            if type_ctrl == Combo :
                last = ctrl.GetTextCtrl().GetLastPosition()
                value = ctrl.GetTextCtrl().GetRange(0,last)

            elif type_ctrl == Text :
                last = ctrl.GetLastPosition()
                value = ctrl.GetRange(0,last)

            elif type_ctrl == Checkbox:
                value = ctrl.GetValue()
                if not value : value = ''

            if value == '': no_blank += 1
            no_ctrl += 1

        return no_ctrl == no_blank


    def OnRefresh(self, event):
        """ Event handler to refresh selected field(i.e. control) after closing child form
        """

        record = GetRefreshInfo()

        # The following commented code is old code candidate for deletion
        # it protects against passing No information back from a form.
        # The new version deals with it below and avoids bringing up a message
        # Check the record
        # This code may not be used because the type of record is verified at the CheckFocus method
        #if record is None:
        #    dlgSimpleMsg('ERROR', 'INVALID data for current field')
        #    return

        # Refresh items in combo controls
        if hasattr(self, 'SetComboItem'):
            self.SetComboItem()

        # Get control need to be refreshed
        parent = self.GetTopLevelParent()
        cur_ctrl = parent.GetPrevTarget('obj', 'ctrl')
        direct_parent = cur_ctrl.GetParent()
        
        # Check the record
        if record is None:
            value = ''
        elif hasattr(record, 'Name'):
            value = str(record.Name)
        else:
            value = str(record)

        if hasattr(record, 'ID'):
            ID = record.ID
        else:
            ID = None

        # if this is part of a combo control, update the ID
        if DB.IsInstanceOf(direct_parent,'Combo'):
            if ID != None:
                direct_parent.SetValue(ID)
        else:        
            # Set value for current control,
            #
            if hasattr(cur_ctrl,'SetValue'):
                cur_ctrl.SetValue(value)
                
        # Set focus to that control    
        cur_ctrl.SetFocus()

        # send an event for a text box
        if hasattr(cur_ctrl,'SendTextUpdatedEvent'):
            cur_ctrl.SendTextUpdatedEvent()


    def SaveValues(self):
        """ Back up the current values of controls in a row panel when focus is moved in """

        record = self.GetValues()

        if record.__dict__ != {}: self.record = record



    def SetPanelLength(self, is_full):
        """ Setter method to set a length of a row panel """
        self._is_full = is_full


    def SetStatus(self, id, use_stock_id=True):
        """ Method to show the status of a panel """

        if use_stock_id : # If want to use stock id of wxPython
            self._status = id

        else: # Else set the status using Id of a row panel
            if id == 0:
                self._status = wx.ID_NEW
            else:
                self._status = wx.ID_OPEN

        SetBullet(self.st_status, self._status)


    def SetAsRow(self, is_row):
        """ Set this panel as a row panel or not"""
        self._is_row = is_row


    def SetUserData(self, data):
        """ Method to set an user data of a panel """
        self._user_data = data


    def SetKey(self, key):
        """ Method to set a key value of a panel """
        self._key = key


    def Undo(self, collection):
        """ Undo Method :
            Clear all fields for a blank panel,
            Display original data for a existing panel """

        if self.Id == 0: # if this panel is new one, simply clear all fields
            for ctrl in self.GetChildren():
                type_ctrl = type(ctrl)
                if type_ctrl not in [ Text, Checkbox, Combo, List ]: continue

                if type_ctrl == Checkbox:
                    ctrl.SetValue(False)

                elif type_ctrl == List:
                    ctrl.DeleteAllItems()

                else:
                    ctrl.SetValue('')

        else:   # Else retrieve original data from database and display it
            if not collection.has_key(self.Key): return

            idx = collection.keys().index(self.Key)
            obj = collection.values()[idx]
            self.SetValues(obj)


    # define setters and getters as Properties
    isRow = xproperty('_is_row', SetAsRow)
    userData = xproperty('_user_data', SetUserData)
    isEmpty = xproperty( IsBlank, None )
    isFull = xproperty( '_is_full', SetPanelLength )
    Key = xproperty('_key', SetKey)
    Status = xproperty('_status', SetStatus)


#----------------------------------------------------------------------#
#    Base class for all control class in this library                  #
#----------------------------------------------------------------------#
class CDMControl(CDMWindow):
    """ Base Control class for CDM project. It's derived from CDMWindow"""

    def __init__(self):
        """ Initialize CDMControl Class"""

        CDMWindow.__init__(self)    # initialize super class

        self._sortId = -1               # variable to set sort order
        self._case_sensitive = True # set case sensitive or not -- for future extension
        self._data_type = ID_TYPE_ALPHA # set data type
        self._name_field = None     # variable to connect this control to a field of DB object
                                        # --> for future extension
        self._check_focus = False       #


    def SetSortId(self, id):
        """ Method to set the sort id"""
        self._sortId = id

    def SetDataType(self, type):
        """ Method to set the data type"""
        self._data_type = type

    def SetFieldName(self, name):
        """ Method to set the name of data field"""
        self._name_field = name

    def SetCheckFocus(self, check):
        self._check_focus = check

    sortId = xproperty( '_sortId', SetSortId )
    dataType = xproperty( '_data_type', SetDataType )
    nameFld = xproperty( '_name_field', SetFieldName )
    chkFocus = xproperty( '_check_focus', SetCheckFocus )


class BitmapButton(CDMControl, wx.lib.buttons.GenBitmapTextButton):
    """  General button with bitmap. Derived from wx.lib.buttons.GenBitmapTextButton """

    def __init__(self, *args, **kwds):
        """ Constructor method of BitmapButton class"""

        CDMControl.__init__(self)
        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.BORDER_NONE
        wx.lib.buttons.GenBitmapTextButton.__init__(self, *args, **kwdsnew)
        self.SetBackgroundColor()

        self._order = wx.ID_NONE    # Set flag to display the sort direction (ascending or descending)
                                    # According to this flag, up/down arrow will be displayed in front of button label

    def SetOrder(self, order):
        """ Method to set the _order flag """
        self._order = order


    def SetBullet(self, order):
        """ Set the button bitmap according to the sort order """
        if order == wx.ID_UP:
            bmp = getSmallUpArrowBitmap()

        elif order == wx.ID_DOWN:
            bmp = getSmallDnArrowBitmap()

        else:
            bmp = None

        self.SetBitmapLabel(bmp)
        self.Refresh()

    Order = xproperty( '_order', SetOrder )



class Button(CDMControl, wx.Button):
    """ Simple Button class w/o bitmap. Derived from wx.Button.
        This class was implemented to add more properties for the CDM project
    """
    def __init__(self, *args, **kwds):

        CDMControl.__init__(self)
        wx.Button.__init__(self, *args, **kwds)
        self.SetBackgroundColor()

        self._order = wx.ID_NONE    # set flag to display the sort order


    def SetOrder(self, order):
        """ Method to set the _order flag """
        self._order = order



class Checkbox(CDMControl, wx.CheckBox):
    """ Checkbox control derived from CDMControl and wx.CheckBox """

    def __init__(self, *args, **kwds):
        """ Constructor for Checkbox control """
        CDMControl.__init__(self)

        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.BORDER_NONE
        wx.CheckBox.__init__(self, *args, **kwdsnew)


class Combo(CDMControl, wx.combo.ComboCtrl):
    """ Combo control. It's derived from CDMControl class and wx.combo.ComboCtrl class
        A combo control consists of Combo box, Popup window and a child control in popup window.
        Thus, two classes are need to be implemented.
        In current version, Combo class and ListCtrlComboPopup class consist a complete Combo Control.
        Combo and ListComboclass and was taken from wxPython demo and modified
    """

    def __init__(self, *args, **kwds):
        """ Constructor of the Combo class """

        CDMControl.__init__(self)

        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.combo.CC_NO_TEXT_AUTO_SELECT|wx.combo.CC_MF_ON_CLICK_AREA
        wx.combo.ComboCtrl.__init__(self, *args, **kwdsnew)

        self._allow_input = False       # Flag to allow user input
        self._in_row = True   # Is this combo control in RowPanel instance?
                              # If it is, focus change should be checked before
                              # opening the popup window
        self._data_type = ID_TYPE_COMBO # Initialize data type for this combo control


        # Create a Popup control
        lccp = ListCtrlComboPopup()

        # Associate them with each other.
        # This also triggers the creation of the ListCtrl.
        self.SetPopupControl(lccp)

        #self.Bind(wx.EVT_KILL_FOCUS, self.OnExit)
        self.GetTextCtrl().Bind(wx.EVT_KILL_FOCUS, self.OnExit)


    def SetItems(self, items, allowBlank=True, do_sort = True):
        """ Wrapping method of SetItems method in ListCtrlComboPopup """
        self.GetPopupControl().GetControl().SetItems(items, allowBlank, do_sort)

    def AddItem(self, item):
        """ Wrapping method of AddItem method in ListCtrlComboPopup """
        self.GetPopupControl().GetControl().AddItem(item)

    def DeleteItem(self, item):
        """ Delete an item in the ListCtrlComboPopup instance """
        list = self.GetListCtrl()
        idx = list.FindItem(-1, item)
        if idx != wx.NOT_FOUND:
            list.DeleteItem(idx)
            list.AdjustPopupHeight()

    def SetColumns(self, columns): # columns : tuple with title and length
        """
            Set columns and column headers
            Arguments : columns - List of Tuples [(header, width), (header, width), ... ]
        """
        self.GetPopupControl().GetControl().SetColumns(columns)


    def SetColumnWidth(self, col, width) : 
        """
            Set column width for a specific column
        """
        self.GetPopupControl().GetControl().SetColumnWidth(col, width)


    def GetListCtrl(self):
        """ Get handle of List Control in ListCtrlPopupCombo class """
        return self.GetPopupControl().GetControl()


    def SetValue(self, value):
        """ Set Combo Control value """

        if value in [ None, '', 0 ]: # if nothing defined, clear the text area
            self.GetTextCtrl().Clear()
            return

        if self._data_type == ID_TYPE_ALPHA: # write string in the text box
            self.GetTextCtrl().SetValue(str(value))
            self.SetInsertionPoint(0) # Move cursor to the start of text

        elif self._data_type == ID_TYPE_COMBO: # by value - Long integer
            self.SetValueByItemData(value)


    def SetValueByItemData(self, value):
        """ Set Combo Control value by value - Long integer"""

        the_list = self.GetPopupControl().GetControl()
        index = the_list.FindItemData(-1, value)

        if index == wx.NOT_FOUND : return

        item = the_list.GetItem(index, 0).GetText()
        self.GetTextCtrl().SetValue(str(item))
        the_list.SetItemValue(value)

        self.SetInsertionPoint(0)


    def SetValueString(self, string):
        """ Set value in the text area of a Combo control directly
            Usually used for Initialize method of CDMFrame"""
        self.GetTextCtrl().SetValue(str(string))

    def OnExit(self, event):
        """ Self Checking Method. Activated when the focus moved out """

        if not self.AllowInput:
            value = self.GetTextCtrl().GetValue()
            list = self.GetPopupControl().GetControl()
            idx = list.FindItem(-1, value)
            if list.GetItemCount() > 0 and idx == wx.NOT_FOUND:
                # The next conditional is needed on Unix systems that do not
                # recognise a blank string when FindItem is used
                if value != '':
                    dlgSimpleMsg('ERROR', 'Input name is not in the list', wx.OK, wx.ICON_ERROR, Parent = self)
                    self.GetTextCtrl().SetFocus()
        self.SetInsertionPoint(0)
        event.Skip()

    def OnButtonClick(self):
        """ Block default behavior (open popup) of ComboCtrl """

        if self._in_row : # If this combo control need to be tested for focus changing
            return

        # Else open or hide the popup window
        # This means that if this combo control is out of a row panel, do its original behavior
        if not self.IsPopupShown():
            self.ShowPopup()

        else:
            self.HidePopup()


    def OpenPopup(self):
        """ Override of OpenPopup method in wx.combo.ComboCtrl.
            It's called immediately after closing the popup window. """

        self.ShowPopup()


    def SetFocus(self):
        """ Move focus to the TextCtrl in Combo control"""
        self.GetTextCtrl().SetFocus()


    def GetValue(self):
        """ Override of the GetValue method.
            Retrieve value according to the _data_type flag """


        # Check this control is empty.
        # This code was implement in one of previous version. May not be used in current version
        #is_blank = False
        #if value == '': is_blank = True

        if self._data_type == ID_TYPE_ALPHA:    # If data type is String
            value = self.GetTextCtrl().GetValue()
            ret_val = value

        elif self._data_type == ID_TYPE_COMBO: # If data type is ID
            the_list = self.GetListCtrl()            
            value = the_list.GetItemValue()
            if value == None:
                ret_val = 0
            else:
                ret_val = value

        else: # If data type is integer or float, use sscanf function
            value = self.GetTextCtrl().GetValue()
            ret_val, is_blank = sscanf( value, self._data_type )

        return ret_val


    def GetValueString(self):
        """ Retrieve string from the TextCtrl in Combo control"""
        last = self.GetTextCtrl().GetLastPosition()
        value = str(self.GetTextCtrl().GetRange(0,last))
        return value


    def SetInput(self, allow_input):
        """ Method to set _allow_input flag"""
        self._allow_input = allow_input

    def InRowPanel(self, is_in_row):
        """ Method to set the position of combo control
            """
        self._in_row = is_in_row

    AllowInput = xproperty( '_allow_input', SetInput )
    InRow = xproperty('_in_row', InRowPanel)


class ListCtrlComboPopup(wx.ListCtrl, wx.combo.ComboPopup):
    """
        An interface between a ComboCtrl and
        a ListCtrl that is used as the popup for the combo widget.
        This code has been taken from the wxPython demo
    """
    __max_height = 300
    __min_width = 500

    def __init__(self):
        """ Constructor method of ListCtrlComboPopup"""
        # Since we are using multiple inheritance, and don't know yet
        # which window is to be the parent, we'll do 2-phase create of
        # the ListCtrl instead, and call its Create method later in
        # our Create method.  (See Create below.)
        self.PostCreate(wx.PreListCtrl())

        # Also init the ComboPopup base class.
        wx.combo.ComboPopup.__init__(self)

    def SetItems(self, items, allowBlank, do_sort = True):
        """ Add items to ListCtrl
            This method is same as SetItems in List Control.
            This method may be replaced the method in the List control in the future
        """

        self.DeleteAllItems()
        if type(items) == list:
            if items == []: return

            has_data = iif( type(items[0][-1] in [int, long]), True, False)
            if do_sort:
                items.sort()
            for item in items:
                self.AddItem(item, has_data)

            # add blank line on top of the list
            if allowBlank:
                self.InsertStringItem(0, '')
                self.SetItemData(0, 0)

        elif type(items) == dict: # implemented for test
            for item ,key in zip(items.values(),items.keys()):
                index = self.InsertStringItem(self.GetItemCount(), str(key))
                self.SetStringItem(index, 1, str(item[1]))
                self.SetItemData(index, item[0])


    def AddItem(self, item, has_data=True):
        """ Add an item to ListCtrl
            This method is same as SetItems in List Control.
            This method may be replaced the method in the List control in the future
        """
        no_column = iif( has_data, len(item)-1, len(item))
        if self.GetColumnCount() != no_column:
            raise ValueError, 'ASSERTION ERROR: wrong number of columns in combo'        
        index = self.InsertStringItem(self.GetItemCount(), str(item[0]))
        for j in range(1,no_column):
            self.SetStringItem(index, j, str(item[j]))

        if has_data:
            self.SetItemData(index, item[-1])


    def SetColumns(self, columns):
        """ Create columns in ListCtrl
            This method is same as SetItems in List Control.
            This method may be replaced the method in the List control in the future
        """

        self.DeleteAllColumns()
        for i, column in enumerate(columns):
            self.InsertColumn(i, column[0], format=wx.LIST_FORMAT_LEFT, width=column[1])


    def OnMotion(self, evt):
        """ Event handler for mouse motion"""
        item, flags = self.HitTest(evt.GetPosition())
        if item >= 0:
            # We no longer select the line during motion to reduce flickering
            # This is why the select line is commented, yet the curitem value
            # is changed to be ready for next click. Since there is no
            # selection, this may be harder for the user to see what is
            # higlighted , yet at the same time the current value will remain
            # displayed, sometime making it easier for the user.
            # The main issue why this was commented is flickering.
            # self.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        """ Event handler for mouse left click """
        self.Select(self.curitem)
        self.value = self.curitem
        self.Dismiss()
        evt.Skip()

    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.


    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        """ Initialize the current value and index of ListCtrl """
        self.value = -1
        self.curitem = -1

    def Create(self, parent):
        """Create the popup child control.  Return true for success. """

        wx.ListCtrl.Create(self, parent,
                        style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.SIMPLE_BORDER|wx.LC_VRULES)

        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True


    def GetControl(self):
        """ Return the widget that is to be used for the popup """
        return self

    def SetStringValue(self, val):
        """ Called just prior to displaying the popup, you can use it to
            'select' the current item. """
        idx = self.value
        if idx != wx.NOT_FOUND:
            self.Select(idx)

    def SetItemValue(self, val):
        """ Set the value of the current item """
        idx = self.FindItemData(-1, val)
        if idx != wx.NOT_FOUND:
            self.Select(idx)
            self.value = idx
        return



    def GetStringValue(self):
        """ Return a string representation of the current item. """
        if self.value >= 0:
            return str(self.GetItemText(self.value))
        return ''


    def GetItemValue(self):
        """ Return the value of the current item. """
        idx = self.value
        # Return None if none was found
        if idx != wx.NOT_FOUND:
            ret_val = self.GetItemData(idx)
        else:
            ret_val = None
        return ret_val


    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        wx.combo.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.combo.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.combo.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        no_item = self.GetItemCount()+1     # for header reserve single line
        if no_item == 1 : no_item += 1  # if there is no item add blank line



        # add one more row to display horizontal scroll bar if needed
        no_item += 1

        f = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)

        # There are several components that may effect the combobox height
        FontHeight = f.GetPixelSize().height 
        CaptionHeight = wx.SystemSettings.GetMetric(wx.SYS_CAPTION_Y)
        ScrollHeight = wx.SystemSettings.GetMetric(wx.SYS_HSCROLL_Y)
        MenuHeight = wx.SystemSettings.GetMetric(wx.SYS_MENU_Y)

        # To simplify matters use the maximal height of these and
        # multiply by the number of items - this will surely add some
        # extra space, yet it is better than no enough space
        height = max(FontHeight,CaptionHeight, ScrollHeight,MenuHeight)*no_item

        # Dont let height be to large for very long lists
        if height > ListCtrlComboPopup.__max_height:
            height = ListCtrlComboPopup.__max_height

        return (ListCtrlComboPopup.__min_width, height) # size of popup window

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.
    # Default returns false.
    def LazyCreate(self):
        return wx.combo.ComboPopup.LazyCreate(self)



class List(CDMControl, wx.ListCtrl):
    """ Dedicated List control. It's derived from CDMControl and wx.ListCtrl class"""

    def __init__(self, *args, **kwds):
        """ Constructor of the Combo class """
        CDMControl.__init__(self)

        wx.ListCtrl.__init__(self, *args, **kwds)

        self._add_blank = True      # Flag to allow blank line at the top of the list


    def CreateColumns(self, columns):
        """ Create columns in a list control """
        for i, column in enumerate(columns):
            self.InsertColumn(i, column[0], format=wx.LIST_FORMAT_LEFT, width=column[1])


    def SetItems(self, items, do_sort=True):
        """ Method to add multiple items to a list control"""

        self.DeleteAllItems()   # if no data, just clear and return
        if items == []: return

        if do_sort : items.sort() # sort items

        # Check the data have item data
        has_data = type(items[0][-1]) in [int, long]
        for i, item in enumerate(items):
            self.AddItem(item, i, has_data) #Call method to add single item in the list control

        if not self._add_blank : return

        # add blank line on top of the list
        self.InsertStringItem(0, '')
        self.SetItemData(0, 0)


    def AddItem(self, item, row, has_data = True):
        """ Method to add single item to a list control """

        no_column = iif(has_data , len(item)-1, len(item))
        if self.GetColumnCount() != no_column:
            raise ValueError, 'ASSERTION ERROR: wrong number of columns'
        index = self.InsertStringItem(row, str(item[0]))     # create new row
        for j in range(1,no_column):                    # add additional column data to new row
            self.SetStringItem(index, j, str(item[j]))
            
        # Check this item has item data
        # Each item of list control can have item data ( should be long type )
        if has_data:
            self.SetItemData(index, item[-1])


    def SetBlankRow(self, allow_blank):
        """ Setter to set the flag which indicate whether the list control allow blank
            on the top"""
        self._add_blank = allow_blank

    AllowBlank = xproperty("_add_blank", SetBlankRow)



class Text(CDMControl, wx.TextCtrl):
    """ Text control derived from CDMControl and wx.TextCtrl """

    def __init__(self, *args, **kwds):
        """ Constructor for Text control """
        CDMControl.__init__(self)
        wx.TextCtrl.__init__(self, *args, **kwds)

    def GetValue(self):
        """ Retrieve formatted value according to the _data_type flag """
        TheText = self.GetValueString()
        ret_val, self._isEmpty = sscanf( TheText, self._data_type )
        return ret_val

    def GetValueString(self):
        """ Retrieve value as a string """
        try:
            Last = self.GetLastPosition()
            RawString = self.GetRange(0,Last)
            TheText = str(RawString)
        except UnicodeEncodeError:
            # Deal with an error that can be created by unicode/text conversion
            # go over each character and
            TheText = repr(RawString)[1:-1]
        return TheText

    def SetValue(self, value):
        """
            Set value of Text control. String is the default data type of a Text control in wxPython.
            This method was implemented to add more convenience to SetValue method.
        """

        self.Clear()        
        try:
            # Try regular conversion to text
            TextValue = str(value)
            self.WriteText(TextValue)
        except UnicodeDecodeError:
            # if not working show escape characters. It is better than 
            # displaying nothing to the user. Also bring an info message box
            # so the user can fix this later on.
            TextValue = repr(value)[1:-1]
            self.WriteText(TextValue)
            # give an indication to the user using a message box
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            dlgSimpleMsg('Info - Unicode issue encountered', 'The system could not display some of the characters properly and therefore converted the string while marking special characters with a \\ escape character. This may happen if text was written in another system. You can continue for now, yet this issue should better be fixed to allow better interoperability between systems. The string was: \n' + str(TextValue) + '\n Here are Additional Details: '+ str(ExceptValue), wx.OK, wx.ICON_INFORMATION, Parent = self)
        self.SetInsertionPoint(0)

    SetValueString = SetValue

    Value = xproperty(None, SetValue )


class StatusBar(wx.StatusBar):
    """ StatusBar Class derived from wx.StatusBar. Not used in current version.
        Implemented for future use"""

    def __init__(self, parent):
        """ Constructor of StatusBar class"""

        self.blick = 0
        self.msg = ''
        wx.StatusBar.__init__(self, parent, -1)

        # This status bar has three fields
        self.SetFieldsCount(1)

        # Clear Fields
        self.SetStatusText(" ", 0)

        self.bgcolor = self.GetBackgroundColour()


    def Notify(self, msg):
        """ Display message on StatusBar"""
        self.SetBackgroundColour('#ff0000')
        self.SetStatusText(msg,0)
        self.msg = msg
        self.Refresh()

    def Clear(self):
        """ Clear StatusBar"""

        self.SetStatusText(" ",0)
        self.SetBackgroundColour(self.bgcolor)

    def OnTimer(self, event):
        """ Timer function to blink or delete text automatically"""
        if self.blick % 2 :
            self.SetStatusText(self.msg)
        else:
            self.SetStatusText(" ")

        if self.blick == 9:
            self.timer.Stop()
            self.SetStatusText(" ", 0)
            self.blick = 0
            self.msg = ''

        self.blick += 1

    def IsRunning(self):
        """ Check the Timer control is running """
        return self.timer.IsRunning()


    def Destroy(self):
        """ Destroy Timer control in StatusBar"""
        self.timer.Destroy()




#-----------------------------------------------------------------------#
#       validator to check the data type in a text box                  #
#-----------------------------------------------------------------------#
class KeyValidator(wx.PyValidator):
    """ Class to validate data input on a control """

    def __init__(self, flag):
        """ Constructor of the KeyValidator class"""
        wx.PyValidator.__init__(self)
        self.flag = flag                # set the validation type. See OnChar method
        self.Bind(wx.EVT_CHAR, self.OnChar)


    def Clone(self):
        """
        Note that every validator must implement the Clone() method.
        """
        return KeyValidator(self.flag)


    def OnChar(self, evt):
        """ Event handler to check key input """
        key_nav = [ wx.WXK_HOME, wx.WXK_END,
                    wx.WXK_LEFT, wx.WXK_RIGHT,
                    wx.WXK_UP, wx.WXK_DOWN,
                    wx.WXK_PAGEUP, wx.WXK_PAGEDOWN ]

        key_copy = [ ord('C')-64, wx.WXK_INSERT]
        # The above keys stand for Ctrl-C and Ctrl-Insert
        # Note that pressing control changes the code reported by GetKeyCode
        # Therefore the special treatment required.

        key_code = evt.GetKeyCode()
        ctrl_key_down = evt.ControlDown() 

        if key_code > 255 : key = None
        else:               key = chr(key_code)


        # Always allow a copy operation
        if not (ctrl_key_down and (key_code in key_copy) ):

            if self.flag == NO_EDIT and ( key_code not in key_nav ):
                    return

            elif self.flag == DIGIT_ONLY and \
                key_code not in key_nav and \
                key in [string.letters+string.punctuation]:

                dlgSimpleMsg("WARNING", "Text input is not allowed in this field", wx.OK, wx.ICON_WARNING, Parent = self)
                return

            elif self.flag == ALPHA_ONLY and \
                    key_code not in key_nav and key in string.digits:

                dlgSimpleMsg("WARNING", "Numeric values are not allowed in this field", wx.OK, wx.ICON_WARNING, Parent = self)
                return

            elif self.flag == NO_INPUT and key_code not in key_nav:
                dlgSimpleMsg("WARNING", "Keyboard input is not allowed in this field.", wx.OK, wx.ICON_WARNING, Parent = self)
                return

        evt.Skip()


#---------------------------------------------------------------------------#
#   functions for a scrolled window                                         #
#   Original code is on the wiki.wxpython.org/wxPython_Cookbook             #
#   adjust the size of the scroll bar
#---------------------------------------------------------------------------#

def adjustScrollBar(frame, swin):
    """ Adjust the size of ScrollBar according to the number of RowPanel """

    sizer = swin.GetSizer()
    w,h = sizer.GetMinSize()
    swin.SetVirtualSize((w,h))




# scroll to current position of a row panel if it is out of scrolled window
def scrollPanel(swin, panel):
    """ Scroll to the position of a RowPanel"""
    x,y = panel.GetPositionTuple()
    hx,hy = panel.GetSizeTuple()

    xunit, yunit = swin.GetScrollPixelsPerUnit()
    cx,cy = swin.GetClientSizeTuple()
    sx,sy = swin.GetViewStart()
    sx *= xunit
    sy *= yunit

    y += sy

    if (y<sy):      swin.Scroll(0,y/yunit)

    if (x<sx):          swin.Scroll(0,-1)

    if ((x+sx)>cx): swin.Scroll(0,-1)

    if ((y+hy-sy)>cy): swin.Scroll(0,y/yunit)

    swin.Refresh()


def SetBullet(ctrl, status):
    """ Set bullet of a StaticText to indicate the status of a RowPanel """

    if status == wx.ID_NEW:
            status_char = '*'

    elif status == wx.ID_EDIT:
            status_char = '!'

    elif status == wx.ID_OPEN:
            status_char = '>'

    elif status == wx.ID_NONE:
            status_char = ''

    else:
        raise ValueError, 'ASSERTION ERROR: could not set bullet - unknown status'
    
    # Since some systems may not have a specific font, avoid an error that
    # will be disruptive.
    try:
        # params: (pointSize, family, style, weight, underline, face, encoding) 
        ctrl.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, '', wx.FONTENCODING_DEFAULT))
        ctrl.SetLabel(status_char)
    except:
        print 'Warning: could not set the label using the default font ' 



def sscanf(value, format):
    """ Retrieve formatted value from a control according to the data type"""

    is_blank = False
    ret_val = value

    if value == '': is_blank = True

    if format == ID_TYPE_INTEG:
        if value == '':
            ret_val = 0
        else:
            ret_val = int(value)

    elif format == ID_TYPE_FLOAT:
        if value == '':
            ret_val = 0.0
        else:
            ret_val = float(value)

    return ret_val, is_blank



def setupMenu(parent, menuItems, createID = True):
    """ Build Popup menu
        menuItems should be tuple, each menuItem should be list """

    isSubMenu = False
    popupID = []
    menu = wx.Menu()

    for i, items in enumerate(menuItems):
        if createID:
            popupID.append(wx.NewId())
        else:
            popupID.append(items[2])

        item = items[0]

        if item[0] == '-':
            menu.AppendSeparator()

        elif item[0] == '+' :

            if not isSubMenu:       # if first submenu item
                submenu = wx.Menu() # create submenu
                submenu.Append(popupID[i], item[1:])
                isSubMenu = True

            else:
                submenu.Append(popupID[i], item[1:])

        else:
            if isSubMenu: # if current item is title of a submenu
                menu.AppendMenu(popupID[i], item, submenu)
                isSubMenu = False

            else:
                menu.Append(popupID[i], item)

        # if callback function exists
        parent.Bind( wx.EVT_MENU, items[1], id = popupID[i] )

    if createID:
        return popupID, menu

    else:
        return menu


def GetRecordByKey(collection, key):
    """ Find an object by given key from a collection.
        This function is implemented to avoid error in index method"""

    if key not in collection.keys() :
        return None

    return collection[key]



def GetInstanceAttr(obj):
    """ Retrieve field data - name and initial value in DB object.
        Then generate a structure-like object to manipulate data of that object """

    record = Struct()
    attrs = obj.__dict__.items()
    for attr in attrs:
        if type(attr[1]) == types.FunctionType or '__'  in attr[0] : continue
        value = iif( type(attr[1]) == DB.Expr, str(attr[1]), attr[1])
        setattr( record, attr[0], value )

    return record


def BuildDbControls(panel, parent, attrs):
    """ Create controls that related to each field of an object in DB
        Not used in current version. Need more test.
    """

    for i, attr in enumerate(attrs):

        if attr[1] == 'Text':
            ctrl = Text(parent, -1, "", style = long(attr[2]))

        elif attr[1] == 'Combo':
            ctrl = Combo(parent, -1, "", style = long(attr[2]))

        elif attr[1] == 'Checkbox':
            ctrl = Checkbox(parent, -1, "", style = long(attr[2]))

        elif attr[1] == 'List':
            ctrl = List(parent, -1, "", style = long(attr[2]))

        if attr[3] != None:
            ctrl.SetValidator(KeyValidator(attr[3]))

        ctrl.sortId = i
        setattr(panel, attr[0], ctrl)


#-------------------------------------------------------------------------------#
# Functions to draw bitmap on BitmapButton. Taken from the wxPython demo files  #
#-------------------------------------------------------------------------------#
def getSmallUpArrowBitmap():
    return wx.BitmapFromImage(getSmallUpArrowImage())

def getSmallUpArrowImage():
    stream = cStringIO.StringIO(getSmallUpArrowData())
    return wx.ImageFromStream(stream)

def getSmallUpArrowData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x00<IDAT8\x8dcddbf\xa0\x040Q\xa4{h\x18\xf0\xff\xdf\xdf\xffd\x1b\x00\xd3\
\x8c\xcf\x10\x9c\x06\xa0k\xc2e\x08m\xc2\x00\x97m\xd8\xc41\x0c \x14h\xe8\xf2\
\x8c\xa3)q\x10\x18\x00\x00R\xd8#\xec\xb2\xcd\xc1Y\x00\x00\x00\x00IEND\xaeB`\
\x82'

def getSmallDnArrowBitmap():
    return wx.BitmapFromImage(getSmallDnArrowImage())

def getSmallDnArrowImage():
    stream = cStringIO.StringIO(getSmallDnArrowData())
    return wx.ImageFromStream(stream)

def getSmallDnArrowData():
    return \
"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x00HIDAT8\x8dcddbf\xa0\x040Q\xa4{\xd4\x00\x06\x06\x06\x06\x06\x16t\x81\
\xff\xff\xfe\xfe'\xa4\x89\x91\x89\x99\x11\xa7\x0b\x90%\ti\xc6j\x00>C\xb0\x89\
\xd3.\x10\xd1m\xc3\xe5*\xbc.\x80i\xc2\x17.\x8c\xa3y\x81\x01\x00\xa1\x0e\x04e\
?\x84B\xef\x00\x00\x00\x00IEND\xaeB`\x82"


def getPencilData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x02\
\xb9IDATX\x85\xc5\x97\xabn\xdc@\x14\x86?\'\x95\x02Z\xe2\x07\x08\x19\xb2\xb4\
\xd2Y\x10\xa9 Mv\xf3\n!\x05a\xce\x03\x84\xe4\x15\xfa\x08\x1e\x14P\x14VP\xe6\
\\\x0c"\x15\xe4H\x91\n\xa2\x10+\xa0\xbc(`\xc1\xee\x14\xf8\xb2\xb6w\xf6\xe6\
\xdd\xaaG2\x98\xf1\xd8\xdf?\xff93c\x07\xc1\xce.\xff3\xdem\xf3en2v\xbe\xfe`g7\
\xf8\xa7\x02J\xb0\x93\xc8{?P\xeb\xe6\x89\x086MA\t\x8f\xe3\x18\x80$I\xb8\xceB\
\x88\xf26\xf6\xbc\x14\xe1ub#\x01n2v\xf7\xf7\xf7\x00\xec\xef\xef\x03`\x8c\xc1\
Z;\x15R\x87yD\xecl\x0bn\x8c\xc1\x18C\x9a\xa6\xf4z=\x86\xc3!\xa7\xe6O\xe3\x99\
X\xa2\x99:\xe9T\x03%\xfc\xf0\xd3\xc7\xaa/M\xd3\xc6\x98^\xaf\xc7\xde\xde{N\
\x7f|\xe7:\x0b\xb1s\xde\xb5\xb6\x80r\x06\x87/\x9f\xe1\xa5\x80\xf7r1\xe9\xc3S\
5\xee\xf5\xf57\xa3\xd1\xdb\xd2\xf7\xad\x95\x027\x19\xbbG\x07\x8f\x0e4\xca/\
\x80\x0f\x17\x17\xe8\xc1\xa0\xe1\xc8h\xf4F\x96e\x18c\x08t\xde\xfc\xd7p\xa0\
\x84\xd7C,\x109\x84\xbc\xae\xf4`\xc0\xe1\xcf\x1b\xd2\x87\'\xb2,\xcb\xfbTkO\
\xcc\nY\xc9\x81Ep\xec\xb4\xa8%R\xf4`P\xb5U\xb5\x12\x02\x96\x86\x96"\x96.\xc3\
U\xe1\xf5P+\\\x86a\x05\xcf\xb2\x8c\x88|\xfe\xe5j\xb9\xb9\xbd\x0b`\x89\x03]\
\xe0\x00\x97aH\x92$P\x00}18>r\x83\xe3#7W@W\xb8\xad\xd9l\x8cAD\xf2~ \x0c\xc3\
\x99\xf1\xde"t\x93\xb1\x8bcAl+i\xab\xc0U\xa0\xe0\x88HU\x84a\x18z\x05\xcc8P\
\xc2#\x11\x90(\xbf\x8a\xd0\xf3>\xaa\xb2\x10.2\x15\xad\xaa$I\xd2\x80\xb7S\xe2\
u *lS\xc9\x0f\x94\x12\xa9(\xe2\xa9\xe4&|*p\x19\xfc\xe6\xf6.\x98[\x03%\xbc-L\
\x85\x86\x0bm\xf8e6-\xc0ep\xf0\xa4 \x8e\xfd\x16\xd7E\xcc\x83\xd7c\x158\xb4R\
\xe0&cW\x07\x00\x88\x9e\xcf\x88P\x01l>\xae\x01WHt\xb9\xed\xf5\xb67\x05U\xee=\
p\x98\xba\xd0\x86\xf7U\xd7\x82C\xcb\x81\xd2\xfey\xe02\xacj\x81\xdd\x0c\x0e\
\xb5\xad\xb8\xfe\xa1\xe0\x1e\xfd\xdfv%\x1c\x8aMI6\x83C\xcb\x81\xab\xabo<?\
\xff"\xe8\x7f\xf5\n\xa9\xe0ZX\xbf!\xbc!`8\x1crv\xf6\x85 \x98\x1dok\xc7\x98\
\xa8\x16U\xb89\xbc\x12\xe0&c\'"\x9c\x9c\x9c4n\x06}\xdbX\x96\xa2J\xdf\x02,\
\xde^W\x85W\x02`\xbam\xb6Cl>\xd32\xdaP\xdfi\xb7*\x1c\x8a"\x9c\xf7G\xb3\x0e\
\xb4\x0b\x1c\x16|\x92\xad\x03\xed\n\xaf\x04\xf8\xfeXDd\xa1+\xdb\x80W\x02\xba\
FWhg\x01\xdb\x00\xb6\xe3/\xda\xb1\x84\x8dh\xb0\xbb\xe2\x00\x00\x00\x00IEND\
\xaeB`\x82'

def getPencilBitmap():
    return wx.BitmapFromImage(getPencilImage())

def getPencilImage():
    stream = cStringIO.StringIO(getPencilData())
    return wx.ImageFromStream(stream)

def getcustomData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x03\x04IDAT8\x8d\xa5\x93QlSu\x14\xc6\x7f\xff{o[z;\xdb\xb5u\xb3c\xe2,\
\x1bA\x18f\xba,\x8bq\xa2\xa8K\xc0\x8c0\rq1D\xb2\xc0\x03\x12\x8d\t1&D\x91\xf8\
`p\xb8DM \x91\xcd,\xf20%5\xfa\x02\xc1\xc0F@\x078p"n\x9a9\x9c\xba\xe9`\x16J\
\xdbu\xdd\xed\xbdw\xb7\xed\xbd>\x98,@\x16_<o\xe7<\xfc\xf2}\xe7|G8\x8e\xc3\
\xff)\xe5\xce\xc1+\x8de{\xab\xc3\xf6nY\xb6}V\xd1a\xce\x92\xf4\x89Y\xe5\xc3O/\
%\xdeZ\x0c nU\xb0\xb3!\xbc\xbb\xae\xd2\xe9p\xa9B\xd8\x80\x95w\xd0\x0c\x9b\
\x84\xe68\xe3\x19\xd7;\xc7G\x92o\xdf\t\x90nm\x1e\x8a\x14\xf7{U!f\xb2E\xd2sE4\
\x13l\xc9\x8d"+"\xe8*\xecZL\xc1m\x80\xcc\\\x91\x8a\'^f\xcb\xab{x\xf2\xb9\xed\
\xc4s\n)SAWJQ\x97H\xde\xde76y\xfe\xd3BO\xfb\xfd\xa9\x17;\xfbC\xd6\x1fg\xd0t\
\x83dz\x16\x7f\x89J`u3}\xef\xb5e\x1b\xd7\x87v\xe4\xf5\xea\x98\\\xf2 \xb9\xe4\
\x00\xc2\x9cn\xbfm\x89F\xd17fL\xfd\xd0T\xf0\xdcM\xd0W X\xb6\x14\xad Cz\x9c\
\xd2{])5\xf0T\xcc[\xbd\x96@\xf4a2\x93+\xb9\xd2\xdf\xd3\xb9`!\xb2\xf1\x88\xeb\
\xe0_\xeb&\xfaz?\xc0\xcf,BY\x82P<\x94\xc8\x16#\xa7;hhm\xab\n\xadh\xc2H\x8fa\
\xfc\xf9\x1dw\xf9#\x94\x84\xef\x0b\x08\xc7q(o\x89yl\xbb\xb8\xddK\xe4\xa3\x93\
\x1f?\xc2h\xf7\x16\x1c\xfe\xb5\x16\n\xe6h\xd8\xd0D`\xf9z\xe6\xe31\x8c\x94 \
\xf1\xabN\xde\xb4R\xa6\xa1=*\xc2\xcf|.\xac"\xed!w\xe5\xe1\x13]\xf5\\\xc6\xcb\
\xe5\x0c\x189X\x96\xfd\x86\x9d\x91~\x025\x9b0\xa7\xbb\x90\xdc\x05\xf2Z\x15\
\xa9s\x837\xd2\x9a\xb2\xa1\xfe\xb5S\xc3JD\xcd\xb5V\x88\xe4\xe1\x97^\xdf\xcc\
\xd9\x94\xcc\xa8\xee\x907!r\xfd\x18\xdbj.\x10\xa8y\x16s\xfa\x10\x92\xab\x80\
\x95\x8dr\xf5\xf4\xf7|2\xfa@\xd7\xfb\xdd\x87\x86\x01\xa4\xdeU\x9d_\x1eiOs\
\xe3\x97\x13\\\xfc\x1b\xf4\x19A\xd9\xb5\xaf\xd8\x1c\x1c\xa4\xbc\xb6\x05\xebz\
\x0f\xb2\xdba>[E|\xe0\x12\xe5\xd1:\x9e\xf7\x0f\xbc\xb9\x90\x03Y\x08I\xf1\xa8\
\x9c\xbf\x98\xa4F\xd1\t\xfe\x1e\xe3\x85\xf0\x05lg)\xf1\x9f\x0fbc\x92KW2u\xee\
\n\xfb~l\xc5\xa5\xfa\x91e\xb1p=IZ\xd1\xbcg\xf2\xeb\xde\x827\x1f/\x1c\xfdl\
\x88F\xa3\x87\xd5\x8f\xed\xc0s\xf5<\xe3G\xbfe\xb8/\xcd\xd0\xc9\x11v\x9di\xa1\
\x94k\xfa\xe4\xd9/\xe6\xbd\xb5O\xef[\x00\xac\xd9z\xa0#T\xd7\x1cZVaGnf\xb4\
\xee\xb1\xdf\x12X\xa3\xc7\x89\xd6\xad\xc5\xe7[\xc9\xe4\xd08\xef\x0e\xac\x9b\
\x99\xca\x97\x9f\x92Uw4\\\xdbT\xb6f\xeb\x81\xbd\x8b&\x11\xa0\xed\xf1\x90Q\
\xbf\xfc\x1e\xa5qU\x14\xc75?h$nn\xdb\xb8\xff\xa7\x89\xc5\xfe\x00\xe0\x1f\x95\
A?\x1bMjg[\x00\x00\x00\x00IEND\xaeB`\x82'

def getcustomBitmap():
    return wx.BitmapFromImage(getcustomImage())

def getcustomImage():
    stream = cStringIO.StringIO(getcustomData())
    return wx.ImageFromStream(stream)


#------------------------------------------------------------------------------#
#           Messaging methods                                                  #
#------------------------------------------------------------------------------#


def dlgTextEntry(Message = None, Caption=None, DefaultValue=None, Parent = None):
    """ General simple dialog to display a message or to get a response from user """
    if Message == None:
        Message = ''
    if Caption == None:
        Caption = ''
    if DefaultValue == None:
        DefaultValue = ''
    dlg = wx.TextEntryDialog(Parent, Message, Caption, DefaultValue, wx.TE_MULTILINE|wx.OK|wx.CANCEL)
    dlg.CenterOnScreen()
    dlg.ShowModal()
    TheText = dlg.GetValue()
    dlg.Destroy()
    return TheText


def dlgSimpleMsg(title, msg, btn=wx.OK, icon=wx.ICON_ERROR, Parent = None):
    """ General simple dialog to display a message or to get a response from user """
    dlg = wx.MessageDialog(Parent, msg, title, btn | icon)
    ans = dlg.ShowModal()
    dlg.Destroy()

    return ans


def dlgNotPrepared():
    """ Simple dialog for unimplemented functions. will be removed """
    dlgSimpleMsg("INFO", "This function is under development", wx.OK, wx.ICON_INFORMATION)


def dlgErrorMsg(level=0, yesno=False, msg_prefix = None, Parent = None):
    (type, value, traceback) = sys.exc_info()
    # Level 0 shows only the error message, without the type
    if level == 0: 
        msg = '%s\n' % ( value )

    # Level 1 shows the error type
    elif level == 1:
        msg = '%s : %s\n' % (type.__name__, value )

    # Level 2 and above shows the entire traceback
    elif level >= 2: # pull out information about the exception
        frame = traceback.tb_frame
        code = traceback.tb_frame.f_code
        msg = '%s : %s\n\nFile : %s\nMethod name : %s\nLine No : %s\n' %  \
                (type.__name__, value, code.co_filename, code.co_name, frame.f_lineno )

    if msg_prefix != None:
        msg = msg_prefix + msg
    if yesno:
        msg += '\n Do you want to continue working on this form? \n Answering "Yes" will keep this form open \n Answering "No", will close this form and discard the last change'


    button = iif( yesno, wx.YES_NO, wx.OK )
    answer = dlgSimpleMsg('ERROR', msg, button, wx.ICON_ERROR, Parent)

    return answer


class dlgFind(wx.Dialog):
    """ Dialog to search string  """
    def __init__(self, target=None, prev_ctrl=None, *args, **kwds):
        """ Constructor of dlgFind class """

        # initialize varibales for search
        self.__found = []       # list to save the controls found
        self.__idx_row = 0      # current cursor position in a panel
        self.__idx_col = 0      # current position of the panel and control
        self.__target = target  # search target ( scrolled window in a frame )
        self.__panels = [ panel.Id for panel in target.GetChildren() ] # list of row panel id in scroll window of a CDMFrame object
        self.__prev_ctrl = prev_ctrl # save current control in a frame for focusing after closing the Find dialog


        kwdsnew = copy.copy(kwds)
        kwdsnew["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwdsnew)
        self.label_1 = wx.StaticText(self, -1, "Find what:")
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "")
        #self.checkbox_1 = wx.CheckBox(self, -1, "Match whole word only") # reserved for future extension
        self.checkbox_2 = wx.CheckBox(self, -1, "Match case")
        self.button_1 = wx.Button(self, -1, "Find Next")
        self.button_2 = wx.Button(self, -1, "Find Prev")
        #self.button_3 = wx.Button(self, -1, "Find All")    # Find All option. Reserved for future extension
        self.button_4 = wx.Button(self, -1, "Close")

        self.__set_properties()
        self.__do_layout()

        # bind event handlers
        self.Bind(wx.EVT_TEXT, self.OnKeyIn, self.text_ctrl_1)
        self.Bind(wx.EVT_BUTTON, self.OnFindNext, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.OnFindPrev, self.button_2)
        #self.Bind(wx.EVT_BUTTON, self.OnFindAll, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.button_4)
        # end wxGlade



    def __set_properties(self):
        """ Set properties of panel and controls """
        self.SetTitle("Find")
        self.SetSize((400, 165))
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))
        self.label_1.SetMinSize((100, 13))
        self.text_ctrl_1.SetMinSize((200, 21))
        self.button_1.Enable(False)
        self.button_2.Enable(False)
        #self.button_3.Enable(False)  --> Match Whole Word option. Reserved for future use


    def __do_layout(self):
        """ Set position of each control """

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add((20, 10), 0, 0, 0)
        sizer_4.Add(self.label_1, 0, wx.ALL, 3)
        sizer_4.Add(self.text_ctrl_1, 0, wx.ALL, 3)
        sizer_3.Add(sizer_4, 0, wx.EXPAND, 0)
        #sizer_3.Add(self.checkbox_1, 0, wx.ALL, 3)
        sizer_3.Add((20, 10), 0, 0, 0)
        sizer_3.Add(self.checkbox_2, 0, wx.ALL, 3)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_5.Add(self.button_1, 0, wx.ALL, 3)
        sizer_5.Add(self.button_2, 0, wx.ALL, 3)
        #sizer_5.Add(self.button_3, 0, wx.ALL, 3)
        sizer_5.Add(self.button_4, 0, wx.ALL, 3)
        sizer_2.Add(sizer_5, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade


    def OnKeyIn(self, event):
        """ Check the key stroke in the text control to activate/deactivate buttons"""
        ctrl = event.GetEventObject()
        value = ctrl.GetValue()
        if value <> '':
            self.button_1.Enable(True)
            self.button_2.Enable(True)
            #self.button_3.Enable(True)
        else:
            self.button_1.Enable(False)
            self.button_2.Enable(False)
            #self.button_3.Enable(False)

        event.Skip()


    def OnFindAll(self, event): # ---> Currently not used. Implemented for future extension
        """ Set Search direction as FORWARD from first panel """
        self.SearchText(wx.ID_SELECTALL)


    def OnFindNext(self, event):
        """ Set Search direction as FORWARD from current panel """
        self.SearchText(wx.ID_FORWARD)


    def OnFindPrev(self, event):
        """ Set Search direction as BACKWARD from current panel """
        self.SearchText(wx.ID_BACKWARD)


    def SearchText(self, findDir):
        """ Do search """

        find_str = str(self.text_ctrl_1.GetValue())

        if not self.checkbox_2.GetValue():     # if match case option is not set
            find_str = find_str.lower()

        if findDir == wx.ID_BACKWARD:           # set panel id range according to the search direction
            find_range = range(self.__idx_row, -1, -1)

        elif findDir == wx.ID_FORWARD:
            find_range = range(self.__idx_row, len(self.__panels))

        else:
            self.__idx_row = 0
            find_range = range(self.__idx_row, len(self.__panels))


        for id in find_range:

            panel = self.__target.FindWindowById(self.__panels[id])
            ctrls = list(panel.GetChildren())
            idcs = range(0, len(ctrls))

            if findDir == wx.ID_BACKWARD:
                ctrls.reverse()
                idcs.reverse()

            for idc, ctrl in zip(idcs, ctrls):
                type_ctrl = type(ctrl)
                if      (findDir == wx.ID_FORWARD and
                        panel.Id == self.__panels[self.__idx_row] and idc <= self.__idx_col ) \
                    or  (findDir == wx.ID_BACKWARD and
                        panel.Id == self.__panels[self.__idx_row] and self.__idx_col <= idc ) \
                    or  not type_ctrl in [Text, Combo]:

                    continue


                value = ctrl.GetValueString()
                if value == '' : continue

                if not self.checkbox_2.GetValue() : # if not match case
                    value = value.lower()

                if not find_str in value: continue

                if type_ctrl == Combo:  ctrl = ctrl.GetTextCtrl()

                ctrl.SetFocus()
                idx = value.index(find_str)
                ctrl.SetSelection(idx, idx+len(find_str))

                if findDir == wx.ID_SELECTALL:
                    if not ctrl in self.__found: self.__found.append(ctrl)
                    continue


                scrollPanel(self.__target, panel)  # scroll if found item is not seen on screen

                self.__idx_row = id
                self.__idx_col = idc
                self.__found.append(ctrl)

                # remove previous control from list
                # turn the highlighted text back to normal text
                if len(self.__found) > 1 :
                    self.__found[-2].SetSelection(0,0)
                    self.__found.pop(-2)

                if findDir != wx.ID_SELECTALL : return

        # When user meet below message, the highlighted text turns back to normal text automatically
        # Since I couldn't find a method to set the property of TextCtrl in Combo control,
        # it should be treated later on.
        if findDir <> wx.ID_SELECTALL :
            dlgSimpleMsg("INFO", "'" + find_str + "' not found", wx.OK, wx.ICON_INFORMATION, Parent = self)

        else:
            dlgSimpleMsg("INFO", "Search ended", wx.OK, wx.ICON_INFORMATION, Parent = self)



    def ClearFoundItems(self):
        """ Clear the found item list """
        for ctrl in self.__found:
            ctrl.SetSelection(0,0)

        self._found = []


    def OnClose(self, event):
        """ Close dialog  """

        self.Destroy()

# end of class dlgFind


class WorkerThread:
    """ Encapsulates a function with a worker thread """
    FunctionToRun = None
    FunctionToRunAtTheEnd = None
    ThreadId = None
    ThreadIsRunning = None
    ErrorDetected = None
    ProcessStop = False
    RunThreadAsProcess = False
    ProcessList = None
    PipeList = None
    Done = False

    def __init__(self, FunctionToRun, FunctionToRunAtTheEnd, RunThreadAsProcess = False):
        "Run the function and create a loop"
        self.ThreadId = None
        self.ErrorDetected = None
        self.FunctionToRun = FunctionToRun
        self.FunctionToRunAtTheEnd = FunctionToRunAtTheEnd
        self.ProcessList = None
        self.PipeList = None
        self.ProcessStop = False
        self.Done = False
        if DB.SystemSupportsProcesses:
            # if the system supports processes, run a process
            (ProcessList, PipeList) = self.EncapsulatingFunction()
        else:
            # else if the system does not support processes, run a thread
            self.ThreadIsRunning = thread.allocate_lock()
            self.ThreadId = thread.start_new_thread(self.EncapsulatingFunction, ())
            # Wait until thread starts and gets the lock
            while not self.ThreadIsRunning.locked() and self.ThreadId != None:
                wx.Yield()

    def StopProcess(self):
        "Can be used to stop the process nicely"
        if DB.SystemSupportsProcesses:
            # stop the process
            NumberOfProcesses = len(self.PipeList)
            for Enum in range(NumberOfProcesses):
                ThePipe = self.PipeList[Enum]
                TheProcess = self.ProcessList[Enum]
                self.ProcessStop = True
                if TheProcess != None and TheProcess.is_alive():
                    # terminate the pipe first
                    ThePipe.close()
                    # now termiate the process
                    TheProcess.terminate()
        else:
            # since python threads can not be stopped then just wait
            # until their end. If a future implementation allows 
            # stopping threads, this should be entered here
            self.WaitForJob()

            
    def AreResultsReady(self):
        "Checks if all results are ready"
        if DB.SystemSupportsProcesses:
            # if the system supports processes, run a process
            NumberOfProcesses = ((self.PipeList != None)+0) and len(self.PipeList)
            AllResultsReady = True
            for Enum in range(NumberOfProcesses):
                ThePipe = self.PipeList[Enum]
                TheProcess = self.ProcessList[Enum]
                # If a process is not alive, it is assumed it gave its
                # results. This will avoid hanging forever in case of
                # an error. Also is self.ProcessStop is raised, this means
                # it is time to exit this loop
                try:
                    AllResultsReady = self.ProcessStop or AllResultsReady and (ThePipe.poll() or not TheProcess.is_alive())
                except:
                    # if an error was raised report that results are ready
                    # this may happen if the process is stopped by the user 
                    # just before polling it
                    AllResultsReady = True
        else:
            # else if the system does not support processes, run a thread
            AllResultsReady = not self.ThreadIsRunning.locked()
        return AllResultsReady

    def WaitForJob(self):
        "Do nothing while the thread/process is done, then return its result"
        while not self.AreResultsReady():
            wx.Yield()
        # now collect the results to return
        TheValueToReturn = self.GetReturnValue()
        # Mark that waiting and collecting results is done. This also means
        # that process/thread has finished and there is no need to terminate
        # it again upon destruction
        self.Done = True
        return TheValueToReturn
    
    def EncapsulatingFunction(self):
        "This method encapsulates the function and creates locks"
        if not DB.SystemSupportsProcesses:
            self.ThreadIsRunning.acquire()
        # This actually runs the function passed
        try:
            (ProcessList, PipeList) = self.FunctionToRun()
            self.ProcessList = ProcessList
            self.PipeList = PipeList            
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            self.ErrorDetected = (ExceptType, ExceptValue)
            (ProcessList, PipeList) = (None, None)
        if not DB.SystemSupportsProcesses:
            self.ThreadIsRunning.release()
            # The thread no longer exists so reset the threadid
            self.ThreadId = None
        return (ProcessList, PipeList)


    def GetReturnValue(self):
        "returns the result stored after running the thread/process"
        # Return None if the thread/process is running or if it was stopped
        # In case of an error the result will be None and the error will be
        # raised again. Note that the error is contained until the value is
        # requested back.
        if not self.AreResultsReady() or self.ProcessStop:
            return None
        else:
            if self.ErrorDetected != None:
                raise self.ErrorDetected[0], self.ErrorDetected[1]
        # Finaly this means results are ready. Collect the results to return
        RetVal = self.FunctionToRunAtTheEnd(self.ProcessList,self.PipeList)
        # return the results
        return RetVal
        
    def __del__(self):
        "the destructor makes sure no processes are running"
        if not self.Done:
            # If something is still running than wait
            self.StopProcess()


#---------------------------------------------------------------------------#
#       This class handles a progress dialog box that shows time elapsed    #
#       it uses a timer                                                     #
#---------------------------------------------------------------------------#
class ProgressDialogTimeElapsed(wx.ProgressDialog):
    """ Dialog to Progress and time elapsed """
    TimerObject = None
    PreviousCursor = None
    WindowAlreadyDestroyed = False
    Parent = None
    WasCanceled = False
    FunctionToRunUponCancel = None

    def __init__(self, Title=None, Message=None, Maximum = 100, Parent = None, ShowBusyCursor = True, UpdateTimeStepInMiliSeconds = 100 , StartTimerUponCreation = True, AllowCancel = False):
        " Constructor also starts the time and shows the dialog "
        self.WindowAlreadyDestroyed = False
        if Title == None:
            Title = 'System is Working'
        if Message == None:
            Message = 'Please Wait'
        self.TimerObject = None
        self.PreviousCursor = None
        self.Parent = Parent
        self.WasCanceled = False
        self.FunctionToRunUponCancel = None
        try:
            StyleToUse = wx.PD_ELAPSED_TIME | wx.PD_APP_MODAL
            if AllowCancel:
                StyleToUse = StyleToUse | wx.PD_CAN_ABORT
            wx.GenericProgressDialog.__init__(self, title = Title, message = Message, maximum = Maximum, parent = Parent, style = StyleToUse ) 
            # Timer is initiated and bound
            if StartTimerUponCreation:
                self.StartTimer(UpdateTimeStepInMiliSeconds)
            if ShowBusyCursor:
                self.PreviousCursor = self.GetCursor()
                self.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
        except:
            self.TimerObject = None
            self.PreviousCursor = None

    def StartTimer(self, UpdateTimeStepInMiliSeconds = 100):
        "Starts the timer"
        self.TimerObject = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.UpdateByTimer, self.TimerObject)
        RetVal = self.TimerObject.Start(UpdateTimeStepInMiliSeconds)
        return RetVal


    def UpdateByTimer(self, Event):
        " Updates the dialog and is called for each timer tick event "
        (DidNotCancel, DidNotSkip) = self.Pulse()
        if not DidNotCancel:
            self.WasCanceled = True
            if self.FunctionToRunUponCancel != None:
                # if a function to call upon cancel is defined, and the
                # process was canceled, call this function
                self.FunctionToRunUponCancel()

    def Destroy(self):
        " Stops the timer and destroys the Dialog Box "
        RetVal = None
        if self.PreviousCursor != None :
            self.SetCursor(self.PreviousCursor)
            self.PreviousCursor = None
        if self.TimerObject != None:
            self.TimerObject.Stop()
            self.Unbind(wx.EVT_TIMER)
            self.TimerObject = None
            RetVal = wx.GenericProgressDialog.Destroy(self)
            if self.Parent != None:
                self.Parent.Raise()
        return RetVal            



#---------------------------------------------------------------------------#
#       Sort panels according to the button pressed                         #
#       The sort order is displayed in front of the button label            #
#---------------------------------------------------------------------------#
def SortPanels(scwin, this_btn, keys=None):
    """ Sort RowPanel object according to key value"""
    if this_btn.sortId < 0: return

    btnwin = this_btn.GetParent()

    # check current order
    order = this_btn.Order #Get order of theis button
    is_sorted = iif( order != wx.ID_NONE, True, False )

    # set new order
    if order == wx.ID_NONE: # if no order -> ascending
        order = wx.ID_UP

    elif order == wx.ID_UP: # if ascending -> descending
        order = wx.ID_DOWN

    else : # if descending, use original order
        order = wx.ID_NONE

    # sort StudyModel object list according to the attribute(i.e. key)
    if order != wx.ID_NONE:

        sortId = this_btn.sortId #this_btn.GetSortId()
        sorted_list, no_blank = [], 0
        for i, panel in enumerate(scwin.GetChildren()):
            for ctrl in panel.GetChildren():
                if not type(ctrl) in [Text, Combo, Checkbox] or ctrl.sortId != sortId:
                    continue

                if type(ctrl) == Checkbox:
                    value = ctrl.GetValue()
                    sorted_list.append((value, panel.Id))
                else:
                    value = ctrl.GetValueString()
                    if value == '': no_blank += 1

                    sorted_list.append((value + '-' + str(i), panel.Id))
                break

        # if all fields are blank, return
        if no_blank == len(sorted_list): return

        sorted_list.sort()
        sorted_list = [ x[1] for x in sorted_list ]
        if order == wx.ID_DOWN: sorted_list.reverse()

    else:
        sorted_list = [ panel.Id for panel in scwin.GetChildren()]
        if 0 in sorted_list:
            sorted_list.remove(0)
            sorted_list.sort()
            sorted_list.append(0)
        else:
            sorted_list.sort()

    if not is_sorted:                       # if current button is not sorted previously
        for btn in btnwin.GetChildren():    # look for a button already sorted
            if type(btn) == BitmapButton and btn.Order != wx.ID_NONE:
                btn.SetBullet(wx.ID_NONE)
                btn.SetOrder(wx.ID_NONE)
                break

    this_btn.Order = order      # Set current order of the button
    this_btn.SetBullet(order)   # display bullet and button label

    # detach panels from sizer to re-arrange using sorted list
    sizer = scwin.GetSizer()
    for panel in scwin.GetChildren():
        sizer.Detach(panel)

    # arrange panel using panel Id in sorted list
    for id in sorted_list:
        panel = scwin.FindWindowById(id)
        sizer.Add(panel, 0, wx.ALL, 1)

    scwin.Layout()
    scwin.Refresh()



#---------------------------------------------------------------------------#
#       Some functions to build and handle basic menu structures            #
#---------------------------------------------------------------------------#


def GenerateStandardMenu (self, SkipItems = None):
    "Generates a standard menu bar with bindings"
    if SkipItems == None:
        SkipItems = []
    # Build the menu
    # Menu Bar
    self.menubar = wx.MenuBar()
    self.SetMenuBar(self.menubar)
    # File Menu
    self.MenuBarFile = wx.Menu()# Create 'File' menu
    # Add File menu items
    if ID_MENU_REPORT_THIS not in SkipItems:
        self.MenuItemReportThis = wx.MenuItem(self.MenuBarFile, ID_MENU_REPORT_THIS, "Sing&le Report", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemReportThis)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemReportThis)
    if ID_MENU_REPORT_ALL not in SkipItems:
        self.MenuItemReportAll = wx.MenuItem(self.MenuBarFile, ID_MENU_REPORT_ALL, "&Report All", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemReportAll)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemReportAll)
    self.MenuBarFile.AppendSeparator()
    if wx.ID_CLOSE not in SkipItems:
        self.MenuItemClose = wx.MenuItem(self.MenuBarFile, wx.ID_CLOSE, "&Close", "", wx.ITEM_NORMAL)
        self.MenuBarFile.AppendItem(self.MenuItemClose)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemClose)
    self.menubar.Append(self.MenuBarFile, "&File")
    # Help Menu
    self.MenuBarHelp = wx.Menu()
    # Add Help menu items
    if ID_MENU_HELP not in SkipItems:
        self.MenuItemHelp = wx.MenuItem(self.MenuBarHelp, ID_MENU_HELP, "&Help", "", wx.ITEM_NORMAL)
        self.MenuBarHelp.AppendItem(self.MenuItemHelp)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemHelp)
    if ID_MENU_HELP_GENERAL not in SkipItems:
        self.MenuItemHelpGeneral = wx.MenuItem(self.MenuBarHelp, ID_MENU_HELP_GENERAL, "&General Help", "", wx.ITEM_NORMAL)
        self.MenuBarHelp.AppendItem(self.MenuItemHelpGeneral)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemHelpGeneral)
    self.MenuBarFile.AppendSeparator()
    if ID_MENU_ABOUT not in SkipItems:
        self.MenuItemAbout = wx.MenuItem(self.MenuBarHelp, ID_MENU_ABOUT, "&About", "", wx.ITEM_NORMAL)
        self.MenuBarHelp.AppendItem(self.MenuItemAbout)
        self.Bind(wx.EVT_MENU,  self.OnMenuSelected, self.MenuItemAbout)
    self.menubar.Append(self.MenuBarHelp, "&Help")
    # Menu Bar end
    return



def OnMenuSelected(self, event=None):
    " Handles Menu selection and returns True if was handled "
    if event == None:
        return True
    MenuID = event.GetId()
    if MenuID == wx.ID_CLOSE:
        # If close was requested by the menu, then cause a close event to be sent 
        # to the raising window. Note that this does not call the window closing
        self.Close()
        return True
    elif MenuID == ID_MENU_REPORT_THIS:
        # Get the collection information behind the form
        CollectionName = self.Collection
        CollectionObject = getattr(DB,CollectionName,None)
        if CollectionObject != None:
            # Now find the active panel information for the form
            ActivePanel = self.GetCurrTarget('obj', 'panel')
            # If this is a valid panel and not a new one
            if ActivePanel != None and ActivePanel.Id != 0:
                # Get the record ID for this panel
                RecordKey = ActivePanel.Key
                OpenForm("ReportViewer",self,key=(CollectionObject[RecordKey],None))
        return True
    elif MenuID == ID_MENU_REPORT_ALL:
        # Get the collection information behind the form
        KeysToReport = None
        if 'ReturnDisplayedRecordKeys' in dir(self):
            KeysToReport = self.ReturnDisplayedRecordKeys()
        CollectionName = self.Collection
        CollectionObject = getattr(DB,CollectionName,None)
        if CollectionObject != None:
            OpenForm("ReportViewer",self,key=(CollectionObject,[('KeyFilter',KeysToReport)]))
        return True
    elif MenuID == ID_MENU_HELP:
        HelpNodeNameToUse = None
        if 'HelpContext' in dir(self):
            HelpNodeNameToUse = self.HelpContext
        HelpClass.openDoc(node = HelpNodeNameToUse)
        return True
    elif MenuID == ID_MENU_HELP_GENERAL:
        HelpClass.openDoc()
        return True
    elif MenuID == ID_MENU_ABOUT:
        OpenAbout(self)
        return True
    return False

# Create an instance for documentation
HelpClass = HelpInterface.Documentation()


