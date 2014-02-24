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

def MultipleExportAsCSV(FilePatternForFilesWithSimulationResults, SimulationResultID = None, ColumnsToExport = '' ):
    """ Generate a CSV file from multiple result files """

    ListOfDataFilesWithResultsUnfiltered = DB.FilePatternMatchOptimizedForNFS(FilePatternForFilesWithSimulationResults)
    # Filter out files with a wrong extension as these may be from a previous
    # run of this script
    ListOfDataFilesWithResults = filter(lambda Entry: DB.os.path.splitext(Entry)[1].lower()!='.csv', ListOfDataFilesWithResultsUnfiltered)
    # Check that the file pattern represents files
    if len(ListOfDataFilesWithResults)==0:
        raise ValueError, 'The file Pattern ' + FilePatternForFilesWithSimulationResults +  ' did not match any file - please make sure the pattern is valid'    
    # Traverse all the files
    for FileName in ListOfDataFilesWithResults:
        print ' Processing the file ' + FileName
        DB.LoadAllData(FileName)
        # If no simulation results are defined, then select the first simulation
        # result. Note that once it is set, all files will be accessed with
        # the same ID.
        if SimulationResultID == None:
            SimulationResultID = sorted(DB.SimulationResults.keys())[0]
        # Generate the file names
        SimulationResultInFocus = DB.SimulationResults[SimulationResultID]
        (FileNameBase,FileNameExt) = DB.os.path.splitext(FileName)
        FileNameToUse = FileNameBase + 'Results.csv'

        if ColumnsToExport.strip() == '':
            SimulationResultInFocus.ExportAsCSV(FileNameToUse)
        else:
            # remove white spaces
            ColumnNames = ColumnsToExport.replace(' ','').replace('\t','').split(',')
            ColumnIndices = [ SimulationResultInFocus.DataColumns.index(ColumnName) for ColumnName in ColumnNames ]
            NewData = [ColumnNames]
            for DataRow in SimulationResultInFocus.Data:
                NewRow = [ DataRow[ColumnIndex] for ColumnIndex in ColumnIndices]
                NewData = NewData + [NewRow]
            # Note that column names are already embeded in the data
            SimulationResultInFocus.ExportAsCSV(FileName = FileNameToUse, DataToExport = NewData, ExportTitles = False)
    return 

 
if __name__ == "__main__":
    # Redirect stdout to File if needed
    (sys.stdout, BackupOfOriginal) = DB.RedirectOutputToValidFile(sys.stdout)
    SimulationResultID = None
    SimulationResultID = None
    if len(sys.argv) > 1:
        FilePatternForFilesWithSimulationResults = sys.argv[1]
        ResultIDToProcessStr = sys.argv[2]
        ColumnsToExport = ', '.join(sys.argv[3:])
    else:
        print 'Info: this script can be invoked from command line using the following syntax:'
        print ' MultiRunExportResultsAsCSV.py FileNamePattern ResultsID ColumnName [...]'
        print ' Note that at least 1 ColumnName is required, more are possible '
        print ''      
        # Ask user to provide file names to merge
        FilePatternForFilesWithSimulationResults = raw_input( 'Please enter the data file name template to process, e.g. DataFile*.zip : ' )
        # Ask about the simulation result of interest
        ResultIDToProcessStr = raw_input( 'Please enter Result ID to be considered. Leave blank to select the first ID by default: ' )
        ColumnsToExport = raw_input( 'Enter column names of interest separated by commas or leave blank for all columns: ' )
    if ResultIDToProcessStr.strip() != '':
        SimulationResultID = int(ResultIDToProcessStr)        
    ReportText = MultipleExportAsCSV(FilePatternForFilesWithSimulationResults, SimulationResultID, ColumnsToExport)
    # Redirect stdout back if needed
    sys.stdout = DB.RedirectOutputBackwards(sys.stdout, BackupOfOriginal)


