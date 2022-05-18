# type: ignore
from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from wx import Dialog
from wx import Gauge
from wx import ICON_INFORMATION
from wx import Point
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP
from wx import Size

from org.pyut.miniogl.ControlPoint import ControlPoint
from pyutmodel.PyutLinkType import PyutLinkType
from org.pyut.ogl.OglAssociationLabel import OglAssociationLabel

from org.pyut.ogl.OglLinkFactory import getOglLinkFactory
from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglAssociation import OglAssociation
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglUseCase import OglUseCase

from org.pyut.ogl.sd.OglSDInstance import OglSDInstance
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage

from pyutmodel.PyutStereotype import PyutStereotype
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutSDInstance import PyutSDInstance
from pyutmodel.PyutSDMessage import PyutSDMessage
from pyutmodel.PyutUseCase import PyutUseCase
from pyutmodel.PyutActor import PyutActor
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutLink import PyutLink

from org.pyut.PyutUtils import PyutUtils

from org.pyut.PyutConstants import PyutConstants

from org.pyut.ui.Mediator import Mediator
from org.pyut.general.Globals import _


def secure_int(x):
    try:
        if x is not None:
            return int(x)
        else:
            return 0
    finally:
        return 0


def secure_bool(x):
    try:
        if x is not None:
            if x in [True, "True", "true", 1, "1"]:
                return True
    except (ValueError, Exception) as e:
        print(f'secure_bool error: {e}')
    return False


class IDFactory:
    nextID = 1

    def __init__(self):
        self._dicID = {}

    def getID(self, theClass):
        if theClass in self._dicID:
            return self._dicID[theClass]
        else:
            clsId = IDFactory.nextID
            self._dicID[theClass] = clsId
            IDFactory.nextID += 1
            return clsId


