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

def GenerateMultiRunSimulationStatistics(FilePatternForFilesWithSimulationResults, SimulationResultID = None, FormatOptions = None, StatisticsFileNamePrefix = None, DeleteSourceFilesUponSuccess = False):
    """ Generate a report for multiple result files """
    # reset output
    TransposedResults = None
    ListOfDataFilesWithResultsUnfiltered = sorted(DB.FilePatternMatchOptimizedForNFS(FilePatternForFilesWithSimulationResults))
    # Filter out files with a wrong extension as these may be from a previous
    # run of this script
    ListOfDataFilesWithResults = filter(lambda Entry: DB.os.path.splitext(Entry)[1].lower()=='.zip', ListOfDataFilesWithResultsUnfiltered)
    # find the common base name for this batch
    ListOfStatisticsFiles = filter(lambda Entry: DB.os.path.splitext(Entry)[1].lower()=='.csv', ListOfDataFilesWithResultsUnfiltered)
    # Check that the file pattern represents files
    if len(ListOfDataFilesWithResults)==0 and len(ListOfStatisticsFiles)==0:
        raise ValueError, 'CSV Statistics Generation Error: The file Pattern ' + FilePatternForFilesWithSimulationResults +  ' did not match any file - please make sure the pattern is valid'
    if len(ListOfDataFilesWithResults)!=0 and len(ListOfStatisticsFiles)!=0:
        raise ValueError, "CSV Statistics Generation Error: Both csv files and zip files were specified by the pattern, please specify only one of these file types"
    # Traverse zip files to create CSV report files
    for FileName in ListOfDataFilesWithResults:
        DB.MessageToUser(' Processing the file ' + FileName)
        try:
            DB.LoadAllData(FileName)
            # If no simulation results are defined, then select the first simulation
            # result. Note that once it is set, all files will be accessed with
            # the same ID.
            if SimulationResultID == None:
                SimulationResultID = sorted(DB.SimulationResults.keys())[0]
            # Create the csv file name by changing the zip file name extension
            if StatisticsFileNamePrefix == None:
                (FileNameNoExtension , FileNameOnlyExtension) = DB.os.path.splitext(FileName)
            else:
                FileNameNoExtension = StatisticsFileNamePrefix
            FileNameToExprotCSV = FileNameNoExtension + '.csv'
            # Generate the report
            TransposedResults = DB.SimulationResults[SimulationResultID].CreateReportAsCSV(FileNameToExprotCSV, FormatOptions)
            # if reached this point, it is safe to remove the source data
            if DeleteSourceFilesUponSuccess:
                DB.MessageToUser('Upon User Request Deleting Data Source File: ' + FileName)
                DB.os.remove(FileName)
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            print "CSV Statistics Generation Warning: Failed to produce CSV report for the file " + str(FileName) + " Here are details about the error:  "  + str(ExceptValue)
        # Accumulate the files to the CSV file list
        ListOfStatisticsFiles = ListOfStatisticsFiles + [FileNameToExprotCSV]
    # If there are multiple csv files or a single csv file with statistics
    if len(ListOfStatisticsFiles)>1 or (len(ListOfStatisticsFiles)==1 and len(ListOfDataFilesWithResults)==0):
        if StatisticsFileNamePrefix == None:
            # find the common base name for this batch
            FileNameCommonPrefix = DB.os.path.commonprefix(ListOfStatisticsFiles)
        else:
            FileNameCommonPrefix = StatisticsFileNamePrefix
        (TransposeMeanArray, TransposeSTDArray, TransposeMedianArray, TransposeMinArray, TransposeMaxArray) = DB.CalculateStatisticsForCSV(ListOfStatisticsFiles, FileNameCommonPrefix)
        # if reached this point, it is safe to remove the source data
        if DeleteSourceFilesUponSuccess:
            for StatisticsFile in ListOfStatisticsFiles:
                DB.MessageToUser('Upon User Request Deleting Statistics Source File: ' + StatisticsFile)
                DB.os.remove(StatisticsFile)
    else:
        # if there was only one file transpose it - do not generate a file
        TransposeMeanArray=TransposedResults
        TransposeSTDArray=None
        TransposeMedianArray=TransposedResults
        TransposeMinArray=TransposedResults
        TransposeMaxArray=TransposedResults       
        
    return (TransposeMeanArray, TransposeSTDArray, TransposeMedianArray, TransposeMinArray, TransposeMaxArray)

 

