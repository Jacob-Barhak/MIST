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
################################################################################

import DataDef as DB
import sys
import pickle

def RunMultipleSimulations(InputFileName, ProjectIndex, NumberOfRepeats, StartRunningIndexStr, OverWriteFiles, ReconstructFromTraceback, NumberOfSimulationStepsOverride, PopulationRepetitionsOverride, ModelOverride, PopulationSetOverride, InitializeCoefficientValues):
    """ Run a specific project in the input FileName Multiple Times """
    def LoadDataAndApplyOverrides(InputFileName, ProjectIndex, ModelOverride, PopulationSetOverride, InitializeCoefficientValues):
        " Loads the data file, and applies overrides for further handling "
        # First load the data - this also erases old results
        DB.LoadAllData(InputFileName)
        # First detect the population override 
        try:
            # Handle PopulationSetOverride
            if DB.IsList(PopulationSetOverride):
                # [x] means ModelID = x
                # The override is provided as a list, pull out the number is the
                # list. This number is the actual ID, not the sort order
                PopulationToUseID = PopulationSetOverride[0]
            elif DB.IsInt(PopulationSetOverride):
                # Extract the PopulationSetID from the sort order of populations
                # This way the user has to tell the index the same way it is
                #  shown in the GUI
                PopulationToUseID = sorted(DB.PopulationSets.keys())[PopulationSetOverride]
            elif PopulationSetOverride==None:
                PopulationToUseID = None
            elif PopulationSetOverride!=None:
                # raise the error to show the error message
                raise ValueError, "Unrecognized input for population"
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Run Multiple Simulations Error: The system could not figure out the index of the populations set - please make sure there are population sets in your file and that you specified the index correctly. Note that a populations set index of 0 means the first populations set and if there are n population sets in a file, the index of the last population set is n-1. If you specified the population set index in bracket, make sure you are not using the population set sort order as without brackets. Here are more details regarding the error: ' + str(ExceptValue)

        # Find the project to use if not defined - auto detect
        try:
            if DB.IsList(ProjectIndex):
                # [x] means ProjectID = x
                # The override is provided as a list, pull out the number in the
                # list. This number is the actual ID, not the sort order
                ProjectID = ProjectIndex[0]
            elif DB.IsInt(ProjectIndex):
                # otherwise use the index to pull out the correct project from 
                # the list. This number is the actual ID, not the sort order
                # This way the user has to tell the index the same way it is 
                # shown in the GUI
                ProjectID = sorted(DB.Projects.keys())[ProjectIndex]
            elif ProjectIndex == None and PopulationToUseID != None:
                # None means the first project in the list
                ProjectID = sorted(DB.Projects.keys())[0]
            else:
                raise ValueError, "Unrecognized input for project"
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Run Multiple Simulations Error: The system could not figure out the index of the project - please make sure there are projects in your file and that you specified the index correctly. Note that a project index of 0 means the first project and if there are n projects in a file, the index of the last project is n-1. If you specified the project index in bracket, make sure you are not using the project sort order as without brackets. Here are more details regarding the error: ' + str(ExceptValue)
        ProjectToRun = DB.Projects[ProjectID]
        # Do not continue changing the project if no simulation requested
        if NumberOfSimulationStepsOverride != 0:
            # Handle NumberOfSimulationStepsOverride - ignore zero since it 
            # means population generation
            if NumberOfSimulationStepsOverride != None:
                ProjectToRun.NumberOfSimulationSteps = NumberOfSimulationStepsOverride
            # Handle PopulationRepetitionsOverride
            if PopulationRepetitionsOverride != None:
                ProjectToRun.NumberOfRepetitions = PopulationRepetitionsOverride
            try:
                # Handle ModelOverride
                if DB.IsList(ModelOverride):
                    # [x] means ModelID = x
                    # The override is provided as a list, pull out the number
                    # in the list. This number is the actual ID, not sort order
                    ProjectToRun.PrimaryModelID = ModelOverride[0]
                    ProjectToRun.Notes = '!!! Model override during simulation launch !!! ' + ProjectToRun.Notes
                elif DB.IsInt(ModelOverride):
                    # Extract the ModelID from the sort order of Models
                    # This way the user has to tell the index the same way it
                    # is shown in the GUI
                    ProjectToRun.PrimaryModelID = sorted(DB.StudyModels.keys())[ModelOverride]
                    ProjectToRun.Notes = '!!! Model override during simulation launch !!! ' + ProjectToRun.Notes
                elif ModelOverride!=None:
                    # raise the error to show the error message
                    raise ValueError, "Unrecognized input for model"
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                raise ValueError, 'Run Multiple Simulations Error: The system could not figure out the index of the model - please make sure there are models in your file and that you specified the index correctly. Note that a model index of 0 means the first model and if there are n models in a file, the index of the last model is n-1. If you specified the model index in bracket, make sure you are not using the model sort order as without brackets. Here are more details regarding the error: ' + str(ExceptValue)
            # Record the population Override in Project
            if PopulationToUseID != None:
                ProjectToRun.PrimaryPopulationSetID = PopulationToUseID
                ProjectToRun.Notes = '!!! Population set override during simulation launch !!! ' + ProjectToRun.Notes
            try:
                # Handle InitializeCoefficientValues Rule overrides
                for (RuleEnum,InitValue) in enumerate(InitializeCoefficientValues):
                    RuleToReplace = ProjectToRun.SimulationRules[RuleEnum]
                    if RuleToReplace.SimulationPhase != 0:
                        raise ValueError, "ASSERTION ERROR: Attempt to replace a rule not in initialization"
                    # Create a new rule using the old one
                    ReplaceRule = DB.SimulationRule(AffectedParam = RuleToReplace.AffectedParam, SimulationPhase = RuleToReplace.SimulationPhase, AppliedFormula = DB.Expr(DB.SmartStr(InitValue)), Notes = '!!! Initialization value override during simulation launch !!! ' + RuleToReplace.Notes)
                    # Now actually replace the rule in the sequence
                    ProjectToRun.SimulationRules[RuleEnum] = ReplaceRule
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                raise ValueError, 'Run Multiple Simulations Error: The system could not apply an initial value override to one or more of the rules. Make sure that the overrides do not exceed the number of initialization rules and that the values are reasonable. Here are more details regarding the error: ' + str(ExceptValue)
            # Make sure that all changes made are valid
            ProjectToRun.VerifyData()
        return (ProjectToRun, PopulationToUseID)

    (FileNameBase,FileNameExt) = DB.os.path.splitext(InputFileName)
    (PathOnly , FileNameOnly, FileNameFullPath) = DB.DetermineFileNameAndPath(InputFileName)
    (FileNameBaseNoPath,TempFileNameExt) = DB.os.path.splitext(FileNameOnly)

    OutputFileNames = []
    ErrorsDetected = []
    # Load the data
    (ProjectToRun, PopulationToUseID) = LoadDataAndApplyOverrides(InputFileName, ProjectIndex, ModelOverride, PopulationSetOverride, InitializeCoefficientValues)
    for Repetition in range(NumberOfRepeats):
        try:
            DeleteResultsAfterSave = True
            StartRunningIndex = int(StartRunningIndexStr)
            FileEnumerationSufix = '_' +('%0'+str(len(str(StartRunningIndex+NumberOfRepeats-1)))+'i')%(StartRunningIndex + Repetition)            
        except:
            FileEnumerationSufix = '_' + StartRunningIndexStr + '_' + ('%0'+str(len(str(NumberOfRepeats-1)))+'i')%(Repetition)
            # do not add a number at the end in case of a single repetition
            # The user supplies suffix only is used in this case so we
            # don't delete results since we expect them all in this file
            DeleteResultsAfterSave = False
            if NumberOfRepeats == 1:
                FileEnumerationSufix = FileEnumerationSufix[:-2]
        FileNameToUse = FileNameBaseNoPath + FileEnumerationSufix
        TraceBackFileNameToUse = FileNameBase + FileEnumerationSufix + '_TraceBack.txt'
        if ReconstructFromTraceback:
            try:
                TraceBackFile = open(TraceBackFileNameToUse,'r')
                SimulationTraceBack = pickle.load(TraceBackFile)
                PopulationTraceBack = SimulationTraceBack[-1]
                TraceBackFile.close()
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                ErrorsDetected = ErrorsDetected + [(Repetition, ExceptType, ExceptValue)]
                print '!'*70
                print 'Run Multiple Simulations Error: Reading from TraceBack File failed - Error Detected in  Repetition # '+ str(Repetition) + ' Here are additional details regarding the error: ' + str(ExceptType) + ' : ' + str(ExceptValue)
                print '!'*70
                # skip this loop iteration - try next repetition
                continue       
        else:
            SimulationTraceBack = None
            PopulationTraceBack = None
        try:
            if NumberOfSimulationStepsOverride != 0 or PopulationToUseID == None:
                Pop = DB.PopulationSets[ProjectToRun.PrimaryPopulationSetID]
                PopulationSizeToGenerate = ProjectToRun.NumberOfRepetitions
            else:
                Pop = DB.PopulationSets[PopulationToUseID]
                PopulationSizeToGenerate = PopulationRepetitionsOverride
            if Pop.IsDistributionBased():
                # If population is distribution based - generate data for it
                # Note that the new population set will have the last ID
                print '#'*70
                print '# Generating Population Set from Distributions' 
                OverridePopulationSet = Pop.GenerateDataPopulationFromDistributionPopulation(GeneratedPopulationSize = PopulationSizeToGenerate, GenerationFileNamePrefix = FileNameToUse + '_Gen' +('Rep'*ReconstructFromTraceback) , RecreateFromTraceBack = PopulationTraceBack)
                # keep the same population name - generation notes are still
                # available - yet the name is important for reference
                OverridePopulationSet.Name = Pop.Name
                print '# Population Set Generated' 
                print '#'*70
                OverrideNumberOfRepetitions = 1
            elif NumberOfSimulationStepsOverride == 0:
                # If requested generating population that is data based
                # Note that the new population set will have the last ID
                print '#'*70
                print '# Expanding Population Set from existing set' 
                # keep the same population name
                OverridePopulationSet = DB.PopulationSets.Copy(Pop.ID, Pop.Name)
                # Figure out how many replicas of the population are needed
                if PopulationRepetitionsOverride != None: 
                    # If override defined, use it
                    NumberOfPopulationReplicas = PopulationRepetitionsOverride
                else:
                    # otherwise, extract it from the project
                    NumberOfPopulationReplicas = ProjectToRun.NumberOfRepetitions
                # Now Apply the multiplier to the data to expand the population
                # so the simulation will not need to do it. Note that
                # in return during simulation using these population
                # the repetition number should be adjusted to 1
                OverridePopulationSet.Data = Pop.Data*NumberOfPopulationReplicas
                print '# Population Set expanded' 
                print '#'*70
                OverrideNumberOfRepetitions = None
            else:
                # If population is data based and no generation request was 
                # made then just use it
                OverridePopulationSet = None
                OverrideNumberOfRepetitions = None

            if NumberOfSimulationStepsOverride != 0:
                # do not run anything if just generating the population
                ScriptFileNameFullPath = ProjectToRun.CompileSimulation(SimulationScriptFileNamePrefix = FileNameToUse + '_Sim'+('Rep'*ReconstructFromTraceback), OverrideRepetitionCount = OverrideNumberOfRepetitions, OverridePopulationSet = OverridePopulationSet , RecreateFromTraceBack = SimulationTraceBack)                
                # Reload data to wipe results from previous run - deprecated 
                # (ProjectToRun, PopulationToUseID) = LoadDataAndApplyOverrides(InputFileName, ProjectIndex, ModelOverride, PopulationSetOverride, InitializeCoefficientValues)            
                # Recalculate filename
                ResultsInfo = ProjectToRun.RunSimulationAndCollectResults(ScriptFileNameFullPath)
            NewFileName = PathOnly + DB.os.sep + FileNameToUse + FileNameExt
            print '#'*70
            print '#'*70
            print '# Repetition number: ' + str (Repetition)
            print '# Creating File Name: ' + NewFileName
            print '#'*70
            print '#'*70

            # Save the new file anyway - if either simulation or generation were executed
            DB.SaveAllData(NewFileName, OverWriteFiles)
            # If not reproduction of previous work write TraceBack file
            # If this is reproduction, then skip writing the file
            if not ReconstructFromTraceback:
                TraceBackFile = open(TraceBackFileNameToUse,'w')
                # if only population generation, handle traceback differently
                if NumberOfSimulationStepsOverride != 0:
                    pickle.dump(ResultsInfo.TraceBack,TraceBackFile)
                else:
                    # For population generation, the TraceBack information
                    # for the population is stored in the last tuple element
                    # Non is used as the first element to signify that no
                    # simulation took place. This conforms with the load
                    # TraceBack code for reconstruction regardless if 
                    # Simulation took place.
                    pickle.dump((None,OverridePopulationSet.TraceBack),TraceBackFile)
                TraceBackFile.close()
            if DeleteResultsAfterSave:
                # in case we are saving in multiple consecutive files 
                # make sure the results are deleted before the next 
                # result set is generated
                DB.SimulationResults.Delete(ResultsInfo.ID)
            # write the file name
            print NewFileName
            OutputFileNames = OutputFileNames + [NewFileName]
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            ErrorsDetected = ErrorsDetected + [(Repetition, ExceptType, ExceptValue)]
            print '!'*70
            print '!'*70
            print 'Run Multiple Simulations Error: Error Detected in Repetition # '+ str(Repetition) + ' Here are additional details regarding the error: ' + str(ExceptType) + ' : ' + str(ExceptValue)
            print '!'*70
            print '!'*70
    print 'Completed All ' + str(NumberOfRepeats) + ' Simulations'
    return OutputFileNames, ErrorsDetected

