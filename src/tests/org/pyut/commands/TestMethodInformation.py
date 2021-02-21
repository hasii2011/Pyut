
from logging import Logger
from logging import getLogger
from typing import List
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename

from org.pyut.model.PyutClassCommon import PyutClassCommon
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutModifier import PyutModifier
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum
from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.commands.MethodInformation import MethodInformation


class TestMethodInformation(TestBase):
    """
    """
    clsLogger:        Logger = None
    methodParamNumber: int = 1
    methodTypeNumber: int = 1

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestMethodInformation.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestMethodInformation.clsLogger

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'MethodInformation.txt')
        saveFile = open(fqFileName)
        self._serializedMethodInformation: str = saveFile.read()
        saveFile.close()

    def tearDown(self):
        pass

    def testSerialize(self):

        pyutClassCommon: PyutClassCommon = PyutClassCommon()
        pyutClassCommon.description = 'I am a test class'

        floatMethod: PyutMethod = self._createTestMethod('floatMethod', PyutVisibilityEnum.PRIVATE,   PyutType('float'))
        finalMethod: PyutMethod = self._createTestMethod('finalMethod', PyutVisibilityEnum.PROTECTED, PyutType('int'))

        pyutModifier: PyutModifier = PyutModifier(modifierTypeName='final')
        finalMethod.addModifier(newModifier=pyutModifier)

        pyutClassCommon.methods = [floatMethod, finalMethod]
        serializedMethods: str = MethodInformation.serialize(pyutClassCommon)

        self.assertNotEqual(0, len(serializedMethods), 'Something should serialize')

        self.logger.warning(f'{serializedMethods=}')

    def testDeserialize(self):

        pyutClassCommon: PyutClassCommon = PyutClassCommon()

        pyutClassCommon = MethodInformation.deserialize(serializedData=self._serializedMethodInformation, pyutObject=pyutClassCommon)

        self.assertEqual('I am a test class', pyutClassCommon.description, 'Who changed the test description')

        pyutMethods: List[PyutMethod] = pyutClassCommon.methods
        self.assertEqual(2, len(pyutMethods), 'I should only deserialize this many')

        for pyutMethod in pyutMethods:
            pyutMethod: PyutMethod = cast(PyutMethod, pyutMethod)
            self.logger.warning(f'{pyutMethod}')
            self.assertIsNotNone(pyutMethod.name, 'Where is my method name')
            self.assertIsNotNone(pyutMethod.visibility, 'Where is the method visibility')
            self.assertIsNotNone(pyutMethod.returnType, 'Where is my return type')

    def _createTestMethod(self, name: str, visibility: PyutVisibilityEnum, returnType: PyutType) -> PyutMethod:

        pyutMethod: PyutMethod = PyutMethod()

        pyutMethod.name       = name
        pyutMethod.visibility = visibility
        pyutMethod.returnType = returnType

        pyutParam: PyutParam = PyutParam(name=f'param{self.methodParamNumber}',
                                         theParameterType=PyutType(f'Type{self.methodTypeNumber}'),
                                         defaultValue='')

        pyutMethod.addParam(pyutParam)

        TestMethodInformation.methodParamNumber += 1
        TestMethodInformation.methodTypeNumber  += 1

        return pyutMethod


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestMethodInformation))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
