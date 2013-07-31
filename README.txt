Copyright (C) 2013 Jacob Barhak
Copyright (C) 2009-2012 The Regents of the University of Michigan
License GPL 3 - See full details below

CONTENTS:
1. INTRODUCTION
2. INSTALLATION
3. HOW TO USE THE SOFTWARE
4. FILES
5. KNOWN BUGS AND FEATURES
6. VERSION HISTORY
7. CONTACT INFORMATION
8. ACKNOWLEDGEMENTS
9. LICENSE


1. INTRODUCTION:

This software supports modeling and Monte-Carlo micro-simulation of parallel state transition processes. It is initially intended to allow modeling of chronic diseases, yet the software is general and may accommodate other models.

The project web site is:
https://github.com/Jacob-Barhak/MIST

For a video introduction and additional information, please visit the following links:
http://www.youtube.com/watch?v=AD896WakR94
https://github.com/scipy/scipy2013_talks/tree/master/talks/jacob_barhak


2. INSTALLATION:

The system can be installed in several fashions in different platforms. There are even expert installations for High Performance Computing (HPC) that are for advanced and expert users. For novice users it is recommended that you use Quick Installation for Windows since it is the simplest and therefore described first.

Quick and Simple Installation for Windows Users:
1) Download and Install Python(x,y) version 2.7 or higher. Here is a direct link http://pythonxy.googlecode.com/files/Py(x,y)-2.7.3.1.exe . Other versions can be found at http://code.google.com/p/pythonxy/wiki/Downloads
2) Download the file MIST-master.zip from github by typing the following URL in a web browser: https://github.com/Jacob-Barhak/MIST/archive/master.zip
3) Unzip the file MIST-master.zip in a directory of your choice. This will be your working directory. You can do this on windows by right clicking the archive and choosing Extract All.

Expert Installation for Linux/OSX:
1) Download and Install Anaconda from https://store.continuum.io/
2) Install WxPython - this installation may require expert assistance and can be found at http://www.wxpython.org/download.php#stable 
3) Download the file MIST-master.zip from github by typing the following URL in a web browser: https://github.com/Jacob-Barhak/MIST/archive/master.zip
4) Unzip the file MIST-master.zip in a directory of your choice. This will be your working directory. 

Alternative Expert Installation Instructions:
1) Install a scientific Python distribution which supports Python 2.7 and includes numpy, matplotlib, and nose. You can choose from a list of those in http://python-for-researchers.readthedocs.org/en/latest/distros.html . You can also Install Python, numpy, matplotlib, and nose separately.
2) Install WxPython if you intend to use the Graphic User Interface and it was not installed by the scientific Python distribution. WxPython installation may require expert assistance and can be found at http://www.wxpython.org/download.php#stable
3) Download the file MIST-master.zip from github by typing the following URL in a web browser: https://github.com/Jacob-Barhak/MIST/archive/master.zip
4) Unzip the file MIST-master.zip in a directory of your choice. This will be your working directory. 

To Test the Above Installations:
1. From the command line run the file TestCode.py. It will test the data definitions and algorithms and should take a few minutes. If you got an all caps "OK" at the end, then you installed the python environment correctly.
2. Run Main.py to see the Graphic User Interface. If the main window shows up, then the WxPython part is installed correctly. You can try to file-load the file Testing.zip to see the examples.

If you are an expert you can install and setup MIST to work in High Performance Computing (HPC) environment. These expert installations may require professional support. Please feel free to use the contact information below for assistance.

To run MIST over the cloud a more complicated setup is needed:
1. Install starcluster http://star.mit.edu/cluster/docs/latest/installation.html
2. Follow the instructions on http://continuum.io/blog/starcluster-anaconda
3. If you have not done so already follow the Quick Installation for Linux/OSX from above on your machine
4. Use the starcluster put command to transfer MIST to the /home directory on the cluster

It is also possible to run MIST simulations in Multi-core environment using Sun Grid Engine. If you wish to install Sun-Grid-Engine on a single machine for testing purposes:
1. Follow the instructions on http://scidom.wordpress.com/2012/01/18/sge-on-single-pc/
2. Follow the Quick Installation for Linux/OSX from above



3. HOW TO USE THE SOFTWARE:

Open the chosen directory created during installation and double-click Main.py. The main form titled as 'MIcroSimulation Tool (MIST)' will open.

The system includes a help system and an example file to aid in learning how to use it. To get started, select help menu in the main form and then select the help sub-option. This will bring up the getting started help page.

You may wish to start learning the system by loading the example file Testing.zip from within the system and exploring it. The examples there are described in details in the file SimulationExamples.pdf




4. FILES:

The software contains the following files:

