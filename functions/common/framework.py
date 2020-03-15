#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import logging
from functions.repository.users_repository import UsersRepository

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class LambdaApiFramework(object):
    
    user_id = None
    cognito_user_id = None
    email = None

    def __init__(self):
        pass

    def validate_String(self, key, val, rule):
        error = []

        try:
            str_val = str(val)
        except:
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

    def validate_Int(self, key, val, rule):
        error = []

        try:
            int_val = int(val)
        except:
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

    def validate_Float(self, key, val, rule):
        error = []

        try:
            float_val = float(val)
        except:
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

    def validate_List(self, key, val, rule):
        error = []
        if isinstance(val, list) is False:
            error.append("Invalid type: %s must be List" % key)
            return error

        if rule is not None:
            pass

        return error

    def validate_Dict(self, key, val, rule):
        error = []
        if isinstance(val, dict) is False:
            error.append("Invalid type: %s must be Dict" % val)
            return error

        if rule is not None:
            pass

        return error


    def validate(self, datas, valid_rules, param_type):
        errors = []
        rules = valid_rules.get(param_type)
        if rules is None:
            LOGGER.warn("validation rules are not set.")
            return errors

        for key in rules.keys():
            val = datas.get(key)
            if val is None:
                LOGGER.info('validation skip: ( %s , %s )' % (key, val))
                continue

            rule = rules.get(key)
            LOGGER.info(json.dumps(rule))
            rule_type = rule.get('type')
            if rule_type:
                if rule_type == "String":
                    error = self.validate_String(key, val, rule.get('rule'))
                elif rule_type == "Int":
                    error = self.validate_Int(key, val, rule.get('rule'))
                elif rule_type == "Float":
                    error = self.validate_Float(key, val, rule.get('rule'))
                elif rule_type == "List":
                    error = self.validate_List(key, val, rule.get('rule'))
                elif rule_type == "Dict":
                    error = self.validate_Dict(key, val, rule.get('rule'))
            else:
                LOGGER.warn('type of rule is required.')

            if error:
                LOGGER.info('validation error : ( %s , %s )' % (key, val))
                LOGGER.warn(json.dumps(error))
                errors.extend(error)
            else:
                LOGGER.info('validation passed : ( %s , %s )' % (key, val))

        if errors:
            LOGGER.info("validation failed.")
            LOGGER.warn(json.dumps(errors))
        else: 
            LOGGER.info("validation passed.")

        return errors



    def controller(self, query_strings=None, body=None, path_params=None):
        LOGGER.warn("controller is not implemented.")
        return 200, {"message": "controller is not implemented."}


    def response(self, statusCode=200, body={"message": "default response"}):
        response = {
            "statusCode": statusCode,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            "body": json.dumps(body)
        }
        LOGGER.info(json.dumps(response))
        return response


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
            if query_strings is not None:
                LOGGER.info("validation : queryStringParameters")
                errors.extend(self.validate(query_strings, valid_rules, 'query_string'))
            if body is not None:
                LOGGER.info("validation : body")
                errors.extend(self.validate(body, valid_rules, 'body'))
            if path_params is not None:
                LOGGER.info("validation : pathParameters")
                errors.extend(self.validate(path_params, valid_rules, 'path_params'))

            if not errors:
                statusCode, response_body = self.controller(query_strings, body, path_params)
            else:
                statusCode = 400
                response_body = {
                    "message": "Invalid parameters",
                    "errors": errors 
                }

        except Exception as ex:
            LOGGER.error(ex)
            statusCode = 500
            response_body = {
                "message": "Internal server error occurs"
            }

        return self.response(statusCode, response_body)
