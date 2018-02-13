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
# Initially developed by Deanna Isaman, Jacob Barhak, Morton Brown, Wen Ye
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
###############################################################################

from __future__ import division
import nose
import DataDef as DB
import math
import sys
import os
import pickle
import subprocess
import datetime
import base64
import csv
import MultiRunSimulation
import MultiRunSimulationStatisticsAsCSV
import MultiRunCombinedReport
import MultiRunExportResultsAsCSV
import ConvertDataToCode
import CreatePlotsFromCSV
import AssembleReportCSV

# Simulation constants
GlobalAllowedDeviationInSTD = 3
MaxSimulationRepetitions = 2
TestLoadOlderFiles = True
TestSupportingScripts = True


def BeepSound(NumberOfBeepForErrors):
    try:
        import Tkinter
        TopLevelWindow = Tkinter.Tk()
        for i in range(NumberOfBeepForErrors):
            TopLevelWindow.bell()
        TopLevelWindow.destroy()
    except:
        for i in range(NumberOfBeepForErrors):
            print '\aBEEP!!!\n'
            

def RandomSeedFunc(SimRepetition):
    """ Change this function to Determine the random seed in each iteration """
    # uncomment to return repetition, otherwise return none
    # return SimRepetition
    return None

# Define the Validation Test Error Counter
GeneralErrorCounter = 0

def BeepForError(NumberOfBeepForErrors = 5, IncreaseErrorCount = False):
    global GeneralErrorCounter
    if IncreaseErrorCount:
        GeneralErrorCounter = GeneralErrorCounter + 1
    BeepSound(NumberOfBeepForErrors)

        

def CheckException(ExceptionInString, ErrorMessageForUser):
    """The function is used to check an exception for a specific string"""
    (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
    MessageToPrint = ErrorMessageForUser + '. Here is the exception: ' + str(ExceptValue)
    if ExceptionInString == None:
        # In case no error was expected, raise an error
        assert False, MessageToPrint
    elif ExceptionInString in str(ExceptValue):
        # in case a specific error was expected print a message
        print MessageToPrint
    else:
        #  If the an error other than expected happens - this is a test issue
        assert False, '*** Bug in test - different error than expected ***. Was expecting to print the following message: "' + ErrorMessageForUser + '" . Actual Error was: ' + str(ExceptValue)
    


def SetupEmptyDB(self):
    " define empty database environment "
    print 'Test Setup Empty Environment'
    # use this method as an override when a full setup is not needed
    DB.CreateBlankDataDefinitions()

def SetupFullDB():
    " define full database environment "
    print 'Test Setup'

    # Define Common Covariates
    DB.Params.AddNew(DB.Param(Name = 'Age', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Official oldest person was 122 at death by Wikipedia'), ProjectBypassID = 0)
    DB.Params.AddNew(DB.Param(Name = 'Gender', Formula = '' , ParameterType = 'Integer' , ValidationRuleParams = '[0,1]', Notes = 'Male = 1, Female = 0'), ProjectBypassID = 0)
    DB.Params.AddNew(DB.Param(Name = 'BP', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,Inf]', Notes = 'Blood Pressure'), ProjectBypassID = 0)
    DB.Params.AddNew(DB.Param(Name = 'Smoke', Formula = '' , ParameterType = 'Integer' , ValidationRuleParams = '[0,1]', Notes = 'Smoking Status'), ProjectBypassID = 0)
    DB.Params.AddNew(DB.Param(Name = 'AF', Formula = '' , ParameterType = 'Integer' , ValidationRuleParams = '[0,1]', Notes = 'Atrial fibrillation'), ProjectBypassID = 0)
    
    ###############################################################################
    
    # Simulation Project - Example 1
    
    # Define Parameters
    # Define States
    DB.States.AddNew(DB.State(ID = 10021 , Name = 'Alive' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 1000002 , Name = 'Dead' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 1000000 , Name = 'Example 1 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 10021 , 1000002 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 1000000 , Name = 'Simulation Example 1: Simple Example' , Notes = '' , DerivedFrom = 0 , MainProcess = 1000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 1000000, FromState = 10021, ToState = 1000002, Probability = DB.Expr('0.0717')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1010, Name='Population set for Simulation Example 1', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','') ,('Alive',''), ('Dead','')] , Data = [[ 30, 1, 0 ]]*9 + [[30,0,1]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1010, Name = 'Simulation Project - Test Example 1' , Notes = 'Simple Example',  PrimaryModelID = 1000000  , PrimaryPopulationSetID = 1010 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 2
    
    # Define Parameters
    # Define States
    DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200001 , Name = 'State1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200092 , Name = 'State2Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 2000000 , Name = 'Example 2 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200001, 2200092 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 2000000 , Name = 'Simulation Example 2: Multiple Transitions in a Chain' , Notes = '' , DerivedFrom = 0 , MainProcess = 2000000  ), ProjectBypassID = 0)
    
    
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 2000000, FromState = 2200000, ToState = 2200001, Probability = DB.Expr('0.1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 2000000, FromState = 2200001, ToState = 2200092, Probability = DB.Expr('0.2')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1020, Name='Population set for Simulation Example 2', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','') ,('State0',''), ('State1',''), ('State2Terminal','')] , Data = [[ 30, 1, 0,0 ]] + [[30, 0 ,1,0]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1020, Name = 'Simulation Project - Test Example 2' , Notes = 'Multiple Transitions in a Chain',  PrimaryModelID = 2000000  , PrimaryPopulationSetID = 1020 , NumberOfSimulationSteps = 5  , NumberOfRepetitions = 500  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 3
    
    # Define Parameters
    # Define States
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200091 , Name = 'State1Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200092 , Name = 'State2Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 3000000 , Name = 'Example 3 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200091, 2200092 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 3000000 , Name = 'Simulation Example 3:  A fork state' , Notes = '' , DerivedFrom = 0 , MainProcess = 3000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 3000000, FromState = 2200000, ToState = 2200091, Probability = DB.Expr('0.3')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 3000000, FromState = 2200000, ToState = 2200092, Probability = DB.Expr('0.6')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1030, Name='Population set for Simulation Example 3', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','') ,('State0',''), ('State1Terminal',''), ('State2Terminal','')] , Data = [[ 30, 1, 0,0 ]], Objectives = [] ), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1030, Name = 'Simulation Project - Test Example 3' , Notes = 'A fork state',  PrimaryModelID = 3000000  , PrimaryPopulationSetID = 1030 , NumberOfSimulationSteps = 2  , NumberOfRepetitions = 1000  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 4
    
    # Define Parameters
    # Define States
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200001 , Name = 'State1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200002 , Name = 'State2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200088 , Name = 'DummyStartEvent' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = True , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 4000000 , Name = 'Example 4 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200001, 2200002, 2200088 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 4000000 , Name = 'Simulation Example 4:  Funny Loop Example' , Notes = '' , DerivedFrom = 0 , MainProcess = 4000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 4000000, FromState = 2200000, ToState = 2200001, Probability = DB.Expr('0.1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 4000000, FromState = 2200001, ToState = 2200002, Probability = DB.Expr('0.2')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 4000000, FromState = 2200002, ToState = 2200000, Probability = DB.Expr('0.3')), ProjectBypassID = 0)
    # Dummy Start
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 4000000, FromState = 2200088, ToState = 2200000, Probability = DB.Expr('1')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1040, Name='Population set for Simulation Example 4', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','') ,('State0',''), ('State1',''), ('State2','')] , Data = [[ 30, 1, 0, 0 ], [ 40, 0, 1, 0 ] , [ 30, 0, 0, 1 ]], Objectives = [] ), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1040, Name = 'Simulation Project - Test Example 4' , Notes = 'Funny Loop Example',  PrimaryModelID = 4000000  , PrimaryPopulationSetID = 1040 , NumberOfSimulationSteps = 5  , NumberOfRepetitions = 500  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 5a
    
    # Define Parameters
    # Define States
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200001 , Name = 'State1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200092 , Name = 'State2Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 51000000 , Name = 'Example 5a : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200001, 2200092 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 51000000 , Name = 'Simulation Example 5a: Multiple Transitions in a Chain with an Expression and Boolean Covariate' , Notes = '' , DerivedFrom = 0 , MainProcess = 51000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 51000000, FromState = 2200000, ToState = 2200001, Probability = DB.Expr('Exp(-(0.4+0.3*Gender))')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 51000000, FromState = 2200001, ToState = 2200092, Probability = DB.Expr('Exp(-(0.4+0.5*Gender))')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1051, Name='Population set for Simulation Example 5a', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','') ,('State0',''), ('State1',''), ('State2Terminal','')] , Data = [[ 1, 1, 0,0 ]] + [[0, 1 ,0,0]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1051, Name = 'Simulation Project - Test Example 5a' , Notes = 'Multiple Transitions in a Chain with an Expression and Boolean Covariate',  PrimaryModelID = 51000000  , PrimaryPopulationSetID = 1051 , NumberOfSimulationSteps = 2  , NumberOfRepetitions = 1000  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 5b
    
    # Define Parameters
    # Define States
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200001 , Name = 'State1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200092 , Name = 'State2Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 52000000 , Name = 'Example 5b : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200001, 2200092 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 52000000 , Name = 'Simulation Example 5b:  Multiple Transitions in a Chain with an Expression and Continuous Covariate' , Notes = '' , DerivedFrom = 0 , MainProcess = 52000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 52000000, FromState = 2200000, ToState = 2200001, Probability = DB.Expr('Exp(-(0.04+0.03*Age))')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 52000000, FromState = 2200001, ToState = 2200092, Probability = DB.Expr('Exp(-(0.04+0.05*Age))')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1052, Name='Population set for Simulation Example 5b', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','') ,('Age','') ,('State0',''), ('State1',''), ('State2Terminal','')] , Data = [[ 1, 45, 1, 0, 0 ]] + [[0, 60, 1, 0, 0]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1052, Name = 'Simulation Project - Test Example 5b' , Notes = 'Multiple Transitions in a Chain with an Expression and Continuous Covariate',  PrimaryModelID = 52000000  , PrimaryPopulationSetID = 1052 , NumberOfSimulationSteps = 2  , NumberOfRepetitions = 1000  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    
    ###############################################################################
    
    # Simulation Project - Example 6
    
    # Define Parameters
    # Define States
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200001 , Name = 'State1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200002 , Name = 'State2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200093 , Name = 'State3Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 6000000 , Name = 'Example 6 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200001, 2200002, 2200093 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 6000000 , Name = 'Simulation Example 6:  Multiple Transitions in a Long Chain with an Expression Containing a Continuous Covariate' , Notes = '' , DerivedFrom = 0 , MainProcess = 6000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 6000000, FromState = 2200000, ToState = 2200001, Probability = DB.Expr('Exp(-(0.04+0.03*Age))')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 6000000, FromState = 2200001, ToState = 2200002, Probability = DB.Expr('Exp(-(0.04+0.05*Age))')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 6000000, FromState = 2200002, ToState = 2200093, Probability = DB.Expr('Exp(-(0.04+0.05*Age))')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1060, Name='Population set for Simulation Example 6', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','') ,('Age','') ,('State0',''), ('State1',''), ('State2',''), ('State3Terminal','')] , Data = [[ 1, 45, 1, 0, 0, 0 ]] + [[0, 60, 1, 0, 0, 0]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1060, Name = 'Simulation Project - Test Example 6' , Notes = 'Multiple Transitions in a Long Chain with an Expression Containing a Continuous Covariate',  PrimaryModelID = 6000000  , PrimaryPopulationSetID = 1060 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 10000  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 7
    
    # Define Parameters
    # Define States
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200001 , Name = 'State1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200002 , Name = 'State2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200088 , Name = 'DummyStartEvent' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = True , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 7000000 , Name = 'Example 7 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200001, 2200002, 2200088 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 7000000 , Name = 'Simulation Example 7: Funny Loop Example with an Expression' , Notes = '' , DerivedFrom = 0 , MainProcess = 7000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 7000000, FromState = 2200000, ToState = 2200001, Probability = DB.Expr('Exp(-(0.02+0.02*Age))')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 7000000, FromState = 2200001, ToState = 2200002, Probability = DB.Expr('Exp(-(0.02+0.01*Age))')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 7000000, FromState = 2200002, ToState = 2200000, Probability = DB.Expr('Exp(-(0.02+0.01*Age))')), ProjectBypassID = 0)
    # Dummy Start
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 7000000, FromState = 2200088, ToState = 2200000, Probability = DB.Expr('1')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1070, Name='Population set for Simulation Example 7', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','') ,('Age','') ,('State0',''), ('State1',''), ('State2','')] , Data = [[ 1, 45, 1, 0, 0 ]] + [[0, 60, 1, 0, 0]], Objectives = [] ), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1070, Name = 'Simulation Project - Test Example 7' , Notes = 'Funny Loop Example with an Expression',  PrimaryModelID = 7000000  , PrimaryPopulationSetID = 1070 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 1000, SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 8
    
    # Define Parameters
    # Define States
    
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200050 , Name = 'EventState' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = True , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200091 , Name = 'State1Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 8000000 , Name = 'Example 8 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200050, 2200091 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 8000000 , Name = 'Simulation Example 8: An Event State in a Chain' , Notes = '' , DerivedFrom = 0 , MainProcess = 8000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 8000000, FromState = 2200000, ToState = 2200050, Probability = DB.Expr('0.0717')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 8000000, FromState = 2200050, ToState = 2200091, Probability = DB.Expr('1')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1080, Name='Population set for Simulation Example 8', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','') ,('State0',''), ('State1Terminal','')] , Data = [[ 30, 1, 0 ]]*9 + [[30,0,1]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1080, Name = 'Simulation Project - Test Example 8' , Notes = 'An Event State in a Chain',  PrimaryModelID = 8000000  , PrimaryPopulationSetID = 1080 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 9
    
    # Define Parameters
    # Define States
    
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200050 , Name = 'EventState' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = True , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200002 , Name = 'State2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200093 , Name = 'State3Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 9000000 , Name = 'Example 9 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200050, 2200002, 2200093 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 9000000 , Name = 'Simulation Example 9: Combined Fork Loop and Event state' , Notes = '' , DerivedFrom = 0 , MainProcess = 9000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 9000000, FromState = 2200000, ToState = 2200050, Probability = DB.Expr('0.1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 9000000, FromState = 2200050, ToState = 2200002, Probability = DB.Expr('0.8')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 9000000, FromState = 2200050, ToState = 2200093, Probability = DB.Expr('0.2')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 9000000, FromState = 2200002, ToState = 2200050, Probability = DB.Expr('0.1')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1090, Name='Population set for Simulation Example 9', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','') ,('State0',''), ('State2',''), ('State3Terminal','')] , Data = [[ 40, 1, 0, 0 ]]*4 + [[ 50, 0, 1, 0 ]]*5 + [[60, 0, 0, 1]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1090, Name = 'Simulation Project - Test Example 9' , Notes = 'Combined Fork Loop and Event state',  PrimaryModelID = 9000000  , PrimaryPopulationSetID = 1090 , NumberOfSimulationSteps = 10  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 10
    
    # Define Parameters
    # Define States
    
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200071 , Name = 'Splitter1' , Notes = '' , IsSplit = True , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200001 , Name = 'State1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200002 , Name = 'State2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200081 , Name = 'Joiner1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 2200071 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200093 , Name = 'State3Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 10010000 , Name = 'Example10SubProcess1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200001 ] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 10020000 , Name = 'Example10SubProcess2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200002 ] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 10000000 , Name = 'Example 10 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200071, 10010000, 10020000, 2200081, 2200093 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 10000000 , Name = 'Simulation Example 10: Split, Join, Simple Test' , Notes = '' , DerivedFrom = 0 , MainProcess = 10000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess

    DB.Transitions.AddNew(DB.Transition(StudyModelID = 10000000, FromState = 2200000, ToState = 2200071, Probability = DB.Expr('0.1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 10000000, FromState = 2200071, ToState = 2200001, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 10000000, FromState = 2200071, ToState = 2200002, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 10000000, FromState = 2200001, ToState = 2200081, Probability = DB.Expr('1.0-2.0/5.0*5.0**0.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 10000000, FromState = 2200002, ToState = 2200081, Probability = DB.Expr('1.0-2.0/5.0*5.0**0.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 10000000, FromState = 2200081, ToState = 2200093, Probability = DB.Expr('1')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1100, Name='Population set for Simulation Example 10', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age',''), ('State0',''), ('State1',''), ('State2',''), ('State3Terminal','')] , Data = [[ 30, 1, 0, 0, 0 ]] + [[ 30, 0, 1, 1, 0 ]], Objectives = [] ), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1100, Name = 'Simulation Project - Test Example 10' , Notes = 'Split, Join, Simple Test',  PrimaryModelID = 10000000  , PrimaryPopulationSetID = 1100 , NumberOfSimulationSteps = 5  , NumberOfRepetitions = 500  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 11
    
    # Define Parameters
    # Define States
    
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200071 , Name = 'Splitter1' , Notes = '' , IsSplit = True , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200051 , Name = 'EventState1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = True , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200002 , Name = 'State2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200003 , Name = 'State3' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200054 , Name = 'EventState4' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = True , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200081 , Name = 'Joiner1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 2200071 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200095 , Name = 'State5Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 11010000 , Name = 'Example11SubProcess1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200051, 2200002 ] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 11020000 , Name = 'Example11SubProcess2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200003, 2200054 ] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 11000000 , Name = 'Example 11 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200071, 11010000, 11020000, 2200081, 2200095 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 11000000 , Name = 'Simulation Example 11: Split, Join, and Event Test' , Notes = '' , DerivedFrom = 0 , MainProcess = 11000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 11000000, FromState = 2200000, ToState = 2200071, Probability = DB.Expr('0.1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 11000000, FromState = 2200071, ToState = 2200051, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 11000000, FromState = 2200071, ToState = 2200003, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 11000000, FromState = 2200051, ToState = 2200002, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 11000000, FromState = 2200003, ToState = 2200054, Probability = DB.Expr('1.0-2.0/5.0*5.0**0.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 11000000, FromState = 2200002, ToState = 2200081, Probability = DB.Expr('1.0-2.0/5.0*5.0**0.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 11000000, FromState = 2200054, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 11000000, FromState = 2200081, ToState = 2200095, Probability = DB.Expr('1')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1110, Name='Population set for Simulation Example 11', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age',''), ('State0',''), ('State2',''), ('State3',''), ('State5Terminal','')] , Data = [[ 30, 1, 0, 0, 0 ]] + [[ 30, 0, 1, 1, 0 ]], Objectives = [] ), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1110, Name = 'Simulation Project - Test Example 11' , Notes = 'Split, Join, and Event Test',  PrimaryModelID = 11000000  , PrimaryPopulationSetID = 1110 , NumberOfSimulationSteps = 5  , NumberOfRepetitions = 500  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    ###############################################################################
    
    
    
    ###############################################################################
    
    # Simulation Project - Example 12
    
    # Define Parameters
    # Define States
    
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200071 , Name = 'Splitter1' , Notes = '' , IsSplit = True , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200001 , Name = 'State1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200002 , Name = 'State2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , PoolingStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200072 , Name = 'Splitter2' , Notes = '' , IsSplit = True , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200003 , Name = 'State3' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200004 , Name = 'State4' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200082 , Name = 'Joiner2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 2200072 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200005 , Name = 'State5' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200081 , Name = 'Joiner1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 2200071 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 2200096 , Name = 'State6Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 12030000 , Name = 'Example12SubProcess3' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200003 ] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 12040000 , Name = 'Example12SubProcess4' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200004 ] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 12010000 , Name = 'Example12SubProcess1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200001, 2200002 ] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 12020000 , Name = 'Example12SubProcess2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200072, 12030000, 12040000, 2200082, 2200005 ] ), ProjectBypassID = 0)
    DB.States.AddNew(DB.State(ID = 12000000 , Name = 'Example 12 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200071, 12010000, 12020000, 2200081, 2200096 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 12000000 , Name = 'Simulation Example 12: Nested split/join test' , Notes = '' , DerivedFrom = 0 , MainProcess = 12000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200000, ToState = 2200071, Probability = DB.Expr('0.1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200071, ToState = 2200001, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200071, ToState = 2200072, Probability = DB.Expr('1')), ProjectBypassID = 0)
    
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200001, ToState = 2200002, Probability = DB.Expr('0.2')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200002, ToState = 2200081, Probability = DB.Expr('1.0-(7.0/10.0)**0.5')), ProjectBypassID = 0)
    
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200072, ToState = 2200003, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200072, ToState = 2200004, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200003, ToState = 2200082, Probability = DB.Expr('1.0-2.0/5.0*5.0**0.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200004, ToState = 2200082, Probability = DB.Expr('1.0-2.0/5.0*5.0**0.5')), ProjectBypassID = 0)
    
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200082, ToState = 2200005, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200005, ToState = 2200081, Probability = DB.Expr('1.0-(7.0/10.0)**0.5')), ProjectBypassID = 0)
    
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 12000000, FromState = 2200081, ToState = 2200096, Probability = DB.Expr('1')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1120, Name='Population set for Simulation Example 12', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age',''), ('State0',''), ('State1',''), ('State2',''), ('State3',''), ('State4',''), ('State5',''), ('State6Terminal','')] , Data = [[ 30, 1, 0, 0, 0, 0, 0, 0 ]] + [[ 30, 0, 1, 0, 1, 1, 0, 0 ]], Objectives = [] ), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1120, Name = 'Simulation Project - Test Example 12' , Notes = 'Nested split/join test',  PrimaryModelID = 12000000  , PrimaryPopulationSetID = 1120 , NumberOfSimulationSteps = 10  , NumberOfRepetitions = 500  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    ###############################################################################
    
    ###############################################################################
    
    # Simulation Project - Example 13
    
    # Define covariates
    #DB.Params.AddNew( DB.Param(Name = 'Age', Formula = '', ParameterType = 'Covariate', ValidationRule = 'Integer', ValidationRuleParams = '[0,130]', Notes = ''), ProjectBypassID = 0)
    
    # Define Parameters
    # Define States
    
    #DB.States.AddNew( DB.State(ID = 2200000, Name = 'State0', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200071, Name = 'Splitter1', Notes = '', IsSplit = True, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200001, Name = 'State1', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200002, Name = 'State2', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200072, Name = 'Splitter2', Notes = '', IsSplit = True, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200003, Name = 'State3', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200004, Name = 'State4', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200082, Name = 'Joiner2', Notes = '', IsSplit = False, JoinerOfSplitter = 2200072, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200005, Name = 'State5', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200081, Name = 'Joiner1', Notes = '', IsSplit = False, JoinerOfSplitter = 2200071, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200096, Name = 'State6Terminal', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = True, ChildStates = []), ProjectBypassID = 0)
    
    #SubProcesses
    DB.States.AddNew( DB.State(ID = 13000002, Name = 'Example13SubProcess1', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200001, 2200002]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 13000003, Name = 'Example13SubProcess3', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200003]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 13000004, Name = 'Example13SubProcess4', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200004]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 13000005, Name = 'Example13SubProcess2', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200072, 2200082, 2200005, 13000003, 13000004]), ProjectBypassID = 0)

    
    #Main Process
    DB.States.AddNew( DB.State(ID = 13000000, Name = 'Example 13 : Main Process', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200000, 2200071, 2200096, 2200081, 13000002, 13000005]), ProjectBypassID = 0)
    
    # Create the model definitions
    DB.StudyModels.AddNew( DB.StudyModel(ID = 13000000, Name = 'Simulation Example 13: Split and join test without termination in a subprocess', Notes = '', DerivedFrom = 0, MainProcess = 13000000), ProjectBypassID = 0)
    
    # Model Transitions
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200072, ToState = 2200004, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200072, ToState = 2200003, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200071, ToState = 2200072, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200081, ToState = 2200096, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200001, ToState = 2200002, Probability = DB.Expr('.2'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200003, ToState = 2200082, Probability = DB.Expr('1-(2/5)*Sqrt(5)'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200082, ToState = 2200005, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200071, ToState = 2200001, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200000, ToState = 2200071, Probability = DB.Expr('.1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200004, ToState = 2200082, Probability = DB.Expr('1-(2/5)*Sqrt(5)'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 13000000, FromState = 2200002, ToState = 2200081, Probability = DB.Expr('.3'), Notes = ''), ProjectBypassID = 0)
    
    #Population Set
    DB.PopulationSets.AddNew( DB.PopulationSet(ID = 1130, Name = 'Population set for Simulation Example 13', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age', ''), ('State0', ''), ('State1', ''), ('State3', ''), ('State4', '')], Data = [[30.0, 1.0, 0.0, 0.0, 0.0], [30.0, 0.0, 1.0, 1.0, 1.0]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1, OccurrenceProbability = '1', AppliedFormula = 'Age+1', Notes = '')]
    
    # Define the project
    DB.Projects.AddNew( DB.Project(ID = 1130, Name = 'Simulation Project - Test Example 13', Notes = 'Split and join test without termination in a subprocess', PrimaryModelID = 13000000, PrimaryPopulationSetID = 1130, NumberOfSimulationSteps = 10, NumberOfRepetitions = 500, SimulationRules = SimRuleList, DerivedFrom = 0), ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    
    ###############################################################################
    
    # Simulation Project - Example 14
    
    
    # Define Parameters
    # Define States
    #DB.States.AddNew( DB.State(ID = 2200000, Name = 'State0', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200051, Name = 'EventState1', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = True, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 14000001, Name = 'EventState2', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = True, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200003, Name = 'State3', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 14000002, Name = 'State4Terminal', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = True, ChildStates = []), ProjectBypassID = 0)
    
    #Add Main Process
    DB.States.AddNew( DB.State(ID = 14000000, Name = 'Example 14: Main Process', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200000, 2200051, 14000001, 2200003, 14000002 ]), ProjectBypassID = 0)
    
    # Create the model definitions
    DB.StudyModels.AddNew( DB.StudyModel(ID = 14000000, Name = 'Simulation Example 14: Multiple events', Notes = '', DerivedFrom = 0, MainProcess = 14000000), ProjectBypassID = 0)
    
    # Model Transitions
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 14000000, FromState = 2200000, ToState = 2200051, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 14000000, FromState = 2200051, ToState = 14000001, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 14000000, FromState = 14000001, ToState = 2200003, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 14000000, FromState = 2200003, ToState = 14000002, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    
    #Population Set
    DB.PopulationSets.AddNew( DB.PopulationSet(ID = 1140, Name = 'Population set for Simulation Example 14', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('State0', '')], Data = [[1.0]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    
    # Define the project
    DB.Projects.AddNew( DB.Project(ID = 1140, Name = 'Simulation Project - Test Example 14', Notes = 'Multiple events', PrimaryModelID = 14000000, PrimaryPopulationSetID = 1140, NumberOfSimulationSteps = 1, NumberOfRepetitions = 100, SimulationRules = SimRuleList, DerivedFrom = 0), ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    
    
    ###############################################################################
    
    # Simulation Project - Example 15
    
    # Define Parameters
    DB.Params.AddNew(DB.Param(Name = 'AgeAtStart', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,Inf]', Notes = 'Age at start of simulation'), ProjectBypassID = 0)
    # Define States
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200091 , Name = 'State1Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 15000000 , Name = 'Example 15 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200091 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 15000000 , Name = 'Simulation Example 15: Simple Table Example' , Notes = '' , DerivedFrom = 0 , MainProcess = 15000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess

    DB.Transitions.AddNew(DB.Transition(StudyModelID = 15000000, FromState = 2200000, ToState = 2200091, Probability = DB.Expr('Table( [[Gender,[NaN,0,1]], [Age,[-Inf,20,40,Inf]]], [[0.1,0.2,0.3],[0.4,0.5,0.6]] )')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1150, Name='Population set for Simulation Example 15', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','') ,('Gender',''), ('State0',''), ('State1Terminal','')] , Data = [[5, 0, 1, 0 ]] + [[25, 0, 1, 0]] + [[45, 0, 1, 0]] + [[5, 1, 1, 0 ]] + [[25, 1, 1, 0]] + [[45, 1, 1, 0]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'AgeAtStart', SimulationPhase = 0 , OccurrenceProbability = '1' , AppliedFormula = 'Age', Notes = 'Copy Age')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1150, Name = 'Simulation Project - Test Example 15' , Notes = 'Simple Table Example',  PrimaryModelID = 15000000  , PrimaryPopulationSetID = 1150 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    
    ###############################################################################
    
    # Simulation Project - Example 16
    
    # Define Parameters
    #DB.Params.AddNew(DB.Param(Name = 'BP', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,Inf]', Notes = 'Blood Pressure'), ProjectBypassID = 0)
    
    # Define States
    #DB.States.AddNew( DB.State(ID = 2200000, Name = 'State0', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200001, Name = 'State1', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200002, Name = 'State2', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200003, Name = 'State3', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200004, Name = 'State4', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200005, Name = 'State5', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)

    DB.States.AddNew( DB.State(ID = 92200012, Name = 'State6', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200013, Name = 'State7', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200014, Name = 'State8', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200015, Name = 'State9', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200016, Name = 'State10', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200017, Name = 'State11', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200018, Name = 'State12', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200019, Name = 'State13', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200020, Name = 'State14', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200021, Name = 'State15', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200022, Name = 'State16', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 10003, Name = 'Death', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = True, ChildStates = []), ProjectBypassID = 0)

    #DB.States.AddNew( DB.State(ID = 2200071, Name = 'Splitter1', Notes = '', IsSplit = True, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200081, Name = 'Joiner1', Notes = '', IsSplit = False, JoinerOfSplitter = 2200071, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew( DB.State(ID = 92200004, Name = 'Example 16: Subprocess1', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200001, 2200002]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200005, Name = 'Example 16: Subprocess2', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200003, 2200004]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200006, Name = 'Example 16: Subprocess3', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200005, 92200012]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200007, Name = 'Example 16: Subprocess4', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [92200013, 92200014]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200008, Name = 'Example 16: Subprocess5', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [92200015, 92200016]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200009, Name = 'Example 16: Subprocess6', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [92200017, 92200018]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200010, Name = 'Example 16: Subprocess7', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [92200019, 92200020]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200011, Name = 'Example 16: Subprocess8', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [92200021, 92200022]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92200003, Name = 'Example 16: Main Process', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200000, 2200071, 2200081, 10003, 92200004, 92200005, 92200006, 92200007, 92200008, 92200009, 92200010, 92200011 ]), ProjectBypassID = 0)


    
    # Create the model definitions
    DB.StudyModels.AddNew( DB.StudyModel(ID = 52000001, Name = 'Simulation Example 16: Function Tests', Notes = '', DerivedFrom = 0, MainProcess = 92200003), ProjectBypassID = 0)
    
    # Model Transitions
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200000, ToState = 2200071, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200071, ToState = 2200001, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200071, ToState = 2200003, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200071, ToState = 2200005, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200071, ToState = 92200013, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200071, ToState = 92200015, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200071, ToState = 92200017, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200071, ToState = 92200019, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200071, ToState = 92200021, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200001, ToState = 2200002, Probability = DB.Expr('Le(Ls(Eq(Eq(-1,-1),Ne(-1,1)),1),0)*Not(Or(0,0)+And(0,1))*IsTrue(.1)*.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200002, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200003, ToState = 2200004, Probability = DB.Expr('Ge(Gr(1,1),0)*Or(0,0,0,1)*And(1,1,1,1)*.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200004, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200005, ToState = 92200012, Probability = DB.Expr('IsInvalidNumber(NaN)*IsInfiniteNumber(-Inf)*Not(IsFiniteNumber(Inf))*(1/Sqrt(Log(16,2)))')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200012, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200013, ToState = 92200014, Probability = DB.Expr('Ln(Exp(Max(.25,0,-3)+Min(.25,100,25)))')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200014, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200015, ToState = 92200016, Probability = DB.Expr('Pi()+1/Log10(10**2)-3.1415926535897931')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200016, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200017, ToState = 92200018, Probability = DB.Expr('Abs(-.5)*Floor(1.9)*Ceil(.1)*Mod(3,2)')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200018, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200019, ToState = 92200020, Probability = DB.Expr('4/Pow(2,3)')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200020, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200021, ToState = 92200022, Probability = DB.Expr('.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 92200022, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 52000001, FromState = 2200081, ToState = 10003, Probability = DB.Expr('1')), ProjectBypassID = 0)

    
    # Populate the table with population sets
    DB.PopulationSets.AddNew( DB.PopulationSet(ID = 111111113, Name = 'Population set for Simulation Example 16', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('State0', ''), ('BP', '')], Data = [[1.0, 0]], Objectives = [] ), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'BP', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'BP + Le(Ls(Eq(Eq(-1,-1),Ne(-1,1)),1),0)*Not(Or(0,0)+And(0,1))*IsTrue(.1)*.5 + Ge(Gr(1,1),0)*Or(0,0,0,1)*And(1,1,1,1)*.5 + IsInvalidNumber(NaN)*IsInfiniteNumber(-Inf)*Not(IsFiniteNumber(Inf))*(1/Sqrt(Log(16,2))) + Ln(Exp(Max(.25,0,-3)+Min(.25,100,25))) + Pi()+1/Log10(10**2)-3.1415926535897931 + Abs(-.5)*Floor(1.9)*Ceil(.1)*Mod(3,2) + 4/Pow(2,3) + .5', Notes = 'Add 4 to BP')]
    
    # Define the project
    DB.Projects.AddNew( DB.Project(ID = 1160, Name = 'Simulation Project - Test Example 16', Notes = 'Function Tests', PrimaryModelID = 52000001, PrimaryPopulationSetID = 111111113, NumberOfSimulationSteps = 2, NumberOfRepetitions = 1000, SimulationRules = SimRuleList, DerivedFrom = 0), ProjectBypassID = 0)
    
    
    ###############################################################################
    
    
    ###############################################################################
    
    # Simulation Project - Example 17
    
    # Define Parameters
    #DB.Params.AddNew( DB.Param(Name = 'Age', Formula = '', ParameterType = 'Integer', ValidationRuleParams = '[0,130]', Notes = ''), ProjectBypassID = 0)
    DB.Params.AddNew( DB.Param(Name = 'Ex17TestCovariate', Formula = '', ParameterType = 'Integer', ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
    DB.Params.AddNew( DB.Param(Name = 'Ex17TestCovariate2', Formula = '', ParameterType = 'Integer', ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
    DB.Params.AddNew( DB.Param(Name = 'State2_Diagnosed', Formula = '', ParameterType = 'Integer', ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)

    # Define States
    #DB.States.AddNew( DB.State(ID = 2200000, Name = 'State0', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200001, Name = 'State1', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200002, Name = 'State2', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200093, Name = 'State3Terminal', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = True, ChildStates = []), ProjectBypassID = 0)

    # Add SubProcess
    DB.States.AddNew( DB.State(ID = 17000000, Name = 'Example 17 : Main Process', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200000, 2200001, 2200002, 2200093]), ProjectBypassID = 0)
    
    # Create the model definitions
    DB.StudyModels.AddNew( DB.StudyModel(ID = 17000000, Name = 'Simulation Example 17: Tests Iif(), conditionals, and feedback to indicators', Notes = '', DerivedFrom = 0, MainProcess = 17000000), ProjectBypassID = 0)
    
    # Model Transitions
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 17000000, FromState = 2200002, ToState = 2200093, Probability = DB.Expr('Iif(State2_Diagnosed, 1, 0)'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 17000000, FromState = 2200001, ToState = 2200002, Probability = DB.Expr('Iif(Gr(Age,32),1,0)'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 17000000, FromState = 2200000, ToState = 2200001, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew( DB.PopulationSet(ID = 1170, Name = 'Population set for Simulation Example 17', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('State0', ''), ('Age', ''), ('Ex17TestCovariate', ''), ('Ex17TestCovariate2', '')], Data = [[1.0, 30.0, 0.0, 0.0]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'State2_Diagnosed', SimulationPhase = 0, OccurrenceProbability = '1', AppliedFormula = 'State2', Notes = '')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1, OccurrenceProbability = '1', AppliedFormula = 'Age+1', Notes = '')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Ex17TestCovariate', SimulationPhase = 1, OccurrenceProbability = 'State0', AppliedFormula = 'Ex17TestCovariate+1', Notes = '')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Ex17TestCovariate2', SimulationPhase = 1, OccurrenceProbability = 'Iif(State0, 1, 0)', AppliedFormula = 'Iif(State0, Ex17TestCovariate2 + 1, Ex17TestCovariate2)', Notes = '')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'State2_Diagnosed', SimulationPhase = 3, OccurrenceProbability = 'State2', AppliedFormula = 'Iif(Gr(Age, 34), 1, 0)', Notes = '')]
    
    # Define the project
    DB.Projects.AddNew( DB.Project(ID = 1170, Name = 'Simulation Project - Test Example 17', Notes = 'Tests Iif(), conditionals, and feedback to indicators', PrimaryModelID = 17000000, PrimaryPopulationSetID = 1170, NumberOfSimulationSteps = 10, NumberOfRepetitions = 50, SimulationRules = SimRuleList, DerivedFrom = 0), ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    
    ###############################################################################
    
    # Simulation Project - Example 18
    
    
    # Define Parameters
    #DB.Params.AddNew( DB.Param(Name = 'Age', Formula = '', ParameterType = 'Integer', ValidationRuleParams = '[0,130]', Notes = ''), ProjectBypassID = 0)
    DB.Params.AddNew( DB.Param(Name = 'Ex18TestQoL', Formula = '', ParameterType = 'Number', ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)
    DB.Params.AddNew( DB.Param(Name = 'Ex18TestCost', Formula = '', ParameterType = 'Number', ValidationRuleParams = '[0,Inf]', Notes = ''), ProjectBypassID = 0)
    
    # Define States
    #DB.States.AddNew( DB.State(ID = 2200000, Name = 'State0', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200001, Name = 'State1', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200002, Name = 'State2', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200093, Name = 'State3Terminal', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = True, ChildStates = []), ProjectBypassID = 0)

    # Add SubProcess
    DB.States.AddNew( DB.State(ID = 18000000, Name = 'Example 18 : Main Process', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200000, 2200001, 2200002, 2200093]), ProjectBypassID = 0)
    
    # Create the model definitions
    DB.StudyModels.AddNew( DB.StudyModel(ID = 18000000, Name = 'Simulation Example 18: Tests Cost/QoL Wizard', Notes = '', DerivedFrom = 0, MainProcess = 18000000), ProjectBypassID = 0)
    
    # Model Transitions
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 18000000, FromState = 2200000, ToState = 2200001, Probability = DB.Expr('1'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 18000000, FromState = 2200001, ToState = 2200002, Probability = DB.Expr('.5'), Notes = ''), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 18000000, FromState = 2200002, ToState = 2200093, Probability = DB.Expr('.5'), Notes = ''), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew( DB.PopulationSet(ID = 1180, Name = 'Population set for Simulation Example 18', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('State0', ''), ('Age', ''), ('Ex18TestQoL', ''), ('Ex18TestCost', '')], Data = [[1.0, 30.0, 0.1, 10]], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1, OccurrenceProbability = '1', AppliedFormula = 'Age + 1', Notes = '')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Ex18TestCost', SimulationPhase = 3, OccurrenceProbability = '1', AppliedFormula = 'CostWizard(0,100,[State1,State2],[Iif(Gr(Age,31),3,0),Iif(Gr(Age,33),2,0)])', Notes = '')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Ex18TestQoL', SimulationPhase = 3, OccurrenceProbability = '1', AppliedFormula = 'CostWizard(1,.5,[State1,State2],[Iif(Gr(Age,31),.1,0),Iif(Gr(Age,33),.2,0)])', Notes = '')]

    
    # Define the project
    DB.Projects.AddNew( DB.Project(ID = 1180, Name = 'Simulation Project - Test Example 18', Notes = 'Tests Cost/QoL Wizard', PrimaryModelID = 18000000, PrimaryPopulationSetID = 1180, NumberOfSimulationSteps = 5, NumberOfRepetitions = 100, SimulationRules = SimRuleList, DerivedFrom = 0), ProjectBypassID = 0)
    
    
    ###############################################################################
    
    
    ###############################################################################
    
    # Simulation Project - Example 19
    
    # Define Parameters
    DB.Params.AddNew(DB.Param(Name = 'TestCov1', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Test Covariate'), ProjectBypassID = 0)
    DB.Params.AddNew(DB.Param(Name = 'TestCov2', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Test Covariate'), ProjectBypassID = 0)
    DB.Params.AddNew(DB.Param(Name = 'TestCov3', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Test Covariate'), ProjectBypassID = 0)
    DB.Params.AddNew(DB.Param(Name = 'TestCov4', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Test Covariate'), ProjectBypassID = 0)
    DB.Params.AddNew(DB.Param(Name = 'TestCov5', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Test Covariate'), ProjectBypassID = 0)

    
    # Define States
    #DB.States.AddNew( DB.State(ID = 2200000, Name = 'State0', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200001, Name = 'State1', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200002, Name = 'State2', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200003, Name = 'State3', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200004, Name = 'State4', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200005, Name = 'State5', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 92200012, Name = 'State6', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 92200013, Name = 'State7', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 92200014, Name = 'State8', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 92200015, Name = 'State9', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 92200016, Name = 'State10', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 10003, Name = 'Death', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = True, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200071, Name = 'Splitter1', Notes = '', IsSplit = True, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    #DB.States.AddNew( DB.State(ID = 2200081, Name = 'Joiner1', Notes = '', IsSplit = False, JoinerOfSplitter = 2200071, IsEvent = False, IsTerminal = False, ChildStates = []), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew( DB.State(ID = 92300004, Name = 'Example 19: Subprocess1', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200001, 2200002]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92300005, Name = 'Example 19: Subprocess2', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200003, 2200004]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92300006, Name = 'Example 19: Subprocess3', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200005, 92200012]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92300007, Name = 'Example 19: Subprocess4', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [92200013, 92200014]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92300008, Name = 'Example 19: Subprocess5', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [92200015, 92200016]), ProjectBypassID = 0)
    DB.States.AddNew( DB.State(ID = 92300003, Name = 'Example 19: Main Process', Notes = '', IsSplit = False, JoinerOfSplitter = 0, IsEvent = False, IsTerminal = False, ChildStates = [2200000, 2200071, 2200081, 10003, 92300004, 92300005, 92300006, 92300007, 92300008]), ProjectBypassID = 0)
    
    # Create the model definitions
    DB.StudyModels.AddNew( DB.StudyModel(ID = 19000000, Name = 'Simulation Example 19: Distribution Function Test', Notes = '', DerivedFrom = 0, MainProcess = 92300003), ProjectBypassID = 0)
    
    
    # Model Transitions
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200000, ToState = 2200071, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200071, ToState = 2200001, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200071, ToState = 2200003, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200071, ToState = 2200005, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200071, ToState = 92200013, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200071, ToState = 92200015, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200001, ToState = 2200002, Probability = DB.Expr('0.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200002, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200003, ToState = 2200004, Probability = DB.Expr('0.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200004, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200005, ToState = 92200012, Probability = DB.Expr('0.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 92200012, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 92200013, ToState = 92200014, Probability = DB.Expr('0.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 92200014, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 92200015, ToState = 92200016, Probability = DB.Expr('0.5')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 92200016, ToState = 2200081, Probability = DB.Expr('1')), ProjectBypassID = 0)
    DB.Transitions.AddNew( DB.Transition(StudyModelID = 19000000, FromState = 2200081, ToState = 10003, Probability = DB.Expr('1')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew( DB.PopulationSet(ID = 1190, Name = 'Population set for Simulation Example 19', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('State0', ''), ('TestCov1', ''), ('TestCov2', ''), ('TestCov3', ''), ('TestCov4', ''), ('TestCov5', '')], Data = [[1.0, 0, 0, 0, 0, 0]], Objectives = [] ), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestCov1', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Le(Bernoulli(0.5), 0.5)', Notes = 'Test Bernoulli random number generation')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestCov2', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Le(Binomial(3,0.5), 1)', Notes = 'Test Binomial random number generation')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestCov3', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Le(Geometric(1-0.5**0.5), 2)', Notes = 'Test Geometric random number generation')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestCov4', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Le(Uniform(0,2),1)', Notes = 'Test Uniform random number generation')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestCov5', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Le(Gaussian(3,1), 3)', Notes = 'Test Gaussian random number generation')]
    
    # Define the project
    DB.Projects.AddNew( DB.Project(ID = 1190, Name = 'Simulation Project - Test Example 19', Notes = 'Distribution Function Test', PrimaryModelID = 19000000, PrimaryPopulationSetID = 1190, NumberOfSimulationSteps = 2, NumberOfRepetitions = 1000, SimulationRules = SimRuleList, DerivedFrom = 0), ProjectBypassID = 0)
    
    
    
    ###############################################################################
    
    
    ###############################################################################
    
    # Simulation Project - Example 20
    
    # Define Parameters
    # Define States
    #DB.States.AddNew(DB.State(ID = 10021 , Name = 'Alive' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 1000002 , Name = 'Dead' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 20000000 , Name = 'Example 20 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 10021, 1000002 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 20000000 , Name = 'Simulation Example 20: Simple Example with Initial Population Defined by Distributions' , Notes = '' , DerivedFrom = 0 , MainProcess = 1000000  ), ProjectBypassID = 20000000)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess
    DB.Transitions.AddNew(DB.Transition(StudyModelID = 20000000, FromState = 10021, ToState = 1000002, Probability = DB.Expr('0.0717')), ProjectBypassID = 0)
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1200, Name='Population set for Simulation Example 20', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','Min(Max(20,Gaussian(30,5)),40)') ,('Alive','Bernoulli(0.9)'), ('Dead','1-Alive')] , Data = [], Objectives = []), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1200, Name = 'Simulation Project - Test Example 20' , Notes = 'Simple Example with Initial Population Defined by Distributions' , PrimaryModelID = 20000000  , PrimaryPopulationSetID = 1200 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 1000  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)


    ###############################################################################
    
    # Simulation Project - Example 21
    
    # Define Parameters
    #DB.Params.AddNew(DB.Param(Name = 'AgeAtStart', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,Inf]', Notes = 'Age at start of simulation'), ProjectBypassID = 0)
    # Define States
    #DB.States.AddNew(DB.State(ID = 2200000 , Name = 'State0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
    #DB.States.AddNew(DB.State(ID = 2200091 , Name = 'State1Terminal' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
    
    # Add SubProcess
    DB.States.AddNew(DB.State(ID = 21000000 , Name = 'Example 21 : Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 2200000, 2200091 ] ), ProjectBypassID = 0)
    
    # Create the model-study definitions
    DB.StudyModels.AddNew(DB.StudyModel( ID = 21000000 , Name = 'Simulation Example 21: Initial Population Defined by Distributions and simple Objectives' , Notes = '' , DerivedFrom = 0 , MainProcess = 21000000  ), ProjectBypassID = 0)
    
    ### Create the model definitions
    ### Model Transitions
    # MainProcess

    DB.Transitions.AddNew(DB.Transition(StudyModelID = 21000000, FromState = 2200000, ToState = 2200091, Probability = DB.Expr('Table( [[Gender,[NaN,0,1]], [Age,[-Inf,20,40,Inf]]], [[0.1,0.2,0.3],[0.4,0.5,0.6]] )')), ProjectBypassID = 0)
    
    
    # Define Objectives (FilterExpr,StatExpr,StatFunction,TargetValue,Weight,CalcValue,CalcError)
    Objectives = []
    Objectives = Objectives + [('Le(Age,20)',                                'Age',              'MEAN',     5,  1, None,None)]
    Objectives = Objectives + [('And(Gr(Age,20), Le(Age,40))',               'Age -25',          'MEAN',     0,  1, None,None)]
    Objectives = Objectives + [('Gr(Age,40)',                                'Age',              'MEAN',     45, 1, None,None)]
    Objectives = Objectives + [('1',                                         'Gender',           'MEAN',     0.5,1, None,None)]
    Objectives = Objectives + [('1',                                         'Age*(Gender-0.5)', 'MEDIAN',   0,  1, None,None)]
    Objectives = Objectives + [('Le(Age,20)',                                'Age',              'STD',      1,  0.1, None,None)]
    Objectives = Objectives + [('And(Gr(Age,20), Le(Age,40))',               'Age',              'PERCENT25',24, 0.1, None,None)]
    Objectives = Objectives + [('And(Gr(Age,20), Le(Age,40))',               'Age',              'PERCENT75',26, 0.1, None,None)]
    Objectives = Objectives + [('Gr(Age,40)',                                'Age',              'MIN'      ,42 ,0.1, None,None)]
    Objectives = Objectives + [('Gr(Age,40)',                                'Age',              'MAX'      ,48 ,0.1, None,None)]
    Objectives = Objectives + [('And(Le(Age,20), Eq(Gender,0))',             '1',                'SUM'      ,100,0.02,None,None)]
    Objectives = Objectives + [('And(Gr(Age,20), Le(Age,40) , Eq(Gender,0))','1',                'SUM'      ,100,0.02,None,None)]
    Objectives = Objectives + [('And(Gr(Age,40), Eq(Gender,0))',             '1',                'SUM'      ,100,0.02,None,None)]
    Objectives = Objectives + [('And(Le(Age,20), Eq(Gender,1))',             'Age**2',           'COUNT'    ,100,0.02,None,None)]
    Objectives = Objectives + [('And(Gr(Age,20), Le(Age,40) , Eq(Gender,1))','Age**2',           'COUNT'    ,100,0.02,None,None)]
    Objectives = Objectives + [('And(Gr(Age,40), Eq(Gender,1))',             'Age**2',           'COUNT'    ,100,0.02,None,None)]
    
    # Populate the table with population sets
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1210, Name='Population set for Simulation Example 21', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','Uniform(1,59)') ,('Gender','Bernoulli(0.6)'), ('State0','1'), ('State1Terminal','0')] , Data = [], Objectives = Objectives), ProjectBypassID = 0)
    
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'AgeAtStart', SimulationPhase = 0 , OccurrenceProbability = '1' , AppliedFormula = 'Age', Notes = 'Copy Age')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1210, Name = 'Simulation Project - Test Example 21' , Notes = 'Initial Population Defined by Distributions and simple Objectives',  PrimaryModelID = 21000000  , PrimaryPopulationSetID = 1210 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 600  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    
    ###############################################################################



    

class GenericSetupAndTearDown:

    setUp = SetupEmptyDB

    def tearDown(self):
        # wipe out all data by creating blank data definitions
        print 'TearDown'
        DB.CreateBlankDataDefinitions()

    def RecordSimResults(self, SimName, ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, OptionalTestFailed, *ArgList):
        """ record the simulation results """
        global ResultsVec, SimRepetition, RandomSeedToUse
        Delimiter = '|'
        self.ResultsVec = self.ResultsVec + [[SimName, self.SimRepetition, Delimiter, ActualOutcomes, Delimiter, ExpectedOutcomes, Delimiter, STDMargins, Delimiter, TestSuccess, OtherTestFailed,  Delimiter, CriticalTestFailed, Delimiter, OptionalTestFailed, Delimiter, self.RandomSeedToUse , Delimiter , str(list(ArgList))]]
    
    def GenReport(self, ResultID, FileName, FormatOptions = None):
        """ Generate a report summarizing the data """    
        RepStr = DB.SimulationResults[ResultID].GenerateReport(FormatOptions)
        FileObject = open(FileName,'w')
        FileObject.write(RepStr)
        FileObject.close()
        return RepStr


        
def AddProject1005AndRun(RandomSeedToUse):
    # Reset database before definng the project
    # fisrt remove the data from the database
    DB.CreateBlankDataDefinitions()
    # now setup a new DB
    SetupFullDB()
    # Project 1010 is changed to project 1005 where Age of 1 person becomes NaN
    # Also replace Age with Age1 parameter which is not bounded
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1005, Name='Population set for Simulation Example 1 with NaN', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','') ,('Alive',''), ('Dead','')] , Data = [[ DB.NaN, 1, 0 ]] + [[ 30, 1, 0 ]]*8 + [[30,0,1]], Objectives = []), ProjectBypassID = 0)
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age +1', Notes = 'Age Increase')]
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1005, Name = 'Simulation Project - Test Example 1 Modified with NaN' , Notes = 'Simple Example', PrimaryModelID = 1000000  , PrimaryPopulationSetID = 1005 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)

    # First Take example 1 and generate results with a known random seed:
    SimulationOptions = [('RandomSeed',RandomSeedToUse)]
    SimulationScriptFullPath1 = DB.Projects[1005].CompileSimulation('SimulationExample1005RndSeed'+str(RandomSeedToUse), RandomStateFileNamePrefix = 'SimRandStateEx1005RndSeed'+str(RandomSeedToUse), SimulationOptions = SimulationOptions, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
    ResultsInfo = DB.Projects[1005].RunSimulationAndCollectResults (SimulationScriptFullPath1, FullResultsOutputFileName = DB.SessionTempDirecory+os.sep+'SimulationResultsExample1RndSeed'+str(RandomSeedToUse)+'.csv', DumpOutputAsCSV=True, FinalResultsOutputFileName = DB.SessionTempDirecory+os.sep+'SimulationResultsExample1RndSeed'+str(RandomSeedToUse)+'FinalData.csv')

    # record the last result for future comparison
    ResultsInfoCopy = DB.copy.deepcopy(ResultsInfo)
    DB.SaveAllData(DB.SessionTempDirecory+os.sep+'Testing_RepRndSeed'+str(RandomSeedToUse)+'.zip',True)
    return ResultsInfoCopy


def AddProject1006():

    # Project 1006 is the same as project 1005 except for population,
    # model, NumberOfSimulationSteps, NumberOfPopulationRepetitions
    # and the AgeIncCoef parameter is set to 1000 - this will later
    # be overridden while trying to override initial parameters.
    # RandomSeed is also defined just to be overriden later on
    # The model and population set are also overriden to be the same as
    # 1005 This will be a test for overriding project during simulation
    # Note that the new rules will not change the results vector or the
    # random number sequence since these appear only once at the
    # begining of simulation and do not involve any random number.
    # However two new columns will appear at the results holding these 
    # numbers, so these columns have to be removed for comparison.

    # Reset database before definng the project
    # fisrt remove the data from the database
    DB.CreateBlankDataDefinitions()
    # now setup a new DB
    SetupFullDB()

    DB.Params.AddNew(DB.Param(Name = 'AgeIncCoef', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
    # The simulation needs this population set
    DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1005, Name='Population set for Simulation Example 1 with NaN', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Age','') ,('Alive',''), ('Dead','')] , Data = [[ DB.NaN, 1, 0 ]] + [[ 30, 1, 0 ]]*8 + [[30,0,1]], Objectives = []), ProjectBypassID = 0)
    # Define simulation Rules
    SimRuleList = []
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'RandomSeed', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '10', Notes = '')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'AgeIncCoef', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '1000', Notes = '')]
    SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'Age + AgeIncCoef', Notes = 'Age Increase')]
    # Define the project
    DB.Projects.AddNew(DB.Project(ID = 1006, Name = 'Simulation Project - Test override for Example 1 Modified with NaN' , Notes = 'Simple Example', PrimaryModelID = 2000000  , PrimaryPopulationSetID = 1020 , NumberOfSimulationSteps = 5  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
    
    DB.SaveAllData(DB.SessionTempDirecory+os.sep+'Testing_MultiRunOverride.zip',True)





class TestSimulationExamples(GenericSetupAndTearDown):

    # Define needed globals 
    ResultsVec = None
    SimRepetition = None
    RandomSeedToUse = None


    def setUp(self):
        " define default simulation environment"
        # use the full DB setup
        SetupFullDB()
    
        # Initialize the global that holds the reults
        self.ResultsVec = []
        
        # Summarize all the tests done so far in a single row:
        # indicate preliminary tests
        self.SimRepetition = -1
        self.RandomSeedToUse = None
        self.RecordSimResults('Preliminary Validation Tests ', [], [], [], True, False, GeneralErrorCounter, 0)

    
    def CheckSimulationOutcomeDistribution(self, FinalDataRecords, ColumnsToExamine, ExpectedOutcomes , AllowedDeviationInSTD, ColumnsToMaskWith = None, IsStateColumnVector = None):
        TestSuccess = True
        CriticalTestSuccess = True
        ActualOutcomes = [0]*len(ColumnsToExamine)
        for Entry in FinalDataRecords:
            for (Index, Column) in enumerate(ColumnsToExamine):
                if ColumnsToMaskWith == None or Entry[ColumnsToMaskWith[Index]] != 0:
                    ActualOutcomes[Index] = ActualOutcomes[Index] + Entry[Column]               
        OutcomesToSum = ActualOutcomes
        ModifiedExpectedOutcomes =  ExpectedOutcomes
        # if IsStateColumnVector is defined as a list, recalcualte 
        if DB.IsList(IsStateColumnVector):
            OutcomesToSum = map(lambda a,b: a*b, ActualOutcomes,IsStateColumnVector)
            ModifiedExpectedOutcomes =  map(lambda a,b: a*b, ExpectedOutcomes,IsStateColumnVector)
        TotalNumberOfOutcomes = round(reduce(lambda a,b: a+b, ModifiedExpectedOutcomes))
        STDMargins = map (lambda Num: ((1.0 - float(Num) / float(TotalNumberOfOutcomes) )*float(Num) / float(TotalNumberOfOutcomes) * TotalNumberOfOutcomes)**0.5 , ExpectedOutcomes)
        AllowedMargins = map (lambda Num: Num * AllowedDeviationInSTD, STDMargins)
        print 'Distribution analysis:'
        print '________________________________________________'
        print 'Actual Distribution was: ' +  str(ActualOutcomes)
        print 'Expected outcome for each state: ' + str(ExpectedOutcomes)
        print 'Allowed Margins for each state: ' + str(AllowedMargins)
        if (IsStateColumnVector == None or DB.IsList(IsStateColumnVector)) and reduce(lambda a,b: a+b, OutcomesToSum)  != TotalNumberOfOutcomes:
            print 'Test FAILURE: Total sum of individuals in states of interest at the simulation end does not sum to ' + str(TotalNumberOfOutcomes)
            BeepForError()
            CriticalTestSuccess = False        
        elif not all(map ( lambda ActualOutcome, ExpectedOutcome, AllowedMargin: abs(ActualOutcome - ExpectedOutcome) <= AllowedMargin, ActualOutcomes, ExpectedOutcomes, AllowedMargins)):
            print 'Statistical Test FAILURE: Number Individuals in at least one state is out of allowed margin'
            BeepForError(1)
            TestSuccess = False    
        else:   
            print 'Test OK - Actual and expected outcomes are within allowed margins'
        print '________________________________________________'
        return ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess
    
    
    def RecoverPartialResults(self, FilePrefixNoExtensition = 'OutcomeResults', MaxRepetition = 2147483647):
        """ Recovers results of an interrupted simulation """
        i = 0
        StopIterations = False
        ResultsVec = []
        while i < MaxRepetition and not StopIterations:
            try:
                File = open(FilePrefixNoExtensition + str(i)+'.txt','r')
                ResultsEntry = pickle.load(File)
                ResultsVec = ResultsVec + ResultsEntry
                File.close()
            except: 
                StopIterations = True
        return ResultsVec
    
    
    def LoadFinalResults(self, FileName = None):
        """ Load results directly from the final file """
        if FileName == None:
            FileName = DB.SessionTempDirecory + os.sep + 'FinalResults.txt'
        File = open(FileName,'r')
        ResultsVec = pickle.load(File)
        File.close()
        return ResultsVec
    
    
    def AnalyzeResults(self, ResultsVec, AllowedDeviation = 1.96, VerboseLevel = 0):
        """ Analyzes the results and prints report"""
        # Calculates the allowed deviation proportion
        # Since scipy may not be installed, 
        try:
            import scipy.special
            ExpectedOutcomeProportion = scipy.special.erf(AllowedDeviation/(2**0.5))
        except:
            ExpectedOutcomeProportion = 0.95
            print ' Cannot exactly calculate the expected successful outcome value - assuming default'
            
        print '$'*70
        print '$'*70
        print '$'*70
        print '$$$$$$$$$$$$$$$$$$$$$$$$$ Results analysis $$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print '$'*70
        print '$'*70
        print '$'*70
        if VerboseLevel >= 1:
            BadTests =  filter (lambda Entry:Entry[9]==False or Entry[10]== True, ResultsVec)
            if BadTests != []:
                print 'FAILURES (not limited to state outcomes) DETECTED IN EXAMPLES:'
                for Entry in BadTests:
                    print '-' +str(Entry) + '\n'
                print '$'*70
                print '$'*70
        print 'ANALYSIS PARAMETERS:'
        print 'Allowed Margin in Standard Deviations: ' + str(AllowedDeviation)
        print 'The Overall Expected Successful Outcome Rate is: ' + str(ExpectedOutcomeProportion)
        # Split the results in groups
        Groups = sorted(list(set(map(lambda Entry : Entry[0] , ResultsVec))))
        # For each group 
        TotalObservedOutcomeFailCount = 0
        TotalOtherFailCount = 0
        TotalCriticalFailCount = 0
        TotalOptionalFailCount = 0
        TotalNumOfTests = 0
        for Group in Groups:
            print '$'*70
            print '$'*70
            print 'Results for Test Group: ' + Group
            GroupObservedOutcomes = []
            Res = filter (lambda Entry: Entry[0] == Group, ResultsVec)
            NumberOfRepetitions = len(Res)
            print 'Simulation repeated ' + str(NumberOfRepetitions) + ' times'
            # Test each result record and calculate each outcome separately
            NumOfTests = len(Res[0][3])
            OutcomeSums = [0]*NumOfTests
            for Entry in Res:
                Outcomes = Entry[3]
                Averages = Entry[5]
                STDs = Entry[7]
                Tests = map (lambda Outcome,Average, STD: abs(Outcome - Average) <= AllowedDeviation*STD , Outcomes, Averages, STDs)
                OutcomeSums = map ( lambda OutcomeForState, PreviousSum: OutcomeForState + PreviousSum, Outcomes, OutcomeSums)
                GroupObservedOutcomes = GroupObservedOutcomes + [Tests]
            OutcomeAverage = map (lambda OutcomeSum: float(OutcomeSum)/float(NumberOfRepetitions), OutcomeSums)
            print 'The Average Outcome in Simulations Was : ' + str(OutcomeAverage)
            print 'The Expected Outcome Reference Should be: ' + str(Averages)
            # Sum the results per state outcome
            InBoundsSums = [0]*NumOfTests
            for i in range(NumOfTests):
                InBoundsSums[i] = reduce(lambda PrevSum, Entry: PrevSum + Entry[i], GroupObservedOutcomes, 0)
                ObservedOutcomeProportion = float(InBoundsSums[i]) / float(len(GroupObservedOutcomes))
                print 'The observed success proportion for test #' + str(i) + ' was: ' + str(ObservedOutcomeProportion*100) + '% , Count = ' + str(InBoundsSums[i])
                TotalObservedOutcomeFailCount = TotalObservedOutcomeFailCount + InBoundsSums[i]
                TotalNumOfTests = TotalNumOfTests + NumberOfRepetitions
            OtherFailuresDetected = reduce (lambda Sum,Entry: Sum + Entry[10] , Res, 0)
            CriticalDetected = reduce (lambda Sum,Entry: Sum + Entry[12] , Res, 0)
            OptionalDetected = reduce (lambda Sum,Entry: Sum + Entry[14] , Res, 0)
            print 'There were ' + str(OtherFailuresDetected) + ' failed tests other than outcomes in states'
            print 'There were ' + str(CriticalDetected) + ' critical failed tests'
            print 'There were ' + str(OptionalDetected) + ' optional tests failed'
            TotalOtherFailCount = TotalOtherFailCount + OtherFailuresDetected
            TotalCriticalFailCount = TotalCriticalFailCount + CriticalDetected
            TotalOptionalFailCount = TotalOptionalFailCount + OptionalDetected
        print '$'*70
        print '$'*70
        print '$'*70
        print 'RESULT SUMMARY'
        print '--------------'
        print 'Note that:'
        print 'Statistical tests are unlikely to fail, yet it is normal that a few failed.'
        print 'Failure of a critical test means there is a problem with the software'
        print ''
        print 'Total Number of Example Outputs Was: ' + str(len(ResultsVec))
        print 'Total Number of Statistical Outcome Test Outliers Was: ' + str(TotalNumOfTests - TotalObservedOutcomeFailCount) + ' Out of ' + str(TotalNumOfTests)
        print 'Total Number of Other Statistical Test Outliers Was: ' + str(TotalOtherFailCount) 
        print 'Total Number of Optional Tests Failed Was: ' + str(TotalOptionalFailCount)
        print 'Total Number of Critical Tests Failed Was: ' + str(TotalCriticalFailCount)
        print '$'*70
        print '$'*70
        print '$'*70

    
    def QuickAnalyze(self):
        """ Analyze and print results using defaults """
        Res=self.LoadFinalResults()
        self.AnalyzeResults(Res)

    
    def RunTestExample1(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 1                ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1010
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        # Age in all alive people should be 33.
        AliveRecords = filter(lambda Entry: Entry[4] == 1 , FinalData)
        IsAgeOfAliveEquals33 = all(map ( lambda Entry: Entry[3] == 33, AliveRecords))
        if IsAgeOfAliveEquals33:
            print 'Simulation Script of Example 1 is OK - Age in all alive people is 33'
        else:
            print 'Test FAILURE - Simulation Script of Example 1 is invalid - Age in all alive people is not 33'
            BeepForError()
            OtherTestFailed = True
           
        # Average age at death =  31.2540
        DeadRecords = filter(lambda Entry: Entry[5] == 1 , FinalData)
        AgeAtDeath = map ( lambda Entry: Entry[3], DeadRecords)
        AverageAgeAtDeath = reduce (lambda a,b: a+b, AgeAtDeath, 0.0) / len(AgeAtDeath)
        print 'Example 1 - Average Age at death is ' + str(AverageAgeAtDeath)
        if abs(AverageAgeAtDeath - 31.2540) < 0.1:
            print 'Simulation Script of Example 1 is OK - close to 32.1727'
        else:
            print 'Statistical Test FAILURE - Simulation Script of Example 1 is invalid - Average age in death is not close enough to 31.2540'
            BeepForError(1)
            OtherTestFailed = True
          
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [4,5], [719.9587 , 280.0413] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess 
        
        self.RecordSimResults('Example001', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, IsAgeOfAliveEquals33 , AverageAgeAtDeath)
    
        return CriticalTestFailed
    
    
    def RunTestExample2(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 2                ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1020
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
        
        # Age in all alive people should be 35.
        AliveRecords = filter(lambda Entry: Entry[6] != 1 , FinalData)
        IsAgeOfAliveEquals35 = all(map ( lambda Entry: Entry[3] == 35, AliveRecords))
        if IsAgeOfAliveEquals35:
            print 'Simulation Script of Example 2 is OK - Age in all alive people is 35'
        else:
            print 'Test FAILURE - Simulation Script of Example 2 is invalid - Age in all alive people is not 35'
            BeepForError()
            OtherTestFailed = True
    
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [4,5,6], [295.2450 , 295.2450 , 409.5100] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess 
        self.RecordSimResults('Example002', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, IsAgeOfAliveEquals35)
    
        return CriticalTestFailed
    
     
    def RunTestExample3(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 3                ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1030
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [4,5,6], [10 , 330 , 660] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess 
        self.RecordSimResults('Example003', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    
        return CriticalTestFailed
    
    
    def RunTestExample4(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 4                ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1040
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        # No individual is ever at the dummy start event state not entered it
        IndexOfDummyStartIndicator = ResultsInfo.DataColumns.index('DummyStartEvent')
    
        StarterDummyEventNeverUsed = all(map(lambda DataRecord: DataRecord[IndexOfDummyStartIndicator: (IndexOfDummyStartIndicator+2)] == [0,0] , ResultsInfo.Data))
        if StarterDummyEventNeverUsed:
            print 'Example 4 OK - Starter dummy event state is never used '
        else:
            print 'Example 4 FAILURE - Starter dummy event state is set or entered'
            BeepForError()
            CriticalTestFailed = True
    
        IsAgeOfEquals35_45_55 = all(map ( lambda Entry: (Entry[3] == 35) or (Entry[3] == 45) or (Entry[3] == 55), FinalData))
        if IsAgeOfEquals35_45_55:
            print 'Simulation Script of Example 4 is OK - Age at the end of simulation is 35,45,55'
        else:
            print 'Test FAILURE - Simulation Script of Example 4 is invalid - in at end of simulation is not 35,45,55'
            BeepForError()
            CriticalTestFailed = True
    
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [4,5,6], [ 791.1000 , 393.1950 , 315.7050 ] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess 
        self.RecordSimResults('Example004', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, StarterDummyEventNeverUsed , IsAgeOfEquals35_45_55)
    

        return CriticalTestFailed
    
    
    def RunTestExample5a(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 5a               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1051
        ExampleString = '5a'
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        print 'Testing Male population'
        OtherTestFailed = False
        CriticalTestFailed = False
        MaleData = filter (lambda Entry: Entry[3] == 1, FinalData )
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( MaleData, [4,5,6], [253.4264,  544.6771, 201.8965 ] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example005a-Male', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    
        print 'Testing Female population'
        OtherTestFailed = False
        CriticalTestFailed = False
        FemaleData = filter (lambda Entry: Entry[3] == 0, FinalData )
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FemaleData, [4,5,6], [108.6889,  441.9822,  449.3290 ] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
    
        self.RecordSimResults('Example005a-Female', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    

        return CriticalTestFailed
    
    
    def RunTestExample5b(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 5b               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1052
        ExampleString = '5b'
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        print 'Testing Male population'
        OtherTestFailed = False
        CriticalTestFailed = False
        MaleData = filter (lambda Entry: Entry[3] == 1, FinalData )
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( MaleData, [5,6,7], [580.4146 , 397.4372 ,  22.1482] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
    
        MaleInState0NotOfAge47 = filter (lambda Entry: Entry[5] == 1 and Entry[4] != 47, MaleData ) ==[]
        if MaleInState0NotOfAge47:
            print 'Test is OK - Male age at state 0 at the end of simulation is 47'
        else:
            print 'Test FAILURE - Male age at state 0 at the end of simulation is not 47'
            BeepForError()
            CriticalTestFailed = True
    
        self.RecordSimResults('Example005b-Male', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, MaleInState0NotOfAge47)
    
        print 'Testing Female population'
        OtherTestFailed = False
        CriticalTestFailed = False
        FemaleData = filter (lambda Entry: Entry[3] == 0, FinalData )
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FemaleData, [5,6,7], [719.3598 , 273.9693 , 6.6709] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
    
        FemaleInState0NotOfAge62 = filter (lambda Entry: Entry[5] == 1 and Entry[4] != 62, FemaleData ) ==[]
        if FemaleInState0NotOfAge62:
            print 'Test is OK - Female age at state 0 at the end of simulation is 62'
        else:
            print 'Test FAILURE - Female age at state 0 at the end of simulation is not 62'
            BeepForError()
            CriticalTestFailed = True        
        self.RecordSimResults('Example005b-Female', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, FemaleInState0NotOfAge62)
    

        return CriticalTestFailed
    
    
    def RunTestExample6(self):
        
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 6                ######'
        print '########################################################################'
        print '########################################################################'
        # Prepare the project for simulation:
        ExampleNumber = 1060
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        print 'Testing Male population'
        OtherTestFailed = False
        CriticalTestFailed = False
        MaleData = filter (lambda Entry: Entry[3] == 1, FinalData )
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( MaleData, [5,6,7,8], [4482.904 , 4949.205 ,  548.587  , 19.305] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        MaleInState0NotOfAge48 = filter (lambda Entry: Entry[5] == 1 and Entry[4] != 48, MaleData ) ==[]
        if MaleInState0NotOfAge48:
            print 'Test is OK - Male age at state 0 at the end of simulation is 48'
        else:
            print 'Test FAILURE - Male age at state 0 at the end of simulation is not 48'
            BeepForError()
            CriticalTestFailed = True
    
        self.RecordSimResults('Example006-Male', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, MaleInState0NotOfAge48)
    
        print 'Testing Female population'
        OtherTestFailed = False
        CriticalTestFailed = False
        FemaleData = filter (lambda Entry: Entry[3] == 0, FinalData )
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FemaleData, [5,6,7,8], [6149.460 ,  3671.033 ,  176.761  , 2.747] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        FemaleInState0NotOfAge63 = filter (lambda Entry: Entry[5] == 1 and Entry[4] != 63, FemaleData ) ==[]
        if FemaleInState0NotOfAge63 :
            print 'Test is OK - Female age at state 0 at the end of simulation is 63'
        else:
            print 'Test FAILURE - Female age at state 0 at the end of simulation is not 63'
            BeepForError()
            CriticalTestFailed = True
    
        self.RecordSimResults('Example006-Female', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, FemaleInState0NotOfAge63)
    

        return CriticalTestFailed
    
    
    def RunTestExample7(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 7                ######'
        print '########################################################################'
        print '########################################################################'
        # Prepare the project for simulation:
        ExampleNumber = 1070
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        print 'Testing Male population'
        OtherTestFailed = False
        CriticalTestFailed = False
        MaleData = filter (lambda Entry: Entry[3] == 1, FinalData )
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( MaleData, [5,6,7], [380.0611 , 292.4802 , 327.4586] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        MaleInState0NotOfAge48 = filter (lambda Entry: Entry[5] == 1 and Entry[4] != 48, MaleData ) ==[]
        if MaleInState0NotOfAge48:
            print 'Test is OK - Male age at state 0 at the end of simulation is 48'
        else:
            print 'Test FAILURE - Male age at state 0 at the end of simulation is not 48'
            BeepForError()
            CriticalTestFailed = True
    
        self.RecordSimResults('Example007-Male', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, MaleInState0NotOfAge48)
    
        print 'Testing Female population'
        OtherTestFailed = False
        CriticalTestFailed = False
        FemaleData = filter (lambda Entry: Entry[3] == 0, FinalData )
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FemaleData, [5,6,7], [447.1718 , 303.2561 , 249.5721] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        FemaleInState0NotOfAge63 = filter (lambda Entry: Entry[5] == 1 and Entry[4] != 63, FemaleData ) ==[]
        if FemaleInState0NotOfAge63 :
            print 'Test is OK - Female age at state 0 at the end of simulation is 63'
        else:
            print 'Test FAILURE - Female age at state 0 at the end of simulation is not 63'
            BeepForError()
            CriticalTestFailed = True
    
        self.RecordSimResults('Example007-Female', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, FemaleInState0NotOfAge63)
    

        return CriticalTestFailed
    
    
    def RunTestExample8(self):
        
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 8                ######'
        print '########################################################################'
        print '########################################################################'
        # Prepare the project for simulation:
        ExampleNumber = 1080
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        # Age in all alive people should be 33.
        AliveRecords = filter(lambda Entry: Entry[4] == 1 , FinalData)
        IsAgeOfAliveEquals33 = all(map ( lambda Entry: Entry[3] == 33, AliveRecords))
        if IsAgeOfAliveEquals33:
            print 'Simulation Script of Example 8 is OK - Age in all alive people is 33'
        else:
            print 'Test FAILURE - Simulation Script of Example 8 is invalid - Age in all alive people is not 33'
            BeepForError()
            CriticalTestFailed = True
           
        # Average age at death =  31.2540
        DeadRecords = filter(lambda Entry: Entry[5] == 1 , FinalData)
        AgeAtDeath = map ( lambda Entry: Entry[3], DeadRecords)
        AverageAgeAtDeath = reduce (lambda a,b: a+b, AgeAtDeath, 0.0) / len(AgeAtDeath)
        print 'Example 8 - Average Age at death is ' + str(AverageAgeAtDeath)
        if abs(AverageAgeAtDeath - 31.2540) < 0.1:
            print 'Simulation Script of Example 8 is OK - close to 32.1727'
        else:
            print 'Statistical Test FAILURE - Simulation Script of Example 8 is invalid - Average age in death is not close enough to 31.2540'
            BeepForError(1)
            OtherTestFailed = True
    
        IndexOfEventIndicator = ResultsInfo.DataColumns.index('EventState')
        SimulationResultsData = ResultsInfo.Data
    
        # The Event state indicator is never set in the results
        StarterDummyEventNeverUsed = all(map(lambda DataRecord: DataRecord[IndexOfEventIndicator] == 0 , SimulationResultsData))
        if StarterDummyEventNeverUsed:
            print 'Example 8 OK - Starter dummy event state is never used '
        else:
            print 'Example 8 FAILURE - Starter dummy event state is set or entered'
            BeepForError()
            CriticalTestFailed = True
            
        # The Entered indicator of the event state remains set at the transition time
        # to the final state. In other words, every change for the same individual must
        # set the entered event state
    
        PreviousRecord = SimulationResultsData[0]
        ErrorRecordsNum = []
        for (Enum, DataRecord) in enumerate(SimulationResultsData):
            if PreviousRecord[0:2] == DataRecord[0:2] and PreviousRecord[3:] != DataRecord[3:] and DataRecord[IndexOfEventIndicator+1] == 0:
                ErrorRecordsNum = ErrorRecordsNum + [Enum]
            PreviousRecord = DataRecord
            
        EventStateEnteredEveryTransition = ErrorRecordsNum != []
        if EventStateEnteredEveryTransition:
            print 'Example 8 OK - Event state is Entered in every transition '
        else:
            print 'Example 8 FAILURE - Event state entered indicator is not properly set'
            BeepForError()
            CriticalTestFailed = True
    
    
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [4,5], [719.9587 , 280.0413] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
    
        self.RecordSimResults('Example008', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, IsAgeOfAliveEquals33, AverageAgeAtDeath, StarterDummyEventNeverUsed, EventStateEnteredEveryTransition)
    

        return CriticalTestFailed
    
    
    def RunTestExample9(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 9                ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1090
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        IndexOfEventIndicator = ResultsInfo.DataColumns.index('EventState')
        SimulationResultsData = ResultsInfo.Data
    
        # The Event state indicator is never set in the results
        EventStateNeverSet = all(map(lambda DataRecord: DataRecord[IndexOfEventIndicator] == 0 , SimulationResultsData))
        if EventStateNeverSet:
            print 'Example 9 OK - Starter dummy event state is never used '
        else:
            print 'Example 9 FAILURE - Starter dummy event state is set or entered'
            BeepForError()
            CriticalTestFailed = True
            
    
        # The Entered indicator of the event state remains set at the transition time
        # to the final state. In other words, every change for the same individual must
        # set the entered event state
    
        PreviousRecord = SimulationResultsData[0]
        ErrorRecordsNum = []
        for (Enum, DataRecord) in enumerate(SimulationResultsData):
            if PreviousRecord[0:2] == DataRecord[0:2] and PreviousRecord[3:] != DataRecord[3:] and DataRecord[IndexOfEventIndicator+1] == 0:
                ErrorRecordsNum = ErrorRecordsNum + [Enum]
            PreviousRecord = DataRecord
    
        EventStateEnteredEveryTransition = ErrorRecordsNum != []
        if EventStateEnteredEveryTransition:
            print 'Example 9 OK - Event state is Entered in every transition '
        else:
            print 'Example 9 FAILURE - Event state entered indicator is not properly set'
            BeepForError()
            CriticalTestFailed = True
            
            
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [4,5,6], [139.4714, 595.8942, 264.6345], GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example009', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, EventStateNeverSet, EventStateEnteredEveryTransition)
    

        return CriticalTestFailed
    
    
    def RunTestExample10(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 10               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1100
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        IndexOfAgeIndicator = ResultsInfo.DataColumns.index('Age')
        IndexOfState0Indicator = ResultsInfo.DataColumns.index('State0')
        IndexOfState1Indicator = ResultsInfo.DataColumns.index('State1')
        IndexOfState2Indicator = ResultsInfo.DataColumns.index('State2')
        IndexOfState3TerminalIndicator = ResultsInfo.DataColumns.index('State3Terminal')
        IndexOfSubProcess1Indicator = ResultsInfo.DataColumns.index('Example10SubProcess1')
        IndexOfSubProcess2Indicator = ResultsInfo.DataColumns.index('Example10SubProcess2')
        IndexOfMainProcessIndicator = ResultsInfo.DataColumns.index('Example_10___Main_Process')
        IndexOfSplitterIndicator = ResultsInfo.DataColumns.index('Splitter1')
        IndexOfJoinerIndicator = ResultsInfo.DataColumns.index('Joiner1')
        IndexOfState1EnteredIndicator = ResultsInfo.DataColumns.index('State1_Entered')
        IndexOfState2EnteredIndicator = ResultsInfo.DataColumns.index('State2_Entered')
        IndexOfState3TerminalEnteredIndicator = ResultsInfo.DataColumns.index('State3Terminal_Entered')
        IndexOfSubProcess1EnteredIndicator = ResultsInfo.DataColumns.index('Example10SubProcess1_Entered')
        IndexOfSubProcess2EnteredIndicator = ResultsInfo.DataColumns.index('Example10SubProcess2_Entered')
        IndexOfSplitterEnteredIndicator = ResultsInfo.DataColumns.index('Splitter1_Entered')
        IndexOfJoinerEnteredIndicator = ResultsInfo.DataColumns.index('Joiner1_Entered')
        SimulationResultsData = ResultsInfo.Data
    
    
        # Age in all alive people should be 35.
        AliveRecords = filter(lambda Entry: Entry[IndexOfState3TerminalIndicator] != 1 , FinalData)
        IsAgeOfAliveEquals35 = all( map ( lambda Entry: Entry[IndexOfAgeIndicator] == 35, AliveRecords))
        if IsAgeOfAliveEquals35:
            print 'Simulation Script of Example 10 is OK - Age in all alive people is 35'
        else:
            print 'Test FAILURE - Simulation Script of Example 10 is invalid - Age in all alive people is not 35'
            BeepForError()
            CriticalTestFailed = True
            
    
        print 'The following rule is tested :\n The subprocess indicators for Sp1 and Sp2 are equal'
        SubProcessIndicatorsEqual = all(map(lambda DataRecord: DataRecord[IndexOfSubProcess1Indicator] ==  DataRecord[IndexOfSubProcess2Indicator] , SimulationResultsData))
        if SubProcessIndicatorsEqual:
            print ' Example 10 Test is OK - test successful'
        else:
            print ' Example 10 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The main subprocess indicator is always set'
        MainProcessIndicatorAlwaysSet = all(map(lambda DataRecord: DataRecord[IndexOfMainProcessIndicator] ==  1 , SimulationResultsData))
        if MainProcessIndicatorAlwaysSet:
            print ' Example 10 Test is OK - test successful'
        else:
            print ' Example 10 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n If the state indicator in state 1 or 2 are set, then the other one and the indicators for the subprocesses SP1 and SP2 are also set, unless the indicator for the terminal state is set, in which case, the other one is reset and both subprocess states are reset. All states may be reset'
        StateCorrelationTest = all(map(lambda DataRecord: [DataRecord[IndexOfState1Indicator] , DataRecord[IndexOfState2Indicator] , DataRecord[IndexOfState3TerminalIndicator] , DataRecord[IndexOfSubProcess1Indicator] , DataRecord[IndexOfSubProcess2Indicator]] in [[1,1,0,1,1] , [1,0,1,0,0], [0,1,1,0,0], [0,0,0,0,0]] , SimulationResultsData)) 
        if StateCorrelationTest:
            print ' Example 10 Test is OK - test successful'
        else:
            print ' Example 10 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n If a subprocess indicator in SP1, SP2 are set, then state indicators 1 and 2 are set.'
        StateAndSubProcessTest = all(map(lambda DataRecord: (DataRecord[IndexOfSubProcess1Indicator], DataRecord[IndexOfState1Indicator]) in [ (0,0), (0,1) , (1,1) ] and (DataRecord[IndexOfSubProcess2Indicator], DataRecord[IndexOfState2Indicator]) in [ (0,0), (0,1) , (1,1)], SimulationResultsData))
        if StateAndSubProcessTest:
            print ' Example 10 Test is OK - test successful'
        else:
            print ' Example 10 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The entered indicators of the subprocess and the subprocess states equal to the entered indicator of the splitter state'
        EnteredIndicatorTest = all(map(lambda DataRecord: (DataRecord[IndexOfState1EnteredIndicator] == DataRecord[IndexOfSubProcess1EnteredIndicator] == DataRecord[IndexOfState2EnteredIndicator] == DataRecord[IndexOfSubProcess2EnteredIndicator] == DataRecord[IndexOfSplitterEnteredIndicator] ), SimulationResultsData))
        if EnteredIndicatorTest:
            print ' Example 10 Test is OK - test successful'
        else:
            print ' Example 10 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The indicator of the splitter and joiner states are never set'
        SplitterAndJoinerNeverSet = all(map(lambda DataRecord: (DataRecord[IndexOfSplitterIndicator] , DataRecord[IndexOfJoinerIndicator] ) == (0,0), SimulationResultsData))
        if SplitterAndJoinerNeverSet:
            print ' Example 10 Test is OK - test successful'
        else:
            print ' Example 10 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The entered indicator of the joiner state is equal to the terminal state indicator which is equal to the entered indicator of the terminal state. '
        EnteredJoinerAndTerminalEqual = all(map(lambda DataRecord: ( DataRecord[IndexOfJoinerEnteredIndicator] == DataRecord[IndexOfState3TerminalIndicator] == DataRecord[IndexOfState3TerminalEnteredIndicator] ) , SimulationResultsData))
        if EnteredJoinerAndTerminalEqual:
            print ' Example 10 Test is OK - test succsesful'
        else:
            print ' Example 10 FAILURE - test not succesful'
            BeepForError()
            CriticalTestFailed = True
    
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfState0Indicator,IndexOfSubProcess1Indicator,IndexOfState3TerminalIndicator], [295.2450 ,  295.2450 , 409.5100], GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example010', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, IsAgeOfAliveEquals35, SubProcessIndicatorsEqual, MainProcessIndicatorAlwaysSet, StateCorrelationTest, StateAndSubProcessTest, EnteredIndicatorTest, SplitterAndJoinerNeverSet, EnteredJoinerAndTerminalEqual)
    

        return CriticalTestFailed
    
    
    def RunTestExample11(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 11               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1110
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        IndexOfAgeIndicator = ResultsInfo.DataColumns.index('Age')
        IndexOfState0Indicator = ResultsInfo.DataColumns.index('State0')
        #IndexOfEventState1Indicator = ResultsInfo.DataColumns.index('EventState1')
        IndexOfState2Indicator = ResultsInfo.DataColumns.index('State2')
        IndexOfState3Indicator = ResultsInfo.DataColumns.index('State3')
        #IndexOfEventState4Indicator = ResultsInfo.DataColumns.index('EventState4')
        IndexOfState5TerminalIndicator = ResultsInfo.DataColumns.index('State5Terminal')
        IndexOfSubProcess1Indicator = ResultsInfo.DataColumns.index('Example11SubProcess1')
        IndexOfSubProcess2Indicator = ResultsInfo.DataColumns.index('Example11SubProcess2')
        IndexOfMainProcessIndicator = ResultsInfo.DataColumns.index('Example_11___Main_Process')
        IndexOfSplitterIndicator = ResultsInfo.DataColumns.index('Splitter1')
        IndexOfJoinerIndicator = ResultsInfo.DataColumns.index('Joiner1')
    
        #IndexOfState0EnteredIndicator = ResultsInfo.DataColumns.index('State0_Entered')
        IndexOfEventState1EnteredIndicator = ResultsInfo.DataColumns.index('EventState1_Entered')
        IndexOfState2EnteredIndicator = ResultsInfo.DataColumns.index('State2_Entered')
        IndexOfState3EnteredIndicator = ResultsInfo.DataColumns.index('State3_Entered')
        #IndexOfEventState4EnteredIndicator = ResultsInfo.DataColumns.index('EventState4_Entered')
        IndexOfState5TerminalEnteredIndicator = ResultsInfo.DataColumns.index('State5Terminal_Entered')
        IndexOfSubProcess1EnteredIndicator = ResultsInfo.DataColumns.index('Example11SubProcess1_Entered')
        IndexOfSubProcess2EnteredIndicator = ResultsInfo.DataColumns.index('Example11SubProcess2_Entered')
        #IndexOfMainProcessEnteredIndicator = ResultsInfo.DataColumns.index('Example_11___Main_Process_Entered')
        IndexOfSplitterEnteredIndicator = ResultsInfo.DataColumns.index('Splitter1_Entered')
        IndexOfJoinerEnteredIndicator = ResultsInfo.DataColumns.index('Joiner1_Entered')
    
        SimulationResultsData = ResultsInfo.Data
    
        # Age in all alive people should be 35.
        AliveRecords = filter(lambda Entry: Entry[IndexOfState5TerminalIndicator] != 1 , FinalData)
        IsAgeOfAliveEquals35 = all( map ( lambda Entry: Entry[IndexOfAgeIndicator] == 35, AliveRecords))
        if IsAgeOfAliveEquals35:
            print 'Simulation Script of Example 11 is OK - Age in all alive people is 35'
        else:
            print 'Test FAILURE - Simulation Script of Example 11 is invalid - Age in all alive people is not 35'
            BeepForError()
            OtherTestFailed = True
            
        print 'The following rule is tested :\n The subprocess indicators for Sp1 and Sp2 are equal'
        SubProcessIndicatorsEqual = all(map(lambda DataRecord: DataRecord[IndexOfSubProcess1Indicator] ==  DataRecord[IndexOfSubProcess2Indicator] , SimulationResultsData))
        if SubProcessIndicatorsEqual:
            print ' Example 11 Test is OK - test succsesful'
        else:
            print ' Example 11 FAILURE - test not succesful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The main subprocess indicator is always set'
        MainProcessIndicatorAlwaysSet = all(map(lambda DataRecord: DataRecord[IndexOfMainProcessIndicator] ==  1 , SimulationResultsData))
        if MainProcessIndicatorAlwaysSet:
            print ' Example 11 Test is OK - test succsesful'
        else:
            print ' Example 11 FAILURE - test not succesful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n If the state indicator in state 2 or 3 are set, then the other one and the indicators for the subprocesses SP1 and SP2 are also set, unless the indicator for the terminal state 5 is set, in which case, the other one is reset and both subprocess states are reset. All States may be reset'
        StateCorrelationTest = all(map(lambda DataRecord: [DataRecord[IndexOfState2Indicator] , DataRecord[IndexOfState3Indicator] , DataRecord[IndexOfState5TerminalIndicator] , DataRecord[IndexOfSubProcess1Indicator] , DataRecord[IndexOfSubProcess2Indicator]] in [[1,1,0,1,1] , [1,0,1,0,0], [0,1,1,0,0], [0,0,0,0,0]] , SimulationResultsData)) 
        if StateCorrelationTest:
            print ' Example 11 Test is OK - test succsesful'
        else:
            print ' Example 11 FAILURE - test not succesful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n If a subprocess indicator in SP1, SP2 are set, then state indicators 2 and 3 are set.'
        StateAndSubProcessTest = all(map(lambda DataRecord: (DataRecord[IndexOfSubProcess1Indicator], DataRecord[IndexOfState2Indicator]) in [ (0,0), (0,1) , (1,1) ] and (DataRecord[IndexOfSubProcess2Indicator], DataRecord[IndexOfState3Indicator]) in [ (0,0), (0,1) , (1,1)], SimulationResultsData))
        if StateAndSubProcessTest:
            print ' Example 11 Test is OK - test succsesful'
        else:
            print ' Example 11 FAILURE - test not succesful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n State 3 and state 5 are never set together unless state 2 is reset'
        StateTest = all(map(lambda DataRecord: (DataRecord[IndexOfState2Indicator], DataRecord[IndexOfState3Indicator], DataRecord[IndexOfState5TerminalIndicator]) != (1,1,1) , SimulationResultsData))
        if StateTest:
            print ' Example 11 Test is OK - test succsesful'
        else:
            print ' Example 11 FAILURE - test not succesful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n The entered indicators of the subprocesses and states 1,2,3 equal to the entered indicator of the splitter state'
        EnteredIndicatorTest = all(map(lambda DataRecord: (DataRecord[IndexOfEventState1EnteredIndicator] == DataRecord[IndexOfState2EnteredIndicator] == DataRecord[IndexOfSubProcess1EnteredIndicator] == DataRecord[IndexOfState3EnteredIndicator] == DataRecord[IndexOfSubProcess2EnteredIndicator] == DataRecord[IndexOfSplitterEnteredIndicator] ), SimulationResultsData))
        if EnteredIndicatorTest:
            print ' Example 11 Test is OK - test successful'
        else:
            print ' Example 11 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The indicator of the splitter and joiner states are never set'
        SplitterAndJoinerNeverSet = all(map(lambda DataRecord: (DataRecord[IndexOfSplitterIndicator] , DataRecord[IndexOfJoinerIndicator] ) == (0,0), SimulationResultsData))
        if SplitterAndJoinerNeverSet:
            print ' Example 11 Test is OK - test successful'
        else:
            print ' Example 11 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The entered indicator of the joiner state is equal to the terminal state indicator which is equal to the entered indicator of the terminal state. '
        EnteredJoinerAndTerminalEqual = all(map(lambda DataRecord: ( DataRecord[IndexOfJoinerEnteredIndicator] == DataRecord[IndexOfState5TerminalIndicator] == DataRecord[IndexOfState5TerminalEnteredIndicator] ) , SimulationResultsData))
        if EnteredJoinerAndTerminalEqual:
            print ' Example 11 Test is OK - test successful'
        else:
            print ' Example 11 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfState0Indicator,IndexOfSubProcess1Indicator,IndexOfState5TerminalIndicator], [295.2450 ,  295.2450 , 409.5100], GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example011', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, IsAgeOfAliveEquals35, SubProcessIndicatorsEqual, MainProcessIndicatorAlwaysSet, StateCorrelationTest, StateAndSubProcessTest, StateTest, EnteredIndicatorTest, SplitterAndJoinerNeverSet, EnteredJoinerAndTerminalEqual)
    

        return CriticalTestFailed
    
    
    
    def RunTestExample12(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 12               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1120
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        IndexOfAgeIndicator = ResultsInfo.DataColumns.index('Age')
        IndexOfState0Indicator = ResultsInfo.DataColumns.index('State0')
        IndexOfState1Indicator = ResultsInfo.DataColumns.index('State1')
        IndexOfState2Indicator = ResultsInfo.DataColumns.index('State2')
        IndexOfState3Indicator = ResultsInfo.DataColumns.index('State3')
        IndexOfState4Indicator = ResultsInfo.DataColumns.index('State4')
        IndexOfState5Indicator = ResultsInfo.DataColumns.index('State5')
        IndexOfState6TerminalIndicator = ResultsInfo.DataColumns.index('State6Terminal')
        IndexOfSubProcess1Indicator = ResultsInfo.DataColumns.index('Example12SubProcess1')
        IndexOfSubProcess2Indicator = ResultsInfo.DataColumns.index('Example12SubProcess2')
        IndexOfSubProcess3Indicator = ResultsInfo.DataColumns.index('Example12SubProcess3')
        IndexOfSubProcess4Indicator = ResultsInfo.DataColumns.index('Example12SubProcess4')
        IndexOfMainProcessIndicator = ResultsInfo.DataColumns.index('Example_12___Main_Process')
        IndexOfSplitter1Indicator = ResultsInfo.DataColumns.index('Splitter1')
        IndexOfSplitter2Indicator = ResultsInfo.DataColumns.index('Splitter2')
        IndexOfJoiner1Indicator = ResultsInfo.DataColumns.index('Joiner1')
        IndexOfJoiner2Indicator = ResultsInfo.DataColumns.index('Joiner2')
    
    
        #IndexOfState0EnteredIndicator = ResultsInfo.DataColumns.index('State0_Entered')
        IndexOfState1EnteredIndicator = ResultsInfo.DataColumns.index('State1_Entered')
        #IndexOfState2EnteredIndicator = ResultsInfo.DataColumns.index('State2_Entered')
        IndexOfState3EnteredIndicator = ResultsInfo.DataColumns.index('State3_Entered')
        IndexOfState4EnteredIndicator = ResultsInfo.DataColumns.index('State4_Entered')
        #IndexOfState5EnteredIndicator = ResultsInfo.DataColumns.index('State5_Entered')
        IndexOfState6TerminalEnteredIndicator = ResultsInfo.DataColumns.index('State6Terminal_Entered')
        IndexOfSubProcess1EnteredIndicator = ResultsInfo.DataColumns.index('Example12SubProcess1_Entered')
        IndexOfSubProcess2EnteredIndicator = ResultsInfo.DataColumns.index('Example12SubProcess2_Entered')
        IndexOfSubProcess3EnteredIndicator = ResultsInfo.DataColumns.index('Example12SubProcess3_Entered')
        IndexOfSubProcess4EnteredIndicator = ResultsInfo.DataColumns.index('Example12SubProcess4_Entered')
        #IndexOfMainProcessEnteredIndicator = ResultsInfo.DataColumns.index('Example_12___Main_Process_Entered')
        IndexOfSplitter1EnteredIndicator = ResultsInfo.DataColumns.index('Splitter1_Entered')
        IndexOfSplitter2EnteredIndicator = ResultsInfo.DataColumns.index('Splitter2_Entered')
        IndexOfJoiner1EnteredIndicator = ResultsInfo.DataColumns.index('Joiner1_Entered')
        #IndexOfJoiner2EnteredIndicator = ResultsInfo.DataColumns.index('Joiner2_Entered')
    
        SimulationResultsData = ResultsInfo.Data
    
        # Age in all alive people should be 40.
        AliveRecords = filter(lambda Entry: Entry[IndexOfState6TerminalIndicator] != 1 , FinalData)
        IsAgeOfAliveEquals40 = all( map ( lambda Entry: Entry[IndexOfAgeIndicator] == 40, AliveRecords))
        if IsAgeOfAliveEquals40:
            print 'Simulation Script of Example 12 is OK - Age in all alive people is 40'
        else:
            print 'Test FAILURE - Simulation Script of Example 12 is invalid - Age in all alive people is not 40'
            BeepForError()
            CriticalTestFailed = True
    
            
        print 'The following rule is tested :\n The subprocess indicators for Sp1 and Sp2 are equal'
        SubProcessIndicatorsEqual1 = all(map(lambda DataRecord: DataRecord[IndexOfSubProcess1Indicator] ==  DataRecord[IndexOfSubProcess2Indicator] , SimulationResultsData))
        if SubProcessIndicatorsEqual1:
            print ' Example 12 Test is OK - test successful'
        else:
            print ' Example 12 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n The subprocess indicators for Sp3 and Sp4 are equal'
        SubProcessIndicatorsEqual2 = all(map(lambda DataRecord: DataRecord[IndexOfSubProcess3Indicator] ==  DataRecord[IndexOfSubProcess4Indicator] , SimulationResultsData))
        if SubProcessIndicatorsEqual2:
            print ' Example 12 Test is OK - test successful'
        else:
            print ' Example 12 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n The main subprocess indicator is always set'
        MainProcessIndicatorAlwaysSet = all(map(lambda DataRecord: DataRecord[IndexOfMainProcessIndicator] ==  1 , SimulationResultsData))
        if MainProcessIndicatorAlwaysSet:
            print ' Example 12 Test is OK - test successful'
        else:
            print ' Example 12 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n If the state indicator in state 1 or 3 are set, then the indicators for the subprocesses SP1 and SP2 are also set, unless the indicator for the terminal state 6 is set, in which case, both subprocess states are reset. All States may be reset, also both subprocesses may be set together without setting states 1,3.'
        StateCorrelationTest = all(map(lambda DataRecord: [DataRecord[IndexOfState1Indicator] , DataRecord[IndexOfState3Indicator] , DataRecord[IndexOfState6TerminalIndicator] , DataRecord[IndexOfSubProcess1Indicator] , DataRecord[IndexOfSubProcess2Indicator]] in [[1,1,0,1,1] , [1,0,0,1,1] , [0,1,0,1,1] ,[1,0,1,0,0], [0,1,1,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,1,1]] , SimulationResultsData)) 
        if StateCorrelationTest:
            print ' Example 12 Test is OK - test succsesful'
        else:
            print ' Example 12 FAILURE - test not succesful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n If a subprocess indicator in SP1, SP2 are set, then state indicators (1 or 2 ) and (3 or 4 or 5) are set, while 3,4,5 are never set together. Also 2,3,4,5,6 can be set without SP1 and SP2 begin set.'
        StateAndSubProcessTest = all(map(lambda DataRecord: (DataRecord[IndexOfSubProcess1Indicator], DataRecord[IndexOfState1Indicator], DataRecord[IndexOfState2Indicator]) in [ (0,0,0), (0,1,0), (0,0,1) , (1,1,0), (1,0,1) ] and (DataRecord[IndexOfSubProcess2Indicator], DataRecord[IndexOfState3Indicator], DataRecord[IndexOfState4Indicator], DataRecord[IndexOfState5Indicator]) in [ (0,0,0,0), (0,1,1,0), (0,0,1,0), (0,1,0,0), (0,0,0,1), (0,0,1,1), (0,1,0,1), (0,0,0,1), (1,1,1,0), (1,0,1,0), (1,1,0,0), (1,0,0,1), (1,0,1,1), (1,1,0,1), (1,0,0,1) ], SimulationResultsData))
        if StateAndSubProcessTest:
            print ' Example 12 Test is OK - test successful'
        else:
            print ' Example 12 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n State 3 and state 6 are never set together unless state 2 is reset'
        StateTest1 = all(map(lambda DataRecord: (DataRecord[IndexOfState2Indicator], DataRecord[IndexOfState3Indicator], DataRecord[IndexOfState6TerminalIndicator]) != (1,1,1) , SimulationResultsData))
        if StateTest1:
            print ' Example 12 Test is OK - test successful'
        else:
            print ' Example 12 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
    
        print 'The following rule is tested :\n States 3,4,5 are never all set together.'
        StateTest2 = all(map(lambda DataRecord: (DataRecord[IndexOfState5Indicator], DataRecord[IndexOfState3Indicator], DataRecord[IndexOfState4Indicator]) not in ((1,1,1)) , SimulationResultsData))
        if StateTest2:
            print ' Example 12 Test is OK - test successful'
        else:
            print ' Example 12 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n The entered indicators of subprocesses SP1, SP2, SP3, SP4 and states 1,3,4 equal to the entered indicator of the splitter states S1 and S2.'
        EnteredIndicatorTest = all(map(lambda DataRecord: (DataRecord[IndexOfState1EnteredIndicator] == DataRecord[IndexOfState3EnteredIndicator] == DataRecord[IndexOfState4EnteredIndicator] == DataRecord[IndexOfSubProcess1EnteredIndicator] == DataRecord[IndexOfSubProcess2EnteredIndicator] == DataRecord[IndexOfSubProcess3EnteredIndicator] == DataRecord[IndexOfSubProcess4EnteredIndicator] == DataRecord[IndexOfSplitter1EnteredIndicator] == DataRecord[IndexOfSplitter2EnteredIndicator] ), SimulationResultsData))
        if EnteredIndicatorTest:
            print ' Example 12 Test is OK - test successful'
        else:
            print ' Example 12 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The indicator of the splitter and joiner states S1, S2, J1, J2 are never set'
        SplitterAndJoinerNeverSet = all(map(lambda DataRecord: (DataRecord[IndexOfSplitter1Indicator] , DataRecord[IndexOfJoiner1Indicator], DataRecord[IndexOfSplitter2Indicator] , DataRecord[IndexOfJoiner2Indicator] ) == (0,0,0,0), SimulationResultsData))
        if SplitterAndJoinerNeverSet:
            print ' Example 12 Test is OK - test successful'
        else:
            print ' Example 12 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The entered indicator of the joiner state J1 is equal to the terminal state indicator which is equal to the entered indicator of the terminal state 6.'
        EnteredJoinerAndTerminalEqual = all(map(lambda DataRecord: ( DataRecord[IndexOfJoiner1EnteredIndicator] == DataRecord[IndexOfState6TerminalIndicator] == DataRecord[IndexOfState6TerminalEnteredIndicator] ) , SimulationResultsData))
        if EnteredJoinerAndTerminalEqual:
            print ' Example 12 Test is OK - test successful'
        else:
            print ' Example 12 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfState0Indicator,IndexOfState1Indicator,IndexOfState2Indicator,IndexOfState6TerminalIndicator], [174.3392 , 125.6437 , 157.7785 , 542.2386], GlobalAllowedDeviationInSTD , [IndexOfMainProcessIndicator, IndexOfSubProcess1Indicator, IndexOfSubProcess1Indicator, IndexOfMainProcessIndicator])
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example012', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, IsAgeOfAliveEquals40, SubProcessIndicatorsEqual1, SubProcessIndicatorsEqual2, MainProcessIndicatorAlwaysSet, StateCorrelationTest, StateAndSubProcessTest, StateTest1, StateTest2, EnteredIndicatorTest, SplitterAndJoinerNeverSet, EnteredJoinerAndTerminalEqual)
    

        return CriticalTestFailed
    
    
    def RunTestExample13(self):
        
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 13               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1130
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        IndexOfAgeIndicator = ResultsInfo.DataColumns.index('Age')
        IndexOfState0Indicator = ResultsInfo.DataColumns.index('State0')
        IndexOfState1Indicator = ResultsInfo.DataColumns.index('State1')
        IndexOfState2Indicator = ResultsInfo.DataColumns.index('State2')
        IndexOfState3Indicator = ResultsInfo.DataColumns.index('State3')
        IndexOfState4Indicator = ResultsInfo.DataColumns.index('State4')
        IndexOfState5Indicator = ResultsInfo.DataColumns.index('State5')
        IndexOfState6TerminalIndicator = ResultsInfo.DataColumns.index('State6Terminal')
        IndexOfSubProcess1Indicator = ResultsInfo.DataColumns.index('Example13SubProcess1')
        IndexOfSubProcess2Indicator = ResultsInfo.DataColumns.index('Example13SubProcess2')
        IndexOfSubProcess3Indicator = ResultsInfo.DataColumns.index('Example13SubProcess3')
        IndexOfSubProcess4Indicator = ResultsInfo.DataColumns.index('Example13SubProcess4')
        IndexOfMainProcessIndicator = ResultsInfo.DataColumns.index('Example_13___Main_Process')
        IndexOfSplitter1Indicator = ResultsInfo.DataColumns.index('Splitter1')
        IndexOfSplitter2Indicator = ResultsInfo.DataColumns.index('Splitter2')
        IndexOfJoiner1Indicator = ResultsInfo.DataColumns.index('Joiner1')
        IndexOfJoiner2Indicator = ResultsInfo.DataColumns.index('Joiner2')
    
    
        #IndexOfState0EnteredIndicator = ResultsInfo.DataColumns.index('State0_Entered')
        IndexOfState1EnteredIndicator = ResultsInfo.DataColumns.index('State1_Entered')
        #IndexOfState2EnteredIndicator = ResultsInfo.DataColumns.index('State2_Entered')
        IndexOfState3EnteredIndicator = ResultsInfo.DataColumns.index('State3_Entered')
        IndexOfState4EnteredIndicator = ResultsInfo.DataColumns.index('State4_Entered')
        #IndexOfState5EnteredIndicator = ResultsInfo.DataColumns.index('State5_Entered')
        IndexOfState6TerminalEnteredIndicator = ResultsInfo.DataColumns.index('State6Terminal_Entered')
        IndexOfSubProcess1EnteredIndicator = ResultsInfo.DataColumns.index('Example13SubProcess1_Entered')
        IndexOfSubProcess2EnteredIndicator = ResultsInfo.DataColumns.index('Example13SubProcess2_Entered')
        IndexOfSubProcess3EnteredIndicator = ResultsInfo.DataColumns.index('Example13SubProcess3_Entered')
        IndexOfSubProcess4EnteredIndicator = ResultsInfo.DataColumns.index('Example13SubProcess4_Entered')
        #IndexOfMainProcessEnteredIndicator = ResultsInfo.DataColumns.index('Example_13___Main_Process_Entered')
        IndexOfSplitter1EnteredIndicator = ResultsInfo.DataColumns.index('Splitter1_Entered')
        IndexOfSplitter2EnteredIndicator = ResultsInfo.DataColumns.index('Splitter2_Entered')
        IndexOfJoiner1EnteredIndicator = ResultsInfo.DataColumns.index('Joiner1_Entered')
        #IndexOfJoiner2EnteredIndicator = ResultsInfo.DataColumns.index('Joiner2_Entered')
    
        SimulationResultsData = ResultsInfo.Data
    
        # Age in all alive people should be 40.
        AliveRecords = filter(lambda Entry: Entry[IndexOfState6TerminalIndicator] != 1 , FinalData)
        IsAgeOfAliveEquals40 = all( map ( lambda Entry: Entry[IndexOfAgeIndicator] == 40, AliveRecords))
        if IsAgeOfAliveEquals40:
            print 'Simulation Script of Example 13 is OK - Age in all alive people is 40'
        else:
            print 'Test FAILURE - Simulation Script of Example 13 is invalid - Age in all alive people is not 40'
            BeepForError()
            CriticalTestFailed = True
    
            
        print 'The following rule is tested :\n The subprocess indicators for Sp1 and Sp2 are equal'
        SubProcessIndicatorsEqual1 = all(map(lambda DataRecord: DataRecord[IndexOfSubProcess1Indicator] ==  DataRecord[IndexOfSubProcess2Indicator] , SimulationResultsData))
        if SubProcessIndicatorsEqual1:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n The subprocess indicators for Sp3 and Sp4 are equal'
        SubProcessIndicatorsEqual2 = all(map(lambda DataRecord: DataRecord[IndexOfSubProcess3Indicator] ==  DataRecord[IndexOfSubProcess4Indicator] , SimulationResultsData))
        if SubProcessIndicatorsEqual2:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n The main subprocess indicator is always set'
        MainProcessIndicatorAlwaysSet = all(map(lambda DataRecord: DataRecord[IndexOfMainProcessIndicator] ==  1 , SimulationResultsData))
        if MainProcessIndicatorAlwaysSet:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n If the state indicator in state 1 or 3 are set, then the indicators for the subprocesses SP1 and SP2 are also set, unless the indicator for the terminal state 6 is set, in which case, both subprocess states are reset. All States may be reset, also both subprocesses may be set together without setting states 1,3.'
        StateCorrelationTest = all(map(lambda DataRecord: [DataRecord[IndexOfState1Indicator] , DataRecord[IndexOfState3Indicator] , DataRecord[IndexOfState6TerminalIndicator] , DataRecord[IndexOfSubProcess1Indicator] , DataRecord[IndexOfSubProcess2Indicator]] in [[1,1,0,1,1] , [1,0,0,1,1] , [0,1,0,1,1] ,[1,0,1,0,0], [0,1,1,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,1,1]] , SimulationResultsData)) 
        if StateCorrelationTest:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n If a subprocess indicator in SP1, SP2 are set, then state indicators (1 or 2 ) and (3 or 4 or 5) are set, while 3,4,5 are never set together. Also 2,3,4,5,6 can be set without SP1 and SP2 begin set.'
        StateAndSubProcessTest = all(map(lambda DataRecord: (DataRecord[IndexOfSubProcess1Indicator], DataRecord[IndexOfState1Indicator], DataRecord[IndexOfState2Indicator]) in [ (0,0,0), (0,1,0), (0,0,1) , (1,1,0), (1,0,1) ] and (DataRecord[IndexOfSubProcess2Indicator], DataRecord[IndexOfState3Indicator], DataRecord[IndexOfState4Indicator], DataRecord[IndexOfState5Indicator]) in [ (0,0,0,0), (0,1,1,0), (0,0,1,0), (0,1,0,0), (0,0,0,1), (0,0,1,1), (0,1,0,1), (0,0,0,1), (1,1,1,0), (1,0,1,0), (1,1,0,0), (1,0,0,1), (1,0,1,1), (1,1,0,1), (1,0,0,1) ], SimulationResultsData))
        if StateAndSubProcessTest:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n State 3 and state 6 are never set together unless state 2 is reset'
        StateTest1 = all(map(lambda DataRecord: (DataRecord[IndexOfState2Indicator], DataRecord[IndexOfState3Indicator], DataRecord[IndexOfState6TerminalIndicator]) != (1,1,1) , SimulationResultsData))
        if StateTest1:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
    
        print 'The following rule is tested :\n States 3,4,5 are never all set together.'
        StateTest2 = all(map(lambda DataRecord: (DataRecord[IndexOfState5Indicator], DataRecord[IndexOfState3Indicator], DataRecord[IndexOfState4Indicator]) not in ((1,1,1)) , SimulationResultsData))
        if StateTest2:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
    
        print 'The following rule is tested :\n The entered indicators of subprocesses SP1, SP2, SP3, SP4 and states 1,3,4 equal to the entered indicator of the splitter states S1 and S2.'
        EnteredIndicatorTest = all(map(lambda DataRecord: (DataRecord[IndexOfState1EnteredIndicator] == DataRecord[IndexOfState3EnteredIndicator] == DataRecord[IndexOfState4EnteredIndicator] == DataRecord[IndexOfSubProcess1EnteredIndicator] == DataRecord[IndexOfSubProcess2EnteredIndicator] == DataRecord[IndexOfSubProcess3EnteredIndicator] == DataRecord[IndexOfSubProcess4EnteredIndicator] == DataRecord[IndexOfSplitter1EnteredIndicator] == DataRecord[IndexOfSplitter2EnteredIndicator] ), SimulationResultsData))
        if EnteredIndicatorTest:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The indicator of the splitter and joiner states S1, S2, J1, J2 are never set'
        SplitterAndJoinerNeverSet = all(map(lambda DataRecord: (DataRecord[IndexOfSplitter1Indicator] , DataRecord[IndexOfJoiner1Indicator], DataRecord[IndexOfSplitter2Indicator] , DataRecord[IndexOfJoiner2Indicator] ) == (0,0,0,0), SimulationResultsData))
        if SplitterAndJoinerNeverSet:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n The entered indicator of the joiner state J1 is equal to the terminal state indicator which is equal to the entered indicator of the terminal state 6.'
        EnteredJoinerAndTerminalEqual = all(map(lambda DataRecord: ( DataRecord[IndexOfJoiner1EnteredIndicator] == DataRecord[IndexOfState6TerminalIndicator] == DataRecord[IndexOfState6TerminalEnteredIndicator] ) , SimulationResultsData))
        if EnteredJoinerAndTerminalEqual:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        print 'The following rule is tested :\n If State 6 is set then either State 5 or State 4 are also set.  In other words, there is no path from state 5 to state 6 and State 6 can be reached only from state 2'
        EnteredJoinerAndTerminalEqual = all(map(lambda DataRecord: ( DataRecord[IndexOfState4Indicator] , DataRecord[IndexOfState5Indicator] , DataRecord[IndexOfState6TerminalIndicator] ) != (0,0,1) , SimulationResultsData))
        if EnteredJoinerAndTerminalEqual:
            print ' Example 13 Test is OK - test successful'
        else:
            print ' Example 13 FAILURE - test not successful'
            BeepForError()
            CriticalTestFailed = True
    
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfState0Indicator,IndexOfState1Indicator,IndexOfState2Indicator,IndexOfState6TerminalIndicator], [174.3392, 174.3392 , 160.2155 , 491.1061], GlobalAllowedDeviationInSTD , [IndexOfMainProcessIndicator, IndexOfSubProcess1Indicator, IndexOfSubProcess1Indicator, IndexOfMainProcessIndicator])
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example013', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, IsAgeOfAliveEquals40, SubProcessIndicatorsEqual1, SubProcessIndicatorsEqual2, MainProcessIndicatorAlwaysSet, StateCorrelationTest, StateAndSubProcessTest, StateTest1, StateTest2, EnteredIndicatorTest, SplitterAndJoinerNeverSet, EnteredJoinerAndTerminalEqual)
    

        return CriticalTestFailed
    
    
    
    def RunTestExample14(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 14               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1140
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
     
        IndexOfEventState1EnteredIndicator = ResultsInfo.DataColumns.index('EventState1_Entered')
        IndexOfEventState1Indicator = ResultsInfo.DataColumns.index('EventState1')
        IndexOfEventState2EnteredIndicator = ResultsInfo.DataColumns.index('EventState2_Entered')
        IndexOfEventState2Indicator = ResultsInfo.DataColumns.index('EventState2')
        IndexOfState3Indicator = ResultsInfo.DataColumns.index('State3')
        IndexOfState4TerminalIndicator = ResultsInfo.DataColumns.index('State4Terminal')
    
    
        IsStatesCorrect = all(map ( lambda DataRecord: ( DataRecord[IndexOfEventState1EnteredIndicator], DataRecord[IndexOfEventState1Indicator], DataRecord[IndexOfEventState2EnteredIndicator], DataRecord[IndexOfEventState2Indicator], DataRecord[IndexOfState3Indicator], DataRecord[IndexOfState4TerminalIndicator] ) == (1, 0, 1, 0, 1, 0), FinalData))
        
        if IsStatesCorrect:
            print 'Simulation Script of Example 14 is OK - test successful'
        else:
            print 'Test FAILURE - Simulation Script of Example 14 is invalid - test not successful'
            BeepForError()
            CriticalTestFailed = True


        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfEventState1EnteredIndicator , IndexOfEventState1Indicator , IndexOfEventState2EnteredIndicator , IndexOfEventState2Indicator , IndexOfState3Indicator , IndexOfState4TerminalIndicator ], [100,0,100,0,100,0], GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example014', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, IsStatesCorrect)
   

        return CriticalTestFailed
    
    
    def RunTestExample15(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 15               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1150
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        IndexOfAgeIndicator = ResultsInfo.DataColumns.index('Age')
        IndexOfAgeAtStartIndicator = ResultsInfo.DataColumns.index('AgeAtStart')
        IndexOfGenderIndicator = ResultsInfo.DataColumns.index('Gender')
        IndexOfState0Indicator = ResultsInfo.DataColumns.index('State0')
        IndexOfState1TerminalIndicator = ResultsInfo.DataColumns.index('State1Terminal')
    
        #IndexOfState0EnteredIndicator = ResultsInfo.DataColumns.index('State0_Entered')
        #IndexOfState1TerminalEnteredIndicator = ResultsInfo.DataColumns.index('State1Terminal_Entered')
    
    
        # Age in all alive people should be either 8,28,48.
        AliveRecords = filter(lambda Entry: Entry[IndexOfState1TerminalIndicator] != 1 , FinalData)
        IsAgeOfAliveOK = all(map ( lambda Entry: Entry[IndexOfAgeIndicator] in [8,28,48], AliveRecords))
        if IsAgeOfAliveOK:
            print 'Simulation Script of Example 15 is OK - Age in all alive people is either 8,28, or 48'
        else:
            print 'Test FAILURE - Simulation Script of Example 15 is invalid - Age in all alive people is not is not 8,28, or 48'
            BeepForError()
            CriticalTestFailed = True
    
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfState0Indicator,IndexOfState1TerminalIndicator], [ 198.9000 , 401.1000] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example015', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, IsAgeOfAliveOK)
    
        GenderIs0Records = filter(lambda Entry: Entry[IndexOfGenderIndicator] == 0 , FinalData)
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( GenderIs0Records, [IndexOfState0Indicator,IndexOfState1TerminalIndicator], [158.4000 , 141.6000] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example015-GenderIs0', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    
        AgeGroup1Records = filter(lambda Entry: Entry[IndexOfAgeAtStartIndicator] <= 20 , FinalData)
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( AgeGroup1Records, [IndexOfState0Indicator,IndexOfState1TerminalIndicator], [94.5000 , 105.5000] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example015-AgeGroup1', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    
        AgeGroup2Records = filter(lambda Entry: 20< Entry[IndexOfAgeAtStartIndicator] <= 40 , FinalData)
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( AgeGroup2Records, [IndexOfState0Indicator,IndexOfState1TerminalIndicator], [63.7000 , 136.3000] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example015-AgeGroup2', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    

        return CriticalTestFailed
    
    
    
    def RunTestExample16(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 16               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1160
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
     
    
        IndexOfBPIndicator = ResultsInfo.DataColumns.index('BP')
        IndexOfState1Indicator = ResultsInfo.DataColumns.index('State1')
        IndexOfState2Indicator = ResultsInfo.DataColumns.index('State2')
        IndexOfState3Indicator = ResultsInfo.DataColumns.index('State3')
        IndexOfState4Indicator = ResultsInfo.DataColumns.index('State4')
        IndexOfState5Indicator = ResultsInfo.DataColumns.index('State5')
        IndexOfState6Indicator = ResultsInfo.DataColumns.index('State6')
        IndexOfState7Indicator = ResultsInfo.DataColumns.index('State7')
        IndexOfState8Indicator = ResultsInfo.DataColumns.index('State8')
        IndexOfState9Indicator = ResultsInfo.DataColumns.index('State9')
        IndexOfState10Indicator = ResultsInfo.DataColumns.index('State10')
        IndexOfState11Indicator = ResultsInfo.DataColumns.index('State11')
        IndexOfState12Indicator = ResultsInfo.DataColumns.index('State12')
        IndexOfState13Indicator = ResultsInfo.DataColumns.index('State13')
        IndexOfState14Indicator = ResultsInfo.DataColumns.index('State14')
        IndexOfState15Indicator = ResultsInfo.DataColumns.index('State15')
        IndexOfState16Indicator = ResultsInfo.DataColumns.index('State16')
    
    
        IsBPEquals8 = all(map ( lambda Entry: Entry[IndexOfBPIndicator] == 8, FinalData))
        if IsBPEquals8:
            print 'Simulation Script of Example 16 is OK - BP is 8'
        else:
            print 'Test FAILURE - Simulation Script of Example 16 is invalid - BP is not 8'
            BeepForError()
            CriticalTestFailed = True
    
              
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfState1Indicator, IndexOfState2Indicator, IndexOfState3Indicator, IndexOfState4Indicator, IndexOfState5Indicator, IndexOfState6Indicator, IndexOfState7Indicator, IndexOfState8Indicator, IndexOfState9Indicator, IndexOfState10Indicator, IndexOfState11Indicator, IndexOfState12Indicator, IndexOfState13Indicator, IndexOfState14Indicator,  IndexOfState15Indicator, IndexOfState16Indicator], [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example016', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    

        return CriticalTestFailed
    
    
    def RunTestExample17(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 17               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1170
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        
        SimulationResultsData = ResultsInfo.Data
     
        IndexOfTime = ResultsInfo.DataColumns.index('Time')
        IndexOfAgeIndicator = ResultsInfo.DataColumns.index('Age')
        IndexOfEx17TestCovariateIndicator = ResultsInfo.DataColumns.index('Ex17TestCovariate')
        IndexOfEx17TestCovariate2Indicator = ResultsInfo.DataColumns.index('Ex17TestCovariate2')
        IndexOfState0Indicator = ResultsInfo.DataColumns.index('State0')
        IndexOfState1Indicator = ResultsInfo.DataColumns.index('State1')
        IndexOfState2Indicator = ResultsInfo.DataColumns.index('State2')
        IndexOfState2DiagnosedIndicator = ResultsInfo.DataColumns.index('State2_Diagnosed')
        IndexOfState3TerminalIndicator = ResultsInfo.DataColumns.index('State3Terminal')
    
        SimulationParametersValid = all(map ( lambda DataRecord: ( DataRecord[IndexOfTime], DataRecord[IndexOfAgeIndicator], DataRecord[IndexOfState0Indicator], DataRecord[IndexOfState1Indicator], DataRecord[IndexOfState2Indicator], DataRecord[IndexOfState3TerminalIndicator], DataRecord[IndexOfState2DiagnosedIndicator], DataRecord[IndexOfEx17TestCovariateIndicator], DataRecord[IndexOfEx17TestCovariate2Indicator]) in [( 0, 30, 1, 0, 0, 0, 0, 0, 0 ), ( 1, 31, 0, 1, 0, 0, 0, 1, 1 ), ( 2, 32, 0, 1, 0, 0, 0, 1, 1 ), ( 3, 33, 0, 0, 1, 0, 0, 1, 1 ), ( 4, 34, 0, 0, 1, 0, 0, 1, 1 ), ( 5, 35, 0, 0, 1, 0, 1, 1, 1 ), ( 6, 36, 0, 0, 0, 1, 1, 1, 1 )], SimulationResultsData))
    
       
        if SimulationParametersValid:
            print 'Simulation Script of Example 17 is OK - Test parameters are all correct'
        else:
            print 'Test FAILURE - Simulation Script of Example 17 is invalid - Test parameters are not all correct'
            BeepForError()
            CriticalTestFailed = True
    
    
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfState0Indicator, IndexOfState1Indicator, IndexOfState2Indicator, IndexOfState3TerminalIndicator], [0, 0, 0, 50] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example017', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    

        return CriticalTestFailed
    
    
    def RunTestExample18(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 18               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1180
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        
        SimulationResultsData = ResultsInfo.Data
     
        IndexOfAgeIndicator = ResultsInfo.DataColumns.index('Age')
        IndexOfEx18TestQoLIndicator = ResultsInfo.DataColumns.index('Ex18TestQoL')
        IndexOfEx18TestCostIndicator = ResultsInfo.DataColumns.index('Ex18TestCost')
        IndexOfState0Indicator = ResultsInfo.DataColumns.index('State0')
        IndexOfState1Indicator = ResultsInfo.DataColumns.index('State1')
        IndexOfState2Indicator = ResultsInfo.DataColumns.index('State2')
        IndexOfState3TerminalIndicator = ResultsInfo.DataColumns.index('State3Terminal')
    
    
        State0Records = filter(lambda Entry: Entry[IndexOfState0Indicator] == 1 , SimulationResultsData)
        State1Records = filter(lambda Entry: Entry[IndexOfState1Indicator] == 1 , SimulationResultsData)
        State2Records = filter(lambda Entry: Entry[IndexOfState2Indicator] == 1 , SimulationResultsData)
        State3Records = filter(lambda Entry: Entry[IndexOfState3TerminalIndicator] == 1 , SimulationResultsData)
        State1AgeLe31Records = filter(lambda Entry: Entry[IndexOfAgeIndicator] <= 31, State1Records)
        State1AgeGr31Records = filter(lambda Entry: Entry[IndexOfAgeIndicator] > 31, State1Records)
        State2AgeLe33Records = filter(lambda Entry: Entry[IndexOfAgeIndicator] <= 33, State2Records)
        State2AgeGr33Records = filter(lambda Entry: Entry[IndexOfAgeIndicator] > 33, State2Records)
    
        IsQoLCorrectA = all(map ( lambda Entry: Entry[IndexOfEx18TestQoLIndicator] == 0.6, State1AgeGr31Records))
        IsQoLCorrectB = all(map ( lambda Entry: Entry[IndexOfEx18TestQoLIndicator] == 0.7, State2AgeGr33Records))
        IsQoLCorrectC = all(map ( lambda Entry: Entry[IndexOfEx18TestQoLIndicator] == 0.5, State3Records + State1AgeLe31Records + State2AgeLe33Records))
        IsQoLCorrectD = all(map ( lambda Entry: Entry[IndexOfEx18TestQoLIndicator] == 0.1, State0Records ))
    
        IsCostCorrectA = all(map ( lambda Entry: Entry[IndexOfEx18TestCostIndicator] == 100000, State1AgeGr31Records))
        IsCostCorrectB = all(map ( lambda Entry: Entry[IndexOfEx18TestCostIndicator] == 10000, State2AgeGr33Records))
        IsCostCorrectC = all(map ( lambda Entry: Entry[IndexOfEx18TestCostIndicator] == 100, State3Records + State1AgeLe31Records + State2AgeLe33Records))
        IsCostCorrectD = all(map ( lambda Entry: Entry[IndexOfEx18TestCostIndicator] == 10, State0Records ))
        
    
        if IsQoLCorrectA:
            print 'Simulation Script of Example 18 is OK - QoL is correct in test A'
        else:
            print 'Test FAILURE - Simulation Script of Example 18 is invalid - QoL is incorrect in test A'
            BeepForError(1)
            CriticalTestFailed = True
            
        if IsQoLCorrectB:
            print 'Simulation Script of Example 18 is OK - QoL is correct in test B'
        else:
            print 'Test FAILURE - Simulation Script of Example 18 is invalid - QoL is incorrect in test B'
            BeepForError(1)
            CriticalTestFailed = True
            
        if IsQoLCorrectC:
            print 'Simulation Script of Example 18 is OK - QoL is correct in test C'
        else:
            print 'Test FAILURE - Simulation Script of Example 18 is invalid - QoL is incorrect in test C'
            BeepForError(1)
            CriticalTestFailed = True
    
        if IsQoLCorrectD:
            print 'Simulation Script of Example 18 is OK - QoL is correct in test D'
        else:
            print 'Test FAILURE - Simulation Script of Example 18 is invalid - QoL is incorrect in test D'
            BeepForError(1)
            CriticalTestFailed = True
    
            
        if IsCostCorrectA:
            print 'Simulation Script of Example 18 is OK - Cost is correct in test A'
        else:
            print 'Test FAILURE - Simulation Script of Example 18 is invalid - Cost is incorrect in test A'
            BeepForError(1)
            CriticalTestFailed = True
            
        if IsCostCorrectB:
            print 'Simulation Script of Example 18 is OK - Cost is correct in test B'
        else:
            print 'Test FAILURE - Simulation Script of Example 18 is invalid - Cost is incorrect in test B'
            BeepForError(1)
            CriticalTestFailed = True
            
        if IsCostCorrectC:
            print 'Simulation Script of Example 18 is OK - Cost is correct in test C'
        else:
            print 'Test FAILURE - Simulation Script of Example 18 is invalid - Cost is incorrect in test C'
            BeepForError(1)
            CriticalTestFailed = True
    
        if IsCostCorrectD:
            print 'Simulation Script of Example 18 is OK - Cost is correct in test D'
        else:
            print 'Test FAILURE - Simulation Script of Example 18 is invalid - Cost is incorrect in test D'
            BeepForError(1)
            CriticalTestFailed = True
        
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfState0Indicator, IndexOfState1Indicator, IndexOfState2Indicator, IndexOfState3TerminalIndicator], [0, 6.2500, 25.0000, 68.7500] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example018', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    

        return CriticalTestFailed
    
    
    
    def RunTestExample19(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 19               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1190
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
    
        IndexOfState1Indicator = ResultsInfo.DataColumns.index('State1')
        IndexOfState2Indicator = ResultsInfo.DataColumns.index('State2')
        IndexOfState3Indicator = ResultsInfo.DataColumns.index('State3')
        IndexOfState4Indicator = ResultsInfo.DataColumns.index('State4')
        IndexOfState5Indicator = ResultsInfo.DataColumns.index('State5')
        IndexOfState6Indicator = ResultsInfo.DataColumns.index('State6')
        IndexOfState7Indicator = ResultsInfo.DataColumns.index('State7')
        IndexOfState8Indicator = ResultsInfo.DataColumns.index('State8')
        IndexOfState9Indicator = ResultsInfo.DataColumns.index('State9')
        IndexOfState10Indicator = ResultsInfo.DataColumns.index('State10')
        IndexOfTestCov1Indicator = ResultsInfo.DataColumns.index('TestCov1')
        IndexOfTestCov2Indicator = ResultsInfo.DataColumns.index('TestCov2')
        IndexOfTestCov3Indicator = ResultsInfo.DataColumns.index('TestCov3')
        IndexOfTestCov4Indicator = ResultsInfo.DataColumns.index('TestCov4')
        IndexOfTestCov5Indicator = ResultsInfo.DataColumns.index('TestCov5')
    
    
            
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfState1Indicator, IndexOfState2Indicator, IndexOfState3Indicator, IndexOfState4Indicator, IndexOfState5Indicator, IndexOfState6Indicator, IndexOfState7Indicator, IndexOfState8Indicator, IndexOfState9Indicator, IndexOfState10Indicator, IndexOfTestCov1Indicator, IndexOfTestCov2Indicator, IndexOfTestCov3Indicator, IndexOfTestCov4Indicator, IndexOfTestCov5Indicator ], [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500] , GlobalAllowedDeviationInSTD, None, [1]*10 + 5*[0])
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example019', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    

        return CriticalTestFailed
    
    
    
    def RunTestExample20(self):
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 20               ######'
        print '########################################################################'
        print '########################################################################'
    
        # Prepare the project for simulation:
        ExampleNumber = 1200
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        # in this example generate a population set
        DistributionPopulationSet = DB.PopulationSets[DB.Projects[ExampleNumber].PrimaryPopulationSetID]
        PopulationSizeToGenerate = DB.Projects[ExampleNumber].NumberOfRepetitions
        GeneratedPopulationSet = DistributionPopulationSet.GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = PopulationSizeToGenerate)
        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = 1, OverridePopulationSet = GeneratedPopulationSet)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        # Age of all people should be between 20 and 43.
        IsAgeBewtween20And43 = all(map ( lambda Entry: 20 <= Entry[3] <= 43, ResultsInfo.Data))
        if IsAgeBewtween20And43:
            print 'Simulation Script of Example 20 is OK - Age in people is between 20 and 43'
        else:
            print 'Test FAILURE - Simulation Script of Example 20 is invalid - Age in people is not between 20 and 43'
            BeepForError()
            OtherTestFailed = True
    
        NumOfAge20Records = len(filter(lambda Entry: Entry[3] == 20, ResultsInfo.Data))
        TheSTDForNumOfAge20Records = (25.0/1000*(1-25.0/1000)*1000)**0.5
        if (25-GlobalAllowedDeviationInSTD*TheSTDForNumOfAge20Records) <= NumOfAge20Records <= (25+GlobalAllowedDeviationInSTD*TheSTDForNumOfAge20Records):
            print 'Simulation Script of Example 20 is OK - The number of individuals of age 20 is within 3 STD of 25'
        else:
            print 'Statistical Test FAILURE - The number of individuals of age 20 is not within 3 STD of 25'
            BeepForError(1)
            OtherTestFailed = True
          
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [4,5], [719.9587 , 280.0413] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess 
        
        self.RecordSimResults('Example020', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0, IsAgeBewtween20And43)
        
        # Dump result summary in file

        return CriticalTestFailed
    

    def RunTestExample21(self):
    
        print '########################################################################'
        print '########################################################################'
        print '########              Testing Simulation Example 21               ######'
        print '########################################################################'
        print '########################################################################'

        # Modify the default teminator stable count to finish test in reasonable time    
        # DB.Params.Modify('GeneticAlgorithmMaxStableGenerationCountTerminator',DB.Param(Name = 'GeneticAlgorithmMaxStableGenerationCountTerminator', Formula = '5' , ParameterType = 'System Option' , ValidationRuleParams = '', Notes = 'Modified default to terminate test faster'), ProjectBypassID = 0)
        # DB.Params.Modify('GeneticAlgorithmMaxEvalsTerminator',DB.Param(Name = 'GeneticAlgorithmMaxEvalsTerminator', Formula = '7500' , ParameterType = 'System Option' , ValidationRuleParams = '', Notes = 'Modified default to terminate test faster'), ProjectBypassID = 0)
    
        # Prepare the project for simulation:
        ExampleNumber = 1210
        ExampleString = str(ExampleNumber-100)
        RandomStateFileName = 'SimRandStateEx' + ExampleString + 'Rep' + str(self.SimRepetition)+ '.txt'
        # SimulationOptions = [ ('RandomSeed', RandomSeedToUse), ('ValidateDataInRuntime', True), ('RepairProblems', True), ('VerboseLevel', 5) ]
        # in this example generate a population set
        DistributionPopulationSet = DB.PopulationSets[DB.Projects[ExampleNumber].PrimaryPopulationSetID]
        PopulationSizeToGenerate = DB.Projects[ExampleNumber].NumberOfRepetitions
        GeneratedPopulationSet = DistributionPopulationSet.GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = PopulationSizeToGenerate)

        SimulationScriptFullPath = DB.Projects[ExampleNumber].CompileSimulation('SimulationExample' + ExampleString, RandomStateFileNamePrefix = RandomStateFileName, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = 1, OverridePopulationSet = GeneratedPopulationSet)
        OtherTestFailed = False
        CriticalTestFailed = False
        ResultsInfo = DB.Projects[ExampleNumber].RunSimulationAndCollectResults (SimulationScriptFullPath, FullResultsOutputFileName = 'SimulationResultsExample' + ExampleString + '.csv', FinalResultsOutputFileName = 'SimulationResultsExample' + ExampleString + 'FinalData.csv')
        FinalData = ResultsInfo.ExtractFinalOutcome()
        self.GenReport(ResultsInfo.ID, DB.SessionTempDirecory + os.sep + 'SimulationReport' + ExampleString + '.txt')
    
        #IndexOfAgeIndicator = ResultsInfo.DataColumns.index('Age')
        IndexOfAgeAtStartIndicator = ResultsInfo.DataColumns.index('AgeAtStart')
        IndexOfGenderIndicator = ResultsInfo.DataColumns.index('Gender')
        IndexOfState0Indicator = ResultsInfo.DataColumns.index('State0')
        IndexOfState1TerminalIndicator = ResultsInfo.DataColumns.index('State1Terminal')

        #IndexOfState0EnteredIndicator = ResultsInfo.DataColumns.index('State0_Entered')
        #IndexOfState1TerminalEnteredIndicator = ResultsInfo.DataColumns.index('State1Terminal_Entered')
    
        AgesAtStart0To20 = [ Entry[IndexOfAgeAtStartIndicator] for Entry in FinalData if 0 < Entry[IndexOfAgeAtStartIndicator] <= 20]
        IsAverageAgeAtStart0To20Between3And7 = 3 < DB.numpy.mean(AgesAtStart0To20) < 7
        if IsAverageAgeAtStart0To20Between3And7:
            print 'Simulation Script of Example 21 is OK - Average Age At Start 0<=Age<20 is betwen 3 and 7'
        else:
            print 'Test FAILURE - Simulation Script of Example 21 is invalid - Average Age At Start 0<=Age<20 is not betwen 3 and 7'
            BeepForError()


        AgesAtStart20To40 = [ Entry[IndexOfAgeAtStartIndicator] for Entry in FinalData if 20 < Entry[IndexOfAgeAtStartIndicator] <= 40]
        IsAverageAgeAtStart20To40Between23And27 = 23 < DB.numpy.mean(AgesAtStart20To40) < 27
        if IsAverageAgeAtStart20To40Between23And27:
            print 'Simulation Script of Example 21 is OK - Average Age At Start 20<=Age<40 is betwen 23 and 27'
        else:
            print 'Test FAILURE - Simulation Script of Example 21 is invalid - Average Age At Start 20<=Age<40 is not betwen 23 and 27'
            BeepForError()


        AgesAtStart40To60 = [ Entry[IndexOfAgeAtStartIndicator] for Entry in FinalData if 40 < Entry[IndexOfAgeAtStartIndicator] <= 60]
        IsAverageAgeAtStart20To40Between43And47 = 43 < DB.numpy.mean(AgesAtStart40To60) < 47
        if IsAverageAgeAtStart20To40Between43And47:
            print 'Simulation Script of Example 21 is OK - Average Age At Start 40<=Age<60 is betwen 43 and 47'
        else:
            print 'Test FAILURE - Simulation Script of Example 21 is invalid - Average Age At Start 40<=Age<60 is not betwen 43 and 47'
            BeepForError()
            
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( FinalData, [IndexOfState0Indicator,IndexOfState1TerminalIndicator], [ 198.9000 , 401.1000] , GlobalAllowedDeviationInSTD)
        CriticalTestFailed = CriticalTestFailed or not CriticalTestSuccess
        self.RecordSimResults('Example021', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0 )
    
        GenderIs0Records = filter(lambda Entry: Entry[IndexOfGenderIndicator] == 0 , FinalData)
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( GenderIs0Records, [IndexOfState0Indicator,IndexOfState1TerminalIndicator], [158.4000 , 141.6000] , GlobalAllowedDeviationInSTD, None , False)
        self.RecordSimResults('Example021-GenderIs0', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    
        AgeGroup1Records = filter(lambda Entry: Entry[IndexOfAgeAtStartIndicator] <= 20 , FinalData)
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( AgeGroup1Records, [IndexOfState0Indicator,IndexOfState1TerminalIndicator], [94.5000 , 105.5000] , GlobalAllowedDeviationInSTD, None , False)
        # Report Age average as other statistical test in this age group
        OtherTestFailed = not IsAverageAgeAtStart0To20Between3And7
        self.RecordSimResults('Example021-AgeGroup1', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)
    
        AgeGroup2Records = filter(lambda Entry: 20< Entry[IndexOfAgeAtStartIndicator] <= 40 , FinalData)
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( AgeGroup2Records, [IndexOfState0Indicator,IndexOfState1TerminalIndicator], [63.7000 , 136.3000] , GlobalAllowedDeviationInSTD, None , False)
        # Report Age average as other statistical test in this age group
        OtherTestFailed = not IsAverageAgeAtStart20To40Between23And27
        self.RecordSimResults('Example021-AgeGroup2', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)

        AgeGroup3Records = filter(lambda Entry: 40< Entry[IndexOfAgeAtStartIndicator] <= 60 , FinalData)
        (ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, CriticalTestSuccess) = self.CheckSimulationOutcomeDistribution( AgeGroup3Records, [IndexOfState0Indicator,IndexOfState1TerminalIndicator], [40.7000 , 159.3000] , GlobalAllowedDeviationInSTD, None , False)
        # Report Age average as other statistical test in this age group
        OtherTestFailed = not IsAverageAgeAtStart20To40Between43And47
        self.RecordSimResults('Example021-AgeGroup3', ActualOutcomes, ExpectedOutcomes, STDMargins, TestSuccess, OtherTestFailed, CriticalTestFailed, 0)

        CriticalTestExpectedResults = [IsAverageAgeAtStart0To20Between3And7, IsAverageAgeAtStart20To40Between23And27, IsAverageAgeAtStart20To40Between43And47]
        AllowedMargins = [ 2, 2, 2, 0.05, 1, 1, 1, 2, 2, 6, 10, 10, 10, 10, 10, 10]

        for (ObjectiveEnum,Objective) in enumerate(GeneratedPopulationSet.Objectives):
            ActualOutcome = Objective[5]
            ExpectedOutcome = Objective[3]
            ErrorMargin = AllowedMargins[ObjectiveEnum]
            TestSuccess = abs(ActualOutcome-ExpectedOutcome)<ErrorMargin
            OtherTestFailed = False
            if ObjectiveEnum<3 and  CriticalTestExpectedResults[ObjectiveEnum] != CriticalTestExpectedResults[ObjectiveEnum]:
                ThisCriticalTestFailed = True
                BeepForError()                
            else: 
                ThisCriticalTestFailed = False
            CriticalTestFailed = CriticalTestFailed or ThisCriticalTestFailed
            self.RecordSimResults('Example021-Objective'+str(ObjectiveEnum), [ActualOutcome], [ExpectedOutcome], [ErrorMargin], [TestSuccess], OtherTestFailed, ThisCriticalTestFailed, 0)

        return CriticalTestFailed





 
  
    def test_Simulations(self):
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
        ################### ACTUAL EXECUTION OF SIMULATION ####################
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################

        print 'simulation of ' +str(len(DB.Projects)) + ' projects'
        assert len(DB.Projects)==22
  
        TestsWithCriticalErrors = 0
        for SimRepetition in range(MaxSimulationRepetitions):
            # ipdte the global parameters for recording
            self.SimRepetition = SimRepetition
            self.RandomSeedToUse = RandomSeedFunc(SimRepetition)
            
            ResultsVecPosBeforeSimulation = len (self.ResultsVec)
        
            for i in range(70,0,-10):
                print '#'*i
            print 'REPETITION ' + str(SimRepetition)
            for i in range(10,80,10):
                print '#'*i
            print
            print

            TestsWithCriticalErrors += self.RunTestExample1()
            TestsWithCriticalErrors += self.RunTestExample2()
            TestsWithCriticalErrors += self.RunTestExample3()
            TestsWithCriticalErrors += self.RunTestExample4()
            TestsWithCriticalErrors += self.RunTestExample5a()
            TestsWithCriticalErrors += self.RunTestExample5b()
            TestsWithCriticalErrors += self.RunTestExample6()
            TestsWithCriticalErrors += self.RunTestExample7()
            TestsWithCriticalErrors += self.RunTestExample8()
            TestsWithCriticalErrors += self.RunTestExample9()
            TestsWithCriticalErrors += self.RunTestExample10()
            TestsWithCriticalErrors += self.RunTestExample11()
            TestsWithCriticalErrors += self.RunTestExample12()
            TestsWithCriticalErrors += self.RunTestExample13()
            TestsWithCriticalErrors += self.RunTestExample14()
            TestsWithCriticalErrors += self.RunTestExample15()
            TestsWithCriticalErrors += self.RunTestExample16()
            TestsWithCriticalErrors += self.RunTestExample17()
            TestsWithCriticalErrors += self.RunTestExample18()
            TestsWithCriticalErrors += self.RunTestExample19()
            TestsWithCriticalErrors += self.RunTestExample20()
            TestsWithCriticalErrors += self.RunTestExample21()
           
            # Output the newer results created in this repetition
            TrackFile = open(DB.SessionTempDirecory + os.sep + 'OutcomeResults' + str(SimRepetition) + '.txt','w')
            pickle.dump(self.ResultsVec[ResultsVecPosBeforeSimulation:],TrackFile)
            TrackFile.close()

        assert TestsWithCriticalErrors == 0, 'Simulations Tests Error, there were simulations with critical tests that did not pass'

        # Now record final reults on file        
        FinalFile = open(DB.SessionTempDirecory + os.sep + 'FinalResults.txt','w')
        pickle.dump(self.ResultsVec,FinalFile)
        FinalFile.close()
        
        # Save data into CSV files
        def SaveAsCSV(ListData, FileName):
            ExportFile = open(FileName,'w')
            for Entry in ListData:
                LineToWrite = str(Entry)[1:-1].replace('[','').replace(']','').replace("'",'')+'\n'
                ExportFile.write (LineToWrite)
            ExportFile.close()
        
        Groups = set(map(lambda Entry : Entry[0] , self.ResultsVec))
        for Group in Groups:
            Res = filter (lambda Entry: Entry[0] == Group, self.ResultsVec)
            SaveAsCSV( Res , DB.SessionTempDirecory + os.sep + Group + 'Results.csv')

        self.QuickAnalyze()




class TestPopulationImportExport(GenericSetupAndTearDown):

    def setUp(self):
        " define default simulation environment"
        # use an empty DB with 2 parameters
        SetupEmptyDB(self)
        DB.Params.AddNew(DB.Param(Name = 'Gender', Formula = '' , ParameterType = 'Integer' , ValidationRuleParams = '[0,1]', Notes = 'Male = 1, Female = 0'), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'BP', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,Inf]', Notes = 'Blood Pressure'), ProjectBypassID = 0)

    def test_PopulationImportExport(self):
        # Test import an export population set
        # Make sure the directory for the file exists
        (PathOnly , FileNameOnly, FileNameFullPath) = DB.DetermineFileNameAndPath(DB.SessionTempDirecory + os.sep + 'TestPopulation.csv')
        # Create a large complex population set
        DB.PopulationSets.AddNew(DB.PopulationSet(ID = 1111111110, Name='Data Population Set Gender~FlipCoin, BP~Gaussian(120,10)', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','') , ('BP','')] , Data = [[1,138.23],[1,102.59],[0,113.64],[1,122.77],[1,121.23],[0,103.11],[1,145.25],[1,135.75],[1,127.46],[1,109.58],[1,141.23],[1,118.29],[0,113.09],[1,124.97],[0,124.1],[0,136.43],[0,110.99],[1,120.31],[0,113],[1,127.67],[1,125.92],[0,126.72],[1,130.34],[1,108.38],[0,113.25],[0,123.66],[1,111.29],[1,114.12],[1,123.11],[0,110.82],[1,140.07],[1,102.86],[1,117.64],[1,103.31],[0,120.09],[0,120.92],[0,135.82],[1,122.04],[1,142.56],[0,118.31],[1,122.37],[0,119.28],[1,121.22],[0,110.96],[0,120.13],[0,117.89],[1,103.5],[0,124.51],[0,113.69],[1,126.54],[0,114.71],[0,120.33],[1,120.37],[0,115.82],[0,130.01],[1,121.88],[1,123.04],[0,118.73],[1,126.79],[1,112.19],[1,111.18],[0,122.11],[0,116.75],[0,109.75],[1,122.5],[1,122.86],[1,125.64],[1,121.44],[1,122.18],[1,122.52],[0,113.09],[1,114.01],[1,94.9],[1,123.41],[0,112.07],[0,109.81],[0,107.42],[0,97.35],[1,122.12],[1,135.06],[1,110.71],[0,128.76],[0,115.31],[1,115.99],[1,106.24],[0,113.11],[0,115.49],[1,119.66],[0,129.51],[1,129.07],[0,110.02],[0,98.78],[1,124.46],[0,125.39],[0,119.4],[0,112.66],[1,105.76],[1,124.9],[0,141.2],[0,125.7],[1,123.87],[1,120.66],[1,103.15],[0,120.26],[1,123.33],[0,113.16],[0,110.09],[0,132.41],[0,109.77],[0,125.95],[0,112.31],[0,96.1],[0,119.74],[0,121.57],[1,120.64],[1,131.47],[1,116.97],[1,119.12],[0,121.72],[0,113.57],[0,111.08],[0,118.86],[1,121.66],[1,107.73],[0,117.67],[1,122.84],[0,114.05],[0,130.31],[0,123.46],[0,108.88],[1,117.71],[1,123.92],[0,117.51],[0,111.52],[1,131.54],[0,113.36],[0,106.67],[1,140.38],[0,128.9],[1,124.6],[1,119.53],[0,126.03],[0,117.66],[0,131.96],[1,118.15],[1,111.8],[0,127.05],[0,102.24],[0,117.39],[1,138.28]], Objectives = []), ProjectBypassID = 0)
        DB.PopulationSets[1111111110].ExportDataToCSV(FileNameFullPath)
        # Check if loading this data works
        (PopDataColumns,PopData) = DB.ImportDataFromCSV(FileNameFullPath)
        # Try to create a new population set like this
        RefPopulationSet = DB.PopulationSet(ID = 1111111120, Name='Loaded copy of Data Population Set Gender~FlipCoin, BP~Gaussian(120,10)', Source = 'Internal', Notes = 'Loaded from CSV file', DerivedFrom = 0, DataColumns = PopDataColumns, Data = PopData, Objectives = [])
        assert DB.PopulationSets[1111111110].DataColumns == RefPopulationSet.DataColumns and DB.PopulationSets[1111111110].Data == RefPopulationSet.Data, 'Population CSV export test FAILURE - Loaded and saved data is not similar'
        return



class TestLoadSave(GenericSetupAndTearDown):

    # override the default setup to use a full DB
    def setUp(self):
        " define default simulation environment"
        # use the full DB setup
        SetupFullDB()


    def test_LoadSave(self):
        if not os.path.exists('InData'):
            os.mkdir('InData')
        # Testing loading and saving options
        # Save this data to the main file
        DB.SaveAllData(FileName='InData'+os.sep+'Testing.zip',Overwrite = True)
        # Add some parameters 1 of each type
        DB.Params.AddNew(DB.Param(Name = 'TestVariable', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'TestInteger', Formula = '' , ParameterType = 'Integer' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'TestSystemOption', Formula = '1' , ParameterType = 'System Option' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'TestExpression', Formula = 'TestVariable + 1' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        # load only the parameters
        DB.Params.Load('InData'+os.sep+'Testing.zip')
        # Check if the Parameter exists - should show no
        assert not DB.Params.has_key('TestVariable'), 'LoadSave test 1 FAILURE - Parameter TestVector should not exist after loading only parameters'
        # add back the parameter
        DB.Params.AddNew(DB.Param(Name = 'TestVariable', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        # Test loading of the original data
        DB.LoadAllData('InData'+os.sep+'Testing.zip')
        # Check if the TestVector Parameter exists
        assert not DB.Params.has_key('TestVariable'), 'LoadSave test 2 FAILURE - Parameter TestVariable should not exist after loading all data'
        return





class TestLoadOlderVersion(GenericSetupAndTearDown):

    def test_LoadOlderVersion(self):
        
        
        # To reconstruct this file with a newer version use the folowing lines
        # import TestCode
        # a=TestSimulationExamples()
        # a=TestCode.TestSimulationExamples()
        # a.RunTestExample1()
        # TestCode.DB.SaveAllData('a.zip')
        # f=open('a.zip','rb')
        # b=f.read()
        # f.close()
        # import base64
        # Txt = base64.encodestring(b)
        # print Txt        
        
        # If requested Test Loading of files from a previous versions:
        FileAsStringEncodedVersion_0_87_0_0 = """UEsDBBQAAAAIADyKzUKhGgTGHQAAAB4AAAALAAAAVmVyc2lvbi50eHTT8DTg8rQw5wJRBlzB6r6e
wSHqXAUGXCUFhlx6AFBLAwQUAAAACAA8is1CDvfk/mQvAACIBAEACgAAAFBhcmFtcy50eHS9fVuT
3Day5nv/inqb8zC7QYDEbSL2QbYkh/bIlo6lcyZiN04oqrvZLa6rq2rqIlvz65fIL8kiLqwutovj
B0sCEkwkCshMJPJyd7fZfv+yqx9v2v/dbdb7w+54d9jsbrbFzb/dvV4elq/rh5uPy93yaf/jarnf
32zFzd2XL7fHZnVo1l++3Nw3d4ebrbz5t/ttefPpL8vV6i832+rmMRl/s1XhyBbXzVb3Y8zNYWtv
ft06/ylRtO00rD7Uu8/ft3ULIUTb+On7/lA/LX6t9/XuW33vm+XN/tNf3m52T8fV0v/bz8P/Wfn2
XzaHeu//pYZfXPywXK/r+8XDZrc47uvFvlnf1YvmsGj2i+Vi+/3wdbNe7BjH4vfN7v6vixZ0ubjb
PD0t1/d+0P2iWbcDPdZDs1l7HNpj/K/lqrmnpl+Pqxpr5zvNzSOm9Hn5SA325pf9bfvvN38sn7ar
+ovQX758Ot5ud5u7er+vvrxZtzMFiY4W9FHdPPoFe36ALNrVlKJdTkk/jSxb5LR8h+WhXrxbtz/b
sv2dPWg7p0dRYnKPtEyvFhHY4tXxsHlqabprf6vvi5/qdb1rAbB+BPu3BU9qIfTfFoNJeQzKf9i0
H/6/xV/Ff/sW7VvszTsnZdH+Z25oIT59Xx+Wf7zZ7TAxExAddVpPoGsJLAvae4IIfPSbIaDmUWhg
55Zu0R9Xm9ul33elDNCc2ssWQ1l5DIow6IkY+l/Jffny87Ld8h+xJP7bJv97ZiA9naWnsyI6K6bz
6r+a+9vCo16cUFeSyRr8WqX/tcqbIX1CtL82jxKDLViVORpHoauWzkp5OjXRaWahM0Dv0dqYRiEK
4YkMaPyibr+EP81w6vnDeW6I8sdT+eOp6Hiqcp5fVd0ukp9VVTHJis5gRzIdL6UCmtCm/aSNn7Sl
SbuJB+Ld/vPu6Bm5LoKvn9pFi0HLFoMuPQZdhRiGoKpboI+rZcu6v25W9y1bP2xarr31jHt9WBy+
tstGAxYPx/UdM2mdn5wXhLvm8evBg4THM+jy51H782joPJqpfKfbHvZLctaNzG6kHKTnTcbzJkO8
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
bera9i3V++0v3Svtg1Pfrr1Pf/P0qP1m948HL3zb/hB/1P7QVsDR/alte/3Ln7c/Dp//5M9NvpsX
QT3Oxnbhd+3jw4vd9XX/wI/apu1jrtseuePf5j0+Du+9+ert+/39mvXQ19P8q9s+hX54vmvv0v5i
197elfk41DD77senr7/j8fFb3URfj+0QlGM7vq5t48ZftHdIn/fFet3/7PtuPfWzd9pblMVh07ja
57Dr+9YPYNuw7P7yt3kMx7bdYVjGkPrhbZu2j6yn+Vcfza5bHH7o79GktU/79Jdlb8sygsM86bqf
J9wd7Y/9A//16fQmzz7s7/vT9oG7h/NSuY596m4+YMP1F32g+zbb4ufXd/HjtvWhzbLE+Y37jPvZ
WXbtfQ7HX/2qafvam45Es1jaB1d3/cv2u+ZoGF75W9+xdqyGvv4GHds/zfOrywT6Z/XlUfp49vXO
e/NxPO769P47v94XZl/A/egf2gunrt8//1FbSq4fz/00lf6e8bl5Pw65z3R4++nu4fP+xvOSb0v4
9vvzkTzVj+ZToo59b+cD11dmm9T9X/SdfP/27bbZ2I9PH+dpPhSu9refNx9iOwEHN2nakXvc3qy/
4XD3+XkbFz/r9kv7yHL9+nwmnvqZOKbP27lS6z92+1t9s/ZrP79LXwXl9Nsv37j9aN7PIbl55fQP
3u/b5Pen9+axT6sjz6PeHX8/j2k6s90b/Yh8/MNP/jkdrWf7YeiXh75bbW678fRUP0P6wb7+el7a
fS3s03I9ObzV/rKPrR/LsX/KH/tZmtvwanyhvVufVh+zG+fdKKe780kxXShiOzeH/bycD/2wHl9c
/jD0M/mLvha+7e/al00b8H6Y1+917heB8tp8uu/6kTp98dK889OnHN/xS0z0JRH/2if41Hx61/GP
v7/zQ3y1r815zX/+/jzcfjG69n+fV8a0il2fbI2PZ3MlvjWP9vq6L+ff90tbmAfVP+YQwnzoduXu
cniuZ/O7fgb339d//uepx/10/PdP+iuP+jro6vLdfBj7KXzKX957qRu/fqG//PG9frj/d97bPt7r
vibjJ8tZUX82L4s+2n3qB2z8+Z325nv/k3r7djtAJc8Jedz9bN7xfsV3p7fvd+9//2m/UP6xX1d+
Px/Hfg72C3VfgbuxXw10NVsuXH15D9fLoU4//aQvihfmzz/t54NRxv/tnp65/fBP83j7OdxX5W5y
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
enaJ916dD/dp/+uZ/09XkF2/m7vu3K5+PYfW0b/k5mfVk/s8LFfluj0hzhm2LOXjG8szwsTBpwR4
owfG7l9v/XhBe4flqaf8d35APeafftSXSLj98LevPT1/5v7w6nx8p+dAt2THfh5uP+Zl/75Onk6o
pse1Pu1+UkzJH19/2c8fOOx/Pi+Y4/BwueOfrj2x8yp/b6FBHX/uH3//y/luc7fcoNT+yNgvB/2y
u+s0u4b//vPRJwtOyzPymQhxXM7G69/NNwnH64/vzxfOKQT28+1eH95EWK6fXiL7+tfTQr3f/6Uh
PVPenaIwfTTbd+O995dHv85lj7sF5ec7/QDWW0/1dfmX+ZZvui0IE7Z7qz8PHj7oF4sJT47zuqj+
5V/MD7TTDdjhu+fnC/m06p17/sdzChynf5Fx81HoHof87vTYWB7NV9Tp2t1f66DmOj81W2rPff32
6/i3njHx++UoTIv8MN9Muf4G/TpZ63fzIT+OL88hPixErF9k9p1K7uvHy6Ph4f4f+r3n6/MQSvzx
jxZeNM63TdMe9X/JHPu/Pfrhaj/9k+M7w9Vbw0v9nwu9u/rw2e2fbd98vPvqwb1TdcOd979++3T/
zpdfhn/EeKdt8cHu/vHDR7tHpzebt+GD04MX3UuPHj+6883nu2/qD/237WP8SN7upQff922nf+R8
0sb9xTC/0R++nd42zn/6P/ahb5Gubt174Ps/67qr95uvcnXrUftf7f8Q3P95+vWv73371f1v2qZh
6JuGbvyd+8e73909fru7N/27dBivdh8+29729Ohu36P+V77/1Ud3vzr1P4T+h1c/n34fp9/fu/vd
9KfU//TGaXfsf8j9D4udO+7OnTvv7e7ev/PHh18fTt9Me1AubXDnzfuPTg9P0zvV9UPM38ZBH2b/
0l3tFqv9T2P3GP3039D/+XjXZj7/8v0/+gv7Qvu169vHq7OXvbth+7RtP/btxxu2z9v2vv/yN2xf
5u1XzU37X7ftyf6nYdue7H9y2/Zk/9N4tb432f/kt+3R/odte7T/cdse7f8yX0/3P2/bo/0v2/Zo
/+u2Pdn/vMw3wP3Pbtue7H8et+3J/me/bY/2f5lvpPsft+3R/qdte7T/edse7f8y30T3v27bk/0v
w7Y92f/itu3J/pdlvhnuf/Hb9mj/w7Y92v+4bY/2f5lvofuft+3R/pdte7T/ddue7H9d5lvh/le3
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
MC/FGQn6YlQumj5P8OKNBO5YMBJ2kEs0EnaQix7p9Arwko0EeilGAg/yMn1eRZbrYCRsx6ozEnaQ
62gk7CDXZfq8iizXYCTQSzQS6CUZCfSi6fNErsVIoJdqJMhLGQYjQV7KoOnjRC7DaCSrl0sruQya
Ps7KMgQjgZ+i6eMUK0MyEvgpmj7OlyKIxxu/iigeb/wqwni88auI4/HGryKQd974dfGIieTxLq4i
lHfexXX5U5bp85asIpjHW7KKaB5vySrCebwlq6w8D1/5ywr08JW/rEQPX/nLivTwlb+I6fGWrCKo
x1uyiqgeb8kqwnq8JauI6/GWrCKwd96SdXEli+zx/qoitMf7q4rYHu+vKoJ75/1VF72I7vH+qiK8
5/mVX3yPN0sVAT7eLFVE+HizVBHi481SRYyPN0sVQT7eLFVE+XizVBHm481SRZyPN0sVgT7eLFVE
+s6bpS5LkpFAL5o+TzGxPo8feYpYn8ePPEWsz+NHniLWxyuvilgfr7wqYn288qqI9Z1XXl0898X6
eOVVEevjlVdFrI9XXhWxPl55VcT6eOVVEevjlVdFrI9XXhWxPl55VcT6eOVVEevjlVdFrI9XXhWx
Pl55VcT6eOVVEevjlVdFrC9gCFnE+njlVRHr45VXRayPV14VsT5eeVXE+njlVRHr45VXRayPV14V
sT5eeVXE+njlVRHr45VXRayPV14VsT5eeVXE+njlVRHr45VXRayPV14VsT5eeVXE+njlVRHr45VX
RayPV14VsT5eeVXE+njlVRHr45VXRayPV14VsT5eeVXE+njlVRHr45VXRayPV14VsT5eeVXE+njl
VRHr45VXVayPV15VsT5eeVXF+njlVRXrizj3q1hfxLlfxfriWe5r8yfdj1WxPl6sVcX6eLFWFevj
xVpVrI8Xa1WxPl6sVcX6In6srmJ9vPKqivXxyqsq1scrr6pYH6+8qmJ9vPKqivXxyqsq1scrr6pY
H6+8qmJ9vPKqivXxyqsq1scrr6pYH6+8qmJ9vPKqivXxyqsq1scrr+r6HT6cyFWsj1deVbE+XnlV
xfp45VVdv8c3YC/rF/lwItf1m3w4kev6VT6cyFWsL+FErmJ9vCWrivXxlqwq1sdbsqpYH2/JqmJ9
vCWrivXxlqwq1sdbsqpYH2/JqmJ9vCWrivXxlqwq1sdbsqpYX8Kgu4r18ZasKtbHW7KqWB9vyapi
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
AAAAAA=="""
        
        # Create a file using the previous version text
        PrevVersionFile = open( DB.SessionTempDirecory + os.sep + 'Testing_Ver_0_87_0_0.zip', 'wb')
        FileAsStringDecodedVersion_0_87_0_0 = base64.decodestring(FileAsStringEncodedVersion_0_87_0_0)
        PrevVersionFile.write(FileAsStringDecodedVersion_0_87_0_0)
        PrevVersionFile.close()
        # Create a blank database
        DB.CreateBlankDataDefinitions()
        # first test the version
        (FileVersion, IsCompatible, IsUpgradable, DidLoad, HasResults) = DB.ReconstructDataFileAndCheckCompatibility(InputFileName = DB.SessionTempDirecory + os.sep + 'Testing_Ver_0_87_0_0.zip', JustCheckCompatibility = True, RegenerationScriptName = None, ConvertResults = False, KnownNumberOfErrors = 0, CatchError = True)
        assert FileVersion == (0,87,0,0,'MIST') and (IsCompatible == (FileVersion == DB.Version)) and IsUpgradable and not DidLoad, 'Load previous File Version test 1 FAILURE - did not understand file version 0.87.0.0. Make sure the file exists.'
        # now actually load the file and make sure that data was loaded
        (FileVersion, IsCompatible, IsUpgradable, DidLoad, HasResults) = DB.ReconstructDataFileAndCheckCompatibility(InputFileName = DB.SessionTempDirecory + os.sep + 'Testing_Ver_0_87_0_0.zip', JustCheckCompatibility = False, RegenerationScriptName = None, ConvertResults = False, KnownNumberOfErrors = 0, CatchError = True)
        assert len(DB.Projects)==21 and DidLoad == True, 'Load previous File Version test 2 FAILURE - did not properly load file version 0.87.0.0. Make sure the file exists ad contains 21 projects.'
        # now try doing the same and creating an output script 
        DB.CreateBlankDataDefinitions()
        ScriptName = DB.SessionTempDirecory + os.sep + 'ReconstructingTesting_Ver0_87_0_0.py'
        (FileVersion, IsCompatible, IsUpgradable, DidLoad, HasResults) = DB.ReconstructDataFileAndCheckCompatibility(InputFileName = DB.SessionTempDirecory + os.sep + 'Testing_Ver_0_87_0_0.zip', JustCheckCompatibility = False, RegenerationScriptName = ScriptName, ConvertResults = False, KnownNumberOfErrors = 0, CatchError = True)
        # now run the script
        ScriptFile = open(ScriptName,'r')
        NameSpaceToRunIn = {}
        try:
            exec ScriptFile in NameSpaceToRunIn
        except:
            assert False, 'Load previous File Version test 3 FAILURE - did not properly run file conversion from file version 0.87.0.0. Make sure the file exists.'
        return




class TestInvalidExpressions(GenericSetupAndTearDown):

    def test_InvalidExpressions(self):

        # test all sorts of invalid expressions
        try:
            DB.Params.AddNew(DB.Param(Name = 'TestParam1', Formula = ' TestParam2  ' , ParameterType = 'Expression' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)
        except:
            CheckException('"TestParam2" used in the expression is not a valid name of a parameter', 'Invalid Expression Test a is OK - Parameter not created since the expression is invalid')
        else:
            assert False, 'Invalid Expression Test a FAILURE - the expression should raise an error'
         
        try:
            DB.Params.AddNew(DB.Param(Name = 'TestParam2', Formula = ' 0.7' , ParameterType = 'Expression' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestParam3', Formula = ' 1-TestParam2  ' , ParameterType = 'Expression' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)    
            # hardcode a cyclic reference 
            DB.Params['TestParam2'].Formula = '1-TestParam3'
            DB.Params['TestParam2'].VerifyValidity()
        except:
            CheckException('meaning a cyclic (recursive) assignment','Invalid Expression Test b is OK - Parameter not created since the expression is invalid')
        else:
            assert False, 'Invalid Expression Test b FAILURE - the expression should raise an error'
        
        try:
            DB.Params.AddNew(DB.Param(Name = 'TestParam4', Formula = ' (TestParam1,2)  ' , ParameterType = 'Expression' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)    
        except:
            CheckException('"TestParam1" used in the expression is not a valid name of a parameter','Invalid Expression Test c is OK - Parameter not created since the expression is invalid')
        else:
            assert False, 'Invalid Expression Test c FAILURE - the expression should raise an error'
        
        try:
            DB.Params.AddNew(DB.Param(Name = 'TestParam5', Formula = ' [0.7]' , ParameterType = 'Expression' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)    
        except:
            CheckException('will result in a vector or a matrix. This is not allowed','Invalid Expression Test d is OK - Parameter not created since the expression is invalid')
        else:
            assert False, 'Invalid Expression Test d FAILURE - the expression should raise an error'
        
        try:
            DB.Params.AddNew(DB.Param(Name = 'TestParam6', Formula = ' 0  ' , ParameterType = 'Expression' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)    
            DB.Params.AddNew(DB.Param(Name = 'TestParam7', Formula = 'Table([[TestParam6,[NaN,2]]],[1])' , ParameterType = 'Expression' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)
        except:
            CheckException(None,'Invalid Expression Test e FAILURE - Parameter not created since the expression should not raise an error')
        else:
            print 'Invalid Expression Test e is OK - the expression is valid'
        
        try:
            DB.Params.AddNew(DB.Param(Name = 'TestParam8', Formula = 'Inf  + NaN ' , ParameterType = 'Expression' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)    
        except:
            CheckException(None,'Invalid Expression Test f FAILURE - the expression should not raise an error')
        else:
            print 'Invalid Expression Test f is OK - the expression is valid'
        
        try:
            DB.Params.AddNew(DB.Param(Name = 'TestParam9', Formula = '[ [1, 2] , [ 1,2 ]]' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)    
        except:
            CheckException('evaluation will result in a vector or a matrix. This is not allowed','Invalid Expression Test g is OK - Parameter not created since the expression is invalid')
        else:
            assert False, 'Invalid Expression Test g FAILURE - the expression should raise an error'


        # Now test a system option 
        try:
            DB.Params.Modify('ValidateDataInRuntime',DB.Param(Name = 'ValidateDataInRuntime', Formula = '10000' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        except:
            CheckException('is a name corresponding to a System Option, while the parameter type is not defined as a system option','Invalid Expression Test h is OK - An error should be generated since the System Option name is restricted to system options')
        else:
            assert False, 'Invalid Expression Test h FAILURE - the parameter modification should raise an error since the System Option name is restricted to system options. No such error Generated and therefore the test error.' 
        
        
        # Test Cyclic reference 1
        try:
            DB.Params.AddNew(DB.Param(Name = 'TestParam10', Formula = 'TestParam10' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)    
        except:
            CheckException('used in the expression is not a valid name of a parameter','Invalid Expression Test i is OK - a Parameter should not be defined due to a circular reference')
        else:
            assert False, 'Invalid Expression Test i FAILURE - the expression should raise an error'
        
        # Test Cyclic reference 2
        try:
            DB.Params.AddNew(DB.Param(Name = 'TestParam10', Formula = '1' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestParam11', Formula = 'TestParam10+1' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
            DB.Params.Modify('TestParam10',DB.Param(Name = 'TestParam10', Formula = 'TestParam11+1' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        except:
            CheckException('Cyclic definition of a parameter was detected','Invalid Expression Test j is OK - a Parameter should not be modified due to a circular reference')
        else:
            assert False, 'Invalid Expression Test j FAILURE - the expression should raise an error'

        
        # Test Cyclic reference 3 + Matrix
        try:
            DB.Params.AddNew(DB.Param(Name = 'TestParam12', Formula = '1' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
            DB.Params.Modify('TestParam12',DB.Param(Name = 'TestParam12', Formula = 'CostWizard(0,0,[1,1],[TestParam12,1])' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        except:
            CheckException('Cyclic definition of a parameter was detected','Invalid Expression Test k is OK - a Parameter should not be modified due to a circular reference')
        else:
            assert False, 'Invalid Expression Test k FAILURE - the expression should raise an error'


        
        # Test Expression syntax validness for supported functions
        FuncExprToTest = [  'Eq(0,TestConstant)',
                            'Ne(0,TestConstant)',
                            'Gr(0,TestConstant)',
                            'Ge(0,TestConstant)',
                            'Ls(0,TestConstant)',
                            'Le(0,TestConstant)',
                            'Or(0,TestConstant)',
                            'And(0,TestConstant)',
                            'Not(0)',
                            'IsTrue(0)',
                            'IsInvalidNumber(0)',
                            'IsInfiniteNumber(0)',
                            'IsFiniteNumber(0)',
                            'Iif (0, 0, TestConstant)',
                            'Table([[TestConstant,[NaN,0,1]]],[0,1])',
                            'CostWizard (0, 0, [TestConstant], [1])',
                            'Exp(0)',
                            'Log(1,1)',
                            'Ln(1)',
                            'Log10(1)',
                            'Pow(1,1)',
                            'Sqrt(0)',
                            'Pi()',
                            'Mod(0,1)',
                            'Abs(0)',
                            'Floor(0)',
                            'Ceil(0)',
                            'Max(0,1,TestConstant)',
                            'Min(0,1,TestConstant)', 
                            'Bernoulli(0.5)', 
                            'Binomial(3,0.5)', 
                            'Geometric(0.5)', 
                            'Uniform(0,2)', 
                            'Gaussian(3,1)']
        
        #Define a parameter to use in some expressions for varaiety of testing
        DB.Params.AddNew(DB.Param(Name = 'TestConstant', Formula = '0' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        # Loop through all tests
        for (Num,CurrentTestFunc) in enumerate(FuncExprToTest):
            try:
                DB.Expr(CurrentTestFunc)
            except:
                CheckException(None,'Expression test A-#' + str(Num) + ' FAILURE - the expression "' + CurrentTestFunc + '" should not raise an error :')
            else:
                print 'Expression test A-#' + str(Num) + ' is OK - the expression "' + CurrentTestFunc + '" is valid'

        
        # Test wrong number of parameters in functions - these tests should all fail
        FuncExprToTest = [  ('[1,]',  'the expression evaluation will result in a vector or a matrix'),
                            ('(1,)',  'a comma is not allowed between parenthesis, except as part of a parameter list for a function.'),
                            ('Max(1,)',  'This may happen if the wrong number of parameters was specified'),
                            ('Max(3-1,3),',  'a comma is not allowed at the end of an expression'),
                            ('Eq(0)', 'This may happen if the wrong number of parameters was specified'),
                            ('Ne(TestConstant)', 'This may happen if the wrong number of parameters was specified'),
                            ('Gr(TestConstant)', 'This may happen if the wrong number of parameters was specified'),
                            ('Ge(0)', 'This may happen if the wrong number of parameters was specified'),
                            ('Ls(0)', 'This may happen if the wrong number of parameters was specified'),
                            ('Le(TestConstant)', 'This may happen if the wrong number of parameters was specified'),
                            ('Or(0)', 'This may happen if the wrong number of parameters was specified'),
                            ('And(TestConstant)', 'This may happen if the wrong number of parameters was specified'),
                            ('Not(0,2)', 'This may happen if the wrong number of parameters was specified'),
                            ('IsTrue(0,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('IsInvalidNumber(0,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('IsInfiniteNumber(0,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('IsFiniteNumber(0,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Iif (0,TestConstant)', 'This may happen if the wrong number of parameters was specified'),
                            ('Table()', 'This may happen if the wrong number of parameters was specified'),
                            ('CostWizard()', 'This may happen if the wrong number of parameters was specified'),
                            ('Exp(1,0)', 'This may happen if the wrong number of parameters was specified'),
                            ('Log(1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Ln(1,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Log10(1,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Pow(1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Sqrt(0,2)', 'This may happen if the wrong number of parameters was specified'),
                            ('Pi(1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Mod(0)', 'This may happen if the wrong number of parameters was specified'),
                            ('Abs(0,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Floor(0,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Ceil(0,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Max()', 'This may happen if the wrong number of parameters was specified'),
                            ('Min()', 'This may happen if the wrong number of parameters was specified'),
                            ('Bernoulli(0.5,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Binomial(3,0.5,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Geometric(0.5,1,2)', 'This may happen if the wrong number of parameters was specified'),
                            ('Uniform(0,2,1)', 'This may happen if the wrong number of parameters was specified'),
                            ('Gaussian(3,1,1)', 'This may happen if the wrong number of parameters was specified')]
        # Loop through all tests
        for (Num,(CurrentTestFunc,ExpectedError)) in enumerate(FuncExprToTest):
            try:
                DB.Expr(CurrentTestFunc)
            except:
                CheckException(ExpectedError,'Expression test B-#' + str(Num) + ' OK - the expression "' + CurrentTestFunc + '" should have raise an error.')
            else:
                assert False, 'Expression test B-#' + str(Num) + ' FAILURE - the expression "' + CurrentTestFunc + '" is invalid and should have raised an error of an invalid number of parameters'


    
        # Expression Evaluation tests
        # Batch A - Bad Evaluation examples
        
        
        DummyExpr=DB.Expr()
        
        assert DummyExpr != None, "Expression Evaluation Test Preparation: Make Sure Expression was created"
        
        Tests = []
        Tests.append(("""DummyExpr.Evaluate('0.1+Age')""",'The value does not immediately evaluate to a number'))
        Tests.append(("""DummyExpr.Evaluate('[0.1+1]')""",' The value does not evaluate to a numeric type'))
        Tests.append(("""DummyExpr.Evaluate('0.1+Expression Evaluation Test A-1')""",'The value does not immediately evaluate to a number'))
        Tests.append(("""DummyExpr.Evaluate('',2)""",'Evaluate() takes at most 2 arguments (3 given)'))
        Tests.append(("""DummyExpr.Evaluate('2/0','Number')""",'Evaluate() takes at most 2 arguments (3 given)'))
        Tests.append(("""DummyExpr.Evaluate('2/0')""",'The value does not immediately evaluate to a number'))
        Tests.append(("""DummyExpr.Evaluate('(-2)**-0.3')""",'The value does not immediately evaluate to a number'))
        Tests.append(("""DummyExpr.Evaluate('Bernoulli(0.5)')""",'The value does not immediately evaluate to a number'))
        
        # Run the tests
        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Expression Evaluation Test A-#' + str(Num) + ' OK - an invalid test was detected')
            else:
                assert False, 'Expression Evaluation Test A-#' + str(Num) + ' FAILURE -  an invalid test was not detected'
        
        
        # Batch B - Good Evaluation examples
        
        Tests = []
        Tests.append(("""DummyExpr.Evaluate('(0.1 + 0.2) * 0.3')""", (0.1 + 0.2) * 0.3 ))
        Tests.append(("""DummyExpr.Evaluate('1 + 2')""",  (1 + 2)))
        Tests.append(("""DummyExpr.Evaluate('((2+6)/4) ** 3')""",  (((2+6)/4) ** 3)))
        Tests.append(("""DummyExpr.Evaluate('Inf')""", DB.Inf))
        Tests.append(("""DummyExpr.Evaluate('3+inf')""", 3+DB.Inf))
        Tests.append(("""DB.IsInvalidNumber(DummyExpr.Evaluate('NaN'))""", 1))
        Tests.append(("""DB.IsInvalidNumber(DummyExpr.Evaluate('0'))""", 0))
        Tests.append(("""DB.IsInfiniteNumber(DummyExpr.Evaluate('0'))""", 0))
        Tests.append(("""DB.IsInfiniteNumber(DummyExpr.Evaluate('-Inf'))""", 1))
        Tests.append(("""DB.IsFiniteNumber(DummyExpr.Evaluate('NaN'))""", 0))
        Tests.append(("""DB.IsFiniteNumber(DummyExpr.Evaluate('0'))""", 1))
        Tests.append(("""DB.Iif (0, 0,2)""", 2))
        Tests.append(("""DB.Iif (5, 0, 2)""", 0))
        Tests.append(("""DB.TableRunTime([[1,[DB.NaN,0,1]]],[4,9])""", 9))
        Tests.append(("""DB.Exp(0.1)""", math.exp(0.1)))
        Tests.append(("""DB.Log(5,2)""", math.log(5,2)))
        Tests.append(("""DB.Ln(5)""", math.log(5)))
        Tests.append(("""DB.Log10(7)""", math.log10(7)))
        Tests.append(("""DB.Pow(2,3)""", 2**3))
        Tests.append(("""DB.Sqrt(3)""", 3**0.5))
        Tests.append(("""DB.Pi()""", math.pi))
        Tests.append(("""DB.Mod(5.1,2)""", 5.1%2))
        Tests.append(("""DB.Abs(-7.1)""", 7.1))
        Tests.append(("""DB.Floor(3.42)""", 3))
        Tests.append(("""DB.Ceil(3.42)""", 4))
        Tests.append(("""DB.Max(1,4,2)""", 4))
        Tests.append(("""DB.Min(1,4,2)""", 1))
        Tests.append(("""0 <= DB.Bernoulli(0.5) <= 1""",1))
        Tests.append(("""0 <= DB.Binomial(3,0.5) <= 3""",1))
        Tests.append(("""0 <= DB.Geometric(0.5)""",1))
        Tests.append(("""0 <= DB.Uniform(0,2) <= 2""",1))
        Tests.append(("""-DB.Inf <= DB.Gaussian(3,1) <= DB.Inf""",1))
        
        # Run the tests
        for (Num,(Test,TestResult)) in enumerate(Tests):
            try:
                Value = eval(Test)
            except:
                CheckException(None, 'Expression Evaluation Test B-#' + str(Num) + ' FAILURE - a valid test did not pass')
            else:
                if Value != TestResult:
                    assert False, 'Expression Evaluation Test B-#' + str(Num) + ' FAILURE - Calculated value does not correspond to the expected value. Calculated value was ' + str(Value) + ' instead of the expected result of ' + str(TestResult)
                else:
                    print 'Expression Evaluation Test B-#' + str(Num) + ' OK - a valid test passed'
              
        
class TestInvalidStateDefinitions(GenericSetupAndTearDown):

    def test_InvalidStateDefinitions(self):
    
        # Test State problems - especially processes and split/joiner states
        # First prepare some states to test
        DB.States.AddNew(DB.State(ID = 92200001 , Name = 'TestingState0' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
        DB.States.AddNew(DB.State(ID = 92200002 , Name = 'TestingState1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
        DB.States.AddNew(DB.State(ID = 92200100 , Name = 'TestingSubProcess1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [92200001,92200002] ), ProjectBypassID = 0)
        DB.States.AddNew(DB.State(ID = 92200073 , Name = 'TestingSplitState1' , Notes = '' , IsSplit = True , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
        DB.States.AddNew(DB.State(ID = 92200084 , Name = 'TestingJoinerState1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 92200073 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
        
        # Now build the tests
        Tests = []
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingSubProcess2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [92200001, 92200002, 9220003] ), ProjectBypassID = 0)""",'does not exist in the states table'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingSubProcess2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = True , IsTerminal = False , ChildStates = [92200001, 92200002] ), ProjectBypassID = 0)""",'A sub-process cannot be an event state / terminal state / splitter state / joiner state'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingSubProcess2' , Notes = '' , IsSplit = True , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [92200001, 92200002] ), ProjectBypassID = 0)""",'A sub-process cannot be an event state / terminal state / splitter state / joiner state'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingSubProcess2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [92200001, 92200002] ), ProjectBypassID = 0)""",'A sub-process cannot be an event state / terminal state / splitter state / joiner state'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingSubProcess2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 92200073 , IsEvent = False , IsTerminal = False , ChildStates = [92200001, 92200002] ), ProjectBypassID = 0)""",'A sub-process cannot be an event state / terminal state / splitter state / joiner state'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 92200200 , Name = 'TestingSubProcess2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [92200100,92200001,92200002] ), ProjectBypassID = 0)""",'Duplicate nested states were detected'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingJoinerState2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 92200001 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)""",'is joining a state that is not a splitter state'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingJoinerState2' , Notes = '' , IsSplit = True , JoinerOfSplitter = 92200073 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)""",'A state cannot be both a splitter and a joiner state'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingJoinerState2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 92200073 , IsEvent = True , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)""",'A state cannot be both an Event state and a joiner state'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingJoinerState2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 92200073 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)""",'A State cannot be both a terminal state and a joiner state'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingEvent' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = True , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)""",'A state cannot be both a Terminal State and an event state'))
        Tests.append(("""DB.States.AddNew(DB.State(ID = 0 , Name = 'TestingEvent' , Notes = '' , IsSplit = True , JoinerOfSplitter = 0 , IsEvent = True , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)""",'A state cannot be both a splitter and an event state'))
        
        # Run the tests

        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'State Test #' + str(Num) + ' OK - an invalid test was detected')
            else:
                assert False, 'State Test #' + str(Num) + ' FAILURE -  an invalid test was not detected'




class TestDistributionPopulations(GenericSetupAndTearDown):

    def test_DistributionPopulations(self):

        try:

            DB.Params.AddNew(DB.Param(Name = 'Age', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Official oldest person was 122 at death by Wikipedia'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'Gender', Formula = '' , ParameterType = 'Integer' , ValidationRuleParams = '[0,1]', Notes = 'Male = 1, Female = 0'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'BP', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,Inf]', Notes = 'Blood Pressure'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'Smoke', Formula = '' , ParameterType = 'Integer' , ValidationRuleParams = '[0,1]', Notes = 'Smoking Status'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'AF', Formula = '' , ParameterType = 'Integer' , ValidationRuleParams = '[0,1]', Notes = 'Atrial fibrillation'), ProjectBypassID = 0)

            DB.Params.AddNew(DB.Param(Name = 'TestCov1', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Test Covariate'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestCov2', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Test Covariate'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestCov3', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Test Covariate'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestCov4', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Test Covariate'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestCov5', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Test Covariate'), ProjectBypassID = 0)

            # Test population sets and parameters based on distributions
            DB.Params.AddNew(DB.Param(Name = 'TestDistributionBernoulli', Formula = 'Bernoulli(0.2)' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestDistributionBinomial', Formula = 'Binomial(90,0.5)' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestDistributionGeometric', Formula = 'Geometric(0.5)' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestDistributionUniform', Formula = 'Uniform(1,2)' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestDistributionGaussian', Formula = 'Gaussian(100,10)' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'TestDistributionExpression', Formula = 'TestCov2 + TestCov3' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        
            DB.Params.AddNew(DB.Param(Name = 'BadTestDistributionBernoulli', Formula = 'Bernoulli(0.2)' , ParameterType = 'Expression' , ValidationRuleParams = '[2,3]', Notes = 'Testing'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'BadTestDistributionBinomial', Formula = 'Binomial(90,0.5)' , ParameterType = 'Expression' , ValidationRuleParams = '[-2,-1]', Notes = 'Testing'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'BadTestDistributionGeometric', Formula = 'Geometric(0.5)' , ParameterType = 'Expression' , ValidationRuleParams = '[-2,-1]', Notes = 'Testing'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'BadTestDistributionUniform', Formula = 'Uniform(1,2)' , ParameterType = 'Expression' , ValidationRuleParams = '[0,0.5]', Notes = 'Testing'), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = 'BadTestDistributionGaussian', Formula = 'Gaussian(100,10)' , ParameterType = 'Expression' , ValidationRuleParams = '[-Inf,-Inf]', Notes = 'Testing'), ProjectBypassID = 0)
        
            # Test a population set based on a distribution
            DistributionPopulationSet = DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','TestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []), ProjectBypassID = 0)
            # Create a new parameter
            DistributionPopulationSet2 = DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','Bernoulli(0.25)') , ('TestCov2','Binomial(90,0.5)') ,  ('TestCov3','Geometric(0.5)'),  ('TestCov4','Uniform(1,2)') , ('TestCov5','Gaussian(100,10)')] , Data = [], Objectives = []), ProjectBypassID = 0)
            # Create a population with dependencies (use expressions)
            DistributionPopulationSet3 = DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','Bernoulli(0.25)') , ('TestCov2','1-TestCov1') ,  ('TestCov3','1-TestCov4'),  ('TestCov4','Uniform(1,2)') , ('TestCov5','100+10*Gaussian(0,1)')] , Data = [], Objectives = []), ProjectBypassID = 0)
            # Create a population with more complicated dependencies (use expressions)
            DistributionPopulationSet4 = DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionExpression') , ('TestCov2','-TestCov3') ,  ('TestCov3','1-TestCov4'),  ('TestCov4','TestCov5/2') , ('TestCov5','Uniform(1,2)')] , Data = [], Objectives = []), ProjectBypassID = 0)
        
            # Test Generation of a data population set based on distributions
            OriginalNumberOfErrorsConsideredAsWarningsForPopulationGeneration = DB.Params['NumberOfErrorsConsideredAsWarningsForPopulationGeneration'].Formula
            DB.Params.Modify( 'NumberOfErrorsConsideredAsWarningsForPopulationGeneration', DB.Param(Name = 'NumberOfErrorsConsideredAsWarningsForPopulationGeneration', Formula = '0' , ParameterType = 'System Option' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
            DistributionPopulationSet.GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)
            DistributionPopulationSet2.GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)
            DistributionPopulationSet3.GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)
            ResultingTestSet = DistributionPopulationSet4.GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)
            DB.Params.Modify( 'NumberOfErrorsConsideredAsWarningsForPopulationGeneration', DB.Param(Name = 'NumberOfErrorsConsideredAsWarningsForPopulationGeneration', Formula = str(OriginalNumberOfErrorsConsideredAsWarningsForPopulationGeneration) , ParameterType = 'System Option' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        
            # test the data generated during the last test
            TestSetData = ResultingTestSet.Data
            FirstColumnIsZero = all(map (lambda Entry: Entry[0] == 0.0 , TestSetData))
            OtherColumnsAreNonZero= all(map (lambda Entry: Entry[2] != 0 and Entry[3] != 0 and Entry[4] != 0  , TestSetData))

            assert (FirstColumnIsZero and OtherColumnsAreNonZero), 'Distribution based test A-DATA FAILURE - Data population created using generation is not correct - data in first column should be zero and other columns should be none zero.'
            print 'Distribution based test A-DATA OK - Data population created using generation was correct - data in the first column was zero and other columns should be none zero.  '
      
        except:
             CheckException(None,'Distribution based test A FAILURE - A data population based on distribution was not successfully created or one of the operations leading to its creation failed.')
        else:
            print 'Distribution based test A OK - A data population based on distribution was successfully created'
        
            
        # Perform additional tests on distributions - these tests should fail
        
        OriginalNumberOfErrorsConsideredAsWarningsForPopulationGeneration = DB.Params['NumberOfErrorsConsideredAsWarningsForPopulationGeneration'].Formula
        # Reduce the number of warnings on screen to 10. Since the tests are set to 
        # fail, this does not diminish the level of testing of random numbers
        DB.Params.Modify( 'NumberOfErrorsConsideredAsWarningsForPopulationGeneration', DB.Param(Name = 'NumberOfErrorsConsideredAsWarningsForPopulationGeneration', Formula = '10' , ParameterType = 'System Option' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        
        DB.Params.AddNew(DB.Param(Name = 'IntegerParamForTestDistribution', Formula = '' , ParameterType = 'Integer' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'BoundedParamForTestDistribution', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[-Inf,-Inf]', Notes = 'Testing'), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'BlankParamForTestDistribution', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'ReferencingBlankParamForTestDistribution', Formula = 'BlankParamForTestDistribution' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'TestFormulaToCreateCyclicReferenceForTestDistribution', Formula = 'TestCov1 + TestCov2' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'TestCovariateFuncToBeUsedLaterToTestFailure', Formula = '2*IntegerParamForTestDistribution' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        
        Tests = []
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','BlankParamForTestDistribution') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = [])""",'Population Dependency on an empty parameter'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','ReferencingBlankParamForTestDistribution') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = [])""",'Population Dependency on an empty parameter'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('IntegerParamForTestDistribution','TestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'Run time integer check error'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('BoundedParamForTestDistribution','TestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestCov2') , ('TestCov2','TestCov3') ,  ('TestCov3','TestCov4'),  ('TestCov4','TestCov5') , ('TestCov5','TestCov1')] , Data = [], Objectives = [])""",'Detected a cyclic dependency'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestCov2+1') , ('TestCov2','TestCov1-1') ,  ('TestCov3','TestCov4'),  ('TestCov4','TestCov5') , ('TestCov5','TestCov1')] , Data = [], Objectives = [])""",'Detected a cyclic dependency'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestCov2') , ('TestCov2','TestFormulaToCreateCyclicReferenceForTestDistribution') ,  ('TestCov3','TestCov4'),  ('TestCov4','TestCov5') , ('TestCov5','TestCov1')] , Data = [], Objectives = [])""",'Detected a cyclic dependency'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestCov2') , ('TestCov2','TestCov3') ,  ('TestCov3','TestCov4'),  ('TestCov4','TestCov5')] , Data = [], Objectives = [])""",'Dependency on an empty parameter'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','BadTestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','TestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','BadTestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','TestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','BadTestDistributionGeometric'),  ('TestCov4','TestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','BadTestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','TestDistributionUniform') , ('TestCov5','BadTestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('BoundedParamForTestDistribution','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','TestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('BoundedParamForTestDistribution','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','TestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('BoundedParamForTestDistribution','TestDistributionGeometric'),  ('TestCov4','TestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('BoundedParamForTestDistribution','TestDistributionUniform') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        Tests.append(("""DB.PopulationSet(ID = 0, Name='Test Distribution Based Population', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCov1','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','TestDistributionUniform') , ('BoundedParamForTestDistribution','TestDistributionGaussian')] , Data = [], Objectives = []).GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = 1000)""",'does not fall within the specified validation bounds'))
        

        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Distribution based Test B #' + str(Num) + ' Ok - This use of a distribution should generate an error')
            else:
                assert False, 'Distribution based test B # ' + str(Num) + ' FAILRUE - This use of a distribution should generate an error.'
        
        DB.Params.Modify( 'NumberOfErrorsConsideredAsWarningsForPopulationGeneration', DB.Param(Name = 'NumberOfErrorsConsideredAsWarningsForPopulationGeneration', Formula = str(OriginalNumberOfErrorsConsideredAsWarningsForPopulationGeneration) , ParameterType = 'System Option' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        
        
        
        # Check population set validity checking
        
        Tests = []
        Tests.append(( """DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Faulty Population set', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','NonExistingDistribution(0.5)') , ('Smoke','Bernoulli(0.25)') , ('AF','Bernoulli(0.75)') , ('Age','Gaussian(60,10)') , ('BP','Gaussian(12,10)')] , Data = [], Objectives = []), ProjectBypassID = 0)""" ,'is not a valid name of a parameter nor a valid function name'))
        Tests.append(( """DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Faulty Population set', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','Gaussian(0.5)') , ('Smoke','Bernoulli(0.25)') , ('AF','Bernoulli(0.75)') , ('Age','Gaussian(60,10)') , ('BP','Gaussian(12,10)')] , Data = [], Objectives = []), ProjectBypassID = 0)""" ,'This may happen if the wrong number of parameters was specified for a function'))
        Tests.append(( """DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Faulty Population set', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','Gaussian(0.5,0.1)') , ('Smoke','Bernoulli(0.25)') , ('NotExistingParam','Bernoulli(0.75)') , ('Age','Gaussian(60,10)') , ('BP','Gaussian(12,10)')] , Data = [], Objectives = []), ProjectBypassID = 0)""" ,'the parameter does not exist in the parameters that were defined'))
        Tests.append(( """DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Faulty Population set', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','NotExistingParam + Bernoulli(0.25)') , ('Smoke','Bernoulli(0.25)') , ('AF','Bernoulli(0.75)') , ('Age','Gaussian(60,10)') , ('BP','Gaussian(12,10)')] , Data = [], Objectives = []), ProjectBypassID = 0)""" ,'used in the expression is not a valid name of a parameter nor a valid function name'))
        Tests.append(( """DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Faulty Population set', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','Bernoulli(Age/100)') , ('Smoke','Bernoulli(0.25)') , ('AF','Bernoulli(0.75)') , ('Age','Gander*10+Gaussian(60,10)') , ('BP','Gaussian(12,10)')] , Data = [], Objectives = []), ProjectBypassID = 0)""" ,'used in the expression is not a valid name of a parameter nor a valid function name'))
        Tests.append(( """DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Faulty Population set', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','Bernoulli(0.5)') , ('Gender','Bernoulli(0.25)') , ('AF','Bernoulli(0.75)') , ('Age','Gaussian(60,10,1)') , ('BP','Gaussian(12,10)')] , Data = [], Objectives = []), ProjectBypassID = 0)""" ,'Duplicate column names detected'))
        Tests.append(( """DB.PopulationSets.AddNew(DB.PopulationSet(ID = 0, Name='Faulty Population set', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Gender','') , ('Smoke','') , ('AF','') , ('Age','') , ('BP','')] , Data = [[11,1,1,60,12]], Objectives = []), ProjectBypassID = 0)""" ,'Parameter Validation Error: The value does not fall within the specified validation bounds provided'))
        Tests.append(( """DB.PopulationSet(ID = 0, Name='Faulty Population set', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestCovariateFuncToBeUsedLaterToTestFailure','TestDistributionBernoulli') , ('TestCov2','TestDistributionBinomial') ,  ('TestCov3','TestDistributionGeometric'),  ('TestCov4','BlankParamForTestDistribution') , ('TestCov5','TestDistributionGaussian')] , Data = [], Objectives = [])""",'used in the population set, is of an invalid parameter type to be used in a population set'))

        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Population Set Validation Test #' + str(Num) + ' OK - an invalid test was detected')
            else:
                assert False, 'Population Set Validation Test #' + str(Num) + ' test FAILURE - an invalid test was not detected'






class TestCostWizardParser(GenericSetupAndTearDown):

    def test_CostWizardParser(self):

        # Test the CostWizard parser
        
        # Add a few parameters
        DB.Params.AddNew(DB.Param(Name = 'TestCovariate1', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'TestCovariate2', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'TestCovariate3', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        
        CostWizardStr = 'CostWizard (0, 100.12, [TestCovariate1,TestCovariate2, TestCovariate3], [ 1, 2, 3.0] )'
        
        try:
            ParsedStruct = DB.CostWizardParserForGUI(CostWizardStr)
        except:
            CheckException(None,'CostWizard parser initial test FAILURE - Error detected while parsing the CostWizard')
        else:
            if ParsedStruct != [0,'100.12',['TestCovariate1','TestCovariate2','TestCovariate3'], ['1','2','3.0'] ]:
                assert False, 'CostWizard parser initial test FAILURE - Information was not correctly parsed. Here is the parsed information:' +str(ParsedStruct)
            else:
                print 'CostWizard parser initial test is OK - the expression was parsed correctly'
      
        
        try:
            CostWizardStrReconstructed = DB.ConstructCostWizardString(ParsedStruct)
        except:
            CheckException(None, 'ConstructCostWizardString test FAILURE - Error detected')
        else:
            if DB.RemoveChars(CostWizardStrReconstructed) != DB.RemoveChars(CostWizardStr):
                assert False, 'ConstructCostWizardString test FAILURE - Reconstructed string does not match the original string: ' +str(CostWizardStrReconstructed)
            else:
                print 'ConstructCostWizardString test is OK - the expression was reassembled correctly'
        
        
        # A set of wrong CostWizard examples
        BadCostWizardStrings = []
        BadCostWizardStrings.append(('TestCovariate1','This string is too short to represent a valid Cost Wizard string '))
        BadCostWizardStrings.append(('(0, 100.12, [TestCovariate1,TestCovariate2, TestCovariate3], [ 1, 2, 3.0] ) ','the expression evaluation will result in a vector or a matrix'))
        BadCostWizardStrings.append(('CostWizard(2, 100.12, [TestCovariate1,TestCovariate2, TestCovariate3], [ 1, 2, 3.0] ) ','The expression was parsed correctly. However it cannot be calculated using dummy parameter values. This may happen if the wrong number of parameters was specified for a function, or if the function generates an error for the dummy value of zero for all parameters'))
        BadCostWizardStrings.append(('CostWizard(100.12, [TestCovariate1,TestCovariate2, TestCovariate3], [ 1, 2, 3.0] ) ','The expression was parsed correctly. However it cannot be calculated using dummy parameter values. This may happen if the wrong number of parameters was specified for a function, or if the function generates an error for the dummy value of zero for all parameters'))
        BadCostWizardStrings.append(('CostWizard( [TestCovariate1,TestCovariate2, TestCovariate3],0,100.12, [ 1, 2, 3.0] ) ','The expression was parsed correctly. However it cannot be calculated using dummy parameter values. This may happen if the wrong number of parameters was specified for a function, or if the function generates an error for the dummy value of zero for all parameters'))
        BadCostWizardStrings.append(('CostWizard (0, 100.12, [TestCovariate2, TestCovariate3], [ 1, 2, 3.0] )','The expression was parsed correctly. However it cannot be calculated using dummy parameter values. This may happen if the wrong number of parameters was specified for a function, or if the function generates an error for the dummy value of zero for all parameters'))
        BadCostWizardStrings.append(('CostWizard (0, 100.12, [None,TestCovariate2, TestCovariate3], [ 1, 2, 3.0] )','The term (token) "None" is a banned system reserved name. Please check the expression for typos as this name should not be used'))
        BadCostWizardStrings.append(('CostWizard (0, 100.12, 7, [ 1, 2, 3.0] )','The expression was parsed correctly. However it cannot be calculated using dummy parameter values. This may happen if the wrong number of parameters was specified for a function, or if the function generates an error for the dummy value of zero for all parameters'))
        BadCostWizardStrings.append(('CostWizard (0, 100.12, (TestCovariate1,TestCovariate2, TestCovariate3), [ 1, 2, 3.0] )','a comma is not allowed between parenthesis, except as part of a parameter list for a function'))
        BadCostWizardStrings.append(('CostWizard (0, 100.12, [[1,2,3],TestCovariate2, TestCovariate3], [ 1, 2, 3.0] )','The expression was parsed correctly. However it cannot be calculated using dummy parameter values. This may happen if the wrong number of parameters was specified for a function, or if the function generates an error for the dummy value of zero for all parameters'))
        BadCostWizardStrings.append(('CostWizard (0, 100.12, [TestVec,TestCovariate2, TestCovariate3], [ 1, 2, 3.0] )','used in the expression is not a valid name of a parameter nor a valid function name'))
        BadCostWizardStrings.append(('CostWizard (0, 100.12, [TestCovariate1,TestCovariate2, TestCovariate3], [ [1,2,3], 2, 3.0] )','The expression was parsed correctly. However it cannot be calculated using dummy parameter values. This may happen if the wrong number of parameters was specified for a function, or if the function generates an error for the dummy value of zero for all parameters'))
        BadCostWizardStrings.append(('CostWizard (0, 100.12, [TestCovariate1,TestCovariate2, TestCovariate3], [ 1, 2, 3.0] ) + 100','To use the cost Wizard correctly, the expression must include the Cost Wizard Function alone'))
        BadCostWizardStrings.append(('100+CostWizard (0, 100.12, [TestCovariate1,TestCovariate2, TestCovariate3], [ 1, 2, 3.0] )','The text does not start with the term "CostWizard" and therefore cannot be parsed. To use the cost Wizard correctly, the expression must start with this term.'))
        # Loop through all wrong CostWizard examples

        for (Num,(CurrentTest,ExceptionInString)) in enumerate(BadCostWizardStrings):
            try:
                DB.CostWizardParserForGUI(CurrentTest)
            except:
                CheckException(ExceptionInString ,'CostWizard parser test #' + str(Num) + ' OK - the expression should not parse well')
            else:
                assert False, 'CostWizard parser test #' + str(Num) + ' FAILURE - the expression was parsed correctly, while needed to raise an error'
    
    
class TestTableRepresentationInRuntime(GenericSetupAndTearDown):

    def test_TableRepresentationInRuntime(self):
        # Test table representation in runtime
        Iter=0
        GoodGenderIndex = [0, 1]
        BadGenderIndex = [0.5 ,2]
        GoodAgeIndex = [10, 30, 50]
        BadAgeIndex = [-100 , 100]
        GoodTimeIndex = [2, 4, 6, 8]
        BadTimeIndex = [0, 1, 3, 10]
        
        for Gender in GoodGenderIndex + BadGenderIndex:
            for Age in GoodAgeIndex + BadAgeIndex:
                for Time in GoodTimeIndex + BadTimeIndex:
                    if (Gender in GoodGenderIndex) and (Age in GoodAgeIndex) and (Time in GoodTimeIndex):
                        Iter = Iter+1
                        OutOfBound = False            
                    else:
                        OutOfBound = True
                    try:
                        # Simulate 'Table([[[1,2,3,4],[5,6,7,8],[9,10,11,12]],[[13,14,15,16],[17,18,19,20],[21,22,23,24]]] , [[Gender,NaN,0,1],[Age,0,20,40,60],[Time,NaN,2,4,6,8]])'
                        Result = DB.TableRunTime([[Gender,[DB.NaN,0,1]],[Age,[0,20,40,60]],[Time,[DB.NaN,2,4,6,8]]],[[[1,2,3,4],[5,6,7,8],[9,10,11,12]],[[13,14,15,16],[17,18,19,20],[21,22,23,24]]])
                    except:
                        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                        if OutOfBound:            
                            print 'Table test OK for Age = ' + str(Age) + ', Gender = ' + str(Gender) + ', Time = ' + str(Time) + ' - the expression should raise an error. Here are details about the error:' + str(ExceptValue)
                        else:
                            CheckException(None, 'Table test FAILURE for Age = ' + str(Age) + ', Gender = ' + str(Gender) + ', Time = ' + str(Time) + ' - the expression should raise an error')
                    else:
                        if Result == Iter:
                            print 'Table test OK for Age = ' + str(Age) + ', Gender = ' + str(Gender) + ', Time = ' + str(Time) + ' - the expression returns the expected value'
                        else:
                            assert False, 'Table test FAILURE for Age = ' + str(Age) + ', Gender = ' + str(Gender) + ', Time = ' + str(Time) + '  - the expression returns the value = ' + str(Result)+ ' when expecting = ' + str(Iter)


    def test_TableExpressionParsing(self):
        # Test Expressions in a table
        DB.Params.AddNew(DB.Param(Name = 'TestCovariate1', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'TestCovariate2', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = 'Testing'), ProjectBypassID = 0)
        
        Tests = []
        Tests.append(("""Table([[TestCovariate1 + 1, [NaN,0,1]]], [4,9])""",9))
        Tests.append(("""Table([[1,[NaN,0,1]]], [TestCovariate1,TestCovariate2])""",1))
        Tests.append(("""Table([[0,[NaN,0,1]]], [Exp(10),TestCovariate1])""",DB.Exp(10)))
        Tests.append(("""Table([[0,[NaN,0,1]]], [6+Min(3,2),9])""",8))
        Tests.append(("""Table([[1-1,[NaN,0,1]]], [4,9])""",4))
        Tests.append(("""Table([[Min(Max(TestCovariate1+5,0),1),[NaN,0,1]]], [4,9])""",9))
        Tests.append(("""Table([[1.5, [0,1,2,3]], [0, [NaN,0,1,2,3,4,5,6,7,8,9]], [2, [NaN,0,1,2,3,4,5,6,7,8,9]]] ,  [[[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0]] , [[1,2,3000,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0]], [[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0],[1,2,3,4,5,6,7,8,9,0]] ])""",3000))
      
        
        # Run the tests for the expression
        for (Num,(Test,TestResult)) in enumerate(Tests):
            try:
                DB.Expr(Test)
            except:
                CheckException(None, 'Table With Expression Test A-#' + str(Num) + ' FAILURE - a valid test did not pass')
            else:
                print 'Table With Expression Test A-#' + str(Num) + ' OK - a valid test passed'

        TestCovariate1=0
        TestCovariate2=1
        NaN=DB.NaN
        Exp = DB.Exp
        Min = DB.Min
        Max = DB.Max
        Table = DB.Table
        print 'Setting the following:'
        print 'TestCovariate1 = ' + str(TestCovariate1)
        print 'TestCovariate2 = ' + str(TestCovariate2)
        print 'NaN = ' + str(NaN)
        print 'Exp = ' + str(Exp)
        print 'Min = ' + str(Min)
        print 'Max = ' + str(Max)
        print 'Table = ' + str(Table)
        
        for (Num,(Test,TestResult)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(None, 'Table With Expression Test B-#' + str(Num) + ' FAILURE - a valid test did not pass')
            else:
                print 'Table With Expression Test B-#' + str(Num) + ' OK - a valid test passed'


        Table = DB.TableRunTime
        print 'Setting the following:'
        print 'Table = ' + str(Table)

        Table = DB.TableRunTime
        for (Num,(Test,TestResult)) in enumerate(Tests):
            try:
                Value = eval(Test)
            except:
                CheckException(None, 'Table With Expression Test C-#' + str(Num) + ' FAILURE - a valid test did not pass')
            else:
                if Value != TestResult:
                    assert False, 'Table With Expression Test C-#' + str(Num) + ' FAILURE - Calculated value does not correspond to the expected value. Calculated value was ' + str(Value) + ' instead of the expected result of ' + str(TestResult)
                else:
                    print 'Table With Expression Test C-#' + str(Num) + ' OK - a valid test passed'



        # Invalid table test
        Tests = []
        Tests.append(("""Table([1, [NaN,0,1]], [4,9])""",'invalid DimensionsArray that does not contain lists'))
        Tests.append(("""Table([[1,[NaN,0,1]]], [[1,2]])""",'Table Size Validation Error: Table sizes do not match array sizes - expected size 2 got 1 with the subset [[1, 2]]'))
        Tests.append(("""Table([[1,[NaN,0,1,2,3,4,5]]], [4,9])""",'Table Size Validation Error: Table sizes do not match array sizes - expected size 6 got 2 with the subset [4, 9]'))
        Tests.append(("""Table([[0.5,[-Inf,2,1]]], [1,9])""",'Table Expression Validation Error: Range bound items are not sorted in ascending order: 2 is higher than 1.'))
        Tests.append(("""Table([[0.5,[-Inf,1,2]], [0.5,[-Inf,1,2]]], [Min(1,2),[3,4]])""",'able Size Validation Error: Table sizes do not match array sizes - the size contains more dimensions than the data - expected size 2 with the subset 1'))
      
        # Run the tests for the invalid tables
        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                DB.Expr(Test)
            except:
                CheckException(ExceptionInString, 'Table With Expression Test D-#' + str(Num) + ' OK - an invalid test was detected')
            else:
                assert False, 'Table With Expression Test D-#' + str(Num) + ' FAiLURE - an invalid test passed'
        



     

class TestCopyEqualityAndModifyDeleteRecords(GenericSetupAndTearDown):


    def setUp(self):
        " define special database environment "

        #Run full stup first which is included
        SetupFullDB()
       
        print 'Test Setup Special Environment'
        # use this method as an override when a special setup is required
        
        DB.CreateBlankDataDefinitions()
        # Define parameters
        DB.Params.AddNew(DB.Param(Name = 'TestParam', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        DB.Params.AddNew(DB.Param(Name = 'TestCoefficient', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,Inf]', Notes = ''), ProjectBypassID = 0)
        
        # Define States
        DB.States.AddNew(DB.State(ID = 910021 , Name = 'TestState1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
        DB.States.AddNew(DB.State(ID = 91000002 , Name = 'TestState2' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
        DB.States.AddNew(DB.State(ID = 91000003 , Name = 'TestStateNotToBeUsed' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = True , ChildStates = [] ), ProjectBypassID = 0)
        
        # Add SubProcess
        DB.States.AddNew(DB.State(ID = 91000000 , Name = 'Test Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [ 910021, 91000002, 91000003 ] ), ProjectBypassID = 0)
        
        # Create the model-study definitions
        DB.StudyModels.AddNew(DB.StudyModel( ID = 91000000 , Name = 'Test Example Model' , Notes = '' , DerivedFrom = 0 , MainProcess = 91000000  ), ProjectBypassID = 0)
        
        ### Create the model definitions
        ### Model Transitions
        # MainProcess
        
        DB.Transitions.AddNew(DB.Transition(StudyModelID = 91000000, FromState = 910021, ToState = 91000002, Probability = DB.Expr('TestCoefficient')), ProjectBypassID = 0)
        
        # Populate the table with population sets
        DB.PopulationSets.AddNew(DB.PopulationSet(ID = 9101, Name='Population set for testing', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestParam','') ,('TestState1',''), ('TestState2','')] , Data = [[ 30, 1, 0 ]]*9 + [[30,0,1]], Objectives = []), ProjectBypassID = 0)
       
        # Define simulation Rules
        SimRuleList = []
        SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestCoefficient', SimulationPhase = 1, OccurrenceProbability = '' , AppliedFormula = '0.0717')]
        SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestParam', SimulationPhase = 1, OccurrenceProbability = '1' , AppliedFormula = 'TestParam +1')]
        
        # Define the project
        DB.Projects.AddNew(DB.Project(ID = 9101, Name = 'Test Simulation Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
        
        # Define Results for the project
        DB.SimulationResults.AddNew(DB.SimulationResult(ProjectID = 9101, PreparedPopulationSet = None , ID = 9101), ProjectBypassID = 0)

        # Define another project for double locking testing
        DB.Projects.AddNew(DB.Project(ID = 9102, Name = 'Test Simulation Project 1' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)



    def test_Equlity(self):
        
        # Test the detailed equality function #
        # Define the project
        ProjectBase = DB.Projects[9101]

        SimRuleList = []
        SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestCoefficient', SimulationPhase = 1, OccurrenceProbability = '' , AppliedFormula = '0.0717')]
        SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestParam', SimulationPhase = 1, OccurrenceProbability = '1' , AppliedFormula = 'TestParam +1')]

        # Define the same project
        ProjectCmp = DB.Project(ID = 9101, Name = 'Test Simulation Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   )
        if DB.IsEqualDetailed(ProjectBase,ProjectCmp):
            print 'Test of instance comparison OK - objects equal'
        else:
            assert False, 'Test of instance comparison FAILURE - objects should be equal'
        
        # Define the same project with a different ID
        ProjectCmp = DB.Project(ID = 9199, Name = 'Test Simulation Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   )
        if DB.IsEqualDetailed(ProjectBase,ProjectCmp):
            print 'Test of instance comparison OK - objects equal'
        else:
            assert False, 'Test of instance comparison FAILURE - objects should be equal'
        
        # Define a different project with a string change
        ProjectCmp = DB.Project(ID = 9101, Name = 'Test Simulation Project - changed' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   )
        if DB.IsEqualDetailed(ProjectBase,ProjectCmp):
            assert False, 'Test of instance comparison FAILURE - objects should be different'
        else:
            print 'Test of instance comparison OK - objects are different'
            
        # Define a different project with a number changed
        ProjectCmp = DB.Project(ID = 9101, Name = 'Test Simulation Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 2  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   )
        if DB.IsEqualDetailed(ProjectBase,ProjectCmp):
            assert False, 'Test of instance comparison FAILURE - objects should be different'
        else:
            print 'Test of instance comparison OK - objects are different'
        
        # Define a different project with a list changed
        SimRuleList1 = []
        SimRuleList1 = SimRuleList1 + [ DB.SimulationRule(AffectedParam = 'TestParam', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'TestParam +2')]
        ProjectCmp = DB.Project(ID = 9101, Name = 'Test Simulation Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList1 , DerivedFrom = 0   )
        if DB.IsEqualDetailed(ProjectBase,ProjectCmp):
            assert False, 'Test of instance comparison FAILURE - objects should be different'
        else:
            print 'Test of instance comparison OK - objects are different'
        
        
    def test_CopyFunctions(self):
        
        # Test copying functions
        TestParamCopy = DB.Params.Copy('TestParam')
        if TestParamCopy.ParameterType != 'Number':
            assert False, 'Test of copying FAILURE - objects should have same type'
        else:
            print 'Test of copying OK - objects have the same type'
            
        # Check Type equal
        TestStateCopy1 = DB.States.Copy(910021)
        
        TestStateCopy2 = DB.States.Copy(910021)
        if TestStateCopy1.Name != 'TestState1_0' or TestStateCopy2.Name != 'TestState1_1':
            assert False, 'Test of copying FAILURE - copied objects names are not following copying rules'
        else:
            print 'Test of copying OK - copied objects names are following copying rules'
        # Check new name number increase
        
        TestStudyModelCopy = DB.StudyModels.Copy(91000000)
        # Check subprocess and transitions exists
        CopyModelRelatedTransitions = TestStudyModelCopy.FindTransitions()
        ModelRelatedTransitions = DB.StudyModels[91000000].FindTransitions()
        MainProcessCopyID = TestStudyModelCopy.MainProcess
        if MainProcessCopyID != DB.StudyModels[91000000].MainProcess or len(ModelRelatedTransitions) != len(CopyModelRelatedTransitions) or TestStudyModelCopy.DerivedFrom != 91000000:
            assert False, 'Test of copying FAILURE - copied objects main process does not agree or the transitions number do not, or Derived field is ivalid'
        else:
            print 'Test of copying OK - copied objects main process agree while transitions also, and Derived field is ok'
        
        TestPopulationSetCopy = DB.PopulationSets.Copy(9101)
        if TestPopulationSetCopy.DerivedFrom != 9101: 
            assert False, 'Test of copying FAILURE - copied object Derived field is ivalid'
        else:
            print 'Test of copying OK - copied object Derived field is OK'
        
        TestProjectCopy = DB.Projects.Copy(9101)
        # Check Derived From
        # Check Rules were copied
        if TestProjectCopy.DerivedFrom != 9101 or not (DB.IsEqualDetailed(TestProjectCopy.SimulationRules, DB.Projects[9101].SimulationRules)): 
            assert False, 'Test of copying FAILURE - copied object Derived field is ivalid or simulation rules do not agree'
        else:
            print 'Test of copying OK - copied object Derived field is OK - and simulation rules agree'
        
        # Delete all model transitions
        for CopyModelRelatedTransition in CopyModelRelatedTransitions:
            DB.Transitions.Delete(CopyModelRelatedTransition, ProjectBypassID = 0)
        
        # Copy the model transitions again from the original model
        TestStudyModelCopy.CopyTransitionsFromAnotherStudyModel(91000000)
        CopyModelRelatedTransitions = TestStudyModelCopy.FindTransitions()
        if len(ModelRelatedTransitions) != len(CopyModelRelatedTransitions):
            assert False, 'Test of Transition copying FAILURE - transitions numbers do not agree'
        else:
            print 'Test of Transition copying OK - transitions numbers agree'
        
        # Now delete these new copies
        DB.Projects.Delete(TestProjectCopy.ID, ProjectBypassID = 0)
        DB.PopulationSets.Delete(TestPopulationSetCopy.ID, ProjectBypassID = 0)
        # Delete all model transitions
        for CopyModelRelatedTransition in CopyModelRelatedTransitions:
            DB.Transitions.Delete(CopyModelRelatedTransition, ProjectBypassID = 0)
        DB.StudyModels.Delete(TestStudyModelCopy.ID, ProjectBypassID = 0)
        #DB.States.Delete(MainProcessCopyID, ProjectBypassID = 0)
        # Delete copy states
        DB.States.Delete(TestStateCopy1.ID, ProjectBypassID = 0)
        DB.States.Delete(TestStateCopy2.ID, ProjectBypassID = 0)
        # Delete copy parameters
        DB.Params.Delete(str(TestParamCopy), ProjectBypassID = 0)
        
        
    def test_ModifyDeleteRecords(self):
        
        SimRuleList = []
        SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestCoefficient', SimulationPhase = 1, OccurrenceProbability = '' , AppliedFormula = '0.0717')]
        SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestParam', SimulationPhase = 1, OccurrenceProbability = '1' , AppliedFormula = 'TestParam +1')]
        SimRuleList1 = []
        SimRuleList1 = SimRuleList1 + [ DB.SimulationRule(AffectedParam = 'TestParam', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'TestParam +2')]

        # Test Bad Project examples:
        Tests = []
        Tests.append(( """DB.Projects.AddNew(DB.Project(ID = 0, Name = 'BAD Project Example' , Notes = 'Testing', PrimaryModelID = 0  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)""", 'The Primary Model to be used by the project is undefined' ))
        Tests.append(( """DB.Projects.AddNew(DB.Project(ID = 0, Name = 'BAD Project Example' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 0 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)""", 'The population set to be used by the project is undefined' ))
        Tests.append(( """DB.Projects.AddNew(DB.Project(ID = 0, Name = 'BAD Project Example' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 1 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)""", 'The population set to be used by the project is undefined' ))
        Tests.append(( """DB.Projects.AddNew(DB.Project(ID = 0, Name = 'BAD Project Example' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 0  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)""", 'The number of simulation steps should be a positive integer' ))
        Tests.append(( """DB.Projects.AddNew(DB.Project(ID = 0, Name = 'BAD Project Example' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = -2  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)""", 'The number of repetitions should be a positive integer' ))

        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Project Validation Test#' + str(Num) + ' OK - an invalid test was detected')
            else:
                assert False, 'Project Validation Test#' + str(Num) + ' test FAILURE -  an invalid test was not detected'

        # Test Simulation Rule examples:
        Tests = []
        Tests.append(( """DB.SimulationRule(AffectedParam = 'NonExistingCoefficient', SimulationPhase = 1 , OccurrenceProbability = '' , AppliedFormula = '0.0717')""",'used in the expression is not a valid name of a parameter nor a valid function name'))
        Tests.append(( """DB.SimulationRule(AffectedParam = 'TestCoefficient', SimulationPhase = 1 , OccurrenceProbability = '' , AppliedFormula = '')""",'The applied formula field in the simulation rule cannot be empty'))
        Tests.append(( """DB.SimulationRule(AffectedParam = 'TestParam', SimulationPhase = 1 , OccurrenceProbability = '1213213NotAnExpression' , AppliedFormula = '0.0717')""",'used in the expression is not a valid name of a parameter nor a valid function name'))
        Tests.append(( """DB.SimulationRule(AffectedParam = 'TestParam', SimulationPhase = 11 , OccurrenceProbability = '' , AppliedFormula = '0.0717')""",'Simulation Phase is out of range.'))
        Tests.append(( """DB.SimulationRule(AffectedParam = 'TestParam', SimulationPhase = -1 , OccurrenceProbability = '' , AppliedFormula = '0.0717')""",'Simulation Phase is out of range.'))
        Tests.append(( """DB.SimulationRule(AffectedParam = 'TestState1', SimulationPhase = 1 , OccurrenceProbability = '' , AppliedFormula = '0.0717')""",'The affected parameter has an invalid parameter type for a simulation rule'))
        Tests.append(( """DB.SimulationRule(AffectedParam = 'RandomSeed', SimulationPhase = 0 , OccurrenceProbability = 'TestState1' , AppliedFormula = '0.0717')""",'System Option initialization is allowed only in the initialization phase and no occurrence probability is allowed'))
        Tests.append(( """DB.SimulationRule(AffectedParam = 'RandomSeed', SimulationPhase = 1 , OccurrenceProbability = '' , AppliedFormula = '0.0717')""",'System Option initialization is allowed only in the initialization phase and no occurrence probability is allowed'))

        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Project Simulation Rule Validation Test#' + str(Num) + ' OK - an invalid test was detected')
            else:
                assert False, 'Project Simulation Rule Validation Test#' + str(Num) + ' test FAILURE -  an invalid test was not detected'

        ### Now modify the data ###

        # Phase 1
        # Test modification in a locked environment
        Tests = []
        Tests.append(( """DB.Params.Delete('TestParam', ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.States.Delete(910021, ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.StudyModels.Delete(91000000, ProjectBypassID = 0)""", 'Locking projects are: Test Simulation Project' ))
        Tests.append(( """DB.Transitions.Delete((91000000, 910021, 91000002), ProjectBypassID = 0)""", 'Locking projects are: Test Simulation Project' ))
        Tests.append(( """DB.PopulationSets.Delete(9101, ProjectBypassID = 0)""", 'Locking projects are: Test Simulation Project' ))
        Tests.append(( """DB.Projects.Delete(9101, ProjectBypassID = 0)""", 'Locking projects are: Test Simulation Project' ))
        Tests.append(( """DB.Params.Modify('TestParam', DB.Param(Name = 'TestParamModified', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.States.Modify(910021, DB.State(ID = 0 , Name = 'TestState1ModifiedWillNotBeRetained' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ) , ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.StudyModels.Modify(91000000 , DB.StudyModel( ID = 0 , Name = 'Test Example Will not be retained' , Notes = '' , DerivedFrom = 0 , MainProcess = 91000000  ) , ProjectBypassID = 0)""", 'Locking projects are: Test Simulation Project' ))
        Tests.append(( """DB.Transitions.Modify( (91000000, 910021, 91000002) , DB.Transition(StudyModelID = 91000000, FromState = 910021, ToState = 91000002, Probability = DB.Expr('0.0717121212') ), ProjectBypassID = 0)""", 'Locking projects are: Test Simulation Project' ))
        Tests.append(( """DB.PopulationSets.Modify(9101, DB.PopulationSet(ID = 0, Name='Will not be retained', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestParam','')] , Data = [[ 30 ]]*10, Objectives = []), ProjectBypassID = 0)""", 'Locking projects are: Test Simulation Project' ))
        Tests.append(( """DB.Projects.Modify(9101, DB.Project( 0, Name = 'Test Project Modified will not be retained' , Notes = 'Testing', PrimaryModelID = 91000000 , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList1 , DerivedFrom = 0   ) , ProjectBypassID = 0)""", 'Locking projects are: Test Simulation Project' ))

        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Modification Phase 1-' + str(Num) + ' test OK - Locked Dependency should raise an error')
            else:
                assert False, 'Modification Phase 1-' + str(Num) + ' test FAILURE - Modification of a Dependant record that is locked was allowed'




        
        # Phase 2
        # Now unlock the simulation project
        try:
            DB.SimulationResults.Delete(9101, ProjectBypassID = 0)
        except:
            CheckException('','Modification test Phase 2 init FAILURE - Unlocking Simulation Dependency raised an error')
        else:
            print 'Modification test Phase 2 init OK - unlocking Simulation dependency successful'
        
        # The test below should now be still locked by the simulation project
        Tests = []
        Tests.append(( """DB.StudyModels.Delete(91000000, ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.Transitions.Delete((91000000, 910021, 91000002), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.PopulationSets.Delete(9101, ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.Params.Modify('TestParam', DB.Param(Name = 'TestParamModified', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.States.Modify(910021, DB.State(ID = 0 , Name = 'TestState1ModifiedWillNotBeRetained' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.StudyModels.Modify(91000000 , DB.StudyModel( ID = 0 , Name = 'Test Example Will not be retained' , Notes = '' , DerivedFrom = 0 , MainProcess = 91000000  ), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.Transitions.Modify( (91000000, 910021, 91000002) , DB.Transition(StudyModelID = 91000000, FromState = 910021, ToState = 91000002, Probability = DB.Expr('0.0717121212') ), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.PopulationSets.Modify(9101, DB.PopulationSet(ID = 0, Name='Will not be retained', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestParam','') ,('TestState1',''), ('TestState2','')] , Data = [[ 30, 1, 0 ]]*10 + [[30,0,1]], Objectives = []), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))

        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Modification Phase 2-' + str(Num) + ' test OK - Locked Dependency on a project should raise an error')
            else:
                assert False, 'Modification Phase 2-' + str(Num) + ' test FAILURE - Modification of a Dependant record on project that is locked was allowed'


        
        # Phase 3
        # Test project bypass is still blocked since two projects use the data or since
        # a model/study are being deleted.
        
        Tests = []
        Tests.append(( """DB.Transitions.AddNew(DB.Transition(StudyModelID = 91000000, FromState = 91000002, ToState = 910021, Probability = DB.Expr('7.17') ), ProjectBypassID = 9101)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project 1' ))
        Tests.append(( """DB.Transitions.Delete((91000000, 91000002, 910021) , ProjectBypassID = 9101)""", 'Cannot delete record as the ID key' ))
        Tests.append(( """DB.Transitions.Modify((91000000, 910021, 91000002) , DB.Transition(StudyModelID = 91000000, FromState = 910021, ToState = 91000002, Probability = DB.Expr('0.0717121212') ), ProjectBypassID = 9101)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project 1' ))
        Tests.append(( """DB.Transitions.Delete((91000000, 910021, 91000002) , ProjectBypassID = 9101)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project 1' ))
        Tests.append(( """DB.StudyModels.Modify(91000000 , DB.StudyModel( ID = 91000000 , Name = 'Test Example' , Notes = '' , DerivedFrom = 0 , MainProcess = 91000000  ), ProjectBypassID = 9101)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project 1' ))
        Tests.append(( """DB.PopulationSets.Modify(9101, DB.PopulationSet(ID = 0, Name='Will not be retained', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestParam','') ,('TestState1',''), ('TestState2','')] , Data = [[ 30, 1, 0 ]]*10 + [[30,0,1]], Objectives = []), ProjectBypassID = 9101)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project 1' ))
        Tests.append(( """DB.PopulationSets.Modify(9101, DB.PopulationSet(ID = 9101, Name='Population set for testing', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestParam','') ,('TestState1',''), ('TestState2','')] , Data = [[ 30, 1, 0 ]]*10 + [[30,0,1]], Objectives = []), ProjectBypassID = 9101)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project 1' ))
        Tests.append(( """DB.StudyModels.Delete(91000000 , ProjectBypassID = 9101)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.PopulationSets.Delete(9101, ProjectBypassID = 9101)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))


        
        # Run the tests
        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Modification Phase 3-' + str(Num) + ' test OK - Locked Dependency to another project should raise an error')
            else:
                assert False, 'Modification Phase 3-' + str(Num) + ' test FAILURE - Modification of a Dependant record to another project that is locked was allowed'


        # Phase 4
        # Delete one project and try the bypass again
        try:
            DB.Projects.Delete(9102, ProjectBypassID = 0)
        except:
            CheckException(None, 'Modification Phase 4 init FAILURE - deleting the blocking Dependency raised an error')
        else:
            print 'Modification Phase 4 init OK - deletion of the blocking dependency was successful'

        
        # Run the tests from before, except the last two that
        
        for (Num,(Test,ExceptionInString)) in enumerate(Tests[:-2]):
            try:
                eval(Test)
            except:
                CheckException(None,'Modification Phase 4a-' + str(Num) + ' test FAILURE - Dependency on another entity raised an error')
            else:
                print 'Modification Phase 4a-' + str(Num) + ' test OK - Modification of a Dependant record was allowed by the system'
        
        
        # Run the last two tests from before

        # Run the tests
        for (Num,(Test,ExceptionInString)) in enumerate(Tests[-2:]):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Modification Phase 4b-' + str(Num) + ' test OK - Dependency on another entity should raise an error')
            else:
                assert False, 'Modification Phase 4b-' + str(Num) + ' test FAILURE - Modification of a Dependant record was allowed by the system'



        
        # Phase 5
        # Modify data not according to proper order and without bypass
        Tests = []
        Tests.append(( """DB.StudyModels.Modify(91000000, DB.StudyModel( ID = 0 , Name = 'Test Example that will never appear in the collection' , Notes = '' , DerivedFrom = 0 , MainProcess = 91000000  ), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.PopulationSets.Modify(9101, DB.PopulationSet(ID = 0, Name='Test Example that will never appear in the collection', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestParam','') ,('TestState1',''), ('TestState2','')] , Data = [[ 30, 1, 0 ]]*10 + [[30,0,1]], Objectives = []), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.Params.Modify('TestParam', DB.Param(Name = 'TestParamModified', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.States.Modify(910021, DB.State(ID = 0 , Name = 'TestState1ModifiedWillNotBeRetained' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ) , ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.StudyModels.Delete(91000000, ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.PopulationSets.Delete(9101, ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.Params.Delete('TestParam', ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.States.Delete(910021, ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.States.Modify(91000000, DB.State(ID = 91000000 , Name = 'Test Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [910021 , 91000002] ), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following study/model entries: Test Example' ))
        Tests.append(( """DB.States.Delete(91000000, ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following study/model entries: Test Example' ))
        
        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Modification Phase 5-' + str(Num) + ' test OK - Dependency on another entity should raise an error')
            else:
                assert False, 'Modification Phase 5-' + str(Num) + ' test FAILURE - Modification of a Dependant record was allowed by the system'
        
        


        
        # Phase 6
        # Test modification time
        # Define simulation Rules
        
        try:
            SimRuleList = []
            SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'TestParam', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = 'TestParam +1')]

            # Test change of time during modification
            OldTime = DB.Projects[9101].CreatedOn
            OldModTime = DB.Projects[9101].LastModified
            # Define the project
            DB.Projects.Modify( 9101, DB.Project( 0, Name = 'Test Project Modified will not be retained' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
            DB.Projects.Modify( 9101, DB.Project( 9101, Name = 'Test Project Modified' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
            NewTime = DB.Projects[9101].CreatedOn
            NewModTime = DB.Projects[9101].LastModified
        
            print ' Checking modification time'
            print ' Times before modification are Creation: ' + str(OldTime) + ' , Modification: ' + str(OldModTime)
            print ' Times after modification are Creation: ' + str(NewTime) + ' , Modification: ' + str(NewModTime)
            if OldTime == NewTime and NewModTime > OldModTime:
                print 'Modification Phase 6 (Time Stamp) Test OK - times are valid'
            else:
                assert False, 'Modification Phase 6 (Time Stamp) Test FAILURE - times are not valid'
        except:
            CheckException(None,'Modification Phase 6 (Time Stamp) Test FAILURE - Error encountered during test')



        Tests.append(( """DB.StudyModels.Modify(91000000, DB.StudyModel( ID = 0 , Name = 'Test Example that will never appear in the collection' , Notes = '' , DerivedFrom = 0 , MainProcess = 91000000  ), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.PopulationSets.Modify(9101, DB.PopulationSet(ID = 0, Name='Test Example that will never appear in the collection', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestParam','') ,('TestState1',''), ('TestState2','')] , Data = [[ 30, 1, 0 ]]*10 + [[30,0,1]], Objectives = []), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.Params.Modify('TestParam', DB.Param(Name = 'TestParamModified', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,1]', Notes = ''), ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.States.Modify(910021, DB.State(ID = 0 , Name = 'TestState1ModifiedWillNotBeRetained' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ) , ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.StudyModels.Delete(91000000, ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.PopulationSets.Delete(9101, ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following projects: Test Simulation Project' ))
        Tests.append(( """DB.Params.Delete('TestParam', ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.States.Delete(910021, ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant population sets: Population set for testing' ))
        Tests.append(( """DB.States.Modify(91000000, DB.State(ID = 91000000 , Name = 'Test Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [910021 , 91000002] ), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following study/model entries: Test Example' ))
        Tests.append(( """DB.States.Delete(91000000, ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following study/model entries: Test Example' ))




        
        # Phase 7
        # Perform some deletions and modifications accoring to proper order
        Tests = []
        Tests.append( """DB.Projects.Modify( 9101, DB.Project( 0, Name = 'Test Project Modified will not be retained' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 3  , NumberOfRepetitions = 100  , SimulationRules = SimRuleList1 , DerivedFrom = 0   ) , ProjectBypassID = 0)""")
        Tests.append( """DB.Projects.Delete(9101, ProjectBypassID = 0)""")
        Tests.append( """DB.Transitions.AddNew(DB.Transition(StudyModelID = 91000000, FromState = 910021, ToState = 91000003, Probability = DB.Expr('0.0000717') ), ProjectBypassID =0)""")
        Tests.append( """DB.Transitions.Delete((91000000, 910021, 91000003), ProjectBypassID = 0)""")
        Tests.append( """DB.StudyModels.Modify(91000000, DB.StudyModel( ID = 0 , Name = 'Test Example that will never appear in the collection' , Notes = '' , DerivedFrom = 0 , MainProcess = 91000000  ), ProjectBypassID = 0)""")
        Tests.append( """DB.PopulationSets.Modify(9101, DB.PopulationSet(ID = 0, Name='Test Example that will never appear in the collection', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('TestParam','') ,('TestState1',''), ('TestState2','')] , Data = [[ 30, 1, 0 ]]*10 + [[30,0,1]], Objectives = []), ProjectBypassID = 0)""")
        Tests.append( """DB.StudyModels.Delete(91000000, ProjectBypassID = 0)""")
        Tests.append( """DB.PopulationSets.Delete(9101, ProjectBypassID = 0)""")
        

        for (Num,Test) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(None,'Modification Phase 7-' + str(Num) + ' test FAILURE - Dependency on another entity raised an error')
            else:
                print 'Modification Phase 7-' + str(Num) + ' test OK - Modification of the record was allowed by the system'

        
        
        # Phase 8
        # Perform some more deletions and modifications out of order, non existing
        
        Tests = []
        Tests.append(( """DB.States.Modify(91000002 , DB.State(ID = 0 , Name = 'TestState1WillNotBeRetained' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ) , ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following states: Test Main Process' ))
        Tests.append(( """DB.States.Delete(91000002 , ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following states: Test Main Process' ))
        Tests.append(( """DB.Params.Delete('TestState1_Entered', ProjectBypassID = 0)""", 'To delete a state indicator, the state that created this state indicator should be deleted' ))
        Tests.append(( """DB.Params.Delete('TestState1', ProjectBypassID = 0)""", 'To delete a state indicator, the state that created this state indicator should be deleted' ))
        Tests.append(( """DB.Params.Delete('TestParamDoesNotExist', ProjectBypassID = 0)""", 'is an invalid ID in Parameters Collection' ))
        Tests.append(( """DB.States.Delete(91000007, ProjectBypassID = 0)""", 'is invalid in the instance of States Collection' ))
        Tests.append(( """DB.StudyModels.Delete(92000000, ProjectBypassID = 0)""", 'is invalid in the instance of the Studies/Models Collection' ))

        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Modification Phase 8-' + str(Num) + ' test OK - Dependency on another entity should raise an error')
            else:
                assert False, 'Modification Phase 8-' + str(Num) + ' test FAILURE - Modification of a Dependant record was allowed by the system'


        
        # Phase 9
        # Create several more blocking situations that were not yet tested
        try:
            # Create a parameter using another parameter
            DB.Params.AddNew(DB.Param(Name = 'TestParamUsingAnotherParam', Formula = 'TestCoefficient' , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
            # Create a new StudyModel that is not attached to any project and
            # a transition associated with it that uses a parameter
            DB.StudyModels.AddNew(DB.StudyModel( ID = 93000000 , Name = 'Test Example Model' , Notes = '' , DerivedFrom = 0 , MainProcess = 91000000  ), ProjectBypassID = 0)
            DB.Transitions.AddNew(DB.Transition(StudyModelID = 93000000, FromState = 910021, ToState = 91000002, Probability = DB.Expr('TestParam')), ProjectBypassID = 0)
        except:
            CheckException(None,'Modification Phase 9 init FAILURE - deleting the blocking Esimation Dependancy raised an error')
        else:
            print 'Modification Phase 9 init OK - deletion of the blocking Estimation dependency was successful'
        
        
        Tests = []
        Tests.append(( """DB.Params.Modify('TestCoefficient', DB.Param(Name = 'TestCoefModified', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0, 1]', Notes = ''), ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant parameters: TestParamUsingAnotherParam' ))
        Tests.append(( """DB.Params.Modify('TestParam', DB.Param(Name = 'TestParamModified', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0, 1]', Notes = ''), ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant transitions: In Test Example Model, From TestState1, To TestState2' ))
        Tests.append(( """DB.Params.Delete('TestCoefficient', ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant parameters: TestParamUsingAnotherParam' ))
        Tests.append(( """DB.Params.Delete('TestParam', ProjectBypassID = 0)""", 'To allow modification, delete/modify all the following dependant transitions: In Test Example Model, From TestState1, To TestState2' ))
        Tests.append(( """DB.StudyModels.Modify(93000000, DB.StudyModel( ID = 93000000 , Name = 'Test Example Model - Modified not to be added' , Notes = '' , DerivedFrom = 0 , MainProcess = 91000000  ), ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following transitions: In Test Example Model, From TestState1, To TestState2' ))
        Tests.append(( """DB.StudyModels.Delete(93000000, ProjectBypassID = 0)""", 'To allow modification, delete/modify all of the following transitions: In Test Example Model, From TestState1, To TestState2' ))

        for (Num,(Test,ExceptionInString)) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(ExceptionInString,'Modification Phase 9-' + str(Num) + ' test OK - Dependency on another entity should raise an error')
            else:
                assert False, 'Modification Phase 9-' + str(Num) + ' test FAILURE - Modification of a Dependant record was allowed by the system'
        

        
        # Phase 10
        # Perform modifications in proper order
        Tests = []
        
        Tests.append( """DB.Transitions.Delete((93000000,910021,91000002), ProjectBypassID = 0)""")
        Tests.append( """DB.Params.Delete('TestParamUsingAnotherParam' , ProjectBypassID = 0)""")
        Tests.append( """DB.StudyModels.Delete(93000000 , ProjectBypassID = 0)""")              
        Tests.append( """DB.States.Modify(91000000 , DB.State(ID = 0 , Name = 'TestProcessWillNotBeRetained' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ) , ProjectBypassID = 0)""")
        Tests.append( """DB.States.Delete(910021 , ProjectBypassID = 0)""")
        Tests.append( """DB.States.Delete(91000002 , ProjectBypassID = 0)""")
        Tests.append( """DB.States.Delete(91000003 , ProjectBypassID = 0)""")
        Tests.append( """DB.States.Delete(91000000 , ProjectBypassID = 0)""")
        Tests.append( """DB.Params.Modify('TestParam', DB.Param(Name = 'TestParam', Formula = '0.0123' , ParameterType = 'Expression' , ValidationRuleParams = '[0, 1]', Notes = ''), ProjectBypassID = 0)""")
        Tests.append( """DB.Params.Modify('TestParam', DB.Param(Name = 'TestParamModified', Formula = '0.133' , ParameterType = 'Expression' , ValidationRuleParams = '[0, 1]', Notes = ''), ProjectBypassID = 0)""")
        Tests.append( """DB.Params.Delete('TestParamModified', ProjectBypassID = 0)""")
        Tests.append( """DB.Params.Delete('TestCoefficient', ProjectBypassID = 0)""")
        
        # Run the test
        for (Num,Test) in enumerate(Tests):
            try:
                eval(Test)
            except:
                CheckException(None,'Final Modification Phase 10-' + str(Num) + ' test FAILURE - Dependency on another entity raised an error')
            else:
                print 'Final Modification Phase 10-' + str(Num) + ' test OK - No problems encountered'
        
        



      
class TestSimulationrunInRuntime(GenericSetupAndTearDown):

    def test_SimulationrunInRuntime(self):

        # Test Functions in a simulation
        
        
        # Test Project for using functions correctly
        TestVal = -0.5
        TestEsp = 1e-14
        
        FunctionCheckList =[('TestExp', 'Exp(Test)',0.60653065971263342),
        ('TestLn', '1.0 + Ln(TestExp)',0.5 ),
        ('TestLog10', '1.0 + Log10(TestExp)',0.78285275904837404 ),
        ('TestPow', 'Pow(TestExp,2)',0.36787944117144233),
        ('TestSqrt', 'Sqrt(TestPow)',0.60653065971263342 ),
        ('TestPi', 'Pi() - 2.5',0.64159265358979312 ),
        ('TestMod', 'Mod(TestExp,2)', 0.60653065971263342),
        ('TestAbs', '1.0 - Abs(-Test)', 0.5),
        ('TestFloor', '-Floor(Test)', 1),
        ('TestCeil', 'Ceil(-Test)', 1),
        ('TestMinMax', 'Min(Max(TestExp,TestLog10,TestLn,0.0),1.0)',0.78285275904837404),
        ('TestIsInvalidNumber1', 'IsInvalidNumber(NaN)', 1),
        ('TestIsInvalidNumber2', 'IsInvalidNumber(nan)', 1),
        ('TestIsInfinite', 'IsInfiniteNumber(inf)', 1),
        ('TestIsFiniteNumber', 'IsFiniteNumber(Inf)+0.5', 0.5)]
        
        # Define parameters
        DB.Params.AddNew(DB.Param(Name = 'Test', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        DB.States.AddNew(DB.State(ID = 9910001 , Name = 'TestState1' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
        
        StateIndex = 2
        StatesForProcess = [9910001]
        for Check in FunctionCheckList:
            DB.Params.AddNew(DB.Param(Name = Check[0], Formula = Check[1] , ParameterType = 'Expression' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
            DB.Params.AddNew(DB.Param(Name = Check[0] + 'Res', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
            DB.States.AddNew(DB.State(ID = 9910000 + StateIndex , Name = 'TestState' + str(StateIndex) , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = [] ), ProjectBypassID = 0)
            StatesForProcess = StatesForProcess + [ 9910000 + StateIndex ]
            StateIndex = StateIndex + 1
        
        # Add SubProcess
        DB.States.AddNew(DB.State(ID = 91000000 , Name = 'Test Main Process' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False , IsTerminal = False , ChildStates = StatesForProcess  ), ProjectBypassID = 0)
        
        # Create the model-study definitions
        DB.StudyModels.AddNew(DB.StudyModel( ID = 91000000 , Name = 'Test Example' , Notes = '' , DerivedFrom = 0 , MainProcess = 91000000  ), ProjectBypassID = 0)
        
        StateIndex = 1
        for Check in FunctionCheckList:
            DB.Transitions.AddNew(DB.Transition(StudyModelID = 91000000, FromState = 9910000+StateIndex, ToState = 9910001+StateIndex, Probability = DB.Expr(Check[1])), ProjectBypassID = 0)
            StateIndex = StateIndex + 1
        
        # Populate the table with population sets
        DB.PopulationSets.AddNew(DB.PopulationSet(ID = 9101, Name='Population set for testing functions', Source = 'Internal', Notes = '', DerivedFrom = 0, DataColumns = [('Test','') ,('TestState1','')] , Data = [[ TestVal, 1 ]], Objectives = [] ), ProjectBypassID = 0)
        
        # Define simulation Rules
        SimRuleList = []
        
        # Add all other checks
        for Check in FunctionCheckList:
            print Check
            SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = Check[0]+'Res', SimulationPhase = 1 , OccurrenceProbability = '1' , AppliedFormula = Check[0])]
        
        # Define the projects
        DB.Projects.AddNew(DB.Project(ID = 9101, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 50  , NumberOfRepetitions = 10  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
        
        # Prepare the project for simulation:
        # Test regular case without random seed
        SimulationScriptFullPathOptions = DB.Projects[9101].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest', SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        
        try:
            ResultsInfo = DB.Projects[9101].RunSimulationAndCollectResults(SimulationScriptFullPathOptions, DeleteScriptFileAfterRun = False)
            FinalData = ResultsInfo.ExtractFinalOutcome()
            AllData = ResultsInfo.Data
            ResultsInfo = None
            ResultsInfo = DB.Projects[9101].RunSimulationAndCollectResults(SimulationScriptFullPathOptions, DeleteScriptFileAfterRun = True)
            #FinalData1 = ResultsInfo.ExtractFinalOutcome()
            AllData1 = ResultsInfo.Data
            DataColumnNames = ResultsInfo.DataColumns
            ResultsInfo = None
        except:
            CheckException(None,'Function simulation FAILURE')
        else:
            print 'Function simulation test finished with no exceptions - check file to verify calculations are ok'

            for Check in FunctionCheckList:
                IndexOfIndicator = DataColumnNames.index(Check[0]+'Res')
                assert all(map(lambda Entry: abs(Entry[IndexOfIndicator] - Check[2]) < TestEsp , FinalData)), ' * FAILURE detected in parameter "' + Check[0] + 'Res" in the simulation'
                    
            # It is highly unlikely that the different random seeds will 
            # generate the same results in both simulations
            assert AllData != AllData1, ' * FAILURE detected - different random seeds produce the same results - Try Running the test again to make sure this is not a random occurrence'
        # If reahed this point, all if ok - print a message
        print 'Function simulation OK - tests were successful'
        
                
        
        # check simulation Options
        # Test the case that Random seed factory default is defined (no affect)
        DB.Params.Delete('RandomSeed', ProjectBypassID = 0)
        SimulationScriptFullPath1 = DB.Projects[9101].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest1')
        
        try:
            ResultsInfo = DB.Projects[9101].RunSimulationAndCollectResults(SimulationScriptFullPath1, DeleteScriptFileAfterRun = False)
            AllData = ResultsInfo.Data
            ResultsInfo = None
            ResultsInfo = DB.Projects[9101].RunSimulationAndCollectResults(SimulationScriptFullPath1, DeleteScriptFileAfterRun = True)
            AllData1 = ResultsInfo.Data
            ResultsInfo = None
            
        except:
            CheckException(None,'Default Factory System options FAILURE')

        else:
            # It is highly unlikely that the different random seeds will generate the
            # same results in both simulations
            assert AllData != AllData1, ' * FAILURE detected - Default Factory System options - different random seeds produce the same results - Try Running the test again to make sure this is not a random occurrence'


        # If reahed this point, all if ok - print a message
        print 'Function simulation OK - Factory System Option tests were successful'
        
        
        
        # Test the case that Random seed default is defined with a value to be used
        DB.Params.AddNew(DB.Param(Name = 'RandomSeed', Formula = '0' , ParameterType = 'System Option' , ValidationRuleParams = '', Notes = ''), ProjectBypassID = 0)
        SimulationScriptFullPath2 = DB.Projects[9101].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest2')
        
        try:
            ResultsInfo = DB.Projects[9101].RunSimulationAndCollectResults(SimulationScriptFullPath2, DeleteScriptFileAfterRun = False)
            AllData = ResultsInfo.Data
            ResultsInfo = None
            ResultsInfo = DB.Projects[9101].RunSimulationAndCollectResults(SimulationScriptFullPath2, DeleteScriptFileAfterRun = True)
            AllData1 = ResultsInfo.Data
            ResultsInfo = None
        except:
            CheckException(None, 'Set System Options simulation FAILURE')
            
        else:
            # It is highly unlikely that the different random seeds will 
            # generate the same results in both simulations
            assert AllData == AllData1, ' * FAILURE detected - Set System options - same random seed produced differnt results'

        # If reahed this point, all if ok - print a message
        print 'Function simulation OK - Set System Option tests were successful'
        

        # Test the case that the Random seed is defined in the simulation rules
        # Add a System Option as a simulation option to check such a rule
        try:
            SimRuleList1 =  [ DB.SimulationRule(AffectedParam = 'RandomSeed', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = 'Test')] + SimRuleList
            DB.Projects.AddNew(DB.Project(ID = 9102, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 50  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList1 , DerivedFrom = 0   ) , ProjectBypassID = 0)
            SimulationScriptFullPath3 = DB.Projects[9102].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest3')
        except:
            CheckException('The value does not immediately evaluate to a number', 'Simulation Rule with Option Test OK. An Error should have been detected')
        else:
            assert False, 'Simulation Rule with Option Test FAILURE. An Error should have been detected since a non number is used in the applied formula'
        
        SimRuleList = [ DB.SimulationRule(AffectedParam = 'RandomSeed', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '1')] + SimRuleList
        SimRuleList = [ DB.SimulationRule(AffectedParam = 'VerboseLevel', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '40')] + SimRuleList
        
        DB.Projects.AddNew(DB.Project(ID = 9103, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 50  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
        
        SimulationScriptFullPath3 = DB.Projects[9103].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest3')
        
        try:
            # AllData hold information from SimulationFunctionAndOptionTest2
            # to be compared to this test
            ResultsInfo = DB.Projects[9103].RunSimulationAndCollectResults(SimulationScriptFullPath3)
            AllData1 = ResultsInfo.Data
            ResultsInfo = None    
        except:
            CheckException(None, 'Override System Options simulation FAILURE')
        else:
            # It is highly unlikely that the different random seeds will generate the
            # same results in both simulations
            assert AllData != AllData1, ' * FAILURE detected - Override System Options - a different random seed produced same results results'
        print 'Override System Options OK - System Option tests were successful'
        
        
        
        # Test that adding a system option in the simulation rules twice raises an error
        SimRuleList = [ DB.SimulationRule(AffectedParam = 'RandomSeed', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '1')] + SimRuleList
        try:
            DB.Projects.AddNew(DB.Project(ID = 9104, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 50  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
            DB.Projects[9104].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTestShouldFail')
        except:
            CheckException('More than one Rule in the project uses the System Option', 'Simulation Rule with repeated System Option Test OK. An Error should have been detected')
        else:
            assert False, 'Simulation Rule with repeated System Option Test FAILURE. An Error should have been detected since Defining the random seed twice is not allowed'
     
        
        # Validate that the following causes an error
        
        # Remove The extra RandomSeed and check the RepairPopulation option
        SimRuleList = [ DB.SimulationRule(AffectedParam = 'RepairPopulation', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '0')] + SimRuleList[1:]
        DB.Projects.AddNew(DB.Project(ID = 9105, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 50  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
        
        try:
            SimulationScriptFullPath4 = DB.Projects[9105].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest4')
            ResultsInfo = DB.Projects[9105].RunSimulationAndCollectResults(SimulationScriptFullPath4)
            AllDataNoPopRepair = ResultsInfo.Data
            DataColumnsNoPopRepair = ResultsInfo.DataColumns
            ResultsInfo = None    
        except:
            CheckException(None,'Override population repair system option test FAILURE. The simulation should have passed without an error')
        else:
            Valid = True
            # Check that all states after the first record are always zero
            # Note that _Diagnosed values may be 1 as these are set to actual during
            # initialization. Therefore ignore them when testing state indicators
            for (StateColumnEnum, StateColumnName) in enumerate(DataColumnsNoPopRepair):
                if StateColumnName.startswith('TestState') and not StateColumnName.endswith('_Diagnosed'):
                    for (RecordEnum, Record) in enumerate(AllDataNoPopRepair[1:]):
                        if Record[StateColumnEnum] != 0:
                            Valid = False
                            break
            if Valid:
                print 'Override population repair system option test OK. The simulation should have not set any states since the main process is not set since the population set was not repaired'
            else:        
                assert False, 'Override population repair system option test FAILURE. The simulation should have not set any states since the main process is not set since the population set was not repaired, Detected position is Row:' + str(RecordEnum + 1) + ' Column: ' + str(StateColumnEnum) 
        
        
        # See what happens for the default error level of 2
        # Check if this is still the default and if changed, ask the programmer
        # to fix it
        if DB.DefaultSystemOptions ['ValidateDataInRuntime']!=2:
            raise ValueError, "ASSERTION ERROR: Datadef default has changed. Change the test code to reflect this. Currently the test code assumes ValidateDataInRuntime=2, change the next 4tests to reflect this"
        
        DB.Params.AddNew(DB.Param(Name = 'BadTestParam', Formula = '' , ParameterType = 'Number' , ValidationRuleParams = '[0,0.5]', Notes = ''), ProjectBypassID = 0)
        # this Rule should raise an error at Time = 3
        SimRuleList = SimRuleList[1:3] + [ DB.SimulationRule(AffectedParam = 'BadTestParam', SimulationPhase = 1 , OccurrenceProbability = '' , AppliedFormula = '0.2*Time')] + SimRuleList[3:]
        DB.Projects.AddNew(DB.Project(ID = 9106, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 50  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
        
        try:
            SimulationScriptFullPath5 = DB.Projects[9106].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest5')
            ResultsInfo = DB.Projects[9106].RunSimulationAndCollectResults(SimulationScriptFullPath5)
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            print 'Parameter bound test with default error level of 2 OK. An Error should have been detected. Here is that error:' + str(ExceptValue)
        else:
            print 'Parameter bound test with default error level of 2 FAILURE. An Error should have been detected'
            BeepForError(IncreaseErrorCount=True)
        
        
        # See what happens for other Error levels
        SimRuleList = [ DB.SimulationRule(AffectedParam = 'ValidateDataInRuntime', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '0')] + SimRuleList
        DB.Projects.AddNew(DB.Project(ID = 9107, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 50  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
        
        try:
            SimulationScriptFullPath6 = DB.Projects[9107].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest6')
            ResultsInfo = DB.Projects[9107].RunSimulationAndCollectResults(SimulationScriptFullPath6)
        except:
            CheckException(None,'Override Validation system option and Parameter bound test 0 FAILURE. An Error should have been ignored')
        else:
            print 'Override Validation system option and Parameter bound test 0 OK. An Error should have been detected.'
        
        
        
        # See what happens for other Error levels
        SimRuleList = [ DB.SimulationRule(AffectedParam = 'ValidateDataInRuntime', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '1')]  + SimRuleList[1:]
        DB.Projects.AddNew(DB.Project(ID = 9108, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 50  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
        
        try:
            SimulationScriptFullPath7 = DB.Projects[9108].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest7')
            ResultsInfo = DB.Projects[9108].RunSimulationAndCollectResults(SimulationScriptFullPath7)
        except:
            CheckException('does not fall within the specified validation bounds provided','Override Validation system option and Parameter bound test 1 OK. An Error should have been detected')
        else:
            assert False, 'Override Validation system option and Parameter bound test 1 FAILURE. An Error should have been detected'
        
        
        # See what happens for other Error levels
        SimRuleList = [ DB.SimulationRule(AffectedParam = 'ValidateDataInRuntime', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '3')] + SimRuleList[1:]
        DB.Projects.AddNew(DB.Project(ID = 9109, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 50  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
        try:
            SimulationScriptFullPath8 = DB.Projects[9109].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest8')
            ResultsInfo = DB.Projects[9109].RunSimulationAndCollectResults(SimulationScriptFullPath8)
        except:
            CheckException('does not fall within the specified validation bounds provided','Override Validation system option and Parameter bound test 3 OK. An Error should have been detected')
        else:
            assert False, 'Override Validation system option and Parameter bound test 3 FAILURE. An Error should have been detected'
        
        
        
        # See what happens on screen when recalculation is requested
        SimRuleList = [ DB.SimulationRule(AffectedParam = 'NumberOfErrorsConsideredAsWarningsForSimulation', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '5')] + SimRuleList
        SimRuleList = [ DB.SimulationRule(AffectedParam = 'NumberOfTriesToRecalculateSimulationStep', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '2')] + SimRuleList
        SimRuleList = [ DB.SimulationRule(AffectedParam = 'NumberOfTriesToRecalculateSimulationOfIndividualFromStart', SimulationPhase = 0 , OccurrenceProbability = '' , AppliedFormula = '30')] + SimRuleList
        # The program generate error and report it. However it will show staff
        # on screen as well and which shows functionality.
        # This error should happen after the system retries calculating year 3 
        # for a total of 5 times until halted, while repeating the same
        # individual 3 time out of 30, each time trying year 3 for 2 times.
        
        DB.Projects.AddNew(DB.Project(ID = 9110, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 50  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
        try:
            SimulationScriptFullPath9 = DB.Projects[9110].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest9')
            ResultsInfo = DB.Projects[9110].RunSimulationAndCollectResults(SimulationScriptFullPath9)
        except:
            CheckException('does not fall within the specified validation bounds provided','Validation Warning test 1 OK. Using the system option to regulate errors passed without a fatal error. Look at screen for further details')
        else:    
            assert False, 'Validation Warning test 1 FAILURE. Using the system option to regulate errors should have raised an error' 
        
        
        # Repeat the above simulation for two years to make sure the problem happens
        # only in year 3.
        DB.Projects.AddNew(DB.Project(ID = 9111, Name = 'Test Project' , Notes = 'Testing', PrimaryModelID = 91000000  , PrimaryPopulationSetID = 9101 , NumberOfSimulationSteps = 2  , NumberOfRepetitions = 1  , SimulationRules = SimRuleList , DerivedFrom = 0   ) , ProjectBypassID = 0)
        try:
            SimulationScriptFullPath10 = DB.Projects[9111].CompileSimulation(SimulationScriptFileNamePrefix = 'SimulationFunctionAndOptionTest10')
            ResultsInfo = DB.Projects[9111].RunSimulationAndCollectResults(SimulationScriptFullPath10)
        except:
            CheckException(None,'Validation Warning test 2 FAILURE. Using two simulation steps should not have caused an error')
        else:    
            print 'Validation Warning test 2 OK. Using two years should work fine.'
        


class TestReportOptions(GenericSetupAndTearDown):

    def setUp(self):
        " define default simulation environment"
        # use the full DB setup
        SetupFullDB()

    def test_ReportOptions(self):
        
        # Run again th simulation for Project 1
        RandomSeedToUse=0
        SimulationScriptFullPath1 = DB.Projects[1010].CompileSimulation('SimulationExample1CopyRndSeed'+str(RandomSeedToUse), RandomStateFileNamePrefix = 'SimRandStateEx1CopyRndSeed'+str(RandomSeedToUse), SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None)
        ResultsInfo = DB.Projects[1010].RunSimulationAndCollectResults (SimulationScriptFullPath1, FullResultsOutputFileName = DB.SessionTempDirecory+os.sep+'SimulationResultsExample1CopyRndSeed'+str(RandomSeedToUse)+'.csv', DumpOutputAsCSV=True, FinalResultsOutputFileName = DB.SessionTempDirecory+os.sep+'SimulationResultsExample1CopyRndSeed'+str(RandomSeedToUse)+'FinalData.csv')
    
        # Create some test reports with different levels of details and parameters
        NumberFormatDict={1:[('ColumnNumberFormat', ['%0.14f','%i'])], 4:[('ColumnNumberFormat', ['%g','%i'])],5:[('ColumnNumberFormat', ['%e','%10d'])],'Default':[]}
        ColumnFilterDict={0:[('ColumnFilter',[('Time','No Summary',' '),('<Covariate>','Average Over All Records',''),('<State Indicator,State_Actual>','Auto Detect',''),('Age','Auto Detect',''),('<State Indicator,Sub-Process_Entered>','Sum Over All Records',''),('<State Indicator,State>','Sum Over Demographics',''),('<State Indicator,State>','Auto Detect',''),('<Header>','Auto Detect',''),('<State Indicator,Sub-Process_Entered>','Sum Over All Records',''),('<State Indicator,State>','Sum Over Demographics',''),('<State Indicator,State>','Auto Detect',''),('<Header>','Auto Detect',''),('<Header>','Auto Detect','')])], 1:[('ColumnFilter',[('Time','Auto Detect','Step'),('<Header>','Auto Detect',''),('Age','Sum Over All Records',''),('Age','Average Over All Records',''),('Age','STD Over All Records',''),('Age','Min Over All Records',''),('Age','Max Over All Records',''),('Age','Sum Over Demographics',''),('Age','Average Over Demographics',''),('Age','STD Over Demographics',''),('Age','Min Over Demographics',''),('Age','Max Over Demographics',''),('Age','Sum Over Last Observations Carried Forward',''),('Age','Average Over Last Observations Carried Forward',''),('Age','STD Over Last Observations Carried Forward',''),('Age','Min Over Last Observations Carried Forward',''),('Age','Max Over Last Observations Carried Forward',''),('Age','Record Count',''),('Age','Demographic Count',''),('Age','Last Value Count',''),('Age','Interval Start',''),('Age','Interval End',''),('Age','Interval Length',''),('Age','No Summary','')])],'Default':[]}
        SummationIntervalDict={}
        SummationIntervalDict[0]=[('SummaryIntervals',[0,1,2,[0,3]])]
        SummationIntervalDict[1]=[('SummaryIntervals',[1,2,3]),('StratifyBy','Table([[Alive,[NaN,0,1]],[Age,[0,31,100]]], [[0,1],[2,3]])')]
        SummationIntervalDict['Default']=[]
        DictByVersion = lambda DictName,Key: DictName[DB.Iif(Key in DictName.keys(),Key,'Default' )]
        OutTxt = {}
        for Version in range(8):
            OutTxt[Version] = self.GenReport(ResultsInfo.ID,DB.SessionTempDirecory+os.sep+'SimulationReport1_Ver'+str(Version)+'.txt', [('DetailLevel',Version),('ShowDependency',Version>5),('ShowHidden',Version>6)]+ DictByVersion(SummationIntervalDict,Version) + DictByVersion(NumberFormatDict,Version) + DictByVersion(ColumnFilterDict,Version) )
   




class TestReportMath(GenericSetupAndTearDown):

    def test_ReportMath(self):
        # Test Report Math
    
        
        # First Take example 1 and generate results with a known random seed:
        ResultsInfoCopy = AddProject1005AndRun(0)
        ResultsInfo = AddProject1005AndRun(1)
        
        # Now generate statistics for Report 0 and  Report 1
        
        ReportOptions = [('StratifyBy', 'Table([[Alive,[NaN,0,1]],[Age,[0,31,100]]], [[0,2],[1,3]])'), ('SummaryIntervals',[1,2,3]), ('ColumnNumberFormat', ['%0.14f','%i']), ('ColumnFilter', [('<Header>', 'Auto Detect', ''), ('Alive', 'Auto Detect', ''), ('Dead', 'Auto Detect', ''), ('Age','Sum Over All Records',''),('Age','Average Over All Records',''),('Age','STD Over All Records',''),('Age','Min Over All Records',''),('Age','Max Over All Records',''),('Age','Sum Over Demographics',''),('Age','Average Over Demographics',''),('Age','STD Over Demographics',''),('Age','Min Over Demographics',''),('Age','Max Over Demographics',''),('Age','Sum Over Last Observations Carried Forward',''),('Age','Average Over Last Observations Carried Forward',''),('Age','STD Over Last Observations Carried Forward',''),('Age','Min Over Last Observations Carried Forward',''),('Age','Max Over Last Observations Carried Forward',''),('Age','Record Count',''),('Age','Demographic Count',''),('Age','Last Value Count',''),('Age','Valid Count of All Records',''),('Age','Valid Count of Demographics',''),('Age','Valid Count of Last Observations Carried Forward',''),('Age','Interval Start',''),('Age','Interval End',''),('Age','Interval Length',''),('Age','No Summary','')] )]
        
        MultiRunSimulationStatisticsAsCSV.GenerateMultiRunSimulationStatistics(DB.SessionTempDirecory+os.sep+'Testing_RepRndSeed0.zip',1,ReportOptions)[0]
        MultiRunSimulationStatisticsAsCSV.GenerateMultiRunSimulationStatistics(DB.SessionTempDirecory+os.sep+'Testing_RepRndSeed1.zip',1,ReportOptions)[0]
        ResultsCSV1Mean = MultiRunSimulationStatisticsAsCSV.GenerateMultiRunSimulationStatistics(DB.SessionTempDirecory+os.sep+'Testing_RepRndSeed0.csv',1,ReportOptions)[0]
        ResultsCSV2Mean = MultiRunSimulationStatisticsAsCSV.GenerateMultiRunSimulationStatistics(DB.SessionTempDirecory+os.sep+'Testing_RepRndSeed1.csv',1,ReportOptions)[0]
        CombinedReport = MultiRunCombinedReport.GenerateCombinedReport([DB.SessionTempDirecory+os.sep+'Testing_RepRndSeed0.zip', DB.SessionTempDirecory+os.sep+'Testing_RepRndSeed1.zip'], None, ReportOptions)
        CombinedReportFileName = DB.SessionTempDirecory+os.sep+'SimulationResultsExample1CombinedRandomRndSeeds.txt'
        FileObject = open(CombinedReportFileName,'w')
        FileObject.write(CombinedReport)
        FileObject.close()

        
        def ConstructFromCSV(FileName, Seperator = ','):
            try:
                ImportFile = open(FileName,'rb')
                ReadLines = csv.reader(ImportFile, delimiter = Seperator)
                DataRead = list(ReadLines)
                ImportFile.close()
            except:
                CheckException(None,'Data Import Error: An Error was encountered trying to access the CSV file. Please make sure the file exists and is not blocked for reading by the system or by another program')
            # Analyze the data
            DataPart = DataRead[:]
            # Convert data from strings to numbers
            Data=[]
            for (RowIndex,Row) in enumerate(DataPart):
                # Process the string and convert each item to the appropriate
                # Data type: None, Integer and Float
                ConvertedRow = []
                for (ColumnIndex,DataEntry) in enumerate(Row):
                    if DataEntry.strip() == '':
                        # No data
                        ConvertedDataEntry = None
                    elif DataEntry.lower() in ['inf','infinity','1.#INF']:
                        # Infinity
                        ConvertedDataEntry = DB.Inf
                    elif DataEntry.lower() in ['-inf','-infinity','-1.#INF']:
                        # -Infinity
                        ConvertedDataEntry = -DB.Inf
                    elif DataEntry.lower() in ['nan','-1.#IND']:
                        # Not a Number
                        ConvertedDataEntry = DB.NaN
                    else:
                        # Assumes numeric data types
                        try:
                            # Check if an integer
                            ConvertedDataEntry = int(DataEntry)
                        except:
                            # Not an integer
                            ConvertedDataEntry = None
                        if ConvertedDataEntry == None:
                            # If not an integer, it is a float or an unknown type
                            try:
                                # Check if a float
                                ConvertedDataEntry = float(DataEntry)
                            except:
                                # Not a float - copy the string
                                ConvertedDataEntry = str(DataEntry)
                    ConvertedRow = ConvertedRow + [ConvertedDataEntry]
                Data = Data + [ConvertedRow]
            RetVal = Data
            return RetVal
        
        CombinedReportCSV = ConstructFromCSV(CombinedReportFileName,'|')
        
        
        # Process the results to allow comparison to precalculated results
        
        # First remove the Project, Model, Population set title rows
        ResultsCSV1MeanTitleRemoved = ResultsCSV1Mean[3:]
        ResultsCSV2MeanTitleRemoved = ResultsCSV2Mean[3:]
        
        # Now transpose results
        ResultsCSV1 = map(None,*ResultsCSV1MeanTitleRemoved)
        ResultsCSV2 = map(None,*ResultsCSV2MeanTitleRemoved)
        # Now remove unneeded title rows
        for Enum in [1,2,3] : ResultsCSV1.pop(0)
        for Enum in [1,2,3] : ResultsCSV1.pop(6)
        for Enum in [1,2,3] : ResultsCSV1.pop(12)
        for Enum in [1,2,3] : ResultsCSV1.pop(18)
        for Enum in [1,2,3] : ResultsCSV2.pop(0)
        for Enum in [1,2,3] : ResultsCSV2.pop(6)
        for Enum in [1,2,3] : ResultsCSV2.pop(12)
        for Enum in [1,2,3] : ResultsCSV2.pop(18)
        for Enum in range(13) : CombinedReportCSV.pop(0)
        for Enum in [1,2,3] : CombinedReportCSV.pop(6)
        for Enum in [1,2,3] : CombinedReportCSV.pop(12)
        for Enum in [1,2,3] : CombinedReportCSV.pop(18)
        for Enum in [1,2] : CombinedReportCSV.pop(24)
        
        
        ## The comparison code below is generated from the following script
        #if 1:
        #    print 'RefCSV1 = ' + str(ConstructFromCSV('Temp\Results1_Confirmation.csv')) 
        #    print 'RefCSV2 = ' + str(ConstructFromCSV('Temp\Results2_Confirmation.csv'))
        #    print 'RefCSV1And2 = ' + str(ConstructFromCSV('Temp\ResultsCombined_Confirmation.csv'))
        
        # This code was generated from SQL queries outside the system to reproduce the
        # same reports generated by the system for the results read from the system.
        # The code above was used to import these SQL queries back to the system and 
        # the imported results below can be comapred to the results obtained from the
        # internal report generation above.
        RefCSV1 = [[1, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, None], [2, 2, 58, 58, 0, 58, 1856, 32, 0, 32, 32, 1856, 32, 0, 32, 32, 1856, 32, 0, 32, 32, 58, 58, 58, 58, 58, 58, 2, 2, 1, None], [3, 3, 39, 39, 0, 39, 1287, 33, 0, 33, 33, 1287, 33, 0, 33, 33, 1287, 33, 0, 33, 33, 39, 39, 39, 39, 39, 39, 3, 3, 1, None], [1, 2, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 2, 2, None], [3, 3, 39, 39, 0, 39, 1287, 33, 0, 33, 33, 1287, 33, 0, 33, 33, 1287, 33, 0, 33, 33, 39, 39, 39, 39, 39, 39, 3, 3, 1, None], [1, 3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 3, 3, None], [1, 1, 800, 800, 727, 73, 24800, 31, 0, 31, 31, 24800, 31, 0, 31, 31, 24800, 31, 0, 31, 31, 800, 800, 800, 800, 800, 800, 1, 1, 1, None], [2, 2, 727, 727, 669, 58, 23264, 32, 0, 32, 32, 23264, 32, 0, 32, 32, 25527, 31.90875, 0.288144445594408, 31, 32, 727, 727, 800, 727, 727, 800, 2, 2, 1, None], [3, 3, 669, 669, 630, 39, 22077, 33, 0, 33, 33, 22077, 33, 0, 33, 33, 26196, 32.745, 0.610689099682144, 31, 33, 669, 669, 800, 669, 669, 800, 3, 3, 1, None], [1, 2, 1527, 800, 1396, 131, 48064, 31.4760969220694, 0.499591928927235, 31, 32, 24800, 31, 0, 31, 31, 25527, 31.90875, 0.288144445594408, 31, 32, 1527, 800, 800, 1527, 800, 800, 1, 2, 2, None], [3, 3, 669, 669, 630, 39, 22077, 33, 0, 33, 33, 22077, 33, 0, 33, 33, 26196, 32.745, 0.610689099682144, 31, 33, 669, 669, 800, 669, 669, 800, 3, 3, 1, None], [1, 3, 2196, 800, 2026, 170, 70141, 31.9403460837887, 0.815897101739567, 31, 33, 24800, 31, 0, 31, 31, 26196, 32.745, 0.610689099682144, 31, 33, 2196, 800, 800, 2196, 800, 800, 1, 3, 3, None], [1, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, None], [2, 2, 669, 669, 669, 0, 21408, 32, 0, 32, 32, 21408, 32, 0, 32, 32, 21408, 32, 0, 32, 32, 669, 669, 669, 669, 669, 669, 2, 2, 1, None], [3, 3, 630, 630, 630, 0, 20790, 33, 0, 33, 33, 20790, 33, 0, 33, 33, 22038, 32.9417040358744, 0.234477561070061, 32, 33, 630, 630, 669, 630, 630, 669, 3, 3, 1, None], [1, 2, 669, None, 669, 0, 21408, 32, 0, 32, 32, None, None, None, None, None, 21408, 32, 0, 32, 32, 669, None, 669, 669, None, 669, 1, 2, 2, None], [3, 3, 630, 630, 630, 0, 20790, 33, 0, 33, 33, 20790, 33, 0, 33, 33, 22038, 32.9417040358744, 0.234477561070061, 32, 33, 630, 630, 669, 630, 630, 669, 3, 3, 1, None], [1, 3, 1299, None, 1299, 0, 42198, 32.4849884526559, 0.499967082758358, 32, 33, None, None, None, None, None, 22038, 32.9417040358744, 0.234477561070061, 32, 33, 1299, None, 669, 1299, None, 669, 1, 3, 3, None], [1, 1, 900, 900, 823, 77, 24800, 31, 0, 31, 31, 24800, 31, 0, 31, 31, 27800, 30.8888888888889, 0.314444420424385, 30, 31, 900, 900, 1000, 800, 800, 900, 1, 1, 1, None], [2, 2, 823, 823, 756, 67, 23264, 32, 0, 32, 32, 23264, 32, 0, 32, 32, 28527, 31.6966666666667, 0.65880702510618, 30, 32, 823, 823, 1000, 727, 727, 900, 2, 2, 1, None], [3, 3, 756, 756, 713, 43, 22077, 33, 0, 33, 33, 22077, 33, 0, 33, 33, 29196, 32.44, 1.03753794307235, 30, 33, 756, 756, 1000, 669, 669, 900, 3, 3, 1, None], [1, 2, 1723, 900, 1579, 144, 48064, 31.4760969220694, 0.499591928927235, 31, 32, 24800, 31, 0, 31, 31, 28527, 31.6966666666667, 0.65880702510618, 30, 32, 1723, 900, 1000, 1527, 800, 900, 1, 2, 2, None], [3, 3, 756, 756, 713, 43, 22077, 33, 0, 33, 33, 22077, 33, 0, 33, 33, 29196, 32.44, 1.03753794307235, 30, 33, 756, 756, 1000, 669, 669, 900, 3, 3, 1, None], [1, 3, 2479, 900, 2292, 187, 70141, 31.9403460837887, 0.815897101739567, 31, 33, 24800, 31, 0, 31, 31, 29196, 32.44, 1.03753794307235, 30, 33, 2479, 900, 1000, 2196, 800, 900, 1, 3, 3, None]]
        RefCSV2 = [[1, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, None], [2, 2, 57, 57, 0, 57, 1824, 32, 0, 32, 32, 1824, 32, 0, 32, 32, 1824, 32, 0, 32, 32, 57, 57, 57, 57, 57, 57, 2, 2, 1, None], [3, 3, 50, 50, 0, 50, 1650, 33, 0, 33, 33, 1650, 33, 0, 33, 33, 1650, 33, 0, 33, 33, 50, 50, 50, 50, 50, 50, 3, 3, 1, None], [1, 2, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 2, 2, None], [3, 3, 50, 50, 0, 50, 1650, 33, 0, 33, 33, 1650, 33, 0, 33, 33, 1650, 33, 0, 33, 33, 50, 50, 50, 50, 50, 50, 3, 3, 1, None], [1, 3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 3, 3, None], [1, 1, 800, 800, 743, 57, 24800, 31, 0, 31, 31, 24800, 31, 0, 31, 31, 24800, 31, 0, 31, 31, 800, 800, 800, 800, 800, 800, 1, 1, 1, None], [2, 2, 743, 743, 686, 57, 23776, 32, 0, 32, 32, 23776, 32, 0, 32, 32, 25543, 31.92875, 0.257402909506241, 31, 32, 743, 743, 800, 743, 743, 800, 2, 2, 1, None], [3, 3, 686, 686, 636, 50, 22638, 33, 0, 33, 33, 22638, 33, 0, 33, 33, 26229, 32.78625, 0.557628572197178, 31, 33, 686, 686, 800, 686, 686, 800, 3, 3, 1, None], [1, 2, 1543, 800, 1429, 114, 48576, 31.4815294880104, 0.499820713905975, 31, 32, 24800, 31, 0, 31, 31, 25543, 31.92875, 0.257402909506241, 31, 32, 1543, 800, 800, 1543, 800, 800, 1, 2, 2, None], [3, 3, 686, 686, 636, 50, 22638, 33, 0, 33, 33, 22638, 33, 0, 33, 33, 26229, 32.78625, 0.557628572197178, 31, 33, 686, 686, 800, 686, 686, 800, 3, 3, 1, None], [1, 3, 2229, 800, 2065, 164, 71214, 31.9488559892328, 0.815076073035562, 31, 33, 24800, 31, 0, 31, 31, 26229, 32.78625, 0.557628572197178, 31, 33, 2229, 800, 800, 2229, 800, 800, 1, 3, 3, None], [1, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, None], [2, 2, 686, 686, 686, 0, 21952, 32, 0, 32, 32, 21952, 32, 0, 32, 32, 21952, 32, 0, 32, 32, 686, 686, 686, 686, 686, 686, 2, 2, 1, None], [3, 3, 636, 636, 636, 0, 20988, 33, 0, 33, 33, 20988, 33, 0, 33, 33, 22588, 32.9271137026239, 0.260139449215688, 32, 33, 636, 636, 686, 636, 636, 686, 3, 3, 1, None], [1, 2, 686, None, 686, 0, 21952, 32, 0, 32, 32, None, None, None, None, None, 21952, 32, 0, 32, 32, 686, None, 686, 686, None, 686, 1, 2, 2, None], [3, 3, 636, 636, 636, 0, 20988, 33, 0, 33, 33, 20988, 33, 0, 33, 33, 22588, 32.9271137026239, 0.260139449215688, 32, 33, 636, 636, 686, 636, 636, 686, 3, 3, 1, None], [1, 3, 1322, None, 1322, 0, 42940, 32.4810892586989, 0.499831335267176, 32, 33, None, None, None, None, None, 22588, 32.9271137026239, 0.260139449215688, 32, 33, 1322, None, 686, 1322, None, 686, 1, 3, 3, None], [1, 1, 900, 900, 835, 65, 24800, 31, 0, 31, 31, 24800, 31, 0, 31, 31, 27800, 30.8888888888889, 0.314444420424385, 30, 31, 900, 900, 1000, 800, 800, 900, 1, 1, 1, None], [2, 2, 835, 835, 768, 67, 23776, 32, 0, 32, 32, 23776, 32, 0, 32, 32, 28543, 31.7144444444444, 0.653230376366247, 30, 32, 835, 835, 1000, 743, 743, 900, 2, 2, 1, None], [3, 3, 768, 768, 713, 55, 22638, 33, 0, 33, 33, 22638, 33, 0, 33, 33, 29229, 32.4766666666667, 1.02173814259603, 30, 33, 768, 768, 1000, 686, 686, 900, 3, 3, 1, None], [1, 2, 1735, 900, 1603, 132, 48576, 31.4815294880104, 0.499820713905975, 31, 32, 24800, 31, 0, 31, 31, 28543, 31.7144444444444, 0.653230376366247, 30, 32, 1735, 900, 1000, 1543, 800, 900, 1, 2, 2, None], [3, 3, 768, 768, 713, 55, 22638, 33, 0, 33, 33, 22638, 33, 0, 33, 33, 29229, 32.4766666666667, 1.02173814259603, 30, 33, 768, 768, 1000, 686, 686, 900, 3, 3, 1, None], [1, 3, 2503, 900, 2316, 187, 71214, 31.9488559892328, 0.815076073035562, 31, 33, 24800, 31, 0, 31, 31, 29229, 32.4766666666667, 1.02173814259603, 30, 33, 2503, 900, 1000, 2229, 800, 900, 1, 3, 3, None]]
        RefCSV1And2 = [[1, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, None], [2, 2, 115, 115, 0, 115, 3680, 32, 0, 32, 32, 3680, 32, 0, 32, 32, 3680, 32, 0, 32, 32, 115, 115, 115, 115, 115, 115, 2, 2, 1, None], [3, 3, 89, 89, 0, 89, 2937, 33, 0, 33, 33, 2937, 33, 0, 33, 33, 2937, 33, 0, 33, 33, 89, 89, 89, 89, 89, 89, 3, 3, 1, None], [1, 2, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 2, 2, None], [3, 3, 89, 89, 0, 89, 2937, 33, 0, 33, 33, 2937, 33, 0, 33, 33, 2937, 33, 0, 33, 33, 89, 89, 89, 89, 89, 89, 3, 3, 1, None], [1, 3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 3, 3, None], [1, 1, 1600, 1600, 1470, 130, 49600, 31, 0, 31, 31, 49600, 31, 0, 31, 31, 49600, 31, 0, 31, 31, 1600, 1600, 1600, 1600, 1600, 1600, 1, 1, 1, None], [2, 2, 1470, 1470, 1355, 115, 47040, 32, 0, 32, 32, 47040, 32, 0, 32, 32, 51070, 31.91875, 0.273304083305061, 31, 32, 1470, 1470, 1600, 1470, 1470, 1600, 2, 2, 1, None], [3, 3, 1355, 1355, 1266, 89, 44715, 33, 0, 33, 33, 44715, 33, 0, 33, 33, 52425, 32.765625, 0.584942054933451, 31, 33, 1355, 1355, 1600, 1355, 1355, 1600, 3, 3, 1, None], [1, 2, 3070, 1600, 2825, 245, 96640, 31.4788273615635, 0.499632898309542, 31, 32, 49600, 31, 0, 31, 31, 51070, 31.91875, 0.273304083305061, 31, 32, 3070, 1600, 1600, 3070, 1600, 1600, 1, 2, 2, None], [3, 3, 1355, 1355, 1266, 89, 44715, 33, 0, 33, 33, 44715, 33, 0, 33, 33, 52425, 32.765625, 0.584942054933451, 31, 33, 1355, 1355, 1600, 1355, 1355, 1600, 3, 3, 1, None], [1, 3, 4425, 1600, 4091, 334, 141355, 31.9446327683616, 0.815402560395311, 31, 33, 49600, 31, 0, 31, 31, 52425, 32.765625, 0.584942054933451, 31, 33, 4425, 1600, 1600, 4425, 1600, 1600, 1, 3, 3, None], [1, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, None], [2, 2, 1355, 1355, 1355, 0, 43360, 32, 0, 32, 32, 43360, 32, 0, 32, 32, 43360, 32, 0, 32, 32, 1355, 1355, 1355, 1355, 1355, 1355, 2, 2, 1, None], [3, 3, 1266, 1266, 1266, 0, 41778, 33, 0, 33, 33, 41778, 33, 0, 33, 33, 44626, 32.9343173431734, 0.247818016362217, 32, 33, 1266, 1266, 1355, 1266, 1266, 1355, 3, 3, 1, None], [1, 2, 1355, None, 1355, 0, 43360, 32, 0, 32, 32, None, None, None, None, None, 43360, 32, 0, 32, 32, 1355, None, 1355, 1355, None, 1355, 1, 2, 2, None], [3, 3, 1266, 1266, 1266, 0, 41778, 33, 0, 33, 33, 41778, 33, 0, 33, 33, 44626, 32.9343173431734, 0.247818016362217, 32, 33, 1266, 1266, 1355, 1266, 1266, 1355, 3, 3, 1, None], [1, 3, 2621, None, 2621, 0, 85138, 32.4830217474246, 0.499807011518956, 32, 33, None, None, None, None, None, 44626, 32.9343173431734, 0.247818016362217, 32, 33, 2621, None, 1355, 2621, None, 1355, 1, 3, 3, None], [1, 1, 1800, 1800, 1658, 142, 49600, 31, 0, 31, 31, 49600, 31, 0, 31, 31, 55600, 30.8888888888889, 0.314357014051488, 30, 31, 1800, 1800, 2000, 1600, 1600, 1800, 1, 1, 1, None], [2, 2, 1658, 1658, 1524, 134, 47040, 32, 0, 32, 32, 47040, 32, 0, 32, 32, 57070, 31.7055555555556, 0.655902538739462, 30, 32, 1658, 1658, 2000, 1470, 1470, 1800, 2, 2, 1, None], [3, 3, 1524, 1524, 1426, 98, 44715, 33, 0, 33, 33, 44715, 33, 0, 33, 33, 58425, 32.4583333333333, 1.02954546709507, 30, 33, 1524, 1524, 2000, 1355, 1355, 1800, 3, 3, 1, None], [1, 2, 3458, 1800, 3182, 276, 96640, 31.4788273615635, 0.499632898309542, 31, 32, 49600, 31, 0, 31, 31, 57070, 31.7055555555556, 0.655902538739462, 30, 32, 3458, 1800, 2000, 3070, 1600, 1800, 1, 2, 2, None], [3, 3, 1524, 1524, 1426, 98, 44715, 33, 0, 33, 33, 44715, 33, 0, 33, 33, 58425, 32.4583333333333, 1.02954546709507, 30, 33, 1524, 1524, 2000, 1355, 1355, 1800, 3, 3, 1, None], [1, 3, 4982, 1800, 4608, 374, 141355, 31.9446327683616, 0.815402560395311, 31, 33, 49600, 31, 0, 31, 31, 58425, 32.4583333333333, 1.02954546709507, 30, 33, 4982, 1800, 2000, 4425, 1600, 1800, 1, 3, 3, None]]
       
        # now do the comparison
        
        def CompareReportResult (Internal, External, RowEnum, ColEnum , Tolerance = 1e-10):
            " comapre Internal report results to extranal imported results "
            # This function will perform the comparison that will compare none values
            # to 0 and will allow numerical error up to tolerance in calculation
            InternalValue = Internal[RowEnum][ColEnum]
            ExternalValue = External[RowEnum][ColEnum]
            if InternalValue == None:
                InternalValue = 0
            if ExternalValue == None:
                ExternalValue = 0
            IsComparisonOK = abs (InternalValue - ExternalValue) < Tolerance 
            if not IsComparisonOK:
                print 'Wrong calculation : ' + str(InternalValue) + ' != ' + str(ExternalValue) + ' at (row,col) = ' + str((RowEnum, ColEnum))
            return IsComparisonOK
        
        NumberOfComparisonOutliers = 0
        NumberOfRows = len (ResultsCSV1) 
        # the repetition count in the last column is ignored
        NumberOfColumns = len (ResultsCSV1[0]) - 1
        if NumberOfRows != len(RefCSV1) or NumberOfColumns != len(RefCSV1[0]):
            assert False, 'Report mathematics test 1 FAILURE. The report has more columns than expected'
        else:
            for RowEnum in range(NumberOfRows):
                for ColEnum in range(NumberOfColumns):
                    if not CompareReportResult(ResultsCSV1, RefCSV1, RowEnum, ColEnum):
                        NumberOfComparisonOutliers = NumberOfComparisonOutliers + 1
            if NumberOfComparisonOutliers == 0:
                print 'Report mathematics test 1 OK. The internal and external results for report 1 were compared well.'
            else:
                assert False, 'Report mathematics test 1 FAILURE. The internal and external results for report 1 did not match in ' + str(NumberOfComparisonOutliers) + ' locations'
        
        
        NumberOfComparisonOutliers = 0
        NumberOfRows = len (ResultsCSV2)
        # the repetition count in the last column is ignored
        NumberOfColumns = len (ResultsCSV2[0]) - 1
        if NumberOfRows != len(RefCSV2) or NumberOfColumns != len(RefCSV2[0]):
            assert False, 'Report mathematics test 2 FAILURE. The report has more columns than expected'
        else:
            for RowEnum in range(NumberOfRows):
                for ColEnum in range(NumberOfColumns):
                    if not CompareReportResult(ResultsCSV2, RefCSV2, RowEnum, ColEnum):
                        NumberOfComparisonOutliers = NumberOfComparisonOutliers + 1
            if NumberOfComparisonOutliers == 0:
                print 'Report mathematics test 2 OK. The internal and external results for report 2 were compared well.'
            else:
                assert False, 'Report mathematics test 2 FAILURE. The internal and external results for report 2 did not match in ' + str(NumberOfComparisonOutliers) + ' locations'
        
        
        NumberOfComparisonOutliers = 0
        NumberOfRows = len (CombinedReportCSV)
        # the repetition count in the last column is ignored
        NumberOfColumns = len (CombinedReportCSV[0]) - 1
        if NumberOfRows != len(RefCSV1And2) or NumberOfColumns != len(RefCSV1And2[0]):
            assert False, 'Report mathematics test 3 FAILURE. The report has more columns than expected'
        else:
            for RowEnum in range(NumberOfRows):
                for ColEnum in range(NumberOfColumns):
                    if not CompareReportResult(CombinedReportCSV, RefCSV1And2, RowEnum, ColEnum):
                        NumberOfComparisonOutliers = NumberOfComparisonOutliers + 1
            if NumberOfComparisonOutliers == 0:
                print 'Report mathematics test 3 OK. The internal and external results for the combined report were compared well.'
            else:
                assert False, 'Report mathematics test 3 FAILURE. The internal and external results for the combined report did not match in ' + str(NumberOfComparisonOutliers) + ' locations'
        

        AddProject1006()
        
        # Run the example again
        # Overrides are the population = 1005, Model = 1000000, RandomSeed = 1, AgeIncCoef =1
        # these should make the simulation equivalent to the second Run
        MultiRunSimulation.RunMultipleSimulations(InputFileName = DB.SessionTempDirecory+os.sep+'Testing_MultiRunOverride.zip', ProjectIndex = [1006], NumberOfRepeats = 1, StartRunningIndexStr = 0, OverWriteFiles = True, ReconstructFromTraceback = False, NumberOfSimulationStepsOverride = 3, PopulationRepetitionsOverride = 100, ModelOverride = [1000000], PopulationSetOverride = [1005], InitializeCoefficientValues = [0,1])
            
        # Load the results file
        DB.LoadAllData(DB.SessionTempDirecory+os.sep+'Testing_MultiRunOverride_0.zip')
        # The results should have the index 1
        ResultsInfo = DB.SimulationResults[1]
        
        NewColumns = ResultsInfo.DataColumns[:]
        TransposedData = map(None,*ResultsInfo.Data)
        
        # remove the columns associated with the newly added Initialization rules
        for ParamName in ['RandomSeed','AgeIncCoef']:
            IndexToRemove = NewColumns.index(ParamName)
            NewColumns.pop(IndexToRemove)
            TransposedData.pop(IndexToRemove)
        FilteredData = map(None,*TransposedData)
        
        
        NumberOfColumns = len (ResultsInfoCopy.DataColumns)
        NumberOfRows = len(ResultsInfoCopy.Data)
        if NumberOfRows != len(FilteredData) or NumberOfColumns != len(NewColumns):
            assert False, 'Multi Run Simulation Override test FAILURE. More columns than expected'
        else:
            for RowEnum in range(NumberOfRows):
                for ColEnum in range(NumberOfColumns):
                    if not(DB.IsNaN(ResultsInfoCopy.Data[RowEnum][ColEnum]) and DB.IsNaN(FilteredData[RowEnum][ColEnum]) or (ResultsInfoCopy.Data[RowEnum][ColEnum] == FilteredData[RowEnum][ColEnum])):
                        print ' - Mismatch in location ' + str((RowEnum,ColEnum)) + ' values are: ' + str((ResultsInfoCopy.Data[RowEnum][ColEnum] , FilteredData[RowEnum][ColEnum]))
                        NumberOfComparisonOutliers = NumberOfComparisonOutliers + 1
            if NumberOfComparisonOutliers == 0:
                print 'Multi Run Simulation Override test OK. The numbers match between override and original simulation results.'
            else:
                assert False, 'Multi Run Simulation Override test FAILURE. The numbers do not match between override and original simulation results. Number of mismatches is ' + str(NumberOfComparisonOutliers) 



 
    
class TestSupportingScriptsAndReproducibilty(GenericSetupAndTearDown):
    
    def setUp(self):
        " define default simulation environment"
        # use the full DB setup
        SetupFullDB()
        # Save the database in the temp directory for simulation
        DB.SaveAllData(FileName = DB.SessionTempDirecory + os.sep + 'Testing.zip', Overwrite = True)
        DB.SaveAllData(FileName = DB.SessionTempDirecory + os.sep + 'TestingForRulesAndPopOverride.zip', Overwrite = True)
        

    # Test the supporting scripts as if from command line
    def RunExternalScript (self, CommandLine, OutputfilePrefix = 'OutScript'):
        """ runs the external script """
        (StdOutData, StdErrData) = ('','')
        try:
            print '#'*70
            print 'Running the Command: '
            ActualCommand = '"'+sys.executable + '" ' + CommandLine
            print ActualCommand
            TheSubProcess = subprocess.Popen( ActualCommand, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
            (StdOutData, StdErrData) = TheSubProcess.communicate()
            ReturnCode = TheSubProcess.returncode
            #The older code used the following command
            #ReturnCode = subprocess.call(ActualCommand, shell = True)
        except OSError:
            # if an error was caught return None
            ReturnCode = None
        print 'Standard Output After Run was:'
        print StdOutData
        print 'Standard Error After Run was:'
        print StdErrData
        print '#'*70
        # Note that a ReturnCode smaller than 0 means the program was killed
        return (ReturnCode, StdOutData, StdErrData)

    def FileExistsAndIsRecent(self, FileName, StartTime):
        """ returns True if the file exists and is recent """
        try:
            FileTimeRaw = os.path.getmtime(FileName)
            FileTime = datetime.datetime.fromtimestamp(FileTimeRaw)
        except:
            print 'file not Found'
            RetVal = False
        else:
            RetVal = FileTime >= StartTime
        return RetVal        


    def test_Reproducibility_Combined(self):
        # test Reproducibility of simulation when simualtion and population 
        # generation are combined
        # First run mutiple simuations that uses popuation distributios
        # Before starting record the time  
        StartTime = datetime.datetime.now()
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunSimulation.py ' + DB.SessionTempDirecory + os.sep + 'Testing.zip 21 2 98000 Y None None None None')
        if ReturnCode != 0:
            assert False, ('Reproducibility Combined test A-0 FAILURE. Script returned bad exit code')
        else:
            print ('Reproducibility Combined test A-0 OK.')
        # test that the file Temp\\testing_98001.zip is recent
        for Repetition in range(2):
            if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_9800' + str(Repetition) + '.zip', StartTime):
                assert False, ('Reproducibility Combined test A-'+ str(Repetition+1) +' FAILURE. No recent Output file created')
            else:
                print ('Reproducibility Combined test A-'+ str(Repetition+1) +' OK.')
            
        TheOrinigalStoredResults = []
        # Record the simulation results
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunExportResultsAsCSV.py ' + '"'+DB.SessionTempDirecory + os.sep + 'Testing_9800?.zip" 1') 
        if ReturnCode != 0:
            assert False, ('Reproducibility Combined test B-0 FAILURE. Script returned bad exit code')
        else:
            print ('Reproducibility Combined test B-0 OK.')
        # test that the file Temp\\Testing_98001.csv is recent
        for Repetition in range(2):
            if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_9800' + str(Repetition) + 'Results.csv', StartTime):
                assert False, ('Reproducibility Combined test B-'+ str(Repetition+1) +' FAILURE. No recent Output file created')
            else:
                # Record the results for latr comparison
                ResFile = open (DB.SessionTempDirecory + os.sep + 'Testing_9800' + str(Repetition) + 'Results.csv' , 'r')
                TheResults = ResFile.read()
                ResFile.close()
                TheOrinigalStoredResults.append(TheResults) 
                
                for FileEnding in ['.zip','Results.csv']:
                    # Now rename the data file to avoid conflict
                    Src = DB.SessionTempDirecory + os.sep + 'Testing_9800' + str(Repetition) + FileEnding
                    Dst = DB.SessionTempDirecory + os.sep + 'Testing_9800' + str(Repetition) + 'OriginalBackup' + FileEnding
                    try:
                        # make sure no other file in DST from previous runs
                        os.remove(Dst)
                    except:
                        # if error - ignore - this means its the first run
                        pass
                    os.rename(Src, Dst)
                    # Now rename the results file to avoid conflict
                    if self.FileExistsAndIsRecent (Src, StartTime):
                        assert False, ('Reproducibility Combined test B-'+ str(Repetition+1) +' FAILURE. Could not rename original file with ending ' + FileEnding)
                #if you reached this point without error give an OK
                print ('Reproducibility Combined test B-'+ str(Repetition+1) +' OK.')

        # Before starting record the time  - just as a precaution
        StartTime = datetime.datetime.now()
        # Now repeat the last two phases - this time by reproducing the results        


        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunSimulation.py ' + DB.SessionTempDirecory + os.sep + 'Testing.zip 21 2 98000 R None None None None')
        if ReturnCode != 0:
            assert False, ('Reproducibility Combined test C-0 FAILURE. Script returned bad exit code')
        else:
            print ('Reproducibility Combined test C OK.')
        # test that the file Temp\\testing_98001.zip is recent
        for Repetition in range(2):
            if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_9800' + str(Repetition) + '.zip', StartTime):
                assert False, ('Reproducibility Combined test C-'+ str(Repetition+1) +' FAILURE. No recent Output file created')
            else:
                print ('Reproducibility Combined test C-'+ str(Repetition+1) +' OK.')
            
        TheRecontructedStoredResults = []
        # Record the simulation results
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunExportResultsAsCSV.py ' + '"'+DB.SessionTempDirecory + os.sep + 'Testing_9800?.zip" 1') 
        if ReturnCode != 0:
            assert False, ('Reproducibility Combined test D-0 FAILURE. Script returned bad exit code')
        else:
            print ('Reproducibility Combined test D-0 OK.')
        # test that the file Temp\\Testing_98001.csv is recent
        for Repetition in range(2):
            if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_9800' + str(Repetition) + 'Results.csv', StartTime):
                assert False, ('Reproducibility Combined test D-'+ str(Repetition+1) +' FAILURE. No recent Output file created')
            else:
                # Record the results for latr comparison
                ResFile = open (DB.SessionTempDirecory + os.sep + 'Testing_9800' + str(Repetition) + 'Results.csv' , 'r')
                TheResults = ResFile.read()
                ResFile.close()
                TheRecontructedStoredResults.append(TheResults) 
                print ('Reproducibility Combined test D-'+ str(Repetition+1) +' OK.')
                
        # Finally - make sure that resuts are the same
        if TheRecontructedStoredResults == TheOrinigalStoredResults:
            print ('Reproducibility Combined test E OK. Results Match between original simulation results and reproduced simulation results')
        else:
            assert False, 'Reproducibility Combined test E FAILURE. Results Mismatch between original simulation results and reproduced simulation results'


    def test_Reproducibility_Seperate(self):
        # test Reproducibility of simulation when simualtion and population 
        # generation are seperated 
        # First run mutiple simuations that uses popuation distributios
        # Before starting record the time  
        StartTime = datetime.datetime.now()
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunSimulation.py ' + DB.SessionTempDirecory + os.sep + 'Testing.zip 21 2 Pop9800 Y 0 None None None')
        if ReturnCode != 0:
            assert False, ('Reproducibility Seperate test A-0 FAILURE. Script returned bad exit code')
        else:
            print ('Reproducibility Seperate test A-0 OK.')
        # test that the file Temp\\Testing_Pop98000_?.zip is recent
        for Repetition in range(2):
            if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_' + str(Repetition) + '.zip', StartTime):
                assert False, ('Reproducibility Seperate test A-'+ str(Repetition+1) +' FAILURE. No recent Output file created')
            else:
                print ('Reproducibility Seperate test A-'+ str(Repetition+1) +' OK.')

        # Now Run the simulations manually starting from the generated 
        # population. Note that -1 indicates last population and 1 indicated
        # that the population will be used once - otherwise there may be
        # square number of repetition due to population size generated.
        for Repetition in range(2):
            (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunSimulation.py ' + DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_'+str(Repetition)+'.zip 21 2 0 Y None 1 None -1')
            if ReturnCode != 0:
                assert False, ('Reproducibility Seperate test A-'+ str(Repetition+3) +' FAILURE. No recent Output file created')
            else:
                print ('Reproducibility Seperate test A-'+ str(Repetition+3) +' OK.')


        TheOrinigalStoredResults = []
        # Record the simulation results
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunExportResultsAsCSV.py ' + '"'+DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_?_0.zip" 1') 
        if ReturnCode != 0:
            assert False, ('Reproducibility Seperate test B-0 FAILURE. Script returned bad exit code')
        else:
            print ('Reproducibility Seperate test B-0 OK.')
        # test that the file Temp\\Testing_98001.csv is recent
        for Repetition in range(2):
            if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_' + str(Repetition) + '_0Results.csv', StartTime):
                assert False, ('Reproducibility Seperate test B-'+ str(Repetition+1) +' FAILURE. No recent Output file created')
            else:
                # Record the results for latr comparison
                ResFile = open (DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_' + str(Repetition) + '_0Results.csv' , 'r')
                TheResults = ResFile.read()
                ResFile.close()
                TheOrinigalStoredResults.append(TheResults) 
                
                for FileEnding in ['_0.zip','_0Results.csv']:
                    # Now rename the data file to avoid conflict
                    Src = DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_' + str(Repetition) + FileEnding
                    Dst = DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_' + str(Repetition) + 'OriginalBackup' + FileEnding
                    try:
                        # make sure no other file in DST from previous runs
                        os.remove(Dst)
                    except:
                        # if error - ignore - this means its the first run
                        pass
                    os.rename(Src, Dst)
                    # Now rename the results file to avoid conflict
                    if self.FileExistsAndIsRecent (Src, StartTime):
                        assert False, ('Reproducibility Seperate test B-'+ str(Repetition+1) +' FAILURE. Could not rename original file with ending ' + FileEnding)
                #if you reached this point without error give an OK
                print ('Reproducibility Seperate test B-'+ str(Repetition+1) +' OK.')

        # Before starting record the time  - just as a precaution
        StartTime = datetime.datetime.now()
        # Now repeat the last two phases - this time by reproducing the results        

        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunSimulation.py ' + DB.SessionTempDirecory + os.sep + 'Testing.zip 21 2 Pop9800 R 0 None None None')
        if ReturnCode != 0:
            assert False, ('Reproducibility Seperate test C-0 FAILURE. Script returned bad exit code')
        else:
            print ('Reproducibility Seperate test C OK.')
        # test that the file Temp\\Testing_Pop98000_?.zip is recent
        for Repetition in range(2):
            if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_' + str(Repetition) + '.zip', StartTime):
                assert False, ('Reproducibility Seperate test C-'+ str(Repetition+1) +' FAILURE. No recent Output file created')
            else:
                print ('Reproducibility Seperate test C-'+ str(Repetition+1) +' OK.')

        # Now Run the simulations manually starting from the generated 
        # population. Note that -1 indicates last population and 1 indicated
        # that the population will be used once - otherwise there may be
        # square number of repetition due to population size generated.
        for Repetition in range(2):
            (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunSimulation.py ' + DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_'+str(Repetition)+'.zip 21 2 0 R None 1 None -1')
            if ReturnCode != 0:
                assert False, ('Reproducibility Seperate test C-'+ str(Repetition+3) +' FAILURE. No recent Output file created')
            else:
                print ('Reproducibility Seperate test C-'+ str(Repetition+3) +' OK.')

        
        TheRecontructedStoredResults = []
        # Record the simulation results
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunExportResultsAsCSV.py ' + '"'+DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_?_0.zip" 1') 
        if ReturnCode != 0:
            assert False, ('Reproducibility Seperate test D-0 FAILURE. Script returned bad exit code')
        else:
            print ('Reproducibility Seperate test D-0 OK.')
        # test that the file Temp\\Testing_98001.csv is recent
        for Repetition in range(2):
            if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_' + str(Repetition) + '_0Results.csv', StartTime):
                assert False, ('Reproducibility Seperate test D-'+ str(Repetition+1) +' FAILURE. No recent Output file created')
            else:
                # Record the results for latr comparison
                ResFile = open (DB.SessionTempDirecory + os.sep + 'Testing_Pop9800_' + str(Repetition) + '_0Results.csv' , 'r')
                TheResults = ResFile.read()
                ResFile.close()
                TheRecontructedStoredResults.append(TheResults) 
                print ('Reproducibility Seperate test D-'+ str(Repetition+1) +' OK.')
                
        # Finally - make sure that resuts are the same
        if TheRecontructedStoredResults == TheOrinigalStoredResults:
            print ('Reproducibility Seperate test E OK. Results Match between original simulation results and reproduced simulation results')
        else:
            assert False, 'Reproducibility Seperate test E FAILURE. Results Mismatch between original simulation results and reproduced simulation results'

       

    def test_SupportingScripts(self):
        
        # first make sure that the modules were imported
        assert MultiRunSimulation != None, 'Module MultiRunSimulation missing'
        assert MultiRunSimulationStatisticsAsCSV != None, 'Module MultiRunSimulationStatisticsAsCSV missing'
        assert MultiRunCombinedReport != None, 'Module MultiRunCombinedReport missing'
        assert MultiRunExportResultsAsCSV != None, 'Module MultiRunExportResultsAsCSV missing'
        assert ConvertDataToCode != None, 'Module ConvertDataToCode missing'
        assert CreatePlotsFromCSV != None, 'Module CreatePlotsFromCSV missing'
        assert AssembleReportCSV != None, 'Module AssembleReportCSV missing'
    
        # Before starting record the time  
        StartTime = datetime.datetime.now()
    
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunSimulation.py ' + DB.SessionTempDirecory + os.sep + 'Testing.zip 20 2 94000')
        if ReturnCode != 0:
            assert False, ('Supporting Script test A-0 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test A-0 OK.')
        # test that the file Temp\\testing_94001.zip is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_94001.zip', StartTime):
            assert False, ('Supporting Script test A-1 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test A-1 OK.')
    
    
        # Before starting record the time  
        StartTime = datetime.datetime.now()
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunSimulation.py ' + DB.SessionTempDirecory + os.sep + 'Testing.zip 0 2 95000 Y None None None None')
        if ReturnCode != 0:
            assert False, ('Supporting Script test B-0 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test B-0 OK.')
        # test that the file Temp\\testing_95001.zip is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_95001.zip', StartTime):
            assert False, ('Supporting Script test B-1 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test B-1 OK.')

        # Make sure Project 1006 exists with the file Testing_MultiRunOverride
        AddProject1006()
    
        # Project 1006 tests the command line interface for overrides
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunSimulation.py ' + DB.SessionTempDirecory+os.sep+'Testing_MultiRunOverride.zip [1006] 1 0 Y 3 100 [1000000] [1005] 0 1')
        if ReturnCode != 0:
            assert False, ('Supporting Script test B-2 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test B-2 OK.')
        # test that the file Temp\\Testing_MultiRunOverride_0.zip is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_MultiRunOverride_0.zip', StartTime):
            assert False, ('Supporting Script test B-3 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test B-3 OK.')
        
    
        # this script report will test many options within the report system:
        # Stratification, time intervals, etc. It tests that the code does not 
        # raise an error, accuracy of the report can be performed outside by 
        # loading the CSV files containing the simulation results in test C
        MockFile = open(DB.SessionTempDirecory + os.sep + 'TestColumnFilter.txt','w')
        MockFile.write('StratifyBy\n')
        MockFile.write('"Table([[Alive,[NaN,0,1]],[Age,[0,31,100]]], [[0,2],[1,3]])"\n')
        MockFile.write('SummaryIntervals\n')
        MockFile.write('[[0,0],1,2,3]\n')
        MockFile.write('ColumnFilter\n')
        MockFile.write("[('<Header>', 'Auto Detect', ''), ('Alive', 'Auto Detect', ''), ('Dead', 'Auto Detect', ''), ('Age','Sum Over All Records',''),('Age','Average Over All Records',''),('Age','STD Over All Records',''),('Age','Min Over All Records',''),('Age','Max Over All Records',''),('Age','Sum Over Demographics',''),('Age','Average Over Demographics',''),('Age','STD Over Demographics',''),('Age','Min Over Demographics',''),('Age','Max Over Demographics',''),('Age','Sum Over Last Observations Carried Forward',''),('Age','Average Over Last Observations Carried Forward',''),('Age','STD Over Last Observations Carried Forward',''),('Age','Min Over Last Observations Carried Forward',''),('Age','Max Over Last Observations Carried Forward',''),('Age','Record Count',''),('Age','Demographic Count',''),('Age','Last Value Count',''),('Age','Interval Start',''),('Age','Interval End',''),('Age','Interval Length',''),('Age','No Summary','')]\n")
        MockFile.close()
           
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunSimulationStatisticsAsCSV.py ' + '"'+DB.SessionTempDirecory + os.sep + 'Testing_9500?.zip" 1 ' + DB.SessionTempDirecory + os.sep + 'TestColumnFilter.txt')
        if ReturnCode != 0:
            assert False, ('Supporting Script test C-0 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test C-0 OK.')
    
        # test that the file Temp\\Testing_9500Median.csv is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_9500Median.csv', StartTime):
            assert False, ('Supporting Script test C-1 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test C-1 OK.')
    
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunExportResultsAsCSV.py ' + '"'+DB.SessionTempDirecory + os.sep + 'Testing_9500?.zip" 1 IndividualID Repetition Time Age Alive Dead ') 
        if ReturnCode != 0:
            assert False, ('Supporting Script test D-0 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test D-0 OK.')
        # test that the file Temp\\Testing_95001.csv is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Testing_95001.csv', StartTime):
            assert False, ('Supporting Script test D-1 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test D-1 OK.')
            # also load the file for later comparison

    
        # This script will test the combined report code does not raise an error. 
        # Accuracy of the report can be determined extranally by loading the report 
        # and comparing it to the analysis of the CSV files containing the
        # simulation results from test C
        MockFile = open(DB.SessionTempDirecory + os.sep + 'Mockstdin.txt','w')
        MockFile.write(DB.SessionTempDirecory + os.sep + 'Testing_95000.zip\n')
        MockFile.write(DB.SessionTempDirecory + os.sep + 'Testing_95001.zip\n')
        MockFile.write('\n')
        MockFile.write('\n')
        MockFile.write('StratifyBy\n')
        MockFile.write('"Table([[Alive,[NaN,0,1]],[Age,[0,31,100]]], [[0,2],[1,3]])"\n')
        MockFile.write('DetailLevel\n')
        MockFile.write('0\n')
        MockFile.write('SummaryIntervals\n')
        MockFile.write('[1,2,3]\n')
        MockFile.write('ColumnNumberFormat\n')
        MockFile.write("['%0.14f','%i']\n")
        MockFile.write('ColumnFilter\n')
        MockFile.write("[('<Header>', 'Auto Detect', ''), ('Alive', 'Auto Detect', ''), ('Dead', 'Auto Detect', ''), ('Age','Sum Over All Records',''),('Age','Average Over All Records',''),('Age','STD Over All Records',''),('Age','Min Over All Records',''),('Age','Max Over All Records',''),('Age','Sum Over Demographics',''),('Age','Average Over Demographics',''),('Age','STD Over Demographics',''),('Age','Min Over Demographics',''),('Age','Max Over Demographics',''),('Age','Sum Over Last Observations Carried Forward',''),('Age','Average Over Last Observations Carried Forward',''),('Age','STD Over Last Observations Carried Forward',''),('Age','Min Over Last Observations Carried Forward',''),('Age','Max Over Last Observations Carried Forward',''),('Age','Record Count',''),('Age','Demographic Count',''),('Age','Last Value Count',''),('Age','Interval Start',''),('Age','Interval End',''),('Age','Interval Length',''),('Age','No Summary','')]\n")
        MockFile.write('\n')
        MockFile.write(DB.SessionTempDirecory + os.sep + 'Report1.txt\n')
        MockFile.close()
    
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('MultiRunCombinedReport.py ' + DB.SessionTempDirecory + os.sep + 'Mockstdin.txt')
        if ReturnCode != 0:
            assert False, ('Supporting Script test E-0 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test E-0 OK.')
        # test that Report1 is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Report1.txt', StartTime):
            assert False, ('Supporting Script test E-1 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test E-1 OK.')
            
    
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('ConvertDataToCode.py ' + DB.SessionTempDirecory + os.sep + 'Testing_95001.zip ' + DB.SessionTempDirecory + os.sep + 'Reconstructtesting_95001.py 0 y')
        if ReturnCode != 0:
            assert False, ('Supporting Script test F-0 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test F-0 OK.')
        # test that Reconstructtesting__95001.py is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'Reconstructtesting_95001.py', StartTime):
            assert False, ('Supporting Script test F-1 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test F-1 OK.')


    
        # test that The report Assembly routine works ok
        AssemblySequenceString = "[ ('" + DB.SessionTempDirecory + os.sep + "Testing_9500Median.csv' , '' ,'', '', 'Title') , ('" + DB.SessionTempDirecory + os.sep + "Testing_9500Median.csv' , 'Start Step', 'End Step', '', 'Title'), ('" + DB.SessionTempDirecory + os.sep + "Testing_9500Median.csv' , '0', '0', 'Stratification - None:', 'Initial'), ('" + DB.SessionTempDirecory + os.sep + "Testing_95000.csv' , '1', '1', '', 'Year 1 File 0'), ('" + DB.SessionTempDirecory + os.sep + "Testing_95000.csv' , '0', '0', '', 'File 0'), ('" + DB.SessionTempDirecory + os.sep + "Testing_95000.csv' , '1', '1', '', 'File 0'), ('" + DB.SessionTempDirecory + os.sep + "Testing_95000.csv' , '2', '2', '', 'File 0'), ('" + DB.SessionTempDirecory + os.sep + "Testing_95000.csv' , '3', '3', '', 'File 0'), ('" + DB.SessionTempDirecory + os.sep + "Testing_95001.csv' , '0', '0', '', 'File 1'), ('" + DB.SessionTempDirecory + os.sep + "Testing_95001.csv' , '1', '1', '', 'File 1'), ('" + DB.SessionTempDirecory + os.sep + "Testing_95001.csv' , '2', '2', '', 'File 1'), ('" + DB.SessionTempDirecory + os.sep + "Testing_95001.csv' , '3', '3', '', 'File 1')  ]"
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('AssembleReportCSV.py "'+ AssemblySequenceString +'" '+ DB.SessionTempDirecory + os.sep + 'SelectedAssembledColumns.csv')
        if ReturnCode != 0:
            assert False, ('Supporting Script test G-0 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test G-0 OK.')
    
    
        # test that the file Temp\\SelectedAssembledColumns.txt is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'SelectedAssembledColumns.csv', StartTime):
            assert False, ('Supporting Script test G-1 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test G-1 OK.')
    
        # Make sure no errors were in the file
        TheFile = open(DB.SessionTempDirecory + os.sep + 'SelectedAssembledColumns.csv')
        TheText = TheFile.read()
        TheFile.close()
        if 'Err' in TheText:
            assert False, ('Supporting Script test G-2 FAILURE. Error detected in assembly')
        else:
            print ('Supporting Script test G-2 OK.')
    
        # Create a file with the assembly sequence
        MockFile = open(DB.SessionTempDirecory + os.sep + 'TestAssembleReportCSV.txt','w')
        MockFile.write(AssemblySequenceString)
        MockFile.close()
    
        # test that The report Assembly routine works ok via file
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('AssembleReportCSV.py ' + DB.SessionTempDirecory + os.sep + 'TestAssembleReportCSV.txt ' + DB.SessionTempDirecory + os.sep + 'SelectedAssembledColumns1.csv')
        if ReturnCode != 0:
            assert False, ('Supporting Script test G-3 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test G-3 OK.')
    
    
        # test that the file Temp\\SelectedAssembledColumns.txt is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'SelectedAssembledColumns1.csv', StartTime):
            assert False, ('Supporting Script test G-4 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test G-4 OK.')
    
        # Make sure no errors were in the file
        TheFile = open(DB.SessionTempDirecory + os.sep + 'SelectedAssembledColumns1.csv')
        TheText = TheFile.read()
        TheFile.close()
        if 'Err' in TheText:
            assert False, ('Supporting Script test G-5 FAILURE. Error detected in assembly')
        else:
            print ('Supporting Script test G-5 OK.')

        # Start optional tests for plot system        
    
        # test that The plot routine works ok
        GraphSequenceString = " [ ('','Start Step','Time'), ('Age','Avg All',''), ('Alive','Avg All',''), ('','Rec Count',''), [('Age','Avg All',''), ('Alive','Avg All',''), ('','Rec Count','nested record count')], ('AnError','Avg All',''), ('Alive','AlsoAnError','')  ], ['File 1', 'File 2'] , ['ko-','k:','rx-','r:']"
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('CreatePlotsFromCSV.py ' + DB.SessionTempDirecory + os.sep + 'SelectedAssembledColumns.csv '+ DB.SessionTempDirecory + os.sep + 'SelectedAssembledPlots.pdf "'+ GraphSequenceString +'"' )
        if ReturnCode != 0:
            assert False, ('Supporting Script test Opt-H-0 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test Opt-H-0 OK.')
    
    
        # test that the file Temp\\SelectedAssembledPlots.pdf is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'SelectedAssembledPlots.pdf', StartTime):
            assert False, ('Supporting Script test Opt-H-1 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test Opt-H-1 OK.')
    
    
        # Create a file with the assembly sequence
        MockFile = open(DB.SessionTempDirecory + os.sep + 'TestPlotSequence.txt','w')
        MockFile.write(GraphSequenceString)
        MockFile.close()
    
        # test that The report Assembly routine works ok via file
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('CreatePlotsFromCSV.py ' + DB.SessionTempDirecory + os.sep + 'SelectedAssembledColumns.csv '  + DB.SessionTempDirecory + os.sep + 'SelectedAssembledPlots1.pdf ' + DB.SessionTempDirecory + os.sep + 'TestPlotSequence.txt' )
        if ReturnCode != 0:
            assert False, ('Supporting Script test Opt-H-2 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test Opt-H-2 OK.')
    
    
        # test that the file Temp\\SelectedAssembledPlots1.pdf is recent
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'SelectedAssembledPlots1.pdf', StartTime):
            assert False, ('Supporting Script test Opt-H-3 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test Opt-H-3 OK.')
    


        # This script will test the CodeFromDocAndSpreadsheet.py script
        # There is  need for a population csv file and a rules text file
        # Note that this is written as binary and read as binary since this was
        # written by a word doc file with some tables.
    
        MockFile = open(DB.SessionTempDirecory + os.sep + 'DocRulesOverride.txt','wb')
        MockFile.write('This file includes override rules for MIST test example 20 \r\nInitialization Rules:\r\nAffected Parameter\rOccurrence probability\rUpdate Rule (New Value)\rNotes\rAge\r1\r50\rOverride age\r\r\nPre state transition Rules:\r\nAffected Parameter\rOccurrence probability\rUpdate Rule (New Value)\rNotes\rAge\r1\rAge + 0.5\rAge Increase by half\r\r\nPost state transition Rules:\r\nAffected Parameter\rOccurrence probability\rUpdate Rule (New Value)\rNotes\rAge\r1\rAge + 0.5\rAge Increase by the other half\r\r\n')
        MockFile.close()

        MockFile = open(DB.SessionTempDirecory + os.sep + 'PopulationDistributionsOverride.csv','w')
        MockFile.write('Study Name,,Testing Population set for Simulation Example 20,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,,,,,Dummy Population,,\nStudy Length,, ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nGroups,, ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nGroup Sizes,, ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nLocation,, ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nPurpose,,Tests exmple 14,Another population to test exmple,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nEndpoints,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nInclusion/Exclusion Criteria,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nSimulation Length,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nSimulation Outcomes,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nAdditional notes,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nInternal Data,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nReference,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,,,,,Multiple references,,\n,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nGroup Size,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nGroup Description,,DEFAULT ,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,,,,,Dummy,,\nInternal Code,,1200,,,,,,1010,,,,,,1020,,,,,,1030,,,,,,1040,,,,,,1051,,,,,,1052,,,,,,1060,,,,,,1070,,,,,,1080,,,,,,1090,,,,,,1100,,,,,,1110,,,,,,1120,,,,,,1130,,,,,,1140,,,,,,1150,,,,,,111111113,,,,,,1170,,,,,,1180,,,,,,1190,,,,,,1210,,\n,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nParameter,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes,,,,Mean (SD),Actual coding ,Notes\nAge,Years,"30 (5) capped at 20,40","Min(Max(20,Gaussian(30,5)),40)",Copied from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code,,,,"35 (5) capped at 25,45","Min(Max(25,Gaussian(35,5)),45)",Changed from example code\nAlive,Proportion,0.9,Bernoulli(0.9),Copied from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code,,,,0.9,Bernoulli(0.8),Changed from example code\nDead,Proportion,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive,,,,0.1 = Not alive,1-Alive,Complamentary to Alive\n,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nObjective,,Filter Expression,Statistics Expression,Statistics Function,Target,Weight,Notes,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nObjective1,,1,Age,MAX,35,1,Maximal Age target is 35,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nObjective2,,1,Age-25,MEAN,0,2,Average Age target is 25,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\nObjective3,,Alive,Age,MEAN,24,2,Average Age of alive individuals is 24,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n')
        MockFile.close()




    
        (ReturnCode, StdOutData, StdErrData) = self.RunExternalScript('CodeFromDocAndSpreadsheet.py ' + DB.SessionTempDirecory + os.sep + 'PopulationDistributionsOverride.csv ' + DB.SessionTempDirecory + os.sep + 'DocRulesOverride.txt ' + DB.SessionTempDirecory + os.sep + 'TestingForRulesAndPopOverride.zip 20')
        if ReturnCode != 0:
            assert False, ('Supporting Script test I-0 FAILURE. Script returned bad exit code')
        else:
            print ('Supporting Script test I-0 OK.')
        # test that a new python generating file exists
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'TestingForRulesAndPopOverride.py', StartTime):
            assert False, ('Supporting Script test I-1 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test I-1 OK.')

        # test that a new zip archive exists
        if not self.FileExistsAndIsRecent (DB.SessionTempDirecory + os.sep + 'TestingForRulesAndPopOverride.zip', StartTime):
            assert False, ('Supporting Script test I-2 FAILURE. No recent Output file created')
        else:
            print ('Supporting Script test I-2 OK.')

        # now check that the new file actually has the new information
        StringToCheck = "try: SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 0, OccurrenceProbability = '1', AppliedFormula = '50', Notes = 'Override age')]\nexcept: AnalyzeVersionConversionError()\ntry: SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 1, OccurrenceProbability = '1', AppliedFormula = 'Age + 0.5', Notes = 'Age Increase by half')]\nexcept: AnalyzeVersionConversionError()\ntry: SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = 'Age', SimulationPhase = 3, OccurrenceProbability = '1', AppliedFormula = 'Age + 0.5', Notes = 'Age Increase by the other half')]\nexcept: AnalyzeVersionConversionError()\n"
        ThePythonFile = open(DB.SessionTempDirecory + os.sep + 'TestingForRulesAndPopOverride.py')
        TheScript = ThePythonFile.read()
        ThePythonFile.close()
        if not StringToCheck in TheScript:
            assert False, ('Supporting Script test I-3 FAILURE. Rules did not change in new file')
        else:
            print ('Supporting Script test I-3 OK.')

        StringToCheck = "try: DB.PopulationSets.AddNew( DB.PopulationSet(ID = 1200, Name = 'DEFAULT ', Source = 'Multiple references', Notes = 'Study Name: Testing Population set for Simulation Example 20. Study Length:  . Groups:  . Group Sizes:  . Location:  . Purpose: Tests exmple 14. Endpoints: . Inclusion/Exclusion Criteria: . Simulation Length: . Simulation Outcomes: . Additional notes: . : . ', DerivedFrom = 0, DataColumns = [('Age', 'Min(Max(20,Gaussian(30,5)),40)'), ('Alive', 'Bernoulli(0.9)'), ('Dead', '1-Alive')], Data = [], Objectives = [ ( DB.Expr('1') , DB.Expr('Age') , 'MAX', 35, 1, None, None ) , ( DB.Expr('1') , DB.Expr('Age-25') , 'MEAN', 0, 2, None, None ) , ( DB.Expr('Alive') , DB.Expr('Age') , 'MEAN', 24, 2, None, None ) ]), ProjectBypassID = 0)\nexcept: AnalyzeVersionConversionError()"
        ThePythonFile = open(DB.SessionTempDirecory + os.sep + 'TestingForRulesAndPopOverride.py')
        TheScript = ThePythonFile.read()
        ThePythonFile.close()
        if not StringToCheck in TheScript:
            assert False, ('Supporting Script test I-4 FAILURE. Population did not change in new file')
        else:
            print ('Supporting Script test I-4 OK.')


if __name__ == "__main__":
    Argv = sys.argv[:]
    Argv.insert(1,"-v")
    nose.main(argv=Argv)



