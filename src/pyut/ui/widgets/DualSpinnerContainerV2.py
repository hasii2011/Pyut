
from typing import Callable

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import EVT_TEXT
from wx import ID_ANY

from wx import SpinCtrl
from wx import CommandEvent

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

SPINNER_WIDTH:  int = 60
SPINNER_HEIGHT: int = 35

@dataclass
class SpinnerValues:
    value0: int = 0
    value1: int = 0

class DualSpinnerContainerV2(SizedStaticBox):
    """
    A component that pairs two spinners in a horizontal panel;  Callers set
    the title to display and optionally the minimum and maximum spinner values
    Ideal for subclassing to use as a way to get x,y coordinates or width, height
    sizes
    """

    DEFAULT_MIN_VALUE: int = 100  # For the control only
    DEFAULT_MAX_VALUE: int = 300  # For the control only

    dscLogger: Logger = getLogger(__name__)     # Used as base class; So needs unique logger


    def __init__(self, sizedPanel: SizedPanel, boxTitle: str,
                 valueChangedCallback: Callable,
                 minValue: int = DEFAULT_MIN_VALUE, maxValue: int = DEFAULT_MAX_VALUE):
        """

        Args:
            sizedPanel   The parent panel
            boxTitle:    The text to display as the static box title
            valueChangedCallback:  The method to call when the value changes;  The method should expect the
                                   first parameter to be an object of type SpinnerValues
            minValue:       The minimum value for the spinner values
            maxValue:       The maximum value for the spinner values

        """

        super().__init__(sizedPanel, ID_ANY, boxTitle)

        self.SetSizerType('horizontal')
        # noinspection PyUnresolvedReferences
        self.SetSizerProps(expand=True, proportion=1, border=(('left','right', 'bottom'),5))

        self._callback: Callable = valueChangedCallback

        self._wxSpinner0Id: int = wxNewIdRef()
        self._wxSpinner1Id: int = wxNewIdRef()

        self._spinner0: SpinCtrl = SpinCtrl(self, self._wxSpinner0Id, "", size=(SPINNER_WIDTH, SPINNER_HEIGHT))
        self._spinner1: SpinCtrl = SpinCtrl(self, self._wxSpinner1Id, "", size=(SPINNER_WIDTH, SPINNER_HEIGHT))

        self._spinner0.SetRange(minValue, maxValue)
        self._spinner1.SetRange(minValue, maxValue)

        self._spinnerValues: SpinnerValues = SpinnerValues(minValue, minValue)
        #
        # Bind to the text control;  Then we can type in or spin
        self.Bind(EVT_TEXT, self._onSpinnerValueChanged, self._spinner0)
        self.Bind(EVT_TEXT, self._onSpinnerValueChanged, self._spinner1)

    def _setSpinnerValues(self, spinnerValues: SpinnerValues):
        """
        Write only;  The appropriate way to retrieve the values is via the change callback
        Args:
            spinnerValues:
        """
        self._spinnerValues = spinnerValues

    spinnerValues = property(fset=_setSpinnerValues, doc='Write only property to initialize spinner values')

    def _onSpinnerValueChanged(self, event: CommandEvent):

        eventId:  int = event.GetId()
        newValue: int = event.GetInt()

        if eventId == self._wxSpinner0Id:
            self._spinnerValues.value0  = newValue
        elif eventId == self._wxSpinner1Id:
            self._spinnerValues.value1  = newValue
        else:
            self.dscLogger.error(f'Unknown spinner event id: {eventId}')

        self._callback(self._spinnerValues)
