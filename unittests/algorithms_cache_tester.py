# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case
from pygccxml import parser
from pygccxml import declarations
from pygccxml import utils


class algorithms_cache_tester_t(parser_test_case.parser_test_case_t):
    # tester source reader
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'core_membership.hpp'
        self.global_ns = None

    def setUp(self):
        decls = parser.parse([self.header], self.config)
        self.global_ns = declarations.get_global_namespace(decls)

    def test_name_based(self):
        cls = self.global_ns.class_(name='class_for_nested_enums_t')

        if "CastXML" in utils.xml_generator:
            self.assertRaises(Exception, lambda: cls.cache.demangled_name)
        elif "GCCXML" in utils.xml_generator:
            self.assertTrue(cls.cache.demangled_name == cls.name)

        cls_full_name = declarations.full_name(cls)
        self.assertTrue(cls.cache.full_name == cls_full_name)

        cls_declaration_path = declarations.declaration_path(cls)
        self.assertTrue(cls.cache.declaration_path == cls_declaration_path)

        enum = cls.enum('ENestedPublic')

        enum_full_name = declarations.full_name(enum)
        self.assertTrue(enum.cache.full_name == enum_full_name)

        enum_declaration_path = declarations.declaration_path(enum)
        self.assertTrue(enum.cache.declaration_path == enum_declaration_path)

        # now we change class name, all internal decls cache should be cleared
        cls.name = "new_name"
        self.assertTrue(not cls.cache.full_name)
        if "GCCXML" in utils.xml_generator:
            self.assertTrue(not cls.cache.demangled_name)
        self.assertTrue(not cls.cache.declaration_path)

        self.assertTrue(not enum.cache.full_name)
        if "GCCXML" in utils.xml_generator:
            self.assertTrue(not enum.cache.demangled_name)
        self.assertTrue(not enum.cache.declaration_path)

    def test_access_type(self):
        cls = self.global_ns.class_(name='class_for_nested_enums_t')
        enum = cls.enum('ENestedPublic')
        self.assertTrue(enum.cache.access_type == 'public')
        enum.cache.reset_access_type()
        self.assertTrue(not enum.cache.access_type)
        self.assertTrue('public' == cls.find_out_member_access_type(enum))
        self.assertTrue(enum.cache.access_type == 'public')


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(algorithms_cache_tester_t))

    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
