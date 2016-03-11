# coding: utf-8
import unittest

from stacker.errors import StackerUndefinedVariable
from stacker.scope import Scope


class TestScope(unittest.TestCase):

    def test_outer_scope(self):
        outer = Scope(None, outer_key=100, inner_key=99)
        inner = Scope(outer, inner_key=50)
        self.assertEqual(inner.find_in_scope('inner_key'), 50)
        self.assertEqual(outer.find_in_scope('inner_key'), 99)

        self.assertEqual(inner.find_in_scope('outer_key'), 100)

    def test_variable_undefined(self):
        scope = Scope(None, variable=100)
        with self.assertRaises(StackerUndefinedVariable):
            scope.find_in_scope('non_existant')



