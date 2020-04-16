
from os import chdir
from os import getcwd
from sys import path as sysPath
from sys import argv

from logging import Logger
from logging import getLogger

import logging.config

from json import load as jsonLoad

from org.pyut.PyutUtils import PyutUtils
from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.ui.PyutApp import PyutApp

from org.pyut.enums.ResourceTextType import ResourceTextType

from org.pyut.general.Lang import Lang
from org.pyut.general.PyutVersion import PyutVersion


class Pyut:

    JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"
    MADE_UP_PRETTY_MAIN_NAME:     str = "Pyut"

    def __init__(self):
        self._setupSystemLogging()
        self.logger: Logger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()
        Lang.importLanguage()

        self._exePath:  str = self._getExePath()
        self._userPath: str = getcwd()      # where the user launched pyut from
        PyutUtils.setBasePath(self._exePath)

        self._cmdLineArgsHandled: bool = False
        """
        If `True` then we handled some command line arguments that do not require the
        full startup of Pyut.  Examples of this are `--help` or `--version`.
        TODO:  Perhaps rename this to `_startupUI` or `_fullStartup` or `_startUI`
        """
        self.handleCommandLineArguments()

    def getUserPath(self) -> str:
        return self._userPath

    def setUserPath(self, theNewValue: str):
        self._userPath = theNewValue
        prefs: PyutPreferences = PyutPreferences()
        prefs[PyutPreferences.STARTUP_DIRECTORY] = theNewValue

    def getCmdLineArgsHandled(self) -> bool:
        return self._cmdLineArgsHandled

    def setCmdLinesArgsHandled(self, theNewValue: bool):
        self._cmdLineArgsHandled = theNewValue

    userPath           = property(getUserPath, setUserPath)
    cmdLineArgsHandled = property(getCmdLineArgsHandled, setCmdLinesArgsHandled)

    def _setupSystemLogging(self):

        configFilePath: str = PyutUtils.retrieveResourcePath(Pyut.JSON_LOGGING_CONFIG_FILENAME)

        with open(configFilePath, 'r') as loggingConfigurationFile:
            configurationDictionary = jsonLoad(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads   = False

    def startApp(self):
        self._setOurSysPath()
        self._updateOurDirectoryPreferences()
        self._displayIntro()
        app: PyutApp = PyutApp(redirect=False)
        app.MainLoop()

    def _getExePath(self) -> str:
        """
        Return the absolute path currently used
        """
        absPath = sysPath[0]
        return absPath

    def _setOurSysPath(self):
        try:
            sysPath.append(self._exePath)
            chdir(self._exePath)
        except OSError as msg:
            self.logger.error(f"Error while setting path: {msg}")

    def _updateOurDirectoryPreferences(self):
        """
        Define last open directory ?
            - default is current directory
            - last opened directory for developers (pyut/src present)
        """
        prefs: PyutPreferences = PyutPreferences()    # Prefs handler
        prefs[PyutPreferences.ORG_DIRECTORY] = getcwd()
        if (self._userPath.find('pyut/src') == -1) and (self._userPath.find('pyut2/src') == -1):

            self.logger.debug(f'self._userPath: {self._userPath}')
            prefs[PyutPreferences.LAST_DIRECTORY] = self._userPath
            self.logger.debug(f'prefs: {prefs}')

    def _displayIntro(self):

        introText: str = PyutUtils.retrieveResourceText(ResourceTextType.INTRODUCTION_TEXT_TYPE)
        print(introText)
        self.displayVersionInformation()

    def displayVersionInformation(self):
        import wx
        import sys
        import platform

        print("Versions: ")
        print(f"PyUt:     {PyutVersion.getPyUtVersion()}")
        print(f'Platform: {platform.platform()}')
        print(f'    System:       {platform.system()}')
        print(f'    Version:      {platform.version()}')
        print(f'    Release:      {platform.release()}')

        print(f'WxPython: {wx.__version__}')
        print(f'Python:   {sys.version.split(" ")[0]}')

    def handleCommandLineArguments(self):
        """
        Handle command line arguments, display help, ...

        @return True if arguments were found and handled (means no startup)
        """

        if len(argv) < 2:
            self.cmdLineArgsHandled = False
            return
        # Treat command line arguments
        if argv[1] == "--version":
            self.displayVersionInformation()
            self.cmdLineArgsHandled = True
            return
        elif argv[1] == "--help":
            print(f"PyUt, version {PyutVersion.getPyUtVersion()}")
            helpText: str = PyutUtils.retrieveResourceText(ResourceTextType.HELP_TEXT_TYPE)
            print(helpText)
            self.cmdLineArgsHandled = True
            return

        for param in argv[1:]:
            if param[:18] == "--start_directory=":
                print(f'Starting with default directory: {param[18:]}')
                self.userPath = param[18:]
        self.cmdLineArgsHandled = False


if __name__ == "__main__":

    print(f"Starting {Pyut.MADE_UP_PRETTY_MAIN_NAME}")

    pyut2: Pyut = Pyut()

    # Launch pyut
    if pyut2.cmdLineArgsHandled is False:
        pyut2.startApp()
