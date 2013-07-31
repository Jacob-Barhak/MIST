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
import copy
import sys

def GenerateCombinedReport(ListOfDataBasesWithResults, SimulationResultIDsToCombine = None, FormatOptions = None):
    """ Generate a combined report for specified result file names """
    # Generate default options if do not exist yet
    TotalIndent = DB.HandleOption('TotalIndent', FormatOptions,'')
    IndentAtom = DB.HandleOption('IndentAtom', FormatOptions,'  ')
    FieldHeader = DB.HandleOption('FieldHeader', FormatOptions,True)
    LineDelimiter = DB.HandleOption('LineDelimiter', FormatOptions,'\n')
    ShowHidden = DB.HandleOption('ShowHidden', FormatOptions,False)
    DetailLevel = DB.HandleOption('DetailLevel', FormatOptions, 0)
    ReportHeader = DB.HandleOption('ReportHeader', FormatOptions, None)
    # Construct the report header
    ConstructReportHeader = (ReportHeader == None)
    if ConstructReportHeader:
        ReportHeader = TotalIndent + 'Combined Report incorporating the following Result Sets:' + LineDelimiter
    # Reset the summary accumulator
    OldPreCalculatedResults = None 
    # Traverse all the files
    for FileName in ListOfDataBasesWithResults:
        if ConstructReportHeader:
            ReportHeader = ReportHeader + TotalIndent + FieldHeader*'File Name: ' + str(FileName) + LineDelimiter
        # Load the data 
        DB.LoadAllData(FileName)
        # defined the simulation result sets of interest. If none are defined,
        # then merge all simulation results
        if SimulationResultIDsToCombine == None:
            SimulationResultIDList = DB.SimulationResults.keys()
        else:
            SimulationResultIDList = SimulationResultIDsToCombine
        # Traverse all simulation result sets of interest
        for SimulationResultID in SimulationResultIDList:
            SimulationResultInFocus = DB.SimulationResults[SimulationResultID]
            if ConstructReportHeader:
                ReportHeader = ReportHeader + TotalIndent + IndentAtom + FieldHeader*'Results ID: ' + str(SimulationResultInFocus.ID) + LineDelimiter
                ReportHeader = ReportHeader + TotalIndent + IndentAtom + IndentAtom + FieldHeader*'Created On: ' + str(SimulationResultInFocus.CreatedOn) + LineDelimiter
                if ShowHidden:
                    ReportHeader = ReportHeader + TotalIndent + IndentAtom + FieldHeader * 'ProjectID: ' + str(SimulationResultInFocus.ProjectID) + LineDelimiter
                if DetailLevel in [0,1]:
                    ReportHeader = ReportHeader + TotalIndent + IndentAtom + FieldHeader * 'For Project: ' + str(DB.Projects[SimulationResultInFocus.ProjectID].Name) + LineDelimiter
                else:
                    # Print details project information only if the amount of
                    # detail requested is above 1
                    RevisedFormatOptions = DB.HandleOption('TotalIndent', FormatOptions, TotalIndent + IndentAtom, True)
                    RevisedFormatOptions = DB.HandleOption('DetailLevel', RevisedFormatOptions, DetailLevel-1, True)
                    ReportHeader = ReportHeader + DB.Projects[SimulationResultInFocus.ProjectID].GenerateReport(RevisedFormatOptions)
            # For each such simulation result calculate summary values
            PreCalculatedResults = SimulationResultInFocus.ResolveReportDataAndOptions(FormatOptions = FormatOptions, UseOnlyPreviousResults = False)
            # feed these results back into the report options
            FormatOptions = DB.HandleOption('PreCalculatedResults', FormatOptions, PreCalculatedResults, True)
            # Make sure that all the calculations are the same for all
            # reports previously made - except from the last value
            if OldPreCalculatedResults != None:
                # Ignore the first iteration
                # now check that everything except from pre-calculated results 
                # and new results is the same.
                # Since ResolveReportDataAndOptions reports old precalcualted
                # results in index 14 of the vector, then ignore this position
                # when comparing options. Also treat position 10 in the vector
                # specially since it will return a different stratification 
                # table class even if the table is the same or None in case of
                # no stratification. 
                # Also the last two elements in the vector should be different
                # so comparing them does not make sense
                # Here is the vector of elements compared:
                #0 = TotalIndent
                #1 = IndentAtom
                #2 = ColumnSpacing
                #3 = FieldHeader
                #4 = LineDelimiter
                #5 = SectionSeparator
                #6 = ShowHidden
                #7 = DetailLevel
                #8 = BlankColumnsJoinedInData
                #9 = ColumnNumberFormat
                #10 = StratifyBy                *** This will be different
                #11 = ReportHeader
                #12 = ReportFooter
                #13 = ColumnFilter
                #14 = PreCalculatedResults      *** This will be different
                #15 = DataColumnsIndicesToShow
                #16 = ColumnTitles
                #17 = CalculationMethods
                #18 = OriginalCalculationMethods
                #19 = DataColumnsWithBlank
                #20 = BlankColumnIndex
                #21 = CalculationTitlesPerColumns
                #22 = MaxTime
                #23 = StartAtYearZero
                #24 = SummaryIntervals
                #25 = TimeInterval
                #26 = StratifyMaxCount
                #27 = StratificationColumnIndices
                #28 = Summaries                      *** This will be different
                #29 = SummariesBaseForNextResultBatch*** This will be different                    
                    
                if PreCalculatedResults[:10] != OldPreCalculatedResults [:10] or ( (PreCalculatedResults[10] and PreCalculatedResults[10].Description()) != (OldPreCalculatedResults[10] and OldPreCalculatedResults[10].Description())) or PreCalculatedResults[11:14] != OldPreCalculatedResults [11:14] or PreCalculatedResults[15:-2] != OldPreCalculatedResults [15:-2]:
                    raise ValueError, 'Results for the file "'+str(FileName)+'" and result set ' + str(SimulationResultID) + ' is not compatible with previous simulation results processed'
            OldPreCalculatedResults = copy.deepcopy(PreCalculatedResults[:])
    if ConstructReportHeader:
        ReportHeader = ReportHeader + TotalIndent + FieldHeader * 'Combined Summary Statistics:' + LineDelimiter
    # Now it is possible to actually generate the report
    # Before this, the PreCalculatedResults in the FromatOptions
    FormatOptions = DB.HandleOption('ReportHeader', FormatOptions, ReportHeader, True)
    FormatOptions = DB.HandleOption('PreCalculatedResults', FormatOptions, PreCalculatedResults, True)
    ReportText = SimulationResultInFocus.GenerateReport(FormatOptions)
    return ReportText        