class PyutXml:
    """
    Class for saving and loading a PyUT UML diagram in XML.
    This class offers two main methods that are save() and load().
    Using the dom XML model, you can, with the saving method, get the
    diagram corresponding XML view. For loading, you have to parse
    the file and indicate the UML frame on which you want to draw
    (See `UmlFrame`).

    Sample use::

        # Write
        pyutXml = PyutXml()
        text = pyutXml.save(oglObjects)
        file.write(text)

        # Read
        dom = parse(StringIO(file.read()))
        pyutXml = PyutXml()
        myXml.open(dom, umlFrame)

    Changelog in PyutXmlV8 :
    - Merged PyutXmlV 7, 6, 5, 4, 3 in PyutXml
    - Set classes ID at save-time and load-time

    :version: $Revision: 1.11 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """
    def __init__(self):
        """
        Constructor
        """
        self.logger: Logger = getLogger(__name__)

        self._this_version = 8
        self._idFactory = IDFactory()

    def save(self, project):
        """
        Aave diagram in XML file.

        @param project

        @author Deve Roux
        @modified Laurent Burgbacher <lb@alawa.ch> : add version support
        @modified C.Dutoit 20021122 : added document container tag
        """
        dlg:    Dialog   = Dialog(None, -1, "Saving...", style=STAY_ON_TOP | ICON_INFORMATION | RESIZE_BORDER, size=Size(207, 70))
        xmlDoc: Document = Document()
        try:
            # xmlDoc: Document  = Document()
            top     = xmlDoc.createElement("PyutProject")
            top.setAttribute('version', str(self._this_version))
            top.setAttribute('CodePath', project.getCodePath())

            xmlDoc.appendChild(top)

            # dlg   = Dialog(None, -1, "Saving...", style=STAY_ON_TOP | ICON_INFORMATION | RESIZE_BORDER, size=Size(207, 70))
            gauge = Gauge(dlg, -1, 100, pos=Point(2, 5), size=Size(200, 30))
            dlg.Show(True)

            # Save all documents in the project
            for document in project.getDocuments():
                documentNode = xmlDoc.createElement("PyutDocument")
                documentNode.setAttribute('type', PyutConstants.diagramTypeAsString(document.getType()))
                top.appendChild(documentNode)

                oglObjects = document.getFrame().getUmlObjects()
                for i in range(len(oglObjects)):
                    gauge.SetValue(i * 100 / len(oglObjects))
                    oglObject = oglObjects[i]
                    if isinstance(oglObject, OglClass):
                        documentNode.appendChild(self._OglClass2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglNote):
                        documentNode.appendChild(self._OglNote2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglActor):
                        documentNode.appendChild(self._OglActor2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglUseCase):
                        documentNode.appendChild(self._OglUseCase2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglLink):
                        documentNode.appendChild(self._OglLink2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglSDInstance):
                        documentNode.appendChild(self._OglSDInstance2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglSDMessage):
                        documentNode.appendChild(self._OglSDMessage2xml(oglObject, xmlDoc))
        except (ValueError, Exception) as e:
            try:
                dlg.Destroy()
                self.logger.error(f'{e}')
            except (ValueError, Exception) as e:
                self.logger.error(f'{e}')
            PyutUtils.displayError(_("Can't save file"))
            return xmlDoc

        dlg.Destroy()

        return xmlDoc

    def open(self, dom, project):
        """
        Open a file and create a diagram.
        """
        dlgGauge = None
        umlFrame = None  # avoid Pycharm warning
        try:
            root = dom.getElementsByTagName("PyutProject")[0]
            if root.hasAttribute('version'):
                version = int(root.getAttribute("version"))
            else:
                version = 1
            if version != self._this_version:
                self.logger.error("Wrong version of the file loader")
                eMsg: str = f'This is version {self._this_version} and the file version is {version}'
                self.logger.error(eMsg)
                raise Exception(f'VERSION_ERROR:  {eMsg}')
            project.setCodePath(root.getAttribute("CodePath"))

            # Create and init gauge
            dlgGauge = Dialog(None, -1, "Loading...", style=STAY_ON_TOP | ICON_INFORMATION | RESIZE_BORDER, size=Size(207, 70))
            gauge    = Gauge(dlgGauge, -1, 5, pos=Point(2, 5), size=Size(200, 30))
            dlgGauge.Show(True)

            # for all elements il xml file
            dlgGauge.SetTitle("Reading file...")
            gauge.SetValue(1)

            for documentNode in dom.getElementsByTagName("PyutDocument"):

                dicoOglObjects = {}     # format {id/name : oglClass}
                dicoLink       = {}     # format [id/name : PyutLink}
                dicoFather     = {}     # format {id child oglClass : [id fathers]}

                docType = documentNode.getAttribute("type")     # Python 3 update

                document = project.newDocument(PyutConstants.diagramTypeFromString(docType))
                umlFrame = document.getFrame()

                mediator: Mediator = Mediator()
                mediator.getFileHandling().showFrame(umlFrame)

                self._getOglClasses(documentNode.getElementsByTagName('GraphicClass'),    dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglNotes(documentNode.getElementsByTagName('GraphicNote'),       dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglActors(documentNode.getElementsByTagName('GraphicActor'),     dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglUseCases(documentNode.getElementsByTagName('GraphicUseCase'), dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglLinks(documentNode.getElementsByTagName("GraphicLink"),       dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglSDInstances(documentNode.getElementsByTagName("GraphicSDInstance"), dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglSDMessages(documentNode.getElementsByTagName("GraphicSDMessage"),   dicoOglObjects, dicoLink, dicoFather, umlFrame)

                # fix the link's destination field
                gauge.SetValue(2)
                dlgGauge.SetTitle("Fixing link's destination...")
                for links in list(dicoLink.values()):
                    for link in links:
                        link[1].setDestination(dicoOglObjects[link[0]].getPyutObject())
                # adding fathers
                dlgGauge.SetTitle("Adding fathers...")
                gauge.SetValue(3)
                for child, fathers in list(dicoFather.items()):
                    for father in fathers:
                        umlFrame.createInheritanceLink(dicoOglObjects[child], dicoOglObjects[father])

                # adding links to this OGL object
                dlgGauge.SetTitle("Adding Links...")
                gauge.SetValue(4)
                for src, links in list(dicoLink.items()):
                    for link in links:
                        createdLink = umlFrame.createNewLink(dicoOglObjects[src], dicoOglObjects[link[1].getDestination().getId()])

                        # fix link with the loaded information
                        pyutLink = createdLink.getPyutObject()
                        traversalLink: PyutLink = link[1]
                        pyutLink.setBidir(traversalLink.getBidir())

                        # pyutLink.setDestinationCardinality(link[1].getDestinationCardinality())
                        # pyutLink.setSourceCardinality(link[1].getSrcCard())
                        pyutLink.destinationCardinality = traversalLink.destinationCardinality
                        pyutLink.sourceCardinality      = traversalLink.sourceCardinality

                        pyutLink.setName(link[1].getName())
        except (ValueError, Exception) as e:
            if dlgGauge is not None:
                dlgGauge.Destroy()
            PyutUtils.displayError(_(f"Can't load file {e}"))
            umlFrame.Refresh()
            return

        # to draw diagram
        umlFrame.Refresh()
        gauge.SetValue(5)

        if dlgGauge is not None:
            dlgGauge.Destroy()

    def _PyutSDInstance2xml(self, pyutSDInstance: PyutSDInstance, xmlDoc: Document):
        """
        Exporting an PyutSDInstance to an miniDom Element.

        @param  pyutSDInstance : Class to save
        @param xmlDoc : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('SDInstance')
        eltId = self._idFactory.getID(pyutSDInstance)

        root.setAttribute('id',           str(eltId))
        root.setAttribute('instanceName', pyutSDInstance.getInstanceName())
        root.setAttribute('lifeLineLength', str(pyutSDInstance.getInstanceLifeLineLength()))
        return root

    def _OglSDInstance2xml(self, oglSDInstance, xmlDoc):
        """
        Exporting an OglSDInstance to a miniDom Element.

        @param OglSDInstance oglSDInstance : Instance to save
        @param xmlDoc : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('GraphicSDInstance')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglSDInstance, root)

        # adding the data layer object
        root.appendChild(self._PyutSDInstance2xml(oglSDInstance.getPyutObject(), xmlDoc))

        return root

    def _PyutSDMessage2xml(self, pyutSDMessage: PyutSDMessage, xmlDoc: Document):
        """
        Exporting an PyutSDMessage to an miniDom Element.

        @param pyutSDMessage : SDMessage to save
        @param xmlDoc : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('SDMessage')

        # ID
        eltId = self._idFactory.getID(pyutSDMessage)
        root.setAttribute('id', str(eltId))

        # message
        root.setAttribute('message', pyutSDMessage.getMessage())

        # time
        idSrc = self._idFactory.getID(pyutSDMessage.getSource())
        idDst = self._idFactory.getID(pyutSDMessage.getDest())
        root.setAttribute('srcTime', str(pyutSDMessage.getSrcTime()))
        root.setAttribute('dstTime', str(pyutSDMessage.getDstTime()))
        root.setAttribute('srcID', str(idSrc))
        root.setAttribute('dstID', str(idDst))

        return root

    def _OglSDMessage2xml(self, oglSDMessage, xmlDoc):
        """
        Exporting an OglSDMessage to an miniDom Element.

        @param oglSDMessage : Message to save
        @param xmlDoc
        @return Element : XML Node
        """
        root = xmlDoc.createElement('GraphicSDMessage')

        # adding the data layer object
        root.appendChild(self._PyutSDMessage2xml(oglSDMessage.getPyutObject(), xmlDoc))

        return root

    def _PyutField2xml(self, pyutField, xmlDoc):
        """
        Exporting a PyutField to an miniDom Element

        @param PyutField pyutField : Field to save
        @param xmlDoc xmlDoc : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('Field')

        # adding the parent XML
        # pyutField is a param
        root.appendChild(self._PyutParam2xml(pyutField, xmlDoc))

        # field visibility
        root.setAttribute('visibility', str(pyutField.getVisibility()))

        return root

    def _PyutParam2xml(self, pyutParam, xmlDoc):
        """
        Exporting a PyutParam to an miniDom Element.

        @param pyutParam : Parameters to save
        @param xmlDoc  : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('Param')

        # param name
        root.setAttribute('name', pyutParam.getName())

        # param type
        root.setAttribute('type', str(pyutParam.getType()))

        # param default value
        defaultValue = pyutParam.getDefaultValue()
        if defaultValue is not None:
            root.setAttribute('defaultValue', defaultValue)

        return root

    def _PyutLink2xml(self, pyutLink: PyutLink, xmlDoc):
        """
        Exporting an PyutLink to a miniDom Element.

        @param PyutLink pyutLink : Link to save
        @param xmlDoc : xml document
        @return Element : XML Node
        """

        root = xmlDoc.createElement('Link')
        # link name
        root.setAttribute('name', pyutLink.getName())

        # link type
        root.setAttribute('type', str(pyutLink.getType().value))

        # link cardinality source
        # root.setAttribute('cardSrc', pyutLink.getSourceCardinality())
        root.setAttribute('cardSrc', pyutLink.sourceCardinality)

        # link cardinality destination
        # root.setAttribute('cardDestination', pyutLink.getDestinationCardinality())
        root.setAttribute('cardDestination', pyutLink.destinationCardinality)

        # link bidir
        root.setAttribute('bidir', str(pyutLink.getBidir()))

        # link source
        srcLinkId = self._idFactory.getID(pyutLink.getSource())
        root.setAttribute('sourceId', str(srcLinkId))

        # link destination
        destLinkId = self._idFactory.getID(pyutLink.getDestination())
        root.setAttribute('destId', str(destLinkId))

        return root

    def _PyutMethod2xml(self, pyutMethod, xmlDoc):
        """
        Exporting an PyutMethod to an miniDom Element.

        @param PyutMethod pyutMethod : Method to save
        @param xmlDoc : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('Method')

        # method name
        root.setAttribute('name', pyutMethod.getName())

        # method visibility
        visibility = pyutMethod.getVisibility()
        if visibility is not None:
            root.setAttribute('visibility', str(visibility.getVisibility()))

        # for all modifiers
        for modifier in pyutMethod.getModifiers():
            xmlModifier = xmlDoc.createElement('Modifier')
            xmlModifier.setAttribute('name', modifier.getName())
            root.appendChild(xmlModifier)

        # method return type
        returnType = pyutMethod.getReturns()
        if returnType is not None:
            xmlReturnType = xmlDoc.createElement('Return')
            xmlReturnType.setAttribute('type', str(returnType))
            root.appendChild(xmlReturnType)

        # method params
        for param in pyutMethod.getParams():
            root.appendChild(self._PyutParam2xml(param, xmlDoc))

        return root

    def _PyutClass2xml(self, pyutClass: PyutClass, xmlDoc: Document):
        """
        Exporting an PyutClass to an miniDom Element.

        @param  pyutClass : Class to save

        @param xmlDoc : xml document

        @return Element : XML Node
        """
        root = xmlDoc.createElement('Class')

        # ID
        classId = self._idFactory.getID(pyutClass)
        root.setAttribute('id', str(classId))

        # class name
        root.setAttribute('name', pyutClass.getName())

        # class stereotype
        stereotype = pyutClass.getStereotype()
        if stereotype is not None:
            root.setAttribute('stereotype', stereotype.name)

        root.setAttribute('description', pyutClass.description)
        root.setAttribute('filename', pyutClass.getFilename())
        root.setAttribute('showMethods', str(pyutClass.showMethods))
        root.setAttribute('showFields',  str(pyutClass.showFields))
        root.setAttribute('showStereotype', str(pyutClass.getShowStereotype()))

        # methods
        for method in pyutClass.methods:
            root.appendChild(self._PyutMethod2xml(method, xmlDoc))

        # fields
        for field in pyutClass.fields:
            root.appendChild(self._PyutField2xml(field, xmlDoc))

        return root

    def _PyutNote2xml(self, pyutNote, xmlDoc):
        """
        Exporting an PyutNote to an miniDom Element.

        @param pyutNote : Note to convert
        @param xmlDoc : xml document
        @return Element          : New miniDom element
        """
        root = xmlDoc.createElement('Note')
        # ID
        noteId = self._idFactory.getID(pyutNote)
        root.setAttribute('id', str(noteId))

        # Note
        name = pyutNote.getName()
        name = name.replace('\n', "\\\\\\\\")
        root.setAttribute('name', name)
        root.setAttribute('filename', pyutNote.getFilename())

        return root

    def _PyutActor2xml(self, pyutActor, xmlDoc):
        """
        Exporting an PyutActor to an miniDom Element.

        @param PyutNote pyutActor : Note to convert
        @param xmlDoc : xml document
        @return Element : New miniDom element
        """
        root = xmlDoc.createElement('Actor')

        actorId = self._idFactory.getID(pyutActor)
        root.setAttribute('id', str(actorId))
        root.setAttribute('name', pyutActor.getName())
        root.setAttribute('filename', pyutActor.getFilename())

        return root

    def _PyutUseCase2xml(self, pyutUseCase, xmlDoc):
        """
        Exporting an PyutUseCase to a miniDom Element.

        @param PyutNote pyutUseCase : Note to convert
        @param xmlDoc xmlDoc : xml document
        @return Element : New miniDom element
        """
        root = xmlDoc.createElement('UseCase')

        useCaseId = self._idFactory.getID(pyutUseCase)
        root.setAttribute('id', str(useCaseId))

        # Note
        root.setAttribute('name', pyutUseCase.getName())

        # filename (lb@alawa.ch)
        root.setAttribute('filename', pyutUseCase.getFilename())

        return root

    def _appendOglBase(self, oglObject, root):
        """
        Saves the position and size of the OGL object in XML node.

        @param OglObject oglObject : OGL Object
        @param Element root : XML node to write
        """
        # Saving size
        w, h = oglObject.GetModel().GetSize()
        root.setAttribute('width', str(float(w)))
        root.setAttribute('height', str(float(h)))

        # Saving position
        x, y = oglObject.GetModel().GetPosition()
        root.setAttribute('x', str(x))
        root.setAttribute('y', str(y))

    def _OglLink2xml(self, oglLink: OglLink, xmlDoc: Document):
        """
        """
        root = xmlDoc.createElement('GraphicLink')

        # Append OGL object base
        # save src and dst anchor points
        x, y = oglLink.GetSource().GetModel().GetPosition()
        root.setAttribute('srcX', str(x))
        root.setAttribute('srcY', str(y))

        x, y = oglLink.GetDestination().GetModel().GetPosition()
        root.setAttribute('dstX', str(x))
        root.setAttribute('dstY', str(y))

        root.setAttribute('spline', str(oglLink.GetSpline()))

        if isinstance(oglLink, OglAssociation):

            center: OglAssociationLabel = oglLink.centerLabel
            src:    OglAssociationLabel = oglLink.sourceCardinality
            dst:    OglAssociationLabel = oglLink._destinationCardinality

            label = xmlDoc.createElement("LabelCenter")
            root.appendChild(label)

            label.setAttribute("x", str(center.oglPosition.x))
            label.setAttribute("y", str(center.oglPosition.y))
            label = xmlDoc.createElement("LabelSrc")
            root.appendChild(label)

            label.setAttribute("x", str(src.oglPosition.x))
            label.setAttribute("y", str(src.oglPosition.y))
            label = xmlDoc.createElement("LabelDst")
            root.appendChild(label)

            label.setAttribute("x", str(dst.oglPosition.x))
            label.setAttribute("y", str(dst.oglPosition.y))

        # save control points (not anchors!)
        for x, y in oglLink.GetSegments()[1:-1]:
            item = xmlDoc.createElement('ControlPoint')
            item.setAttribute('x', str(x))
            item.setAttribute('y', str(y))
            root.appendChild(item)

        # adding the data layer object
        root.appendChild(self._PyutLink2xml(oglLink.getPyutObject(), xmlDoc))

        return root

    def _OglClass2xml(self, oglClass: OglClass, xmlDoc: Document):
        """
        Exporting an OglClass to an miniDom Element.

        @param  oglClass : Class to save
        @param xmlDoc xmlDoc : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('GraphicClass')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglClass, root)

        # adding the data layer object
        root.appendChild(self._PyutClass2xml(oglClass.getPyutObject(), xmlDoc))

        return root

    def _OglNote2xml(self, oglNote, xmlDoc):
        """
        Exporting an OglNote to an miniDom Element.

        @param OglNote oglNote : Note to convert
        @param xmlDoc xmlDoc : xml document

        @return Element        : New miniDom element
        """
        root = xmlDoc.createElement('GraphicNote')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglNote, root)

        # adding the data layer object
        root.appendChild(self._PyutNote2xml(oglNote.getPyutObject(), xmlDoc))

        return root

    def _OglActor2xml(self, oglActor, xmlDoc):
        """
        Exporting an OglActor to an miniDom Element.

        @param OglActor oglActor : Actor to convert
        @param xmlDoc xmlDoc : xml document
        @return Element : New miniDom element
        """
        root = xmlDoc.createElement('GraphicActor')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglActor, root)

        # adding the data layer object
        root.appendChild(self._PyutActor2xml(oglActor.getPyutObject(), xmlDoc))

        return root

    def _OglUseCase2xml(self, oglUseCase, xmlDoc):
        """
        Exporting an OglUseCase to an miniDom Element.

        @param oglUseCase : UseCase to convert
        @param xmlDoc xmlDoc : xml document
        @return Element : New miniDom element

        """
        root = xmlDoc.createElement('GraphicUseCase')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglUseCase, root)

        # adding the data layer object
        root.appendChild(self._PyutUseCase2xml(oglUseCase.getPyutObject(), xmlDoc))

        return root

    def _getParam(self, domElement: Element) -> PyutParameter:

        pyutParam: PyutParameter = PyutParameter(name=domElement.getAttribute('name'), parameterType=domElement.getAttribute('type'))

        if domElement.hasAttribute('defaultValue'):
            pyutParam.setDefaultValue(domElement.getAttribute('defaultValue'))

        return pyutParam

    # noinspection PyUnusedLocal
    def _getOglSDInstances(self, xmlOglSDInstances, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglSDInstances : XML 'GraphicSDInstance' elements

        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded

        @param {id / srcName, OglLink} dicoLink : OGL links loaded

        @param {id / srcName, id / srcName} dicoFather: Inheritance

        @param UmlFrame umlFrame : Where to draw
        """
        for xmlOglSDInstance in xmlOglSDInstances:
            # Main objects
            pyutSDInstance = PyutSDInstance()
            oglSDInstance = OglSDInstance(pyutSDInstance, umlFrame)

            # Data layer
            xmlSDInstance = xmlOglSDInstance.getElementsByTagName('SDInstance')[0]

            # Pyut Data
            pyutSDInstance.setId(int(xmlSDInstance.getAttribute('id')))
            # pyutSDInstance.setInstanceName(xmlSDInstance.getAttribute('instanceName').encode("charmap"))
            # Python 3 is already UTF-8
            pyutSDInstance.setInstanceName(xmlSDInstance.getAttribute('instanceName'))

            pyutSDInstance.setInstanceLifeLineLength(secure_int(xmlSDInstance.getAttribute('lifeLineLength')))

            dicoOglObjects[pyutSDInstance.getId()] = oglSDInstance

            # Adding OGL class to UML Frame
            x = float(xmlOglSDInstance.getAttribute('x'))
            y = float(xmlOglSDInstance.getAttribute('y'))
            w = float(xmlOglSDInstance.getAttribute('width'))
            h = float(xmlOglSDInstance.getAttribute('height'))
            oglSDInstance.SetSize(w, h)
            umlFrame.addShape(oglSDInstance, x, y)

    # noinspection PyUnusedLocal
    def _getOglSDMessages(self, xmlOglSDMessages, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglSDMessages : XML 'GraphicSDInstance elements

        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded

        @param {id / srcName, OglLink} dicoLink : OGL links loaded

        @param {id / srcName, id / srcName} dicoFather: Inheritance

        @param UmlFrame umlFrame : Where to draw
        """
        for xmlOglSDMessage in xmlOglSDMessages:

            # Data layer class
            xmlPyutSDMessage = xmlOglSDMessage.getElementsByTagName('SDMessage')[0]

            # Building OGL
            pyutSDMessage = PyutSDMessage()
            srcID = int(xmlPyutSDMessage.getAttribute('srcID'))
            dstID = int(xmlPyutSDMessage.getAttribute('dstID'))
            srcTime = int(float(xmlPyutSDMessage.getAttribute('srcTime')))
            dstTime = int(float(xmlPyutSDMessage.getAttribute('dstTime')))
            srcOgl = dicoOglObjects[srcID]
            dstOgl = dicoOglObjects[dstID]
            oglSDMessage = OglSDMessage(srcOgl, pyutSDMessage, dstOgl)
            pyutSDMessage.setOglObject(oglSDMessage)
            pyutSDMessage.setSource(srcOgl.getPyutObject(), srcTime)
            pyutSDMessage.setDestination(dstOgl.getPyutObject(), dstTime)

            # Pyut Data
            pyutSDMessage.setId(int(xmlPyutSDMessage.getAttribute('id')))
            # Python 3 is already UTF-8
            pyutSDMessage.setMessage(xmlPyutSDMessage.getAttribute('message'))

            dicoOglObjects[pyutSDMessage.getId()] = pyutSDMessage

            # Adding OGL class to UML Frame
            diagram = umlFrame.GetDiagram()
            dicoOglObjects[srcID].addLink(oglSDMessage)
            dicoOglObjects[dstID].addLink(oglSDMessage)
            diagram.AddShape(oglSDMessage)
            # umlFrame.addShape(oglSDMessage, x, y)

    def _getControlPoints(self, link):
        """
        To extract control points from links.

        Python 3:  This method does not seem to be used;  I'll comment it out and raise an
        exception;  Especially, since I don't know where the `Class` class comes
        from == hasii
        """
        raise NotImplementedError('I guess this method is used after all.  See the comments')
        # class methods for this current class
        # allControlPoints = []
        #
        # for cp in Class.getElementsByTagName('ControlPoint'):
        #
        #     # point position
        #     x = cp.getAttribute('x')
        #     y = cp.getAttribute('y')
        #
        #     point = ControlPoint(x, y)
        #     allControlPoints.append(point)
        #
        # return allControlPoints

    def _getMethods(self, Class):
        """
        To extract methods from interface.
        """
        # class methods for this current class
        allMethods = []
        for Method in Class.getElementsByTagName("Method"):

            # method name
            aMethod = PyutMethod(Method.getAttribute('name'))

            # method visibility
            aMethod.setVisibility(Method.getAttribute('visibility'))

            # for method return type
            Return = Method.getElementsByTagName("Return")[0]
            aMethod.setReturns(Return.getAttribute('type'))

            # for methods param
            allParams = []
            for Param in Method.getElementsByTagName("Param"):
                allParams.append(self._getParam(Param))

            # setting the params for this method
            aMethod.setParams(allParams)
            # adding this method in all class methods
            allMethods.append(aMethod)

        return allMethods

    def _getFields(self, Class):
        """
        To extract fields from Class.
        """
        # for class fields
        allFields = []
        for Field in Class.getElementsByTagName("Field"):

            aField = PyutField()
            aField.setVisibility(Field.getAttribute('visibility'))
            Param = Field.getElementsByTagName("Param")[0]

            if Param.hasAttribute('defaultValue'):
                aField.setDefaultValue(Param.getAttribute('defaultValue'))
            aField.setName(Param.getAttribute('name'))
            aField.setType(Param.getAttribute('type'))

            allFields.append(aField)
        return allFields

    def _getPyutLink(self, obj):
        """
        To extract a PyutLink from an OglLink object.

        @param String obj : Name of the object.
        """
        link = obj.getElementsByTagName("Link")[0]

        aLink = PyutLink()

        aLink.setBidir(bool(link.getAttribute('bidir')))

        # aLink.setDestinationCardinality(link.getAttribute('cardDestination'))
        # aLink.setSourceCardinality(link.getAttribute('cardSrc'))
        aLink.destinationCardinality = link.getAttribute('cardDestination')
        aLink.sourceCardinality      = link.getAttribute('cardSrc')

        aLink.setName(link.getAttribute('name'))
        strLinkType: str = link.getAttribute('type')
        linkType: PyutLinkType = PyutLinkType(int(strLinkType))
        aLink.setType(linkType)
        # source and destination will be reconstructed by _getOglLinks

        sourceId = int(link.getAttribute('sourceId'))
        destId = int(link.getAttribute('destId'))

        return sourceId, destId, aLink

    # noinspection PyUnusedLocal
    def _getOglLinks(self, xmlOglLinks, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        To extract the links from an OGL object.
        """
        def secure_float(floatX):
            if floatX is not None:
                return float(floatX)
            return 0.0

        def secure_spline_int(splineX):
            if splineX is None:
                return 0
            elif splineX == "_DeprecatedNonBool: False" or splineX == "False":
                return 0
            elif splineX == "_DeprecatedNonBool: True" or splineX == "True":
                return 1
            else:
                return int(splineX)

        for link in xmlOglLinks:
            # src and dst anchor position
            sx = secure_float(link.getAttribute("srcX"))
            sy = secure_float(link.getAttribute("srcY"))
            dx = secure_float(link.getAttribute("dstX"))
            dy = secure_float(link.getAttribute("dstY"))
            spline = secure_spline_int(link.getAttribute("spline"))

            # create a list of ControlPoints
            ctrlpts = []
            for ctrlpt in link.getElementsByTagName("ControlPoint"):
                x = secure_float(ctrlpt.getAttribute("x"))
                y = secure_float(ctrlpt.getAttribute("y"))
                ctrlpts.append(ControlPoint(x, y))

            # get the associated PyutLink
            srcId, dstId, pyutLink = self._getPyutLink(link)

            # CD 20060218
            src = dicoOglObjects[srcId]
            dst = dicoOglObjects[dstId]
            linkType = pyutLink.getType()
            pyutLink = PyutLink("", linkType=linkType, source=src.getPyutObject(), destination=dst.getPyutObject())

            oglLinkFactory = getOglLinkFactory()
            oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)
            src.addLink(oglLink)
            dst.addLink(oglLink)
            umlFrame.GetDiagram().AddShape(oglLink, withModelUpdate=False)

            # create the OglLink
            oglLink.SetSpline(spline)

            # give it the PyutLink
            newPyutLink = pyutLink

            # copy the good information from the read link
            newPyutLink.setBidir(pyutLink.getBidir())
            # newPyutLink.setDestinationCardinality(pyutLink.getDestinationCardinality())
            # newPyutLink.setSourceCardinality(pyutLink.getSourceCardinality())
            newPyutLink.destinationCardinality = pyutLink.destinationCardinality
            newPyutLink.sourceCardinality      = pyutLink.sourceCardinality

            newPyutLink.setName(pyutLink.getName())

            # put the anchors at the right position
            srcAnchor = oglLink.GetSource()
            dstAnchor = oglLink.GetDestination()
            srcAnchor.SetPosition(sx, sy)
            dstAnchor.SetPosition(dx, dy)

            # add the control points to the line
            line = srcAnchor.GetLines()[0]  # only 1 line per anchor in pyut
            parent = line.GetSource().GetParent()
            selfLink = parent is line.GetDestination().GetParent()

            for ctrl in ctrlpts:
                line.AddControl(ctrl)
                if selfLink:
                    x, y = ctrl.GetPosition()
                    ctrl.SetParent(parent)
                    ctrl.SetPosition(x, y)

            if isinstance(oglLink, OglAssociation):
                # center = oglLink.getLabels()[CENTER]
                # src = oglLink.getLabels()[SRC_CARD]
                # dst = oglLink.getLabels()[DEST_CARD]

                label = link.getElementsByTagName("LabelCenter")[0]
                x = float(label.getAttribute("x"))
                y = float(label.getAttribute("y"))
                # center.SetPosition(x, y)
                oglLink.centerLabel.oglPosition.x = x
                oglLink.centerLabel.oglPosition.y = y

                label = link.getElementsByTagName("LabelSrc")[0]
                x = float(label.getAttribute("x"))
                y = float(label.getAttribute("y"))
                # src.SetPosition(x, y)
                oglLink.sourceCardinality.oglPosition.x = x
                oglLink.sourceCardinality.oglPosition.y = y

                label = link.getElementsByTagName("LabelDst")[0]
                x = float(label.getAttribute("x"))
                y = float(label.getAttribute("y"))
                dst.SetPosition(x, y)

    # noinspection PyUnusedLocal
    def _getOglActors(self, xmlOglActors, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT actors.

        @param Element[] xmlOglActors : XML 'GraphicActor' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} dicoFather: Inheritance
        @param UmlFrame umlFrame : Where to draw
        """
        for xmlOglActor in xmlOglActors:
            pyutActor = PyutActor()

            # Building OGL Actor
            height = float(xmlOglActor.getAttribute('height'))
            width = float(xmlOglActor.getAttribute('width'))
            oglActor = OglActor(pyutActor, width, height)

            xmlActor = xmlOglActor.getElementsByTagName('Actor')[0]

            pyutActor.setId(int(xmlActor.getAttribute('id')))

            # adding name for this class
            # pyutActor.setName(xmlActor.getAttribute('name').encode("charmap"))
            # Python 3 is already UTF-8
            pyutActor.setName(xmlActor.getAttribute('name'))

            # adding associated filename (lb@alawa.ch)
            pyutActor.setFilename(xmlActor.getAttribute('filename'))

            # Update dicos
            dicoOglObjects[pyutActor.getId()] = oglActor

            # Update UML Frame
            x = float(xmlOglActor.getAttribute('x'))
            y = float(xmlOglActor.getAttribute('y'))
            umlFrame.addShape(oglActor, x, y)

    # noinspection PyUnusedLocal
    def _getOglUseCases(self, xmlOglUseCases, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT actors.

        @param Element[] xmlOglUseCases : XML 'GraphicUseCase' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} dicoFather: Inheritance
        @param UmlFrame umlFrame : Where to draw
        """
        for xmlOglUseCase in xmlOglUseCases:
            pyutUseCase = PyutUseCase()

            # Building OGL UseCase
            height = float(xmlOglUseCase.getAttribute('height'))
            width = float(xmlOglUseCase.getAttribute('width'))
            oglUseCase = OglUseCase(pyutUseCase, width, height)

            xmlUseCase = xmlOglUseCase.getElementsByTagName('UseCase')[0]

            pyutUseCase.setId(int(xmlUseCase.getAttribute('id')))

            # adding name for this class
            # pyutUseCase.setName(xmlUseCase.getAttribute('name').encode("charmap"))
            # Python 3 is already utf-8;  don't need to encode anything
            pyutUseCase.setName(xmlUseCase.getAttribute('name'))

            # adding associated filename (lb@alawa.ch)
            pyutUseCase.setFilename(xmlUseCase.getAttribute('filename'))

            # Update dicos
            dicoOglObjects[pyutUseCase.getId()] = oglUseCase

            # Update UML Frame
            x = float(xmlOglUseCase.getAttribute('x'))
            y = float(xmlOglUseCase.getAttribute('y'))
            umlFrame.addShape(oglUseCase, x, y)

    # noinspection PyUnusedLocal
    def _getOglClasses(self, xmlOglClasses, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglClasses : XML 'GraphicClass' elements

        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded

        @param {id / srcName, OglLink} dicoLink : OGL links loaded

        @param {id / srcName, id / srcName} dicoFather: Inheritance

        @param UmlFrame umlFrame : Where to draw
        """
        for xmlOglClass in xmlOglClasses:

            pyutClass:PyutClass = PyutClass()

            # Building OGL class
            height   = float(xmlOglClass.getAttribute('height'))
            width    = float(xmlOglClass.getAttribute('width'))
            oglClass = OglClass(pyutClass, width, height)

            # Data layer class
            xmlClass = xmlOglClass.getElementsByTagName('Class')[0]

            pyutClass.setId(int(xmlClass.getAttribute('id')))

            # adding name for this class
            # pyutClass.setName(xmlClass.getAttribute('name').encode("charmap"))
            # Python 3 is already utf-8;  don't need to encode anything
            pyutClass.setName(xmlClass.getAttribute('name'))
            # print "PyutXml/open-4d00d"

            # adding description
            pyutClass.description = xmlClass.getAttribute('description')

            # adding stereotype
            if xmlClass.hasAttribute('stereotype'):
                pyutClass.setStereotype(PyutStereotype(xmlClass.getAttribute('stereotype')))

            # adding display properties (cd)
            value = secure_bool(xmlClass.getAttribute('showStereotype'))
            pyutClass.setShowStereotype(value)
            value = secure_bool(xmlClass.getAttribute('showMethods'))
            pyutClass.showMethods = value
            value = secure_bool(xmlClass.getAttribute('showFields'))
            pyutClass.showFields = value

            # adding associated filename (lb@alawa.ch)
            pyutClass.setFilename(xmlClass.getAttribute('filename'))

            # adding methods for this class
            pyutClass.methods = self._getMethods(xmlClass)

            # adding fields for this class
            pyutClass.fields = self._getFields(xmlClass)

            dicoOglObjects[pyutClass.getId()] = oglClass

            # Adding OGL class to UML Frame
            x = float(xmlOglClass.getAttribute('x'))
            y = float(xmlOglClass.getAttribute('y'))

            umlFrame.addShape(oglClass, x, y)

    # noinspection PyUnusedLocal
    def _getOglNotes(self, xmlOglNotes, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT notes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglNotes : XML 'GraphicNote' elements

        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded

        @param {id / srcName, OglLink} dicoLink : OGL links loaded

        @param {id / srcName, id / srcName} dicoFather: Inheritance

        @param UmlFrame umlFrame : Where to draw
        """
        for xmlOglNote in xmlOglNotes:
            pyutNote = PyutNote()

            # Building OGL Note
            height = float(xmlOglNote.getAttribute('height'))
            width = float(xmlOglNote.getAttribute('width'))
            oglNote = OglNote(pyutNote, width, height)

            xmlNote = xmlOglNote.getElementsByTagName('Note')[0]

            pyutNote.setId(int(xmlNote.getAttribute('id')))

            # adding note content for this class
            name = xmlNote.getAttribute('name')
            name = name.replace("\\\\\\\\", "\n")
            pyutNote.content = name

            # adding associated filename (lb@alawa.ch)
            pyutNote.setFilename(xmlNote.getAttribute('filename'))

            # Update dicos
            dicoOglObjects[pyutNote.getId()] = oglNote

            # Update UML Frame
            x = float(xmlOglNote.getAttribute('x'))
            y = float(xmlOglNote.getAttribute('y'))
            umlFrame.addShape(oglNote, x, y)
