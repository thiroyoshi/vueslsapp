#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.common.framework import LambdaApiFramework
from functions.repository.users_repository import UsersRepository


class ApiHandler(LambdaApiFramework):

    def __init__(self):
        super().__init__()

    def controller(self, query_strings=None, body=None, path_params=None):
        username = body.get("username")
        email = body.get("email")
        _ = UsersRepository.post_user_by_cognito_user_id(self.cognito_user_id, username, email)
        statusCode = 201
        body = {
            "message": "created"
        }
        return statusCode, body


def lambda_handler(event, context):
    valid_rules = {
        "body": {
            "username": {
                "required": True,
                "type": "String",
                "rule": {
                    "length": {
                        "upper": 30,
                        "lower": 1
                    }
                }
            },
            "email": {
                "required": True,
                "type": "String",
                "rule": {
                    "length": {
                        "upper": 50,
                        "lower": 1
                    }
                }
            }
        }
    }
    ah = ApiHandler()
    return ah.handler(event, valid_rules)
