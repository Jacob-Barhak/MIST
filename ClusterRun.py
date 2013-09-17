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
# Copyright (C) 2011-2012 The Regents of the University of Michigan
# Initially developed by Jacob Barhak
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

# This script runs the simulations on a Sun Grid Engine (SGE) and collects
# results nd processes them into reports and plots
# It is part of the MIST system and requires an installation of SGE
# This file is just an example and uses SGE with specific definitions
# This script will need changing to run specific simulations



import DataDef as DB
import shlex
import subprocess

StartTimeStr = DB.datetime.datetime.now().isoformat('T').replace(':','_')
ErrorCount = 0

###########################################################
#################### Define Scenario  #####################
###########################################################

# Give a name for the scenario you are running
Scenario = 'TEST'

# Name the file name to run - without the zip extension
FileNamePrefix='Testing'


# This will be the name for the job - this line can be changed by the user
JobName = Scenario +'_'+ FileNamePrefix +'_'+ StartTimeStr

# Define the enviroment for each phase
Phase1Environemnt = '-cwd -p -100'
Phase2Environemnt = '-cwd'
Phase3Environemnt = '-cwd'
Phase4Environemnt = '-cwd'

# Decide which phases to run
# Run simulation and create a zip file with results for each run
RunPhase1A = True
# Create an individual csv statistics file for each zip file
RunPhase1B = True
# Collect statistics from all CSV files into a single CSV file
RunPhase2 = True
# Assmble final report
RunPhase3 = True
# Analyze the results - need to define processing before enabling this stage
RunPhase4A = False
# Generate plots - Nice to have
RunPhase4B = True

# if DebugRun is at least:
#    1 - commands are printed and not passed to the OS, Directories not created
#    2 - skipped report scenarios are printed - possiblly very long list
DebugRun = (DB.sys.platform == 'win32')*1

# define disk usage - this may also speed up computations on a cluster
# Empty List = Leave all files
# 'NoZip' = remove zip files after csv created at RunPhase1B - Low Disk usage
# 'LessCSV' = remove csv files after csv created at RunPhase2 - Lower NFS IO 
# 'NoErr' = do not create log files - can reduce disk space yet not recommended
# 'NoLog' = Do not create Err files - can reduce disk space yet not recommended
# A run that minimizes disk use would be:
# DiskUsage = ['NoZip', 'LessCSV', 'NoErr', 'NoLog']
# Yet for initial runs it is recommended to leave all files and use 
# DiskUsage = []
DiskUsage = []

# Reproduce Results from TraceBack of a previous Run if True
ReproduceResultsFromTraceback = False


# For Reconstruction Purposes in case of a bad run, rerun only those scenario
# ranges where each range is (Start, End) and only variations in between
# where Start<=VariationEnum<=End are executed. Note that all repetitions
# for the variation will be rerun and codes will remain the same so results
# can be remerged into a previous run. Note that generating plots for these
# partial runs may not make sense and phase 3A may generate a report that will
# need manual merging with a previous incomplete report. also note that the
# enumerated variation name appears on reports with a leading 1 and zeros
# and (Start,End) tuples will have this prefix as well

RunOnlyTheseScenarioEnumRanges = []


# Define directories to organize data, results, and log files
DirInput = 'InData' + DB.os.sep
DirLog = 'Log' + DB.os.sep 
DirErr = 'Err' + DB.os.sep 
DirPhase1A = 'Phase1A' + DB.os.sep 
DirPhase1B = 'Phase1B' + DB.os.sep 
DirPhase2 = 'Phase2' + DB.os.sep 
DirPhase3 = 'Phase3' + DB.os.sep 
DirPhase4 = 'Phase4' + DB.os.sep 
DirTemp = DB.DefaultTempPathName + DB.os.sep

Dirs = (DirInput, DirLog, DirErr, DirPhase1A, DirPhase1B, DirPhase2, DirPhase3, DirPhase4, DirTemp) 



# Define running parameters for each scenario

if Scenario in ['TEST']:
    Repetitions = 100
    SimulationTimeOverride = '10'
    PopulationRepetitionsOverride = 'None'



OptionsSeperation1 = []
if Scenario in ['TEST']:
    OptionsSeperation1.append(('  ','NoSeperation1'))

OptionsSeperation2 = []
if Scenario in ['TEST']:
    OptionsSeperation2.append(('  ','NoSeperation2'))

OptionsSeperation3 = []
if Scenario in ['TEST']:
    OptionsSeperation3.append(('  ','NoSeperation3'))
    
