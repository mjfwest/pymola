#!/usr/bin/env python
"""
Modelica parse Tree to AST tree.
"""
from __future__ import print_function, absolute_import, division, unicode_literals

import os
import glob
import unittest
import itertools

import logging
import casadi as ca
import numpy as np

import pymola.backends.casadi.generator as gen_casadi
from pymola.backends.casadi.model import Model, Variable
from pymola.backends.casadi.api import transfer_model, CachedModel
from pymola import parser, ast

loggerpy = logging.getLogger("pymola")
loggerpy.setLevel(logging.INFO)

logging.basicConfig(format='%(name)s - %(asctime)s %(levelname)s %(message)s')

TEST_DIR = os.path.dirname(os.path.realpath(__file__))

db_file = os.path.join(TEST_DIR, 'BigModel')
try:
    os.remove(db_file)
except:
    pass

for f in glob.glob(os.path.join(TEST_DIR, "BigModel*.so")):
    os.remove(f)
for f in glob.glob(os.path.join(TEST_DIR, "BigModel*.dll")):
    os.remove(f)
for f in glob.glob(os.path.join(TEST_DIR, "BigModel*.dylib")):
    os.remove(f)

# Create model, cache it, and load the cache
compiler_options = \
    {'cache': True,
     'detect_aliases': True,
     'replace_constant_values': True,
     'replace_constant_expressions': True,
     'replace_parameter_values': True,
     'replace_parameter_expressions': True,
     'eliminate_constant_assignments': True,
     'reduce_affine_expression': True
    }

ref_model = transfer_model(TEST_DIR, 'BigModel', compiler_options)

# Load from cache:
# cached_model = transfer_model(TEST_DIR, 'BigModel', compiler_options)
