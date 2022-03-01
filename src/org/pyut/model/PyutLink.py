
from typing import Optional
from typing import Union
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from deprecated import deprecated

from org.pyut.model.PyutObject import PyutObject

if TYPE_CHECKING:
    from org.pyut.model.PyutClass import PyutClass
    from org.pyut.model.PyutNote import PyutNote
    
from org.pyut.enums.LinkType import LinkType

# noinspection PyProtectedMember
from org.pyut.general.Globals import _


class PyutLink(PyutObject):
    """
    A standard link between a Class or Note.

    A PyutLink represents a UML link between a Class or a Note in Pyut.

    Example:
    ```python

        myLink  = PyutLink("linkName", OglLinkType.OGL_INHERITANCE, "0", "*")
    ```
    """

    # noinspection PyUnresolvedReferences
    def __init__(self, name="", linkType: LinkType = LinkType.INHERITANCE,
                 cardSrc:      str = "", cardDest: str = "",
                 bidir:        bool = False,
                 source:       'PyutClass' = None,
                 destination:  Union['PyutClass', 'PyutNote'] = None):
        """

        Args:
            name:        The link name
            linkType:    The enum representing the link type
            cardSrc:     The source cardinality
            cardDest:    The destination cardinality
            bidir:      `True` if the link is bidirectional, else `False`
            source:      The source of the link
            destination: The destination of the link
        """
        super().__init__(name)
        self.logger: Logger       = getLogger(__name__)
        self._type:  LinkType = linkType

        self._sourceCardinality:      str  = cardSrc
        self._destinationCardinality: str  = cardDest
        self._bidirectional:          bool = bidir

        from org.pyut.model.PyutLinkedObject import PyutLinkedObject

        self._src:  Optional[PyutLinkedObject] = source
        self._dest: Optional[PyutLinkedObject] = destination

    def _getSourceCardinality(self) -> str:
        """
        Return a string representing source's cardinality

        Returns: string source cardinality
        """
        return self._sourceCardinality

    def _setSourceCardinality(self, cardSrc: str):
        """
        Update the source cardinality.

        Args:
            cardSrc:

        """
        self._sourceCardinality = cardSrc

    def _getDestinationCardinality(self):
        """
        Return a string representing cardinality destination.

        Returns: string destination cardinality
        """
        return self._destinationCardinality

    def _setDestinationCardinality(self, cardDest: str):
        """
        Updating destination cardinality.

        Args:
            cardDest
        """
        self._destinationCardinality = cardDest

    sourceCardinality      = property(_getSourceCardinality,      _setSourceCardinality)
    destinationCardinality = property(_getDestinationCardinality, _setDestinationCardinality)

    def getSource(self):
        """
        Return the source object of the link

        Returns: object Class or Note
        """
        return self._src

    def setSource(self, source):
        """
        Set the source object of this link.
        Args:
            source  PyutClass or PyutNote
        """
        self._src = source

    def getDestination(self):
        """
        Return an object destination who is linked to this link.

        Returns: object PyutClass or PyutNote
        """
        return self._dest

    def setDestination(self, destination):
        """
        Update the link destination.

        Args:
             destination -- PyutClass or PyutNote
        """
        self._dest = destination

    def getBidir(self) -> bool:
        """
        Get the link is bidirectional value

        Returns: `True` if the link is bidirectional else `False`
        """
        return self._bidirectional

    def setBidir(self, bidirectional: bool):
        """
        Update the bidirectional value

        Args:
             bidirectional
        """
        self._bidirectional = bidirectional

    @deprecated(reason='Use linkType')
    def setType(self, linkType: LinkType):
        """
        Update the link type

        Args:
              linkType : Type of the link
        """
        # Python 3 update
        # if type(theType) == StringType or type(theType) == UnicodeType:
        if type(linkType) is int:
            try:
                self._type = LinkType(linkType)
            except (ValueError, Exception) as e:
                self.logger.error(f'setType: {e}')
                self._type = LinkType.INHERITANCE
        else:
            self._type = linkType

    @deprecated(reason='Use linkType')
    def getType(self) -> LinkType:
        """
        Get the link type.

        Returns:
            The type of the link
        """
        return self._type

    @property
    def linkType(self) -> LinkType:
        return self._type

    @linkType.setter
    def linkType(self, theType: LinkType):
        self._type = theType

    def __str__(self):
        """
        String representation.

        Returns:
             string representing link
        """
        return _(f'("{self.getName()}") links from {self._src} to {self._dest}')
