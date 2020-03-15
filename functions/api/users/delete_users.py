#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.common.framework import LambdaApiFramework
from functions.repository.users_repository import UsersRepository

class ApiHandler(LambdaApiFramework):

    def __init__(self):
        super().__init__()

    def controller(self, query_strings=None, body=None, path_params=None):
        result = UsersRepository.delete_user(self.user_id)
        if result:
            statusCode = 200
            body ={
                "message": "success"
            }
        else:
            statusCode = 204
            body ={
                "message": "Not Found cognito_user_id: %s " % self.cognito_user_id
            }
        return statusCode, body
        

def lambda_handler(event, context):
    ah = ApiHandler()
    return ah.handler(event)
