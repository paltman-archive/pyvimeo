import unittest
import doctest

suite = unittest.TestSuite()

import pyvimeo
import pyvimeo.connection
import pyvimeo.exceptions
import pyvimeo.models
import pyvimeo.config

suite.addTest(doctest.DocTestSuite(pyvimeo))
suite.addTest(doctest.DocTestSuite(pyvimeo.connection))
suite.addTest(doctest.DocTestSuite(pyvimeo.exceptions))
suite.addTest(doctest.DocTestSuite(pyvimeo.models))
suite.addTest(doctest.DocTestSuite(pyvimeo.config))

unittest.TextTestRunner(verbosity=2).run(suite)