OptionsSeperation4 = []
if Scenario in ['TEST']:
    OptionsSeperation4.append(('  ','NoSeperation4'))
    
OptionsSeperation5 = []
if Scenario in ['TEST']:
    OptionsSeperation5.append(('  ','NoSeperation5'))

OptionsSeperation6 = []
if Scenario in ['TEST']:
    OptionsSeperation6.append(('  ','NoSeperation6'))


Stratifications = []
if Scenario in ['TEST']:
    StratifyBy = ''
    Stratifications.append(('Stratification - None:',''))


PopulationsToUse = []
if Scenario in ['TEST']:
    PopulationsToUse.append(('None', 'NoPopulationChange'))


ModelsToUse = []
if Scenario in ['TEST']:
    ModelsToUse.append(('None','DefaultModel')) 


ProjectsToUse = []
if Scenario in ['TEST']:
    ProjectsToUse.append(('4','Example5a')) 
    ProjectsToUse.append(('5','Example5b')) 



    
# Define Exclusions / Inlusion criteria to narrow down numbers of simulations
# This is handled by building a title for each variation and making sure that
# the title includes all sub titles in the list for inclusions and none of
# these subtitles together in the case in exclusion.

# By default, there would be no Inclusions/Exclusions
# Also allow variation in no more than a certain number of dimensions.
# Changes are counted around the first dimension
Inclusions = []
Exclusions = []
MaxDimensionsToAllowVariation = 10

# Specify specific Inclusion/exclusion criteria per scenario
if Scenario in ['TEST']:
    pass


# Define the reference in the report

if Scenario in ['TEST']:
    # Define Reference File Name the user should provide - use blank string to auto generate
    ReportReferenceFileName = ''
    # Define the reference to use with column
    ReportReferenceColumnTuple = ( ReportReferenceFileName, 'Ref','All')
    # Define all validation query files to use on final results in a sequence
    FinalReportValidationQueries = []



# Define the times for which the report will be generated
if Scenario in ['TEST']:
    SummaryReportTimes = [('1','10')]



#### Define how the plots should look like:

if Scenario in ['TEST']:
    SummaryIntervals = [[0,0], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1,10], 1]
    ColumnFilter = [('<Header>', 'Auto Detect', ''), 
                    ('State0', 'Sum Over All Records', ''), 
                    ('State1', 'Sum Over All Records', ''), 
                    ('State2Terminal', 'Sum Over Last Observations Carried Forward', '')]
    PlotFilter = [ ('','Start Step','Study Year'), 
                   ('','Rec Count','Record Count'),
                   ('State0', 'Sum All',''),
                   ('State1', 'Sum All',''),
                   ('State2Terminal', 'Sum LOCF','')]
    PlotStyles = ['r-','g-','b-','k-',    'r--','g--','b--','k--',    'r-.','g-.','b-.','k-.',    'r:','g:','b:','k:',    'c-','m-','y-','k.',    'c--','m--','y--','k,',    'c-.','m-.','y-.','k_',    'c:','m:','y:','k|']


# Define the column Filter File Name to be used
ReportFilterFileName = DirTemp + 'ReportFilter.opt'

###########################################################
################ End of Define Scenario  ##################
###########################################################

# Make sure all directories exist:
if DebugRun < 1:
    for Dir in Dirs:
        if not DB.os.path.exists(Dir):
            DB.os.mkdir(Dir)


# Now write the report filter to file
TheFilterFile = open(ReportFilterFileName,'w')
TheFilterFile.write('SummaryIntervals\n')
TheFilterFile.write(str(SummaryIntervals)+'\n')
if StratifyBy != '':
    TheFilterFile.write('StratifyBy\n')
    TheFilterFile.write(repr(StratifyBy)+'\n')
TheFilterFile.write('ColumnFilter\n')
TheFilterFile.write(str(ColumnFilter)+'\n')
TheFilterFile.close()


# Now build all possible combinations of options to run
# These are the variations

SimulationVariationCodes = {}

# Recall the ID for the first variation
FirstVariationID = [ProjectsToUse[0][0], ModelsToUse[0][0], PopulationsToUse[0][0], OptionsSeperation1[0][0], OptionsSeperation2[0][0], OptionsSeperation3[0][0], OptionsSeperation4[0][0], OptionsSeperation5[0][0], OptionsSeperation6[0][0]]

if RunOnlyTheseScenarioEnumRanges != []:
    # If codes were defined - look at the previous last code to deduce digits
    CodeDigitsForVariations = int(DB.math.log10(RunOnlyTheseScenarioEnumRanges[-1][-1]))

