#!/usr/bin/env python

__version__ = "$Revision: 1.3 $"
__author__ = "EI6, eivd, Group Dutoit - Roux"
__date__ = "2002-05-22"

import sys
if ".." not in sys.path:
    sys.path.append("..") # access to the classes to test
import unittest

# Set lang function emulation
def _(x): return x
import __builtin__
__builtin__.__dict__['_'] = _

# Import pyut elements
import os
from wxPython.wx import *
from UmlFrame import UmlFrame
from ErrorManager import RAISE_ERROR_VIEW
from FileHandling import FileHandling
import mediator

##############################################################################
class App(wxApp):
    def OnInit(self):
        return true

class TestUmlFrame(unittest.TestCase):
    """
    This class do basic tests on UmlFrame :
    it creates classes, actors, notes, links, etc...
    @author C.Dutoit
    """

    #>------------------------------------------------------------------------

    def setUp(self):
        """
        Initialize.
        @author C.Dutoit
        """
        # Initialize mediator and error manager
        ctrl = mediator.getMediator()
        ctrl.setScriptMode()
        fileHandling = FileHandling(None, ctrl)
        ctrl.registerFileHandling(fileHandling)
        errorManager = ctrl.getErrorManager()
        errorManager.changeType(RAISE_ERROR_VIEW)

        # Create wx application
        app = App()


        # Create frame
        baseFrame = wxFrame(None, -1, "", size=(10, 10))
        umlFrame = UmlFrame(baseFrame, None)
        umlFrame.Show(true)
        self._umlFrame = umlFrame


    #>------------------------------------------------------------------------

    def testClassCreation(self):
        """
        Test Class Creation
        @author C.Dutoit
        """
        # Create a PyutClass
        try:
            pyutClass = self._umlFrame.createNewClass(10, 10)
        except:
            self.fail("Can't create a PyutClass")

        # Get the corresponding OglClass
        try:
            oglClass = [s for s in self._umlFrame.getDiagram().GetShapes()
                           if s.getPyutObject() is pyutClass][0]
        except:
            self.fail("Can't get OglClass")

        # Testing position
        try:
            x, y = oglClass.GetPosition()
        except:
            self.fail("Can't get OglClass position")
        self.failUnless(x==10 and y==10, "Wrong OglClass position !")


    #>------------------------------------------------------------------------

    def testNoteCreation(self):
        """
        Test Note Creation
        @author C.Dutoit
        """
        # PyutNote creation
        try:
            pyutNote = self._umlFrame.createNewNote(100, 10)
        except:
            self.fail("Can't create a PyutNote")

        # Get OglNote
        try:
            oglNote = [s for s in self._umlFrame.getDiagram().GetShapes()
                           if s.getPyutObject() is pyutNote][0]
        except:
            self.fail("Can't get OglNote")

        # Testing position
        try:
            x, y = oglNote.GetPosition()
        except:
            self.fail("Can't get OglNote position")
        self.failUnless(x==100 and y==10, "Wrong OglNote position !")

    #>------------------------------------------------------------------------

    def testActorCreation(self):
        """
        Test Actor Creation
        @author C.Dutoit
        """
        # Create a PyutActor
        try:
            pyutActor = self._umlFrame.createNewActor(100, 100)
        except:
            self.fail("Can't create a PyutActor")

        # Get the corresponding OglActor
        try:
            oglActor = [s for s in self._umlFrame.getDiagram().GetShapes()
                           if s.getPyutObject() is pyutActor][0]
        except:
            self.fail("Can't get OglActor")

        # Testing position
        try:
            x, y = oglActor.GetPosition()
        except:
            self.fail("Can't get OglActor position")
        self.failUnless(x==100 and y==100, "Wrong OglActor position !")



    #>------------------------------------------------------------------------

    def testUseCaseCreation(self):
        """
        Test UseCase Creation
        @author C.Dutoit
        """
        # Create a PyutUseCase
        try:
            pyutUseCase = self._umlFrame.createNewUseCase(10, 50)
        except:
            self.fail("Can't create a PyutUseCase")

        # Get the corresponding OglUseCase
        try:
            oglUseCase = [s for s in self._umlFrame.getDiagram().GetShapes()
                           if s.getPyutObject() is pyutUseCase][0]
        except:
            self.fail("Can't get OglUseCase")

        # Testing position
        try:
            x, y = oglUseCase.GetPosition()
        except:
            self.fail("Can't get OglUseCase position")
        self.failUnless(x==10 and y==50, "Wrong OglUseCase position !")




    #>------------------------------------------------------------------------

    def testInheritanceLinkCreation(self):
        """
        Test Inheritance link Creation
        @author C.Dutoit
        """
        # Create two PyutClass
        try:
            pyutClass1 = self._umlFrame.createNewClass(20, 10)
            pyutClass2 = self._umlFrame.createNewClass(30, 10)
        except:
            self.fail("Can't create two PyutClass")

        # Get OglObject
        try:
            oglClass1 = [s for s in self._umlFrame.getDiagram().GetShapes()
                           if s.getPyutObject() is pyutClass1][0]
            oglClass2 = [s for s in self._umlFrame.getDiagram().GetShapes()
                           if s.getPyutObject() is  pyutClass2][0]
        except:
            self.fail("Can't get the two OglClass")

        # Create the link
        try:
            self._umlFrame.createInheritanceLink(oglClass1, oglClass2)
        except:
            self.fail("Can't create a inheritance link")


    #>------------------------------------------------------------------------

    def testNewLinkCreation(self):
        """
        Test new link Creation
        @author C.Dutoit
        """
        # Create two PyutClass
        try:
            pyutClass1 = self._umlFrame.createNewClass(20, 20)
            pyutClass2 = self._umlFrame.createNewClass(30, 20)
        except:
            self.fail("Can't create two PyutClass")

        # Get OglObject
        try:
            oglClass1 = [s for s in self._umlFrame.getDiagram().GetShapes()
                           if s.getPyutObject() is pyutClass1][0]
            oglClass2 = [s for s in self._umlFrame.getDiagram().GetShapes()
                           if s.getPyutObject() is  pyutClass2][0]
        except:
            self.fail("Can't get the two OglClass")

        # Create the link
        try:
            self._umlFrame.createNewLink(oglClass1, oglClass2)
        except:
            self.fail("Can't create a new link")
#todo :createNEwLink(src, dst)

    #>------------------------------------------------------------------------

    def testClassCreation(self):
        """
        Test Class Creation
        @author C.Dutoit
        """
        pyutClass = self._umlFrame.createNewClass(10, 10)




def suite():
    """You need to change the name of the test class here also."""
    return unittest.makeSuite(TestUmlFrame)

def main():
    unittest.TextTestRunner().run(suite())

if __name__ == "__main__": main()
