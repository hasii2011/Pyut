
from logging import Logger
from logging import getLogger

from sys import exc_info
from traceback import extract_tb

from wx import CENTRE
from wx import ICON_ERROR
from wx import ICON_EXCLAMATION
from wx import ICON_INFORMATION
from wx import MessageDialog
from wx import OK

from org.pyut.general.Globals import _


class GraphicErrorView:
    """
    This class is an error view which will display error as
    wx message dialogs.

    To use it, use the mediator methods :
     - mediator = Mediator.getMediator()
     -
     - errorManager = mediator.getErrorManager()
     - errorManager.changeType(ErrorViewTypes.GRAPHIC_ERROR_VIEW)
     - errorManager.newFatalError("This is a message", "...")
     - errorManager.newWarning("This is a message", "...")
     - errorManager.newInformation("This is a message", "...")
     -
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def newFatalError(self, msg, title=None, parent=None):

        if title is None:
            title = _("An error occurred...")
        errMsg = msg + "\n\n"
        errMsg += _("The following error occurred : %s") % str(exc_info()[1])
        errMsg += "\n\n---------------------------\n"
        if exc_info()[0] is not None:
            errMsg += "Error : %s" % exc_info()[0] + "\n"
        if exc_info()[1] is not None:
            errMsg += "Msg   : %s" % exc_info()[1] + "\n"
        if exc_info()[2] is not None:
            errMsg += "Trace :\n"
            for el in extract_tb(exc_info()[2]):
                errMsg = errMsg + str(el) + "\n"

        self.logger.error(errMsg)
        try:
            dlg = MessageDialog(parent, errMsg,  title, OK | ICON_ERROR | CENTRE)
            dlg.ShowModal()
            dlg.Destroy()
        except (ValueError, Exception) as e:
            self.logger.error(f'newFatalError: {e}')

    def newWarning(self, msg, title=None, parent=None):

        if title is None:
            title = _("WARNING...")
        self.logger.error(msg)
        try:
            dlg = MessageDialog(parent, msg, title, OK | ICON_EXCLAMATION | CENTRE)
            dlg.ShowModal()
            dlg.Destroy()
        except (ValueError, Exception) as e:
            self.logger.error(f'newWarning: {e}')

    def newInformation(self, msg, title=None, parent=None):

        if title is None:
            title = _("WARNING...")
        self.logger.error(msg)
        try:
            dlg = MessageDialog(parent, msg, title, OK | ICON_INFORMATION | CENTRE)
            dlg.ShowModal()
            dlg.Destroy()

        except (ValueError, Exception) as e:
            self.logger.error(f'newInformation: {e}')

    def displayInformation(self, msg, title=None, parent=None):
        self.logger.error(f"INFORMATION: {title} - {msg} - parent {parent}")
