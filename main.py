"""
Hopefully a single file server.
"""
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from pygit2 import Repository

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
    return PlainTextResponse('Hello, world!')

def obj(request):
    pass

routes = [
    Route('/', home),
    Route('/{repo}/{object}', obj)
]

app = Starlette(debug=True, routes=routes, lifespan=lifespan)
