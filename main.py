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

    def construct(tree, name=""):
        level = ""
        for e in tree:
            if e.id in prev:
                pass
            else:
                if e.type == ObjectType.BLOB:
                    prev[e.id] = e.name
                    p = f'{name}/{e.name}'[1:]
                    level += f'{e.id},{commit.commit_time},{p},{e.size - 1}\n'
                if e.type == ObjectType.TREE:
                    level += construct(e, name=f'{name}/{e.name}')
        return level

    for commit in repo.walk(repo.head.target, SortMode.TOPOLOGICAL | SortMode.TIME | SortMode.REVERSE):
        res += construct(commit.tree)

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

def vers(request):
    """
    Convert file properties to object form.
    """
    repo = Repository(REPO_HOME)
    p = request.path_params['path_to_file']
    prev = {}
    versions = {}
    def construct(tree, name=""):
        names = []
        for e in tree:
            if e.id in prev:
                pass
            else:
                if e.type == ObjectType.BLOB:
                    prev[e.id] = e.name
                    path = f'{name}/{e.name}'[1:]
                    names += [(f'{path}', e.id)]
                if e.type == ObjectType.TREE:
                    names += construct(e, name=f'{name}/{e.name}')
        return names
    
    for commit in repo.walk(repo.head.target, SortMode.TOPOLOGICAL | SortMode.TIME | SortMode.REVERSE):
        fil = construct(commit.tree)
        for v in fil:
            if v[0] in versions:
                versions[v[0]] = versions[v[0]] + [str(v[1])]
            else:
                versions[v[0]] = [str(v[1])]
    res = "\n".join(versions.get(p,[])).rstrip()
    return PlainTextResponse(res)


# RESERVED ROUTES: object, versions
routes = [
    Route('/object', directory),
    Route('/object/', directory), # kindness is virtue
    Route('/object/{object}', obj),
    Route('/object/{object}/{start:int}/-', obj),
    Route('/object/{object}/{start:int}/-/{end:int}', obj),
    Route('/object/{object}/-/{end:int}', obj),
    Route('/versions', directory),
    Route('/versions/', directory), # kindness is virtue
    Route('/versions/{path_to_file:path}', vers),
    Mount('/', app=StaticFiles(directory=SRV_HOME, html=True)),
]

app = Starlette(debug=True, routes=routes, lifespan=lifespan)
