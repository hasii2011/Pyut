
from hasiicommon.ui.UnitTestBaseW import UnitTestBaseW


class TestBase(UnitTestBaseW):

    RESOURCES_PACKAGE_NAME:                   str = 'tests.resources'
    RESOURCES_TEST_CLASSES_PACKAGE_NAME:      str = 'tests.resources.testclass'
    RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME: str = 'tests.resources.testclass.ozzee'
    RESOURCES_TEST_DATA_PACKAGE_NAME:         str = 'tests.resources.testdata'
    RESOURCES_TEST_IMAGES_PACKAGE_NAME:       str = 'tests.resources.testimages'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()