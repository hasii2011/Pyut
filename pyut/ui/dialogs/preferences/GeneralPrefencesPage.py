
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import DD_DEFAULT_STYLE
from wx import DirDialog
from wx import EVT_BUTTON
from wx import EVT_CHECKBOX
from wx import EVT_SPINCTRL
from wx import ID_ANY

from wx import Button
from wx import CheckBox
from wx import CommandEvent
from wx import ID_OK
from wx import SpinCtrl
from wx import SpinEvent
from wx import TextCtrl
from wx import Window

from wx.lib.buttons import GenBitmapButton
from wx.lib.sized_controls import SizedPanel

from wx.lib.sized_controls import SizedStaticBox

from pyut.PyutUtils import PyutUtils

from pyut.ui.dialogs.preferences.BasePreferencesPage import BasePreferencesPage

from pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.resources.img import folder as ImgFolder


@dataclass
class ControlData:
    label:        str      = ''
    initialValue: bool     = False
    instanceVar:  CheckBox = cast(CheckBox, None)
    wxId:         int      = 0


class GeneralPreferencesPage(BasePreferencesPage):
    """
    Implemented using sized components for better platform look and feel
    Using wx IDs to minimize callbacks
    Since these are a bunch of checkboxes that drive true/false preferences,
    I can encapsulate creating them in a list with a dataclass that hosts all
    the necessary creation information;  How esoteric of me !!!  ;-(
    """

    def __init__(self, parent: Window):
        super().__init__(parent)
        self.SetSizerType('vertical')

        self.logger:  Logger = getLogger(__name__)
        self._change: bool   = False

        [
            self._maximizeWxId,        self._autoResizeWxId,            self._showTipsWxId,
            self._toolBarIconSizeWxId, self._loadLastOpenedProjectWxId, self._displayProjectExtensionWxId,
            self._virtualWindowWidthId,
            self._resetTipsWxId,
        ] = PyutUtils.assignID(8)

        self._btnResetTips:          Button   = cast(Button, None)
        self._textDiagramsDirectory: TextCtrl = cast(TextCtrl, None)
        self._virtualWindowWidth:    SpinCtrl = cast(SpinCtrl, None)

        p: PyutPreferences = self._preferences
        self._controlData = [
            ControlData(label='&Full Screen on startup',   initialValue=p.fullScreen,              wxId=self._maximizeWxId),
            ControlData(label='&Resize classes on edit',   initialValue=p.autoResizeShapesOnEdit,  wxId=self._autoResizeWxId),
            ControlData(label='Show &Tips on startup',     initialValue=p.showTipsOnStartup,       wxId=self._showTipsWxId),
            ControlData(label='&Large Toolbar Icons',      initialValue=self._isLargeIconSize(),   wxId=self._toolBarIconSizeWxId),
            ControlData(label='Load Last &Opened Project', initialValue=p.loadLastOpenedProject,   wxId=self._loadLastOpenedProjectWxId),
            ControlData(label='Display Project Extension', initialValue=p.displayProjectExtension, wxId=self._displayProjectExtensionWxId)
        ]

        self._layoutWindow(sizedPanel=self)

    def _layoutWindow(self, sizedPanel: SizedPanel):

        togglePanel: SizedStaticBox = SizedStaticBox(sizedPanel, label='')
        togglePanel.SetSizerType('Vertical')
        togglePanel.SetSizerProps(expand=True, proportion=6)

        for cd in self._controlData:
            control: ControlData = cast(ControlData, cd)
            control.instanceVar = CheckBox(togglePanel, control.wxId, label=control.label)
            control.instanceVar.SetValue(control.initialValue)
            sizedPanel.Bind(EVT_CHECKBOX, self._onValueChanged, id=control.wxId)

        self._btnResetTips = Button(togglePanel, self._resetTipsWxId, 'Reset Tips')

        virtualWindowWidthBox: SizedStaticBox = SizedStaticBox(sizedPanel, label='Virtual Window Width')
        virtualWindowWidthBox.SetSizerType('vertical')
        virtualWindowWidthBox.SetSizerProps(expand=False, proportion=2)

        self._virtualWindowWidth = SpinCtrl(virtualWindowWidthBox, self._virtualWindowWidthId, min=1000, max=25000, size=(75, 25))

        self._virtualWindowWidth.SetValue(self._preferences.virtualWindowWidth)
        sizedPanel.Bind(EVT_SPINCTRL, self._virtualWindowWidthChanged, id=self._virtualWindowWidthId)

        self._layoutDiagramsDirectory(sizedPanel)

        sizedPanel.Bind(EVT_BUTTON, self._onResetTips, id=self._resetTipsWxId)

        self._fixPanelSize(panel=self)

    def _layoutDiagramsDirectory(self, sizedPanel: SizedPanel):
        directoryPanel: SizedStaticBox = SizedStaticBox(sizedPanel, label='Diagrams Directory')

        directoryPanel.SetSizerType('horizontal')
        directoryPanel.SetSizerProps(expand=True, proportion=2)

        textCtrl: TextCtrl = TextCtrl(directoryPanel)
        textCtrl.SetSizerProps(expand=False, proportion=5)

        selectButton: GenBitmapButton = GenBitmapButton(directoryPanel, ID_ANY, ImgFolder.embeddedImage.GetBitmap())
        selectButton.SetSizerProps(expand=False, proportion=1)

        textCtrl.SetValue(self._preferences.diagramsDirectory)
        textCtrl.SetEditable(False)

        self._textDiagramsDirectory = textCtrl
        sizedPanel.Bind(EVT_BUTTON, self._onSelectDiagramsDirectory, selectButton)

    @property
    def name(self) -> str:
        return 'General'

    def _setControlValues(self):
        """
        I don't use this since, I am table driven
        """
        pass

    def _onValueChanged(self, event: CommandEvent):

        eventID:  int = event.GetId()
        newValue: bool = event.IsChecked()
        p:        PyutPreferences = self._preferences

        match eventID:
            case self._maximizeWxId:
                p.fullScreen = newValue
            case self._autoResizeWxId:
                p.autoResizeShapesOnEdit = newValue
            case self._showTipsWxId:
                p.showTipsOnStartup = newValue
            case self._toolBarIconSizeWxId:
                if newValue is True:
                    p.toolBarIconSize = ToolBarIconSize.SIZE_32
                else:
                    p.toolBarIconSize = ToolBarIconSize.SIZE_16
            case self._loadLastOpenedProjectWxId:
                p.loadLastOpenedProject = newValue
            case self._displayProjectExtensionWxId:
                p.displayProjectExtension = newValue
            case _:
                self.logger.error(f'Unknown event ID')

        self._changed = True

    # noinspection PyUnusedLocal
    def _onResetTips(self, event: CommandEvent):
        self._preferences.currentTip = 0

    # noinspection PyUnusedLocal
    def _onSelectDiagramsDirectory(self, event: CommandEvent):
        with DirDialog(None, 'Choose the Diagrams Directory', style=DD_DEFAULT_STYLE) as dlg:
            if dlg.ShowModal() == ID_OK:
                self._preferences.diagramsDirectory = dlg.GetPath()
                self._textDiagramsDirectory.SetValue(self._preferences.diagramsDirectory)

    # noinspection PyUnusedLocal
    def _virtualWindowWidthChanged(self, event: SpinEvent):

        self._preferences.virtualWindowWidth = self._virtualWindowWidth.GetValue()

    def _isLargeIconSize(self) -> bool:
        if self._preferences.toolBarIconSize == ToolBarIconSize.SIZE_32:
            return True
        else:
            return False
