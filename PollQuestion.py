import os
from urlparse import urlparse

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass, package_home
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from OFS.SimpleItem import SimpleItem
from DateTime import DateTime

from Products.Formulator.Form import ZMIForm
from Products.Formulator.XMLToForm import XMLToForm

from Products.Silva.SimpleContent import SimpleContent
from Products.Silva.interfaces import IContent
from Products.Silva import mangle
from Products.Silva.helpers import add_and_edit
from Products.Silva import SilvaPermissions

interfaces = (IContent,)
try:
    from Products.SilvaExternalSources.ExternalSource import ExternalSource
    from Products.SilvaExternalSources.interfaces import IExternalSource
except ImportError:
    class ExternalSource:
        pass
else:
    interfaces = (IContent, IExternalSource)

icon = "www/pollquestion.png"

class OverwriteNotAllowed(Exception):
    """raised when trying to overwrite answers for a used question"""

class ViewableExternalSource(ExternalSource):
    """ExternalSource subclass that has index_html overridden to display the
        external source object's public view as usual
    """

    def index_html(self, *args, **kwargs):
        """this is kinda nasty... copied the index_html Python script to
            avoid having ExternalSources.index_html (which returns the props
            form, not a decent public view, perhaps that should be changed some
            time) 
        """
        content = 'content.html'
        override = 'override.html'
        if hasattr(self.aq_explicit, override):
            renderer = override
        else:
            renderer = content
        self.REQUEST.RESPONSE.setHeader('Content-Type', 
                                            'text/html;charset=utf-8')
        self.REQUEST.RESPONSE.setHeader('Cache-Control','max-age=300')
        return getattr(self, renderer)(view_method='view')

class PollQuestion(SimpleContent, ViewableExternalSource):
    """A poll question of the Silva Poll product"""

    security = ClassSecurityInfo()
    meta_type = 'Silva Poll Question'
    __implements__ = interfaces

    _sql_method_id = 'poll_question'
    _layout_id = 'layout'
    parameters = None

    def __init__(self, id, question, answers):
        PollQuestion.inheritedAttribute('__init__')(self, id,
            '[Title is stored in metadata. This is a bug.]')
        self._question = question
        self._answers = answers
        self.qid = None
        self._init_form()

    def _init_form(self):
        form = ZMIForm('form', 'Properties Form')
        f = open(os.path.join(package_home(globals()), 'www', 
                                'externalSourceForm.form'))
        XMLToForm(f.read(), form)
        f.close()
        self.set_form(form)

    def manage_afterAdd(self, item, container):
        PollQuestion.inheritedAttribute('manage_afterAdd')(self, 
                                                            item, container)
        self.qid = self.service_polls.create_question(self._question, 
                                                        self._answers)

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                              'save')
    def save(self, question, answers, overwrite=False):
        """save question data"""
        votes = self.service_polls.get_votes(self.qid)
        if votes != (len(answers) * [0]) and not overwrite:
            raise OverwriteNotAllowed, self.qid
        self.service_polls.save(self.qid, question, answers)

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'get_OverwriteNotAllowed')
    def get_OverwriteNotAllowed(self):
        return OverwriteNotAllowed

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'get_question')
    def get_question(self):
        """returns a string"""
        return self.service_polls.get_question(self.qid)

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'get_answers')
    def get_answers(self):
        """returns a list of strings"""
        return self.service_polls.get_answers(self.qid)

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'get_votes')
    def get_votes(self):
        """returns a list of ints"""
        return self.service_polls.get_votes(self.qid)

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'manage_vote')
    def manage_vote(self, REQUEST=None):
        if REQUEST is None:
            REQUEST = self.REQUEST
        if not REQUEST or not REQUEST.has_key('answer'):
            return
        answer = REQUEST['answer']
        answers = self.get_answers()
        id = answers.index(answer)
        self.service_polls.vote(self.qid, id)
        REQUEST.RESPONSE.setCookie('voted_cookie_%s' % self.absolute_url(), 
                                    '1', 
                                    expires='Wed, 19 Feb 2020 14:28:00 GMT',
                                    path='/')
        return True

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'has_voted')
    def has_voted(self, REQUEST=None):
        if REQUEST is None:
            REQUEST = self.REQUEST
        return REQUEST.has_key('voted_cookie_%s' % self.absolute_url())

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'start_display_date')
    def start_display_date(self):
        """return the start date/time for displaying the question"""
        return self.service_metadata.getMetadataValue(self, 'silvapolls-date',
                                                      'startdate')

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'end_display_date')
    def end_display_date(self):
        """return the start date/time for displaying the question"""
        return self.service_metadata.getMetadataValue(self, 'silvapolls-date',
                                                      'enddate')

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'display_question')
    def display_question(self):
        """returns True if the question should be displayed, False if not"""
        startdate = self.service_metadata.getMetadataValue(self, 
                  'silvapolls-date', 'startdate')
        enddate = self.service_metadata.getMetadataValue(self,
                  'silvapolls-date', 'enddate')
        now = DateTime()
        return ((startdate and startdate < now) and 
                  (not enddate or enddate > now))

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'display_results')
    def display_results(self):
        """returns True if results should be displayed, False if not"""
        startdate = self.service_metadata.getMetadataValue(self,
                  'silvapolls-date', 'startresultdate')
        enddate = self.service_metadata.getMetadataValue(self,
                  'silvapolls-date', 'endresultdate')
        now = DateTime()
        return ((startdate and startdate < now) and 
                  (not enddate or enddate > now))

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'to_html')
    def to_html(self, REQUEST, **kw):
        """return HTMl for ExternalSource interface"""
        if kw.has_key('display') and kw['display'] == 'link':
            return '<a href="%s">%s</a>' % (self.absolute_url(), 
                                            self.get_title_or_id())
        # XXX is this the expected behaviour? do we want to display a link to
        # the poll instead when the question and results shouldn't be 
        # displayed?
        if not self.display_question() and not self.display_results():
            return ''
        return self.view()

InitializeClass(PollQuestion)

manage_addPollQuestionForm = PageTemplateFile('www/pollQuestionAdd', 
                        globals(), __name__='manage_addPollQuestionForm')

def manage_addPollQuestion(self, id, question, answers, REQUEST=None):
    """add a poll question"""
    if not mangle.Id(self, id).isValid():
        return
    obj = PollQuestion(id, question, answers)
    self._setObject(id, obj)
    obj = getattr(self, id)
    obj.set_title(question)
    add_and_edit(self, id, REQUEST)
    return ''
