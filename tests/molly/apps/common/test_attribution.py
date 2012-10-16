import unittest2 as unittest

from molly.apps.common.attribution import Attribution

class EndpointTestCase(unittest.TestCase):
    def test_attribution_serialises_fields(self):
        licence_name = 'Open Government Licence'
        licence_url = 'http://www.nationalarchives.gov'
        attribution_text = 'Contains public sector information'
        attribution = Attribution(
            licence_name=licence_name,
            licence_url=licence_url,
            attribution_text=attribution_text
        )
        dict = attribution.as_dict()
        self.assertEquals(attribution.as_dict(), {
            'self': 'http://mollyproject.org/common/attribution',
            'licence_name': 'Open Government Licence',
            'licence_url': 'http://www.nationalarchives.gov',
            'attribution_text': 'Contains public sector information'
        })
