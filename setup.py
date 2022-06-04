"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['src/org/pyut/Pyut.py']
DATA_FILES = [('org/pyut/resources', ['src/org/pyut/resources/loggingConfiguration.json']),
              ('org/pyut/resources', ['src/org/pyut/resources/Kilroy-Pyut.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/Help.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/Kudos.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/tips.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/version.txt']),

              ('org/pyut/resources/img', ['src/org/pyut/resources/img/pyut.ico']),


              ]
OPTIONS = {}

setup(
    name='Pyut',
    version='6.7.0',
    app=APP,
    data_files=DATA_FILES,
    packages=['pyutmodel',
              'miniogl',
              'ogl', 'ogl.events', 'ogl.preferences', 'ogl.resources', 'ogl.resources.img', 'ogl.resources.img.textdetails', 'ogl.sd',
              'org',
              'org.pyut',
              'org.pyut.dialogs', 'org.pyut.dialogs.preferences', 'org.pyut.dialogs.preferences.valuecontainers',
              'org.pyut.dialogs.textdialogs',
              'org.pyut.dialogs.tips',
              'org.pyut.enums',
              'org.pyut.errorcontroller',
              'org.pyut.experimental',
              'org.pyut.general', 'org.pyut.general.datatypes', 'org.pyut.general.exceptions',
              'org.pyut.history', 'org.pyut.history.commands',
              'org.pyut.persistence', 'org.pyut.persistence.converters',
              'org.pyut.plugins',
              'org.pyut.plugins.base',
              'org.pyut.plugins.common',
              'org.pyut.plugins.dtd',
              'org.pyut.plugins.fastedit',
              'org.pyut.plugins.gml',
              'org.pyut.plugins.io',
              'org.pyut.plugins.io.javasupport',
              'org.pyut.plugins.io.nativeimagesupport',
              'org.pyut.plugins.io.pyumlsupport',
              'org.pyut.plugins.iopythonsupport', 'org.pyut.plugins.iopythonsupport.pyantlrparser',
              'org.pyut.plugins.orthogonal',
              'org.pyut.plugins.sugiyama',
              'org.pyut.plugins.tools',
              'org.pyut.plugins.xmi',
              'org.pyut.plugins.xsd',
              'org.pyut.preferences',
              'org.pyut.resources',
              'org.pyut.resources.img',
              'org.pyut.resources.img.methodparameters',
              'org.pyut.resources.img.splash',
              'org.pyut.resources.img.toolbar', 'org.pyut.resources.img.toolbar.embedded16', 'org.pyut.resources.img.toolbar.embedded32',
              'org.pyut.resources.locale',
              'org.pyut.ui', 'org.pyut.ui.frame', 'org.pyut.ui.tools', 'org.pyut.ui.widgets'
              ],
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},

    url='https://github.com/hasii2011/PyUt',
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='The Python UML Tool',
    options=dict(py2app=dict(
        plist=dict(
            CFBundleGetInfoString='Edits Pyut UML Files',
            CFBundleIdentifier='org.pyut',
            CFBundleDocumentTypes=[
                {'CFBundleTypeName': 'Pyut'},
                {'CFBundleTypeRole': 'Editor'},
                {'CFBundleTypeExtensions':  ['put', 'xml']}
            ],
            LSMinimumSystemVersion='12',
            LSEnvironment=dict(
                APP_MODE='True',
                PYTHONOPTIMIZE='1',
            ),
        )
    ),
    ),
    setup_requires=['py2app'],
    install_requires=['antlr4-python3-runtime',
                      'orthogonal',
                      'pygmlparser',
                      'pyumldiagrams',
                      'PyGithub',
                      'wxPython',
                      'xmlschema',
                      ]
)
