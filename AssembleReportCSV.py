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
# This file was originally missing a copyright statement yet was part of the
# IEST system with a GPL license.

import DataDef as DB
import sys


def AssembleReport(AssemblySequence, OutputFileName):
    """ Assmbles a CSV report from the AssemblySequence specified """
    # The assmebly sequence is a list of tuples of the form:
    # (Filename, Key1, Key2, Stratification, Title ) where Key1 and Key2
    # distinguish columns from each other by looking at the first two numbers
    # (rows) in each column
    # if the proper Key is found in the FileName, then the entire column is
    # extracted and placed as a columns in the final report
    # Stratification is optional and if provided and not empty, it will be used
    # to select only the stratification defined by adding it to the key.
    # Title is optional and if provided will appear on top of the file name
    # to describe the newly added column in words
    # Currently, rows are assumed to match between files. However, this
    # may change in the future
    OutputReportTransposed = []
    for Entry in AssemblySequence:
        print 'Processing ' + str(Entry)
        if len(Entry) == 3:
            Filename, Key1, Key2 = Entry
            Stratification = ''
            Title = ''
        elif len(Entry) == 4:
            Filename, Key1, Key2, Stratification = Entry
            Title = ''
        else:
            Filename, Key1, Key2, Stratification, Title = Entry
        Key1, Key2 = str(Key1), str(Key2)
        try:
            (DataColumnsDummy,Data) = DB.ImportDataFromCSV(FileName = Filename, ImportColumnNames = False, ConvertTextToProperDataType = False, TextCellsAllowed = False)
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            print 'CSV Assembly Warning: CSV file did not read. Here are details about the error: ' + str(ExceptValue)
            # Reset the data and continue
            Data =[]
        NumberOfRows = len(Data)
        ExtractedColumn = None
        CurrentStratification = ''
        if NumberOfRows == 0:
            OutputReportTransposed.append([Title, '***Err File:' + Filename + ' ***'])
        else:
            NumberOfColumns = max(map(len,Data))
            TransposeData = map(None,*Data)
            for ColumnNum in range(NumberOfColumns):
                # search for column with this key
                Column = TransposeData[ColumnNum]
                # detect the stratification columns that seperate the
                # data chunks. The fourth column - index 3 holds this text
                # since the first 3 entries are project information
                if Column[3].startswith(DB.ReportStratificationHeader):
                    # record the new stratification key and continue
                    CurrentStratification = Column[3]
                else:
                    if Stratification == '' or Stratification == CurrentStratification:
                        # The fourth-sixth column - indices 3-5 hold the keys
                        # since the first 3 entries are project information
                        if Column[3:5] == (Key1,Key2):
                            PreviousExtractedColumn = ExtractedColumn
                            ExtractedColumn = [Title, Filename, Stratification] + list(Column)
                            # since the same time span can repeat itself
                            # several times in a report and we want to collect
                            # only the first, so collect only new columns and
                            # discard duplicates. If Stratification=='' only 
                            # the first reported strata is extracted.
                            if ExtractedColumn != PreviousExtractedColumn:
                                print 'Column Collected'
                                OutputReportTransposed.append(ExtractedColumn)
                            else:
                                print 'Duplicate Column Ignored'
            if ExtractedColumn == None:
                OutputReportTransposed.append([Title, Filename, Stratification] + ['***Err Key1: ' + Key1 + ' ***', '***Err Key2: ' + Key2 + ' ***' ])
    OutputReport = map(None,*OutputReportTransposed)
    DB.ExportDataToCSV(OutputFileName, OutputReport)



if __name__ == "__main__":
    # Redirect stdout to File if needed
    if len(sys.argv) == 3:
        AssemblySequenceCandidate = sys.argv[1].strip()
        InputIsSequence = True
        if AssemblySequenceCandidate.strip()[0]=='[' and AssemblySequenceCandidate.strip()[-1]== ']':
            # This seems to be a valid python list this means the user provided
            # the sequence itself
            AssemblySequence = eval(AssemblySequenceCandidate, DB.EmptyEvalDict)
        else:
            # if this is not a list, then this means the user provided
            # a file
            TheSequenceFile = open(AssemblySequenceCandidate,'r')
            AssemblySequenceText = TheSequenceFile.read()
            TheSequenceFile.close()
            AssemblySequence = eval(AssemblySequenceText, DB.EmptyEvalDict)
        OutputFileName = sys.argv[2]
        AssembleReport(AssemblySequence,OutputFileName)
    else:
        print 'Info: this script can be invoked from command line using the following syntax:'
        print ' AssembleReportCSV.py AssemblySequence OutputFileName'
        print '     AssemblySequence holds the assembly sequence by providing a actual sequence'
        print '     string enclosed in []. If not enclosed in brackets the string holds a file'
        print '     name that holds the sequence string. The assembly sequence is in the form'
        print '     [ ColumnTuple1, ColumnTuple2, ...] where:'
        print '         ColumnTuple# = (Filename, Key1, Key2, Stratification, Title)'
        print '         where Stratification and Title are optional'
        print '         OutputFileName = a name for the output CSV file' 
        print ' The script assembles a single report from several input CSV files according'      
        print ' to the tuples. This is useful for combining reports from several scenarios.'