if __name__ == "__main__":
    # Redirect stdout to File if needed
    (sys.stdout, BackupOfOriginal) = DB.RedirectOutputToValidFile(sys.stdout)
    # Ask user to provide file names to merge
    ListOfDataBasesWithResults = []
    # if command line argument is provided, switch stdin with it
    FileToUse = None
    if len(sys.argv) > 1:
        BackupStdIn = sys.stdin
        FileToUse = open(sys.argv[1], 'r')
        sys.stdin = FileToUse
    else:
        print 'Info: this script can be invoked from command line using the following'
        print '      redirection scheme:'
        print ' MultiRunCombinedReport.py InputParametersFile'
        print ' Note that the InputParametersFile should provide data in the following order'
        print ' 1) A list of data file names, each is a separate line:'
        print '     InputFileName1'
        print '     InputFileName2'
        print '     ...'
        print '     An empty new line to end this list'
        print ' 2) A possibly empty list of ResultsID numbers, each is a separate line:'
        print '     ResultsID1'
        print '     ResultsID2'
        print '     ...'
        print '     An empty new line to end this list'
        print ' 3) A possibly empty list of Format options to change in the form:'
        print '     FormatOptionName1 '
        print '     Value1 '
        print '     FormatOptionName2 '
        print '     Value2 '
        print '     ...'
        print '     An empty new line to end this list'
        print ' 4) Output Report FileName (default is Report.txt - if left empty)'
        print ''
        print 'This script can be used in the rare case where simulations were held'
        print 'separately and information needs to be merged between several existing'
        print 'MIST databases with results'
        print ''
    # now analyze the input
    while 1:
        InputFileName = raw_input( 'Please enter a data file name with results. Leave blank to end the file list: ' )
        if InputFileName.strip() == '':
            break
        else:
            ListOfDataBasesWithResults = ListOfDataBasesWithResults + [InputFileName]
    SimulationResultIDsToCombine = []
    while 1:
        ResultIDToProcessStr = raw_input( 'Please enter Result ID to be considered - leave blank to end list. (If no result IDs are defined in the list, all results are considered by default): ' )
        if ResultIDToProcessStr.strip() == '':
            break
        else:
            SimulationResultIDsToCombine = SimulationResultIDsToCombine + [int(ResultIDToProcessStr)]
    if SimulationResultIDsToCombine == []:
        SimulationResultIDsToCombine = None
    FormatOptions = None
    while 1:
        FormatOptionNameStr = raw_input( 'Enter Format Option Name for change - leave blank to skip: ' )
        if FormatOptionNameStr.strip() == '':
            break
        else:
            FormatOptionsValueStr = raw_input( 'Enter Value for the Format Option as a Python Expression:' )
            FormatOptionValue = eval(FormatOptionsValueStr, DB.EmptyEvalDict)
            FormatOptions = DB.HandleOption(FormatOptionNameStr, FormatOptions, FormatOptionValue, True)
    OutputReportFileName = raw_input( 'Enter the report output file name or leave blank for the default (Report.txt): ' )
    if OutputReportFileName.strip() == '':
        OutputReportFileName = 'Report.txt'
    # Restore stdin
    if FileToUse != None:
        sys.stdin = BackupStdIn
        FileToUse.close()
    # Create the report
    ReportText = GenerateCombinedReport(ListOfDataBasesWithResults, SimulationResultIDsToCombine, FormatOptions)
    # Write to file
    File = open(OutputReportFileName,'w')
    File.write(ReportText)
    File.close()
    # Redirect stdout back if needed
    sys.stdout = DB.RedirectOutputBackwards(sys.stdout, BackupOfOriginal)
