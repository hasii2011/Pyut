
from enum import Enum

from wx import CommandEvent
from wx import PyEventBinder

from wx.lib.newevent import NewEvent

#
# Constructor returns a tuple; First is the event,  The second is the binder
#
NewProjectEvent,              EVENT_NEW_PROJECT               = NewEvent()
NewNamedProjectEvent,         EVENT_NEW_NAMED_PROJECT         = NewEvent()
NewDiagramEvent,              EVENT_NEW_DIAGRAM               = NewEvent()
NewProjectDiagramEvent,       EVENT_NEW_PROJECT_DIAGRAM       = NewEvent()
DeleteDiagramEvent,           EVENT_DELETE_DIAGRAM            = NewEvent()
OpenProjectEvent,             EVENT_OPEN_PROJECT              = NewEvent()
InsertProjectEvent,           EVENT_INSERT_PROJECT            = NewEvent()
SaveProjectEvent,             EVENT_SAVE_PROJECT              = NewEvent()
SaveProjectAsEvent,           EVENT_SAVE_PROJECT_AS           = NewEvent()
CloseProjectEvent,            EVENT_CLOSE_PROJECT             = NewEvent()
UpdateTreeItemNameEvent,      EVENT_UPDATE_TREE_ITEM_NAME     = NewEvent()
UpdateApplicationTitleEvent,  EVENT_UPDATE_APPLICATION_TITLE  = NewEvent()
UpdateApplicationStatusEvent, EVENT_UPDATE_APPLICATION_STATUS = NewEvent()

UMLDiagramModifiedEvent,   EVENT_UML_DIAGRAM_MODIFIED   = NewEvent()
UpdateRecentProjectsEvent, EVENT_UPDATE_RECENT_PROJECTS = NewEvent()

SelectAllShapesEvent,   EVENT_SELECT_ALL_SHAPES   = NewEvent()
DeSelectAllShapesEvent, EVENT_DESELECT_ALL_SHAPES = NewEvent()
AddShapeEvent,          EVENT_ADD_SHAPE           = NewEvent()

CopyShapesEvent,      EVENT_COPY_SHAPES       = NewEvent()
PasteShapesEvent,     EVENT_PASTE_SHAPES      = NewEvent()
CutShapesEvent,       EVENT_CUT_SHAPES        = NewEvent()
UndoEvent,            EVENT_UNDO              = NewEvent()
RedoEvent,            EVENT_REDO              = NewEvent()
CutShapeEvent,        EVENT_CUT_SHAPE         = NewEvent()          # TODO:  I do not think this is used anymore
EditClassEvent,       EVENT_EDIT_CLASS,       = NewEvent()
EditNoteEvent,        EVENT_EDIT_NOTE         = NewEvent()
EditTextEvent,        EVENT_EDIT_TEXT         = NewEvent()
EditActorEvent,       EVENT_EDIT_ACTOR        = NewEvent()
EditUseCaseEvent,     EVENT_EDIT_USE_CASE     = NewEvent()
EditInterfaceEvent,   EVENT_EDIT_INTERFACE    = NewEvent()

AddPyutDiagramEvent, EVENT_ADD_PYUT_DIAGRAM = NewEvent()
AddOglDiagramEvent,  EVENT_ADD_OGL_DIAGRAM  = NewEvent()

SelectToolEvent,               EVENT_SELECT_TOOL                = NewEvent()
SetToolActionEvent,            EVENT_SET_TOOL_ACTION            = NewEvent()
MiniProjectInformationEvent,   EVENT_MINI_PROJECT_INFORMATION   = NewEvent()
ActiveUmlFrameEvent,           EVENT_ACTIVE_UML_FRAME           = NewEvent()
ActiveProjectInformationEvent, EVENT_ACTIVE_PROJECT_INFORMATION = NewEvent()

# The following specifically for the plugin adapter
FrameInformationEvent,         EVENT_FRAME_INFORMATION    = NewEvent()
FrameSizeEvent,                EVENT_FRAME_SIZE           = NewEvent()
SelectedOglObjectsEvent,       EVENT_SELECTED_OGL_OBJECTS = NewEvent()
RefreshFrameEvent,             EVENT_REFRESH_FRAME        = NewEvent()

UpdateEditMenuEvent,    EVENT_UPDATE_EDIT_MENU    = NewEvent()
AssociateEditMenuEvent, EVENT_ASSOCIATE_EDIT_MENU = NewEvent()

ClassNameChangedEvent,       EVENT_CLASS_NAME_CHANGED      = NewEvent()
RequestCurrentProjectEvent,  EVENT_REQUEST_CURRENT_PROJECT = NewEvent()


