
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from deprecated import deprecated
from ogl.OglActor import OglActor
from ogl.OglClass import OglClass
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase
from ogl.sd.OglSDInstance import OglSDInstance

from wx import EVT_CLOSE
from wx import EVT_PAINT

from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import MouseEvent
from wx import Notebook

from ogl.OglInterface2 import OglInterface2
from ogl.OglObject import OglObject
from ogl.OglLink import OglLink

from ogl.sd.OglSDMessage import OglSDMessage

from miniogl.Constants import SKIP_EVENT
from miniogl.DiagramFrame import DiagramFrame
from miniogl.RectangleShape import RectangleShape

from pyut.ui.ActionHandler import ActionHandler
from pyut.ui.Actions import ACTION_ZOOM_IN

from pyut.PyutUtils import PyutUtils

from pyut.history.HistoryManager import HistoryManager

from pyut.experimental.GraphicalHandler import GraphicalHandler

# noinspection PyProtectedMember
from pyut.general.Globals import _

from org.pyut.ui.umlframes.UmlFrameShapeHandler import UmlFrameShapeHandler

from pyut.uiv2.eventengine.Events import AddOglDiagramEvent
from pyut.uiv2.eventengine.Events import AddPyutDiagramEvent
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

DEFAULT_WIDTH = 3000
A4_FACTOR:    float = 1.41

UmlObject  = Union[OglClass, OglLink, OglNote, OglText, OglSDMessage, OglSDInstance, OglActor, OglUseCase, OglInterface2]
UmlObjects = NewType('UmlObjects', List[UmlObject])