~~~~~~~~~~~~~~ Data Definitions ~~~~~~~~~~~~~~
The following files handle the data:
DataDef.py : Defines the data structures of the system.
TestCode.py : A test script that validates the simulation system integrity by running predetermined input examples.
ConvertDataToCode.py : A utility that converts zip file generated by the system to a python script. 
MultiRunCombinedReport.py : A utility that allows combining results from several runs of the same model and population set into a single report. The use of this utility allows running multiple simulations in parallel and combining their results. 
MultiRunSimulation.py : A utility that allows running the same simulation multiple times outside the GUI. Useful for parallel processing on multiple computers. It can be used well with MultiRunSimulationStatisticsAsCSV.py to generate a summary statistics for repetitions. 
MultiRunSimulationStatisticsAsCSV.py : A utility that generates CSV summary reports from several runs of the same project. Combines well with MultiRunSimulation.py that generates input files for this CSV report. The output consists of mean,STD,median,min,max of report columns with regard to different simulation results. 
MultiRunExportResultsAsCSV.py : A utility that generates a CSV file containing the data from a set of result files. 
AssembleReportCSV.py : A utility that assembles a CSV file from multiple CSV files generated by MultiRunExportResultsAsCSV.py 
CreatePlotsFromCSV.py : A utility that constructs plots in a PDF file. The plot data is collected from a CSV file assembled by AssembleReportCSV.py 

~~~~~~~~~~~~~~ Graphic User Interface ~~~~~~~~~~~~~~
CDMLib.py : The main library defining the system GUI
Main.py : The main file that starts the application GUI with the main form
Parameters.py : The parameters form in the GUI
PopulationSets.py : The population set form in the GUI
PopulationData.py : The population data form in the GUI used by population set
Project.py : The project form in the GUI
ReportViewer.py : The report viewer form in the GUI and called by many forms
ResultViewer.py : The result viewer form in the GUI used by the Project form
States.py : The states form in the GUI
StudyModels.py : The model form in the GUI
Transitions.py : The Transition form in the GUI used by the Study/Models form
Wizard.py : The Cost/QoL Wizard form in the GUI
HelpInterface.py : Defined the help interface between forms and html files in the documentation

~~~~~~~~~~~~~~ Supporting Files ~~~~~~~~~~~~~~
The following files and directories are provided:
README.txt : This file, that you are now reading
License.txt : The GPL license text
Documentation : A directory that holds all the html help files
DocSrc.texi : The Texinfo source file used to generate the html help files using the command makeinfo --html DocSrc.texi
ImagePreperation.odp : A presentation file that is used to generate images for the html help files using the save as jpg.
CopyImages.bat : a batch file to copy documentation images to their proper location to match the html files that form the help system
Temp : A directory containing temporary data generated while the system is running - the system recreates it if deleted.
Testing.zip : a data file generated by TestCode.py and contains simulation examples. The examples correspond to those described in SimulationExamples.pdf.
SimulationExamples.pdf : A document describing the examples in Testing.zip that are used to test the simulation system. It also contains calculations of the expected outcomes and provide a description of tests carried out in TestCode.py.
SimulationExamples.doc : The original word version from which SimulationExamples.pdf was created.
TestingResults.mdb : a Microsoft Access Database used to test the report mathematics performing the same calculations as the system and outputs files that can be loaded into TestCode.txt. The file contains visual basic code that generates csv files from InputExample.py results. These csv files can then be converted back to code that is merged into InputExample.py as testing code.
ClusterRun.py : A Python script for running multiple simulations with variation overrides on a cluster. Very similar to MultiRun.bash, with some enhancements such as creating plots. This file should be modified before use to fit the cluster it is running on - otherwise it will probably not work.
CodeFromDocAndSpreadsheet.py : A python script that converts rule text from a word document and CSV file from a spreadsheet with populations into code and a model file. This script was created to handle a specific format used with the Michigan model documentation. This file relies on a very specific format of documents and remains undocumented and should be treated as an example for programmers that want to extend the system. 



5. KNOWN BUGS AND FEATURES:

This version contains only Simulation capabilities. 

The examples provided with the system are used for testing the system. 

Running the TestCode.py script will test that the simulation system is working properly. Running this file will also create the file Testing.zip that is the data file the system can load and tests the simulation results. The file SimulationExamples.pdf analyses these examples and allows results comparison that is performed when TestCode.py is run. To run this in verbose mode from the command line, change the working directory to the installation directory and type nosetests -s 

In addition to the above test script, below is a list of known bugs and issues uncovered during testing that were not yet addressed at the time of this release:


Known Bugs

At the time of release, there were no known reproducible bugs.



Comments/Suggestions & Feature Requests:


R0021: LIST OF COEFFICIENTS FOR COST WIZARD
When using the Cost/QoL wizard, the drop down list for coefficients lists states that do not belong to the project. Selecting these states is allowed, but when you try to run the simulation, you get an error that the state could not be found. The error should come while using/closing the Cost Wizard, or the non-included states should not be listed at all. 
INSTRUCTIONS TO REPRODUCE 
1. Use Cost Wizard on a project such as example 1 
2. Add a state that isn't in the selected project, such as Angina for example 1 
3. Run Simulation