OptionsRunningIndex = 0
TheStr = ""
for (ProjectIDToUse,ProjectTitleToUse) in ProjectsToUse:
    for (ModelIDToUse,ModelTitleToUse) in ModelsToUse:
        for (PopulationIDToUse,PopulationTitleToUse) in PopulationsToUse:
            for (ValueSeperation6,TitleSeperation6) in OptionsSeperation6:
                for (ValueSeperation5,TitleSeperation5) in OptionsSeperation5:
                    for (ValueSeperation4,TitleSeperation4) in OptionsSeperation4:
                        for (ValueSeperation3,TitleSeperation3) in OptionsSeperation3:
                            for (ValueSeperation2,TitleSeperation2) in OptionsSeperation2:
                                for (ValueSeperation1,TitleSeperation1) in OptionsSeperation1:
                                    # This is the candidate key
                                    OptionsKeyTuple = (ProjectIDToUse, ModelIDToUse, PopulationIDToUse, ValueSeperation1, ValueSeperation2, ValueSeperation3, ValueSeperation4, ValueSeperation5, ValueSeperation6)
                                    # Check how many dimensions have variated
                                    DimensionsThatChanged = sum(map(DB.Ne, OptionsKeyTuple, FirstVariationID))
                                    # Check that dimension variations is within
                                    # the allowed number of variations
                                    if DimensionsThatChanged > MaxDimensionsToAllowVariation:
                                        # Skip variations that have more
                                        # dimension variation than allowed
                                        continue
                                    # Check no duplicates were defined by the user
                                    TitleForCheck = ProjectTitleToUse +' '+ ModelTitleToUse +' '+ PopulationTitleToUse +' '+ TitleSeperation1 +' '+ TitleSeperation2 +' '+ TitleSeperation3 +' '+ TitleSeperation4 +' '+ TitleSeperation5 +' '+ TitleSeperation6
                                    if OptionsKeyTuple in SimulationVariationCodes.keys():
                                        raise ValueError, "Error: A duplicate run was detected - please check that no duplicate option was defined. The duplicate option was: " + str([(ProjectIDToUse,ProjectTitleToUse), (ModelIDToUse,ModelTitleToUse), (PopulationIDToUse,PopulationTitleToUse), (ValueSeperation1,TitleSeperation1), (ValueSeperation2,TitleSeperation2), (ValueSeperation3,TitleSeperation3), (ValueSeperation4,TitleSeperation4), (ValueSeperation5,TitleSeperation5), (ValueSeperation6,TitleSeperation6)])
                                    # Check if this variation should be included
                                    # first check exclusions
                                    if Exclusions!=[] and any([all([(TitleTest in TitleForCheck) for TitleTest in TestStrings]) for TestStrings in Exclusions]):
                                        # skip any exclusion in the title 
                                        continue
                                    if Inclusions==[] or any([all([(TitleTest in TitleForCheck) for TitleTest in TestStrings]) for TestStrings in Inclusions]):
                                        # Include variation in list
                                        IsVariationEnumWithinRange = True
                                        if RunOnlyTheseScenarioEnumRanges != []:
                                            IsVariationEnumWithinRange = False
                                            for (StartRange,EndRange) in RunOnlyTheseScenarioEnumRanges:
                                                if (StartRange <= ((10**CodeDigitsForVariations) + OptionsRunningIndex) <= EndRange):
                                                    IsVariationEnumWithinRange = True
                                        if IsVariationEnumWithinRange:
                                            SimulationVariationCodes[OptionsKeyTuple] = OptionsRunningIndex
                                        OptionsRunningIndex = OptionsRunningIndex + 1

if RunOnlyTheseScenarioEnumRanges == []:
    # Code digits are determined at the end if not deduced from existing code
    CodeDigitsForVariations = int(DB.math.log10(OptionsRunningIndex))+2
    
CodeDigitsForRepetitions = int(DB.math.log10(Repetitions))+2


###########################################################
################### Run the simulations ###################
###########################################################


