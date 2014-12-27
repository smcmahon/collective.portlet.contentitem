from collective.portlet.contentitem import ContentItemPortletMessageFactory as _
from plone import api
from plone.app.form.validators import null_validator
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
from zope.interface import implements

import zope.event
import zope.lifecycleevent


class IContentItemPortlet(IPortletDataProvider):
    """A portlet
    """

    content_item = schema.Choice(
            title=_(u"label_content_item", default=u"Content Item"),
            description=_(u'help_content_item',
                          default=u"Content item to display in the portlet."),
            required=True,
            source=SearchableTextSourceBinder({}, default_query='path:'))

    content_uid = schema.TextLine(
            title=u"UID",
            required=False,
            )


class Assignment(base.Assignment):
    """Portlet assignment.
    """

    implements(IContentItemPortlet)

    content_item = None
    content_uid = None

    def __init__(self, content_item=None, content_uid=None):
        self.content_item = content_item
        self.content_uid = content_uid

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        catalog = api.portal.get_tool(name='portal_catalog')
        rez = catalog(UID=self.content_uid)
        return "Content-Item %s" % rez[0].Title


class Renderer(base.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('contentitemportlet.pt')

    def __init__(self, context, request, view, manager, data):
        super(Renderer, self).__init__(context, request, view, manager, data)
        catalog = api.portal.get_tool(name='portal_catalog')
        rez = catalog(UID=data.content_uid)
        if rez:
            self.mybrain = rez[0]
        else:
            self.mybrain = None

    def contentMeta(self):
        return self.mybrain.aq_inner

    def contentObject(self):
        return self.mybrain.aq_inner.getObject()

    def contentURL(self):
        return self.mybrain.aq_inner.getURL()

    def contentTitle(self):
        return self.mybrain.Title

    def contentDescription(self):
        return self.mybrain.Description


class AddForm(base.AddForm):
    """Portlet add form.
    """
    form_fields = form.Fields(IContentItemPortlet)
    form_fields["content_item"].custom_widget = UberSelectionWidget
    form_fields = form_fields.omit('content_uid')

    def create(self, data):
        return Assignment(**data)

    @form.action(_(u"label_save", default=u"Save"), name=u'save')
    def handle_save_action(self, action, data):
        data['content_uid'] = api.content.get_uuid(
            obj=api.content.get(path=data['content_item'])
            )
        self.createAndAdd(data)

    @form.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''


class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(IContentItemPortlet)
    form_fields["content_item"].custom_widget = UberSelectionWidget
    form_fields = form_fields.omit('content_uid')

    @form.action(_(u"label_save", default=u"Save"),
                 condition=form.haveInputWidgets,
                 name=u'save')
    def handle_save_action(self, action, data):
        data['content_uid'] = api.content.get_uuid(
            obj=api.content.get(path=data['content_item'])
            )
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            zope.event.notify(zope.lifecycleevent.ObjectModifiedEvent(self.context))
            self.status = "Changes saved"
        else:
            self.status = "No changes"

        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @form.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''
