Hypermedia as the engine of application state
=============================================

Molly's not like many other applications. Due to its configuration varying between deployments,
e.g., applications being deployed with different configurations, custom extensions, etc, we
can not make generalisations about the nature of Molly's API - a URL structure and configuration
at one institution may yield different responses than the same configuration at another. To work
around this, we only guarantee the existence of one URL on a Molly site - the root. Every other
URL is then referenced by another, and the full site can be discovered from the root. There is
no defined URL structure for the Molly API.

To deal with this unpredictably, the Molly API is structured as a RESTful API (Representational
state transfer) where each API response is completely self-describing. A client which consumes
the Molly API should not expect a particular response from a URL (except in special cases
mentioned below) but should be able to handle a response based on the defined type of the response.

Each response from Molly is a JSON object, where there is at least one element guaranteed: 'self'.
The value of 'self' is a URI defining the type of that response. Clients should have a handler
for each possible type, and then pass on the object to that handler, based on the value of 'self'.

.. note:: This is loosely equivalent to the 'view_name' field in Molly 1.x, but allows for
          hypermedia links to be specified too, removing the need for the /reverse endpoint.

Objects can contain other objects, for example, a request for a place object may contain information
about events which occur at that place. The handler for the place object can then hand each one
of those events to the event handler for that to be handled. This componentised approach allows
for dumb clients which are responsive to changing APIs and which for common code which can
consume responses from differing Molly installs without large code rewrites.

Sometimes applications may only return references to other components, without the full information
for that component. This is indicated by the 'href' value in the returned object, and can be used
by that component to go and fetch its own information to render itself, for example using
post loading, or if that component has different caching or fetch rules (such as real-time
information for a place).

.. todo:: Real code examples
