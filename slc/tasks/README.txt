Doc Tests
=========

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True


-*- extra stuff goes here -*-
The TaskResponse content type
===============================

In this section we are tesing the TaskResponse content type by performing
basic operations like adding, updadating and deleting TaskResponse content
items.

Adding a new TaskResponse content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'TaskResponse' and click the 'Add' button to get to the add form.

    >>> browser.getControl('TaskResponse').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'TaskResponse' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'TaskResponse Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'TaskResponse' content item to the portal.

Updating an existing TaskResponse content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New TaskResponse Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New TaskResponse Sample' in browser.contents
    True

Removing a/an TaskResponse content item
--------------------------------

If we go to the home page, we can see a tab with the 'New TaskResponse
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New TaskResponse Sample' in browser.contents
    True

Now we are going to delete the 'New TaskResponse Sample' object. First we
go to the contents tab and select the 'New TaskResponse Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New TaskResponse Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New TaskResponse
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New TaskResponse Sample' in browser.contents
    False

Adding a new TaskResponse content item as contributor
------------------------------------------------

Not only site managers are allowed to add TaskResponse content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'TaskResponse' and click the 'Add' button to get to the add form.

    >>> browser.getControl('TaskResponse').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'TaskResponse' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'TaskResponse Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new TaskResponse content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The TaskRequest content type
===============================

In this section we are tesing the TaskRequest content type by performing
basic operations like adding, updadating and deleting TaskRequest content
items.

Adding a new TaskRequest content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'TaskRequest' and click the 'Add' button to get to the add form.

    >>> browser.getControl('TaskRequest').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'TaskRequest' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'TaskRequest Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'TaskRequest' content item to the portal.

Updating an existing TaskRequest content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New TaskRequest Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New TaskRequest Sample' in browser.contents
    True

Removing a/an TaskRequest content item
--------------------------------

If we go to the home page, we can see a tab with the 'New TaskRequest
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New TaskRequest Sample' in browser.contents
    True

Now we are going to delete the 'New TaskRequest Sample' object. First we
go to the contents tab and select the 'New TaskRequest Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New TaskRequest Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New TaskRequest
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New TaskRequest Sample' in browser.contents
    False

Adding a new TaskRequest content item as contributor
------------------------------------------------

Not only site managers are allowed to add TaskRequest content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'TaskRequest' and click the 'Add' button to get to the add form.

    >>> browser.getControl('TaskRequest').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'TaskRequest' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'TaskRequest Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new TaskRequest content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Task content type
===============================

In this section we are tesing the Task content type by performing
basic operations like adding, updadating and deleting Task content
items.

Adding a new Task content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Task' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Task').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Task' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Task Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Task' content item to the portal.

Updating an existing Task content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Task Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Task Sample' in browser.contents
    True

Removing a/an Task content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Task
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Task Sample' in browser.contents
    True

Now we are going to delete the 'New Task Sample' object. First we
go to the contents tab and select the 'New Task Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Task Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Task
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Task Sample' in browser.contents
    False

Adding a new Task content item as contributor
------------------------------------------------

Not only site managers are allowed to add Task content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Task' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Task').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Task' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Task Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Task content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



