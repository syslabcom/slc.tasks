"""
ask Report view classes

Two views:

The tasks which have actually been assigned to assignees arranged in a
hierarchy of workplans, task groups and task lists.

The task templates, with a summary of the workflow states of these
tasks as assigned to various assignees. Arranged in hierarchy of task
groups and task lists.

"""

import os
from itertools import count

from lxml import etree
from lxml.builder import E

from Products.CMFPlone.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class TaskReport(BrowserView):
    """
    Base class for Task Reports
    """
    paths_details = {}
    task_states = ["in_progress", "completed", "pending", "on_hold", "late"]
    task_portal_type = ["TaskResponse", "Task"]

    def generate_task_tree(self, group_by_id=False):
        """
        Create a hierarchy of tasks for display.
        Task containers display a count of sub tasks in each workflow state
        TaskRequests have addional details

        Sample tree produced when the group_id is "romania"
        FIXME the top brain actually has a value right now, it should be None
        {'brain': None,
         'contents': {'romania': {'brain': None,
                                  'contents': {'workplanA': {'brain': <Brain>,
                                                             'contents': ...,
                                                             'id': 'node-2',
                                                             'pending': 1}},
                                  'id': 'node-1',
                                  'pending': 1,
                                  'title': 'Romania'}},
         'id': 'node-0',
         'pending': 1}

        generate the html for the tree table body
        """
        if self.context.portal_type == 'TaskRequest':
            # If the report is called on a TaskRequest, set the current_path to the parent,
            # so that the TaskRequest's details are included in the report.
            # Also set the allowed_path to the TaskRequest's path, so that other TaskRequests
            # in the parent will NOT be added to the report.
            self.allowed_path = "/".join(self.context.getPhysicalPath())
            current_path = "/".join(self.context.aq_parent.getPhysicalPath())
        else:
            self.allowed_path = ''
            current_path = "/".join(self.context.getPhysicalPath())

        pc = getToolByName(self, "portal_catalog")
        task_containers = pc.searchResults(portal_type=["Folder",
                                                        "TaskRequest"],
                                           path=current_path,
                                           limit=999999999)
        self.task_container_details = {}
        # map all container paths to their brains once, this is re-used
        # for each group
        for container in task_containers:
            self.task_container_details[container.getPath()] = container

        task_response_brains = pc.searchResults(portal_type=self.task_portal_type,
                                                path=current_path,
                                                limit=999999999)

        self.task_tree = {}
        self.node_count = count()
        for task_response_brain in task_response_brains:
            resp_ob = task_response_brain.getObject()
            req_ob = resp_ob.aq_parent
            review_state = task_response_brain.review_state
            is_late = getattr(req_ob, "dueDate", None) < \
                      getattr(resp_ob, "completionDate", None)

            if group_by_id:
                group_id = task_response_brain.getId
            else:
                group_id = None
            self.add_task_branch_recurse(current_path=current_path,
                                         current_branch=self.task_tree,
                                         is_late=is_late,
                                         review_state=review_state,
                                         brain=task_response_brain,
                                         group_id=group_id)

        # Using the lxml.builder E-factory to create the html
        # http://codespeak.net/lxml/tutorial.html#the-e-factory
        self.tbody = E.tbody()
        hide_responses = group_by_id
        self.html_task_branch_recurse("", self.task_tree, hide_responses, level=0)
        self.tbody_html = etree.tostring(self.tbody,
                                         encoding="UTF-8",
                                         pretty_print=True)

        # make unicode out of the whole shebang
        try:
            self.tbody_html = self.tbody_html.decode('utf-8')
        except UnicodeDecodeError:
            pass


    def add_task_branch_recurse(self, current_path, current_branch,
                                is_late, review_state, brain, group_id=None):

        """
        Generates the a hierarchical dict to contain all the details
        relevant for reports.

        As each TaskResponse is added to the dict, it's state
        (completed, on_hold) is counted on each branch.
        """

        # If a group_id is specified then this is added to the top of
        # the hierarchy
        if group_id:
            current_branch.setdefault("contents", {})
            # FIXME setting "brain" to None for the branch with the
            # group details. It avoids the need for a "portal_type"
            # key:value but it's not very clear what's going on.
            current_branch["contents"].setdefault(group_id, {"brain": None})

        # A unique id is generated for each row, this is required for
        # the jquery.treetable functionality
        if not current_branch.has_key("id"):
            node_id = "node-%s" % self.node_count.next()
            current_branch["id"] = node_id

        # If the TaskResponse is_late, then increment the count for
        # the current_branch
        if is_late:
            late_count = current_branch.setdefault("late", 0)
            current_branch["late"] = late_count + 1

        # get the id of the next folder by comparing paths
        current_path = current_path.rstrip("/")
        remaining_path = brain.getPath().replace(current_path, "")
        remaining_path = remaining_path.lstrip("/")
        current_folder = remaining_path.split("/")[0]
        
        # If we're calling the report directly on a task request, we must filter
        # out all other task requests that might lie in the same folder.
        # This is done by comparing the current path to the allowed_path
        if self.allowed_path and not \
            os.path.join(current_path, current_folder).startswith(self.allowed_path):
            return

        if current_folder == "":
            # Finally, add the TaskResponse details
            current_branch["title"] = brain.Title
            current_branch["brain"] = brain

        else:
            # Increment the count for review_state on the current_branch
            review_state_count = current_branch.setdefault(review_state, 0)
            current_branch[review_state] = review_state_count + 1

            # Add the brain if it hasn't been added already

            # FIXME By adding "brain": None to the group branch
            # (above) we also skip adding it again here. Again it
            # isn't very readable.
            if not current_branch.has_key("brain"):
                current_branch["brain"] = \
                    self.task_container_details.get(current_path, None)

            # Add the next branch
            contents = current_branch.setdefault("contents", {})
            if group_id:
                # now that we have the group_id branch added we can
                # start building up the tree from there
                next_path = current_path
                next_branch = current_branch["contents"][group_id]
                next_branch["title"] = brain.Title
            else:
                next_path = current_path +"/"+ current_folder
                next_branch = contents.setdefault(current_folder, {})

            self.add_task_branch_recurse(current_path=next_path,
                                         current_branch=next_branch,
                                         is_late=is_late,
                                         review_state=review_state,
                                         brain=brain)

    def html_task_branch_recurse(self, parent_id, current_branch,
                                 hide_responses, level=1):
        """
        Generates the html required for the treetable table body by
        walking through the task_tree contents

        "branch" refers to the branch of the tree

        TODO consider breaking this into 4 functions to make it easier
        to read:
        add_group_row, add_task_container_row,
        add_task_request_row, add_task_response_row
        """
        contents = current_branch.get("contents")
        if contents:
            # branch_id is the Folder/TaskRequest/TaskResponse id
            level += 1
            for branch_id in sorted(contents.keys()):
                branch = contents[branch_id]
                brain = branch["brain"]
                # Again, abusing the fact that "brain" is set to None
                # for the group branch
                is_group_branch = not brain
                if hide_responses and not is_group_branch and \
                       brain.portal_type == "TaskResponse":
                    return

                row = E.tr(id=branch["id"])
                self.tbody.append(row)
                if parent_id:
                    row.attrib["class"] = "child-of-%(id)s task-level-%(level)d" % dict(
                        id=parent_id, level=level)
                else:
                    row.attrib["class"] = "task-level-%d" % level

                # The first column
                td_summary = etree.SubElement(row, "td")
                td_summary.attrib["class"] = "first-col"

                # Make unicode out of the descripion, since it might contain non-ASCII
                description = brain and brain.Description or ''
                try:
                    description = description.decode('utf-8')
                except UnicodeEncodeError:
                    pass
                if is_group_branch:
                    td_summary.text = branch.get("title", '')
                    td_summary.attrib["colspan"] = "4"

                elif brain.portal_type == "Folder":
                    td_summary.append(E.a(brain.Title,
                                          href=brain.getURL()+ "/" +
                                          getattr(self, 'link_to', self.__name__)
                                          ))
                    td_summary.attrib["colspan"] = "4"
                    # The state of sub TaskResponses is added below

                # Add the task title, description, contact, priority
                # and due date
                elif brain.portal_type in ["TaskRequest", "Task"]:
                    req_ob = brain.getObject()
                    td_summary.append(E.a(brain.Title,
                                          href=brain.getURL()))
                    td_summary.append(E.div(description))

                    agencyContact = req_ob.agencyContact
                    if agencyContact:
                        agencyContact = agencyContact.decode("utf-8")
                    else:
                        agencyContact = ""
                    row.append(E.td(agencyContact))
                    row.append(E.td(req_ob.priority))
                    row.append(E.td(str(req_ob.dueDate)))

                # For TaskResponses we don't have contact, priority
                # or due date
                elif brain.portal_type == "TaskResponse":
                    resp_ob = brain.getObject()
                    td_summary.append(E.a(brain.Title,
                                          href=brain.getURL()))
                    td_summary.append(E.div(description))

                    td_summary.attrib["colspan"] = "3"
                    row.append(E.td(str(resp_ob.startDate)))

                # Adding a check icon to TaskResponse and Task objects
                # to show their workflow state
                if not is_group_branch and\
                       brain.portal_type in self.task_portal_type:
                    # Display the state of this TaskResponse
                    for state in self.task_states:
                        td = etree.SubElement(row, "td")
                        checkicon = E.img(src=brain.getURL() + "/++resource++slc.tasks.images/check32.png")
                        checkicon.attrib["class"] = 'check-icon'
                        if brain.review_state == state:
                            td.append(checkicon)
                        elif state == "late" and branch.get("late", False):
                            td.append(checkicon)

                if is_group_branch or \
                       brain.portal_type in ["Folder", "TaskRequest"]:
                    # Display the number of sub TasksResponses which
                    # are in each possible state
                    for state in self.task_states:
                        row.append(E.td(str(branch.setdefault(state, 0))))

                self.html_task_branch_recurse(branch["id"],
                                              contents[branch_id],
                                              hide_responses,
                                              level)


