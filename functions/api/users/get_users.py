#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.common.framework import LambdaApiFramework
from functions.repository.users_repository import UsersRepository

class ApiHandler(LambdaApiFramework):

    def __init__(self):
        super().__init__()

    def controller(self, query_strings=None, body=None, path_params=None):
        data = UsersRepository.get_user_by_cognito_user_id(self.cognito_user_id)
        statusCode = 200
        body ={
            "data": data
        }
        return statusCode, body
        

def lambda_handler(event, context):
    ah = ApiHandler()
    return ah.handler(event)
