
import os

from Globals import InitializeClass
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zopyx.smartprintng.plone.browser.pdf import PDFView, PDFDownloadView
from slc.tasks.browser.reports import TasksView, AssigneeTasksView

cwd = os.path.dirname(os.path.abspath(__file__))

class TasksPDFView(PDFDownloadView, TasksView):
    """ Export Tasks report as PDF """

    template = ViewPageTemplateFile('templates/reports_tasks_pdf.pt')
    local_resources = os.path.join(cwd, 'stylesheets')
    transformations = ['makeImagesLocal']


    def __call__(self, *args, **kw):
        self.kw = kw
        self.link_to = 'reports-tasks'
        TasksView.__call__(self)

        pdf_file = PDFDownloadView.__call__(self, *args, **kw)
        return pdf_file


InitializeClass(TasksPDFView)


class TasksAssigneePDFView(PDFDownloadView, AssigneeTasksView):
    """ Export Tasks-assignee report as PDF"""

    template = ViewPageTemplateFile('templates/reports_assignee_tasks_pdf.pt')
    local_resources = os.path.join(cwd, 'stylesheets')
    transformations = ['makeImagesLocal']

    def __call__(self, *args, **kw):
        self.kw = kw
        self.link_to = 'reports-assignee-tasks'
        AssigneeTasksView.__call__(self)

        pdf_file = PDFDownloadView.__call__(self, *args, **kw)
        return pdf_file


InitializeClass(TasksAssigneePDFView)