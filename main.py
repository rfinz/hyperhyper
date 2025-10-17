"""
Hopefully a single file server.
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from pygit2 import Repository
from pygit2.enums import SortMode

REPO_HOME = Path(os.environ.get("HYPERHYPER_REPO_HOME", "."))

@asynccontextmanager
async def lifespan(app):
    """
    Lifespan management.
    """
    print('Startup')
    yield
    print('Shutdown')

def home(request):
    """
    Site index route.
    """
    repo = Repository(REPO_HOME)
    res = ""
    for commit in repo.walk(repo.head.target, SortMode.TOPOLOGICAL | SortMode.TIME | SortMode.REVERSE):
        res += "{} | {} | {}\n".format(commit.commit_time, commit.id, commit.message.rstrip())
        pass
    return PlainTextResponse(res)

def obj(request):
    """
    Get object contents from repo
    """
    repo = Repository(REPO_HOME)
    oid = request.path_params['object']
    return PlainTextResponse(repo.get(oid).data)


routes = [
    Route('/', home),
    Route('/{object}', obj)
]

app = Starlette(debug=True, routes=routes, lifespan=lifespan)
