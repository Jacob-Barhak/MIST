################################################################################
################################################################################
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
# Copyright (C) 2009-2011 The Regents of the University of Michigan
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
#                                                                              #
# This file contains the documentation interface.                              #
################################################################################

# usage example of public methods/members:
# >>> import doc
# >>> HelpClass = Documentation()
# >>> HelpClass.openDoc('modelexample.jpg')
# >>> HelpClass.openDoc(node = 'States')
# >>> if not HelpClass.error: print "It's working!"
# It's working!




import webbrowser, os

class Documentation:
    def __init__(this, docPath=None, docTop='index.html', split=True, useDict=True):
        # docPath: string, full directory path to documentation files
        # docTop: string, top HTML documentation file
        # split: Boolean, files are "split" if there is only one node per HTML file
        
        docPathDefault = os.path.join(os.getcwd(), 'Documentation')
        this.docPath = docPath or docPathDefault
        this.docTop = docTop
        this.error = None
        this.split = split
        this.useDict = useDict
        if this.useDict:
            this.initNodeDict()

        # this is mostly to check if the path is valid
        try:
            open(os.path.join(this.docPath, this.docTop), 'r').close()
        except IOError:
            try:
                open(os.path.join(docPathDefault, this.docTop), 'r').close()
                this.docPath = docPathDefault
            except:
                this.raiseError('Documentation Error: Documentation top file ' + this.docTop + ' cannot be located/opened.')
        except:
            this.raiseError('Documentation Error: Unexpected documentation error.')

    def openDoc(this, filename=None, node=None):
        """Launches the documentation in the default web browser.  Returns true if file can be opened, false otherwise."""
        # filename: string, file to be opened
        # node: string, similar to chapter name

        if this.split:
            # multiple HTML files
            if filename or node:
                # filename or node given
                openFile = filename or node + '.html'
                try:
                    open(os.path.join(this.docPath, openFile), 'r').close()
                    # all good
                except:
                    if this.useDict and node and node in this.nodeDict:
                        newNode = this.nodeDict[node]
                        # recursively call this function with the node name from the dictionary
                        return this.openDoc(node = newNode)
                    else:
                        this.raiseError('Documentation Error: Documentation file ' + openFile + ' cannot be located/opened.')
                        if openFile == this.docTop:
                            return False
                        else:
                            # try doc top file recursively
                            return this.openDoc(filename = this.docTop)
            else:
                # use doc top file
                return this.openDoc(filename = this.docTop)
        else:
            # single HTML file
            if filename:
                try:
                    open(os.path.join(this.docPath, filename), 'r').close()
                    # file opened successfully
                    openFile = filename
                except:
                    this.raiseError('Documentation Error: Documentation file ' + filename + ' cannot be located/opened; trying top file.')
                    try:
                        # try doc top file
                        open(os.path.join(this.docPath, this.docTop), 'r').close()
                        openFile = this.docTop
                    except:
                        this.raiseError('Documentation Error: Documentation file ' + this.docTop + ' cannot be located/opened.')
                        return False
            else:
                # no filename given; try doc top file
                try:
                    open(os.path.join(this.docPath, this.docTop), 'r').close()
                    openFile = this.docTop
                except:
                    this.raiseError('Documentation Error: Documentation file ' + this.docTop + ' cannot be located/opened.')
                    return False
            if node:
                # append node link
                if this.useDict and node in this.nodeDict:
                    openFile = openFile + '#' + this.nodeDict[node]
                else:
                    openFile = openFile + '#' + node
            openFile = openFile.replace('/','%2f') # encode page slashes, such as 'Study/Model'
            openFile = openFile.replace(' ', '%20') # encode spaces

        url = os.path.join(this.docPath, openFile)
        print 'Opening file: ' + url
        webbrowser.open_new(url)
        this.error = None
        return True

    def raiseError(this, message):
        """Used for non-fatal Documentation class errors.  Message is a string."""
        print message
        this.error = message

    def initNodeDict(this):
        """Initializes the dictionary that maps a node argument to the
        actual documentation node.  This essentially creates a back-end index."""
        # To add a new mapping:
        # Add another tuple to the dictionary below, using the request node
        # as the Key, and the HTML filename as the value.
        
        this.nodeDict = {'StudyModels' : 'Study_002fModel',
                         'Transitions' : 'Transitions',
                         'PopulationSets' : 'Populations',
                         'Params' : 'Parameters',
                         'SimulationResults' : 'Simulation',
                         'ReportViewer' : 'Reports',
                         'Wizard' : 'Simulation',
                         'PopulationData' : 'Populations',
                         'Main':'Getting-Started-with-IEST'}


if __name__ == "__main__":
    d = Documentation()
    print d.openDoc(node = 'States')
    print d.openDoc(node = 'Params')
    if d.error:
        print 'Oh dear...'
    else:
        print 'It seems to be working swimmingly.'
    