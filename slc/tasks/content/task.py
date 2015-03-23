"""Definition of the Task content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from slc.tasks import tasksMessageFactory as _
from slc.tasks.interfaces import ITask
from slc.tasks.config import PROJECTNAME

TaskSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.StringField(
        'agencyContact',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Agency contact person"),
            description=_(u"The contact details of people within the agency who can be contacted regarding this task."),
        ),
    ),
    atapi.StringField(
        'assignedTo',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Assigned To"),
            description=_(u"The individuals or groups to whom this task has been assigned."),
        ),
    ),
    atapi.TextField(
        'comments',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Comments"),
            description=_(u"to this task here."),
        ),
    ),
    atapi.ReferenceField(
        'milestone',
        widget=atapi.ReferenceWidget(
            label=_(u"Milestone"),
            description=_(u"The milestone set for this task."),
            format="select",

        ),
        allowed_types=('Milestone'),
        relationship='task_milestone',
    ),
    atapi.StringField(
        'priority',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Priority"),
            description=_(u"The priority of this task."),
            format="select",
        ),
        default=_(u"Medium"),
        vocabulary=["High", "Medium", "Low"]
    ),
    atapi.DateTimeField(
        'dueDate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Due Date"),
            description=_(u"The date that this task must completed"),
        ),
    ),
    atapi.DateTimeField(
        'startDate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Start Date"),
            description=_(u"The date work on this should task should begin"),
        ),
    ),
    atapi.DateTimeField(
        'completionDate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Completion Date"),
            description=_(u"The actual date that this task was completed"),
        ),
    ),
))

TaskSchema['title'].storage = atapi.AnnotationStorage()
TaskSchema['description'].storage = atapi.AnnotationStorage()
TaskSchema['description'].widget.label = 'Instructions' 
schemata.finalizeATCTSchema(TaskSchema, moveDiscussion=False)

class Task(base.ATCTFolder):
    """A task"""
    implements(ITask)

    meta_type = "Task"
    schema = TaskSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    agencyContact = atapi.ATFieldProperty('agencyContact')
    assignedTo = atapi.ATFieldProperty('assignedTo')
    comments = atapi.ATFieldProperty('comments')
    milestone = atapi.ATFieldProperty('milestone')
    priority = atapi.ATFieldProperty('priority')
    dueDate = atapi.ATFieldProperty('dueDate')
    startDate = atapi.ATFieldProperty('startDate')
    completionDate = atapi.ATFieldProperty('completionDate')

atapi.registerType(Task, PROJECTNAME)
