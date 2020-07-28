#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import logging
from pylibs.aws_xray_sdk.core import xray_recorder
from functions.repository.users_repository import UsersRepository

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class LambdaApiFramework(object):

    user_id = None
    cognito_user_id = None
    email = None

    def __init__(self):
        pass

    @xray_recorder.capture('Validate Boolean')
    def __validate_bool(self, val):
        error = []

        if type(val) != bool:
            error.append("Invalid type: %s must be Boolean, val: %s", val)

        return error

    @xray_recorder.capture('Validate String')
    def __validate_string(self, key, val, rule):
        error = []

        try:
            str_val = str(val)
        except Exception as ex:
            LOGGER.error(ex)
            error.append("Invalid type: %s must be String, val: %s" % (key, val))
            return error

        # if isinstance(str_val, str) is False:
        #     error['type'] = "Invalid type: %s must be String" % val
        #     return error

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
        except Exception as ex:
            LOGGER.error(ex)
            error.append("Invalid type: %s must be Int, val: %s" % (key, val))
            return error

        # if isinstance(int_val, int) is False:
        #     error['type'] = "Invalid type: %s must be Int" % val 
        #     return error

        if rule is not None:
            if 'range' in rule:
                LOGGER.info(json.dumps(rule['range']))
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
        except Exception as ex:
            LOGGER.error(ex)
            error.append("Invalid type: %s must be Float, val: %s" % (key, val))
            return error

        # if isinstance(val, float) is False:
        #     error['type'] = "Invalid type: %s must be Float" % val
        #     return error

        if rule is not None:
            if 'range' in rule:
                if rule['range']['upper'] < float_val:
                    error.append("Invalid range: %s is more than %d, val: %d" % (key, rule['range']['upper'], float_val))
                elif float_val < rule['range']['lower']:
                    error.append("Invalid range: %s is less than %d, val: %d" % (key, rule['range']['lower'], float_val))

        return error

    @xray_recorder.capture('Validate List')
    def __validate_list(self, key, val, rule):
        error = []
        if isinstance(val, list) is False:
            error.append("Invalid type: %s must be List" % key)
            return error

        if rule is not None:
            pass

        return error

    @xray_recorder.capture('Validate Dict')
    def __validate_dict(self, key, val, rule):
        error = []
        if isinstance(val, dict) is False:
            error.append("Invalid type: %s must be Dict" % val)
            return error

        if rule is not None:
            pass

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
                required = rules.get(key).get('required')
                if required is None:
                    continue
                if required is True:
                    error.append("required parameter: %s is required" % key)

            if error:
                LOGGER.info("validation failed.")
                LOGGER.warning(json.dumps(error))
            else:
                LOGGER.info("validation skipped. No data is specified.")

            return error

        else:
            for key in rules.keys():
                rule = rules.get(key)
                LOGGER.info("key: %s", key)
                LOGGER.info(json.dumps(rule))

                val = datas.get(key)
                if val is None:
                    required = rule.get('required')
                    if required is None:
                        LOGGER.info('validation skipped. No data is specified: %s', key)
                        continue
                    if required is True:
                        error.append("required parameter: %s is required" % key)

                if not error:
                    rule_type = rule.get('type')
                    if rule_type:
                        if rule_type == "Bool":
                            error = self.__validate_bool(val)
                        elif rule_type == "String":
                            error = self.__validate_string(key, val, rule.get('rule'))
                        elif rule_type == "Int":
                            error = self.__validate_int(key, val, rule.get('rule'))
                        elif rule_type == "Float":
                            error = self.__validate_float(key, val, rule.get('rule'))
                        elif rule_type == "List":
                            error = self.__validate_list(key, val, rule.get('rule'))
                        elif rule_type == "Dict":
                            error = self.__validate_dict(key, val, rule.get('rule'))
                    else:
                        LOGGER.warning('type of rule is not set.')

                if error:
                    LOGGER.info('validation error : ( %s , %s )', key, val)
                    LOGGER.warning(json.dumps(error))
                    errors.extend(error)
                    error = []
                else:
                    LOGGER.info('validation passed : ( %s , %s )', key, val)

        if errors:
            LOGGER.info("validation failed.")
            LOGGER.warning(json.dumps(errors))
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
                continue

            default_val = rule.get('default')
            if default_val is not None:
                new_datas[key] = default_val
                LOGGER.info("set default: %s, %s", key, default_val)
            else:
                LOGGER.info("No default rule is set : %s", key)

        return new_datas

    def controller(self, query_strings=None, body=None, path_params=None):
        LOGGER.warning("controller is not implemented.")
        return 200, {"message": "controller is not implemented."}

    @xray_recorder.capture('Create Response')
    def __response(self, status_code=200, body=None):
        if body is None:
            body = {"message": "default response"}

        if status_code == 200 or status_code == 201:
            body["status"] = "success"
        else:
            body["status"] = "failure"

        response = {
            "statusCode": status_code,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            "body": json.dumps(body)
        }
        LOGGER.info(json.dumps(response))
        return response

    @xray_recorder.capture('Handler')
    def handler(self, event, valid_rules=None):

        LOGGER.info(json.dumps(event))

        self.email = event.get('requestContext').get('authorizer').get('email')
        self.cognito_user_id = event.get('requestContext').get('authorizer').get('cognito_user_id')

        user_data = UsersRepository.get_user_by_cognito_user_id(self.cognito_user_id)
        LOGGER.info(json.dumps(user_data))
        if user_data is None:
            _ = UsersRepository.post_user_by_cognito_user_id(self.cognito_user_id, self.cognito_user_id, self.email)
        else:
            self.user_id = user_data.get('user_id')

        query_strings = None
        body = None
        path_params = None
        if event['httpMethod'] == 'GET':
            query_strings = event.get('queryStringParameters')
        else:
            body = json.loads(event.get('body'))
            path_params = event.get('pathParameters')

        try:
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
            status_code = 500
            response_body = {
                "message": "Internal server error occurs"
            }

        return self.__response(status_code, response_body)