class AssigneeTasksView(TaskReport):
    """
    #985 [R06] Task management - Report: Assignee Tasks

    As a guest, I can view a tree of task groups/task lists/ tasks for
    a particular assignee.

    *Belgium:*
    * Website Management | In Progress | Completed | Pending | On Hold | Late |
    ** FOP national website  | In Progress | Completed | Pending | On Hold | Late |
    *** Add content to and promote national Website | Task contact | Status | Start date | Due Date | Priority |

    """
    template = ViewPageTemplateFile('templates/reports_assignee_tasks.pt')

    def __call__(self):
        """
        Generate the html for the tbody of the treetable and return
        the template
        """
        self.generate_task_tree(group_by_id=True)
        return self.template()


class TasksView(TaskReport):
    """
    #821 [R06] Task management - Report: Workplan Tasks Summary

    As a coordinator, I can view a report showing the status of all
    tasks and the number of FOPs which have completed each task.

    * Website Management | In Progress | Completed | Pending | On Hold | Late |
    ** FOP national website  | In Progress | Completed | Pending | On Hold | Late |
    *** Add content to and promote national Website
    | Task contact | In Progress | Completed | Pending | On Hold | Late | Start date | Due Date | Priority |

    """
    template = ViewPageTemplateFile('templates/reports_tasks.pt')

    def __call__(self):
        """
        Generate the html for the tbody of the treetable and return
        the template
        """
        self.generate_task_tree(group_by_id=False)
        return self.template()

class LegacyTasksView(TaskReport):
    """
    #821 [R06] Task management - Report: Workplan Tasks Summary

    As a coordinator, I can view a report showing the status of all
    tasks and the number of FOPs which have completed each task.

    * Website Management | In Progress | Completed | Pending | On Hold | Late |
    ** FOP national website  | In Progress | Completed | Pending | On Hold | Late |
    *** Add content to and promote national Website
    | Task contact | In Progress | Completed | Pending | On Hold | Late | Start date | Due Date | Priority |

    """
    template = ViewPageTemplateFile('templates/reports_tasks.pt')

    def __call__(self):
        """
        Generate the html for the tbody of the treetable and return
        the template
        """
        self.task_portal_type = ["Task"]
        self.generate_task_tree(group_by_id=False)
        return self.template()
