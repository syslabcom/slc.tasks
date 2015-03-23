"""Definition of the TaskResponse content type
"""
from datetime import datetime

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from slc.tasks import tasksMessageFactory as _
from slc.tasks.interfaces import ITaskResponse
from slc.tasks.config import PROJECTNAME

TaskResponseSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField(
        'assignedTo',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Assigned To"),
            description=_(u"The individuals or groups to whom this task has been assigned."),
        ),
    ),
    atapi.DateTimeField(
        'startDate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Start Date"),
            show_hm=False,
            show_ymd=True,
            starting_year=datetime.now().year,
            description=_(u"The date on which work commenced on this task"),
        ),
    ),
    atapi.DateTimeField(
        'completionDate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Completion Date"),
            show_hm=False,
            show_ymd=True,
            starting_year=datetime.now().year,
            description=_(u"The actual date that this task was completed"),
        ),
    ),

))


TaskResponseSchema['title'].storage = atapi.AnnotationStorage()
TaskResponseSchema['title'].widget.label = _(u'Country')
TaskResponseSchema['description'].storage = atapi.AnnotationStorage()
TaskResponseSchema['description'].widget.label = 'Comments'

schemata.finalizeATCTSchema(
    TaskResponseSchema,
    folderish=True,
    moveDiscussion=False
    )


class TaskResponse(folder.ATFolder):
    """The response to a Task Request"""
    implements(ITaskResponse)

    meta_type = portal_type = "TaskResponse"
    schema = TaskResponseSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    assignedTo = atapi.ATFieldProperty('assignedTo')
    startDate = atapi.ATFieldProperty('startDate')
    completionDate = atapi.ATFieldProperty('completionDate')

atapi.registerType(TaskResponse, PROJECTNAME)