if __name__ == "__main__":
    # Redirect stdout to File if needed
    (sys.stdout, BackupOfOriginal) = DB.RedirectOutputToValidFile(sys.stdout)
    SimulationResultID = None
    FormatOptions = None
    StatisticsFileNamePrefix = None
    ResultIDToProcessStr = ''
    ReportParameterFileNameStr = ''
    StatisticsFileNamePrefixStr = ''
    DeleteSourceFilesUponSuccessStr = ''
    if len(sys.argv) > 1:
        FilePatternForFilesWithSimulationResults = sys.argv[1]
        if len(sys.argv) > 2:
            ResultIDToProcessStr = sys.argv[2]
        if len(sys.argv) > 3:
            ReportParameterFileNameStr = sys.argv[3]
        if len(sys.argv) > 4:
            StatisticsFileNamePrefixStr = sys.argv[4]
        if len(sys.argv) > 5:
            DeleteSourceFilesUponSuccessStr = sys.argv[5]
    else:
        print 'Info: this script can be invoked from command line using the following syntax:'
        print ' MultiRunExportStatisticsAsCSV.py FilePattern [ResID OptFile OutPrefix DelSrc]'
        print ' The default ResID is none meaning the first result'
        print ' OptFile holds report options in the form option \\n Value \\n'
        print ' OutPrefix holds a prefix for the final statistics files'
        print ' if DelSrc is y then upon success the source zip/csv files are removed'
        print ' Results are determined by FilePattern:'
        print ' - a single zip file: generate only a single csv report file'
        print ' - multiple zip file: generate csv report and statistics files'
        print ' - multiple csv report files: generate csv statistics files'
        print ' For multiple csv file use none to ignore ResultsID and OptFile'
        print ''
        print 'This script is useful for extracting a report from a MIST zip archive.' 
        print 'This is very useful for multiple such files created by parallel simulations'
        print ''
        # Ask user to provide file names to merge
        FilePatternForFilesWithSimulationResults = raw_input( 'Please enter the data file name template to process, e.g. DataFile*.zip : ' )
        # Ask about the simulation result of interest
        ResultIDToProcessStr = raw_input( 'Please enter Result ID to be considered. Leave blank to select the first ID by default: ' )
        ReportParameterFileNameStr = raw_input( 'Enter Report Parameters File Name - leave blank to skip: ' )
        StatisticsFileNamePrefixStr = raw_input( 'Enter Statistics Output Prefix File Name - leave blank to skip: ' )
        DeleteSourceFilesUponSuccessStr = raw_input( 'Enter Y to delete the source file upon report creation - leave blank to skip: ' )
    # Now translate the parameters
    if ResultIDToProcessStr.strip().lower() not in ('','none'):
        SimulationResultID = int(ResultIDToProcessStr)
    if ReportParameterFileNameStr.strip().lower() not in ('','none'):
        FormatOptions = DB.LoadOptionList(ReportParameterFileNameStr)
    if StatisticsFileNamePrefixStr.strip().lower() not in ('','none'):
        StatisticsFileNamePrefix = StatisticsFileNamePrefixStr
    DeleteSourceFilesUponSuccess = DeleteSourceFilesUponSuccessStr.strip().lower()[:1]=='y'
    ReportText = GenerateMultiRunSimulationStatistics(FilePatternForFilesWithSimulationResults, SimulationResultID, FormatOptions, StatisticsFileNamePrefix, DeleteSourceFilesUponSuccess)
    # Redirect stdout back if needed
    sys.stdout = DB.RedirectOutputBackwards(sys.stdout, BackupOfOriginal)
