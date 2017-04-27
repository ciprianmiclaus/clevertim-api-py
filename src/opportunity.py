from endpoint import Endpoint, make_single_elem_property, make_multi_elem_property


class Opportunity(Endpoint):

	ENDPOINT = '/opportunity'

	name = make_single_elem_property('name', basestring, '', 'Opportunity headline description')