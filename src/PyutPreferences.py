#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.5 $"
__author__ = "EI6, eivd, Group Dutoit-Roux"
__date__ = "2002-4-17"
# Class maintainer : C.Dutoit - dutoitc@hotmail.com Please contact me if
#                    you got problems
from singleton import Singleton
from ConfigParser import *
import sys, os


# Set the Preferences filename
if sys.platform=="linux2" or sys.platform=="linux":
    PREFS_FILENAME = os.getenv("HOME") + "/.PyutPrefs.dat"
else:
    PREFS_FILENAME="PyutPrefs.dat"
DEFAULT_NB_LOF=5    # Number of last opened files, by default


class PyutPreferences(Singleton):
    """
    The goal of this class is to handle Pyut Preferences, to load them and save
    them from/to a file.
    To use it :
      - instanciate a PyutPreferences object : 
        myPP=PyutPreferences()
      - to get a pyut' preference :
        mypref=myPP["ma_preference"]
      - to set a pyut' preference :
        myPP["ma_preference"]=xxx

      - To change the number of last opened files, use :
        myPP.setNbLOF(x)
      - To get the number of last opened files, use :
        myPP.getNbLOF()
      - To get the list of Last Opened files, use :
        myPP.getLastOpenedFilesList()
      - To add a file to the Last Opened Files list, use :
        myPP.addNewLastOpenedFilesEntry(filename)

    The preferences are automatically loaded on the first instanciation of this
    class and are saved when a value is added or changed automatically, too.
    ---
    @since 1.0
    """
    def init(self):
        """
        Constructor

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._config = None
        self.__loadConfig()

    #>--------------------------------------------------------------------------

    def __getitem__(self, name):
        """
        Return the pyut preferences for the given item

        @param String name : Name of the item for which we return a value
        @return String : value of the pref, or None if inexistant
        @since 1.1.2.7
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if not self._config.has_section("Main"):
            return None

        try:
            return self._config.get("Main", name)
        except NoOptionError:
            return None

    #>--------------------------------------------------------------------------

    def __setitem__(self, name, value):
        """
        Return the pyut preferences for the given item

        @param String name : Name of the item WITHOUT SPACES
        @param String Value : Value for the given name
        @raises TypeError : if the name contains spaces
        @since 1.1.2.7
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Add 'Main' section ?
        if not self._config.has_section("Main"):
            self._config.add_section("Main")

        if " " in list(name):
            raise TypeError, "Name cannot contain a space"

        # Save
        self._config.set("Main", name, str(value))
        self.__saveConfig()

    #>--------------------------------------------------------------------------

    def __saveConfig(self):
        """
        Save datas to config file

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        f=open(PREFS_FILENAME, "w")
        self._config.write(f)
        f.close()

    #>--------------------------------------------------------------------------

    def __loadConfig(self):
        """
        Load datas from config file

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Make sure that the configuration file exist
        try:
            f = open(PREFS_FILENAME, "r")
            f.close()
        except:
            try:
                f = open(PREFS_FILENAME, "w")
                f.write("")
                f.close()
            except:
                print "Can't make %s for saving preferences !" % PREFS_FILENAME
                print "Pyut will not work normally from here..."
                print "Try to create a file named ", PREFS_FILENAME, " " + \
                      "in your home directory..."
                return


        # Read datas
        self._config=ConfigParser()
        self._config.read(PREFS_FILENAME)

        # Create a "LastOpenedFiles" structure ?
        if not self._config.has_section("LastOpenedFiles"):
            # Add section
            self._config=ConfigParser()
            self._config.add_section("LastOpenedFiles")

            # Set last opened files
            self._config.set("LastOpenedFiles", "NbEntries", 
                             str(DEFAULT_NB_LOF))
            for i in range(DEFAULT_NB_LOF):
                self._config.set("LastOpenedFiles", "File" + str(i+1), "")
            self.__saveConfig()

    #>--------------------------------------------------------------------------

    def getNbLOF(self):
        """
        Return the number of last opened files

        @return Number of last opened files
        @since 1.Config0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return int(self._config.get("LastOpenedFiles", "NbEntries"))

    #>--------------------------------------------------------------------------

    def setNbLOF(self, nbLOF):
        """
        Set the number of last opened files

        @param int nbLOF : Number or last opened files
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._config.set("LastOpenedFiles", "NbEntries", 
                         str(max(nbLOF, 0)))
        self.__saveConfig()

    #>--------------------------------------------------------------------------

    def getLastOpenedFilesList(self):
        """
        Return the list of files"

        @return list Last Opened files list
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        lstFiles=[]

        # Read datas
        for index in range(self.getNbLOF()):
            lstFiles.append(self._config.get("LastOpenedFiles", 
                                             "File" + str(index+1)))
        return lstFiles

    #>--------------------------------------------------------------------------

    def addNewLastOpenedFilesEntry(self, filename):
        """
        Add a file to the list of last opened files

        @param String filename : filename to be added
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Get list
        lstFiles=self.getLastOpenedFilesList()

        #Already in list ? => remove
        if filename in lstFiles:
            lstFiles.remove(filename)

        #Insert on top of the list
        lstFiles=[filename]+lstFiles

        #Save
        for i in range(DEFAULT_NB_LOF):
            self._config.set("LastOpenedFiles", "File" + str(i+1), lstFiles[i])
        self.__saveConfig()
