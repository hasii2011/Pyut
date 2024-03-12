from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize
from pyut.preferences.PyutPreferencesV2 import PyutPreferencesV2


class TestPyutPreferencesV2(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 11 March 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

        self._preferences: PyutPreferencesV2 = PyutPreferencesV2()

    def tearDown(self):
        super().tearDown()

    def testSingletonBehavior(self):

        preferences: PyutPreferencesV2 = PyutPreferencesV2()

        original:     str = f'{hex(id(self._preferences))}'
        doppleGanger: str = f'{hex(id(preferences))}'

        self.assertEqual(original, doppleGanger, 'IDs should be valid')

    def testBooleanValuesPresent(self):

        saveShowTipsOnStartup:   bool = self._preferences.showTipsOnStartup
        loadLastOpenedProject:   bool = self._preferences.loadLastOpenedProject
        displayProjectExtension: bool = self._preferences.displayProjectExtension
        autoResizedOnEdit:       bool = self._preferences.autoResizeShapesOnEdit
        fullScreen:              bool = self._preferences.fullScreen
        centerAppOnStartup:      bool = self._preferences.centerAppOnStartup

        self._preferences.showTipsOnStartup       = False
        self._preferences.loadLastOpenedProject   = False
        self._preferences.displayProjectExtension = False
        self._preferences.autoResizeShapesOnEdit   = False
        self._preferences.fullScreen              = True
        self._preferences.centerAppOnStartup      = True

        try:
            self.assertFalse(self._preferences.showTipsOnStartup, '')
            self.assertFalse(self._preferences.loadLastOpenedProject, '')
            self.assertFalse(self._preferences.displayProjectExtension, '')
            self.assertFalse(self._preferences.autoResizeShapesOnEdit, '')
            self.assertTrue(self._preferences.fullScreen, '')
            self.assertTrue(self._preferences.centerAppOnStartup)
        except AssertionError as e:
            raise e
        finally:
            # restore first in case of failure
            self._preferences.showTipsOnStartup       = saveShowTipsOnStartup
            self._preferences.loadLastOpenedProject   = loadLastOpenedProject
            self._preferences.displayProjectExtension = displayProjectExtension
            self._preferences.autoResizeShapesOnEdit   = autoResizedOnEdit
            self._preferences.fullScreen              = fullScreen
            self._preferences.centerAppOnStartup      = centerAppOnStartup

    def testToolBarIconSize(self):
        saveValue:     ToolBarIconSize = self._preferences.toolBarIconSize
        expectedValue: ToolBarIconSize = ToolBarIconSize.SIZE_16

        self._preferences.toolBarIconSize = expectedValue

        actualValue: ToolBarIconSize = self._preferences.toolBarIconSize

        self._preferences.toolBarIconSize = saveValue

        self.assertEqual(expectedValue, actualValue, 'What the heck !!')

    def testDebugErrorViews(self):

        saveValue: bool = self._preferences.debugErrorViews

        self._preferences.debugErrorViews = True

        expectedValue: bool = True
        actualValue:   bool = self._preferences.debugErrorViews

        self._preferences.debugErrorViews = saveValue   # restore possible blowup

        self.assertEqual(expectedValue, actualValue, 'Looks like boolean value not set correctly')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPyutPreferencesV2))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
