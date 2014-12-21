from collective.portlet.contentitem import ContentItemPortletMessageFactory as _
from plone import api
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
from zope.interface import implements


class IContentItemPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    content_item = schema.Choice(
            title=_(u"label_content_item", default=u"Content Item"),
            description=_(u'help_content_item',
                          default=u"Content item to display in the portlet."),
            required=False,
            source=SearchableTextSourceBinder({}, default_query='path:'))

    content_uuid = schema.TextLine(required=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IContentItemPortlet)

    content_item = None

    def __init__(self, content_item=None):
        self.content_item = content_item

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Content-Item Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('contentitemportlet.pt')

    def contentItem(self):
        return self.data.content_item


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IContentItemPortlet)
    form_fields["content_item"].custom_widget = UberSelectionWidget

    def create(self, data):
        # api.content.get_uuid(obj=api.content.get(path=data.content_item))
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IContentItemPortlet)
    form_fields["content_item"].custom_widget = UberSelectionWidget
