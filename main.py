"""
Hopefully a single file server.
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from pygit2 import Repository
from pygit2.enums import SortMode
from pygit2.enums import ObjectType

REPO_HOME = Path(os.environ.get("HYPERHYPER_REPO_HOME", "."))
SRV_HOME = Path(os.environ.get("HYPERHYPER_SRV_HOME", REPO_HOME))

@asynccontextmanager
async def lifespan(app):
    """
    Lifespan management.
    """
    print('Startup')
    yield
    print('Shutdown')

def directory(request):
    """
    Site tree
    """
    repo = Repository(REPO_HOME)
    res = "object,time,name,length\n"
    prev = {}
    for commit in repo.walk(repo.head.target, SortMode.TOPOLOGICAL | SortMode.TIME | SortMode.REVERSE):
        for e in commit.tree:
            if e.id in prev:
                pass
            else:
                if e.type == ObjectType.BLOB:
                    prev[e.id] = e.name
                    res += f"{e.id},{commit.commit_time},{e.name},{e.size - 1}\n"
                elif e.type ==ObjectType.TREE:
                    pass # TO DO: add recursion into directories
                    
    return PlainTextResponse(res)

def obj(request):
    """
    Get object contents from repo
    """
    repo = Repository(REPO_HOME)
    oid = request.path_params['object']

    start = request.path_params.get('start', 0)
    end = request.path_params.get('end', -1)

    res = repo.get(oid).data
    return PlainTextResponse(res[start:end])

def fil(request):
    """
    Convert file properties to object form.
    """
    repo = Repository(REPO_HOME)
    p = request.path_params['path_to_file']
    versions = {}
    for commit in repo.walk(repo.head.target, SortMode.TOPOLOGICAL | SortMode.TIME | SortMode.REVERSE):
        for e in commit.tree:
            if e.name in versions:
                versions[e.name] = versions[e.name] + [str(e.id)]
            else:
                versions[e.name] = [str(e.id)]

    res = "\n".join(set(versions.get(p,[]))).rstrip()
    return PlainTextResponse(res)


# RESERVED ROUTES: object, file
routes = [
    Route('/object', directory),
    Route('/object/{object}', obj),
    Route('/object/{object}/{start:int}/-', obj),
    Route('/object/{object}/{start:int}/-/{end:int}', obj),
    Route('/object/{object}/-/{end:int}', obj),
    Route('/file', directory),
    Route('/file/{path_to_file:path}', fil),
    Mount('/', app=StaticFiles(directory=SRV_HOME, html=True)),
]

app = Starlette(debug=True, routes=routes, lifespan=lifespan)
