
from typing import List
from typing import cast
from typing import Dict

from logging import Logger
from logging import getLogger

from json import dumps as jsonDumps

from os import sep as osSep

from wx import CENTRE
from wx import ICON_ERROR

from wx import ICON_INFORMATION
from wx import OK

from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import MessageBox
from wx import Yield as wxYield

from org.pyut.model.PyutClass import PyutClass

from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin
from org.pyut.plugins.base.PyutPlugin import PyutPlugin

from org.pyut.plugins.iopythonsupport.DlgAskWhichClassesToReverse import DlgAskWhichClassesToReverse
from org.pyut.plugins.iopythonsupport.PyutToPython import PyutToPython
from org.pyut.plugins.iopythonsupport.ReverseEngineerPython2 import ReverseEngineerPython2

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

# noinspection PyProtectedMember
from org.pyut.general.Globals import _


class IoPython(PyutIoPlugin):

    """
    Python code generation/reverse engineering

    """
    def __init__(self, oglObjects, umlFrame):

        super().__init__(oglObjects=oglObjects, umlFrame=umlFrame)

        self.logger: Logger = getLogger(__name__)

        # self._reverseEngineer: ReverseEngineerPython = ReverseEngineerPython()

        self._pyutToPython:    PyutToPython           = PyutToPython()

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        """
        return "Python code generation/reverse engineering"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        """
        return "C.Dutoit <dutoitc@hotmail.com> AND L.Burgbacher <lb@alawa.ch>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        """
        return "1.0"

    def getInputFormat(self) -> PyutPlugin.INPUT_FORMAT_TYPE:
        """
        Return a specification tuple.
            name of the input format
            extension of the input format
            textual description of the plugin input format

        Returns:
            Return a specification tuple.
        """
        return cast(PyutPlugin.INPUT_FORMAT_TYPE, ("Python File(s)", "py", "Syntactically correct Python File"))

    def getOutputFormat(self) -> PyutPlugin.OUTPUT_FORMAT_TYPE:
        """
        Return a specification tuple.
            name of the output format
            extension of the output format
            textual description of the plugin output format

        Returns:
            Return a specification tuple.
        """
        return cast(PyutPlugin.OUTPUT_FORMAT_TYPE, ("Python File(s)", "py", "Syntactically correct Python File"))

    def setExportOptions(self) -> bool:
        return True

    def write(self, oglObjects: List[OglClass]):
        """

        Args:
            oglObjects:
        """
        directory = self._askForDirectoryExport()
        if directory == "":
            return False

        self.logger.info("IoPython Saving...")

        classes: Dict[str, List[str]] = {}
        generatedClassDoc: List[str] = self._pyutToPython.generateTopCode()

        # Create classes code for each object
        for oglObject in [oglObject for oglObject in oglObjects if isinstance(oglObject, OglClass)]:

            oglClass:  OglClass  = cast(OglClass, oglObject)
            pyutClass: PyutClass = cast(PyutClass, oglClass.getPyutObject())

            generatedStanza:    str       = self._pyutToPython.generateClassStanza(pyutClass)
            generatedClassCode: List[str] = [generatedStanza]

            clsMethods: PyutToPython.MethodsCodeType = self._pyutToPython.generateMethodsCode(pyutClass)

            # Add __init__ Method
            if PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR in clsMethods:
                methodCode = clsMethods[PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR]
                generatedClassCode += methodCode
                del clsMethods[PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR]

            # Add others methods in order
            for pyutMethod in pyutClass.methods:
                methodName: str = pyutMethod.getName()
                if methodName != PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR:
                    try:
                        otherMethodCode: List[str] = clsMethods[methodName]
                        generatedClassCode += otherMethodCode
                    except (ValueError, Exception, KeyError) as e:
                        self.logger.warning(f'{e}')

            generatedClassCode.append("\n\n")
            # Save into classes dictionary
            classes[pyutClass.getName()] = generatedClassCode

        # Write class code to a file
        for (className, classCode) in list(classes.items()):
            self._writeClassToFile(classCode, className, directory, generatedClassDoc)

        self.logger.info("IoPython done !")

        MessageBox(_("Done !"), _("Python code generation"), style=CENTRE | OK | ICON_INFORMATION)

    def _writeClassToFile(self, classCode, className, directory, generatedClassDoc):

        filename: str = f'{directory}{osSep}{str(className)}.py'

        file = open(filename, "w")
        file.writelines(generatedClassDoc)
        file.writelines(classCode)

        file.close()

    def read(self, oglObjects, umlFrame: UmlClassDiagramsFrame):
        """
        Reverse engineering

        Args:
            oglObjects:     list of imported objects
            umlFrame:       Pyut's UmlFrame
        """
        # Ask the user which destination file he wants
        # directory=self._askForDirectoryImport()
        # if directory=="":
        #    return False
        (lstFiles, directory) = self._askForFileImport(True)
        if len(lstFiles) == 0:
            return False

        BeginBusyCursor()
        wxYield()
        try:
            reverseEngineer: ReverseEngineerPython2 = ReverseEngineerPython2()
            reverseEngineer.reversePython(umlFrame=umlFrame, directoryName=directory, files=lstFiles)
            # TODO: Don't expose the internals
            self.logger.debug(f'classNames: {jsonDumps(reverseEngineer.visitor.classMethods, indent=4)}')
            self.logger.debug(f'methods: {jsonDumps(reverseEngineer.visitor.parameters, indent=4)}')
        except (ValueError, Exception) as e:
            MessageBox(f'{e}', 'Error', OK | ICON_ERROR)
        EndBusyCursor()

    def askWhichClassesToReverse(self, lstClasses):
        """
        Starts the dialog that asks which classes must be reversed

        Args:
            lstClasses: list of classes potentially reversible

        Returns:
            A list of classes to reverse-engineer
        """
        dlg = DlgAskWhichClassesToReverse(lstClasses)
        lstClassesChosen = dlg.getChosenClasses()
        dlg.Destroy()

        return lstClassesChosen
