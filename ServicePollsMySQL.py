from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.Silva.helpers import add_and_edit

from interfaces import IServicePolls

from sqldb import SQLDB
import _mysql_exceptions

class ServicePollsMySQL(SimpleItem):
    """Service that manages poll data"""

    security = ClassSecurityInfo()
    __implements__ = IServicePolls
    meta_type = 'Silva Service Polls MySQL'

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def manage_afterAdd(self, *a, **kw):
        ServicePollsMySQL.inheritedAttribute('manage_afterAdd')(self, *a, **kw)
        self._init_db()

    def _init_db(self):
        db = self._get_db()
        try:
            db.getSQLData(self, u'SELECT * FROM question')
        except _mysql_exceptions.ProgrammingError:
            self._create_tables(db)

    def _create_tables(self, db):
        db.getSQLData(self, (
            u"""CREATE TABLE question ("""
                """id BIGINT NOT NULL AUTO_INCREMENT, """
                """question TEXT NOT NULL, """
                """PRIMARY KEY (id))"""))
        db.getSQLData(self, (
            u"""CREATE TABLE answer ("""
                """id BIGINT NOT NULL AUTO_INCREMENT, """
                """qid BIGINT NOT NULL, """
                """answer TEXT NOT NULL, """
                """votes BIGINT DEFAULT 0 NOT NULL, """
                """PRIMARY KEY(id), """
                """INDEX(qid))"""))

    def create_question(self, question, answers):
        db = self._get_db()
        db.getSQLData(self, 
            u"INSERT INTO question (question) VALUES ('%(question)s')",
            {'question': question})
        idres = db.getSQLData(self, u'SELECT LAST_INSERT_ID() as id')
        id = idres[0]['id']
        for answer in answers:
            db.getSQLData(self,
                (u"INSERT INTO answer (qid, answer) VALUES (%(qid)s, "
                    "'%(answer)s')"),
                {'qid': id,
                    'answer': answer})
        return id

    def get_question(self, qid):
        db = self._get_db()
        res = db.getSQLData(self,
                u'SELECT * FROM question WHERE id=%(id)s', {'id': qid})
        return res[0]['question']

    def get_answers(self, qid):
        db = self._get_db()
        res = db.getSQLData(self,
                u'SELECT answer FROM answer WHERE qid=%(id)s', {'id': qid})
        return [r['answer'] for r in res]

    def get_votes(self, qid):
        db = self._get_db()
        res = db.getSQLData(self,
                u'SELECT votes FROM answer WHERE qid=%(id)s', {'id': qid})
        return [int(r['votes']) for r in res]

    def save(self, qid, question, answers):
        db = self._get_db()
        db.getSQLData(self,
                u"UPDATE question SET question='%(question)s' WHERE id=%(id)s",
                {'question': question, 'id': qid})
        # this is kinda nasty: first get the ids of the answers, then (in 
        # order!) update the rows
        res = db.getSQLData(self,
                u"SELECT id FROM answer WHERE id=%(id)s", {'id': qid})
        for i, id in enumerate([r['id'] for r in res]):
            db.getSQLData(self,
                u"UPDATE answer SET answer='%(answer)s' where id=%(id)s",
                {'id': id, 'answer': answers[i]})

    def vote(self, qid, index):
        # kinda nasty too, similar problem: we first get all answer rows to
        # find out what answer has index <index>, then do the update
        db = self._get_db()
        res = db.getSQLData(self,
                u"SELECT id, votes FROM answer WHERE qid=%(id)s", {'id': qid})
        idvotes = [(r['id'], int(r['votes'])) for r in res]
        idvotesindex = idvotes[index]
        db.getSQLData(self,
                u"UPDATE answer SET votes=%(votes)s WHERE id=%(id)s",
                {'id': idvotesindex[0], 'votes': idvotesindex[1] + 1})

    def _get_db(self):
        return SQLDB('service_polls_mysqldb')

InitializeClass(ServicePollsMySQL)

manage_addServicePollsForm = PageTemplateFile('www/servicePollsAdd', globals(),
                                        __name__='manage_addServicePollsForm')

def manage_addServicePolls(self, id, title='', REQUEST=None):
    """add service to the ZODB"""
    id = self._setObject(id, ServicePollsMySQL(id, unicode(title, 'UTF-8')))
    add_and_edit(self, id, REQUEST)
    return ''