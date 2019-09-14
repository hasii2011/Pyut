#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.5 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-1-8"

#from wxPython.wx import *
from pyutUtils   import *
from PyutUseCase import *
import wx

[
    TXT_USECASE
] = assignID(1)

class DlgEditUseCase(wx.Dialog):
    """
    Defines a multiline text control dialog for use case editing.
    This dialog is used to ask the user to enter the text that will be
    displayed into an UML Use case.

    Sample of use::
        dlg = DlgEditUseCase(self._uml, -1, pyutUseCase)
        dlg.Destroy()

    :version: $Revision: 1.5 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    #>------------------------------------------------------------------------

    def __init__(self, parent, ID, pyutUseCase):
        """
        Constructor.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        wx.Dialog.__init__(self, parent, ID, _("Use Case Edit"),
                          style = wx.RESIZE_BORDER|wx.CAPTION)

        # Associated PyutUseCase
        self._pyutUseCase = pyutUseCase

        self.SetAutoLayout(True)
        #~ self.SetSize(wx.Size(416, 200))

        #init members vars
        self._text = self._pyutUseCase.getName()
        self._returnAction = -1   #describe how the user exited the dialog box

        #labels
        label = wx.StaticText(self, -1, _("Use case text"))

        #text
        self._txtCtrl = wx.TextCtrl(self, TXT_USECASE, self._text,
                                   size = (400, 180),
                                   style = wx.TE_MULTILINE)

        # Set the focus
        self._txtCtrl.SetFocus()

        #text events
        self.Bind(wx.EVT_TEXT, self._onTxtChange, id=TXT_USECASE)

        #Ok/Cancel
        btnOk = wx.Button(self, wx.OK, _("&Ok"))
        btnOk.SetDefault()
        btnCancel = wx.Button(self, wx.CANCEL, _("&Cancel"))

        #button events
        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)

        # Sizer for buttons
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrButtons.Add(btnOk, 0, wx.RIGHT, 10)
        szrButtons.Add(btnCancel, 0, wx.ALL)

        # Sizer for all components
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrMain.Add(label, 0, wx.BOTTOM, 5)
        szrMain.Add(self._txtCtrl, 1, wx.EXPAND|wx.BOTTOM, 10)
        szrMain.Add(szrButtons, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM)
        # Border
        szrBorder = wx.BoxSizer(wx.VERTICAL)
        szrBorder.Add(szrMain, 1, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(szrBorder)
        szrBorder.Fit(self)

        self.Centre()
        self.ShowModal()

    #>------------------------------------------------------------------------

    def _onTxtChange(self, event):
        """
        Event occuring when TXT_NOTE change.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._text = event.GetString()

    #>------------------------------------------------------------------------

    def _onCmdOk(self, event):
        """
        Handle click on "Ok" button.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        self._pyutUseCase.setName(self._text)
        self._returnAction=wx.OK
        self.Close()


    #>------------------------------------------------------------------------

    def _onCmdCancel(self, event):
        """
        Handle click on "Cancel" button.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._returnAction=wx.CANCEL
        self.Close()

    #>------------------------------------------------------------------------

    def getReturnAction(self):
        """
        Return an info on how the user exited the dialog box

        @return : wx.Ok = click on Ok button; wx.Cancel = click on Cancel button
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._returnAction

