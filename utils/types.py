# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

from enum import Enum


class ModelType(Enum):
    DecisionTree = 'DecisionTree'


class FillNAMode(Enum):
    Average = 'Average'
    Mode = 'Mode'
    Median = 'Median'
    StaticValue = 'StaticValue'


class EncodeMode(object):
    pass
