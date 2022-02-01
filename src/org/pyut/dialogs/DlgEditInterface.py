
from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALIGN_RIGHT
from wx import ALL
from wx import EXPAND
from wx import OK

from wx import BoxSizer
from wx import CommandEvent

from org.pyut.dialogs.DlgEditClassCommon import DlgEditClassCommon

from org.pyut.model.PyutInterface import PyutInterface

# noinspection PyProtectedMember
from org.pyut.general.Globals import _


class DlgEditInterface(DlgEditClassCommon):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent, windowId, pyutInterface: PyutInterface):

        self._pyutInterface:     PyutInterface = pyutInterface
        self._pyutInterfaceCopy: PyutInterface = deepcopy(pyutInterface)

        super().__init__(parent, windowId, _('Edit Interface'), pyutModel=self._pyutInterfaceCopy, editInterface=True)

        self.logger: Logger = DlgEditInterface.clsLogger

        szrMethodButtons: BoxSizer = self._createMethodsUIArtifacts()

        self._szrMain.Add(self._lblMethod,     0, ALL, 5)
        self._szrMain.Add(self._lstMethodList, 1, ALL | EXPAND, 5)
        self._szrMain.Add(szrMethodButtons,    0, ALL | ALIGN_CENTER_HORIZONTAL, 5)

        self._szrMain.Add(self._szrButtons, 0, ALL | ALIGN_RIGHT, 5)

        # Fill Class name
        self._txtName.SetValue(self._pyutModelCopy.getName())
        self._fillMethodList()

        self._szrMain.Fit(self)

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        Called when the Ok button is pressed;  Implement
        Args:
            event:
        """
        #
        # Get common stuff from base class
        #
        self._pyutInterface.name        = self._pyutModelCopy.name
        self._pyutInterface.methods     = self._pyutModelCopy.methods
        self._pyutInterface.description = self._pyutModelCopy.description

        self._returnAction = OK     # This is probably obsolete
        self.SetReturnCode(OK)
        self.EndModal(OK)
