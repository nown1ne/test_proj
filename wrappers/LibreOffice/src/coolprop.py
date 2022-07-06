import uno
import unohelper
import os, urllib.parse, urllib.request

from org.coolprop.wrappers.libreoffice.CalcAddIn import XCoolProp

try:
    from optparse import Option
    import time
    import json
    import os
    import diskcache
    import datetime
except:
    pass


class CoolPropCalcAddin(unohelper.Base, XCoolProp):
    """CoolProp AddIn for LibreOffice Calc.

    This class wraps the interface declared in XCoolProp.idl to the appropriate
    python function calls.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        pip = ctx.getByName("/singletons/com.sun.star.deployment.PackageInformationProvider")
        extension_uri = pip.getPackageLocation('org.coolprop.wrappers.libreoffice')
        extension_path = urllib.request.url2pathname(urllib.parse.urlparse(extension_uri).path)
        disckcache_path = os.path.normpath(os.path.join(extension_path, 'disckcache'))
        cache = diskcache.Cache(directory=disckcache_path, disk=diskcache.JSONDisk)
        self.index = diskcache.Index.fromcache(cache)

    def GetPythonType(self, inpVal):
        """Calculate fluid properties for a given state from SI inputs."""
        try:
            return str(type(inpVal))
        except Exception as e:
            return str(e)

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(CoolPropCalcAddin,
                                         "org.coolprop.wrappers.libreoffice.CalcAddIn",
                                         ("com.sun.star.sheet.AddIn",),
                                        )
