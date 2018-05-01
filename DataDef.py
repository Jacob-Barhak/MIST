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


# This means that throughout the program the division operator will be treated
# as float division.
from __future__ import division

# Import these libraries
import datetime
import re
import math
import os
import sys
import glob
import pickle
import zipfile
import parser
import StringIO
import tokenize
import csv
import types
import copy
import string
import tempfile
import shutil

if sys.version_info[0:2]<(2,7):
    raise ValueError, 'System Initialization Error: The python version installed on this system does not meet the current version requirement of at least python version 2.6. Please install Python 2.7 or above and associated versions of the supporting libraries that correspond to this python version.'

SystemSupportsProcesses = sys.version_info[0:2]!=(2,5) and sys.platform != 'win32'
if SystemSupportsProcesses:
    import multiprocessing

import numpy
import scipy.stats
import inspyred

# Since used by generated scripts, this generates a warning to remove in Spyder
RemoveWarningNotification = [scipy.stats == None, inspyred == None]

# update the module names        
LoadedModuleNames = dir()

# Define the version of the data definitions file
# The string at the end will allow the system to distinguish between
# different revisions of a similar data structure than may or may not be
# compatible with each other. It is the responsibility of the code to
# check what code versions and revisions are compatible with it.
Version = (0,92,3,0,'MIST')

# DEBUG variables
# DebugPrints options are ['Table','TBD','Matrix', 'ExprParse','ExprConstruct', 'PrepareSimulation', 'Load' , 'MultiProcess', 'CSV', 'TempDir']
DebugPrints = []
MyDebugVar = {}
MessagesTBD = []

# First, some useful constants
FloatCompareTolerance = 1e-13 # Tolerance for comparing some floats for equality
Inf = float('inf')    # May be replaced by numpy later on
NaN = float('nan')    # May be replaced by numpy later on
inf = Inf    # Duality needed to support both upper and lower case versions
nan = NaN    # Duality needed to support both upper and lower case versions
InitTime = datetime.datetime(datetime.MINYEAR,1,1)
LowerCaseAlphabet = string.ascii_lowercase
UpperCaseAlphabet = string.ascii_uppercase
NumericCharacters = string.digits
AlphabetNoNumeric = LowerCaseAlphabet + UpperCaseAlphabet
AlphabetAndNumeric = AlphabetNoNumeric + NumericCharacters
ParamTextMatchPattern = '^[' + AlphabetNoNumeric + ']\w*$'
ParamUnderscoreAllowedTextMatchPattern = '^[' + AlphabetNoNumeric + '_]\w*$'
WhiteSpaces = string.whitespace

PythonSuffix = '.py'
TextSuffix = '.txt'
TempSuffix = '.tmp'
DefaultTempPathName = 'Temp'
DefaultTemporaryFileNamePrefix = 'Temp'
DefaultSimulationScriptFileNamePrefix = 'Sim'
DefaultSimulationOutputFileNamePrefix = 'SimOut'
DefaultGenerationScriptFileNamePrefix = 'Gen'
DefaultGenerationOutputFileNamePrefix = 'GenOut'
DefaultRandomStateFileNamePrefix = 'Rand'
DefaultFullResultsOutputFileName = 'SimulationResultsFull.csv'
DefaultFinalResultsOutputFileName = 'SimulationResultsFinal.csv'
DefaultSystemOptions = {'ValidateDataInRuntime':2, 'NumberOfErrorsConsideredAsWarningsForSimulation':200, 'NumberOfErrorsConsideredAsWarningsForPopulationGeneration':400, 'NumberOfTriesToRecalculateSimulationStep':5, 'NumberOfTriesToRecalculateSimulationOfIndividualFromStart':2, 'NumberOfTriesToRecalculateIndividualDuringPopulationGeneration':5, 'SystemPrecisionForProbabilityBoundCheck':1e-14 , 'RepairPopulation':1 , 'VerboseLevel': 5 , 'RandomSeed': NaN, 'GeneticAlgorithmCandidatesPerSelectedIndividual': 10, 'GeneticAlgorithmMaxEvalsTerminator': 7500, 'GeneticAlgorithmMaxStableGenerationCountTerminator':6, 'GeneticAlgorithmTournamentSize': 5, 'GeneticAlgorithmNumberOfElitesToSurviveIfBetterThanWorstOffspring': 15, 'GeneticAlgorithmSolutionPopulationSize': 100, 'GeneticAlgorithmMutationRate': 0.002}
StateIndicatorNotePrefix = 'A State Indicator Automatically Generated for State: '

ParameterTypes = ['Number','Integer','Expression','State Indicator','System Option','System Reserved']
ParamNameExtensitons = ['','_Entered']
ReportCalculationMethods =  ['Auto Detect', 'Sum Over All Records', 'Average Over All Records', 'STD Over All Records', 'Min Over All Records', 'Max Over All Records', 'Valid Count of All Records', 'Sum Over Demographics', 'Average Over Demographics', 'STD Over Demographics', 'Min Over Demographics', 'Max Over Demographics', 'Valid Count of Demographics', 'Sum Over Last Observations Carried Forward', 'Average Over Last Observations Carried Forward', 'STD Over Last Observations Carried Forward', 'Min Over Last Observations Carried Forward', 'Max Over Last Observations Carried Forward', 'Valid Count of Last Observations Carried Forward', 'Record Count', 'Demographic Count', 'Last Value Count', 'Interval Start', 'Interval End', 'Interval Length', 'No Summary' ]
ReportCalculationMethodShortTitles = ['', 'Sum All', 'Avg All', 'STD All', 'Min All', 'Max All', 'Valid All', 'Sum Dem.', 'Avg Dem.', 'STD Dem.', 'Min Dem.', 'Max Dem.', 'Valid Dem.', 'Sum LOCF', 'Avg LOCF', 'STD LOCF', 'Min LOCF', 'Max LOCF', 'Valid LOCF', 'Rec Count', 'Dem. Count', 'Last Count', 'Start Step', 'End Step', 'Interval Length', '']
ReportStratificationHeader = 'Stratification - '
ReportStratificationDescriptionDict = {-1:'None: ', 1:'By initial demographics for cell: ', 2:'By entry demographics to time interval for cell: ', 3:'By record for cell: '}

StatFunctions = ['MEAN', 'STD', 'MEDIAN', 'MIN', 'MAX', 'SUM', 'COUNT'] + ['PERCENT%0.2i'%(Entry) for Entry in range(1,100)]


# A list of reserved words not to be used as parameter names and related
# the builtin reserved words are generated by:
# filter (lambda Entry: Entry[0]!='_', dir(__builtins__))
BannedSymbolsInExpression = ["'",'"','`','~','!','@','#','$','%','^','&',':',';','?','<','>','=','{','}', '//', '\n', '\x0b','\x0c','\r']
PythonReservedWords = ['and','del','from','not','while','as','elif','global','or','with','assert','else','if','pass','yield','break','except','import','print','class','exec','in', 'raise','continue','finally','is','return','def','for','lambda','try','self']
ProgramReservedWords = ['division','DataDef','sys','pickle','tempfile','os','random','args']
BuiltinReservedWords = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'None', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', 'abs', 'all', 'any', 'apply', 'basestring', 'bool', 'buffer', 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'long', 'map', 'max', 'min', 'object', 'oct', 'open', 'ord', 'pow', 'property', 'quit', 'range', 'raw_input', 'reduce', 'reload', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange', 'zip']
OtherReservedWords = ['oo','pi','E','MyLn']
StatisticalContinuousDistributionNames = ['Uniform','Gaussian']
StatisticalDiscreteDistributionNames = ['Bernoulli','Binomial','Geometric']
StatisticalDistributionNames = StatisticalContinuousDistributionNames + StatisticalDiscreteDistributionNames
Expr2SympyFunctionMapping = {'Exp':'exp','Log':'log','Ln':'ln','Pow':'pow','Sqrt':'sqrt'}
Sympy2ExprFunctionMapping = dict(zip(Expr2SympyFunctionMapping.values(), Expr2SympyFunctionMapping.keys()))
ExpressionSupportedFunctionsNames = StatisticalDistributionNames + sorted(Expr2SympyFunctionMapping.keys()) + ['Eq','Ne','Gr','Ge','Ls','Le','Or','And','Not','IsTrue','IsInvalidNumber','IsInfiniteNumber','IsFiniteNumber','Iif','CostWizard','Log10','Pi','Mod','Abs','Floor','Ceil','Max','Min']
RuntimeFunctionNames = [('Table','TableRunTime')]
ExpressionSupportedFunctionsAndSpecialNames = ExpressionSupportedFunctionsNames + ['Inf','NaN','inf','nan'] + reduce(lambda TheList,Entry: TheList + [Entry[0]], RuntimeFunctionNames,[])
AllowedMathOperatorsInExpr = ['+','-','/','*','**']
##SystemReservedParametersToBeCreated = ['Time', 'IndividualID', 'Dummy', 'Repetition', 'AllCoefficients', 'BlankColumn', 'Inf', 'NaN','inf','nan']
SystemReservedParametersToBeCreated = ['Time', 'IndividualID', 'Dummy', 'Repetition', 'BlankColumn', 'Inf', 'NaN','inf','nan']

SystemReservedParametersAllowedInPopulationColumns = ['Dummy']


GlobalsInDB = ['Version', 'Params' , 'States' , 'StudyModels' , 'Transitions' , 'PopulationSets' , 'Projects' , 'SimulationResults']
ClassDescriptionDict = {'ParamsClass':'Parameters Collection' , 'StatesClass':'States Collection' , 'StudyModelsClass':'Studies/Models Collection' , 'TransitionsClass':'Transitions Collection' , 'PopulationSetsClass':'Population Sets Collection' , 'ProjectsClass':'Projects Collection' , 'SimulationResultsClass':'Simulation Results Collection', 'Param':'Parameter' , 'State':'State' , 'StudyModel':'Study/Model' , 'Transition':'Transition' , 'PopulationSet':'Population Set' , 'Project':'Project' , 'SimulationResult':'Simulation Result', 'Expr':'Expression' , 'SimulationRule':'Simulation Rule'}
AppFileNameExtension = '.txt'

EmptyEvalDict = {'__builtins__':'','Inf':Inf,'NaN':NaN,'inf':Inf,'nan':NaN}

# Define Load Options Evaluation Disctionary
# Start with the empty evaluation dictionary
LoadOptionsEvalDict = copy.deepcopy(EmptyEvalDict)
# Add True and False
LoadOptionsEvalDict['True']=True
LoadOptionsEvalDict['False']=False


# Define and Mark the database dirty status flag
# Careful do not access directly, use AccessDirtyStatus instead
DirtyStatusFlag = [False]


# Also some useful functions
IsStr = lambda x: isinstance(x,types.StringType)
IsList = lambda x: isinstance(x,types.ListType)
IsTuple = lambda x: isinstance(x,types.TupleType)
IsFloat = lambda x: isinstance(x,types.FloatType)
IsBoolean = lambda x: isinstance(x,types.BooleanType)
IsInt = lambda x: isinstance(x,types.IntType)
IsNumericType = lambda x: IsFloat(x) or IsInt(x)
IsReducedNumeric = lambda x: (IsFloat(x) or IsInt(x)) and (not IsBoolean(x))
IsDict = lambda x: isinstance(x,types.DictionaryType)
IsNone = lambda x: isinstance(x,types.NoneType)
IsNaN = lambda x: (x==x)==False
IsInf = lambda x: x==Inf or x ==-Inf
IsFinite = lambda x: IsNumericType(x) and not IsNaN(x) and not IsInf(x)
IsClass = lambda x: isinstance(x,types.ClassType)
IsInstance = lambda x: isinstance(x,types.InstanceType)
IsFunction = lambda x: isinstance(x,types.FunctionType)
IsMethod = lambda x: isinstance(x,types.MethodType)
IsInstanceOf = lambda x,y: x.__class__.__name__==y
IsInstanceOfLib = lambda x,y: x.__class__.__module__.startswith(y)

# Transfers ill defined value to zero
Ill2Zero = lambda x: Iif(IsNaN(x) or not IsNumericType(x), 0, x)


def RaiseNaN (InList):
    """ Returns NaN if any member IsNaN, returns the first member otherwise """
    # This function is used to detect NaN in a list of operators. It is useful
    # for raising NaN if any of the inputs/result is NaN. Otherwise it returns
    # the result that should be the first parameter in the list.
    if any(map(IsNaN,InList)):
        return NaN
    else:
        return InList[0]

# Useful functions for reduce
AndOp = lambda x,y: x and y
OrOp = lambda x,y: x or y
NotOp = lambda x: not x
XorOp = lambda x,y: (x or y) and (not (x and y))
SumOp = lambda x,y: x + y
SubOp = lambda x,y: x - y
MultOp = lambda x,y: x * y
PowOp = lambda x,y: x ** y
IsEqualOp = lambda x,y: x == y
IsHigherOp = lambda x,y: x > y
IsLowerOp = lambda x,y: x < y
IsHigherOrEqualOp = lambda x,y: x >= y
IsLowerOrEqualOp = lambda x,y: x <= y
ProdOp = lambda x: reduce(MultOp, x, 1)
# Useful list operators
NotList = lambda ListName: map ( NotOp , ListName )
SetDiff = lambda x,y: list(set(x)-set(y))


try:
    FloatInfo = numpy.finfo(float)
except:
    print 'Warning: some mathematical options do not work properly unless Numpy is installed and properly and loaded to the system.'
    # Other important values


# Define the temp directory class
class TempDirectoryClass(str):
    """ retains the temp directory name """
    def __new__ ( cls, UseDefaultPathName = True, NamePrefix = None, NameSuffix = None, CreateUnderThisDirectory = None):
        """Constructor to allow creation of a non mutable object"""
        # Upon creation of the instance, a new directory may require creation
        # By default the system will use the DefaultTempPathName and will
        # create this directory relative to the working directory if it does 
        # not exist yet.
        # However, if UseDefaultPathName is set to False then a new temporary
        # directory will be created and returned. This option is not currently
        # used, yet may be a possible future use.
        if CreateUnderThisDirectory == None:
            CreateUnderThisDirectory = os.path.dirname(sys.argv[0])
        if NamePrefix == None:
            NamePrefix = DefaultTempPathName
        if NameSuffix == None:
            NameSuffix = ''            
        if UseDefaultPathName:
            # This is the default option, where the system path will be the temp
            # directory below the installation directory of the running program.             
            PathName = os.path.join(CreateUnderThisDirectory, DefaultTempPathName)
            if not os.path.isdir(PathName):
                try:
                    os.makedirs(PathName)
                except:
                    # Check if this directory was not created by another process
                    # while trying to do this from this process. It actually
                    # does not matter who creates the directory as long as it
                    # is created. So if someone else created it, ignore the
                    # error
                    if not os.path.isdir(PathName):
                        raise ValueError, 'Return Path: Cannot recreate the directory ' + repr(PathName) + '. Please check if this path does not already exist and if there are sufficient privileges to create this path'
        else:
            # This is the non default option where a new temporary directory is
            # created using Pythons tempfile library
            PathName = tempfile.mkdtemp(NameSuffix, NamePrefix, CreateUnderThisDirectory)
        return PathName

# Now actually create the temp directory for this session which is a global
# instance that will later be used in many places.
SessionTempDirecory = TempDirectoryClass()
if 'TempDir' in DebugPrints:
    print 'Temp Directory is:'
    print SessionTempDirecory

def RedirectOutputToValidFile(TheFile , ExchangeFileName = None):
    """ Find redirect for TheFile to a real file if not suitable for output """
    # The function should be called in the following manner:
    # (TheFile, BackupOfOriginal) = RedirectOutputToValidFile(TheFile,...)
    # The function returns a tuple
    # (RetFile, BackupOfOriginal)
    # if not redirected, RetFile = OldFile = TheFile
    # If redirected, RetFile != OldFile both representing TheFile before and
    # after redirection. Note that actual redirection does not happen within
    # the function itself. 
    # Note that redirection back to the original file may be required
    # using the following scheme:
    # RedirectOutputBackwards(TheFile, RetFile, BackupOfOriginal)
    # With proper use, this function allows programs that print to stdandard
    # streams to be used when invoked in Idle, Python and Pythonw environments
    # and work properly by internal redirection of the stream to file
    (RetFile, BackupOfOriginal) = (TheFile, TheFile)
    NeedToCreateFile = False
    if not IsInstanceOfLib (TheFile, 'idlelib.rpc'):
        # Check if the file is created by the idle environment
        # if so, it is ok to use it
        # Otherwise, check if the file is an actual os file.
        # first check if it has a file open:
        if not hasattr(TheFile,'fileno'):
            # try to create the file 
            NeedToCreateFile = True
        else:
            try:
                # try to access file status
                os.fstat(TheFile.fileno())
            except:
                # if could not access statistics, this is an invalid file
                NeedToCreateFile = True
        if NeedToCreateFile:
            # if there is a need to create a file
            if ExchangeFileName == None:
                # if not filename is given, create a temp file
                (FileDescriptor, FileName) = tempfile.mkstemp ( TextSuffix, DefaultTemporaryFileNamePrefix , SessionTempDirecory , True)
                RetFile = os.fdopen(FileDescriptor,'w')
            else:
                RetFile = open(ExchangeFileName,'w')
    return (RetFile, BackupOfOriginal)

            
def RedirectOutputBackwards(TheFile, BackupOfOriginal):
    """ Redirect file backwards using backup """
    # This function should be called in the following manner:
    # TheFile = RedirectOutputBackwards(TheFile, BackupOfOriginal)
    # The function complements the following function call:
    # (TheFile, BackupOfOriginal) = RedirectOutputToValidFile(TheFile,...)
    # it restores TheFile to the original file and closes a newly created file
    # if it was created. Note that acrual restoration does not take place
    # within the function, it happens outside the call by the back arrignment.    
    # always return the backup
    RetVal = BackupOfOriginal
    if TheFile != BackupOfOriginal:
        # if a file was open during redirection, close it
        TheFile.close()
    return RetVal

    
def FilePatternMatchOptimizedForNFS(FilePattern):
    "An optimized version of glob optimized for NFS by skip dir list for file"
    # This function behaves almost exactly like glob. However, if no wildcards
    # are found in the pattern name, then the system skips retrieving the 
    # entire directory and just checks if the file exists. Otherwise the 
    # system will just use glob. This is important when accessing files over
    # NFS in cases where there are many files in a directory and they need to 
    # be transferred to different machines. The problem intensifies over large
    # cluster runs and becomes a bottleneck - therefore there is a need to
    # avoid it. 
    # the return is always a list of filenames that match the pattern.
    # The following wildcards in the file pattern will indicated that the slow
    # version of glob has to used: *?[]!. Otherwise it is assumed that
    # the file pattern has only a single file.
    #
    IsWildCardInPattern = False
    WildCardList = '*?[]!'
    for WildChar in WildCardList:
        if WildChar in FilePattern:
            IsWildCardInPattern = True
            break
    if IsWildCardInPattern:
        # if wildcards found use glob
        RetVal = glob.glob(FilePattern)
    else:
        # otherwise just check if the file exists and return a list
        if os.path.exists(FilePattern):
            # Note that os.path.exists is used rather than os.path.isfile
            # so the behavior will match glob that may return a directory
            # return the file name if found
            RetVal = [FilePattern]
        else:
            # return an empty list if not found
            RetVal = []
    return RetVal



# Useful string functions
def RemoveChars(InStr, RemoveStr = None):
    """Removes InStr characters listed in RemoveStr / whitespaces by default"""
    # If no characters are requested, use the whitespace list
    if RemoveStr == None:
        RemoveStr=WhiteSpaces
    OutStr=InStr
    # For each character in the to remove list, replace it with nothing
    for Char in RemoveStr:
        OutStr = OutStr.replace(Char,'')
    return OutStr


def SmartStr(Value):
    """ returns a descriptive str that recognizes values such as NaN and inf """
    if IsStr(Value):
        TempStr = Value
    else:
        TempStr = repr(Value)
    for (StringToReplace) in ['Inf','NaN','-NaN']:
        # Note that -NaN may have a different output and is therefore considered
        # seperatly that NaN. In an attempt to be system independent, these
        # strings are evaluated online.
        ValueToReplace = repr(eval(StringToReplace, EmptyEvalDict))
        TempStr = TempStr.replace(ValueToReplace, StringToReplace)
    return TempStr


# Other useful query functions

def RepVal (Statement, ValueToReplace = None, ReplacementValue = 0):
    """ Replace Statement with ReplacementValue if equals ValueToReplace """
    if Statement == ValueToReplace:
        return ReplacementValue
    else:
        return Statement

def FilterByAnother (DataSequence, BoolSequence):
    """ Filter the DataSequence by BoolSequence , keeping True members"""
    Combined = zip(DataSequence , BoolSequence)
    FilteredTuple = filter (lambda (Data , Bool) : Bool , Combined)
    Result = map (lambda (Data , Bool) : Data , FilteredTuple)
    return Result

def FindDuplicatesInSequence(Sequence):
    """ Returns a list of items that are duplicated in a sequence"""
    Duplicates = []
    for (ItemIndex, Item) in enumerate(Sequence):
        if Item in Sequence[:(ItemIndex)] or Item in Sequence[(ItemIndex+1):]:
            Duplicates = Duplicates + [Item]
            Duplicates = list(set(Duplicates))
    return Duplicates

def TBD( Message = "This code is yet to be constructed"):
    """Print a message that this code is yet to be constructed"""
    global MessagesTBD
    if Message == '':
        for RecordedMessage in MessagesTBD:
            print RecordedMessage
    if Message not in MessagesTBD:
        MessagesTBD = MessagesTBD + [Message]
    if 'TBD' in DebugPrints:
        print 'TBD: ' + Message
    return


def DetermineFileNameAndPath(FileName):
    """Determines file name and path, uses current path if undefined"""
    (OriginalPathOnly , FileNameOnly) = os.path.split (FileName)
    # Make the path absolute to be exact
    PathOnly = os.path.abspath (OriginalPathOnly)
    FileNameFullPath = os.path.join(PathOnly , FileNameOnly)
    return (PathOnly , FileNameOnly, FileNameFullPath)

# Programmatic support
class ClassFunctionWrapper():
    """Class wrapper for a function. Allows calling class without an instance"""
    def __init__(self, FunctionToCall):
        self.__call__ = FunctionToCall
        return

# Create a temporary class to pass data around as if using a pipe
class PipeMock():
    Data = None
    def send(self,DataToSend):
        self.Data = DataToSend
        return
    def recv(self):
        return self.Data
    def close(self):
        self.Data = None
        

def RunFunctionAsProcess(FunctionToRun):
    """ If possible, run the function as a process, return pipe"""
    if not (SystemSupportsProcesses):
        # Handle the serial executions case 
        OutputConnection = PipeMock()
        if 'MultiProcess' in DebugPrints:
            print 'running the function'
        OutputConnection = PipeMock()
        RetVal = FunctionToRun()
        OutputConnection.send(RetVal)
        if 'MultiProcess' in DebugPrints:
            print 'finished running the function'
        # store the result, errors will be handled later
        PipeList = [OutputConnection]
        ProcessList = None
    else:
        def RunAsProcess(ChildConnection):
            RetVal = FunctionToRun()
            ChildConnection.send(RetVal)
            return RetVal
        # Handle the parallel process execution case
        # create connections
        (ParentConnenction, ChildConnection) = multiprocessing.Pipe()
        PipeList = [ParentConnenction]
        # create processes
        if 'MultiProcess' in DebugPrints:
            print 'spawning a process'
        TheProcess = multiprocessing.Process(target = RunAsProcess, args = (ChildConnection,))
        ProcessList = [TheProcess]
        if 'MultiProcess' in DebugPrints:
            print 'process spawned'
        # Now actually start running the process
        TheProcess.start()
    # return the Process and pipe list to be collected by CollectResults
    return (ProcessList, PipeList)



def IsEqualDetailed (Arg1, Arg2, AttributesToSkip = None):
    """ A generic function to compare data in complex structures """
    if type(Arg1) != type(Arg2):
        # Arguments of different types mean inequality
        RetVal = False
    elif IsMethod(Arg1) or IsFunction(Arg1) or IsClass(Arg1):
        # If the attribute is a method, function or instance then
        # no comparison is required
        RetVal = True
    elif IsInstance(Arg1):
        # If these are instances, Check all attributes
        # The default of attributes to skip are the book keeping attributes
        if AttributesToSkip == None:
            AttributesToSkip = ['ID', 'CreatedOn', 'LastModified']
        # Assume instances are equal
        RetVal = True
        # Get a list of attributes of both objects
        SelfAttributes = dir(Arg1)
        OtherAttributes = dir(Arg2)
        # If the attribute list is not the same then skip further comparison
        if SelfAttributes == OtherAttributes:
            # For every attribute that is not in the skip list
            for Attr in SelfAttributes:
                if Attr not in AttributesToSkip:
                    Element1 = getattr(Arg1,Attr)
                    Element2 = getattr(Arg2,Attr)
                    ElementEqual = IsEqualDetailed (Element1, Element2, AttributesToSkip)
                    # If comparison failed, skip checking more elements
                    if not ElementEqual:
                        RetVal = False
                        break
        else:
            RetVal = False
    elif IsDict(Arg1):
        # For dictionaries convert these into lists and continue comparison
        ConvertArg1 = map(None, Arg1.iteritems())
        ConvertArg2 = map(None, Arg2.iteritems())
        RetVal = IsEqualDetailed (ConvertArg1, ConvertArg2, AttributesToSkip)
    elif IsList(Arg1) or IsTuple(Arg1):
        # If this is a list or a tuple, continue comparison per list element
        if len(Arg1) != len(Arg2):
            # Different sizes mean different lists
            RetVal = False
        else:
            # Compare all elements by looping
            RetVal = True
            for Element1, Element2 in zip(Arg1, Arg2):
                ElementEqual = IsEqualDetailed (Element1, Element2, AttributesToSkip)
                # If comparison failed, skip checking more elements
                if not ElementEqual:
                    RetVal = False
                    break
    elif IsNumericType(Arg1) and IsNaN(Arg1):
        # Special care should be taken if NaN are compared
        RetVal = IsNaN(Arg2)
    elif IsNumericType(Arg1) or IsStr(Arg1) or IsNone(Arg1):
        # All other types just check equality
        RetVal = Arg1 == Arg2
    else:
        raise ValueError, 'Assertion Error - Unsupported argument type encountered: ' + str(type(Arg1))
    # Return the result
    return RetVal


def CalcCopyName(Object, NewName = None, BaseName = None):
    """ Calculates an appropriate name for copying """
    if NewName == None:
        # If no specific name was specified, find an appropriate name
        # Before that collect the existing names
        if IsStr(Object) and not IsInstanceOf(Object,'Param'):
            CollectionName = Object
        else:
            CollectionName = Object.__class__.__name__ + 's'
        Collection = globals()[CollectionName]
        if CollectionName == 'Params':
            # Treat parameters differently since they do not have a
            # name attribute
            Names = Collection.keys()
            if BaseName == None:
                BaseName = str(Object)
        else:
            # All other classes are the same
            Names = map(lambda Entry: Entry.Name, Collection.values())
            if BaseName == None:
                BaseName = str(Object.Name)
        # If no name is specified, select a name that does not
        # already exist. For this loop until a name is found.
        Index = 0
        while True:
            NewName = BaseName + '_' + str(Index)
            if NewName in Names:
                Index = Index + 1
            else:
                # This means a name has been found
                break
    # Return the calculated or specified name
    return NewName

def DescribeReturnsName(self):
    """ Return the Name attribute of the class"""
    RetVal = self.Name
    return RetVal


def DependancyErrorCheck(self, DependancyCollection, DependencyDefFunc, ErrorHeaderString):
    DependancyCollectionItems = DependancyCollection.items()
    IsDependant = map(DependencyDefFunc, DependancyCollectionItems)
    if any(IsDependant):
        DependentEntries = FilterByAnother(DependancyCollectionItems, IsDependant)
        DependentKeys = map (lambda (EntryKey,Entry): EntryKey, DependentEntries )
        ErrorDetailString = DependancyCollection.ID2Name(DependentKeys)
        raise ValueError, ErrorHeaderString + ErrorDetailString


# Define system reserved functions

# Boolean and comparison Operators
# Although quite safe, avoid using Python True and False outcomes
# Also note that no special NaN treatment is added to comparison operations

def Eq(x,y):
    """ Replaces the equality Operator x==y """
    if x==y:
        return 1
    else:
        return 0

def Ne(x,y):
    """ Replaces the inequality Operator x!=y """
    if x!=y:
        return 1
    else:
        return 0

def Gr(x,y):
    """ Replaces the Greater than Operator x>y """
    if x>y:
        return 1
    else:
        return 0

def Ge(x,y):
    """ Replaces the Greater than or Equal Operator x>=y """
    if x>=y:
        return 1
    else:
        return 0

def Ls(x,y):
    """ Replaces the Less than Operator x<y """
    if x<y:
        return 1
    else:
        return 0  

def Le(x,y):
    """ Replaces the Less than or Equal Operator x<=y """
    if x<=y:
        return 1
    else:
        return 0



# Define Boolean operations
# Note that Ill argument such as NaN are considered as zero

def Or(*ArgList):
    """ Replaces the Python 'or' operator """
    Res = False
    ArgNum = len(ArgList)
    if ArgNum < 2:
        raise ValueError, 'The Or operator requires at least 2 parameters, whereas ' + str(ArgNum) + ' are provided'
    for Arg in ArgList:
        Res = Res or Ill2Zero(Arg)
    if Res:
        return 1
    else:
        return 0
        
def And(*ArgList):
    """ Replaces the Python 'and' operator """
    Res = True
    ArgNum = len(ArgList)
    if ArgNum < 2:
        raise ValueError, 'The And operator requires at least 2 parameters, whereas ' + str(ArgNum) + ' are provided'
    for Arg in ArgList:
        Res = Res and Ill2Zero(Arg)
    if Res:
        return 1
    else:
        return 0

def Not(x):
    """ Replaces the Python 'not' operator """
    if not Ill2Zero(x):
        return 1
    else:
        return 0
   
def IsTrue(x):
    """ Returns 1 for a non zero number. Returns 0 otherwise """
    if Ill2Zero(x):
        return 1
    else:
        return 0

# Define Special Number functions exposed to the user:
# Note that non numeric types such as matrices have special consideration 
def IsInvalidNumber(x):
    """ Will return 1 for x=NaN or for a non numeric type, 0 otherwise """
    if not IsNumericType(x) or IsNaN(x):
        return 1
    else:
        return 0

def IsInfiniteNumber(x):
    """ Will return 1 for x=-Inf or x=Inf, 0 otherwise """
    if x==Inf or x==-Inf:
        return 1
    else:
        return 0

def IsFiniteNumber(x):
    """ Will return 0 if x is invalid or an Infinite number, 1 otherwise """
    if not IsInvalidNumber(x) and not IsInfiniteNumber(x):
        return 1
    else:
        return 0


# Control and Data Access
def Iif (Statement, TruePart, FalsePart):
    """Immidiate if: if statement is true return TruePart otherwise FalsePart"""
    if Statement:
        return TruePart
    else:
        return FalsePart


def TableParseOnly(*ArgList):
    """ Parses a table definition - return the class """
    # First see if the Arguments to the table are of 2 lists. if so, then
    # the new method of calling is used and there is no need to reconstruct
    # any string.
    if len(ArgList)==2 and IsList(ArgList[0]) and IsList(ArgList[1]):
        # if using the new format, just call the funcion with the arguments
        TempTable = TableClass(DimensionsArray = ArgList[0], ValuesArray = ArgList[1])
    else:
        # Recostruct the Argument list string while replacing back Inf and NaN
        # This is requires since the call to the function already replaced
        # Inf and NaN with values and string conversion will create artifacts.
        # Since the table class requires string representation, this processing
        # is required to provide proper input. The function returns the constructed
        # Table object
        ArgString = str(ArgList)
        ArgString = ArgString.replace(str(Inf),'Inf')
        ArgString = ArgString.replace(str(-Inf),'(-Inf)')
        ArgString = ArgString.replace(str(NaN),'NaN')
        try:
            # Try to create a table class with the input parameters. If unsuccessful
            # raise an error
            TempTable = TableClass( InitString = 'Table'+ArgString, ParseOnly = True)
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Table Parser Error: The table cannot be evaluated. Check the number and the validity of parameters. Here are additional details:' + str(ExceptValue)
    return TempTable

def Table(*ArgList):
    """ Parses a table definition - Validation Time version"""
    # Just call the parser, an error will be raised if there is a problem
    TableParseOnly(*ArgList)
    # return a number
    return 0

def TableRunTime(*ArgList):
    """ Run Time version - parses parameters and returns a value """
    # Call the parser to get a table object
    TableObject = TableParseOnly(*ArgList)
    # Evaluate the table value 
    Value = TableObject.Evaluate()
    # return a number
    return Value


def CostWizard (FunctionType, InitialValue, ParameterVector, CoefficientVector):
    """ Calculate costs and quality of Life using this function """
    # The function uses the approach presented in the following paper:
    # Zhou H, Isaman DJM, Messinger S, Brown MB, Klein R, Brandle M, Herman WH:
    # A Computer Simulation Model of Diabetes Progression, Quality of Life, and
    # Cost. Diabetes Care 28:2856-2863, 2005
    # The function Input is:
    # FunctionType: For a Cost function it is 0, for Qualify of Life it is 1.
    # InitialValue: The base value
    # ParameterVector : A sequence of parameter values
    # CoefficientVector : A sequence of coefficient values associated with the
    #                     parameters in ParameterVector and should be the same
    #                     length of the sequence.
    # Check input validity first

    if FunctionType not in [0,1]:
        raise ValueError, 'Cost Wizard parameter 1 invalid: Unknown Function Type provided for the Cost Wizard'
    if not IsFinite(InitialValue):
        raise ValueError, 'Cost Wizard parameter 2 invalid: Initial value is not a valid finite number'
    if not IsList(ParameterVector):
        raise ValueError, 'Cost Wizard parameter 3 invalid: The Parameter Vector must be a List, i.e. enclosed in brackets'
    if not IsList(CoefficientVector):
        raise ValueError, 'Cost Wizard parameter 4 invalid: The Coefficient Vector must be a List, i.e. enclosed in brackets'
    if len(ParameterVector) != len(CoefficientVector):
        raise ValueError, 'Cost Wizard Parameters 3,4. It is required that the parameter vector and the coefficient vector will be the same size'
    for Member in ParameterVector:
        if not IsFinite(Member):
            raise ValueError, 'Cost Wizard parameter 3: An invalid member detected in the parameter vector. This member is not a valid finite number.'
    for Member in CoefficientVector:
        if not IsFinite(Member):
            raise ValueError, 'Cost Wizard parameter 4: An invalid member detected in the coefficient vector. The coefficient is not a valid finite number'
    # Calculate the dot product of both vectors
    SumOfMult = reduce(SumOp,map(MultOp,ParameterVector,CoefficientVector),0.0)
    if FunctionType == 0:
        # Cost functions
        Result = InitialValue * 10.0**SumOfMult
    elif FunctionType == 1:
        # QOL function
        Result = InitialValue + SumOfMult
    else:
        raise ValueError, 'Cost Wizard Error: The cost wizard does not support this type of cost function.'
    return Result   
    

def Exp(x):
    """ Exponent wrapper for expression resolution"""
    try:
        RetVal = math.exp(x)
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Log(x,n):
    """ Logarithm wrapper for expression resolution"""
    try:
        RetVal = math.log(x,n)
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Ln(x):
    """ Natural Logarithm wrapper for expression resolution"""
    try:
        RetVal = math.log(x)
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Log10(x):
    """ Logarithm base 10 wrapper for expression resolution"""
    try:
        RetVal = math.log10(x)
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Pow(x,n):
    """ Power wrapper for expression resolution"""
    try:
        RetVal = math.pow(x,n)
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Sqrt(x):
    """ Square root wrapper for expression resolution"""
    try:
        RetVal = math.sqrt(x)
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Pi():
    """ Pi wrapper for expression resolution"""
    try:
        RetVal = math.pi
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Mod(x,n):
    """ Modulus wrapper for expression resolution"""
    try:
        RetVal = math.fmod(x,n) 
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Abs(x):
    """ Absolute value wrapper for expression resolution"""
    try:
        RetVal = math.fabs(x) 
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Floor(x):
    """ Floor wrapper for expression resolution"""
    try:
        RetVal = math.floor(x) 
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Ceil(x):
    """ Ceiling wrapper for expression resolution"""
    try:
        RetVal = math.ceil(x)
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal
        

def Max(*ArgList):
    """ Maximum wrapper for expression resolution"""
    # Note that keyword argument key prohibits from using the max option
    # of using a keyword key to define a function
    if len (ArgList) < 2:
        raise ValueError, 'Max function: At least two input arguments are required to calculate a maximum value' 
    try:
        # Note that NaNs will cause returning NaN
        if any(map(IsInvalidNumber,ArgList)):
            RetVal = NaN
        else:
            RetVal = max(ArgList)
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal

def Min(*ArgList):
    """ Minimum wrapper for expression resolution"""
    # Note that keyword argument key prohibits from using the min option
    # of using a keyword key to define a function
    if len (ArgList) < 2:
        raise ValueError, 'Min function: At least two input arguments are required to calculate a minimum value' 
    try:
        # Note that NaNs will cause returning NaN
        if any(map(IsInvalidNumber,ArgList)):
            RetVal = NaN
        else:
            RetVal = min(ArgList)
    except:
        # Return NaN in case of an error
        RetVal = NaN        
    return RetVal


# Statistical distributions
# Statistical distribution functions have two usage modes, if the value x is 
# provided as input then the function will return the cdf for the given x value. 
# When x is not provided, then function returns a random value according to the
# specified distribution and its parameters.
# Statistical functions rely on the Scipy module being loaded. 

def Bernoulli(p):
    """ Bernoulli distribution with chance p """
    try:
        # Random Generator
        RetVal = float(numpy.random.binomial(1,p))
    except:
        # Return NaN in case of an error
        RetVal = NaN
    return RetVal

def Binomial(n,p):
    """ Binomial distribution with chance p and n tries"""
    try:
        # Random Generator
        RetVal = float(numpy.random.binomial(n,p))
    except:
        # Return NaN in case of an error
        RetVal = NaN
    return RetVal

def Geometric(p):
    """ Geometric distribution with chance p """
    try:
        # Random Generator
        RetVal = float(numpy.random.geometric(p))
    except:
        # Return NaN in case of an error
        RetVal = NaN
    return RetVal

def Uniform(a,b):
    """ Uniform distribution with on the interval a,b"""
    try:
        # Random Generator
        RetVal = float(numpy.random.uniform(a,b))
    except:
        # Return NaN in case of an error
        RetVal = NaN
    return RetVal

def Gaussian(mean,std):
    """ Gaussian distribution with parameters mean,std"""
    try:
        # Random Generator
        RetVal = float(numpy.random.normal(mean,std))
    except:
        # Return NaN in case of an error
        RetVal = NaN
    return RetVal



######## Define the Statistical Evaluation Disctionary #######
# Start with the empty evaluation dictionary
StatisticsEvalDict = copy.deepcopy(EmptyEvalDict)
# Add the distribution function names from the globals
for DistName in StatisticalDistributionNames:
    StatisticsEvalDict[DistName] = globals()[DistName]


# Misc functions
def MessageToUser(MessageString, MaxStringSizeToPrint = Inf):
    """ Wrapper function for user feedback """
    TheStringLength = len(MessageString) 
    # For now, just print the message
    if  TheStringLength < MaxStringSizeToPrint:
        print MessageString
    else:
        print MessageString[:min(MaxStringSizeToPrint,TheStringLength)] + (' ### Truncated from an original of %i characters to %i characters ###' % (TheStringLength, MaxStringSizeToPrint))
    TBD ('Improve MessageToUser Mechanism and tie it to the GUI')

def CostWizardParserForGUI(CostWizardString, TreatEmptyAsDefault = False):
    """ A parser for the cost wizard expression for the GUI """
    # This is a Naive parser that tries to understand the cost Wizard
    # string. It performs the following tasks:
    # 0. Checks that the expression is legal/valid
    # 1. ['%0.5v','%i']s default and removes the function name and enclosing parenthesis
    # 2. Tries to locate the two sequences in the string. 
    # 3. Splits the strings at the commas to extract the two initial
    #    parameters and checks that there are only two of these at the beginning
    #    and that these are valid.
    # 4. Makes sure the sequence parameters at the end are valid by splitting
    #    at commas.
    #
    # The Input is:
    # CostWizardString: The string to Parse
    # TreatEmptyAsDefault: A Boolean indicating an empty string is a default
    # The output consists of the following sequence:
    # [FunctionType, InitialValue, ParameterVector, CoefficientVector]   
    # where:
    # FunctionType: either 0 or 1.
    # InitialValue: a string representing the initial value
    # ParameterVector : A sequence of strings representing parameters
    # CoefficientVector : A sequence of strings representing coefficients
    #
    # The function raises an error in case an error was detected while parsing
    # the string.

    # 0. Validates the expression is at all valid by creating an instance of the
    #    Expr class.
    try:
        Expr(CostWizardString)
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Cost Wizard Parser: The expression supplied is not valid. Here are details: ' + str(ExceptValue)
    # first remove all white spaces to make things easier later
    TempStr = RemoveChars(CostWizardString)
    # 1. ['%0.5v','%i'] default
    if TempStr =='' and TreatEmptyAsDefault:
        return [0,0.0,[],[]]
    # Check that the beginning of the string is CostWizard
    if len(TempStr)<21:
        raise ValueError, 'Cost Wizard Parser: This string is too short to represent a valid Cost Wizard string and therefore will not be parsed'        
    # Check string beginning
    if not TempStr.startswith('CostWizard'):
        raise ValueError, 'Cost Wizard Parser: The text does not start with the term "CostWizard" and therefore cannot be parsed. To use the cost Wizard correctly, the expression must start with this term. If a more complicated expression is required, please split it to several separate rules'
    # Check and strip parenthesis
    if TempStr[10] != '(' or TempStr[-1] != ')':
        raise ValueError, 'Cost Wizard Parser: Cost function not fully enclosed in parenthesis or is not the only function in the expression. To use the cost Wizard correctly, the expression must include the Cost Wizard Function alone. If a more complicated expression is required, please split it to several separate rules'
    # 2. Split the string at [
    SequenceSplit = NestedExpressionArgumentSplit(TempStr, EatFunctionWrapper = '()')
    # Make sure there is a correct number of sequences
    if len(SequenceSplit) != 4:
        raise ValueError, 'ASSERTION ERROR: There should be exactly 2 sequences in the CostWizard parameters'
    # 3. ['%0.5v','%i'] the first two parameters:
    # Detect first two parameters and make sure there was no sequence there
    # First check the values of the first param
    if SequenceSplit[0].strip() not in ['0','1']:
        raise ValueError, 'Cost Wizard Parser: Unrecognized type parameter of the CostWizard. The first parameter must be either 0 for a cost function of 1 for a Quality of Life function'
    if SequenceSplit[1].strip() == '':
        raise ValueError, 'ASSERTION ERROR: Empty second parameter detected by the CostWizard. The second parameter must contain the base value before adjustments'
    # Record the function type
    FunctionType = int(SequenceSplit[0])
    # Check validness of second parameter by turning it to an expression
    try:
        Expr(SequenceSplit[1])   
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Cost Wizard Parser: The second parameter is not a valid expression. Here are details: ' + str(ExceptValue)
    # Record the initial value
    InitialValue = SequenceSplit[1]
    # Init the output variables
    FuncOutput = [FunctionType,InitialValue,None,None]
    # 4. Check the last two parameters
    SequenceLengths = [None, None]
    # For each such sequence
    for SeqNum in [0,1]:
        # Check the sequence
        SequenceToCheck = SequenceSplit[SeqNum+2]
        try:
            Expr(SequenceToCheck, ValidationRule = 'Matrix')
        except:        
            raise ValueError, 'Cost Wizard Parser: Proper sequence not detected for parameter #' + str(SeqNum+3)+ ' of CostWizard, if the function was manipulated by hand, remove all enclosing parenthesis and spaces around the brackets'
        # Split the sequence without brackets at the commas
        ParamList = NestedExpressionArgumentSplit(SequenceToCheck.strip()[1:-1])
        SequenceLengths[SeqNum] = len(ParamList)
        # For each member:
        for Member in ParamList:
            # Check each member separately for expression validity. This will
            # also verify that there is no nested sequence since vectors will
            # be reported as errors. This is in a sense an assertion error as
            # the initial expression test should have caught such errors
            try:
                Expr(Member) 
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                raise ValueError, 'ASSERTION ERROR: The parameter "' + Member + '" is not a valid expression. Here are details: ' + str(ExceptValue)
        # After validation, it is possible to add the list to the output
        FuncOutput[2+SeqNum] = ParamList
    # Assertion check - the expr at the beginning should have caught this
    # while trying to evaluate the function.
    if SequenceLengths[0] != SequenceLengths[1]:
        raise ValueError, 'ASSERTION ERROR: sequences are not of the same length. This should have been caught previously while trying to calculate the function'
    # Return the output sequence with the parsed information
    return FuncOutput

def ConstructCostWizardString(CostWizardSequence):
    """ Assembles the Cost Wizard String from a proper sequence """
    # This function is designed to be used from within the GUI and therefore
    # little syntax checking is performed on the data except expression
    # validation at the end.
    if not IsList(CostWizardSequence) or len(CostWizardSequence)!=4:
        raise ValueError, 'ASSERTION ERROR: Invalid input sequence that is not a list or if wrong size, please make sure'
    if CostWizardSequence[0] not in [0,1]:
        raise ValueError, 'ASSERTION ERROR: Unknown type of CostWizard type - parameter 1 should be either 0 or 1'
    if not IsList(CostWizardSequence[2]) or not IsList(CostWizardSequence[3]):
        raise ValueError, 'ASSERTION ERROR: At least one of the last two parameters are not sequences'
    ParamStr1 = str(CostWizardSequence[0])
    ParamStr2 = str(CostWizardSequence[1])
    AddWithComma = lambda Var1,Var2: str(Var1)+','+str(Var2)
    if CostWizardSequence[2]==[]:
        ParamStr3 = '[]'
    else:
        ParamStr3 = '['+reduce(AddWithComma,CostWizardSequence[2])+']'
    if CostWizardSequence[3]==[]:
        ParamStr4 = '[]'
    else:
        ParamStr4 = '['+reduce(AddWithComma,CostWizardSequence[3])+']'
    CostWizardStr = 'CostWizard('+ParamStr1+','+ParamStr2+','+ParamStr3+','+ParamStr4+')'
    # Now test the constructed string for validity
    try:
        Expr(CostWizardStr)
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Cost Wizard Constructor: The constructed cost wizard expression is invalid. Make sure that the parameters used are valid and that the result can be calculated. The constructed expression was: "' + CostWizardStr + '". Here are error details: ' + str(ExceptValue)
    return CostWizardStr


def NestedExpressionArgumentSplit(InputString, EatFunctionWrapper = None):
    """Splits a string of arguments at commas at the topmost nesting level"""
    NestingLevel = 0
    CurrentMember = ''
    SplitOutput = []
    StringToProcess = InputString
    # Eating function wrapper will take away the header and the tail up to the
    # first parenthesis/brackets as long as no comma is encountered.
    # EatFunctionWrapper hold the open/close element to be eaten to - () or []
    # Note that no consistency check is made on the pairing of parenthesis
    # it is assumed that parenthesis are paired properly
    if EatFunctionWrapper != None:
        try:
            StartIndex = InputString.index(EatFunctionWrapper[0]) + 1
            EndIndex = InputString.rindex(EatFunctionWrapper[1])
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'ASSERTION ERROR: Cannot properly strip wrapper parenthesis from function string before splitting at commas "' + InputString + '". Here are error details: ' + str(ExceptValue)
    else:
        StartIndex = 0
        EndIndex = len(InputString)
    StringToProcess = InputString[StartIndex:EndIndex]
    for Char in StringToProcess:
        if Char == ',' and NestingLevel == 0:
            # If comma encountered at the top most level perform the split
                SplitOutput = SplitOutput + [CurrentMember]
                CurrentMember = ''
        else:
            # otherwise record the character
            CurrentMember = CurrentMember + Char
        # Decide on Nesting level
        if Char in '[(':
            # Opening parenthesis and brackets increase nesting level
            NestingLevel = NestingLevel + 1
        elif Char in '])':
            # closing parenthesis and brackets decrease nesting level
            NestingLevel = NestingLevel - 1
    # Note that output elements are striped from spaces
    SplitOutput = SplitOutput + [CurrentMember.strip()]
    return SplitOutput



def HandleOption(OptionName, OptionList, Value = None, UseNewValue = False, DeleteThisOption = False):
    """ Updates or returns the OptionName from a sequence of options """
    if OptionList == None: 
        OptionList = []
    if not UseNewValue:
        DefaultValue = Value
        # If not new value specified, just extract the value
        for (OptionEnum, OptionEntry) in enumerate(OptionList):
            # The code below is deprecated and left here for backup
            # # If the option is specified, return True
            # if IsStr(OptionEntry) and OptionEntry == OptionName:
            #     return True
            # if IsTuple(OptionEntry) and OptionEntry[0] == OptionName:
            if OptionEntry[0] == OptionName:
                # Use deepcopy to avoid passing references of lists
                # this allows modifying these lists later without
                # affecting the original code
                if DeleteThisOption:
                    # if asking to delete this option, copy the list
                    NewListCopy = copy.deepcopy(OptionList)
                    # remove the option from that new copied list
                    NewListCopy.pop(OptionEnum)
                    # return the copied list without the option
                    return NewListCopy
                else:                
                    # if querying for the value
                    return copy.deepcopy(OptionEntry[1])
        # If none found so far, return the DefaultValue            
        return DefaultValue
    else:
        if DeleteThisOption:
            raise ValueError, 'ASSERTION ERROR: An Option can not be deleted and added at the same time'
        NewValue = Value
        # If a New value was specified make the modification in the sequence
        NumAndNameToReplace = filter (lambda (OptionNum, OptionEntry): (IsStr(OptionEntry) and OptionEntry == OptionName) or (IsTuple(OptionEntry) and OptionEntry[0] == OptionName), enumerate(OptionList))
        if NumAndNameToReplace == []:
            # Add the option as it is not in the list
            ReturnList = OptionList + [(OptionName, NewValue)]
        else:
            if len(NumAndNameToReplace)>1:
                raise ValueError, 'ASSERTION ERROR: An Option is defined more than once in an option List'
            NumToReplace = NumAndNameToReplace[0][0]
            ReturnList = copy.deepcopy(OptionList)
            ReturnList[NumToReplace] = (OptionName, copy.deepcopy(NewValue))
        return ReturnList


def SaveOptionList(FileName, OptionList):
    """ Saves the option list to file """
    try:
        TheFile = open(FileName,'w')
        for OptionEntry in OptionList:
            # Save the option
            TheFile.write(str(OptionEntry[0]))
            TheFile.write('\n')
            # Save the option value with repr to allow evaluate later on
            TheFile.write(repr(OptionEntry[1]))
            TheFile.write('\n')
        TheFile.close()
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Save Option List Error: Could not save the option list to the file ' + str(FileName) + ' . Try verifying the path is valid and make sure the file is not in use. Here are further details about the error: ' + str(ExceptValue)
    return True                


def LoadOptionList(FileName):
    """ Loads the option list from file """
    try:
        TheFile = open(FileName)
        FileLines = TheFile.readlines()
        TheFile.close()
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Load Option List Error: Could not load the option list from the file ' + str(FileName) + ' . Try verifying the path is valid and make sure the file contains valid options. Here are further details about the error: ' + str(ExceptValue)
    OptionsList = []
    if len(FileLines)%2 != 0:
        raise ValueError, 'Load Option List Error: Could not load the option list from the file ' + str(FileName) + ' since the file is not in a proper format of Name Value line pairs - The number of lines in the file is not even. '
    Iterator=0
    try:
        while Iterator<len(FileLines):
            ReportParameterNameStr = FileLines[Iterator].strip()
            ReportParameterValueStr = FileLines[Iterator+1].strip()
            ReportParameterValue = eval(ReportParameterValueStr, LoadOptionsEvalDict)
            OptionsList = HandleOption(ReportParameterNameStr, OptionsList, ReportParameterValue, True)
            Iterator=Iterator+2
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Load Option List Error: Could not load the option list from the file ' + str(FileName) + ' due to failure to interpret the file contents . Here are further details about the error: ' + str(ExceptValue)
    return OptionsList


def ImportDataFromCSV(FileName, ImportColumnNames = True, ConvertTextToProperDataType = True, TextCellsAllowed = False):
    """Import data and column names from a CSV file"""
    # First open the file and read data from it
    try:
        ImportFile = open(FileName,'rb')
        ReadLines = csv.reader(ImportFile)
        DataRead = list(ReadLines)
        if 'CSV' in DebugPrints:
            print DataRead
        ImportFile.close()
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'CSV Import Error: An Error was encountered trying to access the CSV file. Please make sure the file exists and is not blocked for reading by the system or by another program. Here are details about the error: ' + str(ExceptValue)
    # Analyze the data
    if ImportColumnNames:
        # convert the list to tuples describing the column data
        DataColumns = map (lambda ColumnName: (ColumnName, ''), DataRead[0])
        DataPart = DataRead[1:]
    else:
        DataColumns = []
        DataPart = DataRead[:]
    # Convert data from strings to numbers
    if ConvertTextToProperDataType:
        Data=[]
        for (RowIndex,Row) in enumerate(DataPart):
            # Process the string and convert each item to the appropriate
            # Data type: None, Integer and Float
            ConvertedRow = []
            for (ColumnIndex,DataEntry) in enumerate(Row):
                if DataEntry == '':
                    # No data
                    ConvertedDataEntry = None
                elif DataEntry.lower() in ['inf','infinity','1.#INF']:
                    # Infinity
                    ConvertedDataEntry = Inf
                elif DataEntry.lower() in ['-inf','-infinity','-1.#INF']:
                    # -Infinity
                    ConvertedDataEntry = -Inf
                elif DataEntry.lower() in ['nan','-1.#IND']:
                    # Not a Number
                    ConvertedDataEntry = NaN
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
                            # Not a float
                            if TextCellsAllowed:
                                # if Text entry is allowed, use the text
                                ConvertedDataEntry = DataEntry
                            else:
                                # if Text is not allowed, then raise an error
                                raise ValueError, 'CSV Import Error: An unrecognized input entry in the CSV file, Data position is ' + str(RowIndex) + ',' + str(ColumnIndex) + ' the entry is "' + DataEntry +'"'
                ConvertedRow = ConvertedRow + [ConvertedDataEntry]
            Data = Data + [ConvertedRow]
    else:
        # In case no conversion is needed
        Data = DataPart
    return (DataColumns,Data)

def ExportDataToCSV(FileName, Data, ColumnHeaders=None):
    """Export data to a CSV file"""
    # Note that the value None will be exported as an empty entry so no
    # change is required to the data at the entry level
    if ColumnHeaders != None:
        DataToExport = [ColumnHeaders] + Data
    else:
        DataToExport = Data
    # Determine the file name
    (PathOnly , FileNameOnly, FileNameFullPath) = DetermineFileNameAndPath(FileName)
    # Open the file for writing and write
    try:
        ExportFile = open (FileNameFullPath,'wb')
        Writer = csv.writer(ExportFile)
        Writer.writerows(DataToExport)
        ExportFile.close()
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'CSV Export Error: An Error was encountered trying to access the CSV file. Please make sure the file is not used by another program and that access is not restricted and that there are sufficient write privileges and space. Here are details about the error: ' + str(ExceptValue)
    return


# Special Variable values
# Assign special variable names with values so that these will parse correctly
# when constructing an expression. 
Time=0
Dummy=0
IndividualID=0


# Definitions of Classes

class Expr(str):
    """Defines an expression that uses parameters"""
    ExpandedExpr = '' # Holds the expanded expression after recursive
                      # substitution of other parameters
    DependantParams = [] # Holds the names of the dependant parameters after
                         # Validation of an expression
    ReplacementSubExpressions = [] # Holds the sub-expressions associated with 
                                   # each dependant param at DependantParams
                                   # These can later be used for validation of
                                   # values.
    ValidationRule = None # Recalls the validation rule used when the 
                          # expression was created.
    RawDependants = [] # A list of tokens recognized in the expression. These
                       # represent nodes in the expression tree                     
    RawReplacement = [] # a list of replacements to replace the tokens. These 
                        # can be used to reconstruct the expression using
                        # a set of assignments statements
    def __new__ ( cls, ExprText = None, ValidationRule = None):
        """Constructor to allow creation of a non mutable object"""
        if ExprText == None:
            ExprText = ''
        # strip leading and trailing white spaces
        ExprText = ExprText.strip() 
        # Create the new object
        RetVal = super(Expr, cls).__new__(cls, ExprText)
        # Reset the expanded string of this expression
        RetVal.ExpandedExpr = ''
        # Set the ValidationRule of this expression
        RetVal.ValidationRule = ValidationRule
        # values of the string
        RetVal.ValidateExpr(None, RetVal.ValidationRule)
        return RetVal

    def __deepcopy__(self, memo={}):
        """ override standard deepcopy operation """
        # This is a strict version where validity checks are remade.
        # However, since deepcopy is not a bottleneck anywhere then this
        # method is used as another assertion check in the program
        # Note that the original Validation rule is used during creation to
        # allow creating a Matrix without raising an error during deepcopy
        RetVal = Expr(str(self), self.ValidationRule)
        if RetVal.DependantParams != self.DependantParams or RetVal.ReplacementSubExpressions != self.ReplacementSubExpressions:
            raise ValueError, 'ASSERTION ERROR: Information did not deepcopy correctly, The new copy does not hold the same attributes as the original'
        # make a link form the original to the copy
        memo[id(self)] = RetVal
        return RetVal
        
    def ExtractParams(self, ExprText = None, StrictNameChecks = True):
        """ Extract the parameter names from the expression """
        # Note that there may be duplications
        if ExprText == None:
            ExprText = str(self)
        ExtractedParams = []
        # Start by detecting all tokens
        TokensInfo = sorted( tokenize.generate_tokens(StringIO.StringIO(ExprText).readline), key = lambda Entry: Entry[2])
        # Note that the current implementation of generate_tokens returns the
        # tokens in order of appearance. Other functions in the code rely on 
        # this fact. To avoid possible future issues we are sorting the tokens 
        # again by location (TokenStart - 3rd return argument).
        for (TokenType, Token, TokenStart, TokenEnd, OriginalString) in TokensInfo:
            if StrictNameChecks:
                # Check if the token is a string representing a parameter
                if re.match(ParamTextMatchPattern,Token) != None:
                    # Make sure it is an existing parameter from a valid type
                    if Params.has_key(Token):
                        if Params[Token].ParameterType == 'System Reserved' and Params[Token].Formula == '':
                            raise ValueError, 'Expression Parameter Extraction: The term (token) "'+ Token +'" is a banned system reserved name. Please check the expression for typos as this name should not be used'
                    else:
                        raise ValueError, 'Expression Parameter Extraction: The term (token) "'+ Token +'" used in the expression is not a valid name of a parameter nor a valid function name'
                    # If reached this point, the parameter is valid.
                    # Add it to the output list
                    ExtractedParams = ExtractedParams + [Token]
            else:
                # Check if the token is a string representing a parameter or a
                # temporary parameter starting with an underscore. This allows
                # testing expressions built from matrix multiplication where
                # transition names start with an underscore to distinguish
                # them from any other parameter name.
                if re.match(ParamUnderscoreAllowedTextMatchPattern,Token) != None:
                    # Add the token to the output list
                    ExtractedParams = ExtractedParams + [Token]
        return ExtractedParams

    def CheckParsedSyntax(self, ParsedTreeAsList, PerformFinalChecks):
        """ Checks the syntax of a parsed expression tree """
        # The function input is:
        # ParsedTreeAsList - a list of the already parsed expression tree that
        #                    can be obtained by parser.expr(MyExpr).tolist()
        # PerformFinalChecks - a Boolean that indicates that final checks should
        #                      be made on the entire expression. This should be
        #                      set to True when the function is called from the
        #                      outside. This way the entire expression will be
        #                      exposed to additional validity checks. When the
        #                      function recursively calls itself this argument
        #                      is set to true.
        # The function returns the following data:
        # Invalid - Contains an error string representing the first problem
        #           encountered in the expression. An expression is invalid
        #           if any mathematical operation with a list takes place
        #           Anywhere in the expression. Or if a tuple is detected that
        #           does not pass arguments to a valid function
        # HasList  - True if the input ParsedTreeAsList is a list at the 
        #            outermost Level, i.e. similar to [1,a,b]
        # HasTuple - True if the input ParsedTreeAsList is a Tuple at the 
        #            outermost Level, i.e. similar to (1,a,b)
        # ModifiedString - A string that shows the expression while replacing
        #                  sequences,tuples, and function calls with a single 
        #                  token. This allows simplifying detection of lists and
        #                  sequences even when these are nested
        # SubstitutedString - In this string, all tokens that are not reserved
        #                     variables and not already numbers are replaced 
        #                     with the number 1.
        # OutString - The original string constructed while traversing the
        #             parsed expression tree
        # EncapsulatedFunctions - A list of functions encountered while
        #                         traversing the expression. sub texts may 
        #                         be repeated if these are recursively 
        #                         encapsulated. 
        Invalid = ''
        HasList = False
        HasTuple = False
        ModifiedString = ''
        SubstitutedString = ''
        OutString = ''
        EncapsulatedFunctions = []
        PrevItem = ''
        # Loop through each member in the list, ignoring the first. These
        # represent nodes or leafs in the parsed tree
        for DataItem in ParsedTreeAsList[1:]:
            if type(DataItem) != type('1'):
                # If the member is a list this means a tree node and therefore
                # recursively analyze it
                (WasInvalid, WasList, WasTuple , ModItemStr, SubsItemStr, ItemStr, PreviouslyDetectedEncapsulatedFunctions ) = self.CheckParsedSyntax(DataItem, False)
            else:
                # Otherwise this is a tree leaf and therefore copy its info
                WasInvalid = ''
                WasList = False
                WasTuple = False
                ModItemStr = DataItem
                PreviouslyDetectedEncapsulatedFunctions = []
                # check if variable by checking if the first character is
                # alphanumeric
                if  DataItem !='' and DataItem[0] in AlphabetNoNumeric:
                    # This means some variable or function, the assumption is
                    # that all names used at this point should be valid.
                    # Check that this is so again and raise an assertion error
                    # if not so
                    if Params.has_key(DataItem):
                        # Just for precaution check existance of the parameter                        
                        if Params[DataItem].ParameterType == 'System Reserved':
                            # If this is a function then retain the name
                            SubsItemStr = DataItem
                        else:
                            # This is another type of parameter, replace it
                            # with the value 1 for substitution
                            SubsItemStr = '1'
                    else:
                        raise ValueError, 'ASSERTION ERROR: unrecognized name of parameter or function. At this point the parameter "' + str(DataItem) + '" should be already verified to be in the parameter list'
                else:
                    # This means a number or an operator
                    SubsItemStr = DataItem           
                ItemStr = DataItem
            # Append the extracted leaf/node information to the output string
            OutString = OutString + ItemStr
            SubstitutedString = SubstitutedString + SubsItemStr
            EncapsulatedFunctions  = EncapsulatedFunctions + PreviouslyDetectedEncapsulatedFunctions
            # The invalid flag is raised if any other member is invalid
            if Invalid == '':
                Invalid = WasInvalid
            ParenthesisEnclosed = ItemStr != '' and (ItemStr[0]=='(') and (ItemStr[-1] ==')')
            # If the output flag of the current operation was already raised
            # this means a previous detection of a sequence, meaning that
            # a mathematical operation is not allowed 
            if HasList and ItemStr in AllowedMathOperatorsInExpr:
                if Invalid == '':
                    Invalid = 'Internal Parser Error - Invalid Operator after a vector: a Mathematical operation is not allowed after brackets (representing a vector). Error encountered at the end of this part of the expression: "' + OutString +'"'
                if "ExprParse" in DebugPrints:
                    print 'INVALID - OP AFTER LIST'
                ModifiedString = ModifiedString + '_INVALID_OP_'+ str(ItemStr) +'_AFTER_LIST_'
            # If the retrieved item is enclosed in parenthesis, verify syntax
            # by paying attention to tuples, previously detected lists and
            # function names
            elif (ParenthesisEnclosed or WasTuple ) and Params.has_key(PrevItem) and Params[PrevItem].ParameterType == 'System Reserved':
                # Check if a valid function name was used before parenthesis.
                # If this was a valid function name, indicate this in the
                # modified string by replacing the entire function and 
                # Arguments with a single token
                ModifiedString = ModifiedString[:-len(PrevItem)] + 'VALID_FUNCTION'
                EncapsulatedFunctions  = EncapsulatedFunctions + [PrevItem + ItemStr]
                # note that the use of a function resets the List flags since
                # a function can take list input and return a number
                WasList = False
                HasList = False
                if "ExprParse" in DebugPrints:
                    print 'Function OK'
            elif WasTuple:
                # Otherwise, this means a tuple was created without a call
                # to a function. In this case, set the flags and the modified
                # string to indicate the problem
                HasTuple = True
                if PrevItem !='(':
                    # If the previous parameter is parenthesis, then just pass
                    # upwards in the hierarchy the fact that a tuple was
                    # detected, the next set of parenthesis cannot change the
                    # fact that this is a tuple so unless this is corrected
                    # later by function enclosing the tuple an error will
                    # eventually be generated
                    if Invalid == '':
                        Invalid = 'Internal Parser Error - a comma is not allowed between parenthesis, except as part of a parameter list for a function. The error was encountered at the end of this part of the expression: "' + OutString +'"'
                    if "ExprParse" in DebugPrints:
                        print 'INVALID - TUPLE'
                ModifiedString = ModifiedString + 'INVALID_TUPLE'
            elif WasList:
                # If a list was detected in a node then the expression will
                # be a list as well, this will continue up the tree until
                # a function is encountered
                HasList = True
                if PrevItem in AllowedMathOperatorsInExpr:
                    if Invalid == '':
                        Invalid = 'Internal Parser Error - invalid operator before a vector - a Mathematical operation is not allowed before brackets (representing a vector). The error was encountered at the end of this part of the expression: "' + OutString +'"'
                    if "ExprParse" in DebugPrints:
                        print 'INVALID - OP BEFORE LIST'
                    ModifiedString = ModifiedString + 'INVALID_LIST_AFTER_OP_'+ str(ItemStr) +''
                else:
                    ModifiedString = ModifiedString + 'LIST'
            else:
                # Nothing special was encountered
                ModifiedString = ModifiedString + ModItemStr
            PrevItem = ItemStr
        if len(ParsedTreeAsList) > 2:
            # Check if the new expression is a list
            # Note that originally the regular expression was '\[(.*,.*)*\]'
            # However it was simplified see reason below
            if re.match('^\[.*,.*\]$',ModifiedString) != None:
                ModifiedString = 'LIST'
                HasList = True
                if "ExprParse" in DebugPrints:
                    print OutString + ' Has a list'
            # Check if the new expression is a Tuple
            # Note that originally the regular expression was '\((.*,.*)*\)'
            # However it was simplified since it caused the system to hang
            elif re.match('^\(.*,.*\)$',ModifiedString) != None:
                # There are two cases:
                # Case A: (1,2,3)
                # Case B: (1),(2),(3)
                # Check that this is actually case A by trying to split it
                # into tuple arguments. then seeing if the parenthesis
                # in the first argument are balanced.
                TupleArguments = NestedExpressionArgumentSplit(ModifiedString, EatFunctionWrapper = '()')
                ParenthisisOpen = TupleArguments[0].count('(')
                ParenthisisClose = TupleArguments[0].count(')')
                if ParenthisisOpen == ParenthisisClose:
                    HasTuple = True
                    if "ExprParse" in DebugPrints:
                        print OutString + ' Has a tuple'
            else:
                if "ExprParse" in DebugPrints:
                    print OutString + ' Is not a tuple nor a list'
            if "ExprParse" in DebugPrints:
                print ModifiedString
        if PerformFinalChecks:
            # If a final check is requested, the entire expression is checked
            # for not being a tuple such as x, . Normally this is allowed by
            # python for expressions such as (x,) or [x,]: these examples are
            # caught previously by the function due to the parenthesis. Yet the
            # comma at the end without parenthesis should not be allowed for
            # an entire expression to be interpreted as a tuple.
            if ModifiedString.strip()[-1:] == ',':
                HasTuple = True
                Invalid = 'Internal Parser Error - a comma is not allowed at the end of an expression. The error was encountered at the end of this part of the expression: "' + OutString +'"'
                if "ExprParse" in DebugPrints:
                    print OutString + ' A tuple without parenthesis created by a comma at its end'
        return (Invalid,HasList,HasTuple,ModifiedString,SubstitutedString,OutString,EncapsulatedFunctions)

    def RecursivelyConstruct(self, ExprText = None, BannedParams = None, StartIndex = 0):
        """Expand the expression by recursive substitution of parameters"""
        # This method should not be called externally and should be accessed
        # through ValidateExpr since the context may change
        if BannedParams == None:
            BannedParams = []
        if ExprText == None:
            ExprText = str(self)
        SubstitutionParams = []
        SubstitutionExprssions = []
        RawSubstitutionParams = []
        RawSubstitutionExprssions = []
        # Extract parameters (this also checks these are valid parameters)
        ParamNames = self.ExtractParams(ExprText)
        # Loop through the parameters and replace these with unique identifiers
        # These are required to avoid problems when later replacing parameters
        # with sub expressions containing other parameters in this list
        ConstructedExpr = ExprText
        Index = StartIndex
        for ParamName in ParamNames:
            # Check if a banned parameter
            if ParamName in BannedParams:
                raise ValueError, 'ASSERTION ERROR: The parameter "'+ ParamName +'" was encountered during expression construction, meaning a cyclic (recursive) assignment of this parameter in some expression defined in the list ' + str(BannedParams) + ' that is used in the expression "' + ExprText +'". This should not be possible and indicates some sort of system error or possibly some sort of data corruption. Recreating the database file may indicate the origin of the problem.'
            # Note that since the parameters are processed
            # in their appearance order and since only
            # simple parameters are allowed, it is safe to
            # just replace the first parameter each time
            # and not worry about other parameters that
            # have the same start
            ConstructedExpr = ConstructedExpr.replace(ParamName,'$'+str(Index)+'$' ,1)
            Index = Index+1
        # record the Raw expression        
        RawConstructedExpr = ConstructedExpr
        # Also, this will be the first output string that defines the entire
        # expression. It corresponds to the tree root and therefore has no
        # corresponding param index in RawSubstitutionParams since it is defined
        # at the level above this one
        RawSubstitutionExprssions = RawSubstitutionExprssions + [RawConstructedExpr]
        # record the next to start from for the next batch
        IndexToStartFromNextLevel = Index
        # Loop again through the parameters found in this equation
        Index = StartIndex
        for ParamName in ParamNames:
            if Params[ParamName].Formula != '' and Params[ParamName].ParameterType != 'System Reserved':
                SubExpr = str(Params[ParamName].Formula)
                (SubConstructedExpr, SubSubstitutionParams, SubSubstitutionExprssions, SubRawSubstitutionParams, SubRawSubstitutionExprssions, IndexToStartFromNextLevel) = self.RecursivelyConstruct(SubExpr, [ParamName] + BannedParams, IndexToStartFromNextLevel)
                # Enclose the expression in parenthesis
                SubConstructedExpr = '(' + SubConstructedExpr + ')'
                # Include the replaced param in the set of parameters
                SubSubstitutionParams = [ParamName] + SubSubstitutionParams
                SubSubstitutionExprssions = [SubConstructedExpr] + SubSubstitutionExprssions
                SubRawSubstitutionParams = ['$'+str(Index)+'$'] + SubRawSubstitutionParams
                # Note that this is the responsibility of the called function to
                # give back the raw expression for the current parameter
            else:
                # For system reserved parameters and parameters without
                # a formula are not enclosed in parenthesis
                SubConstructedExpr = ParamName
                SubSubstitutionParams = [ParamName]
                SubRawSubstitutionParams = ['$'+str(Index)+'$']
                SubRawSubstitutionExprssions = [ParamName]                
                SubSubstitutionExprssions = [ParamName]
            # Replace the unique identifier with the expanded expression
            ConstructedExpr = ConstructedExpr.replace('$'+str(Index)+'$', SubConstructedExpr ,1)
            SubstitutionParams = SubstitutionParams + SubSubstitutionParams
            SubstitutionExprssions = SubstitutionExprssions + SubSubstitutionExprssions
            RawSubstitutionParams = RawSubstitutionParams + SubRawSubstitutionParams
            RawSubstitutionExprssions = RawSubstitutionExprssions + SubRawSubstitutionExprssions
            Index = Index+1
        if 'ExprConstruct' in DebugPrints:
            print 'Constructed the following expression: ' + ConstructedExpr
        return (ConstructedExpr, SubstitutionParams, SubstitutionExprssions, RawSubstitutionParams, RawSubstitutionExprssions, IndexToStartFromNextLevel)

    def ValidateExpr(self, ExprText = None, ValidationRule = None):
        """Validate the expression by 3 checks and update the expanded string"""
        UseDataInSelf = ExprText == None
        if UseDataInSelf:
            ExprText = str(self)
        # Ignore empty expressions
        if ExprText != '':
            # An error will be raised if these operations fail
            # Check for parameters
            self.ExtractParams(ExprText)
            # Check if the expression is not recursively defined
            (ExpandedExpressionString, SubstituionParams, ReplacementSubExpressions, RawSubstitutionParams, RawSubstitutionExprssions, IndexToStartFromNextLevel) = self.RecursivelyConstruct(ExprText)
            # Parse the expression and check its syntax
            self.CheckSyntax(ExprText, ValidationRule )
            if UseDataInSelf:
                # If processing the self data, then:
                # 1. use this validation function to check the expression
                # validness. Since this is called with a parameter, then
                # recursion will not happen more than this specific call.
                self.ValidateExpr(ExpandedExpressionString, ValidationRule)
                # If called with self data, Update the expanded expression 
                self.ExpandedExpr = ExpandedExpressionString
                self.DependantParams = SubstituionParams
                self.ReplacementSubExpressions = ReplacementSubExpressions
                self.RawDependants = RawSubstitutionParams
                self.RawReplacement = RawSubstitutionExprssions
        return

    def CheckSyntax(self, ExprText = None, ValidationRule = None):
        """Checks the syntax of the expression and return related information"""
        if ExprText == None:
            ExprText = str(self)
        if ValidationRule not in ['Matrix', None]:
            raise ValueError, 'ASSERTION ERROR: Unknown Validation rule type for an expression'
        # The function will attempt to validate that the expression is valid
        # by performing different checks on the syntax of the expression
        #
        # Test #0 - Banned Keyword is tested during parameter extraction
        #
        # Test #1 - Banned Symbols
        # Check there are no banned symbols in the expression
        for Symbol in BannedSymbolsInExpression:
            if Symbol in ExprText:
                raise ValueError, 'Expression Syntax Check Error: The banned symbol "'+ Symbol +'" was used in the expression "' + str(self) +'". If this expression is valid in another language, please use terminology suitable for this system.' 
        # Test #2 - Expression should parse with the Python parser
        try:
            ParsedTree = parser.expr(str(self))
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Expression Syntax Check Error: The expression has invalid syntax. This error was generated by the python parser. Here are additional details: ' + str(ExceptValue) 
        # Tests #3-5 require analysis of the parsed data and performed together
        # Analyze the parsed expression for rules #3-5
        # Test #3 - No Tuples exists, except when preceded by a function name
        # Test #4 - No operations with lists are allowed
        # Test #5 - The expression can be calculated without error
        ParsedTreeAsList = ParsedTree.tolist()
        (Invalid,HasList,HasTuple,ModifiedString,SubstitutedString,OutString,EncapsulatedFunctions) = self.CheckParsedSyntax(ParsedTreeAsList, True)
        # Report an invalid expression due to rules 3-4
        if Invalid:
            raise ValueError, 'Expression Syntax Check Error: '+ str(Invalid)
        # Complete test 5 by actual evaluation of the substituted string
        try:
            Answer = eval(SubstitutedString)
        except ZeroDivisionError:
            # warn the user that the operation can result in a division by
            # zero in the program,
            MessageToUser('Warning: Note that division by zero can occur in the expression "' +str(self) + '"')
            Answer=''
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            if ExceptType == ValueError and str(ExceptValue) == 'negative number cannot be raised to a fractional power':
                MessageToUser('Warning: Note that a negative number can be raised to a fractional power in the expression "' +str(self) + '"')
                Answer=''
            else:
                raise ValueError, 'Expression Syntax Check Error: The expression was parsed correctly. However it cannot be calculated using dummy parameter values. This may happen if the wrong number of parameters was specified for a function, or if the function generates an error for the dummy value of zero for all parameters. Here are details about the error: ' + str(ExceptValue)
        # Test #6 - The expression is not a list. Note that if a calculated
        # value exists, it is taken into account as well as the parsed value
        IsExprInMatrixForm = (HasList or (Answer != '' and IsList(Answer)))
        if ValidationRule != 'Matrix':
            if IsExprInMatrixForm:
                raise ValueError, 'Expression Syntax Check Error: the expression evaluation will result in a vector or a matrix. This is not allowed unless the system is expecting a Matrix and this was specified as the validation rule for this expression. The expression evaluated was "' +str(self) + '"'
        else:
            if not IsExprInMatrixForm:
                raise ValueError, 'Expression Syntax Check Error: the expression evaluation will result in a value that is not a vector or a matrix, while a matrix/Vector was requested by the user. The expression evaluated was "' +str(self) + '"'
        # Currently it was decided to keep the option of checking the 
        # expression to be a Matrix. If this option is removed the 
        # commented code below will become handy
        #if IsExprInMatrixForm:
        #    raise ValueError, 'Expression Syntax Check Error: the expression evaluation will result in a vector or a matrix. This is not allowed. Make sure the expression is evaluated to a number. The expression evaluated was "' +str(self) + '"'
        # return as output related information
        return (Invalid,HasList,HasTuple,ModifiedString,SubstitutedString,OutString,EncapsulatedFunctions)


    def Evaluate(self, ExprText = None):
        """ Try to evaluate the expression under the given rules """
        if ExprText == None:
            ExprText = str(self)
        if ExprText.strip()!='':
            # this means no default for empty was defined
            try:
                Result = eval(ExprText , EmptyEvalDict)
            except:
                raise ValueError, 'Expression Evaluation Error: The value does not immediately evaluate to a number. Please consider changing the expression. The Expression was "' + str(ExprText) + '"'
            if not IsNumericType(Result):
                raise ValueError, 'Expression Evaluation Error: The value does not evaluate to a numeric type. Please make sure this is not wrong definition of a list in brackets. The Expression was "' + str(self) + '" and the evaluation value is: ' + str(Result)
        else:
            Result = None        
        return Result


    def IsParamDependant(self, ParamName, ExprText=None):
        """ Returns True if dependant on ParamName """
        if ExprText == None:
            ExprText = str(self)
        Result = ParamName in self.FindDependantParams(ParamType = None, ExprText = ExprText)
        return Result

    def FindDependantParams(self, ParamType = None, ExprText=None):
        """ Returns associated parameter names """
        if ExprText == None:
            # Return already created dependant parameters
            Result = self.DependantParams
        else:
            # Force recalculation 
            (ConstructedExpr, FoundParams, ReplacementSubExpressions, RawSubstitutionParams, RawSubstitutionExprssions, IndexToStartFromNextLevel) = self.RecursivelyConstruct(ExprText)
            Result = FoundParams
        # If a datatype is specified filter the results by the data type
        if ParamType != None:
            Result = filter(lambda Entry: Params[Entry].ParameterType == ParamType, Result)
        return Result        

    def GenerateReport(self, FormatOptions = None):
        """ Generate the report for this entity instance """
        TotalIndent = HandleOption('TotalIndent', FormatOptions,'')
        IndentAtom = HandleOption('IndentAtom', FormatOptions,'  ')
        #ColumnSpacing = HandleOption('ColumnSpacing', FormatOptions,' | ')
        FieldHeader = HandleOption('FieldHeader', FormatOptions,True)
        LineDelimiter = HandleOption('LineDelimiter', FormatOptions,'\n')
        SectionSeparator = HandleOption('SectionSeparator', FormatOptions,70*'_')
        ShowHidden = HandleOption('ShowHidden', FormatOptions,False)
        ShowDependency = HandleOption('ShowDependency', FormatOptions,False)
        DetailLevel = HandleOption('DetailLevel', FormatOptions, 0)
        # DetailLevel = 0 prints only the expression
        # DetailLevel = 1 prints additional information
        ReportString = ''
        if str(self) != '':
            # Empty expressions generate no output
            ReportString = ReportString + TotalIndent + FieldHeader * 'Expression :' + str(self) + LineDelimiter
            if DetailLevel > 0:
                if ShowHidden:
                    ReportString = ReportString + TotalIndent + FieldHeader * 'Expanded Expression: ' + str(self.ExpandedExpr) + LineDelimiter
                if ShowDependency:
                    (ConstructedExpr, FoundParams, ReplacementSubExpressions, RawSubstitutionParams, RawSubstitutionExprssions, IndexToStartFromNextLevel) = self.RecursivelyConstruct()
                    FoundParamsReduced = SetDiff(FoundParams,ExpressionSupportedFunctionsAndSpecialNames)
                    for FoundParam in FoundParamsReduced:
                        ReportString = ReportString + TotalIndent + FieldHeader * 'Depends on: ' + str(FoundParam) + LineDelimiter
                        if Params[FoundParam].Formula != '':
                            RevisedFormatOptions = HandleOption('TotalIndent', FormatOptions, TotalIndent + IndentAtom, True)
                            RevisedFormatOptions = HandleOption('DetailLevel', RevisedFormatOptions, DetailLevel-1, True)
                            ReportString = ReportString + Params[FoundParam].GenerateReport(RevisedFormatOptions)
                # Show the function descriptions
                (Invalid,HasList,HasTuple,ModifiedString,SubstitutedString,OutString,EncapsulatedFunctions) = self.CheckSyntax()
                ComparisonOperatorDict = {'Eq':'=','Ne':'<>','Gr':'>','Ge':'>=','Ls':'<','Le':'<='}
                FunctionsWithExplanations = sorted(['Table', 'Iif'] + ComparisonOperatorDict.keys())
                for EncapsulatedFunction in EncapsulatedFunctions:
                    EncapsulatedFunctionName = EncapsulatedFunction[:EncapsulatedFunction.find('(')]
                    if EncapsulatedFunctionName in FunctionsWithExplanations:
                        ReportString = ReportString + TotalIndent + FieldHeader * ('The sub-expression: ' + str(EncapsulatedFunction) + ' means: ') + LineDelimiter
                        if EncapsulatedFunctionName == 'Table':
                            TableToAnalyze = TableClass(InitString = EncapsulatedFunction)
                            ReportString = ReportString + TableToAnalyze.GenerateReport(FormatOptions)
                        elif EncapsulatedFunctionName == 'Iif':
                            Arguments = NestedExpressionArgumentSplit(EncapsulatedFunction, EatFunctionWrapper = '()')
                            ReportString = ReportString + TotalIndent + IndentAtom + 'If ' + Arguments[0] + ': '+ LineDelimiter
                            ReportString = ReportString + TotalIndent + IndentAtom + IndentAtom + 'Then return (' + Arguments[1] + ') '+ LineDelimiter
                            ReportString = ReportString + TotalIndent + IndentAtom + IndentAtom + 'Else return (' + Arguments[2] + ') '+ LineDelimiter
                        elif EncapsulatedFunctionName in ComparisonOperatorDict.keys():
                            Arguments = NestedExpressionArgumentSplit(EncapsulatedFunction, EatFunctionWrapper = '()')
                            OperatorSignText = ComparisonOperatorDict[EncapsulatedFunctionName]
                            ReportString = ReportString + TotalIndent + IndentAtom + 'Return 1 if ' + Arguments[0] + OperatorSignText + Arguments[1] + ', return 0 otherwise.'+ LineDelimiter
            ReportString = ReportString + TotalIndent + SectionSeparator + LineDelimiter
        return ReportString


    def RenameExpressionTokens(self, TempTokenPrefix, ExprText=None):
        """ Returns expression construction steps using given prefix """
        # This function returns a set of expressions that if evaluated
        # in the given order, they will reconstruct the expanded expression.
        # The leafs of the expression tree are replaced by the tokens
        # corresponding to the variables used, intermediate nodes are
        # replaced by temporary variables that get the prefix given by 
        # TempTokenPrefix enumerated. The output is returned as several lists:
        # AssignedVariables : A list of names, all starting with TempTokenPrefix
        #                     that will be on the receiving side of an =
        #                     operator during assignment. The variables
        #                     are sorted according to execution order
        # AssignedExpressions : A list of expressions, that use existing
        #                       parameter names and variables that are already 
        #                       previously listed in AssignedVariables with 
        #                       a lower index. 
        # AssociatedParameterNames : A list of parameter names that correspond
        #                            to nodes in the expression tree. This list
        #                            corresponds to AssignedVariables and its
        #                            last component is always None since it
        #                            corresponds to the value of the expression
        #                            and to a given parameter.
        # AssociatedExpandedExpressions : A list of expressions that expand
        #                                 nodes in the expression tree. This 
        #                                 corresponds to AssignedVariables and 
        #                                 last component is equal to the entire
        #                                 expression fully expanded
        if ExprText == None:
            TheExpr = self
        else:
            TheExpr = Expr(ExprText)
        # The associated parameters are the same as the dependant parameters,
        # only reversed, with None at the end to represent the full expression
        AssociatedParameterNames = list(reversed(TheExpr.DependantParams)) + [None]
        # The expanded expressions also receive the same treatment only
        # the fully expanded expression is at the end
        AssociatedExpandedExpressions = list(reversed(TheExpr.ReplacementSubExpressions)) + [TheExpr.ExpandedExpr]
        # The expressions are initialized to the RawReplacements and will be
        # replaced later with the proper variable names
        AssignedExpressions = TheExpr.RawReplacement[:]
        AssignedVariables = []
        # now traverse each dependant in the RawDependants list.
        for RawName in TheExpr.RawDependants:
            # The new variable name will have the same number ending as the
            # raw variable. Essentially, the $ signs are stripped and a prefix
            # is added
            NewVariableName = TempTokenPrefix + RawName[1:-1]
            AssignedVariables = AssignedVariables + [NewVariableName]
            # Now loop through all expressions and construct a new set of
            # expressions that replace the RawName with NewVariableName
            # Note that only the first occurrence is replaced. This can serve
            # as an assertion check since in case of some error, this may
            # expose this error later in the program.
            ReplacedAssignedExpressions = [Entry.replace(RawName,NewVariableName,1) for Entry in AssignedExpressions]
            AssignedExpressions = ReplacedAssignedExpressions
        # Finally, reverse the lists to match execution order.
        # Also add the Variable Prefix itself to the end of the
        # AssignedVariables list. This is to indicate that the last
        # expression goes into the temporary variable without numeric
        # suffix. 
        AssignedVariables = list(reversed(AssignedVariables)) + [TempTokenPrefix]
        AssignedExpressions = list(reversed(AssignedExpressions))
        return (AssignedVariables, AssignedExpressions, AssociatedParameterNames, AssociatedExpandedExpressions)


    def WriteCodeForExpression (self, AssignedParameterName, SourceExprText = None, ValidateDataInRuntime = DefaultSystemOptions['ValidateDataInRuntime'], WriteLnFunction = None, Lead = None, Tab = None, TempTokenPrefix = None, OverrideLastCheck = None):
        """ Write code to regenerate expression """
        # This code is reused several times in the code and recreates
        # the expression provided in SourceExprText, to be put into the 
        # AssignedParameterName. if SourceExprText is not defined, self is
        # used as the expression.
        # WriteLnFunction defines a function to write
        # the code and defaults to an internal print statement. Lead defines
        # the lead before any statement being written, it can be used to define
        # the indentation level and defaults to ''. Tab defines the length of
        # the Tab indentation and defaults to 4*' '
        # TempTokenPrefix defines the temporary variable name prefix and
        # defaults to '_Temp' 
        # The Level of validation held in ValidateDataInRuntime:
        # 3 : it is the slowest and most extensive level where all
        #     input parameters are checked before used. This constitutes
        #     a double check since a parameter will be checked both
        #     when assigned a value and when this value is reused.
        #     This is a redundant check of each variable and does not 
        #     add any logical value other than assertion.
        #     This is unnecessary slow, yet the strictest check that
        #     may discover problems due to the redundant checks. 
        #     This option should be used for debugging purposes.
        # 2 : This is the default option where each receiving parameter
        #     is checked upon receiving a value to see if the new value
        #     fits its characteristics. This means that intermediate
        #     parameters with formulas are checked to see if the new
        #     calculated value fits their bounds. Also the final 
        #     evaluate expression is validated against the parameter
        #     that will finally hold it
        # 1 : At this level only one check is made when the entire
        #     expression is expanded and the final evaluated value is 
        #     is about to be assigned to the parameter that will
        #     hold it. No intermediate checks are made and parameter 
        #     function bounds can be violated. Note that this is used
        #     also when calculating temporary variables such as
        #     probabilities.
        # 0 : No validity chacks are made and the values are passed
        #     without bound checking
        # In any case ignore function names and system reserved parameters
        # There is no validity check for these types.
        # if OverrideLastCheck is not None than the check of the last parameter
        # is replaced by a check that is defined by the strings supplied in the
        # sequence. These strings are written consequetively 
        
        def DefaultWriteLnFunction (InStr):
            """ Dummy defualt write line function """
            print InStr

        if SourceExprText == None:
            SourceExpr = self
        else:
            SourceExpr = Expr(SourceExprText)
        if WriteLnFunction == None:
            WriteLnFunction = DefaultWriteLnFunction            
        if Lead == None:
            Lead = ''
        if Tab == None:
            Tab = ' '*4
        if TempTokenPrefix == None:
            TempTokenPrefix = '_Temp'

        # Traverse all building steps fo the expression according to its
        # already parsed tree
        (AssignedVariables, AssignedExpressions, AssociatedParameterNames, AssociatedExpandedExpressions) = SourceExpr.RenameExpressionTokens('_Temp')
        # replace last empty associated name with final parameter name
        # the entire expression will be assigned to
        AssociatedParameterNames[-1] = AssignedParameterName
        # Now write the different steps
        NumberOfBuildSteps = len(AssignedVariables)
        WriteLnFunction (Lead + '_LastExpressionString = "Processing the expression: ' + AssignedParameterName + ' = ' + str(SourceExpr)+ ' ."')
        WriteLnFunction (Lead + '# This expression should expand to: ' + AssignedParameterName + ' = ' + SourceExpr.ExpandedExpr)
        WriteLnFunction (Lead + 'try:')
        for ExpressionBuildStep in range(NumberOfBuildSteps):
            # Write the comment
            WriteLnFunction (Lead + Tab + '# Building Step #' + str(ExpressionBuildStep) + ': ' + AssociatedParameterNames[ExpressionBuildStep] + ' = ' + AssociatedExpandedExpressions[ExpressionBuildStep])
            # write the actual command
            WriteLnFunction (Lead + Tab + AssignedVariables[ExpressionBuildStep] + ' = ' + AssignedExpressions[ExpressionBuildStep])
            # now we can perform validity checks according to
            # ValidateDataInRuntime
            AssociatedParamName = AssociatedParameterNames[ExpressionBuildStep]
            # The last parameter name may be defined as not a parameter and
            # therefore may be ignored here and later checked by the program
            if ( ValidateDataInRuntime >=3 or (ValidateDataInRuntime >=2 and AssociatedParameterNames[ExpressionBuildStep] != AssignedExpressions[ExpressionBuildStep]) or (ValidateDataInRuntime >=1 and ExpressionBuildStep == len(AssignedExpressions)-1) ):
                if (OverrideLastCheck != None and ExpressionBuildStep == NumberOfBuildSteps - 1):
                    # The last parameter may have special treatment if the user
                    # defined the OverrideLastCheck parameter 
                    for OverrideCheckLine in OverrideLastCheck:
                        WriteLnFunction (Lead + Tab + OverrideCheckLine)
                elif Params[AssociatedParamName].ParameterType in ['Number','Integer','Expression']:
                    ValidateBounds = Params[AssociatedParamName].ValidationRuleParams != ''
                    ValidateInteger = Params[AssociatedParamName].ParameterType == 'Integer'
                    if ValidateInteger or ValidateBounds:
                        WriteLnFunction (Lead + Tab + 'try:')
                        if ValidateBounds:
                            # extract the bounds as strings by splitting the list
                            # that looks like '[a,b]' into 'a','b'
                            BoundStrings = Params[AssociatedParamName].ValidationRuleParams.strip()[1:-1].split(',')
                            WriteLnFunction (Lead + Tab + Tab + 'if not (' + BoundStrings[0] + ' <=' + AssignedVariables[ExpressionBuildStep] +' <= ' + BoundStrings[1] + ') :')
                            WriteLnFunction (Lead + Tab + Tab + Tab + 'raise ValueError, "Run time bound check error: the value calculate for ' + AssociatedParamName + ' does not fall within the specified validation bounds provided. The specified bounds were: ' + str(Params[AssociatedParamName].ValidationRuleParams) + ' and the evaluated value was: " + repr('+ AssignedVariables[ExpressionBuildStep] +')')
                        if ValidateInteger:
                            # Validate an integer by rounding it
                            WriteLnFunction (Lead + Tab + Tab + 'if round('+ AssignedVariables[ExpressionBuildStep] +') != '+ AssignedVariables[ExpressionBuildStep] +':')
                            WriteLnFunction (Lead + Tab + Tab + Tab + 'raise ValueError, "Run time integer check error: the value calculate for ' + AssociatedParamName + ' is not an integer as specified. The evaluated value was: " + repr('+ AssignedVariables[ExpressionBuildStep] +')')
                        WriteLnFunction (Lead + Tab + 'except:')
                        WriteLnFunction (Lead + Tab + Tab + '_WarningErrorHandler()')   
        WriteLnFunction (Lead + 'except:')
        WriteLnFunction (Lead + Tab + '_WarningErrorHandler(_InputErrorString = _LastExpressionString, _FatalError = True)')
        # write the line that actually assigns the expression value
        # to the parameter
        WriteLnFunction (Lead + '# Expression building complete - assign to destination parameter ' )
        WriteLnFunction (Lead + AssignedParameterName + ' = ' + AssignedVariables[-1])
        return



class TableClass():
    """Defines a multidimensional table with values, dimensions, and ranges"""
    DescriptionStr = None  # The string that initially defined the table
    DimNum = 0    # The number of dimensions in the table
    Sizes = []    # A sequence containing the size of each dimension
    Values = []   # A multidimensional sequence defining the table
    Dimensions = [] # A list of tuples of the form (DimensionName , DimRange)
                    # where Dimension name is a string and DimRange is
                    # a list of values
    FlatValues = [] # The same as Values, only flattened into a list with
                    # a single dimension
    DataItemsNum = 0 # A number representing the total number of table elements

    def __init__( self , InitString = None , DimensionsArray = None, ValuesArray = None , ParseOnly = False):
        """Constructor with default values and some consistency checks"""
        # Note that the constructor shuld handle both construction by arguments
        # and construction as string since both runtime and compile time
        # Table are possible and use the same code. For example Tables are used
        # for report generation where the text form is used.
        # Note that currently two inpur formats are supported: the new format
        # that uses lists and the old format that uses a string. 
        # The old format is being rolled out and is declared deprecated.
        def VerifySizes(Sizes, Values):
            """Verify Recursively that Value array corresponds to Sizes"""
            # An Error will be raised if mismatch, otherwise True Returned
            # If reached an empty list of size
            if Sizes == []:
                if IsList(Values):
                    raise ValueError, "Table Size Validation Error: Table sizes do not match array sizes - the data contains more dimensions than the size."
            else:
                # if the size still exists
                if not IsList(Values):
                    raise ValueError, "Table Size Validation Error: Table sizes do not match array sizes - the size contains more dimensions than the data - expected size " + str(Sizes[0]) + " with the subset " + str(Values) + " ."
                elif len(Values)!=Sizes[0]:
                    raise ValueError, "Table Size Validation Error: Table sizes do not match array sizes - expected size " + str(Sizes[0]) + " got " + str(len(Values)) + " with the subset " + str(Values) + " ."
                else:
                    for Element in Values:
                        VerifySizes(Sizes[1:], Element)
            # This means ok with this dimension
            return True
        # Define a local constant string that will for error messages
        # Define as a function to skip calculations unless needed
        def TableDescriptionErrorString(self):
            return 'The format should be : DimensionsArray, ValueArray. Where DimensionsArray = [[DimName, [DimRange,..],..]] , ValueArray = [..[NestedValues]..] .  The table expression was: "' + self.Description() + '"'
            
        def ReturnNumericOrString(Item):
            'Returns a numeric value from string if possible otherwise string'
            try:
                # try to evaluate this to a number
                ItemVal = eval (Item , EmptyEvalDict)
                if not IsNumericType(ItemVal):
                    raise ValueError , "Non Numeric Type Detected"
            except:
                # if not evaluated properly, retain the string
                ItemVal=Item
            return ItemVal
        
        # Figure out if old format or new format were used.
        if InitString == None:
            NewTableFormat = True
            Dimensions = DimensionsArray
            Values = ValuesArray
        else:
            try:
                # If the information is provided via an initializing string        
                # Init the table by converting the data in InitString
                # Start with removing the word Table
                TempStr = InitString.strip()
                if not TempStr.startswith('Table'):
                    raise ValueError, 'Table Expression Validation Error: The table expression is missing the keyword "Table" in the beginning of the expression. The expression was: "' + InitString + '"'
                TempStr = TempStr[5:].strip()
                if TempStr[0] != '(' or TempStr[-1] != ')':
                    raise ValueError, 'Table Expression Validation Error: The table is not specified in function form - parenthesis are missing. The expression was: "' + InitString + '"'
                if "Table" in DebugPrints:
                    print 'DEBUG - Table Description = ' + str(InitString)
                SplitArguments = NestedExpressionArgumentSplit(InitString, EatFunctionWrapper = '()')
                # if a list is detected, then we know the new format is used
                if len(SplitArguments) == 2 and SplitArguments[0][0]=='[' and SplitArguments[0][-1]==']' and SplitArguments[1][0]=='[' and SplitArguments[1][-1]==']':
                    NewTableFormat = True
                    # Preprocess the information so that it can be used with
                    # the same code that initializes data.
                    # First figure out table size
                    DimSplit = NestedExpressionArgumentSplit(SplitArguments[0][1:-1])
                    Dimensions = []
                    # start parsing the dimension list
                    try:
                        for DimLine in DimSplit:
                            if DimLine[0]!='[' or DimLine[-1]!=']':
                                raise ValueError, 'Range should be a list'
                            DimLineSplit = NestedExpressionArgumentSplit(DimLine[1:-1])
                            # The format is Name followed by a range list
                            DimName = ReturnNumericOrString(DimLineSplit[0])
                            DimRangeString = DimLineSplit[1]
                            if DimRangeString[0]!='[' or DimRangeString[-1]!=']':
                                raise ValueError, 'Range should be a list'
                            DimRangeSplit = NestedExpressionArgumentSplit(DimRangeString[1:-1])
                            DimLineVal = []
                            for Item in DimRangeSplit:
                                ItemVal = ReturnNumericOrString(Item)
                                DimLineVal.append(ItemVal)
                            Dimensions.append([DimName,DimLineVal])
                    except:
                        raise ValueError, 'Table Expression Validation Error: invalid DimensionsArray was deteted that could not be parsed. ' + TableDescriptionErrorString(self)
                    # If reaced this far, parse the values. Note that this is 
                    # done level by level to support expressions within the 
                    # table values.
                    def ReconstrcutBySplitting(CurrentLevelData, LevelsToGo):
                        "Reconstructs multidimentional array from string"
                        # first split at commas
                        StrippedCurrentLevelData = CurrentLevelData.strip()
                        if len(StrippedCurrentLevelData)<2 or (StrippedCurrentLevelData[1] != '[' and  StrippedCurrentLevelData[-1] != ']'):
                            raise ValueError, 'Split Error: Could not find sequence markers at beginning and end of string ' + repr(StrippedCurrentLevelData) + ' - check the declared dimension level'
                        CurrentSplitLevel = NestedExpressionArgumentSplit(StrippedCurrentLevelData[1:-1])
                        ReturnArray = []
                        for Item in CurrentSplitLevel:
                            if LevelsToGo == 1:
                                ItemVal = ReturnNumericOrString(Item)
                            else:
                                ItemVal = ReconstrcutBySplitting(Item, LevelsToGo-1)
                            ReturnArray.append(ItemVal)
                        return ReturnArray
                    try:
                        Values = ReconstrcutBySplitting(SplitArguments[1],len(Dimensions))
                    except:
                        raise ValueError, 'Table Expression Validation Error: invalid ValuesArray was deteted that could not be parsed. ' + TableDescriptionErrorString(self)
                else:
                    # This is is about to be deprecated
                    NewTableFormat = False
            except:
                raise ValueError, 'Table Expression Validation Error: invalid Input was deteted that could not be parsed. ' + TableDescriptionErrorString(self)

        if NewTableFormat:
            # reset description
            DescriptionStr = None
            # in case the init string was not specified as a string then it is 
            # Assumed that the user supplied the data as nested lists. This is
            # much faster to process for the system
            if not IsList(Dimensions) or not IsList(Values):
                raise ValueError, 'Table Expression Validation Error: invalid Input to Table DimensionsArray, ValueArray are not lists. ' + TableDescriptionErrorString(self)
            DimNum = len(Dimensions)
            # Interpret the number of dimensions
            Sizes = []
            DataItemsNum = 1
            for Dim in range(DimNum):
                # check validity of list
                if not IsList(Dimensions[Dim]):
                    raise ValueError, 'Table Expression Validation Error: invalid DimensionsArray that does not contain lists. ' + TableDescriptionErrorString(self)
                DimSize = len(Dimensions[Dim][1])-1
                # check that the size is not invalid
                if DimSize < 1:
                    raise ValueError, 'Table Expression Validation Error: invalid DimensionsArray with list smaller than 2 range elements for Dimension #' + str(Dim) + '. ' + TableDescriptionErrorString(self)
                Sizes.append(DimSize)
                DimensionName = Dimensions[Dim][0]
                DimRange = Dimensions[Dim][1]
                IsCategorical = IsNaN(DimRange[0])
                for ItemEnum in range(IsCategorical+1, DimSize+1):
                    if DimRange[ItemEnum-1] > DimRange[ItemEnum]:
                        raise ValueError, 'Table Expression Validation Error: Range bound items are not sorted in ascending order: ' + SmartStr(DimRange[ItemEnum-1]) + ' is higher than ' + SmartStr(DimRange[ItemEnum]) + '. ' + TableDescriptionErrorString(self)
                DataItemsNum = DataItemsNum * DimSize
            # Now validate that Values is of valiid Sizes
            try:            
                VerifySizes(Sizes, Values)
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                raise ValueError,  'Table Expression Validation Error: ' + str(ExceptValue) + ' ' + TableDescriptionErrorString(self)
            # To speed up computation, the following FlatValues remains empty
            # these are relevant only in the old format
            FlatValues = None
        else:
            # Define a local constant string that will be used for error messages
            # THIS CODE IS CANDIDATE FOR DEPRECATION !!!
            MessageToUser("Old Table format is deprecated - Please use the faster new format")
            # The description holds only the data
            DescriptionStr = TempStr[1:-1]
            TableDescriptionErrorString = 'The Table Input argument pattern is: D,N_1,N_2,...,N_D,V_1...V_(N1*N2*...*ND),{M_1,R_1_0...R_1_(N_1)}......{M_(N_D),R_D_0...R_D_(N_D)}. D defines the number of dimensions, N_i the dimension size for dimension i, V_i table values, M_i dimension names, R_i_j, the j range bound item for dimension i.'
            # old version text was: Items = Description.split(',')
            Items = NestedExpressionArgumentSplit(InitString, EatFunctionWrapper = '()')
            # Remove leading and following spaces from each item in items
            Items = map (lambda Item: Item.strip() , Items)
            # Interpret the number of dimensions
            try:
                DimNum = int (Items[0])
            except:
                raise ValueError, 'Table Expression Validation Error: A non integer number was detected for the number of dimensions D. ' + TableDescriptionErrorString + ' The table expression was: "' + InitString + '"'
            else:
                if not IsNumericType(DimNum) or DimNum<1:
                    raise ValueError, 'Table Expression Validation Error: A non positive number was detected for the number of dimensions. The first argument of a table represents the number of dimensions. The table expression was: "' + InitString + '"' 
            if "Table" in DebugPrints:
                print 'DEBUG - Table DimNum = ' + str(DimNum)
            # Verify there is enough information about sizes
            if len(Items) < DimNum+1:
                raise ValueError, 'Table Expression Validation Error: Not enough elements to define the sizes of the table. ' + TableDescriptionErrorString + ' There were not enough numbers to define N_i in the given definition. The table expression was: "' + InitString + '"' 
            # Interpret the number of dimensions
            Sizes = []
            DataItemsNum = 1
            SupportingItemsNum = 0
            for Item in Items[1 : DimNum+1]:
                try:
                    Size = eval (Item , EmptyEvalDict)
                except:
                    raise ValueError, 'Table Expression Validation Error: Dimension size does not represent a number. ' + TableDescriptionErrorString + ' At least one of the N_i values does not evaluate to a number. The table expression was: "' + InitString + '"'
                else:
                    if not IsNumericType(Size) or Size<1:
                        raise ValueError, 'Table Expression Validation Error: Dimension size does not represent a positive number. ' + TableDescriptionErrorString + ' At least one of the N_i values does not evaluate to a positive number. The table expression was: "' + InitString + '"'
                    Sizes = Sizes + [Size]
                    DataItemsNum = DataItemsNum * Size
                    SupportingItemsNum = SupportingItemsNum + 2 + Size
            if "Table" in DebugPrints:
                print 'DEBUG - Table Sizes = ' + str(Sizes)
            if len(Items) != 1 + DimNum + SupportingItemsNum + DataItemsNum:
                raise ValueError, 'Table Expression Validation Error: The number of information items is incompatible with the size of the table. ' + TableDescriptionErrorString + ' There were not enough / too many members in the string to accommodate all the information as defined by D and N_i. The table expression was: "' + InitString + '"' 
            # Convert the data into a sequence
            IndexVector = [0] * DimNum
            FlatSequenceString = '['
            SequenceString = '[' * DimNum
            for Item in Items[DimNum+1 : DimNum+DataItemsNum+1]:
                # If the input data in the string is evaluated to a number,
                # the item will be a number. Otherwise it will be a string
                # representing an expression
                if ParseOnly:
                    # if only parsing, make sure it is a valid expression
                    try:
                        Expr(Item)
                    except:
                        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                        raise ValueError, 'Table Expression Validation Error: Table data value items in the table should become numeric. The item "' + str(Item) + '" is not valid. ' + TableDescriptionErrorString + ' The table expression was: "' + InitString + '". Here are additional details on the Error: ' + str(ExceptValue)
                else:
                    # in this case just make sure this is a number
                    # note that 1+2 or a similar constant expression 
                    # is still considered a number
                    try:
                        ItemVal = eval (Item , EmptyEvalDict)
                        if not IsNumericType(ItemVal):
                            raise ValueError , "Non Numeric Type Detected"
                    except:
                        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                        raise ValueError, 'Table Expression Validation Error: Table data value items in the table should be numeric. The item "' + str(Item) + '" is not valid. ' + TableDescriptionErrorString + ' The table expression was: "' + InitString + '" . Here are additional details on the Error: ' + str(ExceptValue)
                ItemToAdd = Item
                DimIndex = DimNum -1
                Separator=','
                # Increase index vector first digit
                IndexVector[DimIndex] = IndexVector[DimIndex]+1
                while DimIndex >=0 and IndexVector[DimIndex] == Sizes[DimIndex]:
                    # Reset current dimension index counter
                    IndexVector[DimIndex] = 0
                    # Add parenthesis to a proper separator
                    Separator = ']'+ Separator +'[' 
                    # Increase the index counter
                    DimIndex = DimIndex - 1
                    # Increase the next dimension index counter
                    if DimIndex >=0:
                        IndexVector[DimIndex] = IndexVector[DimIndex]+1
                SequenceString = SequenceString + ItemToAdd + Separator
                FlatSequenceString = FlatSequenceString + ItemToAdd + ','
            # Remove the unneeded brackets at the end
            SequenceString = SequenceString[0 : -(DimNum+1)]
            FlatSequenceString = FlatSequenceString[0:-1] +']'
            # After the string is created turn it into a sequence
            Values = eval(SequenceString, EmptyEvalDict)
            FlatValues = eval(FlatSequenceString, EmptyEvalDict)
            if "Table" in DebugPrints:
                print 'DEBUG - Table Values = ' + str(Values)
            ### Organize the dimension names and ranges in tuples
            Pos = DimNum+DataItemsNum+1
            Dimensions = []
            for DimIndex in range(DimNum):
                DimensionName = Items[Pos]
                DimRangeInText = Items[Pos+1 : Pos+2+Sizes[DimIndex]]
                # Check validity of the dimension name
                if ParseOnly:
                    # If only validating the table structure, dimension
                    # names should not appear. Instead only numbers are
                    # expected. Assert this:
                    try:
                        float(DimensionName)
                    except:
                        raise ValueError, 'ASSERTION ERROR: found a non number:' + str(DimensionName) +'" while in validate only mode while defining a table'
                else:
                    # In non validation mode, the dimension name should be
                    # a valid Expression.
                    try:
                        Expr(DimensionName)
                    except:
                        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                        raise ValueError, 'Table Expression Validation Error: The table dimension "' + str(DimensionName) +'" contains an invalid expression. Here the table processed' + TableDescriptionErrorString + ' The table expression was: "' + InitString + '" . Here are additional details on the Error: '+ str(ExceptValue)
    
                DimRange = []
                for Item in DimRangeInText:
                    try:
                        ItemVal = eval (Item , EmptyEvalDict)
                    except:
                        raise ValueError, 'Table Expression Validation Error: Range bound item could not be evaluated. Received the value: "' + Item +'". ' + TableDescriptionErrorString + ' The table expression was: "' + InitString + '"' 
                    else:
                        if not IsNumericType(ItemVal):
                            raise ValueError, 'Table Expression Validation Error: Range bound items must be either a number or NaN. Received the value: "' + Item +'". ' + TableDescriptionErrorString + ' The table expression was: "' + InitString + '"'
                    # Check that items are ordered in increasing order
                    if DimRange != [] and not IsNaN(DimRange[-1]) and DimRange[-1] > ItemVal:
                        raise ValueError, 'Table Expression Validation Error: Range bound items are not sorted in ascending order: ' + SmartStr(DimRange[-1]) + ' is higher than ' + str(ItemVal)+'. ' + TableDescriptionErrorString + ' The table expression was: "' + InitString + '"'
                    # Add these to the range
                    DimRange = DimRange + [ItemVal]
                # Add the tuple of Name and the range to the Dimensions vector
                Dimensions = Dimensions + [(DimensionName,DimRange)]
                # Update the position in the text
                Pos = Pos + 2 + Sizes[DimIndex]
            if "Table" in DebugPrints:
                print 'DEBUG - Table Dimensions = ' + str(Dimensions)
        # Transfer calculated data to class members
        self.DescriptionStr = DescriptionStr
        self.DimNum = DimNum
        self.Sizes = Sizes
        self.Values = Values
        self.FlatValues = FlatValues
        self.DataItemsNum = DataItemsNum
        self.Dimensions = Dimensions
        if "Table" in DebugPrints:
            print  DescriptionStr
            print  DimNum
            print  Sizes
            print  Values
            print  Dimensions
        return        


    def LocateDimIndex(self, DimName):
        """ Returns the index of a specific DimName in the Table"""
        # Compare the DimName to the dimension vector
        ReturnDimIndex = None
        for (DimEnum, (DimensionName , DimRange)) in enumerate(self.Dimensions):
            if DimensionName == DimName:
                ReturnDimIndex = DimEnum
        return ReturnDimIndex

    def LocateDimAndRangeIndex(self, DimName, Value):
        """ Locates the dimension index and range subscript index"""
        # The function returns a tuple holding the indices for the dimension and
        # for the range in the form (DimIndex, RangeIndex)
        #
        # Try to locate this dimension in the source table
        DimIndex = self.LocateDimIndex(DimName)
        # If the dimension is in the source table
        if DimIndex != None:
            if IsNaN(Value):
                RangeIndex = NaN
            else:
                # Create a copy of the list vector since it will be
                # changed and we do not want to make changes in the
                # original
                RangeCopy = self.Dimensions[DimIndex][1][:] 
                # if indexed array, replace NaN with -inf
                if IsNaN(RangeCopy[0]):
                    RangeCopy[0] = -Inf
                try:
                    # find the index in the range.
                    CellRangeHigh = Value
                    RangeIndex = map( lambda LowBound, HighBound: LowBound < CellRangeHigh <= HighBound, RangeCopy[:-1], RangeCopy[1:]).index(True)
                except:
                    raise ValueError,'Locate Dimension and Range Error: No dimension %s with the value %g in the range' % (DimName, Value)
        else:
            # If the dimension is not found return None
            RangeIndex = None        
        return (DimIndex, RangeIndex)
        
    def Description(self):
        """ return a string that describes the table """
        # if this is a new table format
        if self.DescriptionStr == None:
            DescriptionStr = SmartStr( (self.Dimensions , self.Values) )
        else:
            DescriptionStr = self.DescriptionStr
        return DescriptionStr

    def Evaluate(self):
        """ Evaluate the return value of a parsed table"""
        # The function assumes that the values for DimensionName in the
        # dimensions are known and are already there
        # Init the result to the entire value multidimensional table set
        Value = self.Values
        for Dim in range(self.DimNum):
            # Traverse the indices and create the index vector
            (DimensionName,DimRange) = self.Dimensions[Dim]
            # Extract the value - at this point it is assumed that the
            # name has been replaced with a value that will be evaluated
            try: 
                DimensionNameValue = float(DimensionName)
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                raise ValueError, 'Table Evaluation Error: The dimension value for dimension #' + str(Dim) + ' : "' + str(self.Dimensions[Dim]) + '" should hold a number. The original input parameters for the table were ' + self.Description() + ' Here are further details about the error: ' + str(ExceptValue)
            # Check the validity of the accessed data
            if IsNaN(DimRange[0]):
                # If the data is categorical, check that the index is correct
                RangeToLookAt = DimRange[1:]
                if DimensionNameValue not in RangeToLookAt:
                    raise ValueError, 'Table Evaluation Error: Table access index not in defined in the index range defined by the range bounds. The Value ' + str(DimensionNameValue) + ' is not in the specified categorical range ' + SmartStr(DimRange[1:])[1:-1] + ' for dimension #' + str(Dim) + ' : "' + SmartStr(self.Dimensions[Dim]) + '". The original input parameters for the table were ' + self.Description() 
                Index = RangeToLookAt.index(DimensionNameValue)
            else:
                # If the data is continuous, find the correct index
                if DimensionNameValue < DimRange[0] or DimensionNameValue > DimRange[-1]:
                    raise ValueError, 'Table Evaluation Error: Table access value is not in the continuous range defined by the range bounds. The Value ' + str(DimensionNameValue) + ' is not in the specified categorical range ' + SmartStr(DimRange)[1:-1] + ' for dimension #' + str(Dim) + ' : "' + SmartStr(self.Dimensions[Dim]) + '". The original input parameters for the table were ' + self.Description()
                Index = 0
                while DimensionNameValue > DimRange[Index]:
                    Index = Index +1
                # Correct the index since the ranges are intervals and the first
                # index should be ignored:
                Index = Index -1
                if Index >= len(DimRange)-1:
                    raise ValueError, 'ASSERTION ERROR: search index is out of range'
            # Reduce the multidimensional table by accessing it with the
            # calculated index to eliminate the topmost dimension
            Value = Value[Index]
        return Value

    def VecIndexToFlatIndex(self, IndexVec, Sizes=None):
        """ Transfer a vector Type index to a flat index to a vector"""
        if Sizes == None:
            Sizes = self.Sizes
            DimNum = self.DimNum
        else:
            DimNum = len(Sizes)
        if len(IndexVec) != DimNum:
            raise ValueError, 'ASSERTION ERROR: Length of Index is not the same as table dimension'
        FlatIndex = 0
        PrepareForNext = 0
        DimIndex = 0
        EndLoopIndex = DimNum - 1
        while True:
            Entry = IndexVec[DimIndex]
            # Traverse DimIndex
            if not (0 <= Entry < Sizes[DimIndex] or IsNaN(Entry)):
                raise ValueError, 'ASSERTION ERROR: Index is out of range for at least one dimension'
            FlatIndex = Entry + PrepareForNext
            # Check if the exit point has been reached
            if DimIndex >= EndLoopIndex:
                break
            DimIndex = DimIndex + 1
            PrepareForNext = FlatIndex * Sizes[DimIndex]
        return FlatIndex

    def FlatIndexToVecIndex(self, FlatIndex, Sizes=None):
        """ Transfer a vector Type index to a flat index to a vector"""
        if Sizes == None:
            Sizes = self.Sizes
            DimNum = self.DimNum
        else:
            DimNum = len(Sizes)
        FlatVecLength = ProdOp(Sizes)
        if not (0 <= FlatIndex < FlatVecLength):
            raise ValueError, 'ASSERTION ERROR: Input flat index is out of allowed range as defined by the table sizes'
        IndexVec = [NaN]*DimNum
        Reminder = FlatIndex
        DimIndex = DimNum - 1
        while True:
            # Traverse DimIndex downwards
            IndexResult = Reminder % Sizes[DimIndex]
            IndexVec[DimIndex] = IndexResult
            # Exit loop here if needed
            if DimIndex == 0:
                break
            # update the reminder for the next iteration
            Reminder = Reminder // Sizes[DimIndex]
            DimIndex = DimIndex - 1
        return IndexVec

    def FigureOutIndex(self, Index):
        """ Figures out if Index is vector or flat and returns both """
        if IsList(Index):
            FlatIndex = self.VecIndexToFlatIndex(Index)
            VectorIndex = Index[:]
        elif IsNumericType(Index):
            FlatIndex = Index
            VectorIndex = self.FlatIndexToVecIndex(Index)
        else:
            raise ValueError, 'ASSERTION ERROR: The table cell index is neither numeric nor a list'
        # return both interprestations
        return (FlatIndex,VectorIndex)


    def AccessCell(self, Index):
        """ Access the table cell indicated by Index for update or retrieval """
        # Note that if index is an integer it is considered a flat index
        # if the index is a vector, it is considered a subscript vector index
        # Note that in both cases both the Values and FlatValues members are
        # Handled.
        # figure out the index and return both representations
        (FlatIndex,VectorIndex) = self.FigureOutIndex(Index)
        # if a flat representtion exist, use the shortcut index
        if self.FlatValues != None:
            # in this case, only access the table to return the cell value
            RetVal = self.FlatValues[FlatIndex]
        else:
            #  There is a need to drill down the multidimentional array
            PointerToList = self.Values
            TempVectorIndex = VectorIndex[:]
            while True:
                CurrentIndex = TempVectorIndex.pop(0)
                if TempVectorIndex == []:
                    # if this is the last diemnsion, retun the result
                    RetVal = PointerToList[CurrentIndex]
                    break
                else:
                    # otherwise, drill don in the multi-dimension Hierarchy
                    PointerToList = PointerToList[CurrentIndex]
        return RetVal


    def GenerateRangeDescriptionArrays(self):
        """ creates arrays of text and size describing the table cells"""
        # Note that DescStrArray is a 2D array, it is only
        # partially initialized here
        DescStrArray = [[]] * self.DataItemsNum
        DescStrSizeArray = [0]*(self.DimNum + 1)
        for FlatIndex in range(self.DataItemsNum):
            VecIndex = self.FlatIndexToVecIndex(FlatIndex)
            # Build string by first traversing dimensions
            for DimIndex in range(self.DimNum):
                DimName = self.Dimensions[DimIndex][0]
                DimRange = self.Dimensions[DimIndex][1]
                RangeIndex = VecIndex[DimIndex] 
                if IsNaN(DimRange[0]):
                     # This means a discrete indexed dimension
                     DimDescStr = DimName + '=' + SmartStr(DimRange[RangeIndex+1])
                else:           
                     # This means a continuous dimension
                     DimDescStr = SmartStr(DimRange[RangeIndex]) + '<' + DimName + '<=' + SmartStr(DimRange[RangeIndex+1])

                # Add the string to the array of strings
                DescStrArray[FlatIndex]= DescStrArray[FlatIndex] + [DimDescStr]
                DescStrSizeArray[DimIndex] = max(DescStrSizeArray[DimIndex], len(DimDescStr))
            # Add the value to the array of strings
            ValDescStr = SmartStr(self.AccessCell(FlatIndex))
            DimIndex = self.DimNum
            DescStrArray[FlatIndex]= DescStrArray[FlatIndex] + [ValDescStr]
            DescStrSizeArray[DimIndex] = max(DescStrSizeArray[DimIndex], len(ValDescStr))
        return (DescStrArray, DescStrSizeArray)

    def GenerateRangeDescriptionText(self, DescStrArray, DescStrSizeArray, Index, ReportValue = True):
        """ return text reporting a cell range with a value if requested """
        # DescStrArray, DescStrSizeArray are generated by the function
        # GenerateRangeDescriptionArrays. Index can be eaither flat of vector
        # type index to the cell of interest. If ReportValue is true (default)
        # then the string will contain the value of the cell at the end
        (FlatIndex,VectorIndex) = self.FigureOutIndex(Index)
        DescStr = ''
        for DimIndex in range(self.DimNum):
            DescStr = DescStr + DescStrArray[FlatIndex][DimIndex].ljust(DescStrSizeArray[DimIndex])+'; '
        DimIndex = self.DimNum
        DescStr = DescStr[:-2] 
        if ReportValue:
            DescStr = DescStr + ' : ' + DescStrArray[FlatIndex][DimIndex].ljust(DescStrSizeArray[DimIndex])
        return DescStr

    def GenerateReport(self, FormatOptions = None):
        """ Generate the report for this entity instance """
        TotalIndent = HandleOption('TotalIndent', FormatOptions,'')
        IndentAtom = HandleOption('IndentAtom', FormatOptions,'  ')
        #ColumnSpacing = HandleOption('ColumnSpacing', FormatOptions,' | ')
        #FieldHeader = HandleOption('FieldHeader', FormatOptions,True)
        LineDelimiter = HandleOption('LineDelimiter', FormatOptions,'\n')
        #SectionSeparator = HandleOption('SectionSeparator', FormatOptions,70*'_')
        #ShowHidden = HandleOption('ShowHidden', FormatOptions,False)
        #ShowDependency = HandleOption('ShowDependency', FormatOptions,False)
        #DetailLevel = HandleOption('DetailLevel', FormatOptions, 0)
        ReportString = ''
        # Generate arrays of texts and text sizes for each cell
        (DescStrArray, DescStrSizeArray) = self.GenerateRangeDescriptionArrays()
        # unravel these text arrays into print
        for FlatIndex in range(self.DataItemsNum):
            DescStr = self.GenerateRangeDescriptionText (DescStrArray, DescStrSizeArray, FlatIndex, True)
            ReportString = ReportString + TotalIndent + IndentAtom + DescStr + LineDelimiter
        return ReportString

    def Describe(self):
        """ Describes the string """
        RetVal = self.GenerateReport()
        return RetVal

    # The following line will allow calling the method directly
    # from the class without an instance to help maintain strict data integrity
    ClassVecIndexToFlatIndex = ClassFunctionWrapper(VecIndexToFlatIndex)
    ClassFlatIndexToVecIndex = ClassFunctionWrapper(FlatIndexToVecIndex)


class Param(str):
    """Defines a parameter that can be used by the system"""
    # The string defines the name of the parameter values are
    # assigned to. The name is unique or blank. The name can
    # be only of a form conforming to the following regular
    # expression: {a-z,A-Z}{a-z,A-Z,0-9,_}*
    Formula = ''           # A string defining a formula - can be number/vector
    ParameterType = ''     # A string - one of the values in ParameterTypes
    ValidationRuleParams = ''    # A string containing a sequence of parameters
                                 # required by the validation rule
    Notes = ''       # A string containing additional notes
    Tags = None  # Contains additional information such as the State ID
                 # That generated a specific state. This is an internal
                 # system variable that is currently not exposed to the user

    def __new__(cls , Name = None, Formula = None , ParameterType = None , ValidationRuleParams = None, Notes = None , Tags = None):
        """Constructor to allow creation of a non mutable object"""
        if Name == None:
            Name = ''
        if Formula == None:
            Formula = ''
        if ParameterType == None:
            ParameterType = ''
        if ValidationRuleParams == None:
            ValidationRuleParams = ''
        if Notes == None:
            Notes = ''
        # Copy the input data. Make sure names and formulas are without
        # spaces leaning and trailing spaces
        It = str.__new__(cls,Name.strip())
        It.Formula = Formula.strip()
        It.ParameterType = ParameterType
        It.ValidationRuleParams = ValidationRuleParams
        It.Notes = Notes
        It.Tags = Tags
        # Assert that the name is valid
        It.ValidateName(Name)
        It.VerifyValidity()     
        return It


    def VerifyValidity(self, ValueToValidate = None):
        """ Verify that the value, parameter type, and validation rule agree """
        if ValueToValidate == None:
            ValueToValidate = self.Formula
        if self.ParameterType not in ParameterTypes:
            raise ValueError, 'Parameter Validation Error: Invalid Parameter type "' + str(self.ParameterType) + '" is defined for Parameter "' + str(self) +'"'
        # Unless specified otherwise, there is no need to check the value
        # Perform the basic validity checks for most parameter types
        if self.ParameterType == 'System Reserved':
            # checking system reserved parameters is not required
            pass
        elif self.ParameterType == 'State Indicator':
            # State Indicator is Boolean - this is checked previously
            # If this is not simulation runtime, Check the associated state
            # to check existence of the state. Note that this check is not
            # performed in runtime since States are not actually defined there.
            # Rather the validity of the parameter is checked at the time of
            # its definition.
            self.ReturnAssociatedState() 
        elif self.ParameterType == 'System Option':
            # A system option is just a nubmer for validity purposes
            if self.Formula == '':
                raise ValueError, 'Parameter Validation Error: In parameter "'+ str(self) + '", a system option is a constant that must hold a numeric value. Please define the formula for the system option.'
        elif self.ParameterType in ['Number', 'Integer']:
            if self.Formula != '':
                raise ValueError, 'Parameter Validation Error: In parameter "'+ str(self) + '", an Integer or a Number cannot hold a value. To define a constant value use a System Option or an Expression.'
        elif self.ParameterType == 'Expression':
            if self.Formula == '':
                raise ValueError, 'Parameter Validation Error: In parameter "'+ str(self) + '", an Expression can not have an empty formula. Please define the formula or change the parameter type.'
            # Attempt to construct an expression object from the text.
            # During the construction process, the expression validity
            # is checked and exceptions are caught
            try:
                TempExpr = Expr(self.Formula)
                # Prevent a cyclic definition of a parameter before it enters
                # the database. It is possible for the expression to be valid
                # and not cyclic, yet use the same parameter name that is about
                # to be declared by self. This code prevents this from
                # happening by checking that the expression does not use the
                # parameter name within it directly, or indirectly. Note that
                # this check should happen only in compile time since in
                # runtime a value is provided rather than a formula. Also note
                # that TempExpr was already computed above.
                if str(self) in TempExpr.DependantParams:
                    raise ValueError, 'Cyclic definition of a parameter was detected. The parameter "' + str(self) + '" is used within the expression "' + str(TempExpr) +'" or is used after the dependencies in the expression are expanded to "' + str(TempExpr.ExpandedExpr) +'". This creates an infinite cyclic definition where a parameter uses itself in definition and cannot be resolved and therefore illegal. You should change the expression or the parameter name to resolve this cyclic reference.'
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                raise ValueError, 'Parameter Validation Error: Expression validation problem in parameter "' + str(self) + '" Here are details: ' +str(ExceptValue)

        # Check Bound validity if bounds are defined
        if self.ValidationRuleParams != '':
            try:
                Bounds = eval (self.ValidationRuleParams , EmptyEvalDict)
            except:
                raise ValueError, 'Parameter Validation Error: Validation bounds for parameter "'+ str(self) + '" do not evaluate properly as an expression. Please make sure bounds are defined properly as a vector [min,max] where min,max are numeric values. The specified bounds were: ' + str(self.ValidationRuleParams)
            else:
                if not IsList(Bounds) or len(Bounds) != 2 or not IsNumericType(Bounds[0]) or not IsNumericType(Bounds[1]) :
                    raise ValueError, 'Parameter Validation Error: Validation bounds for parameter "'+ str(self) + '" have an invalid structure. Either the bounds are not a vector of two members or its members are not numeric. Please make sure bounds are defined properly as a vector [min,max] where min,max are numeric values. The specified bounds were: ' + str(self.ValidationRuleParams)
                elif not (Bounds[0] <= Bounds[1]): 
                    raise ValueError, 'Parameter Validation Error: Validation bounds for parameter "'+ str(self) + '" have a valid structure of [max,min] rather than [min,max]. Consider switching the bound values to create an ascending order. The specified bounds were: ' + str(self.ValidationRuleParams)


        # If checking for value validity for Integer, Number, System Option
        if self.ParameterType in ['Number', 'Integer', 'System Option']:
            if ValueToValidate != '':
                # if value is unknown, then calculate it
                # Try to evaluate the expression
                try:
                    DummyExpr=Expr()
                    NumericResult = DummyExpr.Evaluate(ExprText = ValueToValidate)
                except:
                    (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                    raise ValueError, 'Parameter Validation Error: Value validation problem in parameter "' + str(self) + '" Here are details: ' +str(ExceptValue)

                # now check for integer
                if self.ParameterType ==  'Integer' and round(NumericResult) != NumericResult:
                    raise ValueError, 'Parameter Validation Error: Value for parameter "'+ str(self) + '" is not Integer, where the validation rule is defined as such. Consider redefining the expression or the parameter. The Expression was "' + ValueToValidate + '" and the evaluation value is: ' + str(NumericResult)
    
                # now check tht the number is within bounds
                # the bound vlidity was already checked
                if (self.ValidationRuleParams != '') and not (Bounds[0] <= NumericResult <= Bounds[1]):
                        # Note that the error text here has a different header since
                        # this header is later analyzed to decide 
                        raise ValueError, 'Parameter Validation Error: The value does not fall within the specified validation bounds provided. The specified bounds were: ' + str(self.ValidationRuleParams) + ' and the evaluated value was: ' + SmartStr(NumericResult)
        return



    def ValidateName(self, Name=None):
        """The function verifies a candidate string for a state or parameter"""
        if Name == None:
            Name = str(self)
        if Name == '':
            raise ValueError, 'Parameter Name Validation: The Name must be defined, a blank name is not allowed'
        IsValid = re.match(ParamTextMatchPattern,Name)
        # Check if the given name is valid
        if IsValid == None:
            raise ValueError, 'Parameter Name Validation: The given Name "' + Name + '" is Invalid. Please use an alphanumeric string of the form [a-z,A-Z][a-z,A-Z,0-9,_ ]*'
        # If the name is of a default parameter name, make sure that the
        # parameter is of type system Option
        if Name in DefaultSystemOptions.keys() and self.ParameterType != 'System Option':
            raise ValueError, 'Parameter Name Validation: The given Name "' + Name + '" is a name corresponding to a System Option, while the parameter type is not defined as a system option. Please change the parameter name or redefine the parameter as a system option'
        return

    def ReturnAssociatedState(self):
        """ If a state indicator returns the state ID or None otherwise """
        if self.ParameterType != 'State Indicator':
            StateID = None
        else: 
            # Extract the parameter name from the notes
            if self.Notes[0:len(StateIndicatorNotePrefix)] != (StateIndicatorNotePrefix):
                raise ValueError, 'ASSERTION ERROR: The Note field of state indicator "' + str(self) + '" was changed and is no longer appropriate'
            StateID = self.Tags
            if not States.has_key(StateID) or str(self) not in States[StateID].GenerateAllStateIndicatorNames():
                raise ValueError, 'ASSERTION ERROR: The state indicator "' + str(self) + '" does not represent a valid state - The note or the indicator name may have been changed'
        return StateID

    def IsParamDependant(self, ParamName):
        """ Returns True if dependant on ParamName """
        # Create an Dummy empty Expression to avoid unneeded validity check
        Result = ParamName in self.FindDependantParams(ParamType = None)
        return Result

    def FindDependantParams(self, ParamType = None):
        """ Find the dependant parameters """
        DummyExpr = Expr('')        
        Result = DummyExpr.FindDependantParams(ParamType = None, ExprText = self.Formula)
        # If a data type is specified filter the results by the data type
        if ParamType != None:
            Result = filter(lambda Entry: Params[Entry].ParameterType == ParamType, Result)
        return Result
        
    
    def CheckDependencies(self, CheckForModify = False, ProjectBypassID = 0):
        """ Verifies no dependant data exists """
        # For Parameters, check almost all other collections to establish if
        # deletion and modification is needed.
        # Note that states are not checked since deletion of state indicators
        # is blocked by Modify.
        # Also simulation results are not checked since project check is
        # sufficient.
        # All entities will use the same function
        DependencyDefFunc = lambda (EntryKey, Entry): str(self) in Entry.FindDependantParams()
        # Check transitions:
        DependancyErrorCheck(self, Transitions, DependencyDefFunc, 'Parameter Dependency Error: The parameter or the state indicator "' + str(self) + '" cannot be deleted or modified as there is at least one transition using it. To allow modification, delete/modify all the following dependant transitions: ' )
        # No need to check StudyModels:
        # Check population sets:
        DependancyErrorCheck(self, PopulationSets, DependencyDefFunc, 'Parameter Dependency Error: The parameter or the state indicator "' + str(self) + '" cannot be deleted or modified as there is at least one population set using it. To allow modification, delete/modify all the following dependant population sets: ' )
        # Check Projects that will internally check simulation rules:
        DependancyErrorCheck(self, Projects, DependencyDefFunc, 'Parameter Dependency Error: The parameter or the state indicator "' + str(self) + '" cannot be deleted or modified as there is at least one project using it. To allow modification, delete/modify all the following dependant projects: ' )   
        # Check other parameters that may use the parameter in the formula:
        DependancyErrorCheck(self, Params, DependencyDefFunc, 'Parameter Dependency Error: The parameter or the state indicator "' + str(self) + '" cannot be deleted or modified as there is at least one other parameter using it. To allow modification, delete/modify all the following dependant parameters: ' ) 
        return 

    def GenerateReport(self, FormatOptions = None):
        """ Generate the report for this entity instance """
        TotalIndent = HandleOption('TotalIndent', FormatOptions,'')
        IndentAtom = HandleOption('IndentAtom', FormatOptions,'  ')
        #ColumnSpacing = HandleOption('ColumnSpacing', FormatOptions,' | ')        
        FieldHeader = HandleOption('FieldHeader', FormatOptions,True)
        LineDelimiter = HandleOption('LineDelimiter', FormatOptions,'\n')
        SectionSeparator = HandleOption('SectionSeparator', FormatOptions,70*'_')
        ShowHidden = HandleOption('ShowHidden', FormatOptions,False)
        ShowDependency = HandleOption('ShowDependency', FormatOptions,False)
        DetailLevel = HandleOption('DetailLevel', FormatOptions, 0)
        # DetailLevel = 0 prints only parameter name and type information
        # DetailLevel = 1 additional data is printed
        ReportString = ''
        ReportString = ReportString + TotalIndent + FieldHeader * 'Parameter Name: ' + str(self) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Parameter Type: ' + str(self.ParameterType) + LineDelimiter
        if DetailLevel > 0:
            ReportString = ReportString + TotalIndent + FieldHeader * 'Holds The Formula: ' + str(self.Formula) + LineDelimiter
            ReportString = ReportString + TotalIndent + FieldHeader * 'Specified Validation Rule Parameters: ' + str(self.ValidationRuleParams) + LineDelimiter
            ReportString = ReportString + TotalIndent + FieldHeader * 'Notes: ' + str(self.Notes).replace('\n','\n'+TotalIndent)+ LineDelimiter
            if ShowHidden:
                ReportString = ReportString + TotalIndent + FieldHeader * 'Tags: ' + str(self.Tags) + LineDelimiter
            if ShowDependency:
                RevisedFormatOptions = HandleOption('TotalIndent', FormatOptions, TotalIndent + IndentAtom, True)
                RevisedFormatOptions = HandleOption('DetailLevel', RevisedFormatOptions, DetailLevel-1, True)                        
                FormulaExpr = Expr(self.Formula)
                ReportString = ReportString + FormulaExpr.GenerateReport(RevisedFormatOptions)
                if self.ParameterType == 'State Indicator':
                    ReportString = ReportString + TotalIndent + FieldHeader * 'Associated with the state: ' + str(States[self.Tags].Name) + LineDelimiter
        ReportString = ReportString + TotalIndent + SectionSeparator + LineDelimiter
        return ReportString

    def Copy(self, NewName = None):
        """ Returns an object that copies this one """
        NewName = CalcCopyName(self, NewName)
        # Do not allow copying some types of parameters
        if self.ParameterType in ['State Indicator','System Reserved']:
            raise ValueError, 'Parameter Copy Error: Cannot copy a parameter of type ' + str(self.ParameterType) 
        NewRecord = Param( Name = NewName, Formula = self.Formula , ParameterType = self.ParameterType , ValidationRuleParams = self.ValidationRuleParams , Notes = self.Notes , Tags = self.Tags)
        return NewRecord

    # Description String
    def Describe(self):
        """ Return the string version of self"""
        RetVal = str(self)
        return RetVal



class State:
    """Described the data required for a state in a model or in a study"""
    ID = 0               # Unique key identifier of the state
    Name = ''            # A string containing a name
    Notes = ''           # A string containing additional notes
    IsSplit = False      # A Boolean indicating if the state is a splitter
    JoinerOfSplitter = 0 # If a joiner state, this holds the ID of the splitter
    IsEvent = False      # A Boolean indicating if the state is an event state
    IsTerminal = False   # A Boolean indicating if this is a terminal state
    ChildStates = []     # A sequence containing StateID of child
                         # states of a process

    def __init__( self , ID = 0 , Name = '' , Notes = '' , IsSplit = False , JoinerOfSplitter = 0 , IsEvent = False, IsTerminal = False ,  ChildStates = [] ):
        """Constructor with default values and some consistency checks"""
        # Verify Data
        self.VerifyData (Name ,IsSplit, JoinerOfSplitter, IsEvent, IsTerminal, ChildStates)
        # Copy data
        self.ID = ID
        self.Name = Name
        self.Notes = Notes
        self.IsSplit = IsSplit
        self.JoinerOfSplitter = JoinerOfSplitter
        self.IsEvent = IsEvent
        self.IsTerminal = IsTerminal
        self.ChildStates = copy.deepcopy(ChildStates)
        return

    def VerifyData ( self , Name = None ,IsSplit = None , JoinerOfSplitter = None , IsEvent = None, IsTerminal = None, ChildStates = None ):
        """Verify the data at a shallow level"""
        if Name == None:
            Name = self.Name
        if IsSplit == None:
            IsSplit = self.IsSplit
        if JoinerOfSplitter == None:
            JoinerOfSplitter = self.JoinerOfSplitter
        if IsEvent == None:
            IsEvent = self.IsEvent
        if IsTerminal == None:
            IsTerminal = self.IsTerminal
        if ChildStates == None:
            ChildStates = self.ChildStates
        # A series of consistency check for the name
        # First, try converting it to a parameter name
        # an error will be raised if not allowed        
        self.ConvertNameToParam(Name)
        # Now check that banned extensions are not used
        for Extention in ParamNameExtensitons[1:]:
            if Extention[1:] in Name:
                raise ValueError, 'State Validation Error: The state name cannot contain " ' + Extention[1:] + ' " to avoid parameter name clashes. The Error was raised while trying to define the name: "' + str(Name) + '"'
        # Check if there are conflicts between variables
        if IsSplit and IsEvent:
            raise ValueError, 'State Validation Error: A state cannot be both a splitter and an event state. Note that a splitter state is already defined as immediate. The Error was raised while trying to define the name: "' + str(Name) + '"'
        if IsSplit and JoinerOfSplitter != 0:
            raise ValueError, 'State Validation Error: A state cannot be both a splitter and a joiner state. Two different states are required if both are needed. The Error was raised while trying to define the name: "' + str(Name) + '"'
        if IsSplit and IsTerminal:
            raise ValueError, 'State Validation Error: A state cannot be both a splitter and a terminal state. Please check the data since a terminal state stops simulation and making it a splitter does not make sense. The Error was raised while trying to define the name: "' + str(Name) + '"'
        if IsEvent and JoinerOfSplitter != 0:
            raise ValueError, 'State Validation Error: A state cannot be both an Event state and a joiner state. Note that a joiner state is already defined as immediate. The Error was raised while trying to define the name: "' + str(Name) + '"'
        if IsEvent and IsTerminal:
            raise ValueError, 'State Validation Error: A state cannot be both a Terminal State and an event state. A terminal state stops simulation and it does not make sense maing it an event state. The Error was raised while trying to define the name: "' + str(Name) + '"'
        if IsTerminal and JoinerOfSplitter != 0:
            raise ValueError, 'State Validation Error: A State cannot be both a terminal state and a joiner state. If this is intentional, please define these as two different states. The Error was raised while trying to define the name: "' + str(Name) + '"'
        # Note that the validation that the joiner is a valid splitter state is
        # made at the level of adding the record to the collection. Only
        # superficial test is made at this level
        if ChildStates != [] and (IsEvent or IsSplit or IsTerminal or JoinerOfSplitter != 0):
            raise ValueError, 'A sub-process cannot be an event state / terminal state / splitter state / joiner state. Please redefine the state flags. Note that a sub-process can contain states that are of these kinds within it. The Error was raised while trying to define the name: "' + str(Name) + '"'
        # Check if the subprocess data is valid
        self.IsSubProcess( ChildStates )

        return

    def ConvertNameToParam( self , Name = None):
        """Converts the state name to a parameter name - using underscore"""
        if Name == None:
            Name = self.Name
        # check that the name is not empty
        if Name == '':
            raise ValueError, 'State Name Validation Error: A State name cannot be empty.'
        # Check that the first character is Alphabet without numbers,
        # if not raise an error
        if Name[0] not in AlphabetNoNumeric:
            raise ValueError, 'State Name Validation Error: The first character of a state name must be an alphabet character without a number. The Error was raised while trying to define the name: "' + str(Name) + '"'
        # Run through the string and replace any non alphanumeric character
        # with an underscore
        ReplacedName = ''
        for Character in Name:
            if Character in AlphabetAndNumeric:
                ReplacedName = ReplacedName + Character
            else:
                ReplacedName = ReplacedName + '_'
        return ReplacedName


    def IsSubProcess( self , ChildStates = None , CheckStates = True):
        """Check the pooling sequence and return True if a sub process"""
        if ChildStates == None:
            ChildStates = self.ChildStates
        if not IsList(ChildStates):
            raise TypeError, 'ASSERTION ERROR: child information should be a list'            
        # An empty sequence, this is not a subprocess
        if ChildStates == []:
            return False
        if self.IsSplit or self.JoinerOfSplitter != 0 or self.IsEvent or self.IsTerminal:
            raise ValueError, 'ASSERTION ERROR: A subprocess cannot be a special state i.e. event, splitter, joiner, terminal'
        # Analyze the sequence for errors and determine the type
        for StateID in ChildStates:
            if not States.has_key(StateID):
                raise ValueError, 'ASSERTION ERROR: state ID ' + str(StateID) + ' does not exist in the states table'
        # Make sure a state is not repeated twice in the list
        Duplicates = FindDuplicatesInSequence(ChildStates)
        if Duplicates != []:
            DuplicateStateNames = ''.join(map(lambda Entry: States[Entry].Name + ',' ,Duplicates))[:-1]
            raise ValueError, 'Subprocess Validation Error: At least one state is repeated more than once in the list of child states. Delete the duplicate states from the child state list. Duplicate states are: ' + DuplicateStateNames
        StateIsSubProcess = True
        ListOfSplitters = filter(lambda Entry: States[Entry].IsSplit, ChildStates)
        ListOfJoiners = filter(lambda Entry: States[Entry].JoinerOfSplitter !=0 , ChildStates)
        ListOfSubProcesses = filter(lambda Entry: States[Entry].IsSubProcess() , ChildStates)
        NamesOfSplitters = States.ID2Name(ListOfSplitters)
        NamesOfJoiners = States.ID2Name(ListOfJoiners)
        NamesOfSubProcesses = States.ID2Name(ListOfSubProcesses)
        # Check if there are no duplicate names in children sub-processes
        AllAssociatedChildStates = []
        for StateID in ChildStates:
            (AllChildStates, IsChildSubProcess, ChildNestingLevel) =  States[StateID].FindChildStates()
            AllAssociatedChildStates = AllAssociatedChildStates + AllChildStates
        ListOfDuplicates = FindDuplicatesInSequence(AllAssociatedChildStates)
        if ListOfDuplicates != []:
            NamesOfDuplicates = States.ID2Name(ListOfDuplicates)
            raise ValueError, 'Subprocess Validation Error: Duplicate nested states were detected. The following states were defined more than once when considering all nested subprocesses: "' + NamesOfDuplicates + '" . Please redefine the nesting structure.'
        # Make sure that if a joiner state is defined, then their 
        # splitter state is defined in the list before it.
        # Also make sure that there are at least the same amount of
        # Subprocesses as splitter states.
        for (StateLocation, StateID) in enumerate(ChildStates):
            SplitterID = States[StateID].JoinerOfSplitter                
            if SplitterID != 0:
                if SplitterID not in ChildStates:
                    raise ValueError, 'ASSERTION ERROR: A joiner state was defined in a subprocess without previously defining the corresponding splitter state. The splitter state should be created before the joiner is mentioned in the list.'
                if SplitterID not in ChildStates[:StateLocation]:
                    raise ValueError, 'Subprocess Validation Error: A Splitter state was defined in a subprocess after defining the corresponding joiner state. The splitter  ' + States[SplitterID].Name + ' should be specified in the pooled state list before the joiner state ' + States[StateID].Name + ' is mentioned in the list'
        if len(ListOfSplitters) != len(ListOfJoiners):
            raise ValueError, 'Subprocess Validation Error: More splitter states have been defined in a subprocess than joiner states. Note that each splitter state must have a corresponding joiner mentioned after its definition in the pooled states list. The splitter states were: ' + NamesOfSplitters + '. The joiner states were: ' + NamesOfJoiners
        if len(ListOfSplitters) > len(ListOfSubProcesses):
            raise ValueError, 'Subprocess Validation Error: There are more splitter states than sub-processes. This is not reasonable since each splitter state must lead to at least one sub-process. Here are the splitter states mentioned in the process list: ' + NamesOfSplitters + '. Here is list of sub-processes mentioned in the process: ' + NamesOfSubProcesses
        return StateIsSubProcess


    def FindChildStates (self, CurrentNestingLevel = 0):
        """ The output is of the form of a tuple containing three
            corresponding sequences: (AllStates, IsSubProcess, NestingLevel)
            The function drills down a subprocess defined by self
            and returns all the states associated with this subprocess.
            The function recursively drills through subprocesses in an attempt
            to find duplications. If a duplicate found it raises an error. 
            Note that self itself is considered a subprocess and
            appears at the output.
            NestingLevel is an output vector corresponding to pooled states
            that holds the nesting level where the father sub process is
            level 0, its children 1 grandchildren 2 etc.
            IsSubProcess is an output vector corresponding to AllStates
            that has True if the output state is a subprocess.
            CurrentNestingLevel is also used in the recursion to keep track
            of recursion level.
            This functon It is appropriate for collecting all states of a Model
            """
        if self.ChildStates != []:
            IsSubProcess = [ True ]
        else:
            IsSubProcess = [False]
        # Convert to set for later use
        PossibleChildrenSet = set(self.ChildStates)
        # An assertion check
        if len (PossibleChildrenSet) != len(self.ChildStates):
            raise ValueError, 'ASSERTION ERROR: conversion to set eliminates a member of the self.ChildStates list'
        # First add the state to the output vector
        AllStates = [self.ID]
        NestingLevel = [CurrentNestingLevel]
        # Loop through all the states in the subprocess and recursively call
        # the function for each such state
        for ChildState in self.ChildStates:
            (AllStatesReturned, IsSubProcessReturned, NestingLevelReturned) = States[ChildState].FindChildStates( CurrentNestingLevel+1)
            # Check if a state has already been used in another sub process
            # intersect the current resulting states with the previously
            # accumulated list. If a state was defined twice, the vector will
            # not be empty
            AllStatesReturnedSet = set(AllStatesReturned)
            if len (AllStatesReturnedSet) != len(AllStatesReturned):
                raise ValueError, 'ASSERTION ERROR: conversion to set eliminates a member of the AllStatesReturned list'
            DoubleDefined = PossibleChildrenSet & AllStatesReturnedSet
            if len(DoubleDefined) == 0:
                raise ValueError, 'Descendant State Validation Error: States ' + str(list(DoubleDefined)) + ' are defined in more than one subprocess'
            # Add the output to the result 
            AllStates = AllStates + AllStatesReturned
            NestingLevel = NestingLevel + NestingLevelReturned
            IsSubProcess = IsSubProcess + IsSubProcessReturned
        return (AllStates, IsSubProcess, NestingLevel)




    def FindFatherState(self, StudyModelID):
        """The function finds the father state in a specific Study/Model"""
        # Find the main subprocess from the Study/Model
        MainProcess = States[StudyModels[StudyModelID].MainProcess]
        (AllStates, IsSubProcess, NestingLevel) = MainProcess.FindChildStates ()
        FoundInProcess = 0
        # Loop through all states and check compatibility in its children
        for StateID in AllStates:
            if self.ID in States[StateID].ChildStates:
                if FoundInProcess == 0:
                    FoundInProcess = StateID
                else:
                    raise ValueError, 'ASSERTION ERROR: The state' + self.Name + ' is a child of more than one state in this project'
        return FoundInProcess

    def SubProcessStartInfo(self, StudyModelID):
        """Return the tuple (Splitter ID, State ID) that start the subprocess"""
        # Check if this is a subprocess. 
        if not self.IsSubProcess():
            # If not a subprocess, return (0,0)
            RetVal = (0,0)
        else:
            # If a subprocess, return (SplitterStateID,StartStateID)
            SubProcessFather = self.FindFatherState(StudyModelID)
            # If this is the subprocess, analyze states and transitions
            StartStateCandidates = []
            ErrorStates = []
            # For each sub process state
            for AnalyzedStateID in self.ChildStates:
                # Check all leading transitions into this state
                TransitionsIntoThisState = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey) : StudyModelIDKey == StudyModelID and ToStateKey == AnalyzedStateID, Transitions.keys()))
                # skip analyzing subprocess states
                if not States[AnalyzedStateID].IsSubProcess():
                    if TransitionsIntoThisState == [] :
                        # If there are no transitions to the state it may be an
                        # error. Or it can be a candidate for being the start
                        # state of the entire model
                        if self.ID == StudyModels[StudyModelID].MainProcess:
                            StartStateCandidates = StartStateCandidates + [(0,AnalyzedStateID)]
                        else:
                            ErrorStates = ErrorStates + [AnalyzedStateID]
                    else:
                        # Check transitions coming from outside the process
                        for TransKey in TransitionsIntoThisState:
                            Trans = Transitions[TransKey]
                            # Check if the transitions to this state is from
                            # outside and it is not a join into a joiner state
                            if Trans.FromState not in self.ChildStates and States[AnalyzedStateID].JoinerOfSplitter == 0:
                                OriginatingState = States[Trans.FromState]
                                # verify that the originating state is a splitter
                                if not OriginatingState.IsSplit:
                                    raise ValueError, 'Process Hierarchy Validation Error: The originating state "' + OriginatingState.Name + '" is not a splitter state, yet it leads to the state "'+ States[AnalyzedStateID].Name +'" in another sub process. This indicates that the nesting hierarchy of states and sub processes was not preserved. If this transition is intentional please defined the originating state as a splitter state and make sure it the transition leads to a state in a directly nested subprocess.'
                                # verify that the originating splitter has the
                                # same father as the current subprocess, meaning
                                # that there are no hierarchical jumps
                                OriginatingStateFather = OriginatingState.FindFatherState(StudyModelID)
                                if OriginatingStateFather != SubProcessFather:
                                    raise ValueError, 'Process Hierarchy Validation Error: The subprocess "'+ self.Name +'" and the splitter state "' + OriginatingState.Name + '" leading to it do not belong in the hierarchy to the same subprocess. The splitter state father is "' + States[OriginatingStateFather].Name + '" where as the sub-process father is "'+ States[SubProcessFather].Name +'". Please verify the transitions and the subprocess definitions.'
                                StartStateCandidates = StartStateCandidates + [(Trans.FromState,AnalyzedStateID)]
            # Check if an error was detected
            if ErrorStates != []:
                ErrorStateStrings = States.ID2Name(ErrorStates)
                raise ValueError, 'Process Hierarchy Validation Error: Unlinked states detected. There is at least one state without a transition leading into it. Unless this is the start state for the entire model, all states must be linked. This error means the model is incomplete and therefore the system cannot properly detect the first state in a subprocess. Unlinked states should be linked properly. The error was raised for the following states: ' + ErrorStateStrings
            # Check if several start points exist. Note that at this point
            # this implies several start points for the model. As several
            # Splitters leading to the same process were dealt with before
            if len(StartStateCandidates) > 1:
                StartStateCandidatesString = States.ID2Name(map(lambda (TheFromState,TheAnalyzedStateID): TheAnalyzedStateID, StartStateCandidates))
                raise ValueError, 'Process Hierarchy Validation Error: Several start points have been detected for the sub-process "'+ self.Name +'" . This implies that several states have not been assigned transitions into them or the sub-process has been assigned more than one transition into it. The states in the sub-process need to be linked properly. If this error was caused by a joiner state with no transitions into it since the splitter leads to processes that do not end, then you can resolve this error by creating a transition into the joiner with probability 0. Otherwise, you should modify your model to have a single entry state to the process indicated by no transitions into it. The states with the current links created the problem:' + str(StartStateCandidatesString)
            elif len(StartStateCandidates) == 0:
                # In the future, this point may be reexamined to allow
                # loops without a dummy starting state
                raise ValueError, 'Process Hierarchy Validation Error: No start states have been detected for the subprocess "'+ self.Name +'". There seems to be a cycle (loop) within the process. If this is intentional, try adding a starter event state to start the subprocess to resolve this issue and act as the start state'
            # Extract the return value
            RetVal = StartStateCandidates[0]
        return RetVal

    def GenerateAllStateIndicatorNames(self, StateName = None):
        """Returns a list of state indicator parameter names for this state"""
        if StateName == None:
            StateName = self.Name
        OutputList = []
        Prefix = self.ConvertNameToParam(StateName)
        # Loop through all possible extensions including no extension
        for Extension in ParamNameExtensitons:
            # Create parameter name (assume it already exists in parameter
            ParamName = ( Prefix + Extension)
            # Add the parameter name to the list
            OutputList = OutputList + [ParamName]
        return OutputList

    def SimulationPriorityGroup(self, StudyModelID):
        """Returns a number indicating the Priority Group during simulation"""
        # Subprocesses are always last priority
        if not self.IsSubProcess():
            # Terminal end state
            if self.IsTerminal:
                return 1
            # Splitter states are next
            elif self.IsSplit:
                return 2
            # Joiner states are next
            elif self.JoinerOfSplitter != 0:
                return 3
            # Event states are next
            elif self.IsEvent:
                return 4
            # Regular states are next
            else:
                return 5
        else:
            # Subprocesses are next
            return 6


    def IsParamDependant(self, ParamName):
        """ Returns True if dependant on ParamName """
        Result = ParamName in self.FindDependantParams(ParamType = None)
        return Result

    def FindDependantParams(self, ParamType = None):
        """ Find the dependant parameters """
        Result = self.GenerateAllStateIndicatorNames()
        # If a datatype is specified filter the results by the data type
        if ParamType != None:
            Result = filter(lambda Entry: Params[Entry].ParameterType == ParamType, Result)        
        return Result


    def CheckDependencies(self, CheckForModify = False, ProjectBypassID = 0):
        """ Verifies no dependant data exists """
        # Check that all state parameters are not used elsewhere:
        IndicatorParamNames = self.GenerateAllStateIndicatorNames()
        for ParamName in IndicatorParamNames:
            # Verify the parameter can be deleted. Note that a flag is set
            # to avoid rechecking the parameter is the state that is about to
            # be deleted
            Params[ParamName].CheckDependencies(CheckForModify = CheckForModify, ProjectBypassID = ProjectBypassID)
        # Check that the state is not used in other states
        DependancyErrorCheck(self, States, lambda (EntryKey,Entry): self.ID in Entry.ChildStates, 'State Dependency Error: The state "' + str(self.Name) +'" cannot be deleted or modified as there is at least one other state/subprocess that references it as a pooled state. To allow modification, delete/modify all of the following states: ')
        # Check that the state is not used as a subprocess in a study
        DependancyErrorCheck(self, StudyModels, lambda (EntryKey,Entry): self.ID == Entry.MainProcess, 'State Dependency Error: The state "' + str(self.Name) +'" cannot be deleted or modified as it is used as a main process by at least one study/model. To allow modification, delete/modify all of the following study/model entries: ')
        # Assertion check for transitions. This is a long assertion check
        # that makes sure that there are no transitions using this state. 
        # This check should never be successful as the code above checks 
        # subprocesses and in order to have a transition a StudyModel that
        # uses this subprocess must exist. The existence of such a study/model
        # implies proper integrity checks. However, to avoid code problems in
        # the future, this assertion error is added.
        DependancyErrorCheck(self, Transitions, lambda (EntryKey,Entry): Entry.FromState == self.ID or Entry.ToState == self.ID, 'ASSERTION ERROR: The State "' + str(self.Name) +'" cannot be deleted or modified as there is at least a transition that references it. To allow modification, delete all of the following transitions: ')
        return 

    def GenerateReport(self, FormatOptions = None):
        """ Generate the report for this entity instance """
        TotalIndent = HandleOption('TotalIndent', FormatOptions,'')
        IndentAtom = HandleOption('IndentAtom', FormatOptions,'  ')
        #ColumnSpacing = HandleOption('ColumnSpacing', FormatOptions,' | ')        
        FieldHeader = HandleOption('FieldHeader', FormatOptions,True)
        LineDelimiter = HandleOption('LineDelimiter', FormatOptions,'\n')
        SectionSeparator = HandleOption('SectionSeparator', FormatOptions,70*'_')
        ShowHidden = HandleOption('ShowHidden', FormatOptions,False)
        ShowDependency = HandleOption('ShowDependency', FormatOptions,False)
        DetailLevel = HandleOption('DetailLevel', FormatOptions, 0)
        # DetailLevel = 0 prints only some State information
        # DetailLevel = 1 additional data is printed
        ReportString = ''
        if ShowHidden:
            ReportString = ReportString + TotalIndent + FieldHeader * 'ID: ' + str(self.ID) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Name: ' + str(self.Name ) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Notes: ' + str(self.Notes).replace('\n','\n'+TotalIndent) + LineDelimiter
        if self.IsSplit:
            ReportString = ReportString + TotalIndent + FieldHeader * 'Splitter State' + LineDelimiter
        if self.JoinerOfSplitter:
            ReportString = ReportString + TotalIndent + FieldHeader * 'Joins the State ' + str(States[self.JoinerOfSplitter].Name) + LineDelimiter
            if ShowHidden:
                ReportString = ReportString + TotalIndent + FieldHeader * 'Splitter State ID: ' + str(self.JoinerOfSplitter) + LineDelimiter
        if self.IsEvent:
            ReportString = ReportString + TotalIndent + FieldHeader * 'Event State' + LineDelimiter
        if self.IsTerminal:
            ReportString = ReportString + TotalIndent + FieldHeader * 'Terminal State' + LineDelimiter

        if self.ChildStates != []:
            ReportString = ReportString + TotalIndent + (FieldHeader * 'A Process ') + LineDelimiter
            if DetailLevel > 0:
                for PooledStateID in self.ChildStates:
                    ReportString = ReportString + TotalIndent + IndentAtom + (FieldHeader * 'Containing the State: ') + States[PooledStateID].Name
                    ReportString = ReportString + LineDelimiter
                if ShowHidden:
                    ReportString = ReportString + TotalIndent + FieldHeader * 'ChildStates: ' + str(self.ChildStates) + LineDelimiter



        if ShowDependency:
            StateIndicatorNames=self.GenerateAllStateIndicatorNames()
            for StateIndicatorName in StateIndicatorNames:
                ReportString = ReportString + TotalIndent + FieldHeader * 'Associated with the State Indicator: ' + str(StateIndicatorName) + LineDelimiter
        ReportString = ReportString + TotalIndent + SectionSeparator + LineDelimiter
        return ReportString

    def Copy(self, NewName = None):
        """ Returns an object that copies this one """
        NewName = CalcCopyName(self, NewName)
        NewRecord = State(ID = 0 , Name = NewName , Notes = self.Notes , IsSplit = self.IsSplit , JoinerOfSplitter = self.JoinerOfSplitter , IsEvent = self.IsEvent, IsTerminal = self.IsTerminal,  ChildStates = self.ChildStates  )
        return NewRecord
    
    # Description String
    Describe = DescribeReturnsName


class Transition:
    """Describes transitions between states in the model and in studies"""
    StudyModelID = 0      # The Study/model ID that the transition belongs to
    FromState = 0         # The State ID from which the transition emanated
    ToState = 0           # The State ID the transition reaches    
    Probability = Expr()  # An expression defining the transition probability 
    Notes = ''            # A string indicating the regression function

    def __init__( self , StudyModelID = 0 , FromState = 0 , ToState = 0 , Probability = Expr() , Notes = '' ):
        """Constructor with default values and some consistency checks"""
        # Check if valid data
        self.VerifyTransitionKey(StudyModelID, FromState, ToState)
        # Check parameter values
        self.VerifyTransitionParameters(Probability)
        # Copy Parameters
        self.StudyModelID = StudyModelID
        self.FromState = FromState
        self.ToState = ToState
        self.Probability = Expr(str(Probability))
        self.Notes = Notes
        return
        
    def VerifyTransitionKey( self, StudyModelID = None , FromState = None , ToState = None):
        """Checks if the transition key is valid"""
        # Check Data
        if StudyModelID == None:
            StudyModelID = self.StudyModelID
        if FromState == None:
            FromState = self.FromState
        if ToState == None:
            ToState = self.ToState
        # Check that the input data is valid
        if FromState == ToState:
            raise ValueError, 'Transition Validation Error: Self loop transitions are not supported. A transition cannot lead to the same state it started from. This Error was raised for the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
        # Check if this study exists
        if not StudyModels.has_key(StudyModelID):
            raise ValueError, 'ASSERTION ERROR: StudyModel ID' + str(StudyModelID) + ' does not exist in the Studies table'
        # Verify no transitions out of and into the null state 
        if (FromState == 0 or ToState == 0): 
            raise ValueError, 'Transition Validation Error: The from state and the to state in the transition must by defined for a model. Make sure the states and the model/study are properly defined and are not empty. '
        # Check if the state exists
        if FromState != 0 and not States.has_key(FromState):
            raise ValueError, 'ASSERTION ERROR: The FromState State ID used in transition does not exist in the States table in transition: (' + 'StudyModelID = ' + str (StudyModelID) + ' FromState = ' + str (FromState) + ' , ToState = ' + str (ToState) + ' )'

        if ToState != 0 and not States.has_key(ToState):
            raise ValueError, 'ASSERTION ERROR: The ToState State ID used in ToState does not exist in the States table in transition: (' + 'StudyModelID = ' + str (StudyModelID) + ' FromState = ' + str (FromState) + ' , ToState = ' + str (ToState) + ' )' 
        # Check to see if all states are in the Model states list
        (AllStates, IsSubProcess, NestingLevel) = States[StudyModels[StudyModelID].MainProcess].FindChildStates()
        if FromState != 0 and FromState not in AllStates:
            raise ValueError, 'Transition Validation Error: The transitions starts from a state that does not belong to the study/model. Make sure that all the states used are defined in the main sub-process of the study/model. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
        if ToState != 0 and ToState not in AllStates:
            raise ValueError, 'Transition Validation Error: The transitions ends in a state that does not belong to the study/model. Make sure that all the states used are defined in the main sub-process of the study/model. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
        # Verify these are not transitions from and into sub-processes
        if FromState != 0 and States[FromState].IsSubProcess():
            raise ValueError, 'The FromState State ID is a subprocess state to which a transition is not allowed in transition: (' + 'StudyModelID = ' + str (StudyModelID) + ' FromState = ' + str (FromState) + ' , ToState = ' + str (ToState) + ' )'
            raise ValueError, 'Transition Validation Error: The transition starts in a sub-process rather than a state. Transitions are not allowed from and to sub-processes. IT is possible, however to make a transition from and to a state in this sub-process. Make sure this rule is followed. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
        if ToState != 0 and States[ToState].IsSubProcess():
            raise ValueError, 'Transition Validation Error: The transition ends in a sub-process rather than a state. Transitions are not allowed from and to sub-processes. It is possible, however, to make a transition from and to a state inside this sub-process. Make sure this rule is followed. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
        # If the transition is from a terminal state
        if FromState !=0 and States[FromState].IsTerminal:
            raise ValueError, 'Transition Validation Error: The transition starts from a terminal state. Since a terminal state stops simulation, such a transition is not practical. Please change the state definition or the transition definition. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
        # If the transition is from a splitter state
        if FromState !=0 and States[FromState].IsSplit:
            # Check that the target state has a nesting level one higher
            # then the originating state
            FromStateNestingLevel = FilterByAnother (NestingLevel, map (lambda StateId : StateId == FromState , AllStates))
            ToStateNestingLevel = FilterByAnother (NestingLevel, map (lambda StateId : StateId == ToState , AllStates))
            if len(FromStateNestingLevel) != 1 or len(ToStateNestingLevel) != 1 :
                raise ValueError, 'ASSERTION ERROR: while extracting nesting level in transition: (' + 'StudyModelID = ' + str (StudyModelID) + ' FromState = ' + str (FromState) + ' , ToState = ' + str (ToState) + ' )'
            if ( ToStateNestingLevel[0] - FromStateNestingLevel[0] ) != 1:
                raise ValueError, 'Transition Validation Error: A transition emanating from a splitter state has to end in a state that belongs to a sub-process that belongs to the same process the splitter state is in. In other words, a transition from a splitter state must land in a state with a nesting level higher by 1 than the splitter state. Please change the transition definitions or the sub-processes to follow this rule. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
            # Check that there are no other transitions into this state in the
            # study/Model - meaning it is the first state in the subprocess
            OtherTransitionsToThisState = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey) : StudyModelIDKey == StudyModelID and ToStateKey == ToState and FromStateKey != FromState, Transitions.keys()))
            if OtherTransitionsToThisState != []:
                raise ValueError, 'Transition Validation Error: A transition emanating from a splitter state cannot land in a state that is not the first state in its sub-process. The first transition does not have any transitions leading into it. Please change the transition definitions or the sub-processes to follow this rule. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
        # If the transition is to a joiner state
        if ToState !=0:
            if States[ToState].JoinerOfSplitter != 0:
                # Check that the target state has a nesting level one lower
                # then the originating state
                FromStateNestingLevel = FilterByAnother (NestingLevel, map (lambda StateId : StateId == FromState , AllStates))
                ToStateNestingLevel = FilterByAnother (NestingLevel, map (lambda StateId : StateId == ToState , AllStates))
                if len(FromStateNestingLevel) != 1 or len(ToStateNestingLevel) != 1 :
                    raise ValueError, 'ASSERTION ERROR: while extracting nesting level in transition: (' + 'StudyModelID = ' + str (StudyModelID) + ' FromState = ' + str (FromState) + ' , ToState = ' + str (ToState) + ' )'
                if ( FromStateNestingLevel[0] - ToStateNestingLevel[0] ) != 1:
                    raise ValueError, 'Transition Validation Error: A transition leading to a joiner state has to start from a state that belongs to a sub-process that belongs to the same process the joiner state is in. In other words, a transition to a joiner state must start in a state with a nesting level higher by 1 than the joiner state. Please change the transition definitions or the sub-processes to follow this rule. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
                # Check that the joiner state is pointing to a splitter state that
                # leads to a state in the same subprocess as the state leading to
                # the joiner. Note that this implies that a splitter transition
                # should be defined before the joiner transition.
                SplitterID = States[ToState].JoinerOfSplitter
                if not States.has_key(SplitterID):
                    raise ValueError, 'ASSERTION ERROR: Non existent Splitter ID defined in the joiner state in transition: (' + 'StudyModelID = ' + str (StudyModelID) + ' FromState = ' + str (FromState) + ' , ToState = ' + str (ToState) + ' )'
                JoiningSubprocess = States[FromState].FindFatherState(StudyModelID)
                OtherTransitionsFromSplitterState = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey) : StudyModelIDKey == StudyModelID and FromStateKey == SplitterID, Transitions.keys()))
                ProcessCorrespondanceFound = False
                for (StudyModelIDKey , FromStateKey , ToStateKey) in OtherTransitionsFromSplitterState:
                    SplittingToSubprocess = States[ToStateKey].FindFatherState(StudyModelID)
                    if JoiningSubprocess == SplittingToSubprocess:
                        if ProcessCorrespondanceFound:
                            raise ValueError, 'ASSERTION ERROR: Joiner and splitter lead to the same subprocess (' + str(JoiningSubprocess) + ') more than once in transition: (' + 'StudyModelID = ' + str (StudyModelID) + ' FromState = ' + str (FromState) + ' , ToState = ' + str (ToState) + ' )'
                        else:
                            ProcessCorrespondanceFound = True
                if not ProcessCorrespondanceFound:
                    raise ValueError, 'Transition Validation Error: The transition to the joiner state and all transitions from the corresponding splitter state do not land in the same sub-process. The sub-processes or relevant transitions may need modification. Alternatively a new transition from the splitter should be defined to this sub-process before defining the transition to the joiner. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
            else:
                if FromState !=0 and not States[FromState].IsSplit:
                    # Check that the FromState and the ToState belong to the 
                    # same subprocess.
                    FromFather = States[FromState].FindFatherState(StudyModelID)
                    ToFather = States[ToState].FindFatherState(StudyModelID)
                    if FromFather != ToFather:
                        raise ValueError, 'Transition Validation Error: The transition leads from one process to another. This is possible only for transitions from a splitter state or to a joiner state in a model. In this case, the transition between sub-processes is not appropriate. Either modify the transition states or the appropriate sub-process definitions. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
                    # Add an assertion check just to be sure things stay ok with
                    # future code changes
                    PooledStatesInFather = States[FromFather].ChildStates
                    if (FromState not in PooledStatesInFather) or (ToState not in PooledStatesInFather):
                        raise ValueError, 'ASSERTION ERROR: detected father for ToState and FromState does not contain at least one of these states'
        # Check cycles among instantaneous states (splitter, event, joiner)
        if FromState !=0 and ToState !=0:
            InstanteneousStates = filter ( lambda Entry: States[Entry].IsSplit or States[Entry].JoinerOfSplitter!=0 or States[Entry].IsEvent, AllStates)
            if ToState in InstanteneousStates and FromState in InstanteneousStates:
                # Check for a path between ToState and FromState. If such a path
                # exists between instantaneous state, it will create a cycle of
                # instantaneous states, which is not supported by the system
                TransitionFromAndToInstantaneous = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey) : StudyModelIDKey == StudyModelID and (ToStateKey in InstanteneousStates) and (FromStateKey in InstanteneousStates), Transitions.keys()))
                (ReachableInstaneneousStates, Distances) = StudyModels[StudyModelID].BFS(InitState = ToState, StateFilter = InstanteneousStates , TransitionFilter = TransitionFromAndToInstantaneous)
                if FromState in ReachableInstaneneousStates:
                    raise ValueError, 'Transition Validation Error: Invalid transition that closes a cycle among instantaneous states (event,Joiner,Splitter). Resolving this error may require modification of another transition since a cycle is formed by multiple transitions. Make sure that there is no other path that passes through instantaneous states that starts at the end state and ends in the start state of the transition that raise the error. The Error was raised by the following transition: ' + self.Describe(StudyModelID, FromState, ToState)
        return
        
    def VerifyTransitionParameters( self, Probability = None ):
        """Verify that the data in the transition parameters is valid"""
        if Probability == None:
            Probability = self.Probability

        # Check validity of data
        if Probability != '':
            # Check the validity of the parameter itself. Only double check that
            # this is an expression. Additional checks will be made in runtime
            try:
                Expr(Probability)
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                raise ValueError, 'ASSERTION ERROR: Transition probability should hold a valid expression at this point. Here are additional details: ' + str(ExceptValue)
        return 

    def IsParamDependant(self, ParamName):
        """ Returns True if dependant on ParamName """
        Result = ParamName in self.FindDependantParams(ParamType = None)
        return Result


    def IsLocked(self):
        """ Checks if the transition is locked """
        # A transition is locked if it is used by a locked model
        if not StudyModels.has_key(self.StudyModelID):
            raise ValueError, 'ASSERTION ERROR: Study model does not exist'            
        Result = StudyModels[self.StudyModelID].IsLocked()
        return Result

    def CheckDependencies(self, CheckForModify = False, ProjectBypassID = 0):
        """ Verifies no dependant data exists """
        # It is allowed to modify a transition if it is allowed to modify its
        # StudyModel.
        if not StudyModels.has_key(self.StudyModelID):
            raise ValueError, 'ASSERTION ERROR: Study model does not exist while checking dependencies'            
        StudyModels[self.StudyModelID].CheckDependencies(CheckForModify = CheckForModify, ProjectBypassID=ProjectBypassID, CheckForTransition = True)
        return

    def FindDependantParams(self, ParamType = None):
        """ Returns associated parameter names """
        Result=[]
        Result = Result + self.Probability.FindDependantParams(ParamType=ParamType)
        return Result
            
    def GenerateReport(self, FormatOptions = None):
        """ Generate the report for this entity instance """
        TotalIndent = HandleOption('TotalIndent', FormatOptions,'')
        IndentAtom = HandleOption('IndentAtom', FormatOptions,'  ')
        #ColumnSpacing = HandleOption('ColumnSpacing', FormatOptions,' | ')        
        FieldHeader = HandleOption('FieldHeader', FormatOptions,True)
        LineDelimiter = HandleOption('LineDelimiter', FormatOptions,'\n')
        SectionSeparator = HandleOption('SectionSeparator', FormatOptions,70*'_')
        ShowHidden = HandleOption('ShowHidden', FormatOptions,False)
        ShowDependency = HandleOption('ShowDependency', FormatOptions,False)
        DetailLevel = HandleOption('DetailLevel', FormatOptions, 0)
        # Details level is currently not used        
        StudyModelTitle = 'Model: '
        ProbabilityTitle = 'Probability: '

        ReportString = ''
        if ShowHidden:
            ReportString = ReportString + TotalIndent + FieldHeader * 'ID: ' + str(( self.StudyModelID, self.FromState, self.ToState )) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * StudyModelTitle + str(StudyModels[self.StudyModelID].Name) + LineDelimiter
        if self.FromState !=0:
            ReportString = ReportString + TotalIndent + FieldHeader * 'From State: ' + str(States[self.FromState].Name) + LineDelimiter
        else:
            ReportString = ReportString + TotalIndent + 'This Model Sinks the To State' + LineDelimiter
        if self.ToState !=0:
            ReportString = ReportString + TotalIndent + FieldHeader * 'To State: ' + str(States[self.ToState].Name) + LineDelimiter
        else:
            ReportString = ReportString + TotalIndent + 'Holds the Study Initial Count in as Probability'  + LineDelimiter
        # Check if this is a study with Regression Data
        ReportString = ReportString + TotalIndent + FieldHeader * ProbabilityTitle + str(self.Probability) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Notes: ' + str(self.Notes).replace('\n','\n'+TotalIndent) + LineDelimiter
        if ShowDependency:
            RevisedFormatOptions = HandleOption('TotalIndent', FormatOptions, TotalIndent + IndentAtom, True)
            RevisedFormatOptions = HandleOption('DetailLevel', RevisedFormatOptions, DetailLevel-1, True)        
            ReportString = ReportString + self.Probability.GenerateReport(RevisedFormatOptions)
        ReportString = ReportString + TotalIndent + SectionSeparator + LineDelimiter
        return ReportString


    def Copy(self, NewStudyID):
        """ Returns an object that copies this one """
        # Note that copying a transition means copying it to a new model
        NewRecord = Transition( StudyModelID = NewStudyID , FromState = self.FromState , ToState = self.ToState , Probability = self.Probability , Notes = self.Notes )
        return NewRecord
    
    # Description String
    def Describe(self, StudyModelID = None, FromState = None, ToState = None, ShowStudyModel = True, ShowFrom = True, ShowTo = True):
        """ Returns a string to describe the transition """
        # Check Data
        if StudyModelID == None:
            StudyModelID = self.StudyModelID
        if FromState == None:
            FromState = self.FromState
        if ToState == None:
            ToState = self.ToState
        OutStr = ''
        if ShowStudyModel:
            OutStr = OutStr + ', In ' + str(StudyModels[StudyModelID].Name)
        if ShowFrom:
            OutStr = OutStr + ', From ' + str(States[FromState].Name)
        if ShowTo:
            OutStr = OutStr + ', To ' + str(States[ToState].Name)
        return OutStr[2:]            


class StudyModel:
    """The main entity that defines either a model or a study"""
    ID = 0           # Unique key identifier of the study/model
    Name = ''        # A string containing the name of the study/model
    Notes = ''       # A string containing additional notes
    CreatedOn = InitTime     # The time this entity was created on
    LastModified = InitTime  # The last time this entity was modified on
    DerivedFrom = 0  # The originating Study/Model ID
    MainProcess = 0  # The ID of the state that pools all the states in the
                     # study/model and is considered the main process

    def __init__( self, ID = 0 , Name = '' , Notes = '' , DerivedFrom = 0 , MainProcess = 0 ):
        """Constructor with default values and some consistency checks"""
        self.VerifyStates(MainProcess)
        if DerivedFrom !=0 and not StudyModels.has_key(DerivedFrom):
            raise ValueError, 'ASSERTION ERROR: Derived From record does not exist in collection'
        # copy the data
        self.ID = ID
        self.Name = Name
        self.Notes = Notes
        self.CreatedOn = datetime.datetime.now()
        self.LastModified = datetime.datetime.now()
        self.DerivedFrom = DerivedFrom
        self.MainProcess = MainProcess
        return

    def VerifyStates (self, MainProcess = None):
        """Check the consistancy of Input data regarding the states"""
        if MainProcess == None:
            MainProcess = self.MainProcess
        if not States.has_key(MainProcess):
            raise ValueError, 'Study/Model Validation Error: The main process does not exist in the states table'
        if not States[MainProcess].IsSubProcess():
            raise ValueError, 'Study/Model Validation Error: The state defined for the Study/Model is not a subprocess.'
        return True

    def FindStatesInStudyModel(self, IncludeSubProcess = False):
        """ Return all states without subprocesses uses FindChildStates """
        (StateIDs, IsSubProcess, NestingLevel) = States[self.MainProcess].FindChildStates()
        if IncludeSubProcess:
            return StateIDs
        else:
            StateSequenceWithoutSubProc = FilterByAnother (StateIDs , map (NotOp,IsSubProcess))
            return StateSequenceWithoutSubProc

    def BFS(self, InitState, StateFilter = None , TransitionFilter = None):
        """Breadth first search finding all acessible States from InitState"""
        # Note that the BFS can be applied considering only a subset of states
        # and transitions defined in StateFilter and TransitionFilter
        AllModelStates = self.FindStatesInStudyModel(IncludeSubProcess = True)
        if InitState not in AllModelStates:
            raise ValueError, 'ASSERTION ERROR: The InitState defined for BFS does not belong to the study/model'
        if StateFilter != None:
            if InitState not in StateFilter:
                raise ValueError, ' ASSERTION ERROR: The InitState defined for BFS does not belong to the provided filter'
        else:
            StateFilter = AllModelStates
        if TransitionFilter != None:
           TransitionFilter = sorted(Transitions.keys())
        # No other validity checks are made on the filters, it is the
        # Resposibility of the caller of this function
        CandidateStates = filter (lambda Entry: Entry in StateFilter, AllModelStates)
        ToBeVisited = [(InitState,0)]
        VisitedStates = []
        VisitedDistances = []
        while (len(ToBeVisited)):
            (CurrentState, Dist) = ToBeVisited.pop(0)
            VisitedStates = VisitedStates + [CurrentState]
            VisitedDistances = VisitedDistances + [Dist] 
            RelevantTransitions = filter(lambda (StudyModelID, FromState, ToState): StudyModelID == self.ID and (FromState == CurrentState) and (ToState in CandidateStates) and (ToState not in VisitedStates), TransitionFilter)
            ToBeVisited = ToBeVisited + map(lambda (StudyModelID, FromState, ToState): (ToState, Dist + 1), RelevantTransitions)
        return (VisitedStates, VisitedDistances)

    def VerifyStudyModelValidity(self):
        """ Performs a set of tests on the model to verify its validity """
        # Distinguish Model from Study
        # If this is a model
        # Extract all states of the subprocess
        (StateIDs, IsSubProcess, NestingLevel) = States[self.MainProcess].FindChildStates()
        if "PrepareSimulation" in DebugPrints:
            print 'VerifyStudyModelValidity: State in Model details:'
            print 'StateIDs: ' + str(StateIDs)
            print 'IsSubprocess: ' + str(IsSubProcess)
            print 'NestingLevel: ' + str(NestingLevel)
        for StateIDIndex in range(len(StateIDs)):
            StateID = StateIDs[StateIDIndex]
            # Just run through ordinary calculations in an attempt to find
            # errors while examining the state
            CurrentState = States[StateID]
            CurrentState.IsSubProcess()
            CurrentState.SubProcessStartInfo(self.ID)
            # Make sure that splitter states and event states have at least
            # One transition to exit them
            if CurrentState.IsSplit or CurrentState.IsEvent or CurrentState.JoinerOfSplitter != 0:
                # Find all the transitions out of the state
                TransitionsOutOfThisState = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey) : StudyModelIDKey == self.ID and FromStateKey == StateID, Transitions.keys()))
                if len(TransitionsOutOfThisState) == 0:
                    raise ValueError, 'Model Validation For Runtime Error: The state ' + CurrentState.Name + ' is either a splitter, an event, or a joiner state without any transitions out of it. This is not reasonable. The Error was detected in the Model ' + self.Name
                if CurrentState.JoinerOfSplitter != 0 or CurrentState.IsSplit:
                    for TransKey in TransitionsOutOfThisState:
                        Probability = Transitions[TransKey].Probability
                        RaiseWarning = False
                        if Probability != None and Probability != '':
                            try:
                                NumericProbability = float(Probability)
                            except:
                                RaiseWarning = True
                            if RaiseWarning or NumericProbability != 1.0:
                                MessageToUser('Warning - Transition from the joiner or splitter state ' + str(StateID) +':' + CurrentState.Name + ' into state ' + str(TransKey[2]) + ' has a probability other than 1. This is not reasonable')
            # If the state is a joiner, test the states/processes it joins
            if CurrentState.JoinerOfSplitter != 0:
                def FindFatherByVector (StateIndex, FatherNestingLevel):
                    """ Nested Function - finds the father by vector"""
                    # Find the father process using FindChildStates results
                    # Use the fact that the StateIDs vector is ordered in
                    # Preorder according to the nesting tree. Therefore the
                    # subprocess will always be before a state. This can be
                    # detected by the nesting level increasing while moving
                    # the index left on the vector
                    FatherSearchIndex = StateIndex - 1
                    while NestingLevel[FatherSearchIndex] != (FatherNestingLevel):
                        if "PrepareSimulation" in DebugPrints:
                            print 'Father Search Index: ' + str(FatherSearchIndex)
                        FatherSearchIndex = FatherSearchIndex - 1
                        # Assertion check
                        if FatherSearchIndex < 0:
                            raise ValueError, 'ASSERTION ERROR: Index should not reach 0 since the sub-process should be first'
                    return FatherSearchIndex
                # Find the father of the joining state
                FatherOfJoiningStateIndex = FindFatherByVector( StateIDIndex , NestingLevel[StateIDIndex] -1 )
                # Find all the transitions into the joiner state
                TransitionsIntoThisState = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey) : StudyModelIDKey == self.ID and ToStateKey == StateID, Transitions.keys()))
                OriginatingSplitters = []
                for TransKey in TransitionsIntoThisState:
                    Trans = Transitions[TransKey]
                    if "PrepareSimulation" in DebugPrints:
                        print 'Transition key: ' + str (TransKey) 
                    # Find the father process of the state leading to the
                    # joiner state
                    PrevToJoinerStateIndex = StateIDs.index(Trans.FromState)
                    if "PrepareSimulation" in DebugPrints:
                        print 'PrevToJoinerStateIndex: ' + str (PrevToJoinerStateIndex)
                    FatherOfPrevToJoinerStateIndex = FindFatherByVector( PrevToJoinerStateIndex , NestingLevel[PrevToJoinerStateIndex] -1 )
                    if "PrepareSimulation" in DebugPrints:
                        print 'FatherOfPrevToJoinerStateIndex: ' + str (FatherOfPrevToJoinerStateIndex)
                    # At this point the father is known, Continue searching
                    # for the grandfather
                    GrandFatherOfPrevToJoinerStateIndex = FindFatherByVector( FatherOfPrevToJoinerStateIndex , NestingLevel[PrevToJoinerStateIndex] -2 )
                    if "PrepareSimulation" in DebugPrints:
                        print 'GrandFatherOfPrevToJoinerStateIndex: ' + str (GrandFatherOfPrevToJoinerStateIndex)
                    if FatherOfJoiningStateIndex != GrandFatherOfPrevToJoinerStateIndex:
                        raise ValueError, 'Model Validation For Runtime Error: Sub-process hierarchy problem detected. Please check the sub-process hierarchy as well as related states and transitions. The joiner state ' + CurrentState.Name + ' has an invalid connection from the state ' + States.ID2Name(Trans.FromState) + ' that belongs to the father sub-process ' + States.ID2Name(FatherOfPrevToJoinerStateIndex) + ' and the grand father sub-process ' + States.ID2Name(GrandFatherOfPrevToJoinerStateIndex) +' which is not the same as the process holding the joiner state: ' + States.ID2Name(FatherOfJoiningStateIndex) + '. This was detected in the Model ' + self.Name
                    (OriginatingSplitter, ProcessStartState) = States[StateIDs[FatherOfPrevToJoinerStateIndex]].SubProcessStartInfo(self.ID)
                    OriginatingSplitters = OriginatingSplitters + [OriginatingSplitter]
                # Verify that the splitter state that generated all the 
                # subprocesses to be joined is the one the joiner state
                # marks to be joined
                if not all (map (lambda Entry: Entry == CurrentState.JoinerOfSplitter, OriginatingSplitters)):
                    raise ValueError, 'Model Validation For Runtime Error: Splitter/joiner conflict.  The joiner state ' + CurrentState.Name + ' joins by transition a splitter state that does not correspond to the stated splitter state ' + States.ID2Name(CurrentState.JoinerOfSplitter) +'. The splitter states joined instead are:' + States.ID2Name(OriginatingSplitters) + '. This was detected in the Model ' + self.Name
            # Verify that terminal states belong to the main subprocess
            # and that there are no outwards transitions from them
            if CurrentState.IsTerminal:
                # Terminal states are first priority
                MainProcessStates =  States[self.MainProcess].ChildStates
                TransitionsOutOfThisState = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey) : StudyModelIDKey == self.ID and FromStateKey == StateID, Transitions.keys()))
                if CurrentState.ID not in MainProcessStates or TransitionsOutOfThisState != []:
                    # Terminal state has outwards transitions or not
                    # part of the main subprocess
                    raise ValueError, 'Model Validation For Runtime Error: The terminal state '+ CurrentState.Name + ' has an invalid transition  emanating from it or it is not part of the main process. This was detected in the Model ' + self.Name
        return

    def CheckDependencies(self, CheckForModify = False, ProjectBypassID = 0, CheckForTransition = False):
        """ Verifies no dependant data exists """
        # CheckForModify is true if checking only for modification or addition.
        # if ProjectBypassID is not zero, then that project will not block
        # modification, unless it is locked. However, a Project bypass should
        # still block deletion of studies, while allowing deletion of
        # transitions. Therefore consider the ProjectBypass void if
        # CheckForModify and CheckForTransition are both not set. 
        if not CheckForModify and not CheckForTransition:
            ProjectBypassID = 0        
        # If the population set is locked, modification and deletion is blocked
        LockingList = self.IsLocked()
        if LockingList != []:
            raise ValueError, 'Study/Model Dependency Error: The Study/Model or its transition cannot be deleted or modified as it is locked by a project using it. To allow modification, unlock all locked projects that use this Study/Model - this can be done by deletion of simulation results or deletion of the estimation generated simulation project. Locking projects are: ' + EntityNameByID(LockingList,None)
        # For Studies/models, simulation projects using the ID can block
        # deletion and modification.
        DependancyErrorCheck(self, Projects, lambda (EntryKey,Entry): Entry.PrimaryModelID==self.ID and Entry.ID != ProjectBypassID, 'Study/Model Dependency Error: The Study/Model '  + self.Name + ' or its transition cannot be deleted or modified as there is at least one project using it. To allow modification, delete/modify all of the following projects: ')
        # Transitions that use this study model can block its deletion/modification
        # However, if a modification of a transition is requested by setting the
        # CheckForTransition to True, then do not perform the check
        if not CheckForTransition:
            DependancyErrorCheck(self, Transitions, lambda (EntryKey,Entry): Entry.StudyModelID==self.ID, 'Study/Model Dependency Error: The Study/Model '  + self.Name + ' cannot be deleted or modified as there is a transition associated with it. To allow modification, delete/modify all of the following transitions: ')
        # A Study/model that was derived from another study/model cannot block
        # deletion and modification. This is handled during deletion and
        # therefore this is not checked here
        return

    def IsLocked(self):
        """ Checks if the StudyModel is locked """
        # A StudyModel set is locked if it is used by a locked project
        LockedCandidatesSimulationProject = sorted(filter(lambda Entry: Entry.PrimaryModelID == self.ID, Projects.values()))
        InLockedSimulationProject = reduce(lambda Accumulator, Entry: Accumulator + Entry.IsLocked(),LockedCandidatesSimulationProject,[])
        Result = InLockedSimulationProject
        return Result

    def FindTransitions(self, SortOption = None):
        """ Returns associated transitions """
        ListOfTransitions = sorted(filter(lambda (StudyModelID, FromState, ToState): StudyModelID == self.ID ,Transitions.keys()))
        # If no SortOption specified, just return the list 
        if SortOption == None:
            Result = ListOfTransitions
        elif SortOption == 'SortByOrderInSubProcess':
            ListOfStatesSorted = self.FindStatesInStudyModel()
            # Create a function to calculate the index according to this list
            # Note that StateID of Zero will have index 0 and other state ID's
            # will appear afterwards starting from Index 1.
            IndexInSortedPlaceList  = lambda StateID: StateID and (ListOfStatesSorted.index(StateID) + 1)
            # Now use this function to create a key function for sorting
            KeyFunc  = lambda TransKey: ( IndexInSortedPlaceList(TransKey[1]) , IndexInSortedPlaceList(TransKey[2]) )
            # Sort the list according to this order 
            Result = sorted(ListOfTransitions, cmp=None, key=KeyFunc)
        else:
            raise ValueError, 'Invalid Sorting option specified'
        return Result

    def CopyTransitionsFromAnotherStudyModel(self, SourceModelID, ProjectBypassID = 0):
        """ Copies transitions from a source model to a destination model """
        # First get all the transitions related to the StudyModel
        if SourceModelID not in StudyModels.keys():
            raise ValueError, 'ASSERTION ERROR: SourceModelID to copy transitions from does not exist'
        # Use the sort order defined by the sub-process information since
        # it makes sure joiner states are defined after splitter states and 
        # therefore the transitions can be added in proper order
        ToCopyTransitions = StudyModels[SourceModelID].FindTransitions(SortOption = 'SortByOrderInSubProcess')
        # Now traverse the transitions and actually copy the transition
        CopyCount = 0
        for ToCopyTransition in ToCopyTransitions:
            try: 
                NewRecord = Transitions[ToCopyTransition].Copy(NewStudyID = self.ID)
                Transitions.AddNew(NewRecord, ProjectBypassID = ProjectBypassID)
                CopyCount = CopyCount + 1
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                MessageToUser ('Copying Transitions from the Study/Model ' + StudyModels[SourceModelID].Describe() + ' to Model ' + self.Describe() + '. Could not copy the transition ' + Transitions[ToCopyTransition].Describe() + '. Here are additional details: ' + str(ExceptValue))
        MessageToUser ('Completed Copying Transitions from the Study/Model ' + StudyModels[SourceModelID].Describe() + ' to Model ' + self.Describe() + '. Number of transitions copied sucessfully is: ' + str(CopyCount) + ' out of ' + str(len(ToCopyTransitions)))
        # Return the copy count 
        return (CopyCount, len(ToCopyTransitions))
                

    def IsParamDependant(self, ParamName):
        """ Returns True if dependant on ParamName """
        Result = ParamName in self.FindDependantParams(ParamType = None)
        return Result
        

    def FindDependantParams(self, ParamType = None):
        """ Returns associated parameter names """
        StudyModelTransitions = self.FindTransitions()
        Result=[]
        for Trans in StudyModelTransitions:
            Result = Result + Transitions[Trans].FindDependantParams(ParamType=ParamType)
        return Result
    
    def GenerateReport(self, FormatOptions = None):
        """ Generate the report for this entity instance """
        TotalIndent = HandleOption('TotalIndent', FormatOptions,'')
        IndentAtom = HandleOption('IndentAtom', FormatOptions,'  ')
        #ColumnSpacing = HandleOption('ColumnSpacing', FormatOptions,' | ')
        FieldHeader = HandleOption('FieldHeader', FormatOptions,True)
        LineDelimiter = HandleOption('LineDelimiter', FormatOptions,'\n')
        SectionSeparator = HandleOption('SectionSeparator', FormatOptions,70*'_')
        ShowHidden = HandleOption('ShowHidden', FormatOptions,False)
        #ShowDependency = HandleOption('ShowDependency', FormatOptions,False)
        DetailLevel = HandleOption('DetailLevel', FormatOptions, 0)
        # DetailLevel = 0, states and transitions are not shown
        # DetailLevel = 1, states and transitions are shown
        StudyModelTitle = 'Model Name:'
        ReportString = ''
        if ShowHidden:
            ReportString = ReportString + TotalIndent + FieldHeader * 'ID: ' + str(self.ID) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * StudyModelTitle + str(self.Name) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Notes: ' + str(self.Notes).replace('\n','\n'+TotalIndent) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Created On: ' + str(self.CreatedOn) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Last Modified: ' + str(self.LastModified) + LineDelimiter
        if ShowHidden:
            ReportString = ReportString + TotalIndent + FieldHeader * 'Derived From ID: ' + str(self.DerivedFrom) + LineDelimiter
        if self.DerivedFrom != 0:
            DerivedStudyModelName = StudyModels[self.DerivedFrom].Name
            ReportString = ReportString + TotalIndent + FieldHeader * 'Derived From: ' + str(DerivedStudyModelName) + LineDelimiter
        if ShowHidden:
            ReportString = ReportString + TotalIndent + FieldHeader * 'Main Process ID: ' + str(self.MainProcess ) + LineDelimiter
        if DetailLevel > 0:
            # Show States
            (StateIDs, IsSubProcess, NestingLevel) = States[self.MainProcess].FindChildStates()
            ReportString = ReportString + TotalIndent + FieldHeader * 'The Model Contains the States: ' + LineDelimiter
            for (StateNum,StateID) in enumerate(StateIDs):
                # Consider introducing nesting level as tabs to the report
                #StateNestingLevel = NestingLevel[StateNum]
                RevisedFormatOptions = HandleOption('TotalIndent', FormatOptions, TotalIndent + IndentAtom, True)
                RevisedFormatOptions = HandleOption('DetailLevel', RevisedFormatOptions, DetailLevel-1, True)        
                ReportString = ReportString + States[StateID].GenerateReport(RevisedFormatOptions)
            # Show Transitions
            ReportString = ReportString + TotalIndent + FieldHeader * 'The Model Contains the Transitions: ' + LineDelimiter
            TransitionList = self.FindTransitions('SortByOrderInSubProcess')
            for TransID in TransitionList:
                # Consider introducing nesting level as tabs to the report
                #TransDominantState = TransID[1] or TransID[2]
                #TransNestingLevel = NestingLevel[StateIDs.index(TransDominantState)]
                RevisedFormatOptions = HandleOption('TotalIndent', FormatOptions, TotalIndent + IndentAtom, True)
                RevisedFormatOptions = HandleOption('DetailLevel', RevisedFormatOptions, DetailLevel-1, True)        
                ReportString = ReportString + Transitions[TransID].GenerateReport(RevisedFormatOptions)
        ReportString = ReportString + TotalIndent + SectionSeparator + LineDelimiter
        return ReportString

    def Copy(self, NewName = None, NewMainProcess=None):
        """ Returns an object that copies this one """
        # Note that a new main process can be defined in addition to a new name
        if NewMainProcess == None:
            NewMainProcess = self.MainProcess
        NewName = CalcCopyName(self, NewName)
        NewRecord = StudyModel( ID = 0 , Name = NewName , Notes = self.Notes , DerivedFrom = self.ID , MainProcess = NewMainProcess )
        return NewRecord

    # Description String
    Describe = DescribeReturnsName


class PopulationSet:
    """Provides a definition of a population set at the top level"""
    ID = 0      # Unique key identifier of the population set
    Name = ''   # A string containing the name of the population set
    Source = '' # A string describing the source data for the population set
    Notes = ''  # A string containing additional notes
    CreatedOn = InitTime     # The time this entity was created on
    LastModified = InitTime  # The last time this entity was modified on
    DerivedFrom = 0   # The originating population set ID 
    DataColumns = []  # A sequence of columns, order is important as it
                      # defines the reading order. The columns are a tuple of
                      # two strings (ParamName,Distribution). An empty 
                      # distribution string means data based population
    Data = []   # A 2D array created from nested sequences. It holds each 
                # Individual record in the internal sequence. The internal
                # sequence holds data for the parameters in the same order
                # These are defined in DataColumns
    Objectives = [] # a sequence of tuples that contain:
                    # FilterExpr - a string/Expr that is evaluated and only 
                    #              Data records that are non zero/None/NaN are
                    #              used in calculating the statistics.
                    # StatExpr - a string/Expr that calculated the statistics
                    #            to be evaluated from the filtered records.
                    # StatFunction - a string from StatFunctions that 
                    #                defines the statistics to be applied on
                    #                StatExpr after filtering Data records with
                    #                FilterExpr.
                    # TargetValue - A target number that the should be reached
                    #               by applying StatFunction on StatExpr for
                    #               Data records filtered by FilterExpr.
                    # Weight - The weight of (TargetValue - StatFunction)^2 in
                    #          the final fitness function. This is a number. 
                    # CalcValue - The value calculated by the Generation
                    #             algorithm for this objective statistiic
                    #             This is None for a distribution based
                    #             population.
                    # CalcError - The error contribution of ths objective 
                    #             to the final error. The error is 
                    #             ((CalcValue-TargetValue)*Weight)**2
                    #             This is None for a distribution based
                    #             population.
                    # Note that Objectives is empty in a data population that
                    # has been changed by hand. It will appear only in a data
                    # population generated by the system or in a distribution
                    # based population defined by the user.
    TraceBack = () # Traceability data is a tuple with information that
                   # allows tracing back the simulation to support
                   # reproducibility. This is a hidden entity for debug
                   # purposes. The Tuple includes the following elements:
                   # DerivedFrom: ID of generating distribution population
                   # GeneratingVersion: DataDef version of the generating code
                   # InitialRandomState: Random state at simulation start
                   # RandomStateFileName: Temp file with random state
                   # TemporaryScriptFile: Temp script generating results
                   # CompileArguments: Arguments passed at compile time
                   # Note that this is relevant only for populations generated
                   # from distributions. This TraceBack information is true
                   # for the moment of creation - if the user modifies the
                   # the population data after creation, then this TraceBack
                   # is removed since it is no longer informative. 
                   # Note that this internal Tag can only be set internally by
                   # the system - this happens only after simulation results
                   # are returned and not at init. A report can output this 
                   # information if Hidden information is requested.
                   # Note that TraceBack information is lost if data is 
                   # recreated by recontructing a database or modified. Yet
                   # since version information is also recorded it leaves open
                   # the possibility to reconstruct this information in future 
                   # versions of MIST. This, however, is not guaranteed since
                   # future versions may change the code in a way that
                   # reproducibility will not be feasible - yet reproducibility
                   # should be possible with the original version of the data 
                   # definitions. 
                   

    def __init__(self, ID = 0, Name = '', Source = '', Notes = '', DerivedFrom = 0, DataColumns = [], Data = [], Objectives = []):
        """Constructor with default values and some consistency checks"""
        # Verify that the data is consistent
        self.VerifyData(Data,DataColumns,Objectives)
        if DerivedFrom !=0 and not PopulationSets.has_key(DerivedFrom):
            raise ValueError, 'ASSERTION ERROR: Derived From record does not exist in collection'
        # Copy variables
        self.ID = ID
        self.Name = Name
        self.Source = Source
        self.Notes = Notes
        self.CreatedOn = datetime.datetime.now()
        self.LastModified = datetime.datetime.now()
        self.DerivedFrom = DerivedFrom
        self.DataColumns = copy.deepcopy(DataColumns)
        self.Objectives = copy.deepcopy(Objectives)
        self.Data = copy.deepcopy(Data)
        self.TraceBack = ()
        return

    def IsDistributionBased(self, DataColumns = None, Objectives = None):
        """return true if defined by distributions"""
        if DataColumns == None:
            DataColumns = self.DataColumns
        if Objectives == None:
            Objectives = self.Objectives
        ColumnNames = map(lambda (ColumnName , Distribution) : ColumnName + ', ', DataColumns)
        DuplicateColumns = FindDuplicatesInSequence(ColumnNames)
        if DuplicateColumns != []:
            raise ValueError, 'Population Set Data Columns Validation Error: Duplicate column names detected. Each column name may appear only once. Please remove all duplicates, such that each column appears only once. Duplicate column names are: ' + ''.join(DuplicateColumns)[:-2]
        # Check if it is valid to assign new numbers to these columns
        for (ColumnName , Distribution) in DataColumns:
            if not Params.has_key(ColumnName):
                raise ValueError, 'Population Set Data Columns Validation Error: Invalid parameter name "' + str(ColumnName) + '" used in the population set, the parameter does not exist in the parameters that were defined'
            if ColumnName not in SystemReservedParametersAllowedInPopulationColumns:
                # If allowed internally by definition, makes more checks
                if Params[ColumnName].ParameterType not in ['Integer','Number','State Indicator']:  
                    raise ValueError, 'ASSERTION ERROR: The parameter "' + str(ColumnName) + '" used in the population set, is of an invalid parameter type to be used in a population set '
                if Params[ColumnName].Formula != '':  
                    raise ValueError, 'Population Set Data Columns Validation Error: The parameter "' + str(ColumnName) + '" used in the population set already has a value or an expression that were assigned to it when the population was defined. Please choose another parameter or redefine this parameter'
        # Check that all distributions are defined or none are defined
        HasDistribution = map(lambda (ColumnName , Distribution) : Distribution != '' , DataColumns)
        if HasDistribution == [] :
            raise ValueError, 'Population Set Data Columns Validation Error: No columns are defined for the population set'
        if min(HasDistribution) != max(HasDistribution):
            HasData = map(lambda Entry: not Entry, HasDistribution)
            ColumnsDefinedByDistribution = ''.join(FilterByAnother(ColumnNames, HasDistribution))[:-2]
            ColumnsDefinedByData = ''.join(FilterByAnother(ColumnNames, HasData) )[:-2]
            raise ValueError, 'Population Set Data Columns Validation Error: Invalid definition of the data columns in the population set. Mixing distributions and data parameters is not supported in the population set. Make sure all data columns are either all defined by data parameters or all defined by distribution. Currently the following columns are defined by distribution: ' + ColumnsDefinedByDistribution + '. The Following columns are defined by data: ' + ColumnsDefinedByData
        DefinedByDistribution = HasDistribution[0]
        for Objective in Objectives:
            if len(Objective)!=7:
                raise ValueError, 'Population Set Data Columns Validation Error: Invalid definition of Objectives - objective is not full with 5 elements: (FilterExpr, StatExpr, StatFunction, TargetValue, Weight). The problematic objective is: ' + str(Objective)
            else:
                (FilterExpr, StatExpr, StatFunction, TargetValue, Weight, CalcValue, CalcError) = Objective
                if not IsStr(FilterExpr):
                    raise ValueError, 'Population Set Data Columns Validation Error: Invalid definition of Objectives - objective has an invalid FilterExpr. The problematic objective is: ' + str(Objective) + 'The invalid value is: ' + str(FilterExpr)
                if not IsStr(StatExpr):
                    raise ValueError, 'Population Set Data Columns Validation Error: Invalid definition of Objectives - objective has an invalid StatExpr. The problematic objective is: ' + str(Objective) + 'The invalid value is: ' + str(StatExpr)
                if StatFunction not in StatFunctions:
                    raise ValueError, 'Population Set Data Columns Validation Error: Invalid definition of Objectives - objective has an invalid StatFunction. The problematic objective is: ' + str(Objective) + 'The invalid value is: ' + str(StatFunction)
                if not IsFinite(TargetValue):
                    raise ValueError, 'Population Set Data Columns Validation Error: Invalid definition of Objectives - objective has an invalid TargetValue. The problematic objective is: ' + str(Objective) + 'The invalid value is: ' + str(TargetValue)
                if not IsFinite(Weight):
                    raise ValueError, 'Population Set Data Columns Validation Error: Invalid definition of Objectives - objective has an invalid Weight. The problematic objective is: ' + str(Objective) + 'The invalid value is: ' + str(Weight)
                if DefinedByDistribution:
                    if CalcValue != None and CalcError != None:
                        raise ValueError, 'Population Set Data Columns Validation Error: Invalid definition of Objectives - objective has an invalid CalcValue, CalcError. For a distribution based population these have None. The problematic objective is: ' + str(Objective) + 'The invalid value is: ' + str((CalcValue,CalcError))
                else:
                    if not IsNumericType(CalcValue):
                        raise ValueError, 'Population Set Data Columns Validation Error: Invalid definition of Objectives - objective has an invalid CalcValue. The problematic objective is: ' + str(Objective) + 'The invalid value is: ' + str(CalcValue)
                    if not IsNumericType(CalcError):
                        raise ValueError, 'Population Set Data Columns Validation Error: Invalid definition of Objectives - objective has an invalid CalcError. The problematic objective is: ' + str(Objective) + 'The invalid value is: ' + str(CalcError)

        return DefinedByDistribution

    # The following line will allow calling the method directly
    # from the class without an instance to help maintain strict data integrity
    ClassIsDistributionBased = ClassFunctionWrapper(IsDistributionBased)


    def VerifyColumns(self, DataColumns = None, Objectives = None):
        """Check columns, return dependancies if defined by distributions"""
        # Note that if defined by distributions, the full list of dependencies
        # for each column is returned to later allow distinguishing the order
        # or processing, an empty list is returned otherwise
        def RecursivelyCheckCyclesInPopulationDefinitions(DestinationParamInFocus, BannedParams, DestinationColumns, SourceExpressions):
            """recursively Check if there is an infinite cycle in data columns"""
            DestinationIndex = DestinationColumns.index(DestinationParamInFocus)
            SourceExpression = SourceExpressions[DestinationIndex]
            if SourceExpression.strip() == '':
                raise ValueError, 'ASSERTION ERROR: There was no expression defined for column ' + DestinationParamInFocus 
            # Find all dependant parameters in the expression to be used
            TempExpr=Expr(SourceExpression)
            DependantParams = TempExpr.DependantParams
            DepedencySet = [DestinationParamInFocus]
            # Loop through all dependant parameters
            for DependantParam in DependantParams:
                if DependantParam in BannedParams:
                    raise ValueError, 'Population Set Data Columns Validation Error: Population Dependency Cycle Check: Detected a cyclic dependency. The parameter ' + DependantParam + ' somehow references itself - possibly through other parameters. This cyclic reference was detected while the recursive analysis reached the parameter ' + DestinationParamInFocus + ', and the recursive history includes the following parameters: ' + str(BannedParams) 
                # ignore functions and system reserved parameters
                if Params[DependantParam].ParameterType not in ['System Reserved']:
                    # If the dependant parameter is another population column
                    # then continue recursively checking while adding the current
                    # column to the banned list. If it is referenced later, this
                    # will cause an error
                    if DependantParam in DestinationColumns:
                        DependanciesChecked = RecursivelyCheckCyclesInPopulationDefinitions(DependantParam, BannedParams + [DestinationParamInFocus], DestinationColumns, SourceExpressions)
                        DepedencySet = DepedencySet + DependanciesChecked
                    elif Params[DependantParam].Formula == '':
                        # this check is made here to avoid a runtime error
                        # during population generation. If needed to make
                        # things more convenient to the user during data
                        # entry it can be lifted here and raised during
                        # generation of simulation data.
                        raise ValueError, 'Population Set Data Columns Validation Error: Population Dependency on an empty parameter: The parameter ' + DependantParam + ' does not contain a formula nor references another parameter in the population set. This will result in an error while generating a population set. This reference was detected while analyzing the parameter ' + DestinationParamInFocus
            # Note that the dependency list will always contain the
            # DestinationParamInFocus as part of the set. This does not mean 
            # that the column in focus depends on itself. In that case an error
            # will be created. Also note that the result is a list.
            RetVal = list(set(DepedencySet))
            return RetVal

        def CheckDependenciesInObjectives(DestinationColumns, Objectives):
            """ Check if there is an invalid dependency in Objectives """
            DepedencySet = []
            for Objective in Objectives:
                (FilterExpr, StatExpr, StatFunction, TargetValue, Weight, CalcValue, CalcError) = Objective
                TempStatExpr = Expr(StatExpr)
                TempFilterExpr = Expr(FilterExpr)
                DependantParams = TempStatExpr.DependantParams + TempFilterExpr.DependantParams
                DepedencySet = DepedencySet + DependantParams
                for DependantParam in DependantParams:
                    # ignore functions and system reserved parameters
                    if Params[DependantParam].ParameterType not in ['System Reserved']:
                        # If the dependant parameter is not in a population
                        # column that will be calculated, then raise an error
                        # since there will be no value for this
                        if DependantParam not in DestinationColumns:
                            raise ValueError, 'Population Set Objectives Validation Error: Population Dependency on a parameter that is not calculated: The parameter ' + DependantParam + ' does is not a calculated parameter in the population set. This will result in an error while generating a population set. This reference was detected while analyzing the Objective ' + str(Objective)
            # Trancate the set
            RetVal = list(set(DepedencySet))
            return RetVal
        
        if DataColumns == None:
            DataColumns = self.DataColumns
        if Objectives == None:
            Objectives = self.Objectives
        DefinedByDistribution = PopulationSet.ClassIsDistributionBased(None,DataColumns,Objectives)
        ReturnDependancyList = []
        if DefinedByDistribution:
            # reformat list to reuse later when calling recursive function
            DestinationColumns = map (lambda (ColumnName , Distribution): ColumnName , DataColumns)
            SourceExpressions = map (lambda (ColumnName , Distribution): Distribution, DataColumns)
            # Check if data columns are valid parameters and distributions
            for (ColumnName , Distribution) in DataColumns:
                # Previously checked for validity of Assigned parameter
                # Note that some of this code allows Distribution expressions
                # as well as distribution parameters.
                DependanciesForThisColumn = RecursivelyCheckCyclesInPopulationDefinitions(ColumnName, [], DestinationColumns, SourceExpressions)
                # Ignore the self Dependency as it does not exist. An error
                # would have been returned if this was the case
                DependanciesForThisColumn.remove(ColumnName)
                ReturnDependancyList = ReturnDependancyList + [ DependanciesForThisColumn ]
            DependanciesForObjectives = CheckDependenciesInObjectives(DestinationColumns, Objectives)
            ReturnDependancyList = ReturnDependancyList + DependanciesForObjectives
        return ReturnDependancyList

    # The following line will allow calling the method directly
    # from the class without an instance to help maintain strict data integrity
    ClassVerifyColumns = ClassFunctionWrapper(VerifyColumns)

    def VerifyData(self , Data = None , DataColumns = None, Objectives = None, VerifyValues = True):
        """Check that the data include all columns"""
        # If input variable not supplied, use the data in self
        if Data == None:
            Data = self.Data
        if DataColumns == None:
            DataColumns = self.DataColumns
        if Objectives == None:
            Objectives = self.Objectives
        # Check that the population is not defined by data, distribution, and
        # Objectives
        IsDistributionType = PopulationSet.ClassVerifyColumns(None,DataColumns,Objectives)
        if IsDistributionType and Data != []:
            raise ValueError, 'ASSERTION ERROR: A population set defined by distributions has data attached to it.'
        elif not IsDistributionType and Data == []:
            ColumnNames = ''.join(map(lambda (ColumnName , Distribution) : ColumnName + ', ', DataColumns))[:-2]
            raise ValueError, 'Population Set Data Validation Error: No data was defined for a population not defined by a distribution. A population must be defined by either population data or by data distribution. Data is missing for the following columns: ' + ColumnNames
        if Data != []:
            # check compatibility of sequence lengths
            LengthsCompatible = map(lambda InternalSequence : len(InternalSequence) == len(DataColumns) , Data )
            if not all(LengthsCompatible):
                raise ValueError, 'Population Set Data Validation Error: Number of parameters defined does not conform to the number of columns for this population set.'
            if VerifyValues:
                for (RowNum,DataRecord) in enumerate(Data):
                    for (ColumnNum,DataEntry) in enumerate(DataRecord):
                        ParamName = DataColumns[ColumnNum][0]
                        # If the date in the data entry is None, this means no
                        # data was defined. This is currently allowed and may
                        # be blocked in the future
                        if DataEntry != None:
                            try:
                                Params[ParamName].VerifyValidity(str(DataEntry))
                            except:
                                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                                raise ValueError, 'Population Set Data Validation Error: The data value defined for parameter "' + str(ParamName) + '" used in the population set in array position = '+ str((RowNum+1,ColumnNum+1)) +' is an invalid value. Here are additional details on the error: ' + str(ExceptValue)
        return


    def ImportDataFromCSV(self, FileName, ImportColumnNames = True):
        """Import data and column names from a CSV file"""
        # Note that Distribution based population import is not supported and
        # neither objectives uplod from CSV
        # First open the file and read data from it
        (DataColumns,Data)=ImportDataFromCSV(self, FileName,  ImportColumnNames, ConvertTextToProperDataType = True, TextCellsAllowed = False)
        # Verify the information in the columns, avoid using self keyword
        PopulationSet.ClassVerifyColumns(None,DataColumns)
        # Now verify that this data is valid and corresponds to the columns
        # again avoid using the self keyword
        PopulationSet.ClassVerifyData(None , Data , DataColumns, [])
        self.DataColumns = DataColumns
        self.Data = Data
        return (DataColumns,Data)


    def ExportDataToCSV(self, FileName, ExportColumnNames=True):
        """Export data to a CSV file"""
        # Prepare the data 
        # Note that the value None will be exported as an empty entry so no
        # change is required to the data at the entry level
        if ExportColumnNames:
            if self.IsDistributionBased():
                # Note that currently distribution based population sets cannot
                # be loaded back to the system using the import function. 
                # also objectives are not saved
                ColumnHeaders = self.DataColumns
            else:
                ColumnHeaders = map(lambda (ColumnName , Distribution) : ColumnName, self.DataColumns)
        else:
            ColumnHeaders = None
        ExportDataToCSV(FileName, self.Data, ColumnHeaders)
        return


    def PreparePopulationSetForSimulation(self, StudyModelID , RepairPopulation = DefaultSystemOptions['RepairPopulation'], VerboseLevel = DefaultSystemOptions['VerboseLevel']):
        """ Returns a Population set suitable for simulation of the model """
        if "PreparePopulationSetForSimulation" in DebugPrints:
            print 'ID:' + str(StudyModelID)
        # First create a new population set copied from this population set
        SimulationPopulationSet = PopulationSet( ID = 0, Name = self.Name, Source = 'Prepared for Simulation from: ' + self.Source , Notes = 'Original Notes Before Preparation were: ' + self.Notes, DerivedFrom = self.ID, DataColumns = self.DataColumns, Data = self.Data, Objectives = self.Objectives)
        # Extract all parameter names from the parameter list of the population set
        PopSetParamNames = map(lambda (ParamName, Distribution): ParamName , self.DataColumns )
        # All new parameters will be added from this index position
        NewParamStartPos = len(PopSetParamNames)
        CurrentParamPos = NewParamStartPos - 1
        OverallSortOrder = 0
        # Add all state indicators associated with the model in the project
        # that do not already exist in the simulation population set
        ModelStateIDs = StudyModels[StudyModelID].FindStatesInStudyModel(IncludeSubProcess = True)
        AllModelStateIndicators = []
        NewStateIndicators = []
        AllStateIndicatorHelperDict = {}
        ProcessIndicatorsSetByChild = 0
        # Traverse all states in the model
        for ModelStateID in ModelStateIDs:
            ModelState = States[ModelStateID]
            StateIndicators = ModelState.GenerateAllStateIndicatorNames()
            # Build a list of all state indicators
            AllModelStateIndicators = AllModelStateIndicators + StateIndicators
            # Find out about the father state
            FatherStateID = States[ModelStateID].FindFatherState(StudyModelID)
            for (IndicatorTypeInd, StateIndicator) in enumerate(StateIndicators):
                # Find all ancestors of the state with the same indicator Type
                if FatherStateID != 0:
                    # Modifies the index pos by the fathers index pos. 
                    try:
                        # The dictionary is searched by the new tuple
                        # (Father state ID, Indicator Type Index)
                        FatherRecord = AllStateIndicatorHelperDict[(FatherStateID,IndicatorTypeInd)]
                    except:
                        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                        raise ValueError, 'ASSERTION ERROR: All relevant states of the model should exist in the Helper dictionary when referenced. Here are details of the error:' + str(ExceptValue)
                    # Add the father position to the previously calculated
                    # list of positions. This indicates the Lineage of
                    # sub process ancestors. Each position is a tuple of the
                    # form (PositionID,WasTheFatherNewlyDefined)
                    FatherPos = [(FatherRecord[2],FatherRecord[5])] + FatherRecord[3]
                    # store IDS as well
                    FatherIDs = [FatherStateID] + FatherRecord[1]
                else:
                    FatherPos = []
                    FatherIDs = []                   
                if IndicatorTypeInd != 0:
                    # If this is not an actual state indicator, find the
                    # actual record
                    try:
                        ActualCounterpartRecord = AllStateIndicatorHelperDict[(ModelStateID,0)]
                    except:
                        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                        raise ValueError, 'ASSERTION ERROR: Actual state indicator should be defined before other indicator types. Here are details of the error:' + str(ExceptValue)
                    ActualPos = ActualCounterpartRecord[2]
                else:
                    # If this was the actual record, mark the current
                    # position as actual
                    ActualPos = CurrentParamPos
                # if this is a new
                IsNewParam = StateIndicator not in PopSetParamNames
                if IsNewParam:
                    NewStateIndicators = NewStateIndicators + [StateIndicator]
                    CurrentParamPos = CurrentParamPos + 1
                    ParamPosToStore = CurrentParamPos
                else:
                    ParamPosToStore = PopSetParamNames.index(StateIndicator)
                # The Helper Dictionary holds the following:
                # Key tuple:
                # [0]: The State ID generating this indicator
                # [1]: The indicator type index  (actual, entered etc.)
                # Data list:
                # [0] - State Indicator Param name
                # [1] - The Father State IDs for ancestors
                # [2] - The Indicator position index in the data
                # [3] - The Father Indicator position index in the data
                # [4] - The Actual Indicator position index in the data
                # [5] - Is it a newly created Indicator
                # [6] - If a subprocess state
                # [7] - Child group classification of a subprocess
                # [8] - Sort order
                AllStateIndicatorHelperDict [(ModelStateID, IndicatorTypeInd)] = [StateIndicator, FatherIDs, ParamPosToStore, FatherPos, ActualPos, IsNewParam, ModelState.IsSubProcess(), {} ,OverallSortOrder ]
                OverallSortOrder = OverallSortOrder + 1
        # Update the column list in the new population set
        SimulationPopulationSet.DataColumns = SimulationPopulationSet.DataColumns + map(lambda Entry: (Entry,''), NewStateIndicators)
        if "PrepareSimulation" in DebugPrints:
            print 'RevisedPopulationSet Columns are:' + str(map(None ,enumerate(map(lambda (ParamName,Prevalence): ParamName, SimulationPopulationSet.DataColumns))))
        # Prepare several lists for later use
        InvalidDataRecords = []
        InvalidDataEntries = []
        # Reorder the sort order of the helper vector. This generally does not
        # change results. However, if errors occur they will be presented
        # in a hierarchical way to the user. This means errors concerning
        # subprocesses before will be presented before states, actual states
        # before diagnosed etc.
        HelperIterationList = sorted ( map (None, AllStateIndicatorHelperDict.iteritems()), None , key = lambda (HelperKey, HelperEntry): HelperEntry[8] )
        # Extract child group states for subprocess states. A child group is
        # either: 1) a single non-subprocess state, 2) all the subprocesses
        # belonging to this subprocess that emanate from the same splitter
        for (HelperKey, HelperEntry) in HelperIterationList:
            IsSubProcess = HelperEntry[6]
            # If the state indicator is set to 1 and it is a subprocess
            if IsSubProcess:
                AnalyzedState = States[HelperKey[0]]
                # Create the dictionary for the groups, It already has the
                # default group 0 for all non splitter states
                ChildGroups = {0:[]}
                # traverse all states in the subprocess and create a group
                # for each splitter state
                for ChildStateID in AnalyzedState.ChildStates:
                    if States[ChildStateID].IsSplit:
                        ChildGroups[ChildStateID] = []
                if "PrepareSimulation" in DebugPrints:
                    print 'Processing ID:' + str(AnalyzedState.ID)
                    print 'Child Groups:' + str(ChildGroups)
                # Having the dictionary keys in place, classify the states
                # according to the categories. Note that classification will be
                # according to position codes to speed up checking individuals
                for ChildStateID in AnalyzedState.ChildStates:
                    ChildStateHelperEntry = AllStateIndicatorHelperDict[(ChildStateID,HelperKey[1])]
                    ChildStatePos = ChildStateHelperEntry[2]
                    # Find the splitter states responsible for the subprocesses
                    (SplitterID , StartStateID) = States[ChildStateID].SubProcessStartInfo(StudyModelID)
                    # Add the position to the state
                    try:
                        ChildGroups[SplitterID] = ChildGroups[SplitterID] + [ChildStatePos]
                    except:
                        # This error may be deprecated. Consider removing it
                        # It was left here in case it will be raised again
                        # This may happen if SplitterID is out of range
                        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                        raise ValueError, 'ASSERTION ERROR: Population Set Preparation for Simulation Error. All sub-processes have to be lead to from a splitter state in the sub-process. This error was detected when constructing child groups. Here are details of the error: ' + str(ExceptValue)
                # After the child group was created, dismantle child group 0
                # into several child groups with the key (0,ChildStatePos)
                for ChildStatePos in ChildGroups[0]:
                    ChildGroups[(0,ChildStatePos)] = [ChildStatePos]
                # Now delete child group 0 as it does not represent an actual
                # child group. Rather it was an intermediate stage
                del ChildGroups[0]
                # Update the Entry in the helper vector with this child Group
                AllStateIndicatorHelperDict[HelperKey][7] = ChildGroups
        # Traverse all individuals to check the existing data and update the
        # record with new data
        for (IndividualNum, IndividualRecord) in enumerate(SimulationPopulationSet.Data):
            # First verify that there is no None entry in the data
            # which will make it invalid. Collect all invalid entries.
            # Note that NaN is now considered a valid entry and is not removed
            # The user has to make sure that NaN will not violate any validity
            # checks during computation.
            for (Index,Entry) in enumerate(IndividualRecord):
                if Entry == None:
                    # note that data records are added in reverse order
                    # note that indices have 1 added to them since these
                    # are displayed to the user later on.
                    InvalidDataRecords = [IndividualNum + 1] + InvalidDataRecords
                    InvalidDataEntries = InvalidDataEntries + [(IndividualNum +1, Index+1)]
            # Expand the data to correspond for the new columns
            # Note that this automatically initializes all the new state
            # indicators to 0. This can later be changed if required
            SimulationPopulationSet.Data[IndividualNum] = IndividualRecord = IndividualRecord + [0]*len(NewStateIndicators)
            # Reset flag for detecting records with no state set
            AtLeastOneActualStateIsSet = False
            # Update subprocess values according to current state indicator
            # For this, traverse all state indicators
            for (HelperKey, HelperEntry) in HelperIterationList:
                if "PrepareSimulation" in DebugPrints:
                    print ' Processing HelperEntry: ' + str(HelperEntry)
                # If the state indicator is set to 1
                CurrentStatePos = HelperEntry[2]
                if IndividualRecord[CurrentStatePos] == 1:
                    if HelperKey[1] == 0:
                        # If this was an actual state, mark that at least one
                        # state has been set for this individual
                        AtLeastOneActualStateIsSet = True
                        # Note that only actual state indicators get checked 
                        # for repair. Entered State indicators will not apply
                        # to their 
                        StateAnsestorsToCheck = HelperEntry[3][:]
                        while StateAnsestorsToCheck != []:
                            (StateIndexToCheck, IsStateToCheckIsNew) = StateAnsestorsToCheck.pop(0)
                            # Check if the ancestor is not set to 1.
                            if IndividualRecord[StateIndexToCheck] != 1:
                                # If repairing problems is required
                                if RepairPopulation:
                                    if IsStateToCheckIsNew:
                                        SimulationPopulationSet.Data[IndividualNum][StateIndexToCheck] = IndividualRecord[StateIndexToCheck] = 1
                                        if VerboseLevel >= 10:
                                            MessageToUser('Population Set Preparation for Simulation Warning: The state indicator for the process "' + str(SimulationPopulationSet.DataColumns[StateIndexToCheck][0] )  +'" was set to 1 for individual #' + str(IndividualNum+1) + ' by a child state indicator "' +  str(SimulationPopulationSet.DataColumns[CurrentStatePos][0]) + '"')
                                            ProcessIndicatorsSetByChild = ProcessIndicatorsSetByChild + 1
                                    else:
                                        raise ValueError, 'Population Set Preparation for Simulation Error: The state indicator for the process "' + str(SimulationPopulationSet.DataColumns[StateIndexToCheck][0] )  +'" cannot be set to 1 for individual #' + str(IndividualNum+1) + ' by a child state indicator "' +  str(SimulationPopulationSet.DataColumns[CurrentStatePos][0]) + '". The reason is that this sub-process was defined explicitly in the input as having another value. Setting the system parameter RepairPopulation may resolve this conflict. However, please check the input data before doing so to make sure this is allowed. Ideally, all states should be properly defined in the data.'
            # Verify that for each sub-process set to 1, there is only
            # one child group set to 1. 
            for (HelperKey, HelperEntry) in HelperIterationList:
                # Perform this test only to actual state indicators
                # other state indicator types are not checked since these
                # are either user controlled or Entered which may differ
                # between sub-processes
                if HelperKey[1] == 0:
                    CurrentStatePos = HelperEntry[2]
                    IsSubProcess = HelperEntry[6]
                    ChildGroups = HelperEntry[7]
                    SetChildGroupsDetected = None
                    # If the state indicator is set to 1 and it is a sub-process
                    if IndividualRecord[CurrentStatePos] == 1 and IsSubProcess:
                        for (ChildGroupKey, ChildGroupStatePositions) in ChildGroups.iteritems():
                            # Check that all states of a group are 0
                            SubProcessStatesSet = map (lambda Entry: IndividualRecord[Entry]==1 ,ChildGroupStatePositions)
                            if "PrepareSimulation" in DebugPrints:
                                print 'SetChildGroupsDetected are:' + str(SetChildGroupsDetected)
                                print 'SubProcessStatesSet are:' + str(SubProcessStatesSet)                                    
                            if not IsTuple(ChildGroupKey):
                                # If this is a sub process, this means these 
                                # all have to be equal. 
                                if not all (map (lambda Entry: Entry == SubProcessStatesSet[0], SubProcessStatesSet)):
                                    raise ValueError, 'Population Set Preparation for Simulation Error: Conflicting values have been detected within a child group within a set process. In other words there is a sub-process that does not agree with other sub-processes starting from the same splitter state. This error was detected where a sub-process has been set for individual #' + str(IndividualNum+1) + ' The sub-process indicator is ' + HelperEntry[0] +' which corresponds to column ' + str(CurrentStatePos) + ' and the conflicting sub-process columns are: ' + str (ChildGroupStatePositions) + ' that correspond to the sub-processes' + str(map(lambda Entry, EntryVal: SimulationPopulationSet.DataColumns[Entry][0] + '=' +str(EntryVal), ChildGroupStatePositions,SubProcessStatesSet)) 
                            # Check if a child group was detected to be set
                            if SubProcessStatesSet[0]:
                                # Check if this is the first child group to be set
                                if SetChildGroupsDetected == None:
                                    # Raise the flag indicating that a child group
                                    # was set
                                    SetChildGroupsDetected = FilterByAnother (ChildGroupStatePositions, SubProcessStatesSet)
                                else:
                                    # Raise an error if this is not the first
                                    # child group set for this record
                                    raise ValueError, 'Population Set Preparation for Simulation Error: More than one state is set for a specific sub process in individual #' + str(IndividualNum+1) + ' The set subprocess indicator in which the problem was detected is '+ HelperEntry[0] +' which corresponds to column ' + str(CurrentStatePos) + ' and the conflicting sub-process column that raised while examining the following position: ' + str(ChildGroupStatePositions) + ' Overall, the following related columns are set and may cause the problem ' + str(map(lambda Entry: SimulationPopulationSet.DataColumns[Entry][0], ChildGroupStatePositions+SetChildGroupsDetected)) 
                        if not SetChildGroupsDetected:
                            raise ValueError, 'Population Set Preparation for Simulation Error: No states have been set for a set sub-process for Individual #' + str(IndividualNum+1) + ' The sub-process in which the problem was detected is '+ HelperEntry[0] +' which corresponds to column ' + str(CurrentStatePos)
                            # In the future, this may be corrected by setting the
                            # first state in the subprocess. If this is done, note
                            # that a check should be made that the state is new
            if not AtLeastOneActualStateIsSet:
                raise ValueError, 'Population Set Preparation for Simulation Error: No states have been set for Individual #' + str(IndividualNum+1) + '. Therefore simulation cannot start since no start state exists. To resolve this, please set at least one column in the population set'
                # In the future, this may be corrected by setting the
                # first state in the sub-process. If this is done, note
                # that a check should be made that the state is new
        if InvalidDataRecords != []:
            if RepairPopulation>=10:
                # if RepairPopulation is at a very high level, then remove
                # records with empty data.
                # Note that numbers will be in reverse order to allow deletion
                for RecordNumber in InvalidDataRecords:
                    # Delete the invalid record from the new population set
                    del SimulationPopulationSet.Data[RecordNumber-1]
                    if VerboseLevel >=5:
                        MessageToUser ('While preparing the population set for simulation record #'+str(RecordNumber) + '  was deleted due to missing entries in the following columns:' + str(filter (lambda (IndividualNumTemp, EntryNumber): IndividualNumTemp == RecordNumber, InvalidDataEntries)))
                if len(SimulationPopulationSet.Data)==0:
                    raise ValueError, 'Population Set Preparation for Simulation Error: The population set was emptied from data while removing inappropriate records.'
            else:
                raise ValueError, 'Population Set Preparation for Simulation Error: Invalid records detected in the population set data while preparing for simulation - entries with NaN or None values are not allowed, the following records have such values using the keys (Record #, Entry #):' + str(InvalidDataEntries)
        if VerboseLevel >=1:
            MessageToUser ('Preparing the population set for simulation reports '+str(ProcessIndicatorsSetByChild) + ' process state indicators set by child and ' + str(len(InvalidDataRecords)) + ' records deleted due to missing entries')
        if "PrepareSimulation" in DebugPrints:
            print 'RevisedPopulationSet Columns are:' + str(SimulationPopulationSet.DataColumns)
            print 'RevisedPopulationSet Data is:' + str(SimulationPopulationSet.Data)
        return SimulationPopulationSet    


    def GenerateDataPopulationFromDistributionPopulation(self, GeneratedPopulationSize, GenerationFileNamePrefix = None, OutputFileNamePrefix = None , RandomStateFileNamePrefix = None, GenerationOptions = None, SkipDumpingFilesIfError = True , RecreateFromTraceBack = None, DeleteScriptFileAfterRun = True):
        " Generate a new data population from distributions - encapsulating"
        # Compile the generation script with default options
        ScriptFileNameFullPath = self.CompilePopulationGeneration (GeneratedPopulationSize, GenerationFileNamePrefix , OutputFileNamePrefix , RandomStateFileNamePrefix , GenerationOptions, SkipDumpingFilesIfError, RecreateFromTraceBack )
        # run the generation script and collect results
        Results = self.RunGenerationAndCollectResults(GenerationFileName = ScriptFileNameFullPath, NumberOfProcessesToRun = 0, OutputConnection = None, DeleteScriptFileAfterRun = DeleteScriptFileAfterRun)
        return Results           


    def CompilePopulationGeneration (self, GeneratedPopulationSize, GenerationFileNamePrefix = None, OutputFileNamePrefix = None , RandomStateFileNamePrefix = None, GenerationOptions = None, SkipDumpingFilesIfError = True , RecreateFromTraceBack = None):
        """ Compiles a population generation program and returns its path"""

        def CalculateProperColumnOrderForGeneration():
            """ Determines the proper order of processing columns during generation """
            # extract dependencies
            DependanciesForColumns = self.VerifyColumns()
            # initialize the column order to be the predefined order of columns
            InitialColumnOrder =  map ( lambda (ColumnName , Distribution): ColumnName , self.DataColumns)
            ProperColumnOrder = InitialColumnOrder[:]
            CurrentIndex = 0
            # walk over proper column order vector
            while CurrentIndex < len(ProperColumnOrder):
                ColumnName = ProperColumnOrder[CurrentIndex]
                # since the current index may have changed, look it up in the original
                # list of columns
                ColumnNameIndexInDependecies = InitialColumnOrder.index(ColumnName)
                # find the dependencies on this column and represent them as indices
                # referring to the current sort order list
                DependancyNames = DependanciesForColumns[ColumnNameIndexInDependecies]
                DependancyIndices = map ( lambda Entry: ProperColumnOrder.index(Entry) , DependancyNames)
                if DependancyIndices != []:
                    MaxDependantIndex = max(DependancyIndices)
                    # now check if the dependant will be processed after this column
                    # i.e. check that the index of the max index is higher than the
                    # current index.
                    if MaxDependantIndex > CurrentIndex:
                        # A dependency on a future calculated parameter was detected,
                        # swap the parameters with the last dependant.
                        ProperColumnOrder[CurrentIndex] = ProperColumnOrder[MaxDependantIndex]
                        ProperColumnOrder[MaxDependantIndex] = ColumnName
                        # repeat the loop without increasing the loop index. This means
                        # that the new dependant will now be examined
                        continue
                    elif MaxDependantIndex == CurrentIndex:
                        raise ValueError, "ASSERTION ERROR: Dependency on self should have been detected before this code"
                # increase iterator and continue, note that this does not happen if a
                # switch was made. It happens only when no dependents are found of when
                # dependents have been previously passed
                CurrentIndex = CurrentIndex + 1
            # return the newly calculated column order to process as indices to
            # the original order
            ProperColumnIndexOrder = map (lambda Entry: InitialColumnOrder.index(Entry), ProperColumnOrder)
            return ProperColumnIndexOrder

        def WriteGenLine(InString = None):
            """ Writes a line into the script file, including a new line """
            if InString == None:
                InString = ''
            try:
                GenFile.write (InString + '\n')
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                raise ValueError, 'Population Generation Compilation Error: Error encountered while writing to the script file ' + ScriptFileNameFullPath  +'. Please make sure that the file was not locked by the system due to quota or other reasons. The error was detected for the project ' + self.Name + '. Here are details about the error: ' + str(ExceptValue)
            return

        # if recreating simulation from traceback - some input parameters are 
        # recovered from the traceback - Note that the last element in the
        # tuple recored in _CompileArguments in the previous run
        # Note the Dummy parameters are never used, GenerationOptions are
        # replicated from the previous run since those are substantial to the 
        # simulation and not only control the random seed, also 
        # GeneratedPopulationSize is important - the rest of the
        # parameters are not substantial
        if RecreateFromTraceBack != None:
            (GeneratedPopulationSize, DummyGenerationFileNamePrefix, DummyOutputFileNamePrefix, DummyRandomStateFileNamePrefix, GenerationOptions, DummySkipDumpingFilesIfError) = RecreateFromTraceBack[-1][:-1]
        # first check that this population set is based on a distribution:
        if not self.IsDistributionBased():
            raise ValueError, 'Population Generation Compilation Error: The source population set is not distribution based. Select a distribution based population set to perform a data generation option' 
        if GenerationOptions == None:
            GenerationOptions = []
        GenerationOptionsToUse = []
        # Generation options are defined in the following priority order:
        # 1) GenerationOptions as defined in the function input,
        # 2) User defined system option Defaults,
        # 3) Global system defaults
        # Each system option is handled and collected according to the
        # above priority hierarchy. 
        # Apply global defaults for Generation
        for ParamName in sorted(DefaultSystemOptions.keys()):
            # First define the global system defaults
            GenerationOptionsToUse = HandleOption(ParamName, GenerationOptionsToUse, DefaultSystemOptions[ParamName], True)
            # Override with user defined System option Defaults
            if Params.has_key(ParamName):
                DummyExpr=Expr()
                ActualValue=DummyExpr.Evaluate(ExprText = Params[ParamName].Formula)
                if ActualValue != None:
                    # Use User defined defaults
                    GenerationOptionsToUse = HandleOption(ParamName, GenerationOptionsToUse, ActualValue, True)
            # Override with input supplied in function input:
            ExtractedValue = HandleOption(ParamName, GenerationOptions, None)
            if ExtractedValue != None:
                GenerationOptionsToUse = HandleOption(ParamName, GenerationOptionsToUse, ExtractedValue, True)
        # Now Actually extract the values to variables to use in the code
        ValidateDataInRuntime = HandleOption('ValidateDataInRuntime', GenerationOptionsToUse)
        NumberOfErrorsConsideredAsWarningsForPopulationGeneration = HandleOption('NumberOfErrorsConsideredAsWarningsForPopulationGeneration', GenerationOptionsToUse)
        NumberOfTriesToRecalculateIndividualDuringPopulationGeneration = HandleOption('NumberOfTriesToRecalculateIndividualDuringPopulationGeneration', GenerationOptionsToUse)
        #RepairPopulation = HandleOption('RepairPopulation', GenerationOptionsToUse)
        VerboseLevel = HandleOption('VerboseLevel', GenerationOptionsToUse)
        RandomSeed = HandleOption('RandomSeed', GenerationOptionsToUse)
        # Define how many candidates there are per selected individual
        SystemPrecisionForProbabilityBoundCheck = HandleOption('SystemPrecisionForProbabilityBoundCheck', GenerationOptionsToUse)
        GeneticAlgorithmCandidatesPerSelectedIndividual = HandleOption('GeneticAlgorithmCandidatesPerSelectedIndividual', GenerationOptionsToUse)
        GeneticAlgorithmMaxStableGenerationCountTerminator = HandleOption('GeneticAlgorithmMaxStableGenerationCountTerminator', GenerationOptionsToUse)
        GeneticAlgorithmMaxEvalsTerminator = HandleOption('GeneticAlgorithmMaxEvalsTerminator', GenerationOptionsToUse)
        GeneticAlgorithmTournamentSize = HandleOption('GeneticAlgorithmTournamentSize', GenerationOptionsToUse)
        GeneticAlgorithmNumberOfElitesToSurviveIfBetterThanWorstOffspring = HandleOption('GeneticAlgorithmNumberOfElitesToSurviveIfBetterThanWorstOffspring', GenerationOptionsToUse)
        GeneticAlgorithmSolutionPopulationSize = HandleOption('GeneticAlgorithmSolutionPopulationSize', GenerationOptionsToUse)
        GeneticAlgorithmMutationRate = HandleOption('GeneticAlgorithmMutationRate', GenerationOptionsToUse)

       
        # Extract Default file names
        # Extract Default file names, but first create the TimeStamp
        if GenerationFileNamePrefix == None:
            GenerationFileNamePrefix = DefaultGenerationScriptFileNamePrefix
        if OutputFileNamePrefix == None:
            OutputFileNamePrefix = DefaultGenerationOutputFileNamePrefix   
        if RandomStateFileNamePrefix == None:
            RandomStateFileNamePrefix = DefaultRandomStateFileNamePrefix 
        # Determine the filename and path
        (ScriptFileDescriptor, ScriptFileName) = tempfile.mkstemp ( PythonSuffix, GenerationFileNamePrefix , SessionTempDirecory , True)
        (ScriptPathOnly , ScriptFileNameOnly, ScriptFileNameFullPath) = DetermineFileNameAndPath(ScriptFileName)
        # Now actually create the file
        try:
            GenFile = os.fdopen(ScriptFileDescriptor,'w')
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Population Generation Compilation Error: The script file ' + ScriptFileNameFullPath  +' cannot be created. Please make sure you specified a valid path for the file and that that file name is not in use by the system. The error was detected for the Population set ' + self.Name + '. Here are details about the error: ' + str(ExceptValue)
        # Define constants required later on
        Tab = ' '*4
        # Continue with defining the data for the Generation
        WriteGenLine ('################################################################################')
        TitleFileName ='# ' + ScriptFileNameOnly + ' '*(77-len(ScriptFileNameOnly)) + '#'
        WriteGenLine (TitleFileName)                              
        WriteGenLine ('# This generation script was automatically Generated on: '+ datetime.datetime.now().isoformat(' ')[:19] + '   #')
        WriteGenLine ('# by the MIcroSimulation Tool (MIST).                                          #')
        WriteGenLine ('################################################################################')
        WriteGenLine ()
        WriteGenLine ('##################### Imports #####################')
        WriteGenLine ('from __future__ import division')
        WriteGenLine ('import DataDef')
        WriteGenLine ('import sys')
        WriteGenLine ('import os')
        WriteGenLine ('import pickle')
        WriteGenLine ('import tempfile')        
        WriteGenLine ('#### Create Validation Error/Warning Handler ##### ')
        WriteGenLine ('_WarningCount = 0')
        WriteGenLine ('sys.exc_clear()')
        WriteGenLine ('(_EmptyExceptType, _EmptyExceptValue) = sys.exc_info()[:2]')
        WriteGenLine ('def _WarningErrorHandler( _InputErrorString = None, _FatalError = False):')
        WriteGenLine (Tab + 'global _WarningCount')
        WriteGenLine (Tab + '(_ExceptType, _ExceptValue, _ExceptTraceback) = sys.exc_info()')
        WriteGenLine (Tab + 'if _InputErrorString != None:')
        WriteGenLine (Tab + Tab + 'if (_ExceptType, _ExceptValue) == (_EmptyExceptType, _EmptyExceptValue):')
        WriteGenLine (Tab + Tab + Tab + '(_ExceptType, _ExceptValue) = (ValueError, _InputErrorString)')
        WriteGenLine (Tab + Tab + 'else:')
        WriteGenLine (Tab + Tab + Tab + '_ExceptValue = _InputErrorString + " Here are further details: " + str(_ExceptValue)')
        WriteGenLine (Tab + '_WarningCount = _WarningCount + 1')
        WriteGenLine (Tab + 'if _FatalError or (_WarningCount > ' + SmartStr(NumberOfErrorsConsideredAsWarningsForPopulationGeneration) + '):')
        WriteGenLine (Tab + Tab + 'raise _ExceptType, "Generation Runtime Error: " + str(_ExceptValue)')
        WriteGenLine (Tab + 'else:')
        WriteGenLine (Tab + Tab + 'print "Generation Runtime Warning:" + str(_ExceptValue)')
        # Verify version
        WriteGenLine ('_GeneratingVersion = ' + repr(Version) )
        WriteGenLine ('if DataDef.Version != _GeneratingVersion:')
        WriteGenLine (Tab + "_WarningErrorHandler(_InputErrorString = 'The generation was created with a different version than the data definitions used. This may raise incompatibility issues. The generation script was created with version ' + repr(" + repr(Version) + ") + ' while the definition file version is ' + repr(DataDef.Version), _FatalError = True)")
        WriteGenLine ('############## Load the Required Parameters #######')
        ############## Load the Required Parameters #######
        RelatedParamKeys = self.FindDependantParams() 
        RelatedParams = ParamsClass(map (lambda ParamKey: (ParamKey , Params[ParamKey])  , RelatedParamKeys))
        WriteGenLine ('_ParamsInfo = pickle.loads(' + repr(pickle.dumps(RelatedParams)) + ')')
        WriteGenLine ('_PopulationSetInfo = pickle.loads(' + repr(pickle.dumps(self)) + ')')
        WriteGenLine ('_CompileArguments = pickle.loads(' + repr(pickle.dumps((GeneratedPopulationSize, GenerationFileNamePrefix, OutputFileNamePrefix, RandomStateFileNamePrefix, GenerationOptions, SkipDumpingFilesIfError, RecreateFromTraceBack))) + ')')

        WriteGenLine ()
        WriteGenLine ('#### Constants ####')
        WriteGenLine ('Inf = DataDef.Inf')
        WriteGenLine ('NaN = DataDef.NaN')
        WriteGenLine ('inf = DataDef.Inf')
        WriteGenLine ('nan = DataDef.NaN')
        WriteGenLine ('#### Functions Allowed in Expressions ####')
        for FuncName in ExpressionSupportedFunctionsNames:
            WriteGenLine (FuncName + ' = DataDef.' + FuncName)
        for (FuncName, RunTimeFuncName) in RuntimeFunctionNames:
            WriteGenLine (FuncName + ' = DataDef.' + RunTimeFuncName)
        WriteGenLine ('#### Random seed ####')
        VerboseComment = Iif(VerboseLevel >= 6,'','#')
        if not IsNumericType(RandomSeed) or IsNaN(RandomSeed):
            RandomSeed = None
        # If not recreating from TraceBack figure out the random seed and
        # record the random state on file
        if RecreateFromTraceBack == None:
            WriteGenLine ('try:')
            WriteGenLine (Tab + 'DataDef.numpy.random.seed(' + SmartStr(RandomSeed) +  ')')
            WriteGenLine (Tab + '# Record the initial state of the random generator')
            WriteGenLine (Tab + '_InitialRandomState = DataDef.numpy.random.get_state()')
            WriteGenLine (Tab + '_RandomStateFileName = ""')
            WriteGenLine (VerboseComment + Tab + '(_RandomStateFileDescriptor, _RandomStateFileName) = tempfile.mkstemp ( ' + repr(TextSuffix) + ' , os.path.splitext(__file__)[0] + "_" + ' + repr(RandomStateFileNamePrefix) + '+ "_" , ' + repr(SessionTempDirecory) + ', True)')
            WriteGenLine (VerboseComment + Tab + "_OutFile = os.fdopen (_RandomStateFileDescriptor , 'w')")
            WriteGenLine (VerboseComment + Tab + 'pickle.dump(_InitialRandomState , _OutFile)')
            WriteGenLine (VerboseComment + Tab + "_OutFile.close()")
            WriteGenLine ('except:')
            if SkipDumpingFilesIfError:
                WriteGenLine (Tab + "print 'Warning - could not write the Initial Random State to file, writing to screen instead'")
                WriteGenLine (Tab + "print _InitialRandomState")
            else:
                WriteGenLine (Tab + "_WarningErrorHandler()")
        else:
            # If recreating from TraceBack then use the random state stored 
            # in the traceback
            WriteGenLine ('# Reproduce the Random state from given TraceBack information')
            WriteGenLine ('_InitialRandomState = pickle.loads(' + repr(pickle.dumps( RecreateFromTraceBack[2])) + ')')
            # use original see file name rather than None in case it exists
            WriteGenLine ('_RandomStateFileName = pickle.loads(' + repr(pickle.dumps( RecreateFromTraceBack[3])) + ')')
            WriteGenLine ('DataDef.numpy.random.set_state(_InitialRandomState)')
        WriteGenLine ()
        WriteGenLine ('####### Initialize Results Vector #######')
        WriteGenLine ('_CandidatesResultsVector = []')
        WriteGenLine ('_ResultsVector = []')
        WriteGenLine ('_IndividualObjectives = []')
        WriteGenLine ('_ReturnedObjectives = []')
        WriteGenLine ('_ErrorSum = None')
        WriteGenLine ('############### Execute Generation ###############')
        WriteGenLine ('####### Subject Loop #######')
        WriteGenLine ('IndividualID = 0')
        WriteGenLine ('_NumberOfTriesToGenerateThisIndividual = 0')
        # Generate extra population only if a genetic algorithm is defined
        if self.Objectives != []:
            CandidatePopulationSizeBeforeSelection = GeneratedPopulationSize*GeneticAlgorithmCandidatesPerSelectedIndividual
        else:
            CandidatePopulationSizeBeforeSelection = GeneratedPopulationSize
        WriteGenLine ('while IndividualID < '+ str(CandidatePopulationSizeBeforeSelection) + ':')
        WriteGenLine (Tab + '# Reset Warning/Error Count')
        WriteGenLine (Tab + '_WarningCountBeforeThisIndividual = _WarningCount')
        WriteGenLine (Tab + '# Increase the number of Tries counter')
        WriteGenLine (Tab + '_NumberOfTriesToGenerateThisIndividual = _NumberOfTriesToGenerateThisIndividual + 1')
        # At verbose level of 1 or more, display subject repetition information
        WriteGenLine (Tab + '# Comment/Uncomment the next line to disable/enable printing of verbose information')
        WriteGenLine (Tab + Iif(VerboseLevel >= 10,'','#') + 'print "Calculating Individual #" + str(IndividualID+1)')
        # Init all parameters - Reset to None
        ColumnNames = map ( lambda (ColumnName , Distribution): ColumnName , self.DataColumns)
        AllParamsStr = str(ColumnNames).replace("', '",', ')[2:-2]
        RightSideZeroStr = 'None, '*(len(ColumnNames)-1)+ 'None'
        WriteGenLine (Tab + AllParamsStr + ' = ' + RightSideZeroStr)
        # Write the expressions
        ProperColumnProcessingOrder = CalculateProperColumnOrderForGeneration()
        for ColumnIndex in ProperColumnProcessingOrder:
            (ColumnName , Distribution) = self.DataColumns[ColumnIndex]
            WriteGenLine (Tab + '# Processing the Destination Parameter: ' + ColumnName )
            SourceExpr=Expr(Distribution)
            # Create the expression code
            SourceExpr.WriteCodeForExpression (AssignedParameterName = ColumnName, SourceExprText = None, ValidateDataInRuntime = ValidateDataInRuntime, WriteLnFunction = WriteGenLine, Lead = Tab, Tab = Tab, TempTokenPrefix = '_Temp', OverrideLastCheck = None)
        # Check that no errors were generated before this individual. 
        # If none happened then it is ok to keep this data. otherwise
        # repeat the loop without increasing the individual count
        WriteGenLine (Tab + 'if _WarningCount <= _WarningCountBeforeThisIndividual:')
        # Expand the expression and write it down. It is assumed that the
        # expression was validated and the expanded version exists
        WriteGenLine (Tab + Tab + '# update the results vector')
        WriteGenLine (Tab + Tab + '_CandidatesResultsVector.append([' + AllParamsStr +'])')
        # Increase indvidual count
        WriteGenLine (Tab + Tab + 'IndividualID = IndividualID + 1')
        WriteGenLine (Tab + Tab + '_NumberOfTriesToGenerateThisIndividual = 0')
        WriteGenLine (Tab + 'elif _NumberOfTriesToGenerateThisIndividual >= ' + SmartStr(NumberOfTriesToRecalculateIndividualDuringPopulationGeneration) + ':')
        # Handle the case where the program should raise a fatal error due to
        # too many tries to process the same person
        WriteGenLine (Tab + Tab + '_WarningErrorHandler(_InputErrorString = "The generation was halted since the number of tries to recalculate the same person has been exceeded. If this problem consistently repeats itself, check the formulas to see if these cause too many out of bounds numbers to be generated. Alternatively, try raising the system option NumberOfTriesToRecalculateIndividualDuringPopulationGeneration which is now defined as ' + SmartStr(NumberOfTriesToRecalculateIndividualDuringPopulationGeneration) + '  .  ", _FatalError = True)')
        WriteGenLine (Tab + 'else:')
        # Handle the case where the error was not fatal, yet we do not want to
        # proceed to calculate objectives - we want to go on to calculate the
        # next person in the loop instead
        WriteGenLine (Tab + Tab + 'continue')
        WriteGenLine ('')

        if self.Objectives!=[]:
            # For each Objective, calculate the Filter and Statistics for this 
            # individual and store it for future use
            WriteGenLine (Tab + '# Calculate Objectives Filter and Statistics')
            WriteGenLine (Tab + '_ObjectivesForThisIndividual = []')
            for Objective in self.Objectives:
                WriteGenLine (Tab + '# Processing the objective: ' +str(Objective))
                (FilterExpr, StatExpr, StatFunction, TargetValue, Weight, CalcValue, CalcError) = Objective
                LastValidityCheckCode = 'if not (' + repr(-SystemPrecisionForProbabilityBoundCheck) + ' <= _Temp  <= ' + repr(1.0+SystemPrecisionForProbabilityBoundCheck) + '):'
                ErrorHandlerCode = Tab + '_WarningErrorHandler(_InputErrorString = "The filter probability threshold defined by an objective does not evaluate to a number between 0 and 1 within a tolerance specified by the system option parameter SystemPrecisionForProbabilityBoundCheck. The objective filter evaluated to: " + str(_Temp) + " for the Objective: " + ' + repr(Objective) + ', _FatalError = True)'
                SourceExpr=Expr(FilterExpr)
                SourceExpr.WriteCodeForExpression (AssignedParameterName = '_FilterExprValue', SourceExprText = None, ValidateDataInRuntime = ValidateDataInRuntime, WriteLnFunction = WriteGenLine, Lead = Tab , Tab = Tab, TempTokenPrefix = '_Temp', OverrideLastCheck = [LastValidityCheckCode, ErrorHandlerCode])
                LastValidityCheckCode = 'if not (DataDef.IsFinite(_Temp)):'
                ErrorHandlerCode = Tab + '_WarningErrorHandler(_InputErrorString = "The filter expression defined by an objective does not evaluate to a number, the objective expression evaluated to: " + str(_Temp) + " for the Objective: " + ' + repr(Objective) + ', _FatalError = True)'
                SourceExpr=Expr(StatExpr)
                SourceExpr.WriteCodeForExpression (AssignedParameterName = '_StatExprValue', SourceExprText = None, ValidateDataInRuntime = ValidateDataInRuntime, WriteLnFunction = WriteGenLine, Lead = Tab, Tab = Tab, TempTokenPrefix = '_Temp', OverrideLastCheck = [LastValidityCheckCode, ErrorHandlerCode])
                WriteGenLine (Tab + '# Processing the objective: ' +str(Objective))
                WriteGenLine (Tab + '_ObjectivesForThisIndividual.append((_FilterExprValue, _StatExprValue))')
            WriteGenLine (Tab + '# Collect the calculated objectives information for this individual')
            WriteGenLine (Tab + '_IndividualObjectives.append(_ObjectivesForThisIndividual)')

        if self.Objectives==[]:
            WriteGenLine ('# No Optimization by Genetic Algorithm Defined by Objectives - result is final')
            WriteGenLine ('_ResultsVector = _CandidatesResultsVector')
        else:
            # Define the fitness function
            WriteGenLine ('# The Evolutionary code below is inspired by code initially ' )
            WriteGenLine ('# written as an example by Aaron Lee Garrett who maintains Inspyred ' )
            WriteGenLine ('# Aaron did not ask to maintain any ownership fo the code - he was ' )
            WriteGenLine ('# just trying to help use Inspyerd to solve this. Never the less ' )
            WriteGenLine ('# his help was far and beyond what is normally given as support ' )
            WriteGenLine ('# therefore he is acknowledged in this code. His contribution saved ' )
            WriteGenLine ('# many hours of learning a new library. ' )
            WriteGenLine ('')
   
            WriteGenLine ('def _CandidateGroupEvaluate(_CandidateGroup):')
            WriteGenLine (Tab + '"Define candidate fitness score calculator"')
            WriteGenLine (Tab + '_CandidateGroupInformation = [_IndividualObjectives[_IndividualIndex] for _IndividualIndex in _CandidateGroup]')
            # Transpose the results to handle them properly
            if GeneratedPopulationSize == 1:
                # Handle the extreme end case where we ask for only a single 
                # individual. This case is not handled well by the transpose 
                # command and a dimetion is lost - therefore it is 
                # handeled here seperatly. Note, however, that 
                WriteGenLine (Tab + '_CandidateGroupInformationTransposed = [[_Entry] for _Entry in _CandidateGroupInformation[0]]')
            else:
                # when there are multiple individuals use regular transpose
                WriteGenLine (Tab + '_CandidateGroupInformationTransposed = map(None,*_CandidateGroupInformation)')
                
            WriteGenLine (Tab + '_StatisticsVector = []')
            WriteGenLine (Tab + '_ErrortVector = []')
            WriteGenLine (Tab + '_ErrorSum = 0')
    
            for (ObjectiveEnum,Objective) in enumerate(self.Objectives):
                (FilterExpr, StatExpr, StatFunction, TargetValue, Weight, CalcValue, CalcError) = Objective
                WriteGenLine (Tab + '# Processing the objective: ' +str(Objective))            
                WriteGenLine (Tab + '_StatsVector = [_StatExprValue for (_FilterExprValue, _StatExprValue) in _CandidateGroupInformationTransposed['+str(ObjectiveEnum)+'] if _FilterExprValue]')
                WriteGenLine (Tab + 'if _StatsVector == []:')
                WriteGenLine (Tab + Tab + '_StatisticForThisObjective = Inf')
                WriteGenLine (Tab + Tab + '_WarningErrorHandler(_InputErrorString = "There were no records found that satisfy the filter expression ' + repr(FilterExpr) + ' , check if population size is sufficient to produce any records for this objective", _FatalError = False)')
                WriteGenLine (Tab + 'else:')                
                if StatFunction == 'MEAN':
                    WriteGenLine (Tab + Tab + '_StatisticForThisObjective = DataDef.numpy.mean (_StatsVector)')
                elif StatFunction == 'STD':
                    # Use ddof = 1 when calculaing std
                    WriteGenLine (Tab + Tab + '_StatisticForThisObjective = DataDef.numpy.std(_StatsVector, None, None, None, 1)')
                elif StatFunction == 'MEDIAN':
                    WriteGenLine (Tab + Tab + '_StatisticForThisObjective = DataDef.numpy.median(_StatsVector)')
                elif StatFunction.startswith('PERCENT'):                    
                    # The last two digits defien the range
                    WriteGenLine (Tab + Tab + '_StatisticForThisObjective = DataDef.scipy.stats.scoreatpercentile(_StatsVector,'+StatFunction[-2:] + ' )')
                elif StatFunction == 'MIN':
                    WriteGenLine (Tab + Tab + '_StatisticForThisObjective = min(_StatsVector)')
                elif StatFunction == 'MAX':
                    WriteGenLine (Tab + Tab + '_StatisticForThisObjective = max(_StatsVector)')
                elif StatFunction == 'SUM':
                    WriteGenLine (Tab + Tab + '_StatisticForThisObjective = sum(_StatsVector)')
                elif StatFunction == 'COUNT':
                    WriteGenLine (Tab + Tab + '_StatisticForThisObjective = len(_StatsVector)')
                else:
                    raise ValueError, 'ASSERTION ERROR: Unknown StatFunction type - this should be caught during data entry'
                WriteGenLine (Tab + '_ErrorElement = ((_StatisticForThisObjective - ' + SmartStr(TargetValue) + ') * ' + SmartStr(Weight) + ')**2 ')
                WriteGenLine (Tab + '_ErrortVector.append(_ErrorElement)')
                WriteGenLine (Tab + '_ErrorSum = _ErrorSum + _ErrorElement')
                WriteGenLine (Tab + '_StatisticsVector.append(_StatisticForThisObjective)')
            WriteGenLine (Tab + 'return (_ErrorSum,_StatisticsVector,_ErrortVector)')
    
            WriteGenLine ('')
            WriteGenLine ('# Defining the Genetic Algorithm')
            WriteGenLine ('class _NumpyRandomWrapper(DataDef.numpy.random.RandomState):')
            WriteGenLine (Tab + 'def __init__(self, _seed=None):')
            WriteGenLine (Tab + Tab + 'super(_NumpyRandomWrapper, self).__init__(_seed)')
            WriteGenLine (Tab + 'def sample(self, _Population, _K):')
            WriteGenLine (Tab + Tab + 'return self.choice(_Population, _K, replace=False)')
            WriteGenLine (Tab + 'def random(self):')
            WriteGenLine (Tab + Tab + 'return self.random_sample()')
            WriteGenLine ('')
            WriteGenLine ('# Define a set of candidate indices before entering the mutator' )
            WriteGenLine ('_FullPopulationIndexList = list(range('+str(CandidatePopulationSizeBeforeSelection)+'))' )
            WriteGenLine ('_FullPopulationIndexSet = set(_FullPopulationIndexList)' )
                
            WriteGenLine ('')
            WriteGenLine ('def _Generator(random, args):')
            WriteGenLine (Tab + '"Generate a random candidate represented as a list of unique index values."')
            WriteGenLine (Tab + '_RandomCandidate = list(random.sample(_FullPopulationIndexList, ' + str(GeneratedPopulationSize) + '))')
            WriteGenLine (Tab + 'return _RandomCandidate')
            WriteGenLine ('')
            WriteGenLine ('@DataDef.inspyred.ec.evaluators.evaluator')
            WriteGenLine ('def _Evaluator(_Candidate, args):')
            WriteGenLine (Tab + '"Evaluate a candidate group - Inspyred wrapper for the Evaluation function"')
            WriteGenLine (Tab + '(_ErrorSum,_StatisticsVector,_ErrortVector) = _CandidateGroupEvaluate(_Candidate)')
            WriteGenLine (Tab + 'return _ErrorSum')
            WriteGenLine ('')
            WriteGenLine ('@DataDef.inspyred.ec.variators.crossover')
            WriteGenLine ('def _Crossover(random, _Mom, _Dad, args):')
            WriteGenLine (Tab + '"Crossover two candidates by randomly reassigning non duplicates"')
            WriteGenLine (Tab + '_DadSet = set(_Dad)')
            WriteGenLine (Tab + '_MomSet = set(_Mom)')
            WriteGenLine (Tab + '_Duplicates = list(_DadSet.intersection(_MomSet))')
            WriteGenLine (Tab + '_DifferentElements = list(_DadSet.symmetric_difference(_MomSet))')
            WriteGenLine (Tab + '_DifferentElementsRandomOrder = list(random.permutation(_DifferentElements))')
            WriteGenLine (Tab + '_OutBrother = _Duplicates + _DifferentElementsRandomOrder [:((len(_DadSet)-len(_Duplicates)))]')
            WriteGenLine (Tab + '_OutSister = _Duplicates + _DifferentElementsRandomOrder [-((len(_MomSet)-len(_Duplicates))):]')
            WriteGenLine (Tab + 'return [_OutBrother, _OutSister]')
            WriteGenLine ('')

            WriteGenLine ('@DataDef.inspyred.ec.variators.mutator')
            WriteGenLine ('def _Mutator(random, candidate, args):')
            WriteGenLine (Tab + '"Mutate a candidate. randomly select a legal index at the mutation rate"')
            WriteGenLine (Tab + '_MutationRate = args["mutation_rate"]')
            WriteGenLine (Tab + '_MutationIndices=[]')
            WriteGenLine (Tab + '_Mutant = candidate[:]')
            WriteGenLine (Tab + '_LegalValuesOutOfMutant = list(_FullPopulationIndexSet - set(_Mutant))')
            WriteGenLine (Tab + 'for (_MutantIndex,_MutantValue) in enumerate(_Mutant):')
            WriteGenLine (Tab + Tab + 'if random.random() <= _MutationRate:')
            WriteGenLine (Tab + Tab + Tab + '_MutationIndices.append(_MutantIndex)')
            WriteGenLine (Tab + Tab + Tab + '_LegalValuesOutOfMutant.append(_MutantValue)')
            WriteGenLine (Tab + '# Sample legal values - there is a small possiblilty of no mutation by self replacement')
            WriteGenLine (Tab + '_MutationValues = random.sample(_LegalValuesOutOfMutant,len(_MutationIndices))')
            WriteGenLine (Tab + 'for (_MutantEnum, _MutationIndex) in enumerate(_MutationIndices):')
            WriteGenLine (Tab + Tab + '_Mutant[_MutationIndex] = _MutationValues[_MutantEnum]')
            WriteGenLine (Tab + 'return _Mutant')
            WriteGenLine ('')

            WriteGenLine ('def _BestSolutionStableTermination(population, num_generations, num_evaluations, args):')
            WriteGenLine (Tab + '"Return True if the best fitness does not change for a number of generations."')
            WriteGenLine (Tab + '_StableGenerationCount = args["GeneticAlgorithmMaxStableGenerationCountTerminator"]')
            WriteGenLine (Tab + '(_PrevBestFitness, _PrevBestGeneration) = args.setdefault("BestFitnessInfo", (DataDef.Inf,0))')
            WriteGenLine (Tab + '_CurrentBestFitness = max(population).fitness')
            WriteGenLine (Tab + 'if _CurrentBestFitness < _PrevBestFitness:')
            WriteGenLine (Tab + Tab + 'args["BestFitnessInfo"] = (_CurrentBestFitness, num_generations)')
            WriteGenLine (Tab + Tab + '_RetValue = False')
            WriteGenLine (Tab + 'else:')
            WriteGenLine (Tab + Tab + '_RetValue = (num_generations - _PrevBestGeneration ) >= _StableGenerationCount')
            WriteGenLine (Tab + 'return _RetValue')
            WriteGenLine ('')

            WriteGenLine ('# Prepare for launching the genetic algorithm')
            WriteGenLine ('_RandomStateBeforeGeneticAlgorithm = DataDef.numpy.random.get_state()')
            WriteGenLine ('_RandomGeneratorInstance = _NumpyRandomWrapper()')
            WriteGenLine ('_RandomGeneratorInstance.set_state(_RandomStateBeforeGeneticAlgorithm)')
            WriteGenLine ('_GeneticAlgorithmInstance = DataDef.inspyred.ec.EvolutionaryComputation(_RandomGeneratorInstance)')
            WriteGenLine ('_GeneticAlgorithmInstance.variator = [_Crossover, _Mutator]')
            WriteGenLine ('_GeneticAlgorithmInstance.replacer = DataDef.inspyred.ec.replacers.generational_replacement')
            WriteGenLine ('_GeneticAlgorithmInstance.terminator = [ DataDef.inspyred.ec.terminators.evaluation_termination, _BestSolutionStableTermination]')
            WriteGenLine ('_GeneticAlgorithmInstance.observer = DataDef.inspyred.ec.observers.stats_observer')
            WriteGenLine ('_FinalGeneration = _GeneticAlgorithmInstance.evolve(generator = _Generator, evaluator = _Evaluator, pop_size = ' + str(GeneticAlgorithmSolutionPopulationSize) + ' , bounder = DataDef.inspyred.ec.DiscreteBounder(_FullPopulationIndexList) , maximize=False, tournament_size = ' +str(GeneticAlgorithmTournamentSize) + ' ,  num_selected= ' + str(GeneticAlgorithmCandidatesPerSelectedIndividual) + ' , num_elites = ' + str(GeneticAlgorithmNumberOfElitesToSurviveIfBetterThanWorstOffspring) + ' , max_evaluations = ' + str(GeneticAlgorithmMaxEvalsTerminator) + ', mutation_rate = ' + str (GeneticAlgorithmMutationRate) +', GeneticAlgorithmMaxStableGenerationCountTerminator = ' +str(GeneticAlgorithmMaxStableGenerationCountTerminator) + ' )')
            WriteGenLine ('_BestCandidateFound = max(_FinalGeneration)')
            WriteGenLine ('_BestCandidateFound.candidate.sort()')
            WriteGenLine ('(_ErrorSum,_StatisticsVector,_ErrortVector) = _CandidateGroupEvaluate(_BestCandidateFound.candidate)')
            WriteGenLine ('# Define final results vector by looping over best solution indices')
            WriteGenLine ('_ResultsVector = [_CandidatesResultsVector[_IndividualIndex] for _IndividualIndex in _BestCandidateFound.candidate]')
            WriteGenLine ('')

            # write the result to file
            WriteGenLine ('# Comment/Uncomment the next lines to disable/enable dumping objective statistics')
            VerboseComment = Iif(VerboseLevel >= 5,'','#')
            WriteGenLine (VerboseComment + 'print "Final Statistics Per Objective Using the Following Format:"')
            WriteGenLine (VerboseComment + 'print "Calculated Statistic $ Target Value $ Error from target $ Weight $ Statistics Expression $ Statistics function $ Filter Expression:" ')
            for ObjectiveEnum, Objective in enumerate(self.Objectives):
                (FilterExpr, StatExpr, StatFunction, TargetValue, Weight, CalcValue, CalcError) = Objective
                WriteGenLine (VerboseComment + 'print ( DataDef.SmartStr(_StatisticsVector['+ str(ObjectiveEnum) +']) + " $ ' + SmartStr(TargetValue) + ' $ " + DataDef.SmartStr(_ErrortVector['+ str(ObjectiveEnum) +']) + " $ ' + SmartStr(Weight) + '  $ ' + repr(StatExpr) + ' $ ' + repr(StatFunction) + ' $ ' + repr(FilterExpr)+ '" ) ')
            WriteGenLine (VerboseComment + 'print "Final Weighted Error Sum Was:" + DataDef.SmartStr(_ErrorSum)')
            # Provide a warning for a single individual with objectives
            if GeneratedPopulationSize == 1:
                WriteGenLine (VerboseComment + 'print "WARNING: Note that you are generating a population of size 1 with objectives - typically objectives are defined for multiple individuals"')

            WriteGenLine ('# update the objectives vector for output')
            WriteGenLine ('for (_ObjectiveEnum,_Objective) in enumerate(_PopulationSetInfo.Objectives):')
            WriteGenLine (Tab +'(_FilterExpr, _StatExpr, _StatFunction, _TargetValue, _Weight, _CalcValue, _CalcError) = _Objective')
            WriteGenLine (Tab +'_CalcValue = _StatisticsVector[_ObjectiveEnum]')
            WriteGenLine (Tab +'_CalcError = _ErrortVector[_ObjectiveEnum]')
            WriteGenLine (Tab +'_ReturnedObjectives.append((_FilterExpr, _StatExpr, _StatFunction, _TargetValue, _Weight, _CalcValue, _CalcError))')

        # write the result to file
        WriteGenLine ('# Comment/Uncomment the next lines to disable/enable dumping output file')
        VerboseComment = Iif(VerboseLevel >= 7,'','#')
        WriteGenLine (VerboseComment +'try:')
        WriteGenLine (VerboseComment + Tab + "# Output the results to a file")
        WriteGenLine (VerboseComment + Tab + '(_OutputFileDescriptor, _OutputFileName) = tempfile.mkstemp ( ' + repr(TextSuffix) + ' , ' + repr(OutputFileNamePrefix) + ' , ' + repr(SessionTempDirecory) + ', True)')
        WriteGenLine (VerboseComment + Tab + "_OutFile = os.fdopen (_OutputFileDescriptor , 'w')")
        WriteGenLine (VerboseComment + Tab + 'pickle.dump(_ResultsVector, _OutFile)')
        WriteGenLine (VerboseComment + Tab + "_OutFile.close()")
        WriteGenLine (VerboseComment + 'except:')
        if SkipDumpingFilesIfError:
            WriteGenLine (VerboseComment + Tab + "print 'Warning - could not write results to file'")
        else:
            WriteGenLine (VerboseComment + Tab + "_WarningErrorHandler()")
        # Figure out column names
        NewDataColumns = map( lambda (ParamName,DistributionParam): (ParamName,'') , self.DataColumns)
        WriteGenLine ('# Return PopulationSet parameters. These are: (ID of source population set, column name definitions, results array)')
        WriteGenLine ("_ResultPopulationSetData = ("+ str(self.ID)+' , _GeneratingVersion , _InitialRandomState , os.path.split(_RandomStateFileName)[1] , os.path.split(__file__)[1] , _CompileArguments , ' + repr(NewDataColumns) + ", _ReturnedObjectives, _ErrorSum , _ResultsVector )")
        WriteGenLine ('# Comment/Uncomment the next line to disable/enable printing of verbose information')
        WriteGenLine (Iif(VerboseLevel >= 10,'','#') + "print 'Info: population set generation was successful. A total number of ' + str(_WarningCount) + ' warnings were raised.'")
        try:
            GenFile.close()
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Generation Compilation Error: Error encountered while closing simulation script file ' + ScriptFileNameFullPath  +'. Please make sure that the file was not locked by the system due to quota or other reasons. The error was detected for the population set ' + self.Name + '. Here are details about the error: ' + str(ExceptValue)
        return ScriptFileNameFullPath

    def RunPopulationGenerationSpawned (self, GenerationFileName, OutputConnection = None, DeleteScriptFileAfterRun = True):
        """ Runs the generation """
        # Determine the file names
        (ScriptPathOnly, ScriptFileNameOnly, ScriptFileNameFullPath) = DetermineFileNameAndPath(GenerationFileName)
        (ScriptFileNameNoExtension , ScriptFileNameOnlyExtension ) = os.path.splitext(ScriptFileNameOnly)
        if ScriptFileNameOnlyExtension.lower() not in ['.py', 'py']:
            raise ValueError, 'Generation Execution Error: The generation file name ' + ScriptFileNameFullPath + ' does not have a python extension of "py"'
        # Make sure the module is in the system path. First save the current
        # system path and then change it
        OldSysPath = sys.path
        # Insert the new path at the beginning of the search list so that
        # the correct file will be run in case of duplicate filenames in
        # different directories.
        sys.path.insert(0,ScriptPathOnly)
        # Now try running the generation - enclose this in a try catch clause
        try:
            RunGeneration = None
            # Run the Generation
            RunGeneration = __import__(ScriptFileNameNoExtension)
            # In the past the data was reloaded. However this may cause waste
            # of time (running the same code twice) and therefore commented out
            # reload (RunGeneration)
            # Collect the results into results dictionary
            ReturnedPopulationSetData = RunGeneration._ResultPopulationSetData
            # remove the module from sys.modules to force reload later on
            del(sys.modules[ScriptFileNameNoExtension])
            if DeleteScriptFileAfterRun:
                # in case of an error before here- the file will not be 
                # deleted, so it would be possible to debug 
                try:
                    os.remove(ScriptFileNameFullPath)
                    os.remove(ScriptFileNameFullPath+'c')
                except:
                    # ignore delete error if happens - the file will be left
                    # in the temp dir - no harm donw
                    pass                
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            if ScriptFileNameNoExtension in sys.modules:
                del(sys.modules[ScriptFileNameNoExtension])
            ErrorText = 'Generation Execution Error: An error was encountered while running the generation script file ' + ScriptFileNameFullPath + ' . Here are details about the error: ' + str(ExceptValue)
            # If a connection pipe was provided, use it to report the error
            if OutputConnection != None:
                OutputConnection.send(ErrorText)
                ReturnedPopulationSetData = ErrorText
            else:
                #if no connection was provided, report the error
                raise ValueError, ErrorText
        # Reconstruct the system path
        sys.path = OldSysPath
        # If a connection pipe was provided, use it to report the error
        if OutputConnection != None:
            OutputConnection.send(ReturnedPopulationSetData)
        return ReturnedPopulationSetData 

    def RunPopulationGeneration (self, GenerationFileName, NumberOfProcessesToRun = 0, OutputConnection = None, DeleteScriptFileAfterRun = True):
        """ Runs the Generation if possible/requested as a different process """
        # if NumberOfProcessesToRun = 0, this means run the generation 
        # without opening a new process, i.e. within this process.
        # if NumberOfProcessesToRun is a positive number, then run this 
        # exact number of processes.
        # if the number is negative, then run this -number of simulations
        # in parallel as processes if the system supports multiple processes
        # otherwise, run them serially without opening a new process. 
        # The return value of the function will be the following tuple 
        # (ProcessList, PipeList). ProcessList is empty if no processes were
        # created. PipeList contains a list of pipe or pipe like objects that 
        # contain the simulation results. The caller is responsible to 
        # call CollectGenerationResults on their own to collect the results.
        if SystemSupportsProcesses and NumberOfProcessesToRun > 0:
            raise ValueError, 'ASSERTION ERROR: The system does not support multiprocess in python, yet multiple processes were forced in input parameters to RunSimulation'
        if NumberOfProcessesToRun == 0:
            ProcessEnums = [0]
        else:
            ProcessEnums = range(abs(NumberOfProcessesToRun))
        PipeList = []
        ProcessList = []
        if NumberOfProcessesToRun == 0 or (not SystemSupportsProcesses and NumberOfProcessesToRun <0):
            # Handle the serial executions case 
            for ProcessEnum in ProcessEnums:
                OutputConnection = PipeMock()
                if 'MultiProcess' in DebugPrints:
                    print 'running the file ' + GenerationFileName
                self.RunPopulationGenerationSpawned (GenerationFileName, OutputConnection, DeleteScriptFileAfterRun)
                if 'MultiProcess' in DebugPrints:
                    print 'finished running the file ' + GenerationFileName
                # store the result, errors will be handled later
                PipeList = PipeList + [OutputConnection]
        else:
            # Handle the parallel process execution case
            for ProcessEnum in ProcessEnums:
                # create connections
                (ParentConnenction, ChildConnection) = multiprocessing.Pipe()
                PipeList = PipeList + [ParentConnenction]
                # create processes
                if 'MultiProcess' in DebugPrints:
                    print 'spawning a process for file ' + GenerationFileName
                TheProcess = multiprocessing.Process(target = self.RunPopulationGenerationSpawned, args = (GenerationFileName, ChildConnection, DeleteScriptFileAfterRun))
                ProcessList = ProcessList + [TheProcess]
                if 'MultiProcess' in DebugPrints:
                    print 'process spawned'
                # Now actually start running the process
                TheProcess.start()
        # return the Process and pipe list to be collected by CollectResults
        return (ProcessList, PipeList)

    def CollectResults(self,ProcessList,ConnectionList): 
        """Collects results from RunPopulationGeneration spawned simulations"""
        # If only one generation was run, return the results vector. Otherwise,
        # in case of multiple simulations, return a list with one entry for
        # each result. An error text will be returned in case of an error in 
        # the position corresponding to an unsuccesful run. Also in case of
        # an error in simulation, this error will be raised. Where multiple
        # errors will be reported together in one error message.
        ResultsInfoList = []
        NumberOfResults = len(ConnectionList)
        ProcessEnums = range(NumberOfResults)
        # first collect all data from all processes. This will make the system
        # wait for all processes to finish 
        for ProcessEnum in ProcessEnums:
            ResultsInfo = ConnectionList[ProcessEnum].recv()
            ResultsInfoList = ResultsInfoList + [ResultsInfo]
        # Now if these results are from actual processes, then join them
        if ProcessList != []:
            for ProcessEnum in ProcessEnums:
                ProcessList[ProcessEnum].join()
        # Check if there were any errors
        FullErrorString = ''
        RetValArray=[]
        for ProcessEnum in ProcessEnums:
            ResultsInfo = ResultsInfoList[ProcessEnum]
            if IsStr(ResultsInfo):
                # if an error was detected, report it
                FullErrorString = FullErrorString + 'Generation Execution Error in Process #' + str(ProcessEnum+1) + ' from ' + str(NumberOfResults) + ' : ' + ResultsInfo + '\n'
            else:
                # if no error was detected, then try to store the results
                try:
                    # Actually create a population set from this data
                    # Note that position 0 in the tuple holds the original
                    # population ID, position 1 in the tuple holds column names
                    # and position 2 in the tuple holds the data
                    DerivedFrom, GeneratingVersion, InitialRandomState , RandomStateFileName , TemporaryScriptFile, CompileArguments, DataColumns, ReturnedObjectives, ErrorSum,  Data = ResultsInfo
                    NewNotes = 'Automatically generated from distributions'
                    if (ErrorSum != None):
                        NewNotes = NewNotes + ' with the objective error sum of: ' + SmartStr(ErrorSum)
                    NewNotes = NewNotes + ' . The original population set had the following notes: ' + str(PopulationSets[DerivedFrom].Notes)
                    # Create the population set and use ReturnedObjectives
                    ReturnedPopulationSet = PopulationSet(ID = 0, Name = 'Randomly Generated Data', Source = 'Automatically generated from distributions' , Notes = NewNotes , DerivedFrom = DerivedFrom, DataColumns = DataColumns, Data = Data, Objectives = ReturnedObjectives)
                    # Add TraceBack information to the results
                    ReturnedPopulationSet.TraceBack = (DerivedFrom, GeneratingVersion, InitialRandomState , RandomStateFileName , TemporaryScriptFile, CompileArguments)
                    # Since a record is added rather than modified,
                    # there is no need to specify a bypass project ID
                    RetValArray = RetValArray + [PopulationSets.AddNew(ReturnedPopulationSet)]
                except:
                    (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                    FullErrorString = FullErrorString + 'Generation Result Collection Error in Process #' + str(ProcessEnum+1) + ' from ' + str(NumberOfResults) + ' : Could not store results. Here are additional details about the error: ' + str(ExceptValue) + '\n'
                    RetValArray = RetValArray + [FullErrorString]
        if FullErrorString != '':
            # if there were any errors, raise them
            raise ValueError, FullErrorString
        # if there is only one result set strip the list
        if NumberOfResults == 1:
            RetVal = RetValArray[0]
        else:
            RetVal = RetValArray
        return RetVal

    def RunGenerationAndCollectResults(self, GenerationFileName, NumberOfProcessesToRun = 0, OutputConnection = None, DeleteScriptFileAfterRun = True):
        """ Runs the simulation and collects the results and returns them """
        # this function combines RunPopulationGeneration and CollectResults
        (ProcessList, PipeList) = self.RunPopulationGeneration (GenerationFileName, NumberOfProcessesToRun, OutputConnection, DeleteScriptFileAfterRun)
        RetVal = self.CollectResults(ProcessList, PipeList)
        return RetVal

    def CheckDependencies(self, CheckForModify = False, ProjectBypassID = 0):
        """ Verifies no dependant data exists """
        # CheckForModify is true if checking only for modification.
        # if ProjectBypassID is not zero, then that project will not block
        # modification, unless it is locked. However, a Project bypass should
        # still block deletion of population sets. Therefore consider the
        # ProjectBypass void if CheckForModify and CheckForTransition are both
        # not set. 
        if not CheckForModify:
            ProjectBypassID = 0        
        # If the population set is locked, modification and  deletion is blocked
        LockingList = self.IsLocked()
        if LockingList!=[]:
            raise ValueError, 'The population set cannot be deleted or modified as it is locked by a project using it. To allow modification, unlock all locked projects that use this Population set - this can be done by deletion of simulation results or deletion of the estimation generated simulation project. Locking projects are: ' + EntityNameByID(LockingList,None)
        # For Population sets, projects using the Population set ID can block
        # deletion or modification.
        DependancyErrorCheck(self, Projects, lambda (EntryKey,Entry): Entry.PrimaryPopulationSetID==self.ID and Entry.ID != ProjectBypassID, 'Population Set Dependency Error: The population set '  + self.Name + ' cannot be deleted or modified as there is at least one project using it. To allow modification, delete/modify all of the following projects: ')
        # A population set that was derived from another population set
        # cannot block deletion and modification as this will be handled
        # during deletion by removing the reference.
        return

    def IsLocked(self):
        """ Checks if the population set is locked """
        # A population set is locked if it is used by a locked project
        LockedSimulationProjectCandidates = sorted(filter(lambda Entry: (Entry.PrimaryPopulationSetID==self.ID), Projects.values()))
        InLockedSimulationProject = reduce (lambda Accumulator, Entry: Accumulator + Entry.IsLocked(),LockedSimulationProjectCandidates,[])
        Result = InLockedSimulationProject
        return Result

    def IsParamDependant(self, ParamName):
        """ Returns True if dependant on ParamName """
        Result = ParamName in self.FindDependantParams(ParamType = None)
        return Result

    def FindDependantParams(self, ParamType = None):
        """ Find the dependant parameters """
        # Create a Dummy empty Expression
        DummyExpr = Expr('')
        # Check all data columns names and distributions
        Result = map(lambda (ColumnName , Distribution) : ColumnName, self.DataColumns) 
        Result = Result + reduce(SumOp,map(lambda (ColumnName , Distribution) : DummyExpr.FindDependantParams(ExprText = Distribution), self.DataColumns), [])
        Result = Result + reduce(SumOp,map(lambda (FilterExpr, StatExpr, StatFunction, TargetValue, Weight, CalcValue, CalcError) : DummyExpr.FindDependantParams(ExprText = FilterExpr), self.Objectives), [])
        Result = Result + reduce(SumOp,map(lambda (FilterExpr, StatExpr, StatFunction, TargetValue, Weight, CalcValue, CalcError) : DummyExpr.FindDependantParams(ExprText = StatExpr), self.Objectives), [])
        # If a datatype is specified filter the results by the data type
        if ParamType != None:
            Result = filter(lambda Entry: Params[Entry].ParameterType == ParamType, Result)
        return Result


    def GenerateReport(self, FormatOptions = None):
        """ Generate the report for this entity instance """
        TotalIndent = HandleOption('TotalIndent', FormatOptions,'')
        #IndentAtom = HandleOption('IndentAtom', FormatOptions,'  ')
        ColumnSpacing = HandleOption('ColumnSpacing', FormatOptions,' | ')
        FieldHeader = HandleOption('FieldHeader', FormatOptions,True)
        LineDelimiter = HandleOption('LineDelimiter', FormatOptions,'\n')
        SectionSeparator = HandleOption('SectionSeparator', FormatOptions,70*'_')
        ShowHidden = HandleOption('ShowHidden', FormatOptions,False)
        ReportString = ''
        if ShowHidden:
            ReportString = ReportString + TotalIndent + FieldHeader * 'ID: ' + str(self.ID) + LineDelimiter
            ReportString = ReportString + TotalIndent + FieldHeader * 'Visual TraceBack: ' + str(self.TraceBack) + LineDelimiter
            ReportString = ReportString + TotalIndent + FieldHeader * 'Pickled TraceBack: ' + pickle.dumps(self.TraceBack) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Name: ' + str(self.Name) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Notes: ' + str(self.Notes).replace('\n','\n'+TotalIndent) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Created On: ' + str(self.CreatedOn) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Last Modified: ' + str(self.LastModified) + LineDelimiter
        if ShowHidden:
            ReportString = ReportString + TotalIndent + FieldHeader * 'Derived From ID: ' + str(self.DerivedFrom) + LineDelimiter
        if self.DerivedFrom != 0:
            DerivedPopulationSetName = PopulationSets[self.DerivedFrom].Name
            ReportString = ReportString + TotalIndent + FieldHeader * 'Derived From: ' + str(DerivedPopulationSetName) + LineDelimiter
        if self.IsDistributionBased():
            # This means the population id defined by Distribution:
            ReportString = ReportString + TotalIndent + 'The population is based on the following distributions:' + LineDelimiter
            for (ParamName,Distribution) in self.DataColumns:
                ReportString = ReportString + LineDelimiter
                ReportString = ReportString + TotalIndent + FieldHeader * 'Parameter: ' + str(ParamName) + LineDelimiter
                ReportString = ReportString + TotalIndent + FieldHeader * 'Distributed as: ' + str(Distribution) + LineDelimiter
            ReportString = ReportString + LineDelimiter
            if self.Objectives!=[]:
                ReportString = ReportString + TotalIndent + 'The population holds the following objectives:' + LineDelimiter
                for Objective in self.Objectives:
                    (FilterExpr, StatExpr, StatFunction, TargetValue, Weight, CalcValue, CalcError) = Objective
                    ReportString = ReportString + LineDelimiter
                    ReportString = ReportString + TotalIndent + FieldHeader * 'Filter Expression: ' + str(FilterExpr) + LineDelimiter
                    ReportString = ReportString + TotalIndent + FieldHeader * 'Statistics Expression: ' + str(StatExpr) + LineDelimiter
                    ReportString = ReportString + TotalIndent + FieldHeader * 'Statistics Function: ' + str(StatFunction) + LineDelimiter
                    ReportString = ReportString + TotalIndent + FieldHeader * 'Target Value: ' + str(TargetValue) + LineDelimiter
                    ReportString = ReportString + TotalIndent + FieldHeader * 'Weight: ' + str(Weight) + LineDelimiter
                    ReportString = ReportString + TotalIndent + FieldHeader * 'Calculated Value: ' + str(CalcValue) + LineDelimiter
                    ReportString = ReportString + TotalIndent + FieldHeader * 'Calculated Error: ' + str(CalcError) + LineDelimiter
                ReportString = ReportString + LineDelimiter
        else:
            # This means the population set is based in Data, print it
            # First calculate the largest length string for each column while
            # including the header length first
            HeaderLengths = map(lambda (ParamName,Distribution): len(ParamName), self.DataColumns)
            # Now traverse the data
            for DataRow in self.Data:
                for (ColumnNum, DataEntry) in enumerate(DataRow):
                    HeaderLengths[ColumnNum] = max(HeaderLengths[ColumnNum], len(str(Iif(DataEntry==None,'',DataEntry))))
            # Now use these column lengths while creating the data table
            # First create the title line.
            ReportString = ReportString + TotalIndent
            for (ColumnNum,(ParamName,Distribution)) in enumerate(self.DataColumns):
               ReportString = ReportString + ParamName.rjust(HeaderLengths[ColumnNum]) + ColumnSpacing
            ReportString = ReportString + LineDelimiter
            for (RowNum,DataRow) in enumerate(self.Data):
                ReportString = ReportString + TotalIndent
                for (ColumnNum, DataEntry) in enumerate(DataRow):
                    ReportString = ReportString + str(Iif(DataEntry==None,'',DataEntry)).rjust(HeaderLengths[ColumnNum]) + ColumnSpacing
                ReportString = ReportString + LineDelimiter
        ReportString = ReportString + TotalIndent + SectionSeparator + LineDelimiter
        return ReportString

    def Copy(self, NewName = None):
        """ Returns an object that copies this one """
        NewName = CalcCopyName(self, NewName)
        NewRecord = PopulationSet(ID = 0, Name = NewName, Source = self.Source, Notes = self.Notes, DerivedFrom = self.ID, DataColumns = self.DataColumns, Data = self.Data, Objectives = self.Objectives)
        return NewRecord

    # Description String
    Describe = DescribeReturnsName



class SimulationRule:
    """This entity holds project data required for simulation"""
    # The next parameter is commented as it can be exchanged with the list #
    AffectedParam = Expr()  # The parameter that will change value
    SimulationPhase = None    # The simulation phase in which the rule is
                              # executed:
                              # 0 = Initalization before simulation
                              #     after population generation
                              # 1 = Pre-state transition every time step
                              # 2 = invalid reserved for future use
                              # 3 = Post-state transition every time step
    OccurrenceProbability = Expr()  # Holds the parameter that defines the
                                    # probability for the condition to occur
    AppliedFormula = Expr() # Defines the formula that will change the 
                            # parameter defined in AffectedParam
    Notes = ''       # A string containing additional notes


    def __init__(self, AffectedParam , SimulationPhase , OccurrenceProbability = Expr() , AppliedFormula = Expr() , Notes = ''):
        """Constructor with default values and some consistency checks"""
        # Copy Data
        self.AffectedParam = Expr(str(AffectedParam))
        self.SimulationPhase = SimulationPhase
        self.OccurrenceProbability = Expr(str(OccurrenceProbability))
        self.AppliedFormula = Expr(str(AppliedFormula))
        self.Notes = Notes
        self.VerifyRule()

    def VerifyRule(self, AffectedParam = None, SimulationPhase = None , OccurrenceProbability = None , AppliedFormula = None):
        """Verify the validity of the rule. """
        if AffectedParam == None:
            AffectedParam = self.AffectedParam
        if SimulationPhase == None:
            SimulationPhase = self.SimulationPhase
        if OccurrenceProbability == None:
            OccurrenceProbability = self.OccurrenceProbability
        if AppliedFormula == None:
            AppliedFormula = self.AppliedFormula
        # Check data
        if not Params.has_key(AffectedParam):
            raise ValueError, 'ASSERTION ERROR: The Affected parameter ' + str(AffectedParam) + ' in the simulation rule is invalid. Please'
        # Do not allow an empty formula
        if str(AppliedFormula) == '':
            raise ValueError, 'Simulation Rule Validation Error: The applied formula field in the simulation rule cannot be empty. Please enter an expression to this field'
        if SimulationPhase not in [0,1,3]:
            raise ValueError, 'ASSERTION ERROR: Simulation Phase is out of range.'
        if Params[AffectedParam].ParameterType not in ['Number','Integer','System Option']:
            raise ValueError, 'Simulation Rule Validation Error: The affected parameter has an invalid parameter type for a simulation rule.'
        if Params[AffectedParam].ParameterType == 'System Option' and (SimulationPhase !=0 or self.OccurrenceProbability != ''):
            raise ValueError, 'Simulation Rule Validation Error: System Option initialization is allowed only in the initialization phase and no occurrence probability is allowed. Either change the rule phase, or change the parameter type'
        if Params[AffectedParam].Formula != '' and Params[AffectedParam].ParameterType != 'System Option' and SimulationPhase !=0:
            raise ValueError, 'Simulation Rule Validation Error: The Affected parameter ' + str(AffectedParam) + ' in the rule has a value assigned to it upon definition: ' + str(Params[AffectedParam].Formula) + '. Since this violated the fact that a new value will be assigned in the rule, it is impossible to use this parameter in a rule. It is only possible to override a System Option parameter during initialization. Either use a different parameter in this rule or redefine the parameter to include no value.'
        return 

    def IsParamDependant(self, ParamName):
        """ Returns True if dependant on ParamName """
        Result = ParamName in self.FindDependantParams(ParamType = None)
        return Result

    def FindDependantParams(self, ParamType = None):
        """ Find the dependant parameters """
        Result = []
        Result = Result + self.AffectedParam.FindDependantParams(ParamType = ParamType)
        Result = Result + self.OccurrenceProbability.FindDependantParams(ParamType = ParamType)
        Result = Result + self.AppliedFormula.FindDependantParams(ParamType = ParamType)
        return Result

    def GenerateReport(self, FormatOptions = None):
        """ Generate the report for this entity instance """
        TotalIndent = HandleOption('TotalIndent', FormatOptions,'')
        IndentAtom = HandleOption('IndentAtom', FormatOptions,'  ')
        #ColumnSpacing = HandleOption('ColumnSpacing', FormatOptions,' | ')
        FieldHeader = HandleOption('FieldHeader', FormatOptions,True)
        LineDelimiter = HandleOption('LineDelimiter', FormatOptions,'\n')
        SectionSeparator = HandleOption('SectionSeparator', FormatOptions,70*'_')
        #ShowHidden = HandleOption('ShowHidden', FormatOptions,False)
        ShowDependency = HandleOption('ShowDependency', FormatOptions,False)
        DetailLevel = HandleOption('DetailLevel', FormatOptions, 0)
        # DetailLevel is unused
        ReportString = ''
        ReportString = ReportString + TotalIndent + FieldHeader * 'Affected Parameter: ' + str(self.AffectedParam) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Simulation Phase: ' + ['Init' , 'Pre-state', '*** Invalid Reserved ***' ,'Post-state'][self.SimulationPhase]
        ReportString = ReportString + TotalIndent + FieldHeader * 'Occurrence Probability: ' + str(self.OccurrenceProbability) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Applied Formula: ' + str(self.AppliedFormula) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Rule Notes: ' + str(self.Notes).replace('\n','\n'+TotalIndent) + LineDelimiter
        if ShowDependency:
            RevisedFormatOptions = HandleOption('TotalIndent', FormatOptions, TotalIndent + IndentAtom, True)
            RevisedFormatOptions = HandleOption('DetailLevel', RevisedFormatOptions, DetailLevel-1, True)        
            ReportString = ReportString + self.AffectedParam.GenerateReport(RevisedFormatOptions)
            ReportString = ReportString + self.AppliedFormula.GenerateReport(RevisedFormatOptions)
        ReportString = ReportString + TotalIndent + SectionSeparator + LineDelimiter
        return ReportString

    def Describe(self):
        """ Generates a string that describes the rule """
        ShortFormFormatOptions = [ ('TotalIndent', ''), ('LineDelimiter','; ' ), ('SectionSeparator','' ) ]
        RetVal = self.GenerateReport(ShortFormFormatOptions)
        return RetVal


class Project:
    """Defines a project entity at the top level"""
    ID = 0     # Unique key identifier of the project
    Name = ''         # A string containing the name of the project
    Notes = ''        # A string containing additional notes
    PrimaryModelID = 0  # The Model ID upon which simulation will be based
                        # or 0 for an estimation project
    PrimaryPopulationSetID = 0 # The Population Set ID to be used in simulation
    NumberOfSimulationSteps = 0 # The number of time steps for which the
                                # simulation may reach before termination
    NumberOfRepetitions = 0    # The number of repetitions of the simulation
                               # for each individual
    SimulationRules = []     # A sequence of SimulationRule
    DerivedFrom = 0   # The project ID this project was created from.
    CreatedOn = InitTime     # The time this entity was created on
    LastModified = InitTime  # The last time this entity was modified on

    def __init__(self, ID = 0, Name = '' , Notes = '' , PrimaryModelID = 0  , PrimaryPopulationSetID = 0 , NumberOfSimulationSteps = 0  , NumberOfRepetitions = 0  , SimulationRules = [] , DerivedFrom = 0):
        """Constructor with default values and some consistency checks"""
        # Verify that the data is consistant
        self.VerifyData(Name, Notes, PrimaryModelID, PrimaryPopulationSetID, NumberOfSimulationSteps, NumberOfRepetitions, SimulationRules, DerivedFrom)
        # Copy variables
        self.ID = ID
        self.Name = Name
        self.Notes = Notes
        self.PrimaryModelID = PrimaryModelID
        self.PrimaryPopulationSetID = PrimaryPopulationSetID
        self.NumberOfSimulationSteps = NumberOfSimulationSteps
        self.NumberOfRepetitions = NumberOfRepetitions
        self.DerivedFrom = DerivedFrom
        self.CreatedOn = datetime.datetime.now()
        self.LastModified = datetime.datetime.now()
        self.SimulationRules = copy.deepcopy(SimulationRules)

        
    def VerifyData(self, Name = None , Notes = None, PrimaryModelID = None  , PrimaryPopulationSetID = None , NumberOfSimulationSteps = None  , NumberOfRepetitions = None  , SimulationRules = None , DerivedFrom = None , DerivedCreationDate = None):
        """Verifies that project Data is valid"""
        RetVal = None
        if Name == None:
            Name = self.Name
        if Notes == None:
            Notes = self.Notes
        if PrimaryModelID == None:
            PrimaryModelID = self.PrimaryModelID
        if PrimaryPopulationSetID == None:
            PrimaryPopulationSetID = self.PrimaryPopulationSetID
        if NumberOfSimulationSteps == None:
            NumberOfSimulationSteps = self.NumberOfSimulationSteps
        if NumberOfRepetitions == None:
            NumberOfRepetitions = self.NumberOfRepetitions
        if SimulationRules == None:
            SimulationRules = self.SimulationRules
        if DerivedFrom == None:
            DerivedFrom = self.DerivedFrom
        # Check validness
        if (DerivedFrom != 0) and not Projects.has_key(DerivedFrom):
                raise ValueError, 'ASSERTION ERROR: This project is derived from an non existing project'
        # Check parameters for a simulation project
        if not StudyModels.has_key(PrimaryModelID):
            raise ValueError, 'Project Validation Error: The Primary Model to be used by the project is undefined. Please Define a proper Primary model.'
        if not PopulationSets.has_key(PrimaryPopulationSetID):
            raise ValueError, 'Project Validation Error: The population set to be used by the project is undefined.'
        # Populations based on distribution are now allowed, the following
        # commented lines of code are deprecated and should be removed
        # in the future unless a stricter check is needed
        # if PopulationSets[PrimaryPopulationSetID].Data == []:
        #    raise ValueError, 'Project Validation Error: The population set   "' + PopulationSets.ID2Name(PrimaryPopulationSetID) + '" chosen for the project does not contain data. Make sure the population set is defined by Data, rather than by distribution. The Error was raised for the project "' + Name + '"'
        if (not IsInt(NumberOfSimulationSteps)) or (NumberOfSimulationSteps <= 0):
            raise ValueError, 'Project Validation Error: The number of simulation steps should be a positive integer. The number of simulation steps defined was: ' + str(NumberOfSimulationSteps) + '. The Error was raised for the project "' + Name + '"' 
        if (not IsInt(NumberOfRepetitions)) or (NumberOfRepetitions <= 0):
            raise ValueError, 'Project Validation Error: The number of repetitions should be a positive integer. The number of repetitions defined was: ' + str(NumberOfRepetitions) + '. The Error was raised for the project "' + Name + '"'
        # Check if the simulation rules are valid
        if not IsList(SimulationRules):
            raise ValueError, 'ASSERTION ERROR: Simulation rules are not properly defined '
        # Check that the rules are ordered correctly to construct
        # the phases in a correct sorting order                                      
        RulePhase = map (lambda Entry: Entry.SimulationPhase, SimulationRules)
        RulePhaseDiffAscending = map (IsLowerOrEqualOp , RulePhase[:-1] , RulePhase[1:])
        if not all(RulePhaseDiffAscending):
            raise ValueError, 'ASSERTION ERROR: The rules are ordered in a way that conflicts with the phase order - reorder or redefine the rules'
        return RetVal

    def PrepareForSimulation (self, RepairPopulation = DefaultSystemOptions['RepairPopulation'], VerboseLevel = DefaultSystemOptions['VerboseLevel'], OverridePopulationSet = None):
        """ Validate and Prepare the project and related info for simulation"""
        # Verify the validity of the study model
        SimulationStudyModel = StudyModels[self.PrimaryModelID]
        SimulationStudyModel.VerifyStudyModelValidity()
        # Create the Population set for Simulation
        if OverridePopulationSet == None:
            PreparedPopulationSet = PopulationSets[self.PrimaryPopulationSetID].PreparePopulationSetForSimulation(self.PrimaryModelID, RepairPopulation, VerboseLevel)
        else:
            PreparedPopulationSet = OverridePopulationSet.PreparePopulationSetForSimulation(self.PrimaryModelID, RepairPopulation, VerboseLevel)  
        # Create a Simulation Results structure
        ResultsInfo = SimulationResult(self.ID)
        # Create a list of parameters
        RelatedParamKeys = self.FindDependantParams() 
        # Note that the related state IDs are sorted and therefore outputted
        RelatedStateIDs = SimulationStudyModel.FindStatesInStudyModel(IncludeSubProcess = True)
        RelatedTransitionsKeys = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey) : StudyModelIDKey == self.PrimaryModelID, Transitions.keys()))
        RelatedStates = StatesClass(map (lambda StateID: (StateID , States[StateID])  , RelatedStateIDs))
        RelatedTransitions = TransitionsClass(map (lambda TransKey: (TransKey , Transitions[TransKey]) , RelatedTransitionsKeys))
        RelatedParams = ParamsClass(map (lambda ParamKey: (ParamKey , Params[ParamKey])  , RelatedParamKeys))
        return (SimulationStudyModel, RelatedStateIDs, RelatedStates, RelatedTransitions, PreparedPopulationSet, ResultsInfo, RelatedParams) 

    def CompileSimulation (self, SimulationScriptFileNamePrefix = None, OutputFileNamePrefix = None , RandomStateFileNamePrefix = None, SimulationOptions = None, SkipDumpingFilesIfError = True, OverrideRepetitionCount = None, OverridePopulationSet = None, RecreateFromTraceBack = None):
        """Compiles a simulation program and returns its path"""
        # if recreating simulation from traceback - all input parameters are 
        # recovered from the traceback - Note that the last element in the
        # tuple recored in _CompileArguments in the previous run
        if RecreateFromTraceBack != None:
            # Recreate inputs from traceBack except from OverridePopulationSet
            # and OverrideRepetitionCount which do not get replaced  in compile
            # options since it is the population reconstructed from
            # distributions and holds its own traceback information
            # Note the Dummy parameters are never used, only GenerationOptions
            # are replicated from the previous run since those are substantial
            # to the simulation and not only control the random seed - the rest
            # of the parameters are not substantial or are controlled otherwise
            (DummySimulationScriptFileNamePrefix, DummyOutputFileNamePrefix, DummyRandomStateFileNamePrefix, SimulationOptions, DummySkipDumpingFilesIfError) = RecreateFromTraceBack[-2][:-1]
        if SimulationOptions == None:
            SimulationOptions = []
        SimulationOptionsToUse = []
        # Simulation options are defined in the following priority order:
        # 1) SimulationOptions as defined in the function input,
        # 2) Project definitions,
        # 3) User defined system option Defaults,
        # 4) Global system defaults
        # Each system option is handled and collected according to the
        # above priority hierarchy. 
        # Apply global defaults for simulation
        for ParamName in sorted(DefaultSystemOptions.keys()):
            # First define the global system defaults
            SimulationOptionsToUse = HandleOption(ParamName, SimulationOptionsToUse, DefaultSystemOptions[ParamName], True)
            # Override with user defined System option Defaults
            if Params.has_key(ParamName):
                DummyExpr=Expr()
                ActualValue=DummyExpr.Evaluate(ExprText = Params[ParamName].Formula)
                if ActualValue != None:
                    # Use User defined defaults
                    SimulationOptionsToUse = HandleOption(ParamName, SimulationOptionsToUse, ActualValue, True)
            # Override with user defined system options defined in project rules
            # note that irrelevant system options for simulation are ignored and
            # not checked for validity
            FilteredRules = filter (lambda Rule: Rule.AffectedParam == ParamName and Rule.SimulationPhase == 0 , self.SimulationRules)
            if len(FilteredRules)>1:
                raise ValueError, 'Simulation Compilation Error: More than one Rule in the project uses the System Option: ' + str(ParamName) +' as the affected parameter, remove all repeated definitions and leave only one to allow creating the simulation. The error was detected for the project ' + self.Name 
            elif len(FilteredRules)==1:
                Rule = FilteredRules[0]
                ParamValue = Rule.AppliedFormula.Evaluate()
                SimulationOptionsToUse = HandleOption(ParamName, SimulationOptionsToUse, ParamValue, True)
            # Override with input supplied in function input:
            ExtractedValue = HandleOption(ParamName, SimulationOptions, None)
            if ExtractedValue != None:
                SimulationOptionsToUse = HandleOption(ParamName, SimulationOptionsToUse, ExtractedValue, True)
        # Now Actually extract the values to variables to use in the code
        ValidateDataInRuntime = HandleOption('ValidateDataInRuntime', SimulationOptionsToUse)
        NumberOfErrorsConsideredAsWarningsForSimulation = HandleOption('NumberOfErrorsConsideredAsWarningsForSimulation', SimulationOptionsToUse)
        NumberOfTriesToRecalculateSimulationStep = HandleOption('NumberOfTriesToRecalculateSimulationStep', SimulationOptionsToUse)
        NumberOfTriesToRecalculateSimulationOfIndividualFromStart = HandleOption('NumberOfTriesToRecalculateSimulationOfIndividualFromStart', SimulationOptionsToUse)
        SystemPrecisionForProbabilityBoundCheck = HandleOption('SystemPrecisionForProbabilityBoundCheck', SimulationOptionsToUse)
        RepairPopulation = HandleOption('RepairPopulation', SimulationOptionsToUse)
        VerboseLevel = HandleOption('VerboseLevel', SimulationOptionsToUse)
        RandomSeed = HandleOption('RandomSeed', SimulationOptionsToUse)
        # Record the Traceback information of the population
        if OverridePopulationSet == None:
            PopulationTraceBack = PopulationSets[self.PrimaryPopulationSetID].TraceBack
        else:
            PopulationTraceBack = OverridePopulationSet.TraceBack
        # Extract Default file names, but first create the TimeStamp
        if SimulationScriptFileNamePrefix == None:
            SimulationScriptFileNamePrefix = DefaultSimulationScriptFileNamePrefix
        # Looking at the population TraceBack
        if PopulationTraceBack == ():
            # If no traceback exists for population generation then there is no
            # need for special file name generaation
            PopulationPrefix = '_NoGen_'
        else:
            # To help tracability when generating from a population that
            # was generated itself use the generating script file name 
            # to help find out the connection between scripts.
            # RandomStateFileName for the population is located in 
            # PopulationTraceBack[3]
            (PopScriptPathOnly , PopScriptFileNameOnly, PopScriptFileNameFullPath) = DetermineFileNameAndPath(PopulationTraceBack[3])
            PopulationPrefix = '_'+ os.path.splitext(PopScriptFileNameOnly)[0] + '_'
        SimulationScriptFileNamePrefixUpdated = SimulationScriptFileNamePrefix + PopulationPrefix
        if OutputFileNamePrefix == None:
            OutputFileNamePrefix = DefaultSimulationOutputFileNamePrefix 
        if RandomStateFileNamePrefix == None:
            RandomStateFileNamePrefix = DefaultRandomStateFileNamePrefix

        if OverrideRepetitionCount != None:
            NumberOfRepetitions = OverrideRepetitionCount
        else:
            NumberOfRepetitions = self.NumberOfRepetitions
        if NumberOfRepetitions <=0:
            raise ValueError, 'ASSERTION ERROR: non positive repetition count discovered during Simulation Compilation '

           
        # First prepare the data for simulation
        (SimulationStudyModel, RelatedStateIDs, RelatedStates, RelatedTransitions, PreparedPopulationSet, ResultsInfo, RelatedParams) = self.PrepareForSimulation(RepairPopulation,VerboseLevel,OverridePopulationSet)
        # Check that the population set has data and not only distributions
        if PreparedPopulationSet.Data == []:
            raise ValueError, 'ASSERTION ERROR: population set with no data was encountered during Simulation Compilation - at this point a population set must have data and can not be based on distributions'

        # Determine the filename and path
        (ScriptFileDescriptor, ScriptFileName) = tempfile.mkstemp ( PythonSuffix, SimulationScriptFileNamePrefixUpdated , SessionTempDirecory , True)
        (ScriptPathOnly , ScriptFileNameOnly, ScriptFileNameFullPath) = DetermineFileNameAndPath(ScriptFileName)
        # Now actually create the file
        try:
            SimFile = os.fdopen(ScriptFileDescriptor,'w')
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Simulation Compilation Error: The simulation script file ' + ScriptFileNameFullPath  +' cannot be created. Please make sure you specified a valid path for the file and that that file name is not in use by the system. The error was detected for the project ' + self.Name + '. Here are details about the error: ' + str(ExceptValue)

        # Generate the simulation
        def WriteSimLine(InString = None):
            """ Writes a line into the simulation file, including a new line """
            if InString == None:
                InString = ''
            try:
                SimFile.write (InString + '\n')
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                raise ValueError, 'Simulation Compilation Error: Error encountered while writing to the simulation script file ' + ScriptFileNameFullPath  +'. Please make sure that the file was not locked by the system due to quota or other reasons. The error was detected for the project ' + self.Name + '. Here are details about the error: ' + str(ExceptValue)
            return

        def WriteRules(PhaseNumber, IndentMultiplier, SystemPrecisionForProbabilityBoundCheck):
            """ Writes code for simulation rules for a given phase"""
            for Rule in self.SimulationRules:
                # Filter only covariate update rules for Phase PhaseNumber 
                if Rule.SimulationPhase == PhaseNumber:
                    WriteSimLine (Tab*IndentMultiplier + '# Processing the rule: "' + Rule.Describe() )
                    Term = ''
                    # Deal with probability occurrence clause
                    if Rule.OccurrenceProbability != '':
                        # Recreate the expression, creating the expanded expression
                        ThresholdProbability = Expr(Rule.OccurrenceProbability)
                        # Create the expression code
                        # Check if between 0 and 1 with a tolerance
                        LastValidityCheckCode = 'if not (' + repr(-SystemPrecisionForProbabilityBoundCheck) + ' <= _Temp  <= ' + repr(1.0+SystemPrecisionForProbabilityBoundCheck) + '):'
                        ErrorHandlerCode = Tab + '_WarningErrorHandler(_InputErrorString = "The occurrence probability threshold defined by a rule does not evaluate to a number between 0 and 1 within a tolerance specified by the system option parameter SystemPrecisionForProbabilityBoundCheck. The occurrence probability was evaluated to: " + str(_Temp) + " for the rule: " + ' + repr(Rule.Describe()) + ', _FatalError = True) '
                        ThresholdProbability.WriteCodeForExpression (AssignedParameterName = '_Threshold', SourceExprText = None, ValidateDataInRuntime = ValidateDataInRuntime, WriteLnFunction = WriteSimLine, Lead = Tab*IndentMultiplier, Tab = Tab, TempTokenPrefix = '_Temp', OverrideLastCheck = [LastValidityCheckCode, ErrorHandlerCode])
                        Term = Term + ' DataDef.numpy.random.random() < _Threshold and '
                    # Eat away the extra 'and' and handle IndentMultiplier 
                    if Term != '':
                        # If clause exists
                        Term = Term[:-5]
                        LeadIndent = Tab
                        WriteSimLine (Tab*IndentMultiplier + 'if ' + Term + ':')
                    else:
                        # If clause does not exist
                        LeadIndent = ''
                    TheAppliedFormulaExprToCode = Expr(Rule.AppliedFormula)
                    # Create the expression code
                    TheAppliedFormulaExprToCode.WriteCodeForExpression (AssignedParameterName = Rule.AffectedParam , SourceExprText = None, ValidateDataInRuntime = ValidateDataInRuntime, WriteLnFunction = WriteSimLine, Lead = Tab*IndentMultiplier + LeadIndent, Tab = Tab, TempTokenPrefix = '_Temp', OverrideLastCheck = None )

        # Define constants required later on
        SimulationModelID = SimulationStudyModel.ID
        Tab = ' '*4
        # Continue with defining the data for the simulation
        WriteSimLine ('################################################################################')
        TitleFileName ='# ' + ScriptFileNameOnly + ' '*(77-len(ScriptFileNameOnly)) + '#'
        WriteSimLine (TitleFileName)
        WriteSimLine ('# This simulation script was automatically Generated on: '+ datetime.datetime.now().isoformat(' ')[:19] + '   #')
        WriteSimLine ('# by the MIcroSimulation Tool (MIST).                                          #')
        WriteSimLine ('################################################################################')
        WriteSimLine ()
        WriteSimLine ('##################### Imports #####################')
        WriteSimLine ('from __future__ import division')
        WriteSimLine ('import DataDef')
        WriteSimLine ('import sys')
        WriteSimLine ('import os')
        WriteSimLine ('import pickle')
        WriteSimLine ('import tempfile')        
        WriteSimLine ('#### Create Validation Error/Warning Handler ##### ')
        WriteSimLine ('_WarningCount = 0')
        WriteSimLine ('sys.exc_clear()')
        WriteSimLine ('(_EmptyExceptType, _EmptyExceptValue) = sys.exc_info()[:2]')
        WriteSimLine ('def _WarningErrorHandler( _InputErrorString = None, _FatalError = False):')
        WriteSimLine (Tab + 'global _WarningCount')
        WriteSimLine (Tab + '(_ExceptType, _ExceptValue, _ExceptTraceback) = sys.exc_info()')
        WriteSimLine (Tab + 'if _InputErrorString != None:')
        WriteSimLine (Tab + Tab + 'if (_ExceptType, _ExceptValue) == (_EmptyExceptType, _EmptyExceptValue):')
        WriteSimLine (Tab + Tab + Tab + '(_ExceptType, _ExceptValue) = (ValueError, _InputErrorString)')
        WriteSimLine (Tab + Tab + 'else:')
        WriteSimLine (Tab + Tab + Tab + '_ExceptValue = _InputErrorString + " Here are further details: " + str(_ExceptValue)')
        WriteSimLine (Tab + '_WarningCount = _WarningCount + 1')
        WriteSimLine (Tab + 'if _FatalError or (_WarningCount > ' + SmartStr(NumberOfErrorsConsideredAsWarningsForSimulation) + '):')
        WriteSimLine (Tab + Tab + 'raise _ExceptType, "Simulation Runtime Error: " + str(_ExceptValue)')
        WriteSimLine (Tab + 'else:')
        WriteSimLine (Tab + Tab + 'print "Simulation Runtime Warning:" + str(_ExceptValue)')
        # Verify version
        WriteSimLine ('_GeneratingVersion = ' + repr(Version) )
        WriteSimLine ('if DataDef.Version != _GeneratingVersion:')

        WriteSimLine (Tab + "_WarningErrorHandler(_InputErrorString = 'The simulation was created with a different version than the data definitions used. This may raise incompatibility issues. The simulation script was created with version ' + repr(" + repr(Version) + ") + ' while the definition file version is ' + repr(DataDef.Version), _FatalError = True)")
        WriteSimLine ()
        WriteSimLine ('############## Load the Required Parameters #######')
        ############## Load the Required Parameters #######
        WriteSimLine ('_ParamsInfo = pickle.loads(' + repr(pickle.dumps(RelatedParams)) + ')')
        WriteSimLine ('_StatesInfo = pickle.loads(' + repr(pickle.dumps(RelatedStates)) + ')')
        WriteSimLine ('_ModelInfo = pickle.loads(' + repr(pickle.dumps(SimulationStudyModel)) + ')')
        WriteSimLine ('_TransitionsInfo = pickle.loads(' + repr(pickle.dumps(RelatedTransitions)) + ')')
        WriteSimLine ('_PopulationSetInfo = pickle.loads(' + repr(pickle.dumps(PreparedPopulationSet)) + ')')
        WriteSimLine ('_ProjectInfo = pickle.loads(' + repr(pickle.dumps(self)) + ')')
        WriteSimLine ('_ResultsInfo = pickle.loads(' + repr(pickle.dumps(ResultsInfo)) + ')')
        WriteSimLine ('_PopulationTraceBack = pickle.loads(' + repr(pickle.dumps(PopulationTraceBack)) + ')')
        # Note that OverridePopulationSet is not in CompileArguments to be
        # saved, it can be partilly deduced from _PopulationSetInfo and is
        # added as a comment line after compile arguments for dubug purposes
        WriteSimLine ('_CompileArguments = pickle.loads(' + repr(pickle.dumps((SimulationScriptFileNamePrefix, OutputFileNamePrefix, RandomStateFileNamePrefix, SimulationOptions, SkipDumpingFilesIfError, RecreateFromTraceBack))) + ')')
        WriteSimLine ('#_OverridePopulationSetInfoBeforePreperation = pickle.loads(' + repr(pickle.dumps(OverridePopulationSet)) + ')')
        WriteSimLine ('#_OverrideRepetitionCount = ' + str(OverrideRepetitionCount) )
        
        WriteSimLine ()
        WriteSimLine ('#### Constants ####')
        WriteSimLine ('Inf = DataDef.Inf')
        WriteSimLine ('NaN = DataDef.NaN')
        WriteSimLine ('inf = DataDef.Inf')
        WriteSimLine ('nan = DataDef.NaN')
        WriteSimLine ('#### Functions Allowed in Expressions ####')
        for FuncName in ExpressionSupportedFunctionsNames:
            WriteSimLine (FuncName + ' = DataDef.' + FuncName)
        for (FuncName, RunTimeFuncName) in RuntimeFunctionNames:
            WriteSimLine (FuncName + ' = DataDef.' + RunTimeFuncName)

        WriteSimLine ('#### Random seed ####')

        VerboseComment = Iif(VerboseLevel >= 6,'','#')
        if not IsNumericType(RandomSeed) or IsNaN(RandomSeed):
            RandomSeed = None
        # If not recreating from TraceBack figure out the random seed and
        # record the random state on file
        if RecreateFromTraceBack == None:
            WriteSimLine ('try:')
            WriteSimLine (Tab + 'DataDef.numpy.random.seed(' + SmartStr(RandomSeed) +  ')')
            WriteSimLine (Tab + '# Record the initial state of the random generator')
            WriteSimLine (Tab + '_InitialRandomState = DataDef.numpy.random.get_state()')
            WriteSimLine (Tab + '_RandomStateFileName = ""')
            WriteSimLine (VerboseComment + Tab + '(_RandomStateFileDescriptor, _RandomStateFileName) = tempfile.mkstemp ( ' + repr(TextSuffix) + ' , os.path.splitext(__file__)[0] + "_" + ' + repr(RandomStateFileNamePrefix) + '+ "_" , ' + repr(SessionTempDirecory) + ', True)')
            WriteSimLine (VerboseComment + Tab + "_OutFile = os.fdopen (_RandomStateFileDescriptor , 'w')")
            WriteSimLine (VerboseComment + Tab + 'pickle.dump(_InitialRandomState , _OutFile)')
            WriteSimLine (VerboseComment + Tab + "_OutFile.close()")
            WriteSimLine ('except:')
            if SkipDumpingFilesIfError:
                WriteSimLine (Tab + "print 'Warning - could not write the Initial Random State to file, writing to screen instead'")
                WriteSimLine (Tab + "print _InitialRandomState")
            else:
                WriteSimLine (Tab + "_WarningErrorHandler()")
        else:
            # If recreating from TraceBack then use the random state stored 
            # in the traceback
            WriteSimLine ('# Reproduce the Random state from given TraceBack information')
            WriteSimLine ('_InitialRandomState = pickle.loads(' + repr(pickle.dumps( RecreateFromTraceBack[2])) + ')')
            # use original see file name rather than None in case it exists
            WriteSimLine ('_RandomStateFileName = pickle.loads(' + repr(pickle.dumps( RecreateFromTraceBack[3])) + ')')
            WriteSimLine ('DataDef.numpy.random.set_state(_InitialRandomState)')
        WriteSimLine ()
        # reserved words
        WriteSimLine ('#### Reserved variables words ####')
        WriteSimLine ('IndividualID = 0')
        WriteSimLine ('Repetition = 0')
        WriteSimLine ('Time = 0')
        WriteSimLine ('#### Create State Handler Functions and State Classification Vector ##### ')
        WriteSimLine ()
        StateData = []
        for (StateKey, StateEntry) in RelatedStates.iteritems():
            VarName = StateEntry.GenerateAllStateIndicatorNames()[0]
            FuncName = '_Func_' + VarName
            PriorityGroup = StateEntry.SimulationPriorityGroup(SimulationModelID)
            StateData = StateData + [(StateKey , PriorityGroup , VarName, FuncName)]
        # After StateData has been created, traverse all records again to create
        # handler functions for them
        for (StateKey , PriorityGroup , VarName, FuncName) in StateData:
            StateEntry = RelatedStates[StateKey]
            WriteSimLine ('def ' + FuncName + '():')
            if PriorityGroup == 1:
                WriteSimLine (Tab + '# Terminal End State')
                WriteSimLine (Tab + 'global _Terminate_Time_Loop')
                WriteSimLine (Tab + '_Terminate_Time_Loop = True')
                WriteSimLine (Tab + '_SPQ = []')
                WriteSimLine (Tab + 'return\n')
            elif PriorityGroup == 2:
                WriteSimLine (Tab + '# Splitter State')
                TransitionsFromThisState = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey): StudyModelIDKey == SimulationModelID and FromStateKey == StateKey, RelatedTransitions.keys()))
                # Just check that all transitions probabilities are evaluate
                # to 1 exactly. This is just a symbolic check as probabilities
                # are not used. This is to alert the user to a possible mistake
                ValidProbabilities = map(lambda Entry: Expr(RelatedTransitions[Entry].Probability).ExpandedExpr.strip() in ['1','1.0'],TransitionsFromThisState)
                if not all(ValidProbabilities):
                    raise ValueError, 'Simulation Compilation Error: Cannot compile the simulation for the project ' + self.Name + ' since the model ' + StudyModels.ID2Name(SimulationModelID) + ' may have a mistake. There is at least one Transition probabilities emanating from the splitter state "' + VarName + '" that are not set to 1. Setting all transition probabilities emanating from this splitter state to 1 should resolve this issue'
                IndicatorsString = ''
                ProcessStateIDs = []
                for (StudyModelIDKey , FromStateKey , ToStateKey) in TransitionsFromThisState:
                    OutcomeStateEntry = RelatedStates[ToStateKey]
                    OutcomeStateNames = OutcomeStateEntry.GenerateAllStateIndicatorNames()
                    ProcessID = OutcomeStateEntry.FindFatherState(SimulationModelID)
                    ProcessIndicatorNames = RelatedStates[ProcessID].GenerateAllStateIndicatorNames()
                    IndicatorsString = IndicatorsString + OutcomeStateNames[0] + ', ' + OutcomeStateNames[1] + ', ' + ProcessIndicatorNames[0] + ', ' + ProcessIndicatorNames[1]+ ', '
                    ProcessStateIDs = ProcessStateIDs + RelatedStates[ProcessID].ChildStates
                    # Find state information in previously calculated StateData
                    OutcomeInfoInStateData = filter (lambda (StateKeyInfo , PriorityGroupInfo , VarNameInfo, FuncNameInfo): StateKeyInfo == ToStateKey,  StateData)
                    if len(OutcomeInfoInStateData) != 1:
                        raise ValueError, 'ASSERTION ERROR: DURING RUNTIME: This state should already exist in state data. Error found for a splitter state'
                    # Extract compile time data to define the new SPQ entry
                    ItemForSPQ = (OutcomeInfoInStateData[0])
                    # check if this state requires specialized treatment by
                    # adding it to the SPQ. All states that are not regular,
                    # meaning Priority = 5 require this special attentions
                    if ItemForSPQ[1] != 5:
                        # Write code to that defines this item and adds a small
                        # random number to the priority of the new SPQ entry at
                        # runtime
                        WriteSimLine (Tab + '_NewItemForSPQ = ( ' +str(ItemForSPQ[0]) + ' , ' + str(ItemForSPQ[1]) + ' + DataDef.numpy.random.random()' + ' , ' + str(ItemForSPQ[3]) + ')')
                        # find the correct Index in the SPQ according to the
                        # priority of this state
                        WriteSimLine (Tab + '_IndexToInsert = len(filter( lambda _SPQ_Entry:_NewItemForSPQ[1] > _SPQ_Entry[1] , _SPQ))')
                        WriteSimLine (Tab + '_SPQ.insert(_IndexToInsert , _NewItemForSPQ)')
                SetValuesString = '1, ' * len(TransitionsFromThisState)*4
                # Define the globals
                WriteSimLine (Tab +'global ' + IndicatorsString + VarName)
                # Write code to reset the state indicator
                WriteSimLine (Tab + VarName + ' = 0')
                # Write code to set state indicators emanating from the splitter
                WriteSimLine (Tab + IndicatorsString[:-2] + ' = ' + SetValuesString[:-2])
                WriteSimLine (Tab + 'return\n')
            elif PriorityGroup in [3,4,5]:
                if PriorityGroup == 3:
                    WriteSimLine (Tab + '# Joiner State')
                elif PriorityGroup == 4:
                    WriteSimLine (Tab + '# Event State')
                else:
                    WriteSimLine (Tab + '# Regular state')
                # Explore all possible ways to exit this state
                TransitionsFromThisState = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey): StudyModelIDKey == SimulationModelID and FromStateKey == StateKey, RelatedTransitions.keys()))
                NestedFuncNames = []
                Probabilities = []
                # Write the line that resets _TransitionProbabilities
                WriteSimLine (Tab + '_TransitionProbabilities = []')
                for (StudyModelIDKey , FromStateKey , ToStateKey) in TransitionsFromThisState:
                    OutcomeStateEntry = RelatedStates[ToStateKey]
                    OutcomeStateNames = OutcomeStateEntry.GenerateAllStateIndicatorNames()
                    NestedFuncName = '_NestedFunc_TransFrom' + VarName + 'To' + OutcomeStateNames[0]
                    NestedFuncNames =  NestedFuncNames + [NestedFuncName]
                    # Write code to define the nested function
                    WriteSimLine (Tab + 'def ' + NestedFuncName + '():')
                    # Define variables as global
                    WriteSimLine (Tab + Tab + 'global ' + VarName + ', ' + OutcomeStateNames[0] + ', '+ OutcomeStateNames[1] )
                    # Write code to reset the state indicator
                    WriteSimLine (Tab + Tab + VarName + ' = 0')
                    # Write code to set outcome state and entered states to 1
                    WriteSimLine (Tab + Tab + OutcomeStateNames[0] + ', '+ OutcomeStateNames[1] + ' = 1, 1')
                    OutcomeInfoInStateData = filter (lambda (StateKeyInfo , PriorityGroupInfo , VarNameInfo, FuncNameInfo): StateKeyInfo == ToStateKey,  StateData)
                    if len(OutcomeInfoInStateData) != 1:
                        raise ValueError, 'ASSERTION ERROR: DURING RUNTIME: This state should already exist in state data. Error found for a Joiner/Event/Regular state'
                    # Extract compile time data to define the new SPQ entry
                    ItemForSPQ = (OutcomeInfoInStateData[0])
                    # check if this state requires specialized treatment by
                    # adding it to the SPQ. All states that are not regular,
                    # meaning Priority = 5 require this special attentions
                    if ItemForSPQ[1] != 5:
                        # Write code that adds the new entry to the SPQ.
                        # Note that priority 0 is used to indicate this state
                        # should be processed first in the next step, regardless
                        # of the true priority of the state
                        WriteSimLine (Tab + Tab + '_SPQ.insert( 0, ( ' +str(ItemForSPQ[0]) + ' , 0 , ' + str(ItemForSPQ[3]) + ') )')
                    WriteSimLine (Tab + Tab + 'return')
                    # Validate the probability expression once more, this will
                    # also generate the expanded expression
                    Probabaility = Expr(RelatedTransitions[(StudyModelIDKey , FromStateKey , ToStateKey)].Probability)
                    # Create the expression code
                    # Check if between 0 and 1 with a tolerance
                    LastValidityCheckCode = 'if not (' + repr(-SystemPrecisionForProbabilityBoundCheck) + ' <= _Temp  <= ' + repr(1.0+SystemPrecisionForProbabilityBoundCheck) + '):'
                    ListOfEssentialDependantsStr = str(SetDiff(Expr(Probabaility.ExpandedExpr).DependantParams, ExpressionSupportedFunctionsAndSpecialNames)).replace("'",'')
                    ErrorHandlerCode = Tab +'_WarningErrorHandler(_InputErrorString = "The transition probability is not within the range [0,1] within a tolerance defined by the SystemPrecisionForProbabilityBoundCheck system option parameter. Here are additional details. The Transition is from ' + VarName + ' To ' + OutcomeStateNames[0] + ' with the probability ' + str(Probabaility) + ' that evaluates to " + str(' + str(Probabaility.ExpandedExpr) + ') + " and that expands to ' + str(Probabaility.ExpandedExpr) + ' with the following basic dependants ' + ListOfEssentialDependantsStr + ' getting the values " + str('+ ListOfEssentialDependantsStr + ')' + ', _FatalError = True )'
                    Probabaility.WriteCodeForExpression (AssignedParameterName = '_Threshold' , SourceExprText = None, ValidateDataInRuntime = ValidateDataInRuntime, WriteLnFunction = WriteSimLine, Lead = Tab, Tab = Tab, TempTokenPrefix = '_Temp', OverrideLastCheck = [LastValidityCheckCode, ErrorHandlerCode])
                    # Now add the transition probability to the vector
                    # of transition probabilities
                    WriteSimLine (Tab + '_TransitionProbabilities = _TransitionProbabilities + [_Threshold]')
                    # Update the probability vector
                    Probabilities = Probabilities + [Probabaility.ExpandedExpr]
                if PriorityGroup == 5:
                    # For regular states add a function that does nothing to
                    # handle the situation of transition from a state to itself. 
                    NestedFuncName = '_NestedFunc_TransFrom' + VarName + 'To' + VarName
                    NestedFuncNames =  NestedFuncNames + [NestedFuncName]
                    # Generate code for this Null function
                    WriteSimLine (Tab + 'def ' + NestedFuncName + '():')
                    WriteSimLine (Tab + Tab + 'return')
                # Write code to generate the Nested Handling function vector
                WriteSimLine (Tab + '_HandlingFunctionsForStates = ' + str(NestedFuncNames).replace("'",''))
                # construct a cumulative percentage vector
                WriteSimLine (Tab + '_CumulativeProbabilities = []')
                WriteSimLine (Tab + '_CumulativeProbability = 0.0')
                WriteSimLine (Tab + 'for _TransProbability in _TransitionProbabilities:')
                WriteSimLine (Tab + Tab + '_CumulativeProbability = _CumulativeProbability + _TransProbability')
                WriteSimLine (Tab + Tab + '_CumulativeProbabilities = _CumulativeProbabilities + [_CumulativeProbability]')
                # Only if runtime validation of data is required,
                # Since this is a design issue, raise a fatal error rather
                # than just a warning since otherwise a user may ignore these
                # important design issues
                if ValidateDataInRuntime >= 1:
                    if PriorityGroup in [3,4]:
                        # For event and joiner states
                        # Check if within 0 and 1 within a tolerance
                        WriteSimLine (Tab +'if not (' + repr(1.0-SystemPrecisionForProbabilityBoundCheck) + ' <= _CumulativeProbability  <= ' + repr(1.0+SystemPrecisionForProbabilityBoundCheck) + '):')
                        WriteSimLine (Tab + Tab + '_WarningErrorHandler(_InputErrorString = "The cumulative sum of probabilities emanating from and event or a joiner State ' + VarName + ' is not exactly 1 within a tolerance defined by the SystemPrecisionForProbabilityBoundCheck system option parameter. The cumulative probability calculated was: "+str(_CumulativeProbability), _FatalError = True)')
                    else:
                        # For regular states
                        # Check if within 0 and 1 within a tolerance
                        WriteSimLine (Tab +'if not (' + repr(-SystemPrecisionForProbabilityBoundCheck) + ' <= _CumulativeProbability  <= ' + repr(1.0+SystemPrecisionForProbabilityBoundCheck) + '):')
                        WriteSimLine (Tab + Tab + '_WarningErrorHandler(_InputErrorString = "The cumulative sum of probabilities for states emanating from State ' + VarName + ' is not in the interval [0,1] within a tolerance defined by the SystemPrecisionForProbabilityBoundCheck system option parameter. The cumulative probability calculated was: "+str(_CumulativeProbability), _FatalError = True)')
                if PriorityGroup ==5:
                    # Generate code to add the last value of 1 to the 
                    # cumulative vector for regular states. This is not
                    # required for event states or joiner states that end in 1
                    WriteSimLine (Tab + '_CumulativeProbabilities = _CumulativeProbabilities + [1.0]')
                if PriorityGroup == 3:
                    # A joiner state is also responsible for subprocess reset
                    OriginalSplitter = States[StateKey].JoinerOfSplitter
                    TransitionsFromThisSplitter = sorted(filter (lambda (StudyModelIDKey , FromStateKey , ToStateKey) : StudyModelIDKey == SimulationModelID and FromStateKey == OriginalSplitter, RelatedTransitions.keys()))
                    # Processes to be joined are defined by the splitter state
                    # rather than by transitions into the joiner state
                    ProcessesToBeJoined = map (lambda (StudyModelIDKey , FromStateKey , ToStateKey): RelatedStates[ToStateKey].FindFatherState(SimulationModelID), TransitionsFromThisSplitter)
                    SubProcessIndicatorsString = ''
                    StateIDsToBeRemovedFromSPQ = []
                    ToBeResetSubProcessIDs = []
                    # For each process joined by the joiner
                    for ProcessID in ProcessesToBeJoined:
                        # Find all descendants that are not subprocesses
                        (AllStatesReturned, IsSubProcessReturned, NestingLevelReturned) = States[ProcessID].FindChildStates()
                        NonSubProcessDescendants = FilterByAnother(AllStatesReturned, map(NotOp,IsSubProcessReturned))
                        StateIDsToBeRemovedFromSPQ = StateIDsToBeRemovedFromSPQ + NonSubProcessDescendants
                        SubProcessDescendants = FilterByAnother(AllStatesReturned, IsSubProcessReturned)
                        ToBeResetSubProcessIDs = ToBeResetSubProcessIDs + SubProcessDescendants
                    for ProcessID in ToBeResetSubProcessIDs:
                        SubProcessIndicatorsString = SubProcessIndicatorsString + RelatedStates[ProcessID].GenerateAllStateIndicatorNames()[0] + ', '
                    ResetValuesString = '0, ' * len(ToBeResetSubProcessIDs)
                    # Write code to remove from the SQP states in subprocesses
                    # leading to the joiner state
                    WriteSimLine (Tab + 'for _StateIndexInSPQ in reversed(range(len(_SPQ))):')
                    WriteSimLine (Tab + Tab +'if _SPQ[_StateIndexInSPQ][0] in ' + str (StateIDsToBeRemovedFromSPQ) + ':')
                    WriteSimLine (Tab + Tab + Tab + '_SPQ.pop(_StateIndexInSPQ) ')
                    # Define variables as global
                    WriteSimLine (Tab + 'global ' + SubProcessIndicatorsString[:-2])
                    # Write code to reset all subprocesses indicators leading to
                    # the joiner
                    WriteSimLine (Tab + SubProcessIndicatorsString[:-2] + ' = ' + ResetValuesString[:-2])
                    # Note that the state itself is not reset here and will be reset when the
                    # transition function is processed
                # Write code to generate a random number and test it against the
                # cumulative vector
                WriteSimLine (Tab + '_FlipCoinResult = DataDef.numpy.random.random()')
                WriteSimLine (Tab + '_IndexOfFunction = 0')
                WriteSimLine (Tab + 'while _FlipCoinResult > _CumulativeProbabilities[_IndexOfFunction]:')
                WriteSimLine (Tab + Tab +'_IndexOfFunction = _IndexOfFunction + 1')
                # Write code to generate the correct handling function for the
                # state
                WriteSimLine (Tab + '_HandlingFunctionsForStates[_IndexOfFunction]()')
                WriteSimLine (Tab + 'return\n')
            elif PriorityGroup == 6:
                WriteSimLine (Tab + '# SubProcess State')
                WriteSimLine (Tab + 'raise ValueError, "ASSERTION ERROR: DURING RUNTIME: Sub-process states are not supported at this point in the simulation directly. They are automatically handled by the system"')
                WriteSimLine (Tab + 'return\n')
            else:
                raise ValueError, 'ASSERTION ERROR: DURING RUNTIME: This state has not proper priority code - cannot generate simulation code'

        # Create the State classification vector
        WriteSimLine ()
        SortedStateData = sorted ( StateData, None , key = lambda (ID, Priority, VarName, FuncName): (Priority,ID))
        SortedStateDataRelevantStr = str(map (lambda (ID, Priority, VarName, FuncName): (ID, Priority, FuncName), SortedStateData))
        WriteSimLine ('_StateClassificationVec = ' + SortedStateDataRelevantStr.replace("'",''))

        WriteSimLine ('############### Execute Simulation ###############')
        WriteSimLine ('####### Subject Loop #######')
        WriteSimLine ('_Subject = 0')
        WriteSimLine ('while _Subject < (len(_PopulationSetInfo.Data)):')
        WriteSimLine (Tab + 'IndividualID = IndividualID +1')
        # At verbose level of 10 or more, display repetition information       
        WriteSimLine (Tab + '# Comment/Uncomment the next line to disable/enable printing of verbose information')
        WriteSimLine (Tab + Iif(VerboseLevel >= 10,'','#') + 'print "Simulating Individual #" + str(IndividualID)')
        # Reset the number of times an individual was generated
        # Note that although the same person may be generated several times
        # in each repetition, each such individual is considered separate for
        # the sake of counting tries to calculate the person
        WriteSimLine (Tab + '_NumberOfTriesToGenerateThisIndividual = 1')
        
        WriteSimLine (Tab + '##### Repetition Loop #####')
        WriteSimLine (Tab + 'Repetition = 0')
        WriteSimLine (Tab + 'while Repetition < (' + str( NumberOfRepetitions) + '):')
        WriteSimLine (Tab + Tab + '# Reset repeat individual repetition flag in case it was set')
        WriteSimLine (Tab + Tab + '_RepeatSameIndividualRepetition = False')
        
        WriteSimLine (Tab + Tab + '#Init all parameters - Resetting them to zero')
        # At verbose level of 20 or more, display repetition information
        WriteSimLine (Tab + Tab + '# Comment/Uncomment the next line to disable/enable printing of verbose information')
        WriteSimLine (Tab + Tab + Iif(VerboseLevel >= 20,'','#') + 'print "  Repetition = " + str(Repetition)')

        # Init all parameters - Reset to zero
        # This includes Population set columns, AffectedParameters
        # + State indicators
        # Can be created from the results list
        AllParamsStr = str(ResultsInfo.DataColumns[3:]).replace("', '",', ')[2:-2]
        RightSideZeroStr = '0, '*(len(ResultsInfo.DataColumns[3:])-1)+ '0'
        WriteSimLine (Tab + Tab + AllParamsStr + ' = ' + RightSideZeroStr)

        WriteSimLine (Tab + Tab + '# Init parameters from population set')
        AllPopSetParamsListStr = reduce (lambda LeftArg, RightArg: str(LeftArg) + ', ' + str(RightArg[0]), PreparedPopulationSet.DataColumns,'')[2:]
        WriteSimLine (Tab + Tab + '[' + AllPopSetParamsListStr  + '] = _PopulationSetInfo.Data[IndividualID-1]')

        WriteSimLine (Tab + Tab + '# Init parameters from Initialization Phase')
        WriteRules(0,2,SystemPrecisionForProbabilityBoundCheck)    

        WriteSimLine (Tab + Tab + '# Reset time and load first vector into results')
        WriteSimLine (Tab + Tab + 'Time = 0')

        WriteSimLine (Tab + Tab + '# Load the initial condition into the results vector for this individual')
        WriteSimLine (Tab + Tab + '_ResultsInfoForThisIndividual = [ [IndividualID, Repetition, Time ,' + AllParamsStr +'] ]' )
        
        # Determine if the individual is already at a terminal end state
        # to decide whether to perform simulation at all
        TerminationDeterminationString = 'False'
        for (StateKey , PriorityGroup , VarName, FuncName) in StateData:
            if PriorityGroup == 1:
                TerminationDeterminationString = TerminationDeterminationString + ' or ' + VarName + ' != 0'
        
        WriteSimLine (Tab + Tab + '_Terminate_Time_Loop = ' + TerminationDeterminationString)
        # Reset the number of times a certain simulation step is attempted
        WriteSimLine (Tab + Tab + '_NumberOfTriesToGenerateThisSimulationStep = 0')
        WriteSimLine (Tab + Tab + '_RepeatSameSimulationStep = False')

        WriteSimLine (Tab + Tab + '##### Time Loop #####')
        WriteSimLine (Tab + Tab + 'while Time < ' + str(self.NumberOfSimulationSteps) +':')
        WriteSimLine (Tab + Tab + Tab + 'if _RepeatSameSimulationStep:')
        WriteSimLine (Tab + Tab + Tab + Tab + '# if repeating the same simulation step, reset the flag to avoid infinite loops')
        WriteSimLine (Tab + Tab + Tab + Tab + '_RepeatSameSimulationStep = False')
        WriteSimLine (Tab + Tab + Tab + Tab + '# Load the previous time step results into the results vector for this individual')
        WriteSimLine (Tab + Tab + Tab + Tab + '[_IgnoreIndividualID, _IgnoreRepetition, _IgnoreTime ,' + AllParamsStr +'] = _ResultsInfoForThisIndividual[-1]' )
        # Reset termination. Note that it is ok to terminate regardless of
        # states since we are reloading previous conditions that initially 
        # allowed starting calculations
        WriteSimLine (Tab + Tab + Tab + Tab + '_Terminate_Time_Loop = False')
        WriteSimLine (Tab + Tab + Tab + 'elif _Terminate_Time_Loop:')
        WriteSimLine (Tab + Tab + Tab + Tab + '# If the time loop has to be terminated')
        WriteSimLine (Tab + Tab + Tab + Tab + 'break')
        WriteSimLine (Tab + Tab + Tab + 'else:')
        WriteSimLine (Tab + Tab + Tab + Tab + '# If not repeating the same simulation step, nor terminating, increase the time counter')
        WriteSimLine (Tab + Tab + Tab + Tab + 'Time = Time + 1')
        
        # At verbose level of 30 or more, display time steps
        WriteSimLine (Tab + Tab + Tab + '# Comment/Uncomment the next line to disable/enable printing of verbose information')
        WriteSimLine (Tab + Tab + Tab + Iif(VerboseLevel >= 30,'','#') + 'print "    Time Step = " + str(Time)')
        WriteSimLine (Tab + Tab + Tab + '# Reset Warning/Error Count')
        WriteSimLine (Tab + Tab + Tab + '_WarningCountBeforeThisSimulationStep = _WarningCount')
        WriteSimLine (Tab + Tab + Tab + '# Increase the number of Tries counter')
        WriteSimLine (Tab + Tab + Tab + '_NumberOfTriesToGenerateThisSimulationStep = _NumberOfTriesToGenerateThisSimulationStep + 1')

        WriteSimLine (Tab + Tab + Tab + '##### Phase 1 - Pre State Transition #####')

        WriteRules(1,3,SystemPrecisionForProbabilityBoundCheck)

        WriteSimLine (Tab + Tab + Tab + '##### Phase 2 - Complications Update #####')
        WriteSimLine (Tab + Tab + Tab + '# Reset all state indicators corresponding to entered states')
        EnteredStateIndicators = filter (lambda Item: '_Entered' in Item,ResultsInfo.DataColumns)
        LeftSideStr = str(EnteredStateIndicators).replace("', '",', ')[2:-2]
        RightSideStr = '0, '*(len(EnteredStateIndicators)-1)+ '0'
        WriteSimLine (Tab + Tab + Tab + LeftSideStr + ' = ' + RightSideStr)

        WriteSimLine (Tab + Tab + Tab + '# Reset all state indicators of sub processes that are not set')
        WriteSimLine (Tab + Tab + Tab + '# Distinguish between subprocesses and regular states')

        # Traverse the list of subprocesses, according to the order provided in
        # RelatedStateIDs, since this order will provide a pre-order traversal
        # order of the processes and their nested processes
        for StateID in RelatedStateIDs:
            StateEntry = RelatedStates[StateID]
            if StateEntry.IsSubProcess():
                SubProcessIndicators = StateEntry.GenerateAllStateIndicatorNames()
                # Reset parameters only for Actual and Entered states
                # the rest of the state indicators are user controlled
                for SuffixNumber in [0,1]:
                    SubProcessIndicator = SubProcessIndicators[SuffixNumber]
                    WriteSimLine (Tab + Tab + Tab +'if not ' + SubProcessIndicator + ':')
                    LeftSideStr , RightSideStr = '' , ''
                    for StateID in StateEntry.ChildStates:
                        StateIndicatorNames = RelatedStates[StateID].GenerateAllStateIndicatorNames()
                        StateIndicatorName = StateIndicatorNames[SuffixNumber]
                        LeftSideStr = LeftSideStr + StateIndicatorName + ', '
                        RightSideStr = RightSideStr + '0, '
                    LeftSideStr = LeftSideStr[:-2]
                    RightSideStr = RightSideStr[:-2]
                    WriteSimLine (Tab + Tab + Tab + Tab + LeftSideStr + ' = ' + RightSideStr)

        WriteSimLine (Tab + Tab + Tab +'# Main complications calculation engine')
        # Construct the state vector
        SortedStateDataForProcessing = filter( lambda (ID, Priority, VarName, FuncName): (Priority <= 5), SortedStateData)
        SortedStateDataForProcessingRelevantStr = str(map (lambda (ID, Priority, VarName, FuncName): VarName, SortedStateDataForProcessing))
        # Enumerate and filter the state vector to retain only state indices
        # that are set, then build the SPQ (State Processing Queue) by accessing
        # the State classification vector with the extracted indices
        WriteSimLine (Tab + Tab + Tab + '_StateVec = ' + SortedStateDataForProcessingRelevantStr.replace("'",''))
        WriteSimLine (Tab + Tab + Tab + '_ActiveStatesEnumerated = filter( lambda (_Index, _Entry): _Entry, enumerate (_StateVec))')
        WriteSimLine (Tab + Tab + Tab + '_ActiveStatesMapped = map (lambda (_Index, _Entry): _StateClassificationVec[_Index] , _ActiveStatesEnumerated)')

        # Add a small random number to the priority of the mapped list of
        # active states. This will allow sorting these to receive a random
        # order of states, while grouping states within priority groups and
        # Therefore defines the State Processing Queue (SPQ)
        WriteSimLine (Tab + Tab + Tab + '_ActiveStatesAndRandom = map (lambda (_ID, _Priority, _FuncName): (_ID, _Priority + DataDef.numpy.random.random(), _FuncName) , _ActiveStatesMapped)')
        WriteSimLine (Tab + Tab + Tab + '_SPQ = sorted ( _ActiveStatesAndRandom, None , key = lambda (_ID, _Priority, _FuncName): (_Priority,_ID))')
        WriteSimLine (Tab + Tab + Tab + '# Main processing loop of the SPQ')
        WriteSimLine (Tab + Tab + Tab + 'while _SPQ !=[] and not _Terminate_Time_Loop:')
        WriteSimLine (Tab + Tab + Tab + Tab + '# pop the state from the SPQ')
        WriteSimLine (Tab + Tab + Tab + Tab + '_StateToBeProcessed = _SPQ.pop(0)')
        WriteSimLine (Tab + Tab + Tab + Tab + '# Call the function that handles this state')
        WriteSimLine (Tab + Tab + Tab + Tab + '_StateToBeProcessed[2]()')
        # At verbose level of 4 or more, each state in the SPQ is displayed
        WriteSimLine (Tab + Tab + Tab + Tab + '# Comment/Uncomment the next line to disable/enable printing of verbose information')
        WriteSimLine (Tab + Tab + Tab + Tab + Iif(VerboseLevel >= 40,'','#') + 'print "      " + str(_StateToBeProcessed)')
        WriteSimLine (Tab + Tab + Tab + '##### Phase 3 - Post State Transition #####')
        WriteRules(3,3,SystemPrecisionForProbabilityBoundCheck)

        WriteSimLine (Tab + Tab + Tab + '##### End of Rule Processing #####')
        WriteSimLine (Tab + Tab + Tab + '##### Error Handlers #####')

        # Check that no errors were generated before this TimeStep 
        # If none happened then it is ok to keep this data. otherwise
        # repeat the loop without increasing the individual count
        WriteSimLine (Tab + Tab + Tab + 'if _WarningCount <= _WarningCountBeforeThisSimulationStep:')
        WriteSimLine (Tab + Tab + Tab + Tab + '# Load New results to the results vector')
        WriteSimLine (Tab + Tab + Tab + Tab + '_ResultsInfoForThisIndividual.append([IndividualID, Repetition, Time ,' + AllParamsStr +'])')
        WriteSimLine (Tab + Tab + Tab + Tab + '_NumberOfTriesToGenerateThisSimulationStep = 0')
        WriteSimLine (Tab + Tab + Tab + 'else:')
        WriteSimLine (Tab + Tab + Tab + Tab + Iif(VerboseLevel >= 30,'','#') + 'print "    Repeating the same simulation step due to an error - probably a bad validity check"') 
        WriteSimLine (Tab + Tab + Tab + Tab + '_RepeatSameSimulationStep = True')
        WriteSimLine (Tab + Tab + Tab + Tab + 'if _NumberOfTriesToGenerateThisSimulationStep >= ' + SmartStr(NumberOfTriesToRecalculateSimulationStep) + ':')
        # Handle the situation where there is a need to recalculate the entire
        # individual after several simulation steps have created errors
        # check if this requires full recalculation or stopping the simulation
        WriteSimLine (Tab + Tab + Tab + Tab + Tab + 'if _NumberOfTriesToGenerateThisIndividual < ' + SmartStr(NumberOfTriesToRecalculateSimulationOfIndividualFromStart) + ':')
        # Handle the case where the program repeats calculation for this person
        WriteSimLine (Tab + Tab + Tab + Tab + Tab + Tab + '# Repeat the calculations for this person')
        WriteSimLine (Tab + Tab + Tab + Tab + Tab + Tab + '_RepeatSameIndividualRepetition = True ')
        WriteSimLine (Tab + Tab + Tab + Tab + Tab + Tab + 'break')
        WriteSimLine (Tab + Tab + Tab + Tab + Tab + 'else:')
        # Handle the case where the program should raise a fatal error due to
        # too many tries to fully process the same person
        WriteSimLine (Tab + Tab + Tab + Tab + Tab + Tab + '_WarningErrorHandler(_InputErrorString = "The simulation was halted since the number of tries to recalculate the same person has been exceeded. If this problem consistently repeats itself, check the formulas to see if these cause too many out of bounds numbers to be generated. Alternatively, try raising the system option NumberOfTriesToRecalculateSimulationOfIndividualFromStart which is now defined as ' + SmartStr(NumberOfTriesToRecalculateSimulationOfIndividualFromStart) + '  .  ", _FatalError = True)')

        # Now check if we are repeating the same person or storing
        # the calculated results
        WriteSimLine (Tab + Tab + 'if _RepeatSameIndividualRepetition:')
        WriteSimLine (Tab + Tab + Tab + Iif(VerboseLevel >= 20,'','#') + 'print "  Repeating the same repetition for the same individual due to exceeding the allowed number of simulation steps recalculations for this individual"')
        WriteSimLine (Tab + Tab + Tab + '_NumberOfTriesToGenerateThisIndividual = _NumberOfTriesToGenerateThisIndividual + 1')
        WriteSimLine (Tab + Tab + 'else:')
        WriteSimLine (Tab + Tab + Tab + '# If going to the next individual repetition, save the results and increase the counter')
        WriteSimLine (Tab + Tab + Tab + '# Load New results to the results vector')
        WriteSimLine (Tab + Tab + Tab + '_ResultsInfo.Data.extend(_ResultsInfoForThisIndividual)')
        WriteSimLine (Tab + Tab + Tab + 'Repetition = Repetition + 1')       

        # Deal with the next subject
        WriteSimLine (Tab + '_Subject = _Subject + 1')

        # write the result to file
        WriteSimLine ('# Comment/Uncomment the next lines to disable/enable dumping output file')
        VerboseComment = Iif(VerboseLevel >= 7,'','#')
        WriteSimLine (VerboseComment +'try:')
        WriteSimLine (VerboseComment + Tab + "# Output the results to a file")
        WriteSimLine (VerboseComment + Tab + '(_OutputFileDescriptor, _OutputFileName) = tempfile.mkstemp ( ' + repr(TextSuffix) + ' , ' + repr(OutputFileNamePrefix) + ' , ' + repr(SessionTempDirecory) + ', True)')
        WriteSimLine (VerboseComment + Tab + "_OutFile = os.fdopen (_OutputFileDescriptor , 'w')")
        WriteSimLine (VerboseComment + Tab + 'pickle.dump(_ResultsInfo.Data, _OutFile)')
        WriteSimLine (VerboseComment + Tab + "_OutFile.close()")
        WriteSimLine (VerboseComment + 'except:')
        if SkipDumpingFilesIfError:
            WriteSimLine (VerboseComment + Tab + "print 'Warning - could not write results to file'")
        else:
            WriteSimLine (VerboseComment + Tab + "_WarningErrorHandler()")
        WriteSimLine ('# Comment/Uncomment the next line to disable/enable printing of verbose information')
        WriteSimLine (Iif(VerboseLevel >= 10,'','#') + "print 'Info: population set generation was successful. A total number of ' + str(_WarningCount) + ' warnings were raised.'")
        # Record TraceBack data
        WriteSimLine ('_ResultsInfo.TraceBack = (' + str(self.ID) + ' , _GeneratingVersion , _InitialRandomState , os.path.split(_RandomStateFileName)[1] , os.path.split(__file__)[1] , _CompileArguments, _PopulationTraceBack )')

        try:
            SimFile.close()
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Simulation Compilation Error: Error encountered while closing simulation script file ' + ScriptFileNameFullPath  +'. Please make sure that the file was not locked by the system due to quota or other reasons. The error was detected for the project ' + self.Name + '. Here are details about the error: ' + str(ExceptValue)
        

        return ScriptFileNameFullPath


    def RunSimulationSpawned (self, SimulationFileName, DumpOutputAsCSV = False, FullResultsOutputFileName = None, FinalResultsOutputFileName = None, OutputConnection = None, DeleteScriptFileAfterRun = True):
        """ Runs the simulation """
        if FullResultsOutputFileName == None:
            FullResultsOutputFileName = DefaultFullResultsOutputFileName
        if FinalResultsOutputFileName == None:
            FinalResultsOutputFileName = DefaultFinalResultsOutputFileName
        # Determine the file names
        (ScriptPathOnly, ScriptFileNameOnly, ScriptFileNameFullPath) = DetermineFileNameAndPath(SimulationFileName)
        (ScriptFileNameNoExtension , ScriptFileNameOnlyExtension ) = os.path.splitext(ScriptFileNameOnly)
        if ScriptFileNameOnlyExtension.lower() not in ['.py', 'py']:
            raise ValueError, 'Simulation Execution Error: The simulation file name ' + ScriptFileNameFullPath + ' does not have a python extension of "py"'
        # Make sure the module is in the system path. First save the current
        # system path and then change it
        OldSysPath = sys.path
        # Insert the new path at the beginning of the search list so that
        # the correct file will be run in case of duplicate filenames in
        # different directories.
        sys.path.insert(0,ScriptPathOnly)
        # Now try running the simulation - enclose this in a try catch clause
        try:
            # Remove previous definition
            RunSimulationScript = None
            # Run the simulation
            RunSimulationScript = __import__(ScriptFileNameNoExtension)
            # If file output is specified, output the files
            if DumpOutputAsCSV:
                if FullResultsOutputFileName != '':
                    RunSimulationScript._ResultsInfo.ExportAsCSV(FullResultsOutputFileName)
                if FinalResultsOutputFileName != '':
                    FinalData = RunSimulationScript._ResultsInfo.ExtractFinalOutcome()
                    RunSimulationScript._ResultsInfo.ExportAsCSV(FinalResultsOutputFileName,FinalData)
            # remove the module from sys.modules to force reload later on
            ResultsInfo = RunSimulationScript._ResultsInfo
            del(sys.modules[ScriptFileNameNoExtension])
            # if Requested, delete the .py and .pyc script files
            if DeleteScriptFileAfterRun:
                # in case of an error before here- the file will not be 
                # deleted, so it would be possible to debug 
                try:
                    os.remove(ScriptFileNameFullPath)
                    os.remove(ScriptFileNameFullPath+'c')
                except:
                    # ignore delete error if happens - the file will be left
                    # in the temp dir - no harm donw
                    pass
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            if ScriptFileNameNoExtension in sys.modules:
                del(sys.modules[ScriptFileNameNoExtension])
            ErrorText = 'Simulation Execution Error: An error was encountered while running the simulation script file ' + ScriptFileNameFullPath + ' . Here are details about the error: ' + str(ExceptValue)
            # If a connection pipe was provided, use it to report the error
            if OutputConnection != None:
                OutputConnection.send(ErrorText)
                ResultsInfo = ErrorText
            else:
                #if no connection was provided, report the error
                raise ValueError, ErrorText
        # Reconstruct the system path
        sys.path = OldSysPath
        # If a connection pipe was provided, use it to report output
        if OutputConnection != None:
            OutputConnection.send(ResultsInfo)
        return ResultsInfo


    def RunSimulation (self, SimulationFileName, NumberOfProcessesToRun = 0, DumpOutputAsCSV = False, FullResultsOutputFileName = None, FinalResultsOutputFileName = None, DeleteScriptFileAfterRun = True):
        """ Runs the simulation if possible/requested as a different process """
        # if NumberOfProcessesToRun = 0, this means run the simulation 
        # without opening a new process, i.e. within this process.
        # if NumberOfProcessesToRun is a positive number, then run this 
        # exact number of processes.
        # if the number is negative, then run this -number of simulations
        # in parallel as processes if the system supports multiple processes
        # otherwise, run them serially without opening a new process. 
        # The return value of the function will be the following tuple 
        # (ProcessList, PipeList). ProcessList is empty if no processes were
        # created. PipeList contains a list of pipe or pipe like objects that 
        # contain the simulation results. The caller is responsible to 
        # call CollectSimulationResults on their own to collect the results.
        if SystemSupportsProcesses and NumberOfProcessesToRun > 0:
            raise ValueError, 'ASSERTION ERROR: The system does not support multiprocess in python, yet multiple processes were forced in input parameters to RunSimulation'
        if NumberOfProcessesToRun == 0:
            ProcessEnums = [0]
        else:
            ProcessEnums = range(abs(NumberOfProcessesToRun))
        PipeList = []
        ProcessList = []
        if NumberOfProcessesToRun == 0 or (not SystemSupportsProcesses and NumberOfProcessesToRun <0):
            # Handle the serial executions case 
            for ProcessEnum in ProcessEnums:
                OutputConnection = PipeMock()
                if 'MultiProcess' in DebugPrints:
                    print 'running the file ' + SimulationFileName
                self.RunSimulationSpawned (SimulationFileName, DumpOutputAsCSV, FullResultsOutputFileName, FinalResultsOutputFileName, OutputConnection, DeleteScriptFileAfterRun)
                if 'MultiProcess' in DebugPrints:
                    print 'finished running the file ' + SimulationFileName
                # store the result, errors will be handled later
                PipeList = PipeList + [OutputConnection]
        else:
            # Handle the parallel process execution case
            for ProcessEnum in ProcessEnums:
                # create connections
                (ParentConnenction, ChildConnection) = multiprocessing.Pipe()
                PipeList = PipeList + [ParentConnenction]
                # create processes
                if 'MultiProcess' in DebugPrints:
                    print 'spawning a process for file ' + SimulationFileName
                TheProcess = multiprocessing.Process(target = self.RunSimulationSpawned, args = (SimulationFileName, DumpOutputAsCSV, FullResultsOutputFileName, FinalResultsOutputFileName, ChildConnection, DeleteScriptFileAfterRun))
                ProcessList = ProcessList + [TheProcess]
                if 'MultiProcess' in DebugPrints:
                    print 'process spawned'
                # Now actually start running the process
                TheProcess.start()
        # return the Process and pipe list to be collected by CollectResults
        return (ProcessList, PipeList)

    def CollectResults(self,ProcessList,ConnectionList): 
        """Collects results from RunSimulation spawned simulations """
        # If only one simulation was run, return the results vector. Otherwise,
        # in case of multiple simulations, return a list with one entry for
        # each result. An error text will be returned in case of an error in 
        # the position corresponding to an unsuccesful run. Also in case of
        # an error in simulation, this error will be raised. Where multiple
        # errors will be reported together in one error message.
        ResultsInfoList = []
        NumberOfResults = len(ConnectionList)
        ProcessEnums = range(NumberOfResults)
        # first collect all data from all processes. This will make the system
        # wait for all processes to finish 
        for ProcessEnum in ProcessEnums:
            ResultsInfo = ConnectionList[ProcessEnum].recv()
            ResultsInfoList = ResultsInfoList + [ResultsInfo]
        # Now if these results are from actual processes, then join them
        if ProcessList != []:
            for ProcessEnum in ProcessEnums:
                ProcessList[ProcessEnum].join()
        # Check if there were any errors
        FullErrorString = ''
        for ProcessEnum in ProcessEnums:
            ResultsInfo = ResultsInfoList[ProcessEnum]
            if IsStr(ResultsInfo):
                # if an error was detected, report it
                FullErrorString = FullErrorString + 'Simulation Execution Error in Process #' + str(ProcessEnum+1) + ' from ' + str(NumberOfResults) + ' : ' + ResultsInfo + '\n'
            else:
                # if no error was detected, then try to store the results
                try:
                    SimulationResults.AddNew(ResultsInfo) 
                except:
                    (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                    FullErrorString = FullErrorString + 'Simulation Result Collection Error in Process #' + str(ProcessEnum+1) + ' from ' + str(NumberOfResults) + ' : Could not store results. Here are additional details about the error: ' + str(ExceptValue) + '\n'
        if FullErrorString != '':
            # if there were any errors, raise them
            raise ValueError, FullErrorString
        # if there is only one result set strip the list
        if NumberOfResults == 1:
            RetVal = ResultsInfoList[0]
        else:
            RetVal = ResultsInfoList
        return RetVal


    def RunSimulationAndCollectResults (self, SimulationFileName, NumberOfProcessesToRun = 0, DumpOutputAsCSV = False, FullResultsOutputFileName = None, FinalResultsOutputFileName = None, DeleteScriptFileAfterRun = True):
        """ Runs the simulation and collects the results and returns them """
        # this function combines RunSimulation and CollectResults
        (ProcessList, PipeList) = self.RunSimulation (SimulationFileName, NumberOfProcessesToRun , DumpOutputAsCSV , FullResultsOutputFileName , FinalResultsOutputFileName, DeleteScriptFileAfterRun)
        RetVal = self.CollectResults(ProcessList, PipeList)
        return RetVal




    def IsLocked(self):
        """ Checks if the project is locked """
        # A project is locked if there are simulation results for it or if this
        # an estimation project that another simulation project is derived from
        # The Function will return the locked Entity if it is locked
        ResultFlag = reduce(lambda Accumulator, Entry: Accumulator or Entry.ProjectID==self.ID, SimulationResults.values(), False)
        # Return the result according to the flag
        if ResultFlag:
            Result = [self]            
        else:
            Result = []  
        return Result

    def CheckDependencies(self, CheckForModify = False, ProjectBypassID = 0):
        """ Verifies no dependant data exists """
        # For projects, only locked projects will not allow modification
        LockingList = self.IsLocked()
        if LockingList!=[]:
            raise ValueError, 'Project Dependency Error: The project cannot be deleted or modified as there are already results created for it. To allow project modification, delete all results related to it. For a simulation project delete all simulation results generated from it. Locking projects are: ' + EntityNameByID(LockingList,None)
        # Note that modifying projects that other project have been derived from
        # is allowed unless blocked above as the deletion routine handles this.
        return

    def IsParamDependant(self, ParamName):
        """ Returns True if dependant on ParamName """
        Result = ParamName in self.FindDependantParams(ParamType = None)
        return Result

    def FindDependantParams(self, ParamType = None):
        """ Find the dependant parameters """
        Result = []
        Result = Result + reduce(SumOp,map(lambda Entry: Entry.FindDependantParams(),self.SimulationRules),[])
        if self.PrimaryModelID != 0:
            Result = Result + StudyModels[self.PrimaryModelID].FindDependantParams()
        if self.PrimaryPopulationSetID != 0:
            Result = Result + PopulationSets[self.PrimaryPopulationSetID].FindDependantParams()
        for SimulationRule in self.SimulationRules:
            Result = Result + SimulationRule.FindDependantParams()
        # If a datatype is specified filter the results by the data type
        if ParamType != None:
            Result = filter(lambda Entry: Params[Entry].ParameterType == ParamType, Result)
        return Result
    

    def GenerateReport(self, FormatOptions = None):
        """ Generate the report for this entity instance """
        TotalIndent = HandleOption('TotalIndent', FormatOptions,'')
        IndentAtom = HandleOption('IndentAtom', FormatOptions,'  ')
        #ColumnSpacing = HandleOption('ColumnSpacing', FormatOptions,' | ')
        FieldHeader = HandleOption('FieldHeader', FormatOptions,True)
        LineDelimiter = HandleOption('LineDelimiter', FormatOptions,'\n')
        SectionSeparator = HandleOption('SectionSeparator', FormatOptions,70*'_')
        ShowHidden = HandleOption('ShowHidden', FormatOptions,False)
        #ShowDependency = HandleOption('ShowDependency', FormatOptions,False)
        DetailLevel = HandleOption('DetailLevel', FormatOptions, 0)
            
        # DetailLevel = 0 means only summary project information
        # DetailLevel = 1 means going into details
        ReportString = ''
        if ShowHidden:
            ReportString = ReportString + TotalIndent + FieldHeader * 'ID: ' + str(self.ID) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Project Name: ' + str(self.Name) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Notes: ' + str(self.Notes).replace('\n','\n'+TotalIndent) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Created On: ' + str(self.CreatedOn) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Last Modified: ' + str(self.LastModified) + LineDelimiter
        if self.DerivedFrom != 0:
            DerivedProjectName = Projects[self.DerivedFrom].Name
            ReportString = ReportString + TotalIndent + FieldHeader * 'Derived From the Project: ' + str(DerivedProjectName) + LineDelimiter
        RevisedFormatOptions = HandleOption('TotalIndent', FormatOptions, TotalIndent + IndentAtom, True)
        RevisedFormatOptions = HandleOption('DetailLevel', RevisedFormatOptions, DetailLevel-1, True)        
        # Report for a simulation project 
        ReportString = ReportString + TotalIndent + FieldHeader * 'This is a Simulation Project with the Following Parameters: ' + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Number of Time Steps: ' + str(self.NumberOfSimulationSteps) + LineDelimiter
        ReportString = ReportString + TotalIndent + FieldHeader * 'Number of Repetitions: ' + str(self.NumberOfRepetitions ) + LineDelimiter
        if DetailLevel == 0:
            # Summary information
            ReportString = ReportString + TotalIndent + FieldHeader * 'The Primary Model Used is: ' + StudyModels[self.PrimaryModelID].Name + LineDelimiter
            ReportString = ReportString + TotalIndent + FieldHeader * 'The Population Set is: ' + PopulationSets[self.PrimaryPopulationSetID].Name + LineDelimiter
            ReportString = ReportString + TotalIndent + FieldHeader * 'Total number of rules is: ' + str(len(self.SimulationRules)) + LineDelimiter                
        else:
            # Detailed information
            ReportString = ReportString + TotalIndent + FieldHeader * 'The Primary Model Used is: ' + LineDelimiter
            ReportString = ReportString + StudyModels[self.PrimaryModelID].GenerateReport(RevisedFormatOptions)
            ReportString = ReportString + TotalIndent + FieldHeader * 'The Population Set is: ' + LineDelimiter
            ReportString = ReportString + PopulationSets[self.PrimaryPopulationSetID].GenerateReport(RevisedFormatOptions)
            for (PhaseNum, PhaseTitle) in [(0,'Initialization Rules:'), (1,'Pre state transition Rules:'), (3,'Post state transition Rules:')]:
                ReportString = ReportString + TotalIndent + FieldHeader * PhaseTitle + LineDelimiter
                for Rule in self.SimulationRules:
                    if (Rule.SimulationPhase == PhaseNum):
                        ReportString = ReportString + Rule.GenerateReport(RevisedFormatOptions)
            if self.IsLocked() != []:
                ReportString = ReportString + TotalIndent + FieldHeader * 'This Project Contains Results' + LineDelimiter
            ReportString = ReportString + TotalIndent + FieldHeader * 'The following parameters are used by the project: ' + LineDelimiter
            ParameterListWithFunctions = list(set(self.FindDependantParams()))
            ParameterList = filter (lambda Entry: Entry not in ExpressionSupportedFunctionsAndSpecialNames, ParameterListWithFunctions)
            for ParamName in sorted(ParameterList):
                ReportString = ReportString + Params[ParamName].GenerateReport(RevisedFormatOptions)
        ReportString = ReportString + TotalIndent + SectionSeparator + LineDelimiter
        return ReportString

    def Copy(self, NewName = None):
        """ Returns an object that copies this one """
        NewName = CalcCopyName(self, NewName)
        NewRecord = Project(ID = 0, Name = NewName , Notes = self.Notes, PrimaryModelID = self.PrimaryModelID  , PrimaryPopulationSetID = self.PrimaryPopulationSetID , NumberOfSimulationSteps = self.NumberOfSimulationSteps  , NumberOfRepetitions = self.NumberOfRepetitions  , SimulationRules = self.SimulationRules, DerivedFrom = self.ID)
        return NewRecord

    # Description String
    Describe = DescribeReturnsName


    def CreateNewDefaultPopulationSetForProject(self):
        """ Creates a default population set for the project """
        # The newly created population set will have only a single parameter
        # that corresponds to the first state indicator in the process and
        # it will be set to 1. There will be only a single data record in this
        # data based population set. The newly created record will not be added
        # to the PopulationSets collection - this is a responsibility of the
        # caller.
        ModelID = self.ReturnEstimationModelID()
        NewName = CalcCopyName(Object = 'PopulationSets', BaseName = 'Default Population set for the estimation project: "' + self.Describe() + '"')
        ModelStates = StudyModels[ModelID].FindStatesInStudyModel()
        # after extracting model states, make sure that the first state
        # is a valid state
        FirstStateID = ModelStates[0]
        FirstState = States[FirstStateID]
        if FirstState.IsSplit or FirstState.JoinerOfSplitter!=0 or FirstState.ChildStates != []:
            raise ValueError, 'ASSERTION ERROR: The first state in the model is not a regular state or an event state'
        StateIndicator = FirstState.GenerateAllStateIndicatorNames()[0]
        NewPopulationSet = PopulationSet( Name = NewName, Source = 'Automatically Generated', Notes = 'Default Population Set that was automatically generated for an estimation project', DerivedFrom = 0, DataColumns = [(StateIndicator,'')], Data = [[1]], Objectives = [])
        return NewPopulationSet

        

class SimulationResult:
    """Defines a class for storing simulation results"""
    ID = 0        # A unique identifier for simulation results set
    ProjectID = 0 # Link to the project ID from which the simulation was run
    CreatedOn = InitTime     # The time this entity was created on
    DataColumns = [] # Holds the list of parameters evaluated in the simulation
                     # sort order is important and defines the results order
                     # The parameters should be defined as IndividualID,
                     # Repetition, Time
    Data = []   # A 2D array created from nested sequences. It holds each 
                # Individual record in the internal sequence. The internal
                # sequence holds data for the parameters in the same order
                # These are defined in DataColumns
    TraceBack = () # Traceability data is a tuple with information that
                   # allows tracing back the simulation to support
                   # reproducibility. This is a hidden entity for debug
                   # purposes. The Tuple includes the following elements:
                   # DerivedFrom: ID of generating project
                   # GeneratingVersion: DataDef version of the generating code
                   # InitialRandomState: Random state at simulation start
                   # RandomStateFileName: Temp file with random state
                   # TemporaryScriptFile: Temp script generating results
                   # CompileArguments: Arguments passed at compile time
                   # PopuationTraceBack: population TraceBaack Tuple if exists
                   # This TraceBack information is true for the moment of 
                   # creation if iformation was modified afterwards, then this
                   # TraceBack is removed since it is no longer informative. 
                   # Note that this internal Tag can only be set internally by
                   # the system - this happens only after simulation results
                   # are returned and not at init. A report can output this 
                   # information if Hidden information is requested.
                   # Note that TraceBack information is lost if data is 
                   # recreated by recontructing a database or modified. Yet
                   # since version information is also recorded it leaves open
                   # the possibility to reconstruct this information in future 
                   # versions of MIST. This, however, is not guaranteed since
                   # future versions may change the code in a way that
                   # reproducibility will not be feasible - yet reproducibility
                   # should be possible with the original version of the data 
                   # definitions. 
                    
                            

    def __init__(self, ProjectID , PreparedPopulationSet = None , ID = 0, Data = None):
        """Constructor with default values and some consistency checks"""
        self.ID = ID
        self.ProjectID = ProjectID
        self.CreatedOn = datetime.datetime.now()
        # Construct the set of parameters by combining the parameters in the
        # population set with state indicators held in the model and with
        # affected parameters stated in the project
        DataColumns = []
        if not Projects.has_key(ProjectID):
            raise ValueError, 'ASSERTION ERROR: Cannot create results object for the Project ' + Projects.ID2Name(ProjectID) + ' since the project does not exist in the projects list or is not a simulation project'
        PrimaryModelID = Projects[ProjectID].PrimaryModelID
        PrimaryPopulationSetID = Projects[ProjectID].PrimaryPopulationSetID
        if not StudyModels.has_key(PrimaryModelID):
            raise ValueError, 'ASSERTION ERROR: Cannot create results object for Project #' + str(ProjectID) + ' since the model with Model ID #' + str(PrimaryModelID) + ' stated in the project cannot be found or it is a study'
        if not PopulationSets.has_key(PrimaryPopulationSetID):
            raise ValueError, 'ASSERTION ERROR: Cannot create results object for Project #' + str(ProjectID) + ' since the population set with ID #' + str(PrimaryPopulationSetID) + ' stated in the project cannot be found'
        # If the population set has not been prepared for simulation, then
        # prepare it now. Ideally this should not be the case. This option
        # is provided for debug and possible future need
        if PreparedPopulationSet == None:
            PreparedPopulationSet = PopulationSets[PrimaryPopulationSetID].PreparePopulationSetForSimulation(PrimaryModelID)
        # Copy all parameters from the parameter list of the population set
        PopSetColumns = map(lambda (ParamName, Distribution): ParamName , PreparedPopulationSet.DataColumns )
        # Create a list of affected parameters
        AffectedParameters = map( lambda Item: str(Item.AffectedParam) , Projects[ProjectID].SimulationRules)
        # Remove duplicates from the state indicators and sort parameters
        AffectedParameters = sorted(SetDiff(AffectedParameters, PopSetColumns))
        # Add the PopulationSetColumns First since these are the base
        DataColumns = PopSetColumns + AffectedParameters
        # Add IndividualID, Repetition, and Time parameters to the
        # list, raising an error if these exist as this means these were
        # defined in a population set or a state before and may contain data
        HeaderColumns = ['IndividualID', 'Repetition' , 'Time'] 
        for Item in HeaderColumns:
            if Item in DataColumns:
                raise ValueError, 'ASSERTION ERROR: The parameter "'+ Item +'" exists as a state or as a parameter in the population set in project #'+ str(ProjectID) + ' and therefore creates a conflict for results'
        DataColumns = HeaderColumns + DataColumns
        # Copy to self and init data to no data
        self.DataColumns = DataColumns
        if Data == None:
            self.Data = []
        else:
            self.Data = Data
        self.TraceBack = ()
        return

    def ExportAsCSV(self, FileName, DataToExport = None, ExportTitles = True):
        """ Exports the data to a file in a Comma Separated Values format """
        # If no data is specified, export the entire data in self
        if DataToExport == None:
            DataToExport = self.Data
        if ExportTitles:
            TitleLine = self.DataColumns
        else:
            TitleLine = None
        # Determine the filename and path
        (PathOnly , FileNameOnly, FileNameFullPath) = DetermineFileNameAndPath(FileName)
        ExportDataToCSV(FileName, DataToExport, TitleLine)
        return

    def ExtractFinalOutcome(self):
        """ Extracts the final record of each repetition for each individual """
        ExtractedFinalOutcomeData = []
        PreviousDataRecord = self.Data[0]
        # Traverse records and when the previous and the current records have
        # a different IndividualID and repetition numbers than this means that
        # the previous record was a final outcome of the repetition
        for DataRecord in self.Data:
            if PreviousDataRecord [0:2] != DataRecord [0:2]:
                ExtractedFinalOutcomeData = ExtractedFinalOutcomeData + [PreviousDataRecord]
            PreviousDataRecord = DataRecord
        # Also, the last record is always a final outcome
        ExtractedFinalOutcomeData = ExtractedFinalOutcomeData + [PreviousDataRecord]
        return ExtractedFinalOutcomeData

    def CheckDependencies(self, CheckForModify = False, ProjectBypassID = 0):
        """ Verifies no dependant data exists """
        # No special processing for simulation results
        return

    def IsParamDependant(self, ParamName):
        """ Returns True if dependant on ParamName """
        # Note that this method is deprecated and may be removed in the future
        Result = ParamName in self.FindDependantParams(ParamType = None)
        return Result

    def FindDependantParams(self, ParamType = None):
        """ Find the dependant parameters """
        # Note that this method is deprecated and may be removed in the future
        Result = self.DataColumns
        # If a datatype is specified filter the results by the data type
        if ParamType != None:
            Result = filter(lambda Entry: Params[Entry].ParameterType == ParamType, Result)
        return Result


    def ResolveColumnAttributesForReport (self, ColumnFilter):
        """Resolve column calculation methods as well as data"""
        # First several helper functions
        def ResolveCalculationMethod(self, ParamName, CalculationMethod):
            "Return the calculation method of a parameter"
            if CalculationMethod != 'Auto Detect':
                Result = CalculationMethod
            elif ParamName not in Params.keys():
                raise ValueError, 'ASSERTION ERROR - Unknown parameter when auto detecting calculation method'
            else:
                ParameterType = Params[ParamName].ParameterType
                # Reset calculation for all types that are in to interest
                if ParameterType not in ['Number','Integer','State Indicator']:
                    Result = 'No Summary'
                else:    
                    ValidationRuleParams = Params[ParamName].ValidationRuleParams
                    # Find the affected parameters:
                    AffectedParams = map(lambda Entry: Entry.AffectedParam ,Projects[self.ProjectID].SimulationRules)
                    ParameterMayChangeDuringSimulation = (ParameterType == 'State Indicator') or (ParamName in AffectedParams)
                    if (ParameterType == 'Integer' and ValidationRuleParams.strip() != '' and eval(ValidationRuleParams, EmptyEvalDict) != [0,1]) or (ParameterType == 'State Indicator'):
                        # In the case of Boolean parameters
                        if ParameterMayChangeDuringSimulation:
                            Result = 'Sum Over All Records'
                        else:
                            Result = 'Sum Over Demographics'
                    else:
                        # Take care of the case of System Reserved Parameters
                        # In the case of non-Boolean parameters
                        if ParameterMayChangeDuringSimulation:
                            Result = 'Average Over All Records'
                        else:
                            Result = 'Average Over Demographics'
            return Result                                        


        DataColumnsWithBlank = self.DataColumns + ['BlankColumn']
        BlankColumnIndex = len(DataColumnsWithBlank) - 1
        # Create The Column List to Show:
        if ColumnFilter == []:
            ColumnFilterToUse = map ( lambda Entry: (Entry,'Auto Detect',''), ['<Header>'] + self.DataColumns )
        else:
            ColumnFilterToUse = ColumnFilter
        # Initialize the appropriate columns
        DataColumnsIndicesToShow = []
        #OriginalRequestColumnIndices = []
        ColumnTitles = []
        CalculationMethods = []
        OriginalCalculationMethods = []
        for (OriginalRequestColumnIndex,(ColumnToShow,CalculationMethod,ColumnTitle)) in enumerate(ColumnFilterToUse):
            if ColumnToShow == '<Header>':
                # If this is the header, then create 4 blank columns
                # indexed as the first column
                DataColumnsIndicesToShow = DataColumnsIndicesToShow + [BlankColumnIndex]*4
                ColumnTitles = ColumnTitles + ['']*4
                CalculationMethods = CalculationMethods + [ 'Interval Start', 'Interval End', 'Record Count', 'Demographic Count' ]
                OriginalCalculationMethods = OriginalCalculationMethods + [CalculationMethod]*4
            else:
                for ColumnNum in range(BlankColumnIndex):
                    ParamName = DataColumnsWithBlank[ColumnNum] 
                    if ColumnToShow[0] == '<' and ColumnToShow[-1] == '>':
                        # In the case this is a parameter group that is enclosed
                        # with < and > characters
                        ParameterTypeToShow = ColumnToShow[1:-1].strip()
                        # Create default complimentary rules
                        IncludeRule0 = Params[ParamName].ParameterType == ParameterTypeToShow
                        IncludeRule1 = True
                        IncludeRule2 = True
                        if ParameterTypeToShow.startswith('State Indicator'):
                            Specifications = ParameterTypeToShow.split(',')
                            if len(Specifications)>1:
                                # update the basic rule since the parameter type
                                # carries additional information in the string
                                IncludeRule0 = Params[ParamName].ParameterType == Specifications[0]
                                if IncludeRule0:
                                    if Specifications[1].startswith('Sub-Process'):
                                        # Only subprocesses
                                        IncludeRule1 = States[Params[ParamName].Tags].IsSubProcess()
                                    elif Specifications[1].startswith('State'):
                                        # Only non sub processes
                                        IncludeRule1 = not States[Params[ParamName].Tags].IsSubProcess()
                                    else:
                                        raise ValueError, 'ASSERTION ERROR: State indicator specification not valid'
                                    SecondarySpecStartIndex = Specifications[1].rfind('_')
                                    if SecondarySpecStartIndex != -1:
                                        SecondarySepcification = Specifications[1][SecondarySpecStartIndex:]
                                        if SecondarySepcification == '_Actual':
                                            # For actual states, make sure that
                                            # the state name is the same
                                            # as the state indicator name
                                            IncludeRule2 = ParamName == States[Params[ParamName].Tags].GenerateAllStateIndicatorNames()[0]
                                        else:
                                            # For Entered, Diagnosed, Treated,
                                            # and Complied extensions
                                            IncludeRule2 = ParamName.endswith(SecondarySepcification)
                        if IncludeRule0 and IncludeRule1 and IncludeRule2:
                            DataColumnsIndicesToShow = DataColumnsIndicesToShow + [ColumnNum]
                            ColumnTitles = ColumnTitles + [Iif (ColumnTitle == '', ParamName, ColumnTitle )]
                            CalculationMethods = CalculationMethods + [ResolveCalculationMethod(self,ParamName,CalculationMethod)]
                            OriginalCalculationMethods = OriginalCalculationMethods + [CalculationMethod]
                    else:
                        # In the case a specific parameter is mentioned
                        if ParamName == ColumnToShow:
                            DataColumnsIndicesToShow = DataColumnsIndicesToShow + [ColumnNum]
                            ColumnTitles = ColumnTitles + [Iif (ColumnTitle == '', ParamName, ColumnTitle )]
                            CalculationMethods = CalculationMethods + [ResolveCalculationMethod(self,ParamName,CalculationMethod)]
                            OriginalCalculationMethods = OriginalCalculationMethods + [CalculationMethod]
        # Update column Titles with a * to mark a warning to the user
        TitleSuffixList = [''] * len(ColumnTitles)
        CalculationTitlesPerColumns = map(lambda Entry, Suffix: ReportCalculationMethodShortTitles[ReportCalculationMethods.index(Entry)]+ Suffix, CalculationMethods, TitleSuffixList)
        return (DataColumnsIndicesToShow, ColumnTitles, CalculationMethods, OriginalCalculationMethods, DataColumnsWithBlank, BlankColumnIndex, CalculationTitlesPerColumns)

    def CalculateSummary(self, TimeRange, StratificationParameters, DataColumnsIndicesToShow, CalculationMethods, MaxTime, InitializationValues = None, UseOnlyPreviousResults = False):
        """ Calculates summary statistics for all columns """
        # Calculate the summary for the specified TimeRange and the
        # StratificationParameters = [StratifyIndex , StratifyMaxCount,
        #                          StratificationColumnIndices , StratifyBy].
        # Calculate for the columns defined in DataColumnsIndicesToShow.
        # if InitializationValues is defined, then calculations use these
        # for initializing sums and counts that were previously calculated.
        # Only the requested calculation in CalculationMethods will be
        # performed. Below is a list of calculations:
        # - {Func} Over All Records - will apply (Func} to values from all the
        #   records in the summary interval. When {Func}=Sum, then this is the
        #   default option for Booleans that are not demographics, e.g.
        #   State indicators. When {Func}=Average, It is equivalent to dividing
        #   the sum over all records by the total number of all records in
        #   the interval. This is the default option for non-Booleans that
        #   are not demographics, i.e. may be affected during the
        #   simulation. When {Func} = STD, sample standard deviation is
        #   calculated using the method of provisional means. When {Func} = Min
        #   or when {Func} = Max then the minimal or maximal value of all
        #   records in the interval is reported. {Func} = Valid Count will return
        #   the non NaN count.
        # - {Func} Over Demographics - will apply (Func} to values in records 
        #   entering the summary interval. When {Func}=Sum, this is the default
        #   option for Booleans that are unaffected by the simulation i.e.
        #   non state indicators not in the affected list of the simulation
        #   project. When {Func} = Average, it is equivalent to dividing the
        #   sum over demographics by the total number of records entering the
        #   interval. This is the default option for non-Boolean parameters
        #   that are in the affected list of the simulation. When {Func} = STD,
        #   sample standard deviation is calculated using the method of
        #   provisional means. When {Func} = Min or when {Func} = Max then the
        #   minimal/maximal value of demographics records entering the interval
        #   is reported. {Func} = Valid Count will return the non NaN count.
        # - {Func} Over Last Observations Carried Forward - will apply (Func}
        #   to the last record of each individual. The max time record, 
        #   i.e. either the record in the year of termination, or the last year 
        #   record, is considered. Note that every individual will have exactly 
        #   one record for each repetition. Note that min time is ignored for
        #   this calculation. Note that if a record arrives already at the 
        #   terminal state at time 0, even if 0 is not specified in the 
        #   interval, the record will still be considered for Last Observations
        #   Carried Forward. It is the responsibility of the user to filter out
        #   terminated records on input. {Func} can be Sum, Average, STD, Min,
        #   Max, Valid Count. 
        # - Record Count - Return the total number of records in the
        #   interval. In a sense this ignores the parameter itself
        #   and used by system defaults. 
        # - Demographic count - Returns number of records entering the
        #   interval. In a sense this ignores the parameter itself. 
        # - Interval Start - return the Simulation start step number of the
        #   interval. In a sense this ignores the parameter itself. 
        # - Interval End - return the Simulation end step of the interval.
        #   In a sense this ignores the parameter itself. 
        # - Interval Length - return the number of steps represented in the
        #   interval. In a sense this ignores the parameter itself.
        # - No Summary - No summary is returned for the column. This is the
        #   default for system Reserved Parameters such as IndividualID, Time,
        #   and Repetition.
        # Note that an Auto Detect option can be specified by the user and it
        # is interpreted by the system to one of the above options.
        # If UseOnlyPreviousResults is set then only initialization
        # values are considered without new data from this result set.

        def CalculateCoreStats(DataVec, SumsVec, MinVec, MaxVec, AvgVec, VarVec, NonNaNCountVec, Count):
            """ Caluclate statistics and output them """
            Count = Count + 1
            for ColumnNum in ColumnsToCalculate:
                if ColumnNum < len(DataVec):
                    DataEntry = DataVec[ColumnNum]
                    if not IsNaN(DataEntry):
                        if NonNaNCountVec[ColumnNum] == 0:
                            # if this is the first occurance, just copy the data
                            NonNaNCountVec[ColumnNum] = 1
                            SumsVec[ColumnNum] = DataEntry
                            MinVec[ColumnNum] = DataEntry
                            MaxVec[ColumnNum] = DataEntry
                            AvgVec[ColumnNum] = DataEntry
                            VarVec[ColumnNum] = 0
                        else:
                            # otherwise, accumulate statistics
                            NonNaNCountVec[ColumnNum] = NonNaNCountVec[ColumnNum] + 1
                            SumsVec[ColumnNum] = SumsVec[ColumnNum] + DataEntry
                            MinVec[ColumnNum] = min(MinVec[ColumnNum],DataEntry)
                            MaxVec[ColumnNum] = max(MaxVec[ColumnNum],DataEntry)
                            # Use a method for provisional means
                            Diff = DataEntry - AvgVec[ColumnNum]
                            AvgVec[ColumnNum] = AvgVec[ColumnNum] + Diff/NonNaNCountVec[ColumnNum]
                            VarVec[ColumnNum] = VarVec[ColumnNum] + Diff*(DataEntry - AvgVec[ColumnNum])
                elif ColumnNum > len(DataVec):
                    # Note that the last column ColumnNum == len(DataVec)
                    # is blank and therefore ignored during this check.
                    raise ValueError, "ASSERTION ERROR - accessing an invalid column in the results"
            return (SumsVec, MinVec, MaxVec, AvgVec, VarVec, NonNaNCountVec, Count)

        def SafeVarToStd(Variance,NumberOfEntries):
            """ calculates STD from Variance return NaN rather than an Error """
            # This function performs a safe division by number of entries and
            # returns NaN is case on 1 person or no people. Note that this 
            # function may be called with 0 people, which will also return NaN
            if NumberOfEntries <= 1:
                RetVal = NaN
            else:
                # Note that NumberOfEntries-1 is used for calculating STD
                # rather than just NumberOfEntries
                RetVal = Sqrt(Variance/(NumberOfEntries-1))
            return RetVal

        [StratifyIndex, StratifyMaxCount, StratificationColumnIndices, StratifyBy] = StratificationParameters
        if (StratifyIndex >= StratifyMaxCount):
            raise ValueError, 'Summary Calculation Error: The stratification cell index is out of bounds. The flat stratification index is ' + str(StratifyIndex) + ' beyond max number of cells: ' + str(StratifyMaxCount) 
        if (TimeRange != None or len(TimeRange) != 2) and not ( (0 <= TimeRange[0] <= Projects[self.ProjectID].NumberOfSimulationSteps) and (0 <= TimeRange[1])) :
            # Note that Time range[1] can be higher than the simulation steps,
            # but range[0] should have been detected - it is an assertion error
            raise ValueError, 'Summary Calculation Error: The time range for calculating counts ' + str(TimeRange) + ' is out of the range defined by the project: [0,' + str(Projects[self.ProjectID].NumberOfSimulationSteps) + ']'
        # Skip calculations for time interval ranges where numbers are higher
        # than the maximal time that records have reached in this simulation
        SkipCalculationForThisRange = TimeRange[0] > MaxTime
        if InitializationValues == None:
            # If no previous initial values were specified, use defualt values
            RecordCount = 0
            DemographicCount = 0
            LastValueCount = 0
            ZeroVec = len(self.DataColumns)*[0]
            NaNVec = len(self.DataColumns)*[NaN]

            Sums = NaNVec[:]
            Avgs = NaNVec[:]
            Vars = NaNVec[:]
            Mins = NaNVec[:]
            Maxs = NaNVec[:]
            ValidCounts = ZeroVec[:]
            DemographicSums = NaNVec[:]
            DemographicAvgs = NaNVec[:]
            DemographicVars = NaNVec[:]
            DemographicMins = NaNVec[:]
            DemographicMaxs = NaNVec[:]
            DemographicValidCounts = ZeroVec[:]
            LastValueSums = NaNVec[:]
            LastValueAvgs = NaNVec[:]
            LastValueVars = NaNVec[:]
            LastValueMins = NaNVec[:]
            LastValueMaxs = NaNVec[:]
            LastValueValidCounts = ZeroVec[:]

        else:
            (Sums, Avgs, Vars, Mins, Maxs, ValidCounts, DemographicSums, DemographicAvgs, DemographicVars, DemographicMins, DemographicMaxs, DemographicValidCounts, LastValueSums, LastValueAvgs,  LastValueVars, LastValueMins, LastValueMaxs, LastValueValidCounts, RecordCount, DemographicCount, LastValueCount) = InitializationValues
        # Locate the Columns in focus such as the TimeColumn
        TimeColumnIndex = self.DataColumns.index('Time')
        RepetitionColumnIndex = self.DataColumns.index('Repetition')
        IndividualIdColumnIndex = self.DataColumns.index('IndividualID')
        ColumnsToCalculate = list(set(DataColumnsIndicesToShow))
        # now Actually look at records unless skipping or using previous results
        if not UseOnlyPreviousResults and not SkipCalculationForThisRange:
            # Reset the last row
            LastRowThatFitsCell = None
            for (RowNum,DataRow) in enumerate(self.Data):
                # Record the initial row for the individual. i.e. Time = 0
                if ( 0 == DataRow[TimeColumnIndex] ):
                    InitialRow = DataRow
                    # rest the record entering the first time interval
                    FirstRowInTimeInterval = None
                # Record the first row for the individual entering the
                # specifiec time interval. Only the first record that fits 
                # the time interval start is used
                if (FirstRowInTimeInterval == None) and (TimeRange[0] == DataRow[TimeColumnIndex]):
                    FirstRowInTimeInterval = DataRow
                # Figure out if there is a need to startify and how
                # First assume that calculations should be made.
                GenerateStatisticsForThisStratificationCell = True
                # Check if there is a need to check the stratification table
                # Recall that the last index indicates all records with no 
                # stratification and should always be reported
                if StratifyIndex < StratifyMaxCount-1:
                    # Depending on the stratification cell value defined by the user
                    # the system will check the proper record according to the
                    # following values:
                    StratificationMethod = StratifyBy.AccessCell(StratifyIndex)
                    if StratificationMethod == 0:
                        # Ignore cell if no stratification defined
                        GenerateStatisticsForThisStratificationCell = False
                    elif StratificationMethod == 1:
                        # If demographic stratification defined
                        RecordForStratification = InitialRow
                    elif StratificationMethod == 2:
                        # If stratification by first record in time interval
                        if FirstRowInTimeInterval != None:
                            # reached the first record within the time interval 
                            RecordForStratification = FirstRowInTimeInterval
                        else:
                            # if not yet reached the mininum time, then
                            # there is no need to stratify
                            GenerateStatisticsForThisStratificationCell = False
                    elif StratificationMethod == 3:
                        # If stratification by every record
                        RecordForStratification = DataRow
                    else:
                        raise ValueError, 'Report Stratification Error - Invalid cell stratification method value ' + str(StratificationMethod) + ' in position ' + str(StratifyIndex) + ' in the stratification table: ' + str(StratifyBy.Description()) + ' . Please redefine the stratification method'
                    if GenerateStatisticsForThisStratificationCell:
                        # For all stratification indices before the last
                        # Extract the vector index using the values in the data
                        IndexVector = []
                        for ColumnIndex in StratificationColumnIndices:
                            DimName = self.DataColumns[ColumnIndex]
                            Value = RecordForStratification[ColumnIndex]
                            (DimIndex, RangeIndex) = StratifyBy.LocateDimAndRangeIndex(DimName,Value)
                            IndexVector = IndexVector + [RangeIndex]
                        # Check if this cell compares to the requested
                        # Stratification Index.
                        (FlatIndex,DummyVectorIndex) = StratifyBy.FigureOutIndex(IndexVector)
                        # Generate statistics for cells that the table data 
                        # indicate as non zero. This allows the user to define
                        # startification by part
                        GenerateStatisticsForThisStratificationCell = (FlatIndex == StratifyIndex)
                # If it is ok to proceed with calculations, go ahead
                if GenerateStatisticsForThisStratificationCell:
                    # Process demographics only by detecting the minimal time
                    if ( TimeRange[0] == DataRow[TimeColumnIndex] ):
                        (DemographicSums, DemographicMins, DemographicMaxs, DemographicAvgs, DemographicVars, DemographicValidCounts, DemographicCount) =  CalculateCoreStats(DataRow, DemographicSums, DemographicMins, DemographicMaxs, DemographicAvgs, DemographicVars, DemographicValidCounts, DemographicCount)
                    # Process records within the time limits
                    if TimeRange[0] <= DataRow[TimeColumnIndex] <= TimeRange[1]:
                        (Sums, Mins, Maxs, Avgs, Vars, ValidCounts, RecordCount) =  CalculateCoreStats(DataRow, Sums, Mins, Maxs, Avgs, Vars, ValidCounts, RecordCount)
                    # Process records with time smaller than the max specified
                    if DataRow[TimeColumnIndex] <= TimeRange[1]:
                        # The last row is now the current row. Note that this
                        # is calculated only if the stratification criteria
                        # was passed. Later on, this record may be used
                        # if it will be proven to be the last record for this
                        # individual.
                        LastRowThatFitsCell = DataRow
                # Now, outside the stratification critera, check if this is the
                # last record for the individual and act accordingly to compute
                # LOCF calculations. Process records with time smaller than the
                # max specified
                if DataRow[TimeColumnIndex] <= TimeRange[1]:
                    LastRowFlag = False
                    NextRowNum = RowNum + 1
                    # Check if the last record in the data has been reached
                    if  NextRowNum < len(self.Data):
                        NextRow = self.Data[NextRowNum]
                        # If the next record is beyond the max time range
                        # specified or its individualID or repetition is
                        # different, then this is the last record for this
                        # individual in this repetition for this time frame
                        if (NextRow[TimeColumnIndex] > TimeRange[1]) or (DataRow[RepetitionColumnIndex] != NextRow[RepetitionColumnIndex]) or (DataRow[IndividualIdColumnIndex] != NextRow[IndividualIdColumnIndex]):
                            LastRowFlag = True
                    else:
                        # If this is the last record in the list
                        LastRowFlag = True
                    # Check if this is a last row for the individual
                    if LastRowFlag:
                        # Check if any record for this individual passed the
                        # stratification test
                        if LastRowThatFitsCell != None:
                            # Now calculate LOCF calcualtion for this last
                            # recorded record
                            (LastValueSums, LastValueMins, LastValueMaxs, LastValueAvgs, LastValueVars, LastValueValidCounts, LastValueCount) =  CalculateCoreStats(LastRowThatFitsCell, LastValueSums, LastValueMins, LastValueMaxs, LastValueAvgs, LastValueVars, LastValueValidCounts, LastValueCount)
                        # Since this is the last row flag and we expect to
                        # process no more record from this individual, then
                        # is is ok to reset LastRowThatFitsCell for the next
                        # individual.
                        LastRowThatFitsCell = None
        # Now divide the variance by the count to get the std
        STDs = map(SafeVarToStd, Vars, ValidCounts)
        DemographicSTDs = map(SafeVarToStd, DemographicVars, DemographicValidCounts)
        LastValueSTDs = map(SafeVarToStd, LastValueVars, LastValueValidCounts)
        IntervalStart = TimeRange[0]
        IntervalEnd = TimeRange[1]
        IntervalLength = TimeRange[1] - TimeRange[0] + 1
        Result = []
        for (ColumnSortIndex,ColumnNum) in enumerate(DataColumnsIndicesToShow):
            # Traverse all columns and construct the summary results
            if ColumnNum <= len(self.DataColumns):
                # First take care of a blank column that has no data other than
                # derived calculations such as summary interval or record count
                if ColumnNum == len(self.DataColumns) and (CalculationMethods[ColumnSortIndex] not in ['Record Count', 'Demographic Count', 'Last Value Count', 'Interval Start', 'Interval End', 'Interval Length']):
                    SummaryValue = None
                # If no records were encountered in this stratification then
                # use None. Do this for all 3 levels: All, Demographics, LOCF
                # in any case report Time interval since it is used as a key
                # in reports
                elif (RecordCount == 0 or ( DemographicCount == 0 and CalculationMethods[ColumnSortIndex].endswith('Over Demographics') ) or ( LastValueCount == 0 and CalculationMethods[ColumnSortIndex].endswith('Over Last Observations Carried Forward') )) and CalculationMethods[ColumnSortIndex] not in ['Interval Start', 'Interval End', 'Interval Length']:
                    SummaryValue = None
                # otherwise, go over the calculation and report it
                elif CalculationMethods[ColumnSortIndex] == 'Sum Over All Records':
                    SummaryValue = Sums[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Average Over All Records':
                    SummaryValue = Avgs[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'STD Over All Records':
                    SummaryValue = STDs[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Min Over All Records':
                    SummaryValue = Mins[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Max Over All Records':
                    SummaryValue = Maxs[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Valid Count of All Records':
                    SummaryValue = ValidCounts[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Sum Over Demographics':
                    SummaryValue = DemographicSums[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Average Over Demographics':
                    SummaryValue = DemographicAvgs[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'STD Over Demographics':
                    SummaryValue = DemographicSTDs[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Min Over Demographics':
                    SummaryValue = DemographicMins[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Max Over Demographics':
                    SummaryValue = DemographicMaxs[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Valid Count of Demographics':
                    SummaryValue = DemographicValidCounts[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Sum Over Last Observations Carried Forward':
                    SummaryValue = LastValueSums[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Average Over Last Observations Carried Forward':
                    SummaryValue = LastValueAvgs[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'STD Over Last Observations Carried Forward':
                    SummaryValue = LastValueSTDs[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Min Over Last Observations Carried Forward':
                    SummaryValue = LastValueMins[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Max Over Last Observations Carried Forward':
                    SummaryValue = LastValueMaxs[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Valid Count of Last Observations Carried Forward':
                    SummaryValue = LastValueValidCounts[ColumnNum]
                elif CalculationMethods[ColumnSortIndex] == 'Record Count':
                    SummaryValue = RecordCount
                elif CalculationMethods[ColumnSortIndex] == 'Demographic Count':
                    SummaryValue = DemographicCount
                elif CalculationMethods[ColumnSortIndex] == 'Last Value Count':
                    SummaryValue = LastValueCount
                elif CalculationMethods[ColumnSortIndex] == 'Interval Start':
                    SummaryValue = IntervalStart
                elif CalculationMethods[ColumnSortIndex] == 'Interval End':
                    SummaryValue = IntervalEnd
                elif CalculationMethods[ColumnSortIndex] == 'Interval Length':
                    SummaryValue = IntervalLength
                elif CalculationMethods[ColumnSortIndex] == 'No Summary':
                    SummaryValue = None
                else:
                    raise ValueError, "ASSERTION ERROR - Unsupported calculation method while calculating summaries"
            else:
                raise ValueError, "ASSERTION ERROR - accessing an invalid column in the results. Fourth Assertion Check "
            Result = Result + [SummaryValue]
            # output the updated initialization values in case these are needed
            UpdatedInitializationValues = (Sums, Avgs, Vars, Mins, Maxs, ValidCounts, DemographicSums, DemographicAvgs, DemographicVars, DemographicMins, DemographicMaxs, DemographicValidCounts, LastValueSums, LastValueAvgs,  LastValueVars, LastValueMins, LastValueMaxs, LastValueValidCounts, RecordCount, DemographicCount, LastValueCount)
        if Result == []:
            raise ValueError, "Summary Calculation Error: No valid columns found in results. Please try and redefine the report columns"
        return (Result, UpdatedInitializationValues)


    def PrepareSummaryIntervals(self, SummaryIntervals):
        "Prepares the summary intervals to fit the result set"
        # Prepare the summation intervals according to the number of
        # simulation steps as defined in the project. Also Extract the maximal
        # time from the maximum time reached in simualtion. Later on
        # simulation steps outside the MaxTime Bound will be reported as NaN
        NumberOfSimulationSteps = Projects[self.ProjectID].NumberOfSimulationSteps
        MaxTime = 0
        TimeColumnIndex = self.DataColumns.index('Time')
        for DataRecord in self.Data:
            MaxTime = Max(MaxTime,DataRecord[TimeColumnIndex])
        StartAtYearZero = (0 in SummaryIntervals) + 0
        # Filter out bad interval inputs such as non integers, non pairs,
        # descending pairs, negatives and out of range, and non integer pairs
        # in case of a pair the lower number must be in NumberOfSimulationSteps
        # and a higher second number can exceed the range
        NewSummaryIntervals = filter (lambda Entry: (IsInt(Entry) and (0 < Entry < NumberOfSimulationSteps)) or (IsList(Entry) and len(Entry)==2 and (Entry[0]<=Entry[1]) and IsInt(Entry[0]) and IsInt(Entry[1]) and (0 <= Entry[0] <= NumberOfSimulationSteps)) , SummaryIntervals)
        # Now add the Time Intervals adding NumberOfSimulationSteps at the end,
        # unless already defined.
        TotalSumInterval = [1 - StartAtYearZero, NumberOfSimulationSteps]
        if TotalSumInterval not in NewSummaryIntervals:
            NewSummaryIntervals = NewSummaryIntervals + [TotalSumInterval]
        return (MaxTime, StartAtYearZero, NewSummaryIntervals)

    def CalculateStatisticsForAllSummaryIntervals(self, MaxTime, StartAtYearZero, SummaryIntervals, StratifyBy, DataColumnsIndicesToShow, CalculationMethods, SummariesBaseFromPreviousResultBatch = None, UseOnlyPreviousResults = False):
        "Calculates the statistics for the report"
        # Figure out how many startification cells are needed.
        # Always Report the summary without stratification
        StratificationColumnIndices = []
        if StratifyBy == None:
            # this means that this is the unstratified result
            StratifyMaxCount = 1
        else:
            # Figure out stratification
            StratifyMaxCount = 1 + StratifyBy.DataItemsNum
            # This means we have to make checks against table cell index
            # locate these columns in the data
            for (DimName, DimRange) in StratifyBy.Dimensions:
                try:
                    ColumnIndexInResults = self.DataColumns.index(DimName)
                    StratificationColumnIndices.append(ColumnIndexInResults) 
                except:
                    raise ValueError, 'Summary Calculation Error: Could not locate the stratification dimension ' + str(DimName)+ ' in the results as specified by option StratifyBy ' + str(StratifyBy.Description())  + '. This column does not exist in the results columns for this project'
        # Initialize some statistics:
        EmptyCategoryVector = [0]*(len(SummaryIntervals))
        TimeInterval = EmptyCategoryVector[:]
        Summaries = []
        SummariesBaseForNextResultBatch = []
        # Loop through each stratification cell
        for StratifyIndex in range(StratifyMaxCount):
            Summaries.append(EmptyCategoryVector[:])
            SummariesBaseForNextResultBatch.append(EmptyCategoryVector[:])
        NumberOfSimulationSteps = Projects[self.ProjectID].NumberOfSimulationSteps
        for (SummaryIntervalIndex, SummaryInterval) in enumerate(SummaryIntervals):
            # Build the time intervals
            if IsList(SummaryInterval):
                TimeInterval[SummaryIntervalIndex] = [SummaryInterval]
            else:
                TimeInterval[SummaryIntervalIndex] = []
                TimeUnit = 1 - StartAtYearZero
                # The time unit has to be lower than the number of
                # simulation steps.
                while TimeUnit <= NumberOfSimulationSteps:
                    TimeInterval[SummaryIntervalIndex].append([TimeUnit,min(TimeUnit + SummaryInterval - 1, NumberOfSimulationSteps)])
                    TimeUnit = TimeUnit + SummaryInterval
            # Init summary vectors
            EmptyInitVector = [0]*len(TimeInterval[SummaryIntervalIndex])
            # Loop through each stratification cell 
            for StratifyIndex in range(StratifyMaxCount):
                Summaries[StratifyIndex][SummaryIntervalIndex] = EmptyInitVector[:]
                SummariesBaseForNextResultBatch[StratifyIndex][SummaryIntervalIndex] = EmptyInitVector[:]
                for (TimeIntervalIndex,[StartTime,EndTime]) in enumerate(TimeInterval[SummaryIntervalIndex]):
                    # handle previous batch results
                    if SummariesBaseFromPreviousResultBatch == None:
                        # default 0 initialization values
                        InitializationValues = None
                    else:
                        # Pass results from previous batch for initialization
                        InitializationValues = SummariesBaseFromPreviousResultBatch[StratifyIndex][SummaryIntervalIndex][TimeIntervalIndex]
                    (Result, UpdatedInitializationValues) = self.CalculateSummary( [StartTime,EndTime], [StratifyIndex,StratifyMaxCount,StratificationColumnIndices,StratifyBy], DataColumnsIndicesToShow, CalculationMethods, MaxTime , InitializationValues, UseOnlyPreviousResults)
                    Summaries[StratifyIndex][SummaryIntervalIndex][TimeIntervalIndex] = Result
                    SummariesBaseForNextResultBatch[StratifyIndex][SummaryIntervalIndex][TimeIntervalIndex] = UpdatedInitializationValues
        return (TimeInterval, StratifyMaxCount, StratificationColumnIndices, Summaries, SummariesBaseForNextResultBatch)

    def ResolveReportDataAndOptions (self, FormatOptions = None, UseOnlyPreviousResults = False):
        """ Generate the Data and the Options for the report"""
        TotalIndent = HandleOption('TotalIndent', FormatOptions,'')
        IndentAtom = HandleOption('IndentAtom', FormatOptions,'  ')
        ColumnSpacing = HandleOption('ColumnSpacing', FormatOptions,' | ')
        FieldHeader = HandleOption('FieldHeader', FormatOptions,True)
        LineDelimiter = HandleOption('LineDelimiter', FormatOptions,'\n')
        SectionSeparator = HandleOption('SectionSeparator', FormatOptions,70*'_')
        ShowHidden = HandleOption('ShowHidden', FormatOptions,False)
        DetailLevel = HandleOption('DetailLevel', FormatOptions, 0)
        # Report Specific
        BlankColumnsJoinedInData = HandleOption('BlankColumnsJoinedInData', FormatOptions,False)
        SummaryIntervals = HandleOption('SummaryIntervals', FormatOptions,[[0,0],1,5,10,20])
        ColumnNumberFormat = HandleOption('ColumnNumberFormat', FormatOptions, ['%0.5f','%i'])
        # By default there is no stratification
        StratifyBy = HandleOption('StratifyBy', FormatOptions, None)
        # Check that the stratification expression is a valid table expression
        if StratifyBy != None:
            # First check this is a valid expression
            Expr(StratifyBy)
            # Then check it is a valid table. Return the table class or None
            StratifyBy = TableClass(InitString = StratifyBy)
        # ReportHeader can be used to change he header in case multiple reports
        # are generated. 
        ReportHeader = HandleOption('ReportHeader', FormatOptions, None)
        ReportFooter = HandleOption('ReportFooter', FormatOptions, None)
        # Note that if SummaryIntervals has the number 0, this means
        # summation will start from year 0, otherwise, it will start from year 1
        # alternatively, if Summation intervals holds sequences, these sequences
        # will be used to define the specific time Intervals rather than jumps.
        # for example the following is valid: [1,2,[0,5],[0,10]]
        # Also note that with details level 0, only summaries are printed. With
        # detail level 1 raw data is printed, and with detail level 2 and above
        # also project data is drilled down.
        # ColumnNumberFormat defines how number precision is to be formatted.
        # It is a tuple of two strings. The first string stands for float format
        # and the second for integer format. For float format, if the letter V/v
        # appears in the end, this means relative precision with a desired
        # precision compared to the max where the number of significant
        # digits preceding the letter V/v. Otherwise formatting is according to
        # the string defined. Note that lower case 'v' means that each category
        # of information, i.e. Raw Data, Sums, and Averages are dealt with
        # separately when considering relative numbers. An upper case 'V' means
        # that all numbers in the column are considered when determining the
        # precision for that column.
        ColumnFilter = HandleOption('ColumnFilter', FormatOptions, [])
        # The column filter holds tuples such as:
        # (ParamName, CalculationMethod, ColumnTitle)
        # ParamName holds the names of the parameters for which output will
        # be generated. Also the output can be filtered according to 
        # Parameter Type, when the parameter type name is enclosed in <>.
        # State Indicators can be followed by ',State' or ',Sub-Process' that
        # can further be followed by state indicator suffixes where '_Actual'
        # stands for the actual state with no suffix. Also the group named as
        # <Header> can be used do define the header information for an interval.
        # ColumnTitle defines alternative title labels in case the user wishes
        # to do so. In case of an empty string the original name is used.
        # CalculationMethod defines how the columns will be summarized in the
        # Summary interval. By default, all columns are displayed with sums and
        # averages. Note that duplication of columns is possible.
        # PreCalculatedResults holds results pre-calculated outside the report
        # function that will be displayed. Note that in this case, the
        # formatting of the report will be a bit different as specific data
        # pertaining to the current result set will not be displayed.
        # Moreover the %V formatting option will be treated as %v.
        PreCalculatedResults = HandleOption('PreCalculatedResults', FormatOptions, None)
        # This way, this function can be used and reused to accumulate results
        # from multiple SimulationResult objects before writing a final report
        # Note that if no pre-calculated results exist UseOnlyPreviousResults
        # is overridden and considered to be true to avoid zero results.
        if PreCalculatedResults == None:
            # If no pre-calcualted results exist
            SummariesBaseForNextResultBatch = None
            # If no pre-calcualted results exist, calculations are required for
            # this result set.
            UseOnlyPreviousResults = False
        else:
            # If pre-calcualted results exist extract the last member that
            # represents the base for calculating summaries
            SummariesBaseForNextResultBatch = PreCalculatedResults[-1]
        # Resolve all column attributes
        (DataColumnsIndicesToShow, ColumnTitles, CalculationMethods, OriginalCalculationMethods, DataColumnsWithBlank, BlankColumnIndex, CalculationTitlesPerColumns) =  self.ResolveColumnAttributesForReport(ColumnFilter)
        # Update summary intervals
        (MaxTime, StartAtYearZero, SummaryIntervals) = self.PrepareSummaryIntervals(SummaryIntervals)
        # Update summaries
        (TimeInterval, StratifyMaxCount, StratificationColumnIndices, Summaries, SummariesBaseForNextResultBatch) = self.CalculateStatisticsForAllSummaryIntervals(MaxTime, StartAtYearZero, SummaryIntervals, StratifyBy, DataColumnsIndicesToShow, CalculationMethods, SummariesBaseForNextResultBatch, UseOnlyPreviousResults)
        # Return a tuple with all calculated data
        return (TotalIndent, IndentAtom, ColumnSpacing, FieldHeader, LineDelimiter, SectionSeparator, ShowHidden, DetailLevel, BlankColumnsJoinedInData, ColumnNumberFormat, StratifyBy, ReportHeader, ReportFooter, ColumnFilter, PreCalculatedResults, DataColumnsIndicesToShow, ColumnTitles, CalculationMethods, OriginalCalculationMethods, DataColumnsWithBlank, BlankColumnIndex, CalculationTitlesPerColumns, MaxTime, StartAtYearZero, SummaryIntervals, TimeInterval, StratifyMaxCount, StratificationColumnIndices, Summaries, SummariesBaseForNextResultBatch)


    def GenerateReport(self, FormatOptions = None):
        """ Generate the report for this entity instance """
        # Resolve the data and options
        # Note that by default there is no calculation of no data, unless
        # there are no PreCalculatedResults that will force recalculations.
        # In other words, calling generate report expects calculations to be
        # provided to it in PreCalculatedResults and only if these are not
        # defined the current results will be calculated. This is awkward.
        # However, it allows accumulated batch calculations from outside the
        # system using a utility and therefore implemented this way.
        (TotalIndent, IndentAtom, ColumnSpacing, FieldHeader, LineDelimiter, SectionSeparator, ShowHidden, DetailLevel, BlankColumnsJoinedInData, ColumnNumberFormat, StratifyBy, ReportHeader, ReportFooter, ColumnFilter, PreCalculatedResults, DataColumnsIndicesToShow, ColumnTitles, CalculationMethods, OriginalCalculationMethods, DataColumnsWithBlank, BlankColumnIndex, CalculationTitlesPerColumns, MaxTime, StartAtYearZero, SummaryIntervals, TimeInterval, StratifyMaxCount, StratificationColumnIndices, Summaries, SummariesBaseForNextResultBatch) = self.ResolveReportDataAndOptions(FormatOptions, True)
        # Calculate desired precisions for each column
        FormatStrings = [None]*len(DataColumnsIndicesToShow)
        for (ColumnSortIndex,ColumnNum) in enumerate(DataColumnsIndicesToShow):
            # Note that we create two entries for formats:
            # FormatStrings[ColumnSortIndex][0] to format actual data
            # FormatStrings[ColumnSortIndex][1] to format summary results
            FormatStrings[ColumnSortIndex] = [None, None]
            ParamName = DataColumnsWithBlank[ColumnNum]
            ColumnIsInteger = (ParamName in ['Repetition','Time','IndividualID']) or (ColumnNum == BlankColumnIndex) or (Params[ParamName].ParameterType in  ['Integer','State Indicator'] ) 
            FormatStrings[ColumnSortIndex] = [ColumnNumberFormat[0]]*2
            if ColumnIsInteger:
                # Integer columns
                # Correct the format of the actual data to Integer
                FormatStrings[ColumnSortIndex][0] = ColumnNumberFormat[1][:]
                if CalculationMethods[ColumnSortIndex] in ['Sum Over All Records', 'Sum Over Demographics', 'Record Count', 'Demographic Count', 'Interval Start', 'Interval End', 'Interval Length']:
                    # Correct the format of summary to Integer
                    FormatStrings[ColumnSortIndex][1] = ColumnNumberFormat[1][:]
            if CalculationMethods[ColumnSortIndex] in ['No Summary']:
                FormatStrings[ColumnSortIndex][1] = '%0.0s'
            if ColumnNum == BlankColumnIndex:
                # No text for the blank column data 
                FormatStrings[ColumnSortIndex][0] = '%0.0s'
        # Calculate the largest length string for each column while
        # including the header length first
        HeaderLengths = map(lambda Entry1, Entry2: max(len(Entry1),len(Entry2)), ColumnTitles, CalculationTitlesPerColumns)
        # If no precalculated resulte exist traverse the data
        if PreCalculatedResults == None:
            for DataRow in self.Data:
                for (ColumnSortIndex,ColumnNum) in enumerate(DataColumnsIndicesToShow):
                    # Treat blank column by checking index
                    if ColumnNum < len(DataRow):
                        DataEntry = DataRow[ColumnNum]
                        if not IsFinite(DataEntry):
                            EntryLength = len(SmartStr(DataEntry))
                        else:
                            EntryLength = len(FormatStrings[ColumnSortIndex][0]%(DataEntry))
                    elif ColumnNum > len(DataRow):
                        raise ValueError, "ASSERTION ERROR - accessing an invalid column beyond blank"
                    else:
                        DataEntry = None
                        EntryLength = 0
                    HeaderLengths[ColumnSortIndex] = max(HeaderLengths[ColumnSortIndex], EntryLength)
        # Now traverse the Summary data as well
        for StratifyIndex in range(StratifyMaxCount):
            for (SummaryIntervalIndex, SummaryInterval) in enumerate(SummaryIntervals):
                for (TimeIntervalIndex,[StartTime,EndTime]) in enumerate(TimeInterval[SummaryIntervalIndex]):
                    for (ColumnSortIndex,ColumnNum) in enumerate(DataColumnsIndicesToShow):
                        SummaryEntry = Summaries[StratifyIndex][SummaryIntervalIndex][TimeIntervalIndex][ColumnSortIndex]
                        # Handle None entries 
                        if SummaryEntry == None:
                            EntryLength = 0
                        elif not IsFinite(SummaryEntry):
                            EntryLength = len(SmartStr(SummaryEntry))
                        else:
                            EntryLength = len(FormatStrings[ColumnSortIndex][1]%(SummaryEntry))
                        HeaderLengths[ColumnSortIndex] = max(HeaderLengths[ColumnSortIndex], EntryLength)
        # If ReportHeader exists use it, otherwise create the title
        if ReportHeader == None:
            ReportString = ''
            ReportString = ReportString + TotalIndent + FieldHeader * 'Results ID: ' + str(self.ID) + LineDelimiter
            ReportString = ReportString + TotalIndent + FieldHeader * 'Created On: ' + str(self.CreatedOn) + LineDelimiter
            if ShowHidden:
                ReportString = ReportString + TotalIndent + FieldHeader * 'ProjectID: ' + str(self.ProjectID) + LineDelimiter
                ReportString = ReportString + TotalIndent + FieldHeader * 'Visual TraceBack: ' + str(self.TraceBack) + LineDelimiter
                ReportString = ReportString + TotalIndent + FieldHeader * 'Pickled TraceBack: ' + pickle.dumps(self.TraceBack) + LineDelimiter
            if DetailLevel in [0,1]:
                ReportString = ReportString + TotalIndent + FieldHeader * 'For Project: ' + str(Projects[self.ProjectID].Name) + LineDelimiter
            else:
                # Print details project information only if the amount of detail
                # requested is above 1
                RevisedFormatOptions = HandleOption('TotalIndent', FormatOptions, TotalIndent + IndentAtom, True)
                RevisedFormatOptions = HandleOption('DetailLevel', RevisedFormatOptions, DetailLevel-1, True)
                ReportString = ReportString + Projects[self.ProjectID].GenerateReport(RevisedFormatOptions)
        else:
            ReportString = ReportHeader
        # Calculate the title string
        TitlesString = ''
        TitlesStringSummary = ''
        for (ColumnSortIndex,ColumnNum) in enumerate(DataColumnsIndicesToShow):
            Title = ColumnTitles [ColumnSortIndex]
            # For blank columns from the header use a blank separator
            ColumnSpacingToUse = Iif (ColumnNum == BlankColumnIndex and BlankColumnsJoinedInData, ' '*len(ColumnSpacing), ColumnSpacing)
            TitlesString = TitlesString + TotalIndent + Title.rjust(HeaderLengths[ColumnSortIndex]) + ColumnSpacingToUse 
            TitlesStringSummary = TitlesStringSummary + TotalIndent + Title.rjust(HeaderLengths[ColumnSortIndex]) + ColumnSpacing 
        # Print details project information only if the amount of detail
        # requested is above 0 and no precalculated results exist
        if ReportHeader == None:
            if DetailLevel > 0 and PreCalculatedResults == None:
                ReportString = ReportString + TotalIndent + FieldHeader * 'The Raw Results are: ' + LineDelimiter
                # Now use these column lengths while creating the data table
                # First create the title line.
                ReportString = ReportString + TitlesString + LineDelimiter
                # Now print the data
                for (RowNum,DataRow) in enumerate(self.Data):
                    ReportString = ReportString + TotalIndent
                    for (ColumnSortIndex,ColumnNum) in enumerate(DataColumnsIndicesToShow):
                        # For blank columns from the header use a blank
                        # separator, also use blank format for None calues 
                        Title = ColumnTitles[ColumnSortIndex]
                        ColumnSpacingToUse = Iif (ColumnNum == BlankColumnIndex and BlankColumnsJoinedInData, ' '*len(ColumnSpacing), ColumnSpacing)
                        if ColumnNum == BlankColumnIndex:
                            DataEntryString = ''
                        elif not IsFinite(DataRow[ColumnNum]):
                            DataEntryString = SmartStr(DataRow[ColumnNum])
                        else:
                            DataEntryString = (FormatStrings[ColumnSortIndex][0]%(DataRow[ColumnNum]))
                        ReportString = ReportString + (DataEntryString).rjust(HeaderLengths[ColumnSortIndex]) + ColumnSpacingToUse
                    ReportString = ReportString + LineDelimiter
                ReportString = ReportString + LineDelimiter
            ReportString = ReportString + TotalIndent + FieldHeader * 'Summary Statistics:' + LineDelimiter
        # Generate arrays of texts and text sizes for each stratification cell
        if StratifyBy != None:
            (DescStrArray, DescStrSizeArray) = StratifyBy.GenerateRangeDescriptionArrays()
        # Print the statistics
        # Loop through all stratification cell indices 
        for StratifyIndex in range(StratifyMaxCount):
            # Print the stratification title
            if StratifyIndex == StratifyMaxCount - 1:
                ReportStatisticsForThisStratificationCell = -1
                StartificationCellDescription = ''
            else:
                ReportStatisticsForThisStratificationCell = StratifyBy.AccessCell(StratifyIndex)
                StartificationCellDescription = StratifyBy.GenerateRangeDescriptionText (DescStrArray, DescStrSizeArray, StratifyIndex, False)
            if ReportStatisticsForThisStratificationCell:
                StartificationTitle = ReportStratificationHeader + ReportStratificationDescriptionDict[ReportStatisticsForThisStratificationCell] + StartificationCellDescription
                ReportString = ReportString + TotalIndent + FieldHeader * StartificationTitle + LineDelimiter
                # First print the Titles String again 
                ReportString = ReportString + TitlesStringSummary + LineDelimiter
                # Then print a string showing the calculation titles
                for (ColumnSortIndex,ColumnNum) in enumerate(DataColumnsIndicesToShow):
                    Title = CalculationTitlesPerColumns[ColumnSortIndex]
                    ReportString = ReportString + TotalIndent + Title.rjust(HeaderLengths[ColumnSortIndex]) + ColumnSpacing 
                ReportString = ReportString + LineDelimiter
                for (SummaryIntervalIndex, SummaryInterval) in enumerate(SummaryIntervals):
                    for (TimeIntervalIndex,[StartTime,EndTime]) in enumerate(TimeInterval[SummaryIntervalIndex]):
                        DataRow = Summaries[StratifyIndex][SummaryIntervalIndex][TimeIntervalIndex]
                        for (ColumnSortIndex,ColumnNum) in enumerate(DataColumnsIndicesToShow):
                            DataEntry = DataRow[ColumnSortIndex]
                            # Handle None Entries
                            if DataEntry == None:
                                DataEntryString = ''
                            elif not IsFinite(DataEntry):
                                DataEntryString = SmartStr(DataEntry)
                            else:
                                DataEntryString = FormatStrings[ColumnSortIndex][1]%(DataEntry)
                            ReportString = ReportString + DataEntryString.rjust(HeaderLengths[ColumnSortIndex]) + ColumnSpacing
                        ReportString = ReportString + LineDelimiter
        if ReportFooter == None:
            if ColumnFilter != []:
                ReportString = ReportString + TotalIndent + FieldHeader*'Report Column Filter was:' + str(ColumnFilter) + LineDelimiter
            ReportString = ReportString + TotalIndent + SectionSeparator + LineDelimiter
        else:
            ReportString = ReportString + ReportFooter
        return ReportString

    # Description String
    def Describe(self):
        """ Return description string containing both ID and project name """
        return 'Result #' + str(self.ID) + ' associated with project ' + Projects[self.ProjectID].Name


    def CreateReportAsCSV(self, FileNameToExprotCSV, FormatOptions = None):
        """ Generate the CSV report for this entity instance """
        # Set constants
        ColumnSpacing = ' | '
        LineDelimiter = '\n'
        # Generate default options of do not exist yet
        FormatOptions = HandleOption('TotalIndent', FormatOptions, '', True)
        FormatOptions = HandleOption('IndentAtom', FormatOptions, '  ', True)
        FormatOptions = HandleOption('ColumnSpacing', FormatOptions, ColumnSpacing, True)
        FormatOptions = HandleOption('FieldHeader', FormatOptions, True, True)
        FormatOptions = HandleOption('LineDelimiter', FormatOptions, LineDelimiter, True)
        FormatOptions = HandleOption('ShowHidden', FormatOptions, False, True)
        FormatOptions = HandleOption('DetailLevel', FormatOptions, 0, True)
        # Override column number options with %r to generate 
        FormatOptions = HandleOption('ColumnNumberFormat', FormatOptions, ['%r','%r'],True)
        # Override column header and footer to generate only the table of interest
        FormatOptions = HandleOption('ReportHeader', FormatOptions, '', True)
        FormatOptions = HandleOption('ReportFooter', FormatOptions, '', True)
        # Resolve all column attributes
        ColumnFilter = HandleOption('ColumnFilter', FormatOptions, [])
        # A CSV report must start with Header definitions to allow
        # collecting its results later. So if it not detected at start,
        # then define it at start.
        if len(ColumnFilter)==0 or len(ColumnFilter[0])==0 or ColumnFilter[0][0]!='<Header>':
            ColumnFilter = [('<Header>', 'Auto Detect', '')] + ColumnFilter        
        ResultsArrays = []
        # Generate the report
        ReportResultString = self.GenerateReport(FormatOptions)
        ProcessedReportResultRowsList = ReportResultString.split(LineDelimiter)[:-1]
        RowValues = []
        ProjectID = self.ProjectID
        ProjectName = Projects[ProjectID].Describe()
        ModelID = Projects[ProjectID].PrimaryModelID
        ModelName = StudyModels[ModelID].Describe()
        PopulationID = Projects[ProjectID].PrimaryPopulationSetID
        PopulationName = PopulationSets[PopulationID].Describe()
        OverallNumberOfColumns = None
        OverallNumberOfRows = None
        for (RowNum,RowString) in enumerate(ProcessedReportResultRowsList):
            # Add Project specifications as titles at start
            ColumnValues = [ProjectName, ModelName, PopulationName]
            if RowString.startswith(ReportStratificationHeader):
                CountFromHeader = 0
                # The header has only one cell
                ColumnList = [RowString]
            else:
                # This removes the last empty cell caused by the | at the end
                ColumnList = RowString.split(ColumnSpacing)[:-1]
            for Entry in ColumnList:
                # The first three rows after stratification are title strings 
                if CountFromHeader < 3:
                    # strip the text from spaces that center it
                    EntryValue = Entry.strip()
                else:
                    # Otherwise they are values
                    if Entry.strip() == '':
                        # Empty values turn to None
                        EntryValue = None
                    else:
                        # Regular values are evaluated to Int/Float
                        EntryValue = eval(Entry ,EmptyEvalDict)
                ColumnValues = ColumnValues + [EntryValue]
            if RowNum == 1:
                # The number of columns can be deduced from the titles row
                NumberOfColumns = len(ColumnValues)
            elif CountFromHeader != 0:
                # validate rectangular array
                if len(ColumnValues) != NumberOfColumns:
                    raise ValueError, 'Create CSV report: The number of columns in Row #' +str(RowNum) + ' is ' + str(len(ColumnValues)) + '. It is not the same as previous rows: '+ str(NumberOfColumns) + ' This indicates a problem in converting the report. Check that there are no delimiter characters such as ''|'' or '','' or ''\\n'' in table column labels.'
            RowValues = RowValues + [ColumnValues]
            CountFromHeader = CountFromHeader + 1
        # Validate array size
        if OverallNumberOfColumns == None:
            OverallNumberOfRows = len(RowValues)
            OverallNumberOfColumns = NumberOfColumns
        else:
            if len(RowValues) != OverallNumberOfRows or NumberOfColumns!= OverallNumberOfColumns:
                raise ValueError, 'Create CSV report: The number of columns/rows is' + str(NumberOfColumns)+ '/' + str(len(RowValues)) + '. It is not the same as previous files: ' + str(OverallNumberOfColumns)+ '/' + str(len(OverallNumberOfRows)) + ' This indicates a problem in converting the report. Check that there are no delimiter characters such as ''|'' or '','' or ''\\n'' in table column labels. Also check that all result files were generated in a similar manner and there are no major differences between them.'
        ResultsArrays = ResultsArrays + [RowValues]
        # transpose the text before writing it to file, since the transposed
        # version is easier to read by a human.
        TransposedResults = map(None,*RowValues)
        ExportDataToCSV(FileNameToExprotCSV, TransposedResults)
        return TransposedResults


def CalculateStatisticsForCSV(FileNameList, OutputFileNamePrefix):
    """ Calculate Statistics for CSV """
    RawArray = None
    TransposeMeanArray = []
    TransposeSTDArray = []
    TransposeMedianArray = []
    TransposeMinArray = []
    TransposeMaxArray = []
    ReportCalculationMethodShortTitlesSpecial = [str(None), '', 'Start Step', 'End Step', 'Interval Length' ]
    # Traverse all the files in the file list to initialize Data
    for (FileNameEnum,FileName) in enumerate(FileNameList):
        # Load the file
        (DataColumns,Data) = ImportDataFromCSV(FileName, ImportColumnNames = False, ConvertTextToProperDataType = True, TextCellsAllowed = True)
        # Transpose the data back so it can be handled as originally generated
        RowValues = map(lambda *Entry: list(Entry), *Data)
        # Extract the OverallNumberOfRows
        OverallNumberOfRows = len(RowValues)
        # For the First pass only - create Empty Arrays for Results
        if FileNameEnum == 0:
            RawArray = [None]*(OverallNumberOfRows)
            MeanArray = [None]*(OverallNumberOfRows)
            STDArray = [None]*(OverallNumberOfRows)
            MedianArray = [None]*(OverallNumberOfRows)
            MinArray = [None]*(OverallNumberOfRows)
            MaxArray = [None]*(OverallNumberOfRows)
        CountFromHeader = 0
        # The new arrays have to be initialized to the correct size for each
        # column and also include the number of repetitions at the end.
        # Therefore another pass is made over each row to construct each cell
        for RowNum in range(OverallNumberOfRows):
            # Note that stratification information will exist in 
            # the fourth column - index 3 since the first 3 entries
            # are project information.
            if IsStr(RowValues[RowNum][3]) and RowValues[RowNum][3].startswith(ReportStratificationHeader):
                CountFromHeader = 0
            # Check that number of columns is matching
            if RowNum == 1:
                # The number of columns can be deduced from the titles row
                NumberOfColumns = len(RowValues[RowNum])
            elif CountFromHeader != 0:
                # validate rectangular array except from headers
                if len(RowValues[RowNum]) != NumberOfColumns:
                    raise ValueError, 'ASSERTION ERROR: The number of columns in Row #' +str(RowNum) + ' is ' + str(NumberOfColumns) + '. It is not the same as previous rows: '+ str(NumberOfColumns) + ' This indicates a problem in converting the report. Check that there are no delimiter characters such as ''|'' or '','' or ''\\n'' in table column labels.'
            if CountFromHeader < 3:
                # Add the repetition count column
                RowValues[RowNum].append(Iif(CountFromHeader == 1, 'Repetition count', ''))
                Row = RowValues[RowNum][:]
            else:
                # Copy the first 3 columns that describe project information
                # These were artificially added at CSV file generation
                RowValues[RowNum].append(None) 
                Row = RowValues[RowNum][0:3]+[None]*(NumberOfColumns-3) + [len(FileNameList)]
            # Now initialize the results arrays. Do this only for the first file
            if FileNameEnum == 0:
                MeanArray[RowNum] = Row[:]
                STDArray[RowNum] = Row[:]
                MedianArray[RowNum] = Row[:]
                MinArray[RowNum] = Row[:]
                MaxArray[RowNum] = Row[:]
                RawArray[RowNum] = Row[:]
            if CountFromHeader >= 3:
                # now look specifically at columns and cells
                # Note that the last added column is not traversed
                # also start calculations ignoring the first 3 headers 
                # containing the project, model, and  population titles
                for ColNum in range(3, NumberOfColumns):
                    # Index 2 in rows means skipping the first two columns
                    # that include the calculation description
                    if str(RowValues[2][ColNum]).strip() in ReportCalculationMethodShortTitlesSpecial:
                        # Columns with interval data or no data are just copied
                        StatInitCellValue = RowValues[RowNum][ColNum]
                        CellValue = None
                    else:
                        # Initialize the raw array 
                        StatInitCellValue = None
                        CellValue = RowValues[RowNum][ColNum]
                    # If this is the first file
                    if FileNameEnum == 0:
                        RawArray[RowNum][ColNum] = [CellValue]
                        MeanArray[RowNum][ColNum] = StatInitCellValue
                        STDArray[RowNum][ColNum] = StatInitCellValue
                        MedianArray[RowNum][ColNum] = StatInitCellValue
                        MinArray[RowNum][ColNum] = StatInitCellValue
                        MaxArray[RowNum][ColNum] = StatInitCellValue
                    else:
                        # if this is not the first file, accumulate statistics
                        # as a sublist
                        RawArray[RowNum][ColNum].append(CellValue)
            # Increase the header count 
            CountFromHeader = CountFromHeader + 1

    # Loop again through rows to calculate statistics for the RawData
    # collected in the previous pass
    CountFromHeader = 0
    for RowNum in range(OverallNumberOfRows):
        # Detect new startification 
        # Note that stratification information will be exist in 
        # the fourth column - index 3 since the first 3 entries
        # are project information
        if IsStr(RowValues[RowNum][3]) and RowValues[RowNum][3].startswith(ReportStratificationHeader):
            CountFromHeader = 0
        # Process only data - ignore calculation method headers
        if CountFromHeader >=3:
            # Start calculations ignoring the first 3 headers containing the
            # project, model, and  population titles
            for ColNum in range(3, NumberOfColumns+1):
                # Check that the calcuation method found in column index 2
                # is valid for statistical analysis. The calculation method
                # must always be in that position since the header is
                # forced at the start of the report.
                if str(RowValues[2][ColNum]).strip() not in ReportCalculationMethodShortTitlesSpecial:
                    # Prepare data in the cells.
                    FilteredForNoneValues = filter (lambda Entry: Entry != None, RawArray[RowNum][ColNum])
                    if FilteredForNoneValues == []:
                        # If no values are left, report None for thst cell
                        MeanArray[RowNum][ColNum] = None
                        STDArray[RowNum][ColNum] = None
                        MedianArray[RowNum][ColNum] = None
                        MinArray[RowNum][ColNum] = None
                        MaxArray[RowNum][ColNum] = None
                    else:
                        # If no None are left, calculate
                        MeanArray[RowNum][ColNum] = numpy.mean(FilteredForNoneValues)
                        if len(FilteredForNoneValues)>1:
                            # If there are enough elements use STD calculation
                            STDArray[RowNum][ColNum] = numpy.std(a = FilteredForNoneValues, ddof = 1)
                        else:
                            # If only 1 element is defined, return NaN
                            STDArray[RowNum][ColNum] = NaN
                        MedianArray[RowNum][ColNum] = numpy.median(FilteredForNoneValues)
                        MinArray[RowNum][ColNum] = min(FilteredForNoneValues)
                        MaxArray[RowNum][ColNum] = max(FilteredForNoneValues)
        # Increase the header count 
        CountFromHeader = CountFromHeader + 1
    # Write results to file
    # transpose the text before writing it to file, since the transposed
    # version is easier to read by a human.
    TransposeMeanArray=map(None,*MeanArray)
    TransposeSTDArray=map(None,*STDArray)
    TransposeMedianArray=map(None,*MedianArray)
    TransposeMinArray=map(None,*MinArray)
    TransposeMaxArray=map(None,*MaxArray)
    ExportDataToCSV(OutputFileNamePrefix + 'Mean.csv',TransposeMeanArray)
    ExportDataToCSV(OutputFileNamePrefix + 'STD.csv',TransposeSTDArray)
    ExportDataToCSV(OutputFileNamePrefix + 'Median.csv',TransposeMedianArray)
    ExportDataToCSV(OutputFileNamePrefix + 'Min.csv',TransposeMinArray)
    ExportDataToCSV(OutputFileNamePrefix + 'Max.csv',TransposeMaxArray)
    # Return the transposed report arrays
    return (TransposeMeanArray, TransposeSTDArray, TransposeMedianArray, TransposeMinArray, TransposeMaxArray)

  
def AddNewCalcID(self, Entry, ProjectBypassID = 0):
    """Add a new record to a collection and reset the ID of the record"""
    # If ID is not defined, i.e. 0 - add the ID
    if Entry.ID == 0:
        # Calculate get max key value or 0 if empty list and raise by 1
        EntryID = max( self.keys() or [0,] ) + 1
        Entry.ID = EntryID
    else:
        if self.has_key(Entry.ID):
            # Note that this an assertion error for any entity other than
            # parameters (other entities should not have the same key)
            raise KeyError, 'Add New Record Key Error: Cannot add a new record an entry with the key ' + str(Entry.ID) + ' Already exists in an instance of the ' + ClassDescriptionDict[self.__class__.__name__]     
    self[Entry.ID] = Entry
    # Mark the data as dirty as it was just changed
    AccessDirtyStatus(True)    
    return Entry


def CopyRecordInCollection(self, SourceID, NewName = None):
    """ Copies the source ID to a new record, try using the NewName """
    if not self.has_key(SourceID):
        raise KeyError, 'ASSERTION ERROR: Cannot copy record as the ID key ' + str(SourceID) + ' is invalid in the instance of the ' + ClassDescriptionDict[self.__class__.__name__]
    NewRecord = self[SourceID].Copy(NewName)
    Entry = self.AddNew(NewRecord)
    return Entry


def DeleteByID(self, ID, CheckForModify = False, ProjectBypassID = 0):
    """Deletes a record from a collection given its key ID"""
    # CheckForModify is true if checking only for modification.
    # if ProjectBypassID is not zero, then that project will not block
    # modification of certain entities, unless it is locked.
    if not self.has_key(ID):
        raise KeyError, 'ASSERTION ERROR: Cannot delete record as the ID key ' + str(ID) + ' is invalid in the instance of the ' + ClassDescriptionDict[self.__class__.__name__] 
    else:
        try:
            self[ID].CheckDependencies(CheckForModify = CheckForModify, ProjectBypassID=ProjectBypassID)
            Entry = self[ID]
            del self[ID]
            # If this is not a modification deletion, reset all derived
            # records of the collection. Note that this should not cause an
            # Error and therefore it is safe during deletion and modification
            # should not trigger such modification
            # Mark the data as dirty as it was just changed
            if not CheckForModify:
                ResetDerivedFrom(self,ID)
            AccessDirtyStatus(True)        
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Deletion Error: An Error was encountered while deleting the entry described as "' + self.ID2Name(ID) +'" in the ' + ClassDescriptionDict[self.__class__.__name__] + ' . Here are additional details:' + str(ExceptValue)
    # Return the Deleted Entry to allow undoing deletion by Modify
    return Entry


def ModifyByID(self, ID, NewEntry, ProjectBypassID = 0):
    """Modifies the Entry in a collection to the given ID to NewEntry"""
    # if ProjectBypassID is not zero, then that project will not block
    # modification of certain entities, unless it is locked.
    if not self.has_key(ID):
        raise KeyError, 'ASSERTION ERROR: Cannot modify record as the ID key' + str(ID) + ' is invalid in the ' + ClassDescriptionDict[self.__class__.__name__] 
    else:
        # If the record has the field CreatedOn, then retain the original.
        # Check if this field exists before doing so
        if hasattr(self[ID],'CreatedOn'):
            OriginalTime = self[ID].CreatedOn
            NewEntry.CreatedOn = OriginalTime
        # Also try to set the ID of the NewEntry to the modified ID. This is
        # possible only when NewEntry has an ID field
        if 'ID' in dir(NewEntry):
            if NewEntry.ID not in [0,ID]:
                raise ValueError, 'ASSERITON ERROR: The new record has the ID "' + str(NewEntry.ID) +'" while the old record has the ID,"' + str(ID) +'" in the ' + ClassDescriptionDict[self.__class__.__name__] + '. Problem encountered while undoing deletion, when addition did not succeed. Here are additional details while undoing deletion.'
            NewEntry.ID = ID
        # Current implementation may change. For now the record is deleted and
        # then added to the collection. While deleting perform checks required
        # for modification that are less strict and will not block modification
        # due to dependency
        OldEntry = self.Delete(ID, CheckForModify = True, ProjectBypassID = ProjectBypassID)
        # Since the record is deleted and adding a new record may cause an
        # error, try to catch errors during adding so that deletion may be
        # undone
        try:
            RetVal = self.AddNew(NewEntry, ProjectBypassID)
            # Mark the data as dirty as it was just changed
            AccessDirtyStatus(True)        
        except:
            # If addition did not succeed, restore the deleted OldEntry.
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            # If adding is unsuccessful, raise an assertion error, otherwise,
            # communicate the error to the user
            try:
                RetVal = self.AddNew(OldEntry, ProjectBypassID)
            except:
                (ExceptType1, ExceptValue1, ExceptTraceback1) = sys.exc_info()
                raise ValueError, 'ASSERITON ERROR: an Error was encountered while modifying the ID "' + str(ID) +'" in the ' + ClassDescriptionDict[self.__class__.__name__] + '. Problem encountered while undoing deletion, when addition did not succeed. Here are additional details while undoing deletion:' + str(ExceptValue1) + ' . Here are additional details about failure to add a new record' +  str(ExceptValue1)
            raise ValueError, 'Modification Error: An Error was encountered while modifying the entry described as "' + self.ID2Name(ID) +'" in the ' + ClassDescriptionDict[self.__class__.__name__] + '. Adding the new record did not succeed. Here are additional details about failure to add a new record' +  str(ExceptValue)         
    return RetVal


def GenerateReportForCollection(self, FormatOptions = None):
    """ Generate the report for all entities in the collection """
    KeyFilter = HandleOption('KeyFilter', FormatOptions, None)
    if KeyFilter == None:
        KeyFilter = sorted(self.keys())
    ReportString = ''
    for ID in KeyFilter:
        if ID not in self.keys():
            raise ValueError, 'ASSERTION ERROR: An Error was encountered while reporting the ID "' + str(ID) +'" in the ' + ClassDescriptionDict[self.__class__.__name__] + ' does not exist - The filter should be checked.'
        else:
            ReportString = ReportString + self[ID].GenerateReport(FormatOptions)
    return ReportString


def EntityNameByID(self, InputID):
    """ Returns a string of names for a sequence of IDs """
    # This is useful to generate names for ID sequences for error messages
    if IsList(InputID):
        NamesList = map(lambda Entry: self[Entry].Describe() + ', ', InputID)
        RetVal = ''.join(NamesList)[:-2]
    elif InputID == None:
        # In this case, just show the entire collection
        NamesList = map(lambda Entry: Entry.Describe() + ', ', self)
        RetVal = ''.join(NamesList)[:-2]        
    else:
        # This is the case a single ID was supplied not in a sequence
        RetVal = self[InputID].Describe()
    return RetVal



def ResetDerivedFrom (self, ID):
    """ Resets the DerviedFrom field in other records in the collection"""
    # The function works for all entities with the DerivedFrom field
    # use the first item in the collection to dynamically determine this
    for Entry in self.itervalues():
        if 'DerivedFrom' in dir(Entry):
            if Entry.DerivedFrom==ID:
                self[Entry.ID].DerivedFrom = 0
                AccessDirtyStatus(True)
        else:
            # If any item does not have a derived from field,
            # do not continue the checks, just break the loop and get out
            # this means that this class does not support this feature
            break
    return


def ExportInstance(self, FileName, Overwrite = True):
    """Saves the object instance using pickle in the given filename"""
    try:
        # If overwrite is not allowed, check for existence of file name
        if Overwrite == False:
            if os.path.isfile(FileName):
                raise ValueError, 'Export Instance Error: A file with the name "'+ FileName + ' already exists. The filename should be replaced with another name that is valid.'
        # Open the file
        File = open (FileName , 'w')
        # Dump the data to file using pickle
        pickle.dump(self,File)
        # Close the file
        File.close()
        # Dirty status unknown and therefore no change is made in it
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Export Error: Could not properly export to file. Here are additional details on the error: ' +  str(ExceptValue)
    return


def SaveInstance(self, FileName, CompressFile = False, VariableName = None):
    """Saves only the object to a given file name"""
    # Important Note: Saving only the instance may not be an efficient
    # way to work as this may create duplicate entries in the zip file
    # Consider saving all parameters instead. Note that for this reason
    # This function and its load counterpart may become obsolete
    #    
    # Strip the 'class' word from the class name to get instance name
    try:
        if VariableName == None:
            VariableName = self.__class__.__name__[:-5]
        # First, pickle the objects into a string
        try:
            # try pickling directly to string
            PickledString = pickle.dumps(self)
        except:
            MessageToUser("Save Warning: A problem was encountered while saving - trying an alternate save method")
            try:
                # if memory does not allow this, try using a file 
                (TempFileDescriptor, TempFileName) = tempfile.mkstemp ( TempSuffix, DefaultTemporaryFileNamePrefix , SessionTempDirecory , True)
                # Now actually create the file
                TempFile = os.fdopen(TempFileDescriptor,'w')
                pickle.dump(self,TempFile)
                TempFile.close()
                # now reopen the file and read it into the string
                TempFile = open(TempFileName,'r')
                PickledString = TempFile.read()
                TempFile.close()
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                raise ValueError, 'Save Error: Could not prepare the file. Here are additional details on the error: ' +  str(ExceptValue)
            else:
                MessageToUser("Save Info: Alternate save method successful")
        #Open the archive file in append mode
        TheOutputFile = zipfile.ZipFile(FileName,'a',Iif(CompressFile,zipfile.ZIP_DEFLATED,zipfile.ZIP_STORED))
        # Now use the strings to populate the file
        TheOutputFile.writestr(VariableName + AppFileNameExtension , PickledString)
        TheOutputFile.close()
        # Dirty Status unknown and therefore no change is made in it
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Save Error: Could not properly save to file. Here are additional details on the error: ' +  str(ExceptValue)
    return


def LoadInstance(self, FileName, VariableName = None):
    """Loads instance data from single file, overriding current data """
    # Important Note: Saving only the instance may not be an efficient
    # way to work as saving an instance may create duplicate entries in the zip
    # file. Consider saving all parameters instead. Note that for this reason
    # This function and its save counterpart may become obsolete
    #
    # If needed Strip the 'class' word from the class name to get instance name
    try:
        if VariableName == None:
            VariableName = self.__class__.__name__[:-5]
        # Open the archive file
        TheInputFile = zipfile.ZipFile(FileName,'r')
        # Read the strings into the global
        StringToUnpickle = TheInputFile.read( VariableName + AppFileNameExtension )
        TheInputFile.close()
        VarData = pickle.loads(StringToUnpickle)
        globals()[VariableName] = VarData
        # Mark the data as dirty as it was just changed
        # Dirty Status unknown and therefore no change is made in it
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Load Error: Could not properly Load the file. Here are additional details on the error: ' +  str(ExceptValue)
    return


def ImportInstance(self, FileName, VariableName = None):
    """Returns the object instance using pickle from the given filename"""
    # Note that to use this function, the following usage is appropriate:
    # InstanceName = InstanceName.ImportInstance(Filename)
    #
    # If needed Strip the 'class' word from the class name to get instance name
    try:
        if VariableName == None:
            VariableName = self.__class__.__name__[:-5]
        # Open the file
        if not os.path.isfile(FileName):
            raise ValueError, 'Import Instance Error: A file with the name "'+ FileName + ' does not exist. The filename should be replaced with another name that is valid.'
        File = open (FileName , 'r')
        # load the object from file using pickle
        StringToUnpickle = File.read()
        File.close()
        VarData = pickle.loads(StringToUnpickle)
        globals()[VariableName] = VarData
        # Mark the data as dirty as it was just changed
        AccessDirtyStatus(True)
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Import Error: Could not properly Load the file. Here are additional details on the error: ' +  str(ExceptValue)
    return


def AccessDirtyStatus(DirtyStatus = None):
    """get or set the Dirty status of the Database"""
    # This function is used to query/set/reset the dirty flag through
    # one interface. One global variable that belongs to this module will
    # be accessed by calling this function.
    # If input is not supplied or Non is supplied, the function will return
    # the current value of the flag. If the input is Boolean the flag will be
    # set/reset according to the flag.
    # The function replaces in a sense the concept of a static variable in
    # other languages
    global DirtyStatusFlag
    # First Check the input
    if IsBoolean(DirtyStatus):
        # If the input is a Boolean, then set the global dirty status flag
        # to the supplied value
        DirtyStatusFlag = [DirtyStatus]
    elif DirtyStatus != None:
        raise ValueError, 'ASSERTION ERROR: The dirty status input must be a Boolean or None'
    # Return the current flag value
    return DirtyStatusFlag[0]


class ParamsClass(dict):
    """A dictionary to hold Param"""

    #Add new method
    def AddNew(self, Entry, ProjectBypassID = 0):
        """Add a new parameter to Params"""
        if self.has_key(str(Entry)):
            raise KeyError, 'Add New Parameter Error: Cannot add a new record since an entry with the key "' + str(Entry) + '" Already exists in the ' + ClassDescriptionDict[self.__class__.__name__] 
        self[str(Entry)] = Entry
        # Mark the data as dirty as it was just changed
        AccessDirtyStatus(True)
        return Entry


    #Delete method
    def Delete(self, ID, CheckForModify = False, ProjectBypassID = 0):
        """Delete parameter from Params"""
        if not self.has_key(ID):
            raise KeyError, 'ASSERTION ERROR: Cannot delete record as the ID key ' + str(ID) + ' is an invalid ID in ' + ClassDescriptionDict[self.__class__.__name__] 
        else:
            if self[ID].ParameterType == 'State Indicator':
                raise ValueError, 'Deletion Error: Deletion of the state indicator ' + self.ID2Name(ID) + ' is not allowed through parameter manipulation. To delete a state indicator, the state that created this state indicator should be deleted.'
            else:
                try:
                    self[ID].CheckDependencies(CheckForModify = CheckForModify, ProjectBypassID=ProjectBypassID)
                    Entry = self[ID]
                    del self[ID]
                except:
                    (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                    raise ValueError, 'Deletion Error: An error was encountered while deleting the entry described as ' + self.ID2Name(ID) + ' in the ' + ClassDescriptionDict[self.__class__.__name__] + '. Here are additional details:' + str(ExceptValue)
        # Mark the data as dirty as it was just changed
        AccessDirtyStatus(True)
        return Entry

    Modify = ModifyByID
    
    Copy = CopyRecordInCollection

    ID2Name = EntityNameByID

    # Export, Save and Load methods
    Import = ImportInstance
    Export = ExportInstance
    Save = SaveInstance
    Load = LoadInstance
    GenerateReport = GenerateReportForCollection    



class TransitionsClass(dict):
    """A dictionary to hold Transition"""

    def AddNew(self,Entry, ProjectBypassID = 0):
        """Add a new Transition to Transitions"""
        if self.has_key((Entry.StudyModelID , Entry.FromState , Entry.ToState)):
            raise KeyError, 'Add New Entry Error: Cannot add a new record since a transition between the same states in the same study/model already exists in  the ' + ClassDescriptionDict[self.__class__.__name__] + ' . The new transition is: ' + Entry.Describe() 
        try:
            Entry.CheckDependencies(CheckForModify = True, ProjectBypassID = ProjectBypassID)
        except:
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Add New Entry Error: Cannot add the new record ' + Entry.Describe() + ' to the ' + ClassDescriptionDict[self.__class__.__name__] + '. Here are additional details on the error:' + str(ExceptValue)

        self[(Entry.StudyModelID , Entry.FromState , Entry.ToState)] = Entry
        # Mark the data as dirty as it was just changed
        AccessDirtyStatus(True)
        return Entry
    
    Delete = DeleteByID
    
    Modify = ModifyByID

    # Note that the input argument name changes for a transition. However, the
    # same code can be used as NewName replaces NewStudyID, However the default
    # of None will cause an error copying, and therefore an argument should be
    # defined when using it.        
    
    Copy = CopyRecordInCollection
    
    ID2Name = EntityNameByID

    # Export, Save and Load methods
    Import = ImportInstance
    Export = ExportInstance
    Save = SaveInstance
    Load = LoadInstance
    GenerateReport = GenerateReportForCollection    



class StatesClass(dict):
    """A dictionary to hold State"""

    def AddNew (self,Entry, ProjectBypassID = 0):
        """ Add a new state and its associated parameters """
        # Verify that no parameter with the same state name exists.
        StateNames = map (lambda (StateKey, StateEntry) : StateEntry.Name , States.iteritems())
        if Entry.Name in StateNames:
            raise ValueError, 'Add New Record Error: A State with the name "' + Entry.Name +'" already exists in the ' + ClassDescriptionDict[self.__class__.__name__]
        # Also checks against close state names that will result
        # in an ambiguity of parameter names, This will be caught
        # by checking the parameters. Yet this is here to raise
        # a more meaningful error to the user
        ConvertedStateNames = map (lambda (StateKey, StateEntry) : StateEntry.ConvertNameToParam() , States.iteritems())
        SimilarStates = FilterByAnother(StateNames, map ( lambda ConvertedStateName: Entry.ConvertNameToParam() == ConvertedStateName, ConvertedStateNames))
        if SimilarStates != []:
            raise ValueError, 'Add New Record Error: A State with the name ' + Entry.Name +' resembles a state with a similar name ' + str(SimilarStates) + ' that will convert to a state indicator with the same name when spaces are replaced with underscore characters. Therefore it is not possible to add that state to the ' + ClassDescriptionDict[self.__class__.__name__] + '. Please choose a new state name.'
        # Check consistency of Pooling States and sub-processes with recursion
        # to prevent overlap. If no exception raised, one can continue
        (AllStates, IsSubProcess, NestingLevel) = Entry.FindChildStates ( CurrentNestingLevel = 0)
        # Create all possible extensions
        ParamNames = Entry.GenerateAllStateIndicatorNames()
        # Check and Create State Indicator Parameters with
        # all possible extensions
        for ParamName in ParamNames:
            if Params.has_key(ParamName):
                raise ValueError, 'Add New Record Error: Cannot add a state since an existing parameter blocks the creation of the state indicator ' + ParamName + ' in the parameter collection. To create the state, delete or rename the already existing parameter in the parameters collection.'
        # In case this is a joiner state, check that it points to a valid
        # splitter state - Note that this was not possible to do at the record
        # level since only superficial tests that do not access the collection
        # information are made at that level
        if Entry.JoinerOfSplitter != 0:
            if not States.has_key(Entry.JoinerOfSplitter):
                raise ValueError, 'ASSERTION ERROR: The State "' + Entry.Name +'" is joining a state that does not exist'
            if not States[Entry.JoinerOfSplitter].IsSplit:
                raise ValueError, 'ASSERTION ERROR: The State "' + Entry.Name +'" is joining a state that is not a splitter state'
        # Add the state to the state list            
        AddNewCalcID(self,Entry)
        # Add the parameters to the parameter list. Although at this point is
        # unlikely, if an error occurs delete the State and raise an error
        AddedParams = []
        try:
            for ParamName in ParamNames:
                NewParam = Param(Name = ParamName, Formula = '' , ParameterType = 'State Indicator' , ValidationRuleParams = '[0,1]', Notes =  StateIndicatorNotePrefix + Entry.Name , Tags = Entry.ID)
                AddedParam = Params.AddNew(NewParam, ProjectBypassID)
                # Keep track of added params
                AddedParams.append(AddedParam)
        except:
            # Delete the added state from the states list
            del self[Entry.ID]
            # Delete the already added params
            for AddedParam in AddedParams:
                # Bypass all check while doing so since there were just added
                del Params[str(AddedParam)]
            # Re-raise the error
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Add New Record Error: The state indicator parameter corresponding to the state "' + Entry.Name + '" cannot be created, Therefore the state cannot be added to the states list. Here are additional details:' + str(ExceptValue)            
        # Mark the data as dirty as it was just changed
        AccessDirtyStatus(True)
        return Entry

    def Delete(self, ID, CheckForModify = False, ProjectBypassID = 0):
        """ Delete a State and its associated Parameters """
        def RestoreDeletedParams(DeletedParams):
            """ Internal function to restore deleted parameters """
            # Restore the deleted parameters - this should never happen.
            # The code here is stricter than needed to avoid any unforeseen
            # issues that may arise in the future. This code is more of a
            # safeguard.
            for DeletedParam in DeletedParams:
                Params[str(DeletedParam)] = DeletedParam
        if not self.has_key(ID):
            raise KeyError, 'ASSERTION ERROR: Cannot delete record as the ID key ' + str(ID) + ' is invalid in the instance of ' + ClassDescriptionDict[self.__class__.__name__]
        else:
            self[ID].CheckDependencies(CheckForModify = CheckForModify, ProjectBypassID=ProjectBypassID)
            # Extract the parameter names that require deletion with the state
            ParamNames = self[ID].GenerateAllStateIndicatorNames()
            # Keep a list of deletions
            DeletedParams=[]
            try:
                # Try to delete each one
                for ParamName in ParamNames:
                    if not Params.has_key(ParamName):
                        raise ValueError, 'ASSERTION ERROR: The state indicator with the name ' + ParamName + ' does not exist in the parameter table whereas  it should exist as a counterpart of a state. It was somehow deleted before and by this the data definitions were corrupted.'
                    DeletedParams = DeletedParams + [Params.pop(ParamName)]
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                # Restore deleted parameters to maintain data integrity 
                RestoreDeletedParams(DeletedParams)
                # now raise an error
                raise ValueError, 'Deletion Error: An Error was encountered while deleting the state indicator ' + ParamName +' corresponding to the State "' + self[ID].Name + '". Here are additional details:' + str(ExceptValue) 
            try:
                # Delete the state record
                Entry = self[ID]
                del self[ID]
            except:
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                # Restore deleted parameters to maintain data integrity 
                RestoreDeletedParams(DeletedParams)
                raise ValueError, 'Deletion Error: An Error was encountered while deleting the state ' + self[ID].Name + ' from the ' + ClassDescriptionDict[self.__class__.__name__] + '. Here are additional details:' + str(ExceptValue)
        # Mark the data as dirty as it was just changed
        AccessDirtyStatus(True)
        return Entry

    Modify = ModifyByID

    Copy = CopyRecordInCollection

    ID2Name = EntityNameByID
    
    # Export, Save and Load methods
    Import = ImportInstance
    Export = ExportInstance
    Save = SaveInstance
    Load = LoadInstance
    GenerateReport = GenerateReportForCollection    


class StudyModelsClass(dict):
    """A dictionary to hold StudyModel"""

    # Add a method for adding a new parameter
    AddNew = AddNewCalcID
    Delete = DeleteByID
    Modify = ModifyByID

    def Copy(self, SourceID, NewName = None):
        """ Copies the source ID to a new record, try using the NewName """
        if not self.has_key(SourceID):
            raise KeyError, 'ASSERTION ERROR: Cannot copy record as the ID key ' + str(SourceID) + ' is invalid in the instance of ' + ClassDescriptionDict[self.__class__.__name__] 
        # Note that this kind of copy, copies all transitions as well.
        try:
            # Add the new study  record to the collection
            NewRecord = self[SourceID].Copy(NewName)
            NewStudyModelEntry = self.AddNew(NewRecord)
        except:
            # Re-raise the error
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Copy Record Error: Copying the study/model was unsuccessful when adding the study model record. Here are additional details: ' + str(ExceptValue)
        # Copy all the relevant transitions and add them to the transition
        # collection
        NewCreatedTransitions = []
        try:
            # Transitions are sorted by their order in the subprocess to allow
            # introducing them in proper order and avoid defining them in an
            # order such as Joiners are connected before their splitters
            TransKeys = self[SourceID].FindTransitions('SortByOrderInSubProcess')
            for TransKey in TransKeys:
                NewTransKey = Transitions.Copy(TransKey, NewStudyModelEntry.ID)
                NewCreatedTransitions.append(NewTransKey)
        except:
            # If this point was reached, then there may be a need to remove
            # the newly created  transitions
            for NewCreatedTransition in NewCreatedTransitions:
                del Transitions[NewCreatedTransition]               
            # Now also remove the Copied Study/Model
            del self[NewStudyModelEntry.ID]
            # Re-raise the error
            (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
            raise ValueError, 'Copy Record Error: Copying the Study/Model was unsuccessful when adding the transitions related to the study model record. Here are additional details:' + str(ExceptValue)
        return NewStudyModelEntry

    ID2Name = EntityNameByID
    
    # Export, Save and Load methods
    Import = ImportInstance
    Export = ExportInstance
    Save = SaveInstance
    Load = LoadInstance
    GenerateReport = GenerateReportForCollection    


class PopulationSetsClass(dict):
    """A dictionary to hold PopulationSet"""

    # Add a method for adding a new parameter
    AddNew = AddNewCalcID
    Delete = DeleteByID
    Modify = ModifyByID
    Copy = CopyRecordInCollection

    ID2Name = EntityNameByID

    # Export, Save and Load methods
    Import = ImportInstance
    Export = ExportInstance
    Save = SaveInstance
    Load = LoadInstance
    GenerateReport = GenerateReportForCollection    


class ProjectsClass(dict):
    """A dictionary to hold Project"""

    # Add a method for adding a new parameter
    AddNew = AddNewCalcID
    Delete = DeleteByID
    Modify = ModifyByID
    Copy = CopyRecordInCollection

    ID2Name = EntityNameByID

    # Export, Save and Load methods
    Import = ImportInstance
    Export = ExportInstance
    Save = SaveInstance
    Load = LoadInstance
    GenerateReport = GenerateReportForCollection    


class SimulationResultsClass(dict):
    """A dictionary to hold Results"""

    # Add a method for adding a new parameter
    AddNew = AddNewCalcID
    Delete = DeleteByID
    Modify = ModifyByID

    ID2Name = EntityNameByID

    # Export, Save and Load methods
    Import = ImportInstance
    Export = ExportInstance
    Save = SaveInstance
    Load = LoadInstance
    GenerateReport = GenerateReportForCollection    


def ReconstructDataFileAndCheckCompatibility(InputFileName, JustCheckCompatibility = False, RegenerationScriptName = None, ConvertResults = False, KnownNumberOfErrors = 0, CatchError = True, OutputModelFileName = None):
    """ This function converts an old file to a new data version """
    # InputFileName is the name of the file to be loaded.
    # If RegenerationScriptName is None then the system will run the conversion
    # script it generates. Otherwise, the system will generate the conversion
    # script under the name given and will not execute it.
    # If JustCheckCompatibility is True, the system notifies that the file
    # version is not compatible with the current version, i.e. requires some
    # sort of conversion. 
    # By default No Errors are allowed to be generated during running the
    # conversion script. This should be kept this way and changed with caution
    # by a programmer only when required. This option should not be exposed
    # to the user.
    # By default, simulation results will not be converted since this
    # requires much effort and time and may not fit new versions of code.
    # However, a user can request to convert these as well by setting
    # ConvertResults to true.
    # If CatchError is set to True then no errors are geneated by the function
    # Instead messages are generated for the user and the function returns
    # without error. In this case the DidLoad flag is returned as True and data
    # is not loaded.
    # If OutputModelFileName is not None, then it will determine the output
    # model file name to be saved after reconstruction from code.
    # The function returns a tuple of the form:
    # (FileVersion, IsCompatible, IsUpgradable, DidLoad, HasResults)
    # FileVersion stands for the input filename version
    # IsCompatible is True if a matching version to the current file
    # IsUpgradable is True if can be upgraded to the current version
    # DidLoad is true is data was succesfully loaded
    # HasResults is True if there are any simulation results stored in the file

    def IsCompatibleVersion (AnotherVersion):
        "Returns True if AnotherVersion is compatible with the current version"
        # This version is compatible only with itself
        RetVal = (AnotherVersion == Version)
        return RetVal

    def CanVersionBeUpgraded (AnotherVersion):
        "Returns True if AnotherVersion can be upgraded to the current version"
        # Only versions with datadef lower or equal than the current version 
        # can be upgraded to the current version. The Last text 
        # identifier in the version muat match. Future versions may change.
        RetVal = AnotherVersion[0:4] <= Version[0:4] and AnotherVersion[4] == Version[4] 
        return RetVal
    
    def DeleteTempLoadedObjects():
        """ Delete the temp objects created during load to save space """
        for VariableName in GlobalsInDB:
            VarNameToDelete = 'Temp' + VariableName
            if VarNameToDelete in globals().keys():
                del globals()[VarNameToDelete]
        return None

    # Update old version with new functions to help with the transition
    LoadAllData(InputFileName, 'Temp')
    # check if there is a need to create a simulation file. It is created if
    # the input defines RegenerationScriptName or if the loaded version does
    # not have a proper version.
    FileVersion = globals()['TempVersion']
    IsCompatible = IsCompatibleVersion(FileVersion)
    IsUpgradable = CanVersionBeUpgraded(FileVersion)
    DidLoad = False
    HasResults = 'TempSimulationResults' in globals().keys()
    try: 
        if not IsUpgradable and not IsCompatible:
            raise ValueError, 'Bridge File Version Error: The file version to be converted was created with a more recent code version ' + str(FileVersion)  + ' than the current code version ' + str(Version)  + ' . Please update your software version to allow loading this file as it can not be loaded with the current version'
        if JustCheckCompatibility and not IsCompatible:
            raise ValueError, 'Bridge File Version Error: The file version that created this file ' + str(FileVersion)  + ' is not compatible with a the current version ' + str(Version)  + ' .'
        # Create a script file only if an upgrade is needed or requested by the user
        if not JustCheckCompatibility and (IsUpgradable or IsCompatible):
            # Create the header of the conversion file
            Out = ""
            Out = Out + "################################################################################\n"
            Out = Out + "# This script was automatically Generated on: "+ datetime.datetime.now().isoformat(" ")[:19] + "              #\n"
            Out = Out + "# by a utility in the Indirect Estimation and Simulation Tool (IEST).          #\n"
            Out = Out + "################################################################################\n"
            Out = Out + "import DataDef as DB\n"
            Out = Out + "import sys\n"
            Out = Out + "import traceback\n"
            # Define Inf,inf,NaN,nan constants since these may appear in data
            # These constants are overridden only if they do not exist yet
            Out = Out + "if 'Inf' not in globals().keys():"
            Out = Out + "    Inf = DB.Inf\n"
            Out = Out + "if 'NaN' not in globals().keys():"
            Out = Out + "    NaN = DB.NaN\n"
            Out = Out + "if 'inf' not in globals().keys():"
            Out = Out + "    inf = DB.inf\n"
            Out = Out + "if 'nan' not in globals().keys():"
            Out = Out + "    nan = DB.nan\n"
            Out = Out + "ErrorCount = []\n"
            Out = Out + "def AnalyzeVersionConversionError():\n"
            Out = Out + "    traceback.print_exc()\n"
            Out = Out + "    ErrorDetails = sys.exc_info()\n"
            Out = Out + "    ErrorCount.append(ErrorDetails)\n"
            Out = Out + "    if len(ErrorCount)>" + str(KnownNumberOfErrors) + ":\n"
            Out = Out + "        raise ValueError, 'Bridge File Version Error: Too many errors to proceed'\n"
            Out = Out + "    print  70*'*' \n"
            Out = Out + "    print  70*'*' \n"
            # This function should make sure conversion is ok for special characters
            # in string to be combined with the code string and still work
            ToStr = lambda String: repr(String)
            KeysToProcess = sorted(globals()['TempStates'].keys())
            # Pass through all the regular states
            while KeysToProcess != []:
                ID = KeysToProcess.pop(0)
                if 'Load' in DebugPrints:
                    MessageToUser ('Processing State ID ' + str(ID)+ '')
                Entry = globals()['TempStates'][ID]
                DependantNotYetRegistered = False
                for PooledID in Entry.ChildStates:
                    if PooledID in KeysToProcess:
                        DependantNotYetRegistered = True
                if Entry.JoinerOfSplitter != 0  and Entry.JoinerOfSplitter in KeysToProcess:
                    DependantNotYetRegistered = True                
                if DependantNotYetRegistered:
                    KeysToProcess.append(ID)
                    if 'Load' in DebugPrints:
                        MessageToUser ('***************ID ' + str(ID)+ ' passed***************')
                else:
                    Out = Out + "try: DB.States.AddNew( DB.State(ID = " + ToStr(Entry.ID) + ", Name = " + ToStr(Entry.Name) + ", Notes = " + ToStr(Entry.Notes) + ", IsSplit = " + ToStr(Entry.IsSplit) + ", JoinerOfSplitter = " + ToStr(Entry.JoinerOfSplitter) + ", IsEvent = " + ToStr(Entry.IsEvent) + ", IsTerminal = " + ToStr(Entry.IsTerminal) + ", ChildStates = " + ToStr(Entry.ChildStates) + "), ProjectBypassID = 0)\nexcept: AnalyzeVersionConversionError()\n"
            KeysToProcess = sorted(globals()['TempParams'].keys())
            while KeysToProcess != []:
                ID = KeysToProcess.pop(0)
                if 'Load' in DebugPrints:
                    MessageToUser ('Processing Param ' + str(ID)+ '')
                Entry = globals()['TempParams'][ID]
                DependantNotYetRegistered = False
                if Entry.Formula != '':
                    # Use code that detects all the used tokens
                    ExprText = Entry.Formula
                    # Start by detecting all tokens
                    TokensInfo = tokenize.generate_tokens(StringIO.StringIO(ExprText).readline)
                    for (TokenType, Token, TokenStart, TokenEnd, OriginalString) in TokensInfo:
                        # Check if the token is a string represents a parameter
                        if re.match(ParamTextMatchPattern,Token) != None and Token in KeysToProcess:
                             DependantNotYetRegistered = True
                if DependantNotYetRegistered:
                    KeysToProcess.append(ID)
                    if 'Load' in DebugPrints:
                        MessageToUser ('***************ID ' + str(ID)+ ' passed***************')
                # Modify System Option defaults if these are defined in the new
                # database
                elif (Entry.ParameterType == 'System Option') and (Entry in (DefaultSystemOptions.keys())):
                    Out = Out + "try: DB.Params.Modify( " + ToStr(Entry) + ", DB.Param(Name = " + ToStr(Entry)+ ", Formula = " + ToStr(Entry.Formula)+ ", ParameterType = " + ToStr(Entry.ParameterType)+ ", ValidationRuleParams = " + ToStr(Entry.ValidationRuleParams)+ ", Notes = " + ToStr(Entry.Notes)+ "), ProjectBypassID = 0)\nexcept: AnalyzeVersionConversionError()\n"
                # process only non state indicators and non System reserved as these
                # are already defined
                elif Entry.ParameterType not in ['State Indicator','System Reserved']:
                    Out = Out + "try: DB.Params.AddNew( DB.Param(Name = " + ToStr(Entry)+ ", Formula = " + ToStr(Entry.Formula)+ ", ParameterType = " + ToStr(Entry.ParameterType)+ ", ValidationRuleParams = " + ToStr(Entry.ValidationRuleParams)+ ", Notes = " + ToStr(Entry.Notes)+ "), ProjectBypassID = 0)\nexcept: AnalyzeVersionConversionError()\n"
            KeysToProcess = sorted(globals()['TempStudyModels'].keys())
            while KeysToProcess != []:
                ID = KeysToProcess.pop(0)
                if 'Load' in DebugPrints:
                    MessageToUser ('Processing StudyModel ID' + str(ID)+ '')
                Entry = globals()['TempStudyModels'][ID]
                DependantNotYetRegistered = False
                if Entry.DerivedFrom in KeysToProcess:
                    DependantNotYetRegistered = True
                if DependantNotYetRegistered:
                    KeysToProcess.append(ID)
                    if 'Load' in DebugPrints:
                        MessageToUser ('***************ID ' + str(ID)+ ' passed***************')
                else:
                    Out = Out + "try: DB.StudyModels.AddNew( DB.StudyModel(ID = " + ToStr(Entry.ID)+ ", Name = " + ToStr(Entry.Name)+ ", Notes = " + ToStr(Entry.Notes)+ ", DerivedFrom = " + ToStr(Entry.DerivedFrom)+ ", MainProcess = " + ToStr(Entry.MainProcess)+ "), ProjectBypassID = 0)\nexcept: AnalyzeVersionConversionError()\n"
            KeysToProcess = sorted(globals()['TempTransitions'].keys())
            while KeysToProcess != []:
                ID = KeysToProcess.pop(0)
                if 'Load' in DebugPrints:
                    MessageToUser ('Processing Transition ID' + str(ID)+ '')
                DependantNotYetRegistered = False
                # Wait with transitions into joiners after processing transitions
                # out of their prespective splitter states
                (CurrentStudyModelID, CurrentFromStateID, CurrentToStateID) = ID
                if CurrentToStateID != 0:
                    SplitterToFinish = globals()['TempStates'][CurrentToStateID].JoinerOfSplitter
                else:
                    SplitterToFinish = 0
                if SplitterToFinish != 0:
                    if (CurrentStudyModelID, SplitterToFinish) in map (lambda (StudyModelID, FromStateID, ToStateID): (StudyModelID, FromStateID), KeysToProcess):
                        DependantNotYetRegistered = True    
                Entry = globals()['TempTransitions'][ID]
                if DependantNotYetRegistered:
                    KeysToProcess.append(ID)
                    if 'Load' in DebugPrints:
                        MessageToUser ('***************ID ' + str(ID)+ ' passed***************')
                else:
                    Out = Out + "try: DB.Transitions.AddNew( DB.Transition(StudyModelID = " + ToStr(Entry.StudyModelID) + ", FromState = " + ToStr(Entry.FromState) + ", ToState = " + ToStr(Entry.ToState) + ", Probability = DB.Expr(" + ToStr(Entry.Probability) + "), Notes = " + ToStr(Entry.Notes)+ "), ProjectBypassID = 0)\nexcept: AnalyzeVersionConversionError()\n"
            KeysToProcess = sorted(globals()['TempPopulationSets'].keys())
            while KeysToProcess != []:
                ID = KeysToProcess.pop(0)
                if 'Load' in DebugPrints:
                    MessageToUser ('Processing Population Set ID' + str(ID)+ '')
                Entry = globals()['TempPopulationSets'][ID]
                DependantNotYetRegistered = False
                if Entry.DerivedFrom in KeysToProcess:
                    DependantNotYetRegistered = True
                if DependantNotYetRegistered:
                    KeysToProcess.append(ID)
                    if 'Load' in DebugPrints:
                        MessageToUser ('***************ID ' + str(ID)+ ' passed***************')
                else:
                    # Process Objectives - exist only from version (0,90,0,0) 
                    if FileVersion[:-1] < (0,90,0,0):
                        # before this version no objectives were defined
                        EntryObjectivesStr = "[]"
                    else:
                        # if versin is proper use the defined objectives
                        EntryObjectivesStr = ToStr(Entry.Objectives)                        
                    Out = Out + "try: DB.PopulationSets.AddNew( DB.PopulationSet(ID = " + ToStr(Entry.ID)+ ", Name = " + ToStr(Entry.Name)+ ", Source = " + ToStr(Entry.Source)+ ", Notes = " + ToStr(Entry.Notes)+ ", DerivedFrom = " + ToStr(Entry.DerivedFrom)+ ", DataColumns = " + ToStr(Entry.DataColumns)+ ", Data = " + ToStr(Entry.Data)+ ", Objectives = " + EntryObjectivesStr + " ), ProjectBypassID = 0)\nexcept: AnalyzeVersionConversionError()\n"
            KeysToProcess = sorted(globals()['TempProjects'].keys())
            while KeysToProcess != []:
                ID = KeysToProcess.pop(0)
                if 'Load' in DebugPrints:
                    MessageToUser ('Processing Project ID' + str(ID)+ '')
                Entry = globals()['TempProjects'][ID]
                DependantNotYetRegistered = False
                if Entry.DerivedFrom in KeysToProcess:
                    DependantNotYetRegistered = True
                if DependantNotYetRegistered:
                    KeysToProcess.append(ID)
                    if 'Load' in DebugPrints:
                        MessageToUser ('***************ID ' + str(ID)+ ' passed***************')
                else:
                    # Process the rules list:
                    Out = Out + "SimRuleList = []\n"
                    for Rule in Entry.SimulationRules:
                        # Define simulation Rules
                        Out = Out + "try: SimRuleList = SimRuleList + [ DB.SimulationRule(AffectedParam = " + ToStr(Rule.AffectedParam)+ ", SimulationPhase = " + ToStr(Rule.SimulationPhase)+ ", OccurrenceProbability = " + ToStr(Rule.OccurrenceProbability)+ ", AppliedFormula = " + ToStr(Rule.AppliedFormula)+ ", Notes = " + ToStr(Rule.Notes)+ ")]\nexcept: AnalyzeVersionConversionError()\n"
                    Out = Out + "try: DB.Projects.AddNew( DB.Project(ID = " + ToStr(Entry.ID)+ ", Name = " + ToStr(Entry.Name)+ ", Notes = " + ToStr(Entry.Notes)+ ", PrimaryModelID = " + ToStr(Entry.PrimaryModelID)+ ", PrimaryPopulationSetID = " + ToStr(Entry.PrimaryPopulationSetID)+ ", NumberOfSimulationSteps = " + ToStr(Entry.NumberOfSimulationSteps)+ ", NumberOfRepetitions = " + ToStr(Entry.NumberOfRepetitions)+ ", SimulationRules = SimRuleList, DerivedFrom = " + ToStr(Entry.DerivedFrom)+ "), ProjectBypassID = 0)\nexcept: AnalyzeVersionConversionError()\n"
            if ConvertResults:
                KeysToProcess = sorted(globals()['TempSimulationResults'].keys())
                while KeysToProcess != []:
                    ID = KeysToProcess.pop(0)
                    if 'Load' in DebugPrints:
                        MessageToUser ('Processing SimulationResults ID' + str(ID)+ '')
                    Entry = globals()['TempSimulationResults'][ID]
                    DependantNotYetRegistered = False
                    if DependantNotYetRegistered:
                        KeysToProcess.append(ID)
                        if 'Load' in DebugPrints:
                            MessageToUser ('***************ID ' + str(ID)+ ' passed***************')
                    else:
                        # Note that a Population Set will be automatically recreated 
                        # rather than copied from a previously created result set
                        Out = Out + "try: DB.SimulationResults.AddNew( DB.SimulationResult( ProjectID = " + ToStr(Entry.ProjectID) + " , PreparedPopulationSet = None , ID = " + ToStr(Entry.ID) + ", Data = " + ToStr(Entry.Data) + "), ProjectBypassID = 0)\nexcept: AnalyzeVersionConversionError()\n"

            # The assumption is that no results were generated and therefore there 
            # is no transfer of such data.
            if RegenerationScriptName == None:
                # Execute the script without saving it. Note that the script will
                # be executed in the current name space and therefore the database
                # may change therefore in case of an error the system will load
                # an empty dictionary.
                try:
                    exec Out in globals(), locals()
                except:
                    (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                    # If unable to load the file for any reason, reload blank to 
                    # delete unwanted data that may have already been loaded
                    CreateBlankDataDefinitions()
                    # Then re-raise the error 
                    raise ExceptType, ExceptValue
                # If got here, DidLoad is True
                DidLoad = True
            else:
                # Save all the data to file, file name output is similar to the
                # program name, with the suffix _out.zip instead of .py
                # Note that this line is added to the script file only when saved.
                (ScriptPathOnly , ScriptFileNameOnly, ScriptFileNameFullPath) = DetermineFileNameAndPath(RegenerationScriptName)
                if OutputModelFileName != None:
                    (OutputModelFileNamePathOnly , OutputModelFileNameOnly, OutputModelFileNameFullPath) = DetermineFileNameAndPath(OutputModelFileName)
                else:
                    OutputModelFileNameFullPath = ScriptFileNameFullPath[:-3] + '_out.zip'
                Out = Out + "DB.SaveAllData(" + ToStr(OutputModelFileNameFullPath) + ", Overwrite = True, CreateBackupBeforeSave = True )\n"
                # Determine path and filename properly
                ScriptFile = open(ScriptFileNameFullPath,'w')
                ScriptFile.write (Out)
                ScriptFile.close()
    except:
        # In case an error was raised during this function make sure that
        # temp data was erased.
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        # Delete the temp objects created during load to save space
        DeleteTempLoadedObjects()
        # Then re-raise the error
        if CatchError:
            MessageToUser(str(ExceptValue))
        else:
            raise ExceptType, ExceptValue                
    else:
        # in any case, delete the temporary objects
        DeleteTempLoadedObjects()
    return (FileVersion, IsCompatible, IsUpgradable, DidLoad, HasResults)


def BackupFile(FileName, BackupFileName = None):
    """ Backup the previous file - typically before saving """
    if BackupFileName == None:
        (FileNameNoExtention, Extension) = os.path.splitext(FileName)
        CurrentTime = datetime.datetime.now().isoformat()
        TimeStamp = CurrentTime.replace(':', '').replace('.', '').replace('T', '').replace('-','')
        BackupFileName = FileNameNoExtention + '_' + TimeStamp + Extension
    try:
        shutil.copyfile(FileName, BackupFileName)
        CreatedBackupFileName = BackupFileName
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Save Backup File Error: Could not backup the file: ' + str(FileName) + ' to ' + str(BackupFileName) + ' . Here are details about the error: ' + str(ExceptValue)
    return CreatedBackupFileName


# Define functions to save and load the entire database
def SaveAllData(FileName, Overwrite = False, CompressFile = True, CreateBackupBeforeSave = False):
    """ Writes all the data into a single file that can later be loaded """
    # The function returns the Full path of the filename and the Backup filename
    try:
        AbsoluteFileName = os.path.abspath(FileName)
        # First try to backup the current file if it exists
        TheFileNameExists = os.path.isfile(AbsoluteFileName)
        CreatedBackupFileName = None
        if CreateBackupBeforeSave and TheFileNameExists:
            try:
                CreatedBackupFileName = BackupFile(AbsoluteFileName)
            except:
                # ignore the error, just print it out to the user
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                MessageToUser(str(ExceptValue)) 
        if TheFileNameExists and ((not Overwrite) or (Overwrite and CreateBackupBeforeSave and CreatedBackupFileName == None)):
            # If overwrite is not allowed, then check for existence of file name
            # Also check if overwrite was allowed and a backup was requested and
            # was not created, this means that overwrite is allowed only if
            # the backup was successful if requested. 
            raise ValueError, 'Save Error: A file with the name ' + FileName + ' already exists and a backup was not created. Please choose a new file or make sure a backup can be created.'
        # First, pickle the objects into strings
        StringsToSave={}
        for VariableName in GlobalsInDB:
            try:
                StringsToSave[VariableName] = pickle.dumps(globals()[VariableName])
            except:
                MessageToUser("Save All Warning: A problem was encountered while saving - trying an alternate save method")
                try:
                    # if memory does not allow this, try using a file
                    (TempFileDescriptor, TempFileName) = tempfile.mkstemp ( TempSuffix, DefaultTemporaryFileNamePrefix , SessionTempDirecory , True)
                    # Now actually create the file
                    TempFile = os.fdopen(TempFileDescriptor,'w')
                    pickle.dump(globals()[VariableName],TempFile)
                    TempFile.close()
                    # now reopen the file and read it into the string
                    TempFile = open(TempFileName,'r')
                    StringsToSave[VariableName] = TempFile.read()
                    TempFile.close()
                except:
                    (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                    raise ValueError, 'Save All Error: Could not prepare the file. Here are additional details on the error: ' +  str(ExceptValue)
                else:
                    MessageToUser("Save All Info: Alternate save method successful")
        # Open the archive file
        TheOutputFile = zipfile.ZipFile(AbsoluteFileName,'w',Iif(CompressFile,zipfile.ZIP_DEFLATED,zipfile.ZIP_STORED))
        # Now use the strings to populate the file
        for VariableName in GlobalsInDB:
             TheOutputFile.writestr(VariableName + AppFileNameExtension , StringsToSave[VariableName])
        TheOutputFile.close()
        # Mark the data not dirty as it was just saved
        AccessDirtyStatus(False)
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        raise ValueError, 'Save All Error: Could not properly save to file. Here are additional details on the error: ' +  str(ExceptValue)
    return (AbsoluteFileName, CreatedBackupFileName)


def LoadAllData(FileName, TempPrefix = None):
    """ Loads all the data from single file, overriding current data"""
    # If LoadToTemp is set then all variables are loaded to temporary variables
    # with the prefix defined in Temp, e.g. if TempPrefix ="Temp" then States
    # will be loaded to TempStates. This allows keeping two versions of files
    # for conversion.
    if TempPrefix == None:
        TempPrefix = ''
    try:
        # Check for existence of file name
        if not os.path.isfile(FileName):
            raise ValueError, 'Load Error: A file with the name "'+ FileName + '" does not exist. Please choose an existing file to load data from'
        # Open the archive file
        TheInputFile = zipfile.ZipFile(FileName,'r')
        # Read the strings
        for VariableName in GlobalsInDB:
            try:
                StringToUnpickle = TheInputFile.read( VariableName + AppFileNameExtension )
                VarData = pickle.loads(StringToUnpickle)
            except:
                # If an error was encountetred for any parameter other than 
                # 'version' raise an error. In case of 'version' allow this since
                # older files may not have this parameter.
                (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
                Msg = 'Error Encountered During Load: The Variable ' + VariableName + ' could not be loaded. Here are additional details: ' + str(ExceptValue)
                if VariableName == 'Version':
                    MessageToUser (Msg)
                    VarData = None
                else:
                    raise ValueError, Msg
            globals()[TempPrefix + VariableName] = VarData
        TheInputFile.close()
        # Mark the data not dirty as it was just loaded
        if TempPrefix != '':
            AccessDirtyStatus(False)
    except:
        (ExceptType, ExceptValue, ExceptTraceback) = sys.exc_info()
        # If unable to load the file for any reason, reload blank to delete
        # unwanted data that may have already been loaded
        CreateBlankDataDefinitions()
        # Then re-raise the error 
        raise ExceptType, ExceptValue
    return

def CreateBlankDataDefinitions():
    """ Create a blank database """
    global Params
    global States
    global StudyModels
    global Transitions
    global PopulationSets
    global Projects
    global SimulationResults
    # Define the global tables from the classes
    Params = ParamsClass()
    States = StatesClass()
    StudyModels = StudyModelsClass()
    Transitions = TransitionsClass()
    PopulationSets = PopulationSetsClass()
    Projects = ProjectsClass()
    SimulationResults = SimulationResultsClass()
    # Add system reserved parameters
    # Define system variables
    for ParamName in SystemReservedParametersToBeCreated:
        Params.AddNew(Param(Name = ParamName, Formula = ParamName , ParameterType = 'System Reserved' , ValidationRuleParams = '', Notes = 'Place holder to represent the ' + ParamName + ' system reserved variable'), ProjectBypassID = 0)
    # Define System reserved functions
    # Define the functions supported in expressions as reserved words
    for FuncName in ExpressionSupportedFunctionsNames:
        Params.AddNew(Param(Name = FuncName, Formula = FuncName , ParameterType = 'System Reserved' , ValidationRuleParams = '', Notes = 'Place holder to represent the ' + FuncName + ' function'), ProjectBypassID = 0)
    # Define the functions supported in expressions as reserved words,
    # and make their runtime replacement a banned parameter
    for (FuncName, RunTimeFuncName) in RuntimeFunctionNames:
        Params.AddNew(Param(Name = FuncName, Formula = FuncName , ParameterType = 'System Reserved' , ValidationRuleParams = '', Notes = 'Place holder to represent the ' + FuncName + ' function'), ProjectBypassID = 0)
        Params.AddNew(Param(Name = RunTimeFuncName, Formula = '' , ParameterType = 'System Reserved' , ValidationRuleParams = '', Notes = 'Parameter Banned for use since it is a command used in simulation runtime'), ProjectBypassID = 0)
    # Define the banned parameters to be used as this are python reserved words
    for Item in list(set(PythonReservedWords + ProgramReservedWords + BuiltinReservedWords + OtherReservedWords + sorted(Sympy2ExprFunctionMapping.keys()))):
        # a set is used since 'pow' is defined twice
        Params.AddNew(Param(Name = Item, Formula = '' , ParameterType = 'System Reserved' , ValidationRuleParams = '', Notes = 'Parameter Banned for use since it is a python reserved word, or a command used in simulation'), ProjectBypassID = 0)
    # Define default system options
    for (ParamName,ParamValue) in sorted(list(DefaultSystemOptions.iteritems())):
        Params.AddNew(Param(Name = ParamName, Formula = SmartStr(ParamValue) , ParameterType = 'System Option' , ValidationRuleParams = '', Notes = 'The default value for the ' + ParamName + ' system option'), ProjectBypassID = 0)
    # This initial DB is not dirty
    AccessDirtyStatus(False)

# Now create the blank DB
Params = None
States = None
StudyModels = None
Transitions = None
PopulationSets = None
Projects = None
SimulationResults = None

MessageToUser ('Loading Module DataDef.py, Version ' + str(Version))
CreateBlankDataDefinitions()