if __name__ == "__main__":
    # Redirect stdout to File if needed
    (sys.stdout, BackupOfOriginal) = DB.RedirectOutputToValidFile(sys.stdout)
    # uncomment the next line for debug info regarding redirection
    # print (sys.stdout, BackupOfOriginal)
    ProjectToRun = None
    NumberOfRepeats = 100
    StartRunningIndex = 0
    OverWriteFilesOrReconstructFromTracebackStr = ''
    NumberOfSimulationStepsOverride = None
    PopulationRepetitionsOverride = None
    ModelOverride = None
    PopulationSetOverride = None
    InitializeCoefficientValues = []
    # If there are command line arguments passed, use them rather than ask
    # questions from the user
    if len(sys.argv) > 1:
        InputFileName = sys.argv[1]
        if len(sys.argv) > 2:
            ProjectToRun = eval(sys.argv[2], DB.EmptyEvalDict)
        if len(sys.argv) > 3:
            NumberOfRepeats = int(sys.argv[3])
        if len(sys.argv) > 4:
            StartRunningIndexStr = (sys.argv[4])
        if len(sys.argv) > 5:
            OverWriteFilesOrReconstructFromTracebackStr = sys.argv[5]
        if len(sys.argv) > 6:
            NumberOfSimulationStepsOverride = eval(sys.argv[6], DB.EmptyEvalDict)
        if len(sys.argv) > 7:
            PopulationRepetitionsOverride = eval(sys.argv[7], DB.EmptyEvalDict)
        if len(sys.argv) > 8:
            ModelOverride = eval(sys.argv[8], DB.EmptyEvalDict)
        if len(sys.argv) > 9:
            PopulationSetOverride = eval(sys.argv[9], DB.EmptyEvalDict)
        if len(sys.argv) > 10:
            InitializeCoefficientValues = map(lambda Entry: eval(Entry, DB.EmptyEvalDict), sys.argv[10:])
    else:
        # Ask the user for information
        # Ask the user to provide file name to run
        print 'Info: this script can be invoked from command line using the following syntax:'
        print ' MultiRunSimulation.py FileName [OptionalArguments...] '
        print ' OptionalArguments consists of the following parameters in this order:'
        print '  ProjectIndex: is the sort order of the project in the file, unless enclosed'
        print '                by brackets in which case it means the internal project ID.' 
        print '                the default is 0 - meaning the first project in the file'
        print '  Repetitions: The number of times to repeat the simulation'
        print '  StartIndex: A string that will become a suffix to the filename in output.'
        print '              if it is an integer - it will start the enumerated sequence of'
        print '              output files and will not accumulate results in the same file.'
        print '  OverWriteFilesOrReconstructFromTraceback: If y (default), then output'
        print '                                            files will overwrite old ones. '
        print '                                            If r then reconstruct simulation'
        print '                                            from TraceBack files in same dir'
        print '  NumberOfSimulationStepsOverride: Defines a new number of simulation steps'
        print '                                   for the project. Use None for no override'
        print '                                   Zero indicates population generation '
        print '                                   alone without simulation' 
        print '  PopulationRepetitionsOverride: Defines a new number of times to repeat the'
        print '                                 population within the same file. This is '
        print '                                 especially useful for distribution based '
        print '                                 population sets. Use None for no override.'
        print '  ModelOverrideID: The sort order of the Model to override the Model in the'
        print '                   current project. If None, then no override occurs. If '
        print '                   enclosed in brackets then the internal ID is used.'
        print '  PopulationOverrideID: The sort order of the PopulationSet to override the'
        print '                        PopulationSet used in the current project. Negative' 
        print '                        means counting from last. None = no override.'
        print '                        [Number in Brackets] = use internal ID'
        print '  RuleValueOverrides: A set of numeric values to override the value in the'
        print '                      Project rules. These values should be in the same order'
        print '                      rules are defined in the project.'
        print ''
        print ' This script is very useful for running MIST batch simulations in parallel'
        print ''
        InputFileName = raw_input( 'Please enter a data file name to be simulated: ' )
        DB.LoadAllData(InputFileName)
        UnsortedSimulationProjects = filter (lambda Entry: Entry.ProjectType == 'Simulation', DB.Projects.values())
        SimulationProjects = sorted(UnsortedSimulationProjects, key = lambda Entry:Entry.ID)
        # Ask the user which project to use
        print
        ProjectToRun = None
        for (ProjectEnum,SimulationProject) in enumerate(SimulationProjects):
            print 'The following project was detected'
            print SimulationProject.GenerateReport()
            UseThisProject = raw_input( 'Should I use this project? Y for Yes (Default): ' )
            # Ask the user which project to use
            if UseThisProject.strip().lower() in ['y' , '']:
                ProjectToRun = [SimulationProject.ID]
                break
        # Add repetition information
        print
        NumberOfRepeatsStr = raw_input( 'Please enter the number of times to perform this simulation (100 by default): ' )
        if NumberOfRepeatsStr.strip() != '':
            NumberOfRepeats = int(NumberOfRepeatsStr)
        # Handle Start index
        print
        StartRunningIndexStr = raw_input( 'Please enter the suffix/start number for the running index for the simulation repeats (0 by default): ' )
        # Should files be replaced
        print
        OverWriteFilesOrReconstructFromTracebackStr = raw_input( 'Should I overwrite files with the same names or reconstruct simulation from TraceBack? Y for Yes t overwrite (Default), R for Reconstruct and overwrite:' )
        # Number of repetitions override
        NumberOfSimulationStepsOverrideStr = raw_input( 'Please enter the number of simulation steps to override the project default. Zero means population generation alone without simulation. Use None for no change (Default):' )
        if NumberOfSimulationStepsOverrideStr.strip() != '':
            NumberOfSimulationStepsOverride = eval(NumberOfSimulationStepsOverrideStr, DB.EmptyEvalDict)
        # Number of population repetitions override
        PopulationRepetitionsOverrideStr = raw_input( 'Please enter the number of population repetitions to override the project defualt. Use None for no change (Default):' )
        if PopulationRepetitionsOverrideStr.strip() != '':
            PopulationRepetitionsOverride = eval(PopulationRepetitionsOverrideStr, DB.EmptyEvalDict)
        # Handle model overrides
        UnsortedModels = filter (lambda Entry: Entry.StudyLength ==0, DB.StudyModels.values())
        ModelsToParse = sorted(UnsortedModels, key = lambda Entry:Entry.ID)
        print
        print 'Here is a list of Models - sorted by internal ID' 
        for (ModelEnum,Model) in enumerate(ModelsToParse):
            print str(ModelEnum)+ ') ' + Model.Describe()
        ModelOverrideStr = raw_input( 'Enter a model number to override the current model used in the project. 0 Means the first Model in the list. Use None for no replacement (Default):' )
        if ModelOverrideStr.strip() != '':
            ModelOverride = eval(ModelOverrideStr, DB.EmptyEvalDict)
        # Handle population overrides
        print
        PopulationSetsToParse = sorted(DB.PopulationSets.values(), key = lambda Entry:Entry.ID)
        print 'Here is a list of Population Sets - sorted by internal ID' 
        for (PopSetEnum,PopSet) in enumerate(PopulationSetsToParse):
            print str(PopSetEnum)+ ') ' + PopSet.Describe()
        PopulationSetOverrideStr = raw_input( 'Enter a population set number to override the Population set used in the project. 0 Means the first Population in the list, negative means counting Backwards from last. Use None for no replacement (Default):' )
        if PopulationSetOverrideStr.strip() != '':
            PopulationSetOverride = eval(PopulationSetOverrideStr, DB.EmptyEvalDict)
        # Handle Rule value overrides
        print
        for SimRule in SimulationProject.SimulationRules:
            print 'Consider the simulation rule: \n' + SimRule.GenerateReport()
            RuleValueOverrideStr = raw_input( 'Enter a numeric value to replace the Applied Formula. Leave blank to start simulation:' )
            if RuleValueOverrideStr.strip() == '':
                break
            else:
                InitializeCoefficientValues.append(eval(RuleValueOverrideStr, DB.EmptyEvalDict))
    # Interpret the text of OverWriteFilesOrReconstructFromTracebackStr to Boolean 
    OverWriteFiles = (OverWriteFilesOrReconstructFromTracebackStr.strip().lower() in ['y' , 'r', ''])
    ReconstructFromTraceback = 'r' in OverWriteFilesOrReconstructFromTracebackStr.strip().lower()
    # Now run the simulations
    (OutputFileNames, ErrorsDetected) = RunMultipleSimulations(InputFileName, ProjectToRun, NumberOfRepeats, StartRunningIndexStr, OverWriteFiles, ReconstructFromTraceback, NumberOfSimulationStepsOverride, PopulationRepetitionsOverride, ModelOverride, PopulationSetOverride, InitializeCoefficientValues)
    
    print '#'*70
    print '#'*70
    print '#'*70
    print 'Generation complete, here is the list of generated output files'
    for OutputFileName in OutputFileNames:
        print OutputFileName
    print '#'*70
    print '#'*70
    print '#'*70
    for ErrorDetected in ErrorsDetected:
        (Repetition, ExceptType, ExceptValue) = ErrorDetected
        print '!'*70
        print '!'*70
        print 'Run Multiple Simulations Error: Error Detected in Repetition # '+ str(Repetition) + ' Here are additional details regarding the error:' + str(ExceptValue)
        print '!'*70
        print '!'*70
    # Redirect stdout back if needed
    sys.stdout = DB.RedirectOutputBackwards(sys.stdout, BackupOfOriginal)
