import py

from question import Question
from dummydb import DB

def test_question():
    question = Question('How are you?', ['good', 'bad', 'whatever'])
    assert question.question == 'How are you?'
    question.vote(0)
    assert question.votes == [1, 0, 0]
    py.test.raises(IndexError, 'question.vote(3)')

def test_db():
    db = DB()
    question1 = Question('How are you?', ['good', 'bad', 'whatever'])
    id1 = db.store(question1)
    q1ret = db.get(id1)
    assert q1ret.question == question1.question
    assert q1ret.answers == question1.answers
    assert q1ret.votes == question1.votes
    q1ret.vote(0)
    assert q1ret.votes == [1, 0, 0]
    db.update(id1, q1ret)
    q1retret = db.get(id1)
    assert q1retret.votes == [1, 0, 0]
