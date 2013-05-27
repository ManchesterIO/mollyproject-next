import unittest2 as unittest

from molly.apps.common.components import Attribution, Source


class SourceTestCase(unittest.TestCase):
    def test_source_serialises_fields(self):
        licence_name = 'Open Government Licence'
        licence_url = 'http://www.nationalarchives.gov'
        attribution_text = 'Contains public sector information'
        attribution_url = 'http://www.gov.uk'
        attribution = Attribution(
            licence_name=licence_name,
            licence_url=licence_url,
            attribution_text=attribution_text,
            attribution_url=attribution_url
        )
        url = "http://example.com/provider"
        version = 2
        source = Source(url, version, attribution)
        self.assertEquals(source._asdict(), {
            'self': 'http://mollyproject.org/common/source',
            'attribution': attribution._asdict(),
            'url': url,
            'version': version
        })
