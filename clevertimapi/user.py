from .session import Session
from .endpoint import Endpoint, make_single_readonly_property


class User(Endpoint):

	ENDPOINT = '/user'

	name = make_single_readonly_property('user', '', 'User\'s name')
	email = make_single_readonly_property('email', '', 'User\'s email')

	is_owner = make_single_readonly_property('is_owner', False, 'Boolean indicator if the user is the owner of the Clevertim account')
	is_admin = make_single_readonly_property('is_admin', False, 'Boolean indicator if the user is an administrator of the Clevertim account')

	permissions = make_single_readonly_property('permissions', [], 'A list of permissions this user has')

	registration_pending = make_single_readonly_property('pending', False, 'True when the user has been invited to join Clevertim but has not yet joined, False if the user has registered')


Session.register_endpoint(User)