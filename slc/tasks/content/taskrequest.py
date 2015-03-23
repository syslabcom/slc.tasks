"""Definition of the TaskRequest content type
"""
from datetime import datetime

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from slc.tasks import tasksMessageFactory as _
from slc.tasks.interfaces import ITaskRequest
from slc.tasks.config import PROJECTNAME

TaskRequestSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField(
        'agencyContact',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Agency contact person"),
            description=_(u"The contact details of people within the agency who can be contacted regarding this task."),
        ),
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
            show_hm=False,
            show_ymd=True,
            starting_year=datetime.now().year,
            description=_(u"The date that this task must completed"),
        ),
    ),
))

TaskRequestSchema['title'].storage = atapi.AnnotationStorage()
TaskRequestSchema['description'].storage = atapi.AnnotationStorage()
TaskRequestSchema['description'].widget.label = 'Instructions'

schemata.finalizeATCTSchema(
    TaskRequestSchema,
    folderish=True,
    moveDiscussion=False
)


class TaskRequest(folder.ATFolder):
    """Details of a requested Task"""
    implements(ITaskRequest)

    meta_type = portal_type = "TaskRequest"
    schema = TaskRequestSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    agencyContact = atapi.ATFieldProperty('agencyContact')
    priority = atapi.ATFieldProperty('priority')
    dueDate = atapi.ATFieldProperty('dueDate')

atapi.registerType(TaskRequest, PROJECTNAME)
