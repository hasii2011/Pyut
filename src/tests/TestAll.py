
from typing import List

import logging
from logging import Logger
from logging import getLogger
from logging import config as loggingConfig

from sys import path as sysPath
from sys import argv as sysArgv

from json import load as jsonLoad

from importlib import import_module

from glob import glob

from unittest import TestResult
from unittest import TextTestRunner
from unittest.suite import TestSuite

from HtmlTestRunner import HTMLTestRunner


class TestAll:
    """
    The class that can run our unit tests in various formats
    """
    NOT_TESTS: List[str] = ['TestAll', 'TestMiniOgl', 'TestBase', 'TestTemplate', 'TestIoFile', 'TestUmlFrame']

    def __init__(self):

        self._setupSystemLogging()

        self.logger: Logger = getLogger(__name__)

        self._testSuite: TestSuite = self._getTestSuite()

    def runTextTestRunner(self) -> int:

        status: TestResult = TextTestRunner().run(self._testSuite)
        self.logger.info(f'Test Suite Status: {status}')
        if len(status.failures) != 0:
            return 1
        else:
            return 0

    def runHtmlTestRunner(self) -> int:

        runner = HTMLTestRunner(report_name='PyutTestResults', combine_reports=True, add_timestamp=True)
        status = runner.run(self._testSuite)
        if len(status.failures) != 0:
            return 1
        else:
            return 0

    def _setupSystemLogging(self):
        """
        Read the unit test logging configuration file
        """
        from tests.TestBase import JSON_LOGGING_CONFIG_FILENAME

        with open(JSON_LOGGING_CONFIG_FILENAME, 'r') as loggingConfigurationFile:
            configurationDictionary = jsonLoad(loggingConfigurationFile)

            loggingConfig.dictConfig(configurationDictionary)
            logging.logProcesses = False
            logging.logThreads   = False

    def _getTestSuite(self) -> TestSuite:
        """

        Returns:
            A suite of all tests in the unit test directory
        """
        modules: List[str] = self.__getTestableModuleNames()
        fSuite: TestSuite = TestSuite()
        for module in modules:
            try:
                m = import_module(module)
                fSuite.addTest(m.suite())
            except (ValueError, Exception) as e:
                self.logger.error(f'Module import problem with: {module}:  {e}')
        return fSuite

    def __getTestableModuleNames(self) -> List[str]:
        """
        Removes modules that are not unit tests

        Returns:
            A list of module names that we can find in this package
        """

        fModules = glob("Test*.py")
        # remove .py extension
        modules = list(map(lambda x: x[:-3], fModules))
        for doNotTest in TestAll.NOT_TESTS:
            modules.remove(doNotTest)

        return modules


def main():

    if ".." not in sysPath:
        sysPath.append("..")  # access to the classes to test

    testAll: TestAll = TestAll()
    if len(sysArgv) < 2:
        status: int = testAll.runTextTestRunner()
    else:
        status = 0
        for param in sysArgv[1:]:
            if param[:22] == "--produce-html-results":
                print(f'Running HTML Tests')
                status: int = testAll.runHtmlTestRunner()

    return status


if __name__ == "__main__":
    main()
