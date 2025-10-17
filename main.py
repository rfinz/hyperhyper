"""
Hopefully a single file server.
"""
import os
import datetime
from contextlib import asynccontextmanager
from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from pygit2 import Repository
from pygit2.enums import SortMode

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

def tree(request):
    """
    Site tree
    """
    repo = Repository(REPO_HOME)
    res = ""
    for commit in repo.walk(repo.head.target, SortMode.TOPOLOGICAL | SortMode.TIME):
        res += "{} | {} | {}\n".format(datetime.datetime.fromtimestamp(commit.commit_time), commit.id, commit.message.rstrip())

    return PlainTextResponse(res)

def obj(request):
    """
    Get object contents from repo
    """
    repo = Repository(REPO_HOME)
    oid = request.path_params['object']
    return PlainTextResponse(repo.get(oid).data)

# RESERVED ROUTES: tree, object
routes = [
    Route('/tree', tree),
    Route('/object/{object}', obj),
    Mount('/', app=StaticFiles(directory=SRV_HOME, html=True)),
]

app = Starlette(debug=True, routes=routes, lifespan=lifespan)
