# xu60
an ideal backend

**xu60** is a 
- Content-Addressable 
- Hyper Text Transport Protocol 
- Application Programmatic Interface

where hashes and character indexes

define immutable URLs

for re-usable content, (mostly) guaranteed not to rot as a website grows, changes, is edited, or is otherwised enhanced (or regressed)

## scope
1. **xu60** should provide an HTTP server that is simultaneously capable of serving traditional web pages, scripts, and styles alongside whatever content-addressable data an application developer sees fit
2. **xu60** should contain additional functionality for querying document version histories and displaying document metadata such as original paths, edit dates, etc.
3. besides documents, content-addressable document histories, and document/history metadata, **xu60** should remain agnostic to use-case and ship as few features as is plausible
4. **xu60** should virtually never re-code the core algorithms that make its features possible. high-performance versions of virtually every element already exist--**xu60** is a thin application layer built around known technologies. plus I'm dumb

## demo and installation

**xu60** comes with an SPA (built with htmx!! [under construction]) that serves as both a technical demonstration of the server's capabilities, proof-of-concept object browser, and tour of the server's own code.

**xu60** is currently not packaged for distribution, and every aspect (including the project name) is subject to change as the project grows and changes

```sh
# to run xu60 in its current state:
git clone https://github.com/rfinz/xu60.git #clone the repository
cd xu60 #navigate into the project
python -m venv env #create a virtual environment
source env/bin/activate #activate the virtual environment
pip install -r requirements.txt #install required dependencies
uvicorn main:app #run the asgi application
# -> the demo should now be available at 127.0.0.1:8000
```

## to do
- [] finish demo SPA
- [] package python application for distribution
- [] re-write README to reflect the installation differences between a git based development install and using the package as a requirement for your own application

