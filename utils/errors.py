# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0


class UserError(Exception):
    pass


class DatasetNotSelectedError(UserError):
    pass


class InvalidDatasetUrl(UserError):
    pass


class DataSetNotExistsError(UserError):
    pass


class InvalidColumnError(UserError):
    pass


class RequirementUnfulfilledError(UserError):
    pass


class ExistsNaException(UserError):
    pass
