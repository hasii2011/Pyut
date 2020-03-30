
from typing import List
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from time import time

from pygmlparser.Edge import Edge

from wx import CENTRE
from wx import ICON_ERROR
from wx import MessageDialog
from wx import OK
from wx import Yield as wxYield

from org.pyut.MiniOgl.AnchorPoint import AnchorPoint
from org.pyut.MiniOgl.ControlPoint import ControlPoint
from org.pyut.MiniOgl.Shape import Shape

from org.pyut.enums.PyutAttachmentPoint import PyutAttachmentPoint

from org.pyut.ui.UmlFrame import UmlFrame

from pygmlparser.Parser import Parser
from pygmlparser.Graph import Graph
from pygmlparser.Node import Node
from pygmlparser.graphics.Point import Point

from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.PyutToPlugin import PyutToPlugin

from org.pyut.plugins.orthogonal.TulipMaker import TulipMaker
from org.pyut.plugins.orthogonal.TulipMaker import OglToTulipMap
from org.pyut.plugins.orthogonal.CartesianConverter import CartesianConverter


class ToOrthogonalLayout(PyutToPlugin):
    """
    Layout the UML class diagram by changing the links to an orthogonal layout
    """
    def __init__(self, umlObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects:  list of ogl objects
            umlFrame:    A Pyut umlFrame
        """
        super().__init__(umlObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

    def getName(self):
        """
        Returns: the name of the plugin.
        """
        return "Orthogonal Layout"

    def getAuthor(self):
        """
        Returns:
            The author's name
        """
        return "Humberto A. Sanchez II"

    def getVersion(self):
        """
        Returns:
            The plugin version string
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Returns:
            The menu title for this plugin
        """
        return "Orthogonal Layout"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            If False, the import will be cancelled.
        """
        return True

    def doAction(self, umlObjects: List[OglClass], selectedObjects: List[OglClass], umlFrame: UmlFrame):
        """
        Do the tool's action

        Args:
            umlObjects:         list of the uml objects of the diagram
            selectedObjects:    list of the selected objects
            umlFrame:           The diagram frame
        """
        if umlFrame is None:
            self.displayNoUmlFrame()
            return
        if len(umlObjects) == 0:
            self.displayNoUmlObjects()
            return

        self.logger.info(f'Begin Orthogonal algorithm')

        tulipMaker: TulipMaker = TulipMaker()

        tulipMaker.translate(umlObjects)
        success: TulipMaker.LayoutStatus = tulipMaker.layout()
        if success[0] is False:
            dlg = MessageDialog(None, success[1],  'Layout Error', OK | ICON_ERROR | CENTRE)
            dlg.ShowModal()
            dlg.Destroy()

        pathToLayout: str = tulipMaker.pathToLayout

        parser: Parser = Parser()

        parser.loadGML(path=pathToLayout)
        parser.parse()

        gmlGraph: Graph = parser.graph
        gmlNodes: Graph.Nodes = gmlGraph.graphNodes
        gmlEdges: Graph.Edges = gmlGraph.graphEdges

        self.logger.info(f'Graph Node count: {len(gmlNodes)} Edge Count: {len(gmlEdges)}')

        nodeIdMap: OglToTulipMap = tulipMaker.nodeIdMap
        edgeIdMap: OglToTulipMap = tulipMaker.edgeIdMap

        self._reLayoutNodes(umlObjects, umlFrame, gmlNodes, nodeIdMap)

        self._reLayoutLinks(umlObjects, umlFrame, gmlEdges, edgeIdMap)

    def _reLayoutNodes(self, umlObjects: List[OglClass], umlFrame: UmlFrame, gmlNodes: Graph.Nodes, nodeIdMap: OglToTulipMap):
        """

        Args:
            umlObjects:
            umlFrame:
            gmlNodes:
            nodeIdMap:
        """

        for umlObj in umlObjects:
            if isinstance(umlObj, OglClass) or isinstance(umlObj, OglNote):
                gmlNodeId: int = nodeIdMap[umlObj.GetID()]
                gmlNode: Node = gmlNodes[gmlNodeId]
                self._stepNodes(umlObj, gmlNode)
            self._animate(umlFrame)

    def _reLayoutLinks(self, umlObjects, umlFrame: UmlFrame, gmlEdges, edgeIdMap):

        for umlLink in umlObjects:
            if isinstance(umlLink, OglLink):
                umlLink: OglLink = cast(OglLink, umlLink)
                gmlEdgeId: int = edgeIdMap[umlLink.GetID()]
                # gmlEdge:   Edge    = gmlEdges[gmlEdgeId]
                gmlEdge: Edge = [gEdge for gEdge in gmlEdges if gEdge.id == gmlEdgeId][0]  # TODO Modify the parser to store as a map
                self._stepEdges(umlLink=umlLink, gmlEdge=gmlEdge)
            self._animate(umlFrame)

    def _stepNodes(self, srcShape: Shape, gmlNode: Node):

        oldX, oldY = srcShape.GetPosition()
        cartesianX: int = gmlNode.graphics.x
        cartesianY: int = gmlNode.graphics.y

        newX, newY = CartesianConverter.cartesianToScreen(cartesianX, cartesianY)

        self.logger.info(f'{srcShape} - oldX,oldY = {oldX},{oldY} newX,newY = {newX},{newY}')

        srcShape.SetPosition(newX, newY)

    def _stepEdges(self, umlLink: OglLink, gmlEdge: Edge):

        line: Tuple[Point] = gmlEdge.graphics.line
        nPoints: int = len(line)
        self.logger.info(f'{umlLink} has points {nPoints}')
        #
        # Work around a bug for now
        #
        anchors = umlLink.getAnchors()
        srcAnchor: AnchorPoint = anchors[0]
        dstAnchor: AnchorPoint = anchors[1]

        relSrcX, relSrcY, relDstX, relDstY = self._getRelativeCoordinates(srcShape=umlLink.getSourceShape(), destShape=umlLink.getDestinationShape())
        self.logger.info(f' relSrc: ({relSrcX}, {relSrcY}) -  relDst: ({relDstX}, {relDstY})')

        srcAnchor.SetPosition(relSrcX, relSrcY)
        dstAnchor.SetPosition(relDstX, relDstY)
        if nPoints > 0:
            ptNumber: int = 0
            while ptNumber < nPoints:
                if 0 < ptNumber < (nPoints - 1):
                    self.logger.info(f'process point # {ptNumber}')
                    ptToAdd: Point = line[ptNumber]
                    cartesianX: int = ptToAdd.x
                    cartesianY: int = ptToAdd.y
                    newX, newY = CartesianConverter.cartesianToScreen(cartesianX, cartesianY)
                    controlPoint: ControlPoint = ControlPoint(newX, newY)
                    umlLink.AddControl(controlPoint)
                ptNumber += 1

    def _animate(self, umlFrame):
        """
        Does an animation simulation

        Args:
            umlFrame:
        """
        umlFrame.Refresh()
        self.logger.debug(f'Refreshing ...............')
        wxYield()
        t = time()
        while time() < t + 0.05:
            pass

    def _getRelativeCoordinates(self, srcShape, destShape):

        srcX, srcY = srcShape.GetPosition()
        dstX, dstY = destShape.GetPosition()

        orientation = self._getOrientation(srcX, srcY, dstX, dstY)
        self.logger.info(f'orientation: {orientation}')
        sw, sh = srcShape.GetSize()
        dw, dh = destShape.GetSize()
        if orientation == PyutAttachmentPoint.NORTH:
            srcX, srcY = sw / 2, 0
            dstX, dstY = dw / 2, dh
        elif orientation == PyutAttachmentPoint.SOUTH:
            srcX, srcY = sw / 2, sh
            dstX, dstY = dw / 2, 0
        elif orientation == PyutAttachmentPoint.EAST:
            srcX, srcY = sw, sh / 2
            dstX, dstY = 0, dh / 2
        elif orientation == PyutAttachmentPoint.WEST:
            srcX, srcY = 0, sh / 2
            dstX, dstY = dw, dh / 2

        return srcX, srcY, dstX, dstY

    def _getOrientation(self, srcX, srcY, destX, destY) -> PyutAttachmentPoint:
        """
        Given a source and destination, returns where the destination
        is located according to the source.

        Args:
            srcX:   X pos of src point
            srcY:   Y pos of src point
            destX:  X pos of dest point
            destY:  Y pos of dest point

        Returns:
            The attachment point on the destination
        """
        deltaX = srcX - destX
        deltaY = srcY - destY
        if deltaX > 0:  # dest is not east
            if deltaX > abs(deltaY):    # dest is west
                return PyutAttachmentPoint.WEST
            elif deltaY > 0:
                return PyutAttachmentPoint.NORTH
            else:
                return PyutAttachmentPoint.SOUTH
        else:   # dest is not west
            if -deltaX > abs(deltaY):   # dest is east
                return PyutAttachmentPoint.EAST
            elif deltaY > 0:
                return PyutAttachmentPoint.NORTH
            else:
                return PyutAttachmentPoint.SOUTH
