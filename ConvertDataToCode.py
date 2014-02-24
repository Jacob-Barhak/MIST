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

# This module contains a utility that converts a file with data back to code
# that can regenerate the data base.
# This utility is deprecated and may be removed in the future

import DataDef as DB
import sys

if __name__ == "__main__":
    # Redirect stdout to File if needed
    (sys.stdout, BackupOfOriginal) = DB.RedirectOutputToValidFile(sys.stdout)
    # If there are command line arguments passed, use them rather than ask
    # questions from the user
    RegenerationScriptName = "TheGeneratedDataCode.py"
    KnownNumberOfErrors = 0
    ConvertResultsStr = 'No'
    SavedModelFileName = None
    # If there are command line arguments passed, use them rather than ask
    # questions from the user
    if len(sys.argv) > 1:
        InputFileName = sys.argv[1]
        if len(sys.argv) > 2:
            RegenerationScriptName = sys.argv[2]
        if len(sys.argv) > 3:
            KnownNumberOfErrors = int(sys.argv[3])
        if len(sys.argv) > 4:
            ConvertResultsStr = sys.argv[4]
        if len(sys.argv) > 5:
            SavedModelFileNameStr = sys.argv[5]
    else:
        print 'Info: this script can be invoked from command line using the following syntax:'
        print ' ConvertDataToCode.py FileName [ScriptName [ErrCount [DoResults [SaveFile]]]]'
        print ' FileName is the input data definitions file name '
        print ' ScriptName is the output python regenerating script name '
        print ' ErrCount should normally be kept at zero which is the default '
        print ' if DoResults is yes or y (not default) results will be also converted '
        print ' SaveFile defines the name the script uses to save the model file '
        print ''        
        print ' The script is used to convert MIST zip archives into code that can be'
        print ' manipulated by a programmer. This is useful when trying to make changes'
        print ' on data that has many dependencies.'
        print ''        
        InputFileName = raw_input( 'Please enter the data file name to convert to code : ')
        RegenerationScriptNameStr = raw_input( 'Please enter the code file name to be generated, or press enter to select the default of "TheGeneratedDataCode.py" : ')
        if RegenerationScriptNameStr.strip() != '':
            RegenerationScriptName = RegenerationScriptNameStr
        KnownNumberOfErrorsStr = raw_input( 'Please enter the number of errors to be tolerated while converting or press enter to select the default of 0 : ')
        if KnownNumberOfErrorsStr.strip() != '':
            KnownNumberOfErrors = int(KnownNumberOfErrorsStr)
        ConvertResultsStr = raw_input( 'Please enter YES or Y if you wish to convert the results as well as other data structures: ')
        SavedModelFileNameStr = raw_input( 'Please enter the save model file name to use in the script to save the file. or press enter to select the default using the script with "_out.zip" suffix : ')
        if SavedModelFileNameStr.strip() != '':
            SavedModelFileName = SavedModelFileNameStr
    ConvertResults = ConvertResultsStr.strip().lower() in ['yes','y']
    DB.ReconstructDataFileAndCheckCompatibility(InputFileName, JustCheckCompatibility = False, RegenerationScriptName = RegenerationScriptName, ConvertResults = ConvertResults, KnownNumberOfErrors = KnownNumberOfErrors, CatchError = False, OutputModelFileName = SavedModelFileName)
    # Redirect stdout back if needed
    sys.stdout = DB.RedirectOutputBackwards(sys.stdout, BackupOfOriginal)