J0007: IMPROVE MESSAGES TO USER MECHANISM FOR SIMULATION LOG
Currently a simulation shows messages to the user in a command box behind the windows while preparing or running a simulation. In the future, it would be nice to have a window that holds a log for user messages, possibly with different colors for different levels of information that the user can conveniently browse and study.



J0011: USER CAN OVERRIDE POPULATION REPAIR AND ADVERSELY AFFECT SIMULATION 
The user can create a population with the main process not defined and a state in that sub-process set. If the system option RepairPopulation is set to False, the simulation will end after one time step since the main process will reset all states afterwards. This is unreasonable behavior that should be banned. 



J0016: CONSIDER ADDING STARTED AND EXITED STATE INDICATORS
Considered adding state indicators _Exited , _Started that will contain additional information regarding a state. This will allow assessing which transition was used and if an individual moved from a certain state. Also consider adding special state indicators such as _Duration to keep the time a user was in the state.


J0020: ALLOW BOTTOM UP CASCADING CHANGES THROUGH SPECIAL GUI 

Currently, if a parameter was user by any entity in the system, it cannot be changed. There are work-around solutions that allow creation of copies. However, if multiple entities are involved, many copies of many entities should be created. This increases the chance of human error and it is just cumbersome. Moreover, the problem is not only with parameters, is it with any entity that is used by another entity.
The locks are in place for a reason and the system provides a data to code tool that allows recreating a data base from scratch where this change is present. However, it is still not easy for a user who just wants to go back and make a simple change in a parameter value/formula or even just a note for a state.
Adding a special version of the GUI that will allow making this change through forms just for the purpose of reconstructing a database will be helpful. 



J0030: It is impossible to cancel simulation of population generation from GUI

While running the simulation from GUI in Windows, there is no cancel button that can be pressed to stop the simulation. In some cases, this is desirable and it would be a nice to have feature.

There is a cancel button in the Linux version since version 0.78.0.0.




6. VERSION HISTORY:

MIST Verion (0,88,0,0,'MIST') - 31-Jul-2013:
	- Redefinition of Table function to improve speed and remove previous issues
	- Documentation adjusted with additions to running MIST over the cloud
	- GUI Bug fix 

MIST Verion (0,87,0,0,'MIST') - 16-Jun-2013:
	- Split from IEST : Estimation removed, only Simulation remains
	- Simplification/improvement of Parameters / Models / Simulation Rules
	- MIST runs over the cloud and on sun Grid Engine clusters
	- Reproducibility and traceability were improved
	- Restructured test suite 
	- Documentation adjusted to the changes

	
MIST is a split from IEST. below are IEST versions:

IEST Version (0,85,0,0,'Base') - 27-Feb-2012:
    - Improvements to validity checks to prevent deadlocking the user due to cyclic references and machine precision issues.
    - Some internal changes to force deterministic calculation order on simulations.
    - Documentation and minor changes in command line utilities.


IEST Version (0,83,0,0,'Base') - 10-Feb-2012:
    - Minor improvements to validity checks and error messages to improve user experience
    - Minor GUI improvements
    - Minor improvements to cluster run, and other utilities and a new utility to support conversion from documentation


IEST Version (0,82,0,0,'Base') - 10-Jan-2012:
    - Minor GUI fixes to display well on multiple resolutions
    - Minor improvement in DB test script


IEST Version (0,81,0,0,'Base') - 21-Dec-2011:
    - Proper NaN initialization in reports allows better tracking of missing values
    - Some minor GUI improvements allow easier viewing or long project rule functions
    - Creating csv report is much faster for many repetitions
    - The system now support generating plots of simulation results as pdf files using matplotlib


IEST Version (0,80,0,0,'Base') - 16-May-2011:
    - The system requires Python 2.7. Previous python versions are no longer supported.
    - The system can run simulations in parallel on a cluster using slurm
    - The report system includes new calculations, stratification, and NaN represents missing values
    - The system supports loading and saving report options
    - The system supports simulation with population sets defined by distribution 
    - Inf or inf and NaN or nan can be used in user expressions
 

IEST Version (0,78,0,0,'Base') - 2-Sep-2010:
    - The system was tested with Python 2.6
    - Simulation, population, and report generation through the GUI can be canceled if using python 2.6 on Linux
    - Special characters will now display with escape codes in systems that do not support them
    - It is not possible to delete a parameter in a child form of a project form
    - The Population data form can handle long expression
    - CSV report is now constructed transposed to make it easier to read
    - CSV report assembly added
    - Instructional videos were added to the documentation