class UmlFrame(UmlFrameShapeHandler):
    """
    Represents a canvas for drawing diagrams.
    It provides all the methods to add new classes, notes, links...
    It also routes some click events to the mediator. See the `OnLeftDown`
    method.
    """
    PIXELS_PER_UNIT_X: int = 20
    PIXELS_PER_UNIT_Y: int = 20

    clsUmlFrameLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Notebook, eventEngine: IEventEngine):
        """

        Args:
            parent: The parent window
        """
        from org.pyut.ui.EditObjectHandler import EditObjectHandler

        super().__init__(parent)

        self.logger:       Logger       = UmlFrame.clsUmlFrameLogger
        self._eventEngine: IEventEngine = eventEngine

        self._actionHandler:      ActionHandler    = ActionHandler(eventEngine=eventEngine)
        self._editObjectHandler: EditObjectHandler = EditObjectHandler(eventEngine=eventEngine)

        self.maxWidth:  int  = DEFAULT_WIDTH
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        nbrUnitsX: int = int(self.maxWidth / UmlFrame.PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / UmlFrame.PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0
        self.SetScrollbars(UmlFrame.PIXELS_PER_UNIT_X, UmlFrame.PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)

        self._historyManager: HistoryManager = HistoryManager(self)

        # Close event
        self.Bind(EVT_CLOSE, self.evtClose)
        self.Bind(EVT_PAINT, self.OnPaint)

        self.SetInfinite(True)

        self._defaultCursor = self.GetCursor()

    @property
    def historyManager(self) -> HistoryManager:
        """
        Read-only as this is created on the frame initialization.

        Returns:  The frame's history manager.
        """
        return self._historyManager

    # noinspection PyUnusedLocal
    def setCodePath(self, path: str):
        """
        Set the code path

        Args:
            path:
        """
        assert False, 'This method is unsupported'
        # project = self._mediator.getFileHandling().getProjectFromFrame(self)
        # if project is not None:
        #     project.setCodePath(path)
        # else:
        #     self.logger.info("Passing setCodePath in UmlFrame-setCodePath")

    def displayDiagramProperties(self):
        """
        Display class diagram properties
        """
        PyutUtils.displayError(_("Not yet implemented !"))

    # noinspection PyUnusedLocal
    def evtClose(self, event):
        """
        Clean close, event handler on EVT_CLOSE

        Args:
            event:
        """
        self._historyManager.destroy()
        self.Destroy()

    def OnLeftDown(self, event: MouseEvent):
        """
        Manage a left down mouse event.
        If there's an action pending in the mediator, give it the event, else
        let it go to the next handler.
        """
        # self.logger.debug(f' leftDown - action waiting: {self._mediator.actionWaiting()}')
        # self.logger.debug(f' leftDown - action waiting: {self._actionHandler.actionWaiting}')
        # if self._mediator.actionWaiting():
        if self._actionHandler.actionWaiting:
            x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
            # skip = self._mediator.doAction(x, y)
            skip = self._actionHandler.doAction(self, x, y)

            # if self._mediator.getCurrentAction() == ACTION_ZOOM_IN:
            if self._actionHandler.currentAction == ACTION_ZOOM_IN:
                DiagramFrame._BeginSelect(self, event)

            if skip == SKIP_EVENT:
                DiagramFrame.OnLeftDown(self, event)

        else:
            # DiagramFrame.OnLeftDown(self, event)
            super().OnLeftDown(event)

    def OnLeftUp(self, event: MouseEvent):
        """
        To make the right action if it is a selection or a zoom.
        """
        # self.logger.debug(f' leftUp - current action: {self._mediator.getCurrentAction()}')
        # self.logger.debug(f' leftDown - action waiting: {self._actionHandler.actionWaiting}')
        # if self._mediator.getCurrentAction() == ACTION_ZOOM_IN:
        if self._actionHandler.currentAction == ACTION_ZOOM_IN:
            width, height = self._selector.GetSize()
            x, y = self._selector.GetPosition()
            self._selector.Detach()
            self._selector = cast(RectangleShape, None)
            self.DoZoomIn(x, y, width, height)
            self.Refresh()
            # self._mediator.updateTitle()
            self._actionHandler.updateTitle()
        else:
            # DiagramFrame.OnLeftUp(self, event)
            super().OnLeftUp(event)

    def OnLeftDClick(self, event: MouseEvent):
        """
        Manage a left double click mouse event.

        Args:
            event:
        """
        x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        self.logger.debug(f'leftDoubleClick - {x},{y}')
        # self._mediator.editObject(x, y)     # TODO send event to a dialog handler
        self._editObjectHandler.editObject(x, y)
        # DiagramFrame.OnLeftDClick(self, event)
        super().OnLeftDClick(event)

    def newDiagram(self):
        """
        Remove all shapes, get a brand new empty diagram.
        TODO:  rename to clearDiagram
        """
        self._diagram.DeleteAllShapes()
        self.Refresh()

    def getDiagram(self):
        """
        Returns this frame's diagram

        Returns:  wx.Diagram
        """
        return self._diagram

    def getUmlObjects(self) -> UmlObjects:
        """
        Retrieve UML objects from the UML Frame

        Returns:  The Uml objects on this diagram
        """
        umlObjects: UmlObjects = UmlObjects([])

        for s in self._diagram.GetShapes():
            # This is a duplicate of the UmlObject, since I cannot use NewType
            if isinstance(s, (OglClass, OglLink, OglNote, OglText, OglSDMessage, OglSDInstance, OglActor, OglUseCase, OglInterface2)):
                umlObjects.append(s)

        return umlObjects

    def getWidth(self):
        """

        Returns:  The frame width

        """
        return self.maxWidth

    def getHeight(self):
        """

        Returns: The frame height
        """
        return self.maxHeight

    # def getObjectsBoundaries(self):
    #     """
    #     TODO:  This appears to be an unused method
    #
    #     Return object boundaries (coordinates)
    #
    #     """
    #     infinite = 1e9
    #     minx     = infinite
    #     maxX     = -infinite
    #     miny     = infinite
    #     maxy     = -infinite
    #
    #     # Get boundaries
    #     for shapeObject in self._diagram.GetShapes():
    #         # Get object limits
    #         ox1, oy1 = shapeObject.GetPosition()
    #         ox2, oy2 = shapeObject.GetSize()
    #         ox2 += ox1
    #         oy2 += oy1
    #
    #         # Update min-max
    #         minx = min(minx, ox1)
    #         maxX = max(maxX, ox2)
    #         miny = min(miny, oy1)
    #         maxy = max(maxy, oy2)
    #
    #     # Return values
    #     return minx, miny, maxX, maxy

    def getUmlObjectById(self, objectId: int):
        """

        Args:
            objectId:  The id of the object we want

        Returns:  The uml object that has the specified id. If there is no
        matching object returns `None`
        """

        for shape in self.GetDiagram().GetShapes():
            if isinstance(shape, (OglObject, OglLink)):
                if shape.pyutObject.id == objectId:
                    return shape
        return None

    @deprecated('Use the historyManager property')
    def getHistory(self):
        """
        """
        return self._historyManager

    # noinspection PyUnusedLocal
    def _onAddPyutDiagram(self, event: AddPyutDiagramEvent):
        """
        Calls addHierarchy with the Pyut class list.
        """
        import pyut.experimental.PyutModelClasses as pdc

        BeginBusyCursor()

        gh: GraphicalHandler = GraphicalHandler(umlFrame=self, maxWidth=self.maxWidth, historyManager=self._historyManager)
        gh.addHierarchy(pdc.PyutClassNames)

        EndBusyCursor()

    # noinspection PyUnusedLocal
    def _onAddOglDiagram(self, event: AddOglDiagramEvent):
        """
        Calls addHierarchy with the Ogl class list.
        """
        import pyut.experimental.PyutModelClasses as pdc

        BeginBusyCursor()

        gh: GraphicalHandler = GraphicalHandler(umlFrame=self, maxWidth=self.maxWidth, historyManager=self._historyManager)
        gh.addHierarchy(pdc.OglClassNames)

        EndBusyCursor()
