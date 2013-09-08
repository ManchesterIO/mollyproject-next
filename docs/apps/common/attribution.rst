``http://mollyproject.org/common/attribution`` - Source Data Attribution
========================================================================

Some source data is used under license or other attribution. These items typically
have an attribution block associated with them. Clients should render the attribution
appropriately, and verbatim, as otherwise the terms of use of the source data
may be violated.

::

    {
        self: "http://mollyproject.org/common/attribution",
        licence_name: "Open Government Licence",
        licence_url: "http://www.nationalarchives.gov.uk/doc/open-government-licence/",
        attribution_text: "Contains public sector information provided by the Met Office"
    }

Blocks of this type are localised according to the Accept-Language headers sent in
the HTTP request. The ``licence_name`` and ``licence_url`` fields are the canonical
names and links to the full terms of use of associated with this source data. The
``attribution_text`` is usage-specific text associated with this particular data.
All fields are optional.
