#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.common.framework import LambdaApiFramework
from functions.repository.users_repository import UsersRepository

class ApiHandler(LambdaApiFramework):

    def __init__(self):
        super().__init__()

    def controller(self, query_strings=None, body=None, path_params=None):
        result = UsersRepository.put_user(self.user_id, body)
        if result:
            statusCode = 200
            body ={
                "message": "success"
            }
        else:
            statusCode = 404
            body ={
                "message": "Not Found cognito_user_id: %s " % self.cognito_user_id
            }
        return statusCode, body
        

def lambda_handler(event, context):
    valid_rules = {
        "body":{
            "username" : {
                "type" : "String",
                "rule" : {
                    "length" : {
                        "upper" : 30,
                        "lower" : 1
                    }
                }
            },
            "email" : {
                "type" : "String"
            }
        }
    }
    ah = ApiHandler()
    return ah.handler(event, valid_rules)
