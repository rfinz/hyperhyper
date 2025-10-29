# the design and demise of xu60

- Link rot
- BitTorrent
- Source control(git, mercurial)
- Hypermedia (the Possiplex, Hypercard, HTTP, HTML, HTMX, HATEOAS, REST)
- IPFS
- The Dark Forest internet
- the federated social internet

How does one extend the functionality of static websites in a way that
1. brings them to life?
   - static websites have very little *conversation* to them
   - the distinction between "static" and "dynamic" can be boiled down to this: "static" just means "receding", while dynamic just means "racing to keep up"
   - dynamism *could* be inserted by the *end user*, in fact, this seems to be the design ethos of hypermedia systems
2. requires very little "out of band" information about the nature of the extension
   - no additional protocols
   - no arcane chain of actions
   - mostly human readable by default
   - mostly "self-documented", i.e. an end user can figure out what is going on without reading much documentation
3. in a way that doesn't force a particular vision for a particular product or configuration
   - extensible(? what this means I'm not particularly sure, especially if I intend to keep the project under the GPL)
   - as few keywords/reserved words/concepts as possible
   - more options available, but "out of the way": you don't need to know about them in order to access all of the functionality of the extension
   
It seems to me that [htmx](https://htmx.org/) holds a piece of the solution: blur the lines between static and dynamic "web" "site" by making HTML into a ***true***, fully capable, hypertext.
   
   
   

