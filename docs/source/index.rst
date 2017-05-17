.. clevertim-api-py documentation master file, created by
   sphinx-quickstart on Mon May 15 10:34:23 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
Clevertim Python API documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Background
==========

`Clevertim CRM <https://www.clevertim.com>`_ is a simple CRM and web based contact management system for small businesses. It allows small teams to keep their contacts, companies, sales opportunities, support cases, files, notes and emails together in one central web location, making it accessible from anywhere and from any device.

The Clevertim Python API allows you to connect to your `Clevertim CRM <https://www.clevertim.com>`_ account and manipulate your data programmatically.
The API connection requires an API key, which is user based (i.e. each onboarded Clevertim user will have a different API key) and the data visibility rules, data updates and deletions will observe the user permissions set in Clevertim. Any changes done via the API will be visible in the "What's New" section in Clevertim.

The Clevertim Python API is a Python wrapper on top of the Clevertim REST API which is described at `https://github.com/clevertim/clevertim-crm-api <https://github.com/clevertim/clevertim-crm-api>`_ and it can be used directly via tools like curl. The Clevertim Python API makes it easier to use the REST API by providing valuable cross-linking of models, validating inputs/outputs, provide client side caching and trying to make your life as a developer easier. The Clevertim Python API is being developed at `https://github.com/ciprianmiclaus/clevertim-api-py <https://github.com/ciprianmiclaus/clevertim-api-py>`_.
   
Getting started
===============

Install the Clevertim Python API
--------------------------------

::

	pip install clevertimapi

The Clevertim Python API supports the following versions of Python: 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, 3.6, pypy and pypy3.


Get your API key
----------------
	
In order to connect to connect to Clevertim you will need an API key. This is available in Clevertim in the `My Info & settings / API Key section <https://www.clevertim.com/welcome/#info-settings>`_. You might have to generate the API key the first time.

The API key consists of a long alpha-numeric set of characters and it should look like this:

::

	ITHkCPbXdOWfGNTj5qOzNJkceftfRWwGXtrU39exmW0UzVwKUiZ1343

The above API key is included for illustration purposes only to help you identify the API key in Clevertim. The API key above will be used in the examples on this website, but please keep in mind, your API key will be different.

Create a Session
----------------

The Session instance is at the heart of the API and it's the first object you create. All the other objects and endpoints require a session object to be passed in.
The Session object is the place that stores the API key, makes all the REST requests and provides some caching.

.. code-block:: python

	from clevertimapi import Session
	
	session = Session(api_key='ITHkCPbXdOWfGNTj5qOzNJkceftfRWwGXtrU39exmW0UzVwKUiZ1343')

This session object will then be used in all subsequent request and object instantiations where a session is required.	

The concept of key
------------------

All objects/endpoints in the system have a **key**. You can think of the key as a primary key, in relational DB terminology, or a unique identifier. The key is the identifier that identifies a particular contact, company, etc. among all the other items of the same kind. For objects of different type, the key could overlap. For example, you could have a Contact and a Case with the same key.

New objects which have not yet saved to Clevertim do *not* have a key. The key will be None. Once an object's save method is call to persist it in Clevertim, a key will be allocated from the server to identify that object uniquely among all others of the same type.

Some simple examples
--------------------

Loading a contact which exists in Clevertim:

.. code-block:: python

	from clevertimapi import Contact

	contact = Contact(session, key=1234)
	# now access the contact
	print(contact.first_name)

Adding a new contact

.. code-block:: python

	from clevertimapi import Contact

	contact = Contact(session)
	contact.first_name = 'Mike'
	contact.last_name = 'Johnson'
	contact.save()
	# at this point, the contact will be persisted on the server
	# and allocated a key
	print(contact.key)

Editing an existing contact

.. code-block:: python

	from clevertimapi import Contact

	contact = Contact(session, key=1234)
	# add a new email for this contact
	contact.emails.add('joe.dorian@gmail.com')
	# now save the change to the server
	contact.save()

Deleting an existing contact

.. code-block:: python

	from clevertimapi import Contact

	contact = Contact(session, key=1234)
	contact.delete()
	# the contact instance continues to hold the previous data
	# but it has been deleted from the server
	# and its key will be None
	assert contact.key is None

Lazy loading of data
--------------------

Any resource/object can be loaded in a lazy or eager fashion. This is controlled via the lazy_load parameter when the instance is created.
Here is an example.

Eager loading will load the instance on creation. Eager loading is the default *modus operandi*.

.. code-block:: python

	from clevertimapi import Contact

	# the next line makes a REST request to the server and
	# load the instance
	contact = Contact(session, key=1234)

Lazy loading will not load the instance on creation, but on the first access of a property that comes from the server.

.. code-block:: python

	from clevertimapi import Contact

	# the next line will not make a REST call
	contact = Contact(session, key=1234, lazy_load=True)
	# accessing the key will not load the object
	# since the key is available on the client side
	print(contact.key)
	# the next call will make the REST call
	print(contact.first_name)

.. warning::
	* When working with eagerly loaded instances, an incorrect key will raise an exception on instance creation.
	* When working with lazily loaded instances, an incorrect key will only raise on the first access of the property.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
