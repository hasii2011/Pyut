
from typing import cast

from logging import Logger
from logging import getLogger

from pyutmodelv2.PyutUseCase import PyutUseCase

from ogl.OglUseCase import OglUseCase

from pyut.ui.wxcommands.BaseWxCreateCommand import BaseWxCreateCommand

from pyut.ui.eventengine.EventType import EventType

from pyut.ui.eventengine.IEventEngine import IEventEngine


class CommandCreateOglUseCase(BaseWxCreateCommand):

    def __init__(self, x: int, y: int, eventEngine: IEventEngine):

        super().__init__(canUndo=True, name='Create Use Case', x=x, y=y, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

    def _createPrototypeInstance(self) -> OglUseCase:

        pyutUseCase: PyutUseCase = PyutUseCase(name=self._oglPreferences.defaultNameUsecase)
        oglUseCase:  OglUseCase  = OglUseCase(pyutUseCase)

        return oglUseCase

    def _placeShapeOnFrame(self):

        oglUseCase:  OglUseCase  = cast(OglUseCase, self._shape)                 # get old or prototype on first use

        pyutUseCase: PyutUseCase = cast(PyutUseCase, oglUseCase.pyutObject)
        self._oglObjWidth, self._oglObjHeight = oglUseCase.GetSize()

        self._shape = OglUseCase(pyutUseCase, w=self._oglObjWidth, h=self._oglObjHeight)      # create new one

        self._eventEngine.sendEvent(EventType.EditUseCase, pyutUseCase=pyutUseCase)

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbAddOglObjectToFrame)
