# -*- coding: utf-8 -*-
# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import unittest

from zope.interface.verify import verifyObject
from Products.SilvaPoll.interfaces import IPollQuestion, IPollQuestionVersion
from Products.SilvaPoll.testing import FunctionalLayer


class QuestionTestCase(unittest.TestCase):
    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('author')

    def test_question(self):
        factory = self.root.manage_addProduct['SilvaPoll']
        factory.manage_addPollQuestion(
            'poll', 'Poll Status',
            question='Does it poll ?', answers=['Yeah baby', 'Well, not really'])
        self.assertTrue('poll' in self.root.objectIds())

        poll = self.root.poll
        self.assertTrue(verifyObject(IPollQuestion, poll))

        version = poll.get_editable()
        self.assertTrue(verifyObject(IPollQuestionVersion, version))

        self.assertEqual(version.get_question(), 'prout ?')
        self.assertEqual(version.get_answers(), [])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(QuestionTestCase))
    return suite