# Process Phase 1
if RunPhase1A or RunPhase1B:
    # Loop through variations 
    for (Variation, VariationEnum) in sorted(SimulationVariationCodes.iteritems(), key = lambda Entry:Entry[1]):
        for RepeatEnum in range(Repetitions):
            (ProjectIDToUse, ModelIDToUse, PopulationIDToUse, ValueSeperation1, ValueSeperation2, ValueSeperation3, ValueSeperation4, ValueSeperation5, ValueSeperation6) = Variation
            RunningIndex = ((10**CodeDigitsForVariations) + (VariationEnum)) * 10**CodeDigitsForRepetitions + RepeatEnum
            JobEnv = 'qsub ' + Phase1Environemnt
            if 'NoLog' not in DiskUsage:
                JobEnv = JobEnv + ' -o ' + DirLog + 'Out'+str(RunningIndex)+'_'+str(RepeatEnum) +'.log'
            if 'NoErr' not in DiskUsage:
                JobEnv = JobEnv + ' -e ' + DirErr + 'Out'+str(RunningIndex)+'_'+str(RepeatEnum) +'.err'
            JobEnv = JobEnv + ' -N ' + JobName + 'V' + str(VariationEnum) + 'R' +str(RepeatEnum)
            #--dependency=singleton
            ScriptToRun = '#!/bin/bash\n'
            ScriptToRun = ScriptToRun + 'echo "Start Variation ' + str(VariationEnum) + ' Repetition ' + str(RepeatEnum) + '"\n'
            # Run the simulation
            # Start by running the simualtion to produce result files
            if RunPhase1A:
                if ReproduceResultsFromTraceback:
                    OverWriteFilesOrReconstructFromTraceback = 'R'
                else:
                    OverWriteFilesOrReconstructFromTraceback = 'Y'
                ScriptToRun = ScriptToRun + 'python MultiRunSimulation.py ' + DirInput + FileNamePrefix + '.zip ' + ProjectIDToUse + ' 1 ' + str(RunningIndex) + ' ' + OverWriteFilesOrReconstructFromTraceback + ' ' + SimulationTimeOverride  + ' ' + PopulationRepetitionsOverride + ' ' + ModelIDToUse + ' ' + PopulationIDToUse + '   ' + ValueSeperation1 + ' ' + ValueSeperation2 + ' ' + ValueSeperation3 + ' ' + ValueSeperation4 + ' ' +  ValueSeperation5 + ' ' + ValueSeperation6 + '\n'
                ScriptToRun = ScriptToRun + 'mv ' + DirInput + FileNamePrefix + '_'+ str(RunningIndex) + '.zip' + ' ' + DirPhase1A + '\n'
                ScriptToRun = ScriptToRun + 'mv ' + DirInput + FileNamePrefix + '_'+ str(RunningIndex) + '_TraceBack.txt' + ' ' + DirPhase1A + '\n'
            else:
                ScriptToRun = ScriptToRun + 'echo "Phase1A disabled by request"\n'
            # Write the command that converts the zip file to results csv report
            if RunPhase1B:
                ScriptToRun = ScriptToRun + 'python MultiRunSimulationStatisticsAsCSV.py ' + DirPhase1A + FileNamePrefix + '_'+ str(RunningIndex) + '.zip 1 ' + ReportFilterFileName + ' ' + DirPhase1B + FileNamePrefix + '_'+ str(RunningIndex) + (' y' * ('NoZip' in DiskUsage)) + '\n'
            else:
                ScriptToRun = ScriptToRun + 'echo "Phase1B disabled by request"\n'
            print '#'*70
            print 'Running the following job command:'
            print JobEnv
            print 'With the script:'
            print ScriptToRun
            # Actual script To Run
            if DebugRun:
                (CommandStdOut, CommandStdErr) = ('Debug Mode','')
            else:
                (CommandStdOut, CommandStdErr) = subprocess.Popen(shlex.split(JobEnv), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(ScriptToRun)
                if CommandStdErr!='':
                    print '!'*10 + 'ERROR DETECTED' + '!'*10
                    print CommandStdErr
                    ErrorCount = ErrorCount + 1
            print 'Out:'
            print CommandStdOut

            


###########################################################
################### Extract statistics ####################
###########################################################

# Process Phase 2
# Loop through variations
if RunPhase2:
    for (Variation, VariationEnum) in sorted(SimulationVariationCodes.iteritems(), key = lambda Entry:Entry[1]):
        RunningIndex = (10**CodeDigitsForVariations) + VariationEnum
        JobEnv = 'qsub ' + Phase2Environemnt
        if 'NoLog' not in DiskUsage:
            JobEnv = JobEnv + ' -o ' + DirLog + 'OutCollect'+str(RunningIndex)+'.log'
        if 'NoErr' not in DiskUsage:
            JobEnv = JobEnv + ' -e ' + DirErr + 'OutCollect'+str(RunningIndex)+'.err'
        JobEnv = JobEnv + ' -N ' + JobName + 'V' + str(VariationEnum) + 'Collect'
        JobEnv = JobEnv + ' -hold_jid "' + JobName + 'V' + str(VariationEnum) + 'R*"'
        ScriptToRun = '#!/bin/bash\n'
        ScriptToRun = ScriptToRun + 'echo "Collecting Variation ' + str(VariationEnum) + '"\n'
        ScriptToRun = ScriptToRun + 'python MultiRunSimulationStatisticsAsCSV.py "' + DirPhase1B + FileNamePrefix + '_' + str(RunningIndex) + '[0-9]'*(CodeDigitsForRepetitions)+'.csv"' + ' None None ' + DirPhase2 + FileNamePrefix + '_' + str(RunningIndex) + (' y' * ('LessCSV' in DiskUsage)) + '\n'
        print '#'*70
        print 'Running the following job command:'
        print JobEnv
        print 'With the script:'
        print ScriptToRun
        # Actual script To Run
        # For each such project collect all the csv reports previously
        # calculated into csv statistics
        if DebugRun:
            (CommandStdOut, CommandStdErr) = ('Debug Mode','')
        else:
            (CommandStdOut, CommandStdErr) = subprocess.Popen(shlex.split(JobEnv), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(ScriptToRun)
            if CommandStdErr!='':
                print '!'*10 + 'ERROR DETECTED' + '!'*10
                print CommandStdErr
                ErrorCount = ErrorCount + 1
            else:
                if CommandStdOut[0:9] != 'Your job ':
                    # Normal response is "Your job # ("Name") was submitted"
                    print '!'*10 + 'POSSIBLE ERROR - NO SUBMITTED JOB DETECTED' + '!'*10
                    ErrorCount = ErrorCount + 1
        print 'Out:'
        print CommandStdOut

##### Calculate report and plots #####

print '#'*70
print '#'*20 + '  Creating Reports and Plots  ' + '#'*20


#Construct ReportStr

PlotStrList = []
ReportStr = ''
RunningIndexBase = (10**CodeDigitsForVariations)

TempFilePrefix = DirTemp + FileNamePrefix

# If no reference file is defined, the first file will be used to create the
# two first reference columns. Note that an error will be generated at the top
# of the thirs column to indicate no reference was provided by the user
if ReportReferenceFileName=='':
    ReportReferenceFileName = DirPhase2 + FileNamePrefix + "_" + str(RunningIndexBase) + "Mean.csv"
    UserReferenceFileExists = False
    ReportReferenceColumnTuple =''    
else:
    UserReferenceFileExists = True


ValueSeperation1,TitleSeperation1


def CalculateCompactProjectTitle():
    "Calcualte variation title by finding differences between components"
    TheTitle = (TitleStratifications+ ' ')*(len(Stratifications)>1) 
    TheTitle = TheTitle + (ProjectTitleToUse+ ' ')*(len(ProjectsToUse)>1)
    TheTitle = TheTitle + (ModelTitleToUse+ ' ')*(len(ModelsToUse)>1)
    TheTitle = TheTitle + (PopulationTitleToUse+ ' ')*(len(PopulationsToUse)>1)
    TheTitle = TheTitle + (TitleSeperation1+ ' ')*(len(OptionsSeperation1)>1)
    TheTitle = TheTitle + (TitleSeperation2+ ' ')*(len(OptionsSeperation2)>1)
    TheTitle = TheTitle + (TitleSeperation3+ ' ')*(len(OptionsSeperation3)>1)
    TheTitle = TheTitle + (TitleSeperation4+ ' ')*(len(OptionsSeperation4)>1)
    TheTitle = TheTitle + (TitleSeperation5+ ' ')*(len(OptionsSeperation5)>1)
    TheTitle = TheTitle + (TitleSeperation6+ ' ')*(len(OptionsSeperation6)>1)
    # Yet never leave the title complemetly empty
    if TheTitle == '':
        TheTitle = 'No Name'
    return TheTitle


# Each scenario can have its own order in the report. So the following code 
# can be replicated with different scenarios. However, this is not trivial
# for novices and therefore the if statement is Trivialy True. You can
# uncomment the if statement, and intend the block and create a replica with 
# your changes that will allow several scenarios to be served in the same file

if Scenario in [Scenario]:
    PlotTitles = []
    TitleList = []
    TitleSkip = []
    TheStr =  "[('"+ReportReferenceFileName+"','',''), ('"+ReportReferenceFileName+"','Start Step','End Step'), \n"
    TheStr = TheStr + UserReferenceFileExists*(""+str(ReportReferenceColumnTuple)+",\n")
    for (ProjectIDToUse,ProjectTitleToUse) in ProjectsToUse:
        for (ModelIDToUse,ModelTitleToUse) in ModelsToUse:
            TheStr = TheStr + "('"+ReportReferenceFileName+"','',''),\n"
            for (PopulationIDToUse,PopulationTitleToUse) in PopulationsToUse:
                for (ValueSeperation6,TitleSeperation6) in OptionsSeperation6:
                    for (ValueSeperation5,TitleSeperation5) in OptionsSeperation5:
                        for (ValueSeperation4,TitleSeperation4) in OptionsSeperation4:
                            for (ValueSeperation3,TitleSeperation3) in OptionsSeperation3:
                                for (ValueSeperation2,TitleSeperation2) in OptionsSeperation2:
                                    for (ValueSeperation1,TitleSeperation1) in OptionsSeperation1:
                                        for (ValueStratifications,TitleStratifications) in Stratifications:
                                            for (StartTime,EndTime) in SummaryReportTimes:
                                                TheTitle = CalculateCompactProjectTitle()
                                                try:
                                                    RunningIndex = RunningIndexBase + SimulationVariationCodes[(ProjectIDToUse, ModelIDToUse, PopulationIDToUse, ValueSeperation1, ValueSeperation2, ValueSeperation3, ValueSeperation4, ValueSeperation5, ValueSeperation6)]
                                                except KeyError:
                                                    TitleSkip.append(TheTitle)
                                                    continue
                                                TheStr = TheStr + "('" + DirPhase2 + FileNamePrefix + "_" + str(RunningIndex) + "Mean.csv','"+StartTime+"','"+EndTime+"','"+ValueStratifications+"','"+TheTitle+"'), \n"
    TheStr = TheStr + "('"+ReportReferenceFileName+"','','')"+UserReferenceFileExists*(","+str(ReportReferenceColumnTuple)) +" ] "
    if DebugRun>=2:
        print ' INFO: The report skipped the following combinatorial variations during creation: ' + str(set(TitleSkip))
    
    # create a report instructions file
    TempFile = open(TempFilePrefix+'_Temp.txt','w')
    TempFile.write(TheStr)
    TempFile.close()
    ReportStr = ReportStr + 'python AssembleReportCSV.py ' + TempFilePrefix + '_Temp.txt '+ DirPhase3 + FileNamePrefix + "_Out.csv\n"
    
    
    
    PlotTitles = []
    TitleSkip = []
    TheStr =  "[('"+ReportReferenceFileName+"','',''), ('"+ReportReferenceFileName+"','Start Step','End Step'), \n"
    for (ValueStratifications,TitleStratifications) in Stratifications:
        TheStr = TheStr + UserReferenceFileExists*(""+str(ReportReferenceColumnTuple)+",\n")
        TitleList = []
        for (ProjectIDToUse,ProjectTitleToUse) in ProjectsToUse:
            for (ModelIDToUse,ModelTitleToUse) in ModelsToUse:
                TheStr = TheStr + "('"+ReportReferenceFileName+"','',''),\n"
                for (PopulationIDToUse,PopulationTitleToUse) in PopulationsToUse:
                    for (ValueSeperation6,TitleSeperation6) in OptionsSeperation6:
                        for (ValueSeperation5,TitleSeperation5) in OptionsSeperation5:
                            for (ValueSeperation4,TitleSeperation4) in OptionsSeperation4:
                                for (ValueSeperation3,TitleSeperation3) in OptionsSeperation3:
                                    for (ValueSeperation2,TitleSeperation2) in OptionsSeperation2:
                                        for (ValueSeperation1,TitleSeperation1) in OptionsSeperation1:
                                            for (StartTime,EndTime) in [(str(Year),str(Year)) for Year in range(int(SimulationTimeOverride)+1)]:
                                                TheTitle = CalculateCompactProjectTitle()
                                                try:
                                                    RunningIndex = RunningIndexBase + SimulationVariationCodes[(ProjectIDToUse, ModelIDToUse, PopulationIDToUse, ValueSeperation1, ValueSeperation2, ValueSeperation3, ValueSeperation4, ValueSeperation5, ValueSeperation6)]
                                                except KeyError:
                                                    TitleSkip.append(TheTitle)
                                                    continue
                                                TheStr = TheStr + "('" + DirPhase2 + FileNamePrefix + "_" + str(RunningIndex) + "Mean.csv','"+StartTime+"','"+EndTime+"','"+ValueStratifications+"','"+TheTitle+"'), \n"
                                            if TheTitle not in TitleSkip: TitleList = TitleList + [TheTitle]
        PlotTitles = PlotTitles + [TitleList]
    TheStr = TheStr + "('"+ReportReferenceFileName+"','','')"+UserReferenceFileExists*(","+str(ReportReferenceColumnTuple)) +" ] "
    if DebugRun>=2:
        print ' INFO: The report skipped the following combinatorial variations during creation: ' + str(set(TitleSkip))
    
    # create a report instructions file
    TempFile = open(TempFilePrefix+'_Temp_Yearly.txt','w')
    TempFile.write(TheStr)
    TempFile.close()
    ReportStr = ReportStr + 'python AssembleReportCSV.py ' + TempFilePrefix + '_Temp_Yearly.txt '+ DirPhase3 + FileNamePrefix + "_Out_Yearly.csv\n"
    
    # Create the non stratified plots
    PlotInstructions = [PlotFilter, PlotTitles[0], PlotStyles]
    TempFile = open(TempFilePrefix+'_Temp_Yearly.plt','w')
    TempFile.write(str(PlotInstructions))
    TempFile.close()
    PlotStrList.append("python CreatePlotsFromCSV.py " + DirPhase3 + FileNamePrefix + "_Out_Yearly.csv " + DirPhase4 + FileNamePrefix + "_Out_Yearly.pdf " + TempFilePrefix + "_Temp_Yearly.plt\n")
    
    if len(Stratifications) >1:
        # Create the diabetic stratified plots
        PlotInstructions = [PlotFilter, PlotTitles[1] + PlotTitles[2], PlotStyles]
        TempFile = open(TempFilePrefix+'_Temp_Yearly_Strat.plt','w')
        TempFile.write(str(PlotInstructions))
        TempFile.close()
        PlotStrList.append("python CreatePlotsFromCSV.py " + DirPhase3 + FileNamePrefix + "_Out_Yearly.csv " + DirPhase4 + FileNamePrefix + "_Out_Yearly_Strat.pdf " + TempFilePrefix + "_Temp_Yearly_Strat.plt\n")
    
    
    # To Allow viewing also create graph for each population if there are a few of these
    if len(PopulationsToUse) > 1:
        for (PopulationEnum,(PopulationIDToUse,PopulationTitleToUse)) in enumerate(PopulationsToUse):
            # Isolate population Titles to show from the list by title
            PlotTitlesToUse = [Entry for Entry in PlotTitles[0] if ((PopulationTitleToUse+' ') in Entry)]
            # Create the non stratified plots
            PlotInstructions = [PlotFilter, PlotTitlesToUse, PlotStyles]
            TempFile = open(TempFilePrefix+'_Temp_Yearly_'+PopulationTitleToUse+'.plt','w')
            TempFile.write(str(PlotInstructions))
            TempFile.close()
            PlotStrList.append("python CreatePlotsFromCSV.py " + DirPhase3 + FileNamePrefix + "_Out_Yearly.csv " + DirPhase4 + FileNamePrefix + "_Out_Yearly_"+PopulationTitleToUse+".pdf " + TempFilePrefix + "_Temp_Yearly_"+PopulationTitleToUse+".plt\n")
    
            if len(Stratifications) >1:
                # Isolate population Titles to show from the list by title
                PlotTitlesToUse = [Entry for Entry in PlotTitles[1] + PlotTitles[2] if ((PopulationTitleToUse+' ') in Entry)]
                # Create the diabetic stratified plots
                PlotInstructions = [PlotFilter, PlotTitlesToUse, PlotStyles]
                TempFile = open(TempFilePrefix+'_Temp_Yearly_Strat_'+PopulationTitleToUse+'.plt','w')
                TempFile.write(str(PlotInstructions))
                TempFile.close()
                PlotStrList.append("python CreatePlotsFromCSV.py " + DirPhase3 + FileNamePrefix + "_Out_Yearly.csv " + DirPhase4 + FileNamePrefix + "_Out_Yearly_Strat_"+PopulationTitleToUse+".pdf " + TempFilePrefix + "_Temp_Yearly_Strat_"+PopulationTitleToUse+".plt\n")




# Process Phase 3
if RunPhase3:
    print '#'*70
    JobEnv = 'qsub ' + Phase3Environemnt
    if 'NoLog' not in DiskUsage:
        JobEnv = JobEnv + ' -o ' + DirLog + 'OutPhase3.log'
    if 'NoErr' not in DiskUsage:
        JobEnv = JobEnv + ' -e ' + DirErr + 'OutPhase3.err'
    JobEnv = JobEnv + ' -N ' + JobName + '_FinalRep'
    JobEnv = JobEnv + ' -hold_jid "' + JobName + 'V*"'
    
    ScriptToRun = '#!/bin/bash\n'
    ScriptToRun = ScriptToRun + 'echo "Final Report Collection"\n'
    ScriptToRun = ScriptToRun + ReportStr
    
    print '#'*70
    print 'Running the following job command:'
    print JobEnv
    print 'With the script:'
    print ScriptToRun
    # Actual script To Run
    # For each such project collect all the csv reports previously
    # calculated into csv statistics
    if DebugRun:
        (CommandStdOut, CommandStdErr) = ('Debug Mode','')
    else:
        (CommandStdOut, CommandStdErr) = subprocess.Popen(shlex.split(JobEnv), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(ScriptToRun)
        if CommandStdErr!='':
            print '!'*10 + 'ERROR DETECTED' + '!'*10
            print CommandStdErr
            ErrorCount = ErrorCount + 1
    print 'Out:'
    print CommandStdOut


# Process Phase 4
print '#'*70

ScriptList = []
if RunPhase4A:
    for ValidationQueryFile in FinalReportValidationQueries:
        # AnalyzeSimulationResults.py is not part of the core MIST distribution
        # It is intended for analysis of results. Replace this command with
        # your own processing mechanism.
        ScriptToRun = '#!/bin/bash\n'
        ScriptToRun = ScriptToRun + 'echo "Post Processing Final Report"\n'
        ScriptToRun = ScriptToRun + 'python AnalyzeSimulationResults.py ' + DirPhase3 + FileNamePrefix + '_Out.csv ' + ValidationQueryFile + ' ' + DirPhase4 + 'QueryOut_' + FileNamePrefix + '_' + ValidationQueryFile + '\n'
        ScriptList.append(ScriptToRun)
    
if RunPhase4B:
    for PlotStr in PlotStrList:
        ScriptToRun = '#!/bin/bash\n'
        ScriptToRun = ScriptToRun + 'echo "Post Processing Plots from Final Report"\n'
        ScriptToRun = ScriptToRun + PlotStr
        ScriptList.append(ScriptToRun)

for (ScriptEnum,ScriptToRun) in enumerate(ScriptList):
    JobEnv = 'qsub ' + Phase4Environemnt
    if 'NoLog' not in DiskUsage:
        JobEnv = JobEnv + ' -o ' + DirLog + ('OutPhase4_%0.'+str(int(DB.Log10(len(ScriptList)))+1)+'i.log')%(ScriptEnum)
    if 'NoErr' not in DiskUsage:
        JobEnv = JobEnv + ' -e ' + DirErr + ('OutPhase4_%0.'+str(int(DB.Log10(len(ScriptList)))+1)+'i.err')%(ScriptEnum)
    JobEnv = JobEnv + ' -N ' + JobName + '_PostFinalRep'
    JobEnv = JobEnv + ' -hold_jid "' + JobName + '_FinalRep"'

    print '#'*70
    print 'Running the following job command:'
    print JobEnv
    print 'With the script:'
    print ScriptToRun
    # Actual script To Run
    # For each such project collect all the csv reports previously
    # calculated into csv statistics
    if DebugRun:
        (CommandStdOut, CommandStdErr) = ('Debug Mode','')
    else:
        (CommandStdOut, CommandStdErr) = subprocess.Popen(shlex.split(JobEnv), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(ScriptToRun)
        if CommandStdErr!='':
            print '!'*10 + 'ERROR DETECTED' + '!'*10
            print CommandStdErr
            ErrorCount = ErrorCount + 1
    print 'Out:'
    print CommandStdOut




print '#'*70
print 'Scenario is: ' + Scenario
print 'Total Number of Variations is %i' % len(SimulationVariationCodes)
print 'Total Number of Repetitions is %i' % Repetitions
CountVec = (len(SimulationVariationCodes)*Repetitions, len(SimulationVariationCodes), 1, len(ScriptList))
print 'Total Number of Jobs is %i = %i + %i + %i + %i for phases 1,2,3,4' %( (sum(CountVec),) + CountVec )
print '#'*70

if ErrorCount > 0:
    print '!'*70
    print '!'*70
    print '!'*70
    print ' '*20 + str(ErrorCount) + ' ERRORS DETECTED IN SCRIPT' 
    print '!'*70
    print '!'*70
    print '!'*70
else:
    print 'OK '*20
    print 'OK '*20
    print ' '*20 + 'SCRIPT LAUNCHED OK' 
    print 'OK '*20
    print 'OK '*20
    
