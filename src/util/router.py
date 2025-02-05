import sys, glob
from collections.abc import Iterable
from importlib.machinery import SourceFileLoader
from menu.components.Router import Router

def getPages (path) -> Iterable:
    path = "\\".join(sys.path[0].split("\\")) + path
    sys.path.append(path)
    
    files = glob.glob(path + "/*.py")
    res = dict()
    
    for file in files:
        fileName:str = file.split("\\")[-1]
        foo = SourceFileLoader(fileName[:-3], f"{path.split('/')[-1]}/{fileName}").load_module()
        
        pageName = foo.page.name.lower()
        if pageName in res.keys():
            raise Exception("Duplicate page names found")
        res[pageName] = foo.page
    return res

router:Router = Router(getPages("\\pages"))