class EventType(str, Enum):
    """
    UpdateApplicationTitleEvent
        Updates the application title
        parameters:
            newFilename: str
            currentFrameZoomFactor : float
            projectModified : bool

    UpdateApplicationStatusEvent
        Updates the application status bar
        parameters:
            applicationStatusMsg:  The new message to display

    RemoveDocumentEvent
        Removes the currently selected document

    NewNamedProjectEvent
        Creates a new project in the project manager and the appropriate UI elements
        parameter:
            projectFilename:  The fully qualified file name
            callback:         The callback to return the IPyutProject object

    InsertProjectEvent
        parameter:
            projectFilename:  The fully qualified file name

    NewDiagramEvent
        Creates a new diagram on the current project
        parameter:
            diagramType:   A value from the DiagramType enumeration

    NewProjectDiagramEvent
        Creates a new diagram for the given project;  Includes the UI and model artifacts
        parameters:
            NewProjectDiagramInformation

    CutShapeEvent
        Cuts only the specified shape
        parameter:
            shapeToCut

    EditClassEvent
        Invokes the Edit Class dialog
        parameter:
            pyutClass

    EditNoteEvent
        Invokes the Edit Note dialog
        parameter:
            pyutNote

    EditTextEvent
        Invokes the Edit Text dialog
        parameter:
            pyutText

    EditActorEvent
        Invokes a general Edit dialog for the name
        parameter:
            pyutActor

    AddShapeEvent
        Adds the specified shape on the UI
        parameter:
            oglObject      The Ogl document to place on the UML UmlFrame

    SelectToolEvent
        Use to select tools in the toolbar as a visual add to the end-user/developer
        parameter:
            toolId - The tool id;  The value generated by wx.NewIdRef

    SetToolActionEvent
        Used to set the appropriate tool action for the ActionHandler.
        parameter
            action The action identifier from Actions

    MiniProjectInformationEvent:
        Used to get some project data;
        parameters
            callback - Callback that is invoked with a parameter of type MiniProjectInformation

    ActiveUmlFrameEvent
        Used to retrieve the currently active frame
        parameters:
            callback - Callback this is invoked with a parameter of type UmlDiagramsFrame

    ActiveProjectInformationEvent
        Used to get information on the active project so that the UML Object edit dialogs
        can do their job
        parameters:
            callback - Callback that is invoked with a parameter of type ActiveProjectInformation

    FrameInformationEvent
        Use by the plugin adaptor to provide low level to plugins that need item
        parameters:
            callback - Callback this is invoked with a parameter of type FrameInformation

    UpdateEditMenuEvent
        Used to update the Edit menu Undo/redo menu items.  This involves using the
        command processor associated with each Uml Frame
        parameters:
            commandProcessor - The command processor associated with the currently visible UML Frame

    AssociateEditMenuEvent:
        Used on the initial creation of a UML frame to associate it with the Edit Menu
        parameters:
            commandProcessor - The command processor associated with the currently visible UML Frame

    ClassNameChangedEvent:
        Used if a dialog or some code changes a class name.  We have to update the model and the
        model
        parameters:
            oldClassName - the old class name
            newClassName - the new class name

    Events with no parameters get stuffed into the enumeration as instances, so they can be used
    event engine simple send method;  To simplify enumeration creation I create instances for all
    event types
    """

    commandEvent:  CommandEvent
    pyEventBinder: PyEventBinder

    def __new__(cls, title: str, commandEvent: CommandEvent, binder: PyEventBinder) -> 'EventType':
        obj = str.__new__(cls, title)
        obj._value_ = title

        obj.commandEvent  = commandEvent
        obj.pyEventBinder = binder
        return obj

    NewProject              = ('NewProject',              NewProjectEvent(),              EVENT_NEW_PROJECT)
    NewNamedProject         = ('NewNamedProject',         NewNamedProjectEvent,           EVENT_NEW_NAMED_PROJECT)
    NewDiagram              = ('NewDiagram',              NewDiagramEvent(),              EVENT_NEW_DIAGRAM)
    NewProjectDiagram       = ('NewProjectDiagram',       NewProjectDiagramEvent(),       EVENT_NEW_PROJECT_DIAGRAM)
    DeleteDiagram           = ('DeleteDiagram',           DeleteDiagramEvent(),           EVENT_DELETE_DIAGRAM)
    OpenProject             = ('OpenProject',             OpenProjectEvent(),             EVENT_OPEN_PROJECT)
    InsertProject           = ('InsertProject',           InsertProjectEvent(),           EVENT_INSERT_PROJECT)
    SaveProject             = ('SaveProject',             SaveProjectEvent(),             EVENT_SAVE_PROJECT)
    SaveProjectAs           = ('SaveProjectAs',           SaveProjectAsEvent(),           EVENT_SAVE_PROJECT_AS)
    CloseProject            = ('CloseProject',            CloseProjectEvent(),            EVENT_CLOSE_PROJECT)
    UpdateTreeItemName      = ('UpdateTreeItemName',      UpdateTreeItemNameEvent(),      EVENT_UPDATE_TREE_ITEM_NAME)
    UpdateApplicationTitle  = ('UpdateApplicationTitle',  UpdateApplicationTitleEvent(),  EVENT_UPDATE_APPLICATION_TITLE)
    UpdateApplicationStatus = ('UpdateApplicationStatus', UpdateApplicationStatusEvent(), EVENT_UPDATE_APPLICATION_STATUS)

    UpdateRecentProjects    = ('UpdateRecentProjects', UpdateRecentProjectsEvent(), EVENT_UPDATE_RECENT_PROJECTS)

    UMLDiagramModified      = ('UMLDiagramModified',   UMLDiagramModifiedEvent(),   EVENT_UML_DIAGRAM_MODIFIED)

    SelectAllShapes   = ('SelectAllShapes',        SelectAllShapesEvent(),   EVENT_SELECT_ALL_SHAPES)
    DeSelectAllShapes = ('DeSelectAllShapesEvent', DeSelectAllShapesEvent(), EVENT_DESELECT_ALL_SHAPES)
    AddShape          = ('AddShapeEvent',          AddShapeEvent(),          EVENT_ADD_SHAPE)
    CopyShapes        = ('CopyShapes',             CopyShapesEvent(),        EVENT_COPY_SHAPES)
    PasteShapes       = ('PasteShapes',            PasteShapesEvent(),       EVENT_PASTE_SHAPES)
    CutShapes         = ('CutShapes',              CutShapesEvent(),         EVENT_CUT_SHAPES)
    Undo              = ('Undo',                   UndoEvent(),              EVENT_UNDO)
    Redo              = ('Redo',                   RedoEvent(),              EVENT_REDO)
    CutShape          = ('CutShape',               CutShapeEvent(),          EVENT_CUT_SHAPE)

    AddPyutDiagram = ('AddPyutDiagram', AddPyutDiagramEvent(), EVENT_ADD_PYUT_DIAGRAM)
    AddOglDiagram  = ('AddOglDiagram',  AddOglDiagramEvent(),  EVENT_ADD_OGL_DIAGRAM)

    SelectTool               = ('SelectTool',               SelectToolEvent(),               EVENT_SELECT_TOOL)
    SetToolAction            = ('SetToolAction',            SetToolActionEvent(),            EVENT_SET_TOOL_ACTION)
    MiniProjectInformation   = ('MiniProjectInformation',   MiniProjectInformationEvent(),   EVENT_MINI_PROJECT_INFORMATION)
    ActiveUmlFrame           = ('ActiveUmlFrame',           ActiveUmlFrameEvent(),           EVENT_ACTIVE_UML_FRAME)
    ActiveProjectInformation = ('ActiveProjectInformation', ActiveProjectInformationEvent(), EVENT_ACTIVE_PROJECT_INFORMATION)
    EditClass                = ('EditClass',                EditClassEvent(),                EVENT_EDIT_CLASS)
    EditNote                 = ('EditNote',                 EditNoteEvent(),                 EVENT_EDIT_NOTE)
    EditText                 = ('EditText',                 EditTextEvent(),                 EVENT_EDIT_TEXT)
    EditActor                = ('EditActor',                EditActorEvent(),                EVENT_EDIT_ACTOR)
    EditUseCase              = ('EditUseCase',              EditUseCaseEvent(),              EVENT_EDIT_USE_CASE)
    EditInterface            = ('EditInterface',            EditInterfaceEvent(),            EVENT_EDIT_INTERFACE)

    FrameInformation         = ('FrameInformation',   FrameInformationEvent(),   EVENT_FRAME_INFORMATION)
    FrameSize                = ('FrameSize',          FrameSizeEvent(),          EVENT_FRAME_SIZE)
    SelectedOglObjects       = ('SelectedOglObjects', SelectedOglObjectsEvent(), EVENT_SELECTED_OGL_OBJECTS)
    RefreshFrame             = ('RefreshFrame',       RefreshFrameEvent(),       EVENT_REFRESH_FRAME)

    UpdateEditMenu    = ('UpdateEditMenu',    UpdateEditMenuEvent(),    EVENT_UPDATE_EDIT_MENU)
    AssociateEditMenu = ('AssociateEditMenu', AssociateEditMenuEvent(), EVENT_ASSOCIATE_EDIT_MENU)

    ClassNameChanged      = ('ClassNameChanged',      ClassNameChangedEvent(),      EVENT_CLASS_NAME_CHANGED)
    RequestCurrentProject = ('RequestCurrentProject', RequestCurrentProjectEvent(), EVENT_REQUEST_CURRENT_PROJECT)
