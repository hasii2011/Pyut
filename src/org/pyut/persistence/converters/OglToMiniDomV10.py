
from typing import Tuple
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint

from org.pyut.enums.AttachmentPoint import AttachmentPoint

from org.pyut.model.PyutActor import PyutActor
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutClassCommon import PyutClassCommon
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutInterface import PyutInterface
from org.pyut.model.PyutLink import PyutLink
from org.pyut.model.PyutNote import PyutNote
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutSDInstance import PyutSDInstance
from org.pyut.model.PyutSDMessage import PyutSDMessage
from org.pyut.model.PyutText import PyutText
from org.pyut.model.PyutUseCase import PyutUseCase
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglAssociation import OglAssociation
from org.pyut.ogl.OglAssociationLabel import OglAssociationLabel
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglInterface2 import OglInterface2
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglText import OglText
from org.pyut.ogl.OglUseCase import OglUseCase
from org.pyut.ogl.sd.OglSDInstance import OglSDInstance
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage

from org.pyut.persistence.converters.PyutXmlConstants import PyutXmlConstants
from org.pyut.persistence.converters.IDFactory import IDFactory


class OglToMiniDom:
    """
    The refactored version of the original methods that were part of the monolithic
     PyutXml`xxx` classes.

     This version is
        * renamed for clarity
        * uses typing for developer clarity
        * removes 'magic' strings shared between it and the ToOgl/ToPyutXml classes
        * Updated using google docstrings

    """
    def __init__(self):

        self.logger:     Logger    = getLogger(__name__)
        self._idFactory: IDFactory = IDFactory()

    def oglClassToXml(self, oglClass: OglClass, xmlDoc: Document) -> Element:
        """
        Exports an OglClass to a minidom Element.

        Args:
            oglClass:   Graphic Class to save
            xmlDoc:     The document to append to

        Returns:
            The newly created `GraphicClass` element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_CLASS)

        root = self.__appendOglBase(oglClass, root)

        # adding the data layer object
        root.appendChild(self._pyutClassToXml(cast(PyutClass, oglClass.getPyutObject()), xmlDoc))

        return root

    def oglInterface2ToXml(self, oglInterface: OglInterface2, xmlDoc: Document) -> Element:
        """

        Args:
            oglInterface:   Lollipop to convert
            xmlDoc:         xml document

        Returns:
            New minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_LOLLIPOP)

        destAnchor:      SelectAnchorPoint = oglInterface.destinationAnchor
        attachmentPoint: AttachmentPoint   = destAnchor.attachmentPoint
        x, y = destAnchor.GetPosition()

        root.setAttribute(PyutXmlConstants.ATTR_LOLLIPOP_ATTACHMENT_POINT, attachmentPoint.__str__())
        root.setAttribute(PyutXmlConstants.ATTR_X, str(x))
        root.setAttribute(PyutXmlConstants.ATTR_Y, str(y))

        # parentUmlClass: OglClass = destAnchor.GetParent()
        # parentId:       int      = self._idFactory.getID(parentUmlClass.getPyutObject())
        # self.logger.info(f'Interface implemented by class id: {parentId}')

        # root.setAttribute(PyutXmlConstants.ATTR_IMPLEMENTED_BY_CLASS_ID, str(parentId))
        root.appendChild(self._pyutInterfaceToXml(oglInterface.pyutInterface, xmlDoc))

        return root

    def oglNoteToXml(self, oglNote: OglNote, xmlDoc: Document) -> Element:
        """
        Export an OglNote to a minidom Element.

        Args:
            oglNote:    Note to convert
            xmlDoc:     xml document

        Returns:
            New minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_NOTE)

        self.__appendOglBase(oglNote, root)

        root.appendChild(self._pyutNoteToXml(cast(PyutNote, oglNote.getPyutObject()), xmlDoc))

        return root

    def oglTextToXml(self, oglText: OglText, xmlDoc: Document) -> Element:

        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_TEXT)

        self.__appendOglBase(oglText, root)
        root.appendChild(self._pyutTextToXml(oglText.pyutText, xmlDoc))

        return root

    def oglActorToXml(self, oglActor: OglActor, xmlDoc: Document) -> Element:
        """
        Exporting an OglActor to a minidom Element.

        Args:
            oglActor:   Actor to convert
            xmlDoc:     xml document

        Returns:
            New minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_ACTOR)

        self.__appendOglBase(oglActor, root)

        root.appendChild(self._pyutActorToXml(cast(PyutActor, oglActor.getPyutObject()), xmlDoc))

        return root

    def oglUseCaseToXml(self, oglUseCase: OglUseCase, xmlDoc: Document) -> Element:
        """
        Export an OglUseCase to a minidom Element.

        Args:
            oglUseCase:  UseCase to convert
            xmlDoc:      xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_USE_CASE)

        self.__appendOglBase(oglUseCase, root)

        root.appendChild(self._pyutUseCaseToXml(cast(PyutUseCase, oglUseCase.getPyutObject()), xmlDoc))

        return root

    def oglLinkToXml(self, oglLink: OglLink, xmlDoc: Document):
        """
        Export an OgLink to a minidom element
        Args:
            oglLink:    OglLink to convert
            xmlDoc:     xml document

        Returns:
            A new minidom element
        """
        root = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_LINK)

        # save source and destination anchor points
        x, y = oglLink.GetSource().GetModel().GetPosition()
        simpleX, simpleY = self.__getSimpleCoordinates(x, y)
        root.setAttribute(PyutXmlConstants.ATTR_LINK_SOURCE_ANCHOR_X, simpleX)
        root.setAttribute(PyutXmlConstants.ATTR_LINK_SOURCE_ANCHOR_Y, simpleY)

        x, y = oglLink.GetDestination().GetModel().GetPosition()
        simpleX, simpleY = self.__getSimpleCoordinates(x, y)

        root.setAttribute(PyutXmlConstants.ATTR_LINK_DESTINATION_ANCHOR_X, simpleX)
        root.setAttribute(PyutXmlConstants.ATTR_LINK_DESTINATION_ANCHOR_Y, simpleY)

        root.setAttribute(PyutXmlConstants.ATTR_SPLINE, str(oglLink.GetSpline()))

        if isinstance(oglLink, OglAssociation):

            center: OglAssociationLabel = oglLink.centerLabel
            src:    OglAssociationLabel = oglLink.sourceCardinality
            dst:    OglAssociationLabel = oglLink.destinationCardinality

            assocLabels = {
                PyutXmlConstants.ELEMENT_ASSOC_CENTER_LABEL:      center,
                PyutXmlConstants.ELEMENT_ASSOC_SOURCE_LABEL:      src,
                PyutXmlConstants.ELEMENT_ASSOC_DESTINATION_LABEL: dst
            }
            for eltName in assocLabels:
                elt: Element = self.__createAssocLabelElement(eltName, xmlDoc, assocLabels[eltName])
                root.appendChild(elt)

        # save control points (not anchors!)
        for x, y in oglLink.GetSegments()[1:-1]:
            item = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_CONTROL_POINT)
            item.setAttribute(PyutXmlConstants.ATTR_X, str(x))
            item.setAttribute(PyutXmlConstants.ATTR_Y, str(y))
            root.appendChild(item)

        # adding the data layer object

        root.appendChild(self._pyutLinkToXml(oglLink.getPyutObject(), xmlDoc))

        return root

    def oglSDInstanceToXml(self, oglSDInstance: OglSDInstance, xmlDoc: Document) -> Element:
        """
        Export an OglSDInstance to a minidom Element

        Args:
            oglSDInstance:  Instance to convert
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_SD_INSTANCE)

        self.__appendOglBase(oglSDInstance, root)

        root.appendChild(self._pyutSDInstanceToXml(cast(PyutSDInstance, oglSDInstance.getPyutObject()), xmlDoc))

        return root

    def oglSDMessageToXml(self, oglSDMessage: OglSDMessage, xmlDoc: Document) -> Element:
        """
        Export an OglSDMessage to a minidom Element.

        Args:
            oglSDMessage:   Message to convert
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        root = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_SD_MESSAGE)

        # adding the data layer object
        root.appendChild(self._pyutSDMessageToXml(oglSDMessage.getPyutObject(), xmlDoc))

        return root

    def _pyutClassToXml(self, pyutClass: PyutClass, xmlDoc: Document) -> Element:
        """
        Exporting a PyutClass to a miniDom Element.

        Args:
            pyutClass:  The pyut class to save
            xmlDoc:     The xml document to update

        Returns:
            The new updated element
        """
        root = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_CLASS)

        classId: int = self._idFactory.getID(pyutClass)
        root.setAttribute(PyutXmlConstants.ATTR_ID, str(classId))
        root.setAttribute(PyutXmlConstants.ATTR_NAME, pyutClass.getName())

        stereotype = pyutClass.getStereotype()
        if stereotype is not None:
            root.setAttribute(PyutXmlConstants.ATTR_STEREOTYPE, stereotype.getStereotype())

        root.setAttribute(PyutXmlConstants.ATTR_FILENAME,    pyutClass.getFilename())

        root = self._pyutClassCommonToXml(pyutClass, root)

        root.setAttribute(PyutXmlConstants.ATTR_SHOW_METHODS,       str(pyutClass.showMethods))
        root.setAttribute(PyutXmlConstants.ATTR_SHOW_FIELDS,        str(pyutClass.showFields))
        root.setAttribute(PyutXmlConstants.ATTR_SHOW_STEREOTYPE,    str(pyutClass.getShowStereotype()))
        root.setAttribute(PyutXmlConstants.ATTR_DISPLAY_PARAMETERS, pyutClass.displayParameters.value)

        # methods
        for method in pyutClass.methods:
            root.appendChild(self._pyutMethodToXml(method, xmlDoc))
        # fields
        for field in pyutClass.fields:
            root.appendChild(self._pyutFieldToXml(field, xmlDoc))

        return root

    def _pyutInterfaceToXml(self, pyutInterface: PyutInterface, xmlDoc: Document) -> Element:

        root = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_INTERFACE)

        classId: int = self._idFactory.getID(pyutInterface)
        root.setAttribute(PyutXmlConstants.ATTR_ID, str(classId))
        root.setAttribute(PyutXmlConstants.ATTR_NAME, pyutInterface.getName())

        root = self._pyutClassCommonToXml(pyutInterface, root)

        for method in pyutInterface.methods:
            root.appendChild(self._pyutMethodToXml(method, xmlDoc))

        for className in pyutInterface.implementors:
            self.logger.info(f'implementing className: {className}')
            root.appendChild(self._pyutImplementorToXml(className, xmlDoc))

        return root

    def _pyutClassCommonToXml(self, classCommon: PyutClassCommon, root: Element) -> Element:

        root.setAttribute(PyutXmlConstants.ATTR_DESCRIPTION, classCommon.description)
        # root.setAttribute(PyutXmlConstants.ATTR_FILENAME,    pyutInterface.getFilename())

        return root

    def _pyutMethodToXml(self, pyutMethod, xmlDoc) -> Element:
        """
        Exporting a PyutMethod to a miniDom Element

        Args:
            pyutMethod: Method to save
            xmlDoc:     xml document

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_METHOD)

        root.setAttribute(PyutXmlConstants.ATTR_NAME, pyutMethod.getName())

        visibility: PyutVisibilityEnum = pyutMethod.getVisibility()
        visName:    str                = self.__safeVisibilityToName(visibility)

        if visibility is not None:
            root.setAttribute(PyutXmlConstants.ATTR_VISIBILITY, visName)

        for modifier in pyutMethod.getModifiers():
            xmlModifier: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_MODIFIER)
            xmlModifier.setAttribute(PyutXmlConstants.ATTR_NAME, modifier.getName())
            root.appendChild(xmlModifier)

        returnType = pyutMethod.getReturns()
        if returnType is not None:
            xmlReturnType: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_RETURN)
            xmlReturnType.setAttribute(PyutXmlConstants.ATTR_TYPE, str(returnType))
            root.appendChild(xmlReturnType)

        for param in pyutMethod.getParams():
            root.appendChild(self._pyutParamToXml(param, xmlDoc))

        return root

    def _pyutImplementorToXml(self, className: PyutInterface.ClassName, xmlDoc: Document) -> Element:

        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_IMPLEMENTOR)

        root.setAttribute(PyutXmlConstants.ATTR_IMPLEMENTING_CLASS_NAME, className)

        return root

    def _pyutFieldToXml(self, pyutField: PyutField, xmlDoc: Document) -> Element:
        """
        Export a PyutField to a miniDom Element
        Args:
            pyutField:  The PyutField to save
            xmlDoc:     The xml document to update

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_FIELD)

        root.appendChild(self._pyutParamToXml(pyutField, xmlDoc))
        visibility: PyutVisibilityEnum = pyutField.getVisibility()
        visName:    str                = self.__safeVisibilityToName(visibility)
        root.setAttribute(PyutXmlConstants.ATTR_VISIBILITY, visName)

        return root

    def _pyutParamToXml(self, pyutParam: PyutParam, xmlDoc: Document) -> Element:
        """
        Export a PyutParam to a miniDom Element

        Args:
            pyutParam:  Parameter to save
            xmlDoc:     XML Node

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_PARAM)

        root.setAttribute(PyutXmlConstants.ATTR_NAME, pyutParam.getName())
        root.setAttribute(PyutXmlConstants.ATTR_TYPE, str(pyutParam.getType()))

        defaultValue = pyutParam.getDefaultValue()
        if defaultValue is not None:
            root.setAttribute(PyutXmlConstants.ATTR_DEFAULT_VALUE, defaultValue)

        return root

    def _pyutNoteToXml(self, pyutNote: PyutNote, xmlDoc: Document) -> Element:
        """
        Export a PyutNote to a miniDom Element.

        Args:
            pyutNote:   Note to convert
            xmlDoc:     xml document

        Returns:
            New miniDom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_NOTE)

        noteId: int = self._idFactory.getID(pyutNote)
        root.setAttribute(PyutXmlConstants.ATTR_ID, str(noteId))

        content: str = pyutNote.content
        content = content.replace('\n', "\\\\\\\\")
        root.setAttribute(PyutXmlConstants.ATTR_CONTENT, content)

        root.setAttribute(PyutXmlConstants.ATTR_FILENAME, pyutNote.getFilename())

        return root

    def _pyutTextToXml(self, pyutText: PyutText, xmlDoc: Document) -> Element:

        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_TEXT)
        textId: int = self._idFactory.getID(pyutText)

        root.setAttribute(PyutXmlConstants.ATTR_ID, str(textId))
        content: str = pyutText.content
        content = content.replace('\n', "\\\\\\\\")

        root.setAttribute(PyutXmlConstants.ATTR_CONTENT, content)
        root.setAttribute(PyutXmlConstants.ATTR_TEXT_SIZE,     str(pyutText.textSize))
        root.setAttribute(PyutXmlConstants.ATTR_IS_BOLD,       str(pyutText.isBold))
        root.setAttribute(PyutXmlConstants.ATTR_IS_ITALICIZED, str(pyutText.isItalicized))
        root.setAttribute(PyutXmlConstants.ATTR_FONT_NAME,     pyutText.textFont.value)

        return root

    def _pyutActorToXml(self, pyutActor: PyutActor, xmlDoc: Document) -> Element:
        """
        Export an PyutActor to a minidom Element.
        Args:
            pyutActor:  Actor to convert
            xmlDoc:     xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_ACTOR)

        actorId = self._idFactory.getID(pyutActor)
        root.setAttribute(PyutXmlConstants.ATTR_ID, str(actorId))
        root.setAttribute(PyutXmlConstants.ATTR_NAME, pyutActor.getName())
        root.setAttribute(PyutXmlConstants.ATTR_FILENAME, pyutActor.getFilename())

        return root

    def _pyutUseCaseToXml(self, pyutUseCase: PyutUseCase, xmlDoc: Document) -> Element:
        """
        Export a PyutUseCase to a minidom Element.

        Args:
            pyutUseCase:    Use case to convert
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        root = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_USE_CASE)

        useCaseId = self._idFactory.getID(pyutUseCase)
        root.setAttribute(PyutXmlConstants.ATTR_ID,       str(useCaseId))
        root.setAttribute(PyutXmlConstants.ATTR_NAME,     pyutUseCase.getName())
        root.setAttribute(PyutXmlConstants.ATTR_FILENAME, pyutUseCase.getFilename())

        return root

    def _pyutLinkToXml(self, pyutLink: PyutLink, xmlDoc: Document) -> Element:
        """
        Exporting a PyutLink to a miniDom Element.

        Args:
            pyutLink:   Link to save
            xmlDoc:     xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_LINK)

        root.setAttribute(PyutXmlConstants.ATTR_NAME,            pyutLink.getName())
        root.setAttribute(PyutXmlConstants.ATTR_TYPE,            pyutLink.getType().name)
        root.setAttribute(PyutXmlConstants.ATTR_CARDINALITY_SOURCE,      pyutLink.sourceCardinality)
        root.setAttribute(PyutXmlConstants.ATTR_CARDINALITY_DESTINATION, pyutLink.destinationCardinality)
        root.setAttribute(PyutXmlConstants.ATTR_BIDIRECTIONAL,           str(pyutLink.getBidir()))

        srcLinkId:  int = self._idFactory.getID(pyutLink.getSource())
        destLinkId: int = self._idFactory.getID(pyutLink.getDestination())

        root.setAttribute(PyutXmlConstants.ATTR_SOURCE_ID,      str(srcLinkId))
        root.setAttribute(PyutXmlConstants.ATTR_DESTINATION_ID, str(destLinkId))

        return root

    def _pyutSDInstanceToXml(self, pyutSDInstance: PyutSDInstance, xmlDoc: Document) -> Element:
        """
        Exporting a PyutSDInstance to an minidom Element.

        Args:
            pyutSDInstance:     Class to convert
            xmlDoc:             xml document

        Returns:
            A new minidom element
        """
        root:  Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_SD_INSTANCE)
        eltId: int     = self._idFactory.getID(pyutSDInstance)

        root.setAttribute(PyutXmlConstants.ATTR_ID,               str(eltId))
        root.setAttribute(PyutXmlConstants.ATTR_INSTANCE_NAME,    pyutSDInstance.getInstanceName())
        root.setAttribute(PyutXmlConstants.ATTR_LIFE_LINE_LENGTH, str(pyutSDInstance.getInstanceLifeLineLength()))

        return root

    def _pyutSDMessageToXml(self, pyutSDMessage: PyutSDMessage, xmlDoc: Document) -> Element:
        """
        Exporting a PyutSDMessage to an minidom Element.
        Args:
            pyutSDMessage:  SDMessage to export
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_SD_MESSAGE)

        eltId = self._idFactory.getID(pyutSDMessage)
        root.setAttribute(PyutXmlConstants.ATTR_ID, str(eltId))

        # message
        root.setAttribute(PyutXmlConstants.ATTR_MESSAGE, pyutSDMessage.getMessage())

        # time
        idSrc = self._idFactory.getID(pyutSDMessage.getSource())
        idDst = self._idFactory.getID(pyutSDMessage.getDest())
        root.setAttribute(PyutXmlConstants.ATTR_SOURCE_TIME_LINE,      str(pyutSDMessage.getSrcTime()))
        root.setAttribute(PyutXmlConstants.ATTR_DESTINATION_TIME_LINE, str(pyutSDMessage.getDstTime()))
        root.setAttribute(PyutXmlConstants.ATTR_SD_MESSAGE_SOURCE_ID,      str(idSrc))
        root.setAttribute(PyutXmlConstants.ATTR_SD_MESSAGE_DESTINATION_ID, str(idDst))

        return root

    def __createAssocLabelElement(self, eltText: str, xmlDoc: Document, oglLabel: OglAssociationLabel) -> Element:
        """
        Creates an element of the form:

        ```html
        `<eltText x="nnnn.n" y="nnnn.n"/>`
        ```

        e.g.

        ```html
            `<LabelCenter x="1811.0" y="1137.5"/>`
        ```

        Args:
            eltText:    The element name
            xmlDoc:     The minidom document
            oglLabel:   A description of a label includes text and position

        Returns:
            A new minidom element
        """
        label: Element = xmlDoc.createElement(eltText)

        x: int = oglLabel.oglPosition.x
        y: int = oglLabel.oglPosition.y

        simpleX, simpleY = self.__getSimpleCoordinates(x, y)
        self.logger.info(f'x,y = ({x},{y})   simpleX,simpleY = ({simpleX},{simpleY})')
        label.setAttribute(PyutXmlConstants.ATTR_X, simpleX)
        label.setAttribute(PyutXmlConstants.ATTR_Y, simpleY)

        return label

    def __appendOglBase(self, oglObject: OglObject, root: Element) -> Element:
        """
        Saves the position and size of the OGL object in XML node.

        Args:
            oglObject:  OGL Object
            root:      XML node to update

        Returns:
            The updated element
        """
        # Saving size
        w, h = oglObject.GetModel().GetSize()
        simpleW, simpleH = self.__getSimpleDimensions(w, h)
        root.setAttribute(PyutXmlConstants.ATTR_WIDTH,  simpleW)
        root.setAttribute(PyutXmlConstants.ATTR_HEIGHT, simpleH)

        # Saving position
        x, y = oglObject.GetModel().GetPosition()
        simpleX, simpleY = self.__getSimpleCoordinates(x, y)
        root.setAttribute(PyutXmlConstants.ATTR_X, simpleX)
        root.setAttribute(PyutXmlConstants.ATTR_Y, simpleY)

        return root

    def __getSimpleDimensions(self, w: int, h: int) -> Tuple[str, str]:
        # reuse code but not name
        return self.__getSimpleCoordinates(w, h)

    def __getSimpleCoordinates(self, x: int, y: int) -> Tuple[str, str]:
        """

        Args:
            x: coordinate
            y: coordinate

        Returns:
            Simple formatted string versions of the above

        """
        simpleX: str = str(int(x))      # some older files used float
        simpleY: str = str(int(y))      # some older files used float

        return simpleX, simpleY

    def __safeVisibilityToName(self, visibility: Union[str, PyutVisibilityEnum]) -> str:
        """
        Account for old pre V10 code
        Args:
            visibility:

        Returns:
            The visibility name
        """

        if isinstance(visibility, str):
            visStr: str = PyutVisibilityEnum.toEnum(visibility).name
        else:
            visStr = visibility.name

        return visStr
