#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import re
from decimal import Decimal
from traceback import format_exc
from aws_xray_sdk.core import xray_recorder

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class LambdaApiFramework(object):

    user_id = None
    cognito_user_id = None
    email = None

    def __init__(self):
        pass

    @xray_recorder.capture('Validate Boolean')
    def __validate_bool(self, key, val, param_type):
        error = []

        if val not in ["True", "False", "true", "false"]:
            error.append("Invalid type: %s must be Bool, val: %s" % (key, val))

        return error

    @xray_recorder.capture('Validate String')
    def __validate_string(self, key, val, rule):
        error = []

        try:
            str_val = str(val)
        except Exception:
            error.append("Invalid type: %s must be String, val: %s" % (key, val))
            return error

        if rule is not None:
            if 'length' in rule:
                if rule['length']['upper'] < len(str_val):
                    error.append("Invalid length: %s is longer than %d, val: %s" % (key, rule['length']['upper'], str_val))
                elif len(str_val) < rule['length']['lower']:
                    error.append("Invalid length: %s is shorter than %d, val: %s" % (key, rule['length']['lower'], str_val))

            # TODO: Not tested
            if 'regex' in rule:
                match = re.fullmatch(rule['regex'], str_val)
                if match is not None:
                    error.append("Invalid regex: %s is not matched to regex[%s], val: %s" % (key, rule['regex'], str_val))

        return error

    @xray_recorder.capture('Validate Int')
    def __validate_int(self, key, val, rule):
        error = []

        try:
            int_val = int(val)
        except Exception:
            error.append("Invalid type: %s must be Int, val: %s" % (key, val))
            return error

        if rule is not None:
            if 'range' in rule:
                LOGGER.info(json.dumps(rule['range'], ensure_ascii=False))
                if rule['range']['upper'] < int_val:
                    error.append("Invalid range: %s is more than %d, val: %d" % (key, rule['range']['upper'], int_val))
                elif int_val < rule['range']['lower']:
                    error.append("Invalid range: %s is less than %d, val: %d" % (key, rule['range']['lower'], int_val))

        return error

    @xray_recorder.capture('Validate Float')
    def __validate_float(self, key, val, rule):
        error = []

        try:
            float_val = float(val)
        except Exception:
            error.append("Invalid type: %s must be Float, val: %s" % (key, val))
            return error

        if rule is not None:
            if 'range' in rule:
                if rule['range']['upper'] < float_val:
                    error.append("Invalid range: %s is more than %d, val: %d" % (key, rule['range']['upper'], float_val))
                elif float_val < rule['range']['lower']:
                    error.append("Invalid range: %s is less than %d, val: %d" % (key, rule['range']['lower'], float_val))

        return error

    @xray_recorder.capture('Validate List')
    def __validate_list(self, key, val, rule, param_type):
        error = []
        if isinstance(val, list) is False:
            error.append("Invalid type: %s must be List" % key)
            return error

        if rule is None:
            return error

        element_validation = rule.get('elements')
        if element_validation:
            for item in val:
                error.extend(self.__validate_data(item, element_validation, param_type))

        return error

    @xray_recorder.capture('Validate Dict')
    def __validate_dict(self, key, val, rule, param_type):
        error = []
        if isinstance(val, dict) is False:
            error.append("Invalid type: %s must be Dict" % val)
            return error

        if rule is None:
            return error

        keys = rule.get('keys')
        if keys:
            error.extend(self.__validate_data(val, keys, param_type))

        return error

    @xray_recorder.capture('Validate')
    def __validate(self, datas, valid_rules, param_type):

        LOGGER.info("validation : %s", param_type)

        error = []
        errors = []

        rules = valid_rules.get(param_type)
        if rules is None:
            LOGGER.warning("validation rules are not set.")
            return errors

        if datas is None:
            for key in rules.keys():
                rule = rules.get(key)
                LOGGER.info("key: %s", key)
                LOGGER.info(json.dumps(rule, ensure_ascii=False))

                required = rule.get('required')
                LOGGER.info(required)
                if required is not None and required is True:
                    error.append("required parameter: %s is required" % key)

            if error:
                LOGGER.info('validation error : Data is not specified.')
                LOGGER.warning(json.dumps(error, ensure_ascii=False))
                errors.extend(error)
        else:
            errors.extend(self.__validate_data(datas, rules, param_type))

        if errors:
            LOGGER.info("validation failed.")
            LOGGER.warning(json.dumps(errors, ensure_ascii=False))
        else:
            LOGGER.info("all validation passed.")

        return errors

    @xray_recorder.capture('Set Default Values')
    def __set_defalut(self, datas, valid_rules, param_type):

        LOGGER.info("set default : %s", param_type)

        rules = valid_rules.get(param_type)
        if rules is None:
            LOGGER.warning("validation rules are not set.")
            return datas

        if datas is None:
            new_datas = {}
        else:
            new_datas = datas

        for key in rules.keys():
            rule = rules.get(key)
            LOGGER.info("key: %s", key)
            LOGGER.info(json.dumps(rule))

            val = new_datas.get(key)
            if val is not None:
                LOGGER.info("val is set : %s, %s", key, val)
                continue

            default_val = rule.get('default')
            if default_val is not None:
                new_datas[key] = default_val
                LOGGER.info("set default: %s, %s", key, default_val)
            else:
                LOGGER.info("No default rule is set : %s", key)

        return new_datas

    def __validate_data(self, datas, rules, param_type):
        error = []
        errors = []

        for key in rules.keys():
            rule = rules.get(key)
            LOGGER.info("key: %s", key)
            LOGGER.info(json.dumps(rule, ensure_ascii=False))

            val = datas.get(key)
            if val is None:
                required = rule.get('required')
                if required is True:
                    error.append("required parameter: %s is required" % key)
                else:
                    LOGGER.info('validation skip: ( %s , %s )', key, val)
                    continue

            if not error:
                rule_type = rule.get('type')
                if rule_type:
                    if rule_type == "Bool":
                        error = self.__validate_bool(key, val, param_type)
                    elif rule_type == "String":
                        error = self.__validate_string(
                            key, val, rule.get('rule'))
                    elif rule_type == "Int":
                        error = self.__validate_int(
                            key, val, rule.get('rule'))
                    elif rule_type == "Float":
                        error = self.__validate_float(
                            key, val, rule.get('rule'))
                    elif rule_type == "List":
                        error = self.__validate_list(
                            key, val, rule.get('rule'), param_type)
                    elif rule_type == "Dict":
                        error = self.__validate_dict(key, val, rule, param_type)
                else:
                    LOGGER.warning('type of rule is not set.')

            if error:
                LOGGER.info('validation error : ( %s , %s )', key, val)
                LOGGER.warning(json.dumps(error, ensure_ascii=False))
                errors.extend(error)
                error = []
            else:
                LOGGER.info('validation passed : ( %s , %s )', key, val)

        return errors

    def controller(self, query_strings=None, body=None, path_params=None):
        LOGGER.warning("controller is not implemented.")
        return 200, {"message": "controller is not implemented."}

    @xray_recorder.capture('Create Response')
    def __response(self, status_code=200, body=None):
        if body is None:
            body = {"message": "default response"}

        if status_code in (200, 201):
            body["status"] = "success"
        else:
            body["status"] = "failure"

        response = {
            "statusCode": status_code,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            "body": json.dumps(body, ensure_ascii=False, default=self.__dump_unsupported_types)
        }
        LOGGER.info(json.dumps(response, ensure_ascii=False))
        return response

    @xray_recorder.capture('Dump Unsupported Type')
    def __dump_unsupported_types(self, obj):
        if isinstance(obj, Decimal):
            if int(obj) == obj:
                return int(obj)
            return float(obj)

        try:
            return str(obj)
        except Exception:
            return None

    @xray_recorder.capture('Handler')
    def handler(self, event, valid_rules=None):

        LOGGER.info(json.dumps(event, ensure_ascii=False))

        try:
            # Get user info from requestContext
            self.email = event.get('requestContext').get('authorizer').get('email')
            self.cognito_user_id = event.get('requestContext').get('authorizer').get('cognito_user_id')
            self.user_id = self.cognito_user_id
            # TODO: Must check user_id exists or not

            # Get request parameters
            query_strings = event.get('queryStringParameters')
            path_params = event.get('pathParameters')
            body_json = event.get('body')
            if body_json is not None:
                body = json.loads(body_json)
            else:
                body = None

            # validate request parameters
            errors = []
            if valid_rules is not None:
                rules = valid_rules.get('queryString')
                if rules is not None or query_strings is not None:
                    errors.extend(self.__validate(query_strings, valid_rules, 'queryString'))
                rules = valid_rules.get('body')
                if rules is not None or body is not None:
                    errors.extend(self.__validate(body, valid_rules, 'body'))
                rules = valid_rules.get('pathParams')
                if rules is not None or path_params is not None:
                    errors.extend(self.__validate(path_params, valid_rules, 'pathParams'))
            else:
                LOGGER.warning("validation rules are not set.")

            if not errors:
                # set default val
                if valid_rules is not None:
                    rules = valid_rules.get('queryString')
                    if rules is not None or query_strings is not None:
                        query_strings = self.__set_defalut(query_strings, valid_rules, 'queryString')

                    rules = valid_rules.get('body')
                    if rules is not None or body is not None:
                        body = self.__set_defalut(body, valid_rules, 'body')

                    rules = valid_rules.get('pathParams')
                    if rules is not None or path_params is not None:
                        path_params = self.__set_defalut(path_params, valid_rules, 'pathParams')

                # handle request
                xray_recorder.begin_subsegment('Controller')
                status_code, response_body = self.controller(query_strings, body, path_params)
                xray_recorder.end_subsegment()
            else:
                status_code = 400
                response_body = {
                    "message": "Invalid parameters",
                    "errors": errors
                }

        except Exception as ex:
            LOGGER.error(ex)
            LOGGER.error(format_exc())
            status_code = 500
            response_body = {"message": "Internal server error occurs"}

        return self.__response(status_code, response_body)
