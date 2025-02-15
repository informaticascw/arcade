import os, glob
from collections.abc import Iterable
from importlib.machinery import SourceFileLoader
from menu.components.Router import Router

def getPages (path:str) -> Iterable:
    res = dict()
    
    for file in glob.glob(os.path.join(path, "*.py")):
        fileName = os.path.basename(file)
        foo = SourceFileLoader(fileName.replace(".py", ""), file).load_module()
        
        pageName = foo.page.name.lower()
        if pageName in res.keys():
            raise Exception("Duplicate page names found")
        res[pageName] = foo.page

    return res

router:Router = Router(getPages(os.path.join("src", "menu", "pages")))