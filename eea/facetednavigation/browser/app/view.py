""" Faceted views
"""
from zope.component import getUtility
from zope.component import queryAdapter
from zope.schema.interfaces import IVocabularyFactory
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import IFacetedWrapper

class FacetedContainerView(object):
    """ Faceted view
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def language_present(self):
        """ Is there any widget for Language index?
        """
        criteria = ICriteria(self.context)
        for criterion in criteria.values():
            if criterion.get('index', None) == 'Language':
                if not criterion.hidden:
                    return True
        return False

    @property
    def positions(self):
        """ Return available columns
        """
        voc = getUtility(IVocabularyFactory,
                         'eea.faceted.vocabularies.WidgetPositions')
        return voc(self.context)

    def get_context(self, content=None):
        """ Return context
        """
        wrapper = queryAdapter(self.context, IFacetedWrapper)
        if not wrapper:
            return self.context
        return wrapper(content)

    def get_sections(self, position='', mode='view'):
        """ Get sections for given position or return all sections
        """
        voc = getUtility(IVocabularyFactory,
                         'eea.faceted.vocabularies.WidgetSections')
        voc = voc(self.context)
        if not position or mode != 'view':
            return [t for t in voc]

        widgets = self.get_view_widgets(position=position)
        sections = [widget.data.get('section') for widget in widgets]
        return [term for term in voc if term.value in sections]

    def get_view_widgets(self, position='', section=''):
        """ Get not hidden widgets
        """
        widgets = self.get_widgets(position, section)
        for widget in widgets:
            if widget.hidden:
                continue
            yield widget

    def get_widgets(self, position='', section=''):
        """ Get all widgets
        """
        criteria = ICriteria(self.context)
        for criterion in criteria.values():
            if position and criterion.get('position', 'right') != position:
                continue
            if section and criterion.get('section', 'default') != section:
                continue
            widget = criteria.widget(wid=criterion.get('widget'))
            yield widget(self.context, self.request, criterion)
