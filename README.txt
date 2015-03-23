.. contents::

.. Note!
   -----
   Update the following URLs to point to your:

   - code repository
   - bug tracker
   - questions/comments feedback mail
   (do not set a real mail, to avoid spams)

   Or remove it if not used.

- Code repository: https://svn.syslab.com/svn/OSHA/slc.tasks
- Questions, comments, bug reports to info@syslab.com



Introduction
************

slc.tasks consists of some content types and reports which facilitate
a particular form of project management i.e. where a single task is
typically assigned to many groups/individuals to complete separately.

A TaskRequest consists of the relevant details: instructions, due date
etc., an Action to assign this request and contains the assigned
TaskResponses.

A list of group_ids is used to define the potential assignee groups. 

The Assign action creates a TaskResponse for each chosen assignee
group. A local role of editor is set on the TaskResponses so that
members of that group can comment on the task, mark it as complete
etc.

TaskContainers are Folders which also have the Assign action which
will recursively assign all contained TaskRequests to the selected
groups if they have not already been assigned. (For OSHA this replaces
the notions of Workplans / Task-groups / Task-lists)

A new Hierarchy of TaskContainers ("Workplan") can be created from an
existing one by copying and pasting, the TaskResponses will not be
copied. TaskRequests can be assigned to all sub tasks recursively.

The workflow state of multiple TaskResponses can be changed via the
normal "Change state" workflow tool.

Content Types
*************

A TaskRequest has the following fields:
    title
    description ("instruction")
    agencyContact
    priority
    dueDate

TaskRequest contain TaskResponses with the following fields:
    title (assignee group title)
    description ("comments")
    assignedTo (assignee group id)
    startDate
    completionDate

(also possibly add priority and dueDate from the parent to the catalog metadata)

Reports
*******

A TaskContainer displays a count of the workflow state of each
contained TaskResponse. Since TaskContainers can contain other
TaskContainers, this can be used to get an overview of logical groups
of Tasks.

 The browser view @@reports-assignee-tasks presents the hierarchy of
 TaskContainers ordered by assignee.


