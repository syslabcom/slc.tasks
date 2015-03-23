"""
Task Request view classes

"""
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.content.browser.foldercontents import FolderContentsTable


class TaskRequestView(BrowserView):
    """
    Base class for Task Reports
    """
    template = ViewPageTemplateFile('templates/taskrequest.pt')

    def get_responses(self):
        return self.context.listFolderContents(
            contentFilter={'portal_type':"TaskResponse"}
            )

    def is_current_state(self, state, taskresponse):
        if state == 'late':
            return getattr(self.context, 'dueDate', None) and getattr(self.context, 'dueDate', None) \
                < getattr(taskresponse, 'completionDate', None)
        wft = getToolByName(self.context, 'portal_workflow')
        review_state = wft.getStatusOf("taskresponse_workflow",
                                       taskresponse)["review_state"]
        return state == review_state

    def contents_table(self):
        table = TaskContentsTable(aq_inner(self.context), self.request)
        return table.render()

    def __call__(self):
        return self.template()

class TaskContentsTable(FolderContentsTable):
    """
    List all content in the current folder except for TaskResponses,
    as they are already listed.
    """
    def __init__(self, context, request):
        portal_types = []
        for content_type in context.allowedContentTypes():
            content_type_title = content_type.Title()
            if content_type_title != "TaskResponse":
                portal_types.append(content_type_title)
        if portal_types == []:
            # {"portal_type":None} returns everything since
            # getFolderContents is used instead of a catalog query
            # A dummy portal_type string is used here so that nothing
            # is returned
            portal_types = "AbsolutelyNoContentType"
        super(TaskContentsTable,
              self).__init__(context,
                             request,
                             contentFilter={"portal_type":portal_types})
