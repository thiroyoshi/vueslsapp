# -*- coding: utf-8 -*-
import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    # pylintのバグ
    # https://github.com/PyCQA/pylint/issues/414
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            return int(o)
        return super(DecimalEncoder, self).default(o)