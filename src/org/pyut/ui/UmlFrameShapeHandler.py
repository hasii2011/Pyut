
from typing import Union

from logging import Logger
from logging import getLogger

from wx import Brush
from wx import Pen
from wx import Window

from org.pyut.miniogl.DiagramFrame import DiagramFrame
from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.model.PyutActor import PyutActor
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutNote import PyutNote
from org.pyut.model.PyutText import PyutText
from org.pyut.model.PyutUseCase import PyutUseCase
from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglClass import OglClass

from org.pyut.ogl.OglInterface2 import OglInterface2
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglText import OglText
from org.pyut.ogl.OglUseCase import OglUseCase

from org.pyut.general.Globals import _


class UmlFrameShapeHandler(DiagramFrame):

    def __init__(self, parent: Window):

        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

    def createNewClass(self, x, y):
        """
        Add a new class at (x, y).

        @return PyutClass : the newly created PyutClass
        """
        pyutClass: PyutClass = PyutClass(_("NoName"))
        oglClass:  OglClass  = OglClass(pyutClass)

        self.addShape(oglClass, x, y)
        self.Refresh()
        return pyutClass

    def createNewNote(self, x: int, y: int):
        """
        Add a new note at (x, y).

        Args:
            x:
            y:

        Returns:    the newly created PyutNote
        """
        pyutNote: PyutNote = PyutNote()
        oglNote:  OglNote  = OglNote(pyutNote)

        self.addShape(oglNote, x, y)
        self.Refresh()
        return pyutNote

    def createNewText(self, x: int, y: int):
        """
        Add some new text at (x, y)
        Args:
            x:
            y:

        Returns:  The newly created PyutText
        """
        pyutText: PyutText = PyutText()
        oglText:  OglText  = OglText(pyutText)

        self.addShape(oglText, x, y)
        self.Refresh()

        return pyutText

    def createNewActor(self, x, y):
        """
        Add a new actor at (x, y).

        @return PyutActor : the newly created PyutActor
        """
        pyutActor: PyutActor = PyutActor()
        oglActor:  OglActor  = OglActor(pyutActor)

        self.addShape(oglActor, x, y)
        self.Refresh()
        return pyutActor

    def createNewUseCase(self, x, y):
        """
        Add a new use case at (x, y).

        @return PyutUseCase : the newly created PyutUseCase
        """
        pyutUseCase: PyutUseCase = PyutUseCase()
        oglUseCase:  OglUseCase  = OglUseCase(pyutUseCase)

        self.addShape(oglUseCase, x, y)
        self.Refresh()
        return pyutUseCase

    def addShape(self, shape: Union[OglObject, OglInterface2, SelectAnchorPoint],
                 x: int, y: int, pen: Pen = None, brush: Brush = None, withModelUpdate: bool = True):
        """
        Add a shape to the UmlFrame.

        Args:
            shape: the shape to add
            x: coord of the center of the shape
            y: coord of the center of the shape
            pen: pen to use
            brush:  brush to use
            withModelUpdate: if true the model of the shape will update from the shape (view) when added to the diagram.
        """
        shape.SetDraggable(True)
        shape.SetPosition(x, y)
        if pen is not None:
            shape.SetPen(pen)
        if brush is not None:
            shape.SetBrush(brush)
        self._diagram.AddShape(shape, withModelUpdate)
