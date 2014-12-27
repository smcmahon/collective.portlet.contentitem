Introduction
============

collective.portlet.contentitem does something ver simple: it allows you to display some or all of a content item in a portlet.

When you add or edit a content-item portlet, you'll be able to choose the represented content item via a tree browser, just as with the navigation portlet.

Odds are that the template used to render the portlet won't do what you want. Just override it with jbot as collective.portlet.contentitem.contentitemportlet.py.

Available view methods are:

    * view/contentMeta -- returns the content's catalog representation (brain)

    * view/contentObject -- returns the content object itself

    * view/contentURL -- returns the content URL

    * view/contentTitle -- returns the content title

    * view/contentDescription -- returns the content description
