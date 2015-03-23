"""
Task Response view classes

"""

from DateTime import DateTime
import datetime

from collective.z3cform.datetimewidget.widget_date import DateWidget
from plone.z3cform import z2

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class TaskResponseView(BrowserView):
    """
    Base class for Task Reports

    TODO Add error checking
    """
    template = ViewPageTemplateFile('templates/taskresponse.pt')

    def __call__(self):
        self.request.set("disable_border", True)

        # TODO test this and swap it in
        # site = getSite()
        # wft = site.portal_workflow

        context = self.context
        wft = context.portal_workflow

        form = self.request.form
        comments = form.get("task_comments", "")
        if comments:
            context.setDescription(comments)

        start_date_year = form.get("startDate-year", "")
        start_date_month = form.get("startDate-month", "")
        start_date_day = form.get("startDate-day", "")
        if start_date_year and start_date_month and start_date_day:
            context.startDate = DateTime("%s/%s/%s" % \
                                         (form["startDate-year"],
                                          form["startDate-month"],
                                          form["startDate-day"])
                                         )

        completion_date_year = form.get("completionDate-year", "")
        completion_date_month = form.get("completionDate-month", "")
        completion_date_day = form.get("completionDate-day", "")
        if completion_date_year and completion_date_month \
               and completion_date_day:
            context.completionDate = DateTime("%s/%s/%s" % \
                                              (form["completionDate-year"],
                                           form["completionDate-month"],
                                           form["completionDate-day"])
                                          )

        workflow_action = form.get("workflow_action", None)
        # FIXME only reindex when something has changed
        context.reindexObject()
        if workflow_action:
            wft.doActionFor(context, workflow_action)
        if form:
            # Reload the page, clearing the form
            self.request.response.redirect(context.absolute_url())
        else:
            return self.template()

    def date_input_widget(self, name):
        z2.switch_on(self)
        widget = DateWidget(self.request)
        widget.name = name
        widget.id = name
        context = self.context
        date = getattr(context, name)
        if date:
            widget.value = (date.year(), date.month(), date.day())
        widget.show_today_link = True
        widget.ignoreContext = False
        widget.update()
        return widget.render()
