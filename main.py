from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

@asynccontextmanager
async def lifespan(app):
    print('Startup')
    yield
    print('Shutdown')

def home(request):
    return PlainTextResponse('Hello, world!')

routes = [
    Route('/', home)

]

app = Starlette(debug=True, routes=routes, lifespan=lifespan)
