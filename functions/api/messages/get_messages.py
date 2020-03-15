#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.common.framework import LambdaApiFramework
from functions.repository.messages_repository import MessagesRepository

class ApiHandler(LambdaApiFramework):

    def __init__(self):
        super().__init__()

    def controller(self, query_strings=None, body=None, path_params=None):
        messages = MessagesRepository.get_message_by_user_id(self.user_id)
        statusCode = 200
        body ={
            "messages": messages
        }
        return statusCode, body
        

def lambda_handler(event, context):
    ah = ApiHandler()
    return ah.handler(event)