IEST Version (0,75,0,0,'Base') - 05-May-2010:
    - Simulation and generation code was modified to:
        * expand expressions and allow proper intermediate validation of user defined functions.
    - GUI was fixed to:
        * avoid listbox text length limitation on Windows to affect rule data entry
        * bring proper help page in simulation
        * support top down functionality
        * properly handle the case where the user declines loading results from a previous version
    - Documentation was updated to:
        * show the difference between user defined parameter functions and assignments to parameters


IEST Version (0,70,0,0,'Base') - 11-Dec-2009:
    - Estimation Engine implemented in Python
    - Code tested on Linux (Debian with appropriate libraries installed)
    - Some minor fixes in the GUI
    - Some modifications to make initial population generation less strict: 1) allowing to use the IndividualID parameter as a counter during population generation from distributions. 2) Ignoring inconsistencies between states and sub-processes in the Entered and User manipulated state indicators.
    - File Version control added
    - Documentation updated


IEST Version 0.60 - 15-Feb-2009:
    - First release


	

7. CONTACT INFORMATION:


Jacob Barhak Ph.D.
email: jacob.barhak@gmail.com
http://sites.google.com/site/jacobbarhak/




8. ACKNOWLEDGEMENTS:

Special thanks to the pioneers who started this project and dreamed of a modeling framework before I joined the effort:
Deanna Isaman - Who was the spirit behind the great ideas I am pursuing and who taught me my first steps in disease modeling
Morton Brown - Who provided guidance and challenged the system to improve and by this shaped important concepts in the system
William H. Herman - Who provided expert advice regarding disease modeling and opened opportunities in the disease modeling world

Many thanks to the creators of Python, WxPython, NumPy, and SciPy that publicly released their work. Specifically, the code uses examples released by WxPython documentation and demo. These examples were extremely helpful in speeding up the development.

Special thanks to the following (in no particular order) for their help in various stages of this work:
Honghong Zhou
Fredric Isaman
Shari Messinger Cayetano
Michael Brandle
The Michigan Python Users Group
The Center for Advanced Computing at the University of Michigan
Chris Scheller
Wen Ye
Donghee Lee
Ray Lillywhite
Aidan Feldman
Michael Kylman 
Continuum Analytics
Star Cluster at MIT
Sun Grid Engine
Robin Dunn
Rayson Ho
Bruce Fields

MIST was developed independently without financial support.

Previous Sponsors of IEST:
This work was supported by the National Institutes of Health through the Biostatistics Core of the Michigan Diabetes Research and Training Center under Grant P60-DK-20572, and through grant R21-DK075077 "Chronic Disease Modeling for Clinical Research Innovations" by the National Institutes of Health.


9. LICENSE:

Copyright (C) 2013 Jacob Barhak
Copyright (C) 2009-2012 The Regents of the University of Michigan

This file is part of the MIcroSimulation Tool (MIST).
The MIcroSimulation Tool (MIST) is free software: you
can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

The MIcroSimulation Tool (MIST) is distributed in the
hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ADDITIONAL CLARIFICATION

The MIcroSimulation Tool (MIST) is distributed in the 
hope that it will be useful, but "as is" and WITHOUT ANY WARRANTY of any 
kind, including any warranty that it will not infringe on any property 
rights of another party or the IMPLIED WARRANTIES OF MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE. THE AUTHORS assume no responsibilities 
with respect to the use of the MIcroSimulation Tool (MIST).  

The MIcroSimulation Tool (MIST) was derived from the Indirect Estimation  
and Simulation Tool (IEST) and uses code distributed under the IEST name.
The change of the name signifies a split from the original design that 
focuses on microsimulation. For the sake of completeness, the copyright 
statement from the original tool developed by the University of Michigan
is provided below and is also mentioned above.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%% Original Copyright %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


Copyright (C) 2009-2012 The Regents of the University of Michigan
Initially developed by Deanna Isaman, Jacob Barhak, Morton Brown, Wen Ye
Additional coding by Donghee Lee, Ray Lillywhite, Aidan Feldman
Videos by Michael Kylman 

This file is part of the Indirect Estimation and Simulation Tool (IEST).
The Indirect Estimation and Simulation Tool (IEST) is free software: you
can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

The Indirect Estimation and Simulation Tool (IEST) is distributed in the
hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ADDITIONAL CLARIFICATION

The Indirect Estimation and Simulation Tool (IEST) is distributed in the 
hope that it will be useful, but "as is" and WITHOUT ANY WARRANTY of any 
kind, including any warranty that it will not infringe on any property 
rights of another party or the IMPLIED WARRANTIES OF MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE. THE UNIVERSITY OF MICHIGAN assumes no 
responsibilities with respect to the use of the Indirect Estimation and 
Simulation Tool (IEST).  

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%% End Of Original Copyright %%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
