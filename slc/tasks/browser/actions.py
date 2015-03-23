"""
BrowserView Classes for Actions specific to Tasks

AssignTaskView: create TaskResponses for each selected assignee

"""

import itertools

from Acquisition import aq_parent, aq_base, aq_inner
from zope.app.component.hooks import getSite
import zope.event

from Products.Archetypes.event import ObjectInitializedEvent
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.content.browser.tableview import Table
from plone.app.content.browser.foldercontents import FolderContentsTable


class AssignTaskView(BrowserView):
    """
    create TaskResponses for each selected assignee
    """
    template = ViewPageTemplateFile('templates/actions_assign_task.pt')

    assignees = None

    def assign_tasks(self):
        for assignee in self.assignees:
            if assignee not in self.context.objectIds():
                self.context.invokeFactory("TaskResponse", assignee)
                task_response = self.context.get(assignee, None)
                if task_response:
                    task_response.title = self.assignee_groups.get(assignee,
                                                                   assignee)
                    task_response.assignedTo = assignee
                    task_response.manage_setLocalRoles(assignee, ["Editor"])
                    task_response.__ac_local_roles_block__ = True
                    # We may need to reindex:
                    # task_response.reindexObjectSecurity()
                    # Explicitly triggering the ObjectInitializedEvent
                    # otherwise the stickystatusmessages don't get created
                    event = ObjectInitializedEvent(task_response)
                    zope.event.notify(event)

    def __call__(self):
        self.request.set("disable_border", True)
        self.existing_assignees = self.context.objectIds()
        self.assignee_groups = {}
        for i in self._inherited_group_roles():
            self.assignee_groups[i[0]] = i[3]

        self.group_ids = sorted([
            i for i in self.assignee_groups.keys() \
            if i not in self.existing_assignees
            ])

        form = self.request.form
        self.assignees = form.get("assignees", None)
        do_assign = form.get("form.button.assign", False)
        do_cancel = form.get("form.button.cancel", False)
        if form == {}:
            return self.template()
        elif do_cancel:
            self.request.response.redirect(self.context.absolute_url())
        elif self.assignees:
            assignees = set(self.assignees)
            self.existing_assignees = sorted(
                assignees.intersection(self.existing_assignees)
                )
            self.assignees = sorted(
                assignees.difference(self.existing_assignees)
                )
            self.assign_tasks()
            return self.template()


    # From plone.app.workflow.browser.sharing

    def inherited(self, context=None):
        """Return True if local roles are inherited here.
        """
        if context is None:
            context = self.context
        if getattr(aq_base(context), '__ac_local_roles_block__', None):
            return False
        return True

    def _inherited_group_roles(self):
        """
        only returning group roles instead of the original version of
        _inherited_roles which also returned user roles

        Returns a tuple with the acquired local roles. """
        context = self.context

        if not self.inherited(context):
            return []

        portal = getSite()
        result = []
        cont = True
        if portal != context:
            parent = aq_parent(context)
            while cont:
                if not getattr(parent, 'acl_users', False):
                    break
                userroles = parent.acl_users._getLocalRolesForDisplay(parent)
                for user, roles, role_type, name in userroles:
                    # Only returning the groups which have "Reader" role
                    if role_type == "group" and "Reader" in roles:
                        # Find user in result
                        found = 0
                        for user2, roles2, type2, name2 in result:
                            if user2 == user:
                                # Check which roles must be added to roles2
                                for role in roles:
                                    if not role in roles2:
                                        roles2.append(role)
                                found = 1
                                break
                        if found == 0:
                            # Add it to result and make sure roles is a list so
                            # we may append and not overwrite the loop variable
                            result.append([user, list(roles), role_type, name])
                if parent == portal:
                    cont = False
                elif not self.inherited(parent):
                    # Role acquired check here
                    cont = False
                else:
                    parent = aq_parent(parent)

        # Tuplize all inner roles
        for pos in range(len(result)-1, -1, -1):
            result[pos][1] = tuple(result[pos][1])
            result[pos] = tuple(result[pos])

        return tuple(result)

class TaskContentsTable(FolderContentsTable):
    """
    List TaskResponses in the current folder
    """
    def __init__(self, context, request,
                 contentFilter={"portal_type":"TaskResponse"}):
        self.context = context
        self.request = request
        self.contentFilter = contentFilter
        self.items = self.folderitems()

        url = context.absolute_url()
        view_url = url + '/@@taskresponse-manage'
        self.table = Table(request, url, view_url, self.items,
                           show_sort_column=self.show_sort_column,
                           buttons=self.buttons)



class TaskResponseManage(BrowserView):
    """
    folder_contents view for TaskResponses to allow the standard
    Delete/Change State etc. to be used.
    """
    template = ViewPageTemplateFile('templates/taskresponse-manage.pt')

    def __call__(self):
        return self.template()

    def contents_table(self):
        table = TaskContentsTable(aq_inner(self.context), self.request)
        return table.render()
