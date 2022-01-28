
from logging import Logger
from logging import getLogger

from org.pyut.general.datatypes.Dimensions import Dimensions
from org.pyut.general.datatypes.Position import Position

from org.pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize

from org.pyut.preferences.BaseSubPreference import BaseSubPreference

from org.pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from org.pyut.preferences.PreferencesCommon import PreferencesCommon


class MainPreferences(BaseSubPreference):

    MAIN_SECTION:    str = 'Main'

    USER_DIRECTORY:             str = 'userPath'
    ORG_DIRECTORY:              str = 'orgDirectory'
    LAST_DIRECTORY:             str = 'LastDirectory'
    SHOW_TIPS_ON_STARTUP:       str = 'Show_Tips_On_Startup'
    AUTO_RESIZE_SHAPE_ON_EDIT:  str = 'Auto_Resize_Shape_On_Edit'
    SHOW_PARAMETERS:            str = 'Show_Parameters'
    FULL_SCREEN:                str = 'Full_Screen'
    CURRENT_TIP:                str = 'Current_Tip'
    EDITOR:                     str = 'Editor'
    STARTUP_SIZE:               str = 'startup_size'
    STARTUP_POSITION:           str = 'startup_position'
    CENTER_DIAGRAM:             str = 'center_diagram'
    CENTER_APP_ON_STARTUP:      str = 'center_app_on_startup'  # If 'False' honor startup_x, startup_y
    TOOL_BAR_ICON_SIZE:         str = 'tool_bar_icon_size'

    MAIN_PREFERENCES: PREFS_NAME_VALUES = {
        USER_DIRECTORY:            '.',
        ORG_DIRECTORY:             '.',
        LAST_DIRECTORY:            '.',
        SHOW_TIPS_ON_STARTUP:      'False',
        AUTO_RESIZE_SHAPE_ON_EDIT: 'True',
        SHOW_PARAMETERS:           'False',
        FULL_SCREEN:               'False',
        CURRENT_TIP:               '0',
        EDITOR:                    'brackets',
        STARTUP_SIZE:              Dimensions(1024, 768).__str__(),
        STARTUP_POSITION:          Position(5, 5).__str__(),
        CENTER_DIAGRAM:            'False',
        CENTER_APP_ON_STARTUP:     'True',
        TOOL_BAR_ICON_SIZE:        ToolBarIconSize.SIZE_32.value
    }

    def init(self, *args, **kwds):

        self.logger:  Logger            = getLogger(__name__)

        BaseSubPreference.init(self, *args, **kwds)

        self._preferencesCommon: PreferencesCommon = PreferencesCommon(self._config)

    def addAnyMissingMainPreferences(self):

        try:
            if self._config.has_section(MainPreferences.MAIN_SECTION) is False:
                self._config.add_section(MainPreferences.MAIN_SECTION)

            for prefName in MainPreferences.MAIN_PREFERENCES.keys():
                if self._config.has_option(MainPreferences.MAIN_SECTION, prefName) is False:
                    self.__addMissingMainPreference(prefName, MainPreferences.MAIN_PREFERENCES[prefName])
        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    @property
    def userDirectory(self) -> str:
        return self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.USER_DIRECTORY)

    @userDirectory.setter
    def userDirectory(self, theNewValue: str):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.USER_DIRECTORY, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def orgDirectory(self) -> str:
        return self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.ORG_DIRECTORY)

    @orgDirectory.setter
    def orgDirectory(self, theNewValue: str):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.ORG_DIRECTORY, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def lastOpenedDirectory(self) -> str:
        return self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.LAST_DIRECTORY)

    @lastOpenedDirectory.setter
    def lastOpenedDirectory(self, theNewValue: str):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.LAST_DIRECTORY, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def showTipsOnStartup(self) -> bool:
        return self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.SHOW_TIPS_ON_STARTUP)

    @showTipsOnStartup.setter
    def showTipsOnStartup(self, newValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.SHOW_TIPS_ON_STARTUP, str(newValue))
        self._preferencesCommon.saveConfig()

    @property
    def autoResizeShapesOnEdit(self) -> bool:
        return self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.AUTO_RESIZE_SHAPE_ON_EDIT)

    @autoResizeShapesOnEdit.setter
    def autoResizeShapesOnEdit(self, newValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.AUTO_RESIZE_SHAPE_ON_EDIT, str(newValue))
        self._preferencesCommon.saveConfig()

    @property
    def showParameters(self) -> bool:
        return self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.SHOW_PARAMETERS)

    @showParameters.setter
    def showParameters(self, theNewValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.SHOW_PARAMETERS, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def fullScreen(self) -> bool:
        return self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.FULL_SCREEN)

    @fullScreen.setter
    def fullScreen(self, theNewValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.FULL_SCREEN, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def currentTip(self) -> int:
        return self._config.getint(MainPreferences.MAIN_SECTION, MainPreferences.CURRENT_TIP)

    @currentTip.setter
    def currentTip(self, theNewValue: int):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.CURRENT_TIP, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def editor(self) -> str:
        return self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.EDITOR)

    @editor.setter
    def editor(self, theNewValue: str):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.EDITOR, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def startupSize(self) -> Dimensions:

        serializedDimensions: str = self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_SIZE)
        return Dimensions.deSerialize(serializedDimensions)

    @startupSize.setter
    def startupSize(self, newValue: Dimensions):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_SIZE, newValue.__str__())
        self._preferencesCommon.saveConfig()

    @property
    def centerDiagram(self):
        centerDiagram: bool = self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.CENTER_DIAGRAM)
        return centerDiagram

    @centerDiagram.setter
    def centerDiagram(self, theNewValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.CENTER_DIAGRAM, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def centerAppOnStartUp(self) -> bool:
        centerApp: bool = self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.CENTER_APP_ON_STARTUP)
        return centerApp

    @centerAppOnStartUp.setter
    def centerAppOnStartUp(self, theNewValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.CENTER_APP_ON_STARTUP, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def startupPosition(self) -> Position:

        serializedPosition: str = self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_POSITION)
        return Position.deSerialize(serializedPosition)

    @startupPosition.setter
    def startupPosition(self, newValue: Position):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_POSITION, newValue.__str__())
        self._preferencesCommon.saveConfig()

    @property
    def toolBarIconSize(self) -> ToolBarIconSize:
        enumStr: str = self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.TOOL_BAR_ICON_SIZE)
        return ToolBarIconSize(enumStr)

    @toolBarIconSize.setter
    def toolBarIconSize(self, newSize: ToolBarIconSize):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.TOOL_BAR_ICON_SIZE, newSize.value)
        self._preferencesCommon.saveConfig()

    def __addMissingMainPreference(self, preferenceName, value: str):
        self._preferencesCommon.addMissingPreference(MainPreferences.MAIN_SECTION, preferenceName, value)
