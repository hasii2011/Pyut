#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.3 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

from PyutLinkedObject import *

class PyutActor(PyutLinkedObject):
    """
    Represents a Use Case actor (data layer).
    An actor, in data layer, only has a name. Linking is resolved by
    parent class `PyutLinkedObject` that defines everything needed for
    links connections.

    :version: $Revision: 1.3 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """
    def __init__(self, name = ""):
        """
        Constructor.
        @param String name : The name of the actor

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        PyutLinkedObject.__init__(self, name)

