from zope.i18nmessageid import MessageFactory
ContentItemPortletMessageFactory = MessageFactory('collective.portlet.contentitem')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
