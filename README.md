# hyperhyper
an ideal backend

**hyperhyper** is a 
- Content-Addressable 
- Hyper Text Transport Protocol 
- Application Programmatic Interface

where hashes and character indexes

define immutable URLs

for re-usable content, (mostly) guaranteed not to rot as a website grows, changes, is edited, or is otherwised enhanced (or regressed)

## scope
1. **hyperhyper** should provide an HTTP server that is simultaneously capable of serving traditional web pages, scripts, and styles alongside whatever content-addressable data an application developer sees fit
2. **hyperhyper** should contain additional functionality for querying document version histories and displaying document metadata such as original paths, edit dates, etc.
3. besides documents, content-addressable document histories, and document/history metadata, **hyperhyper** should remain agnostic to use-case and ship as few features as is plausible
4. **hyperhyper** should virtually never re-code the core algorithms that make its features possible. high-performance versions of virtually every element already exist--**hyperhyper** is a thin application layer built around known technologies. plus I'm dumb
