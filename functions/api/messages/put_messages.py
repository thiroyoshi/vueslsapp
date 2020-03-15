#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.common.framework import LambdaApiFramework
from functions.repository.messages_repository import MessagesRepository

class ApiHandler(LambdaApiFramework):

    def __init__(self):
        super().__init__()

    def controller(self, query_strings=None, body=None, path_params=None):
        message_id = body.get("message_id")
        message = body.get("message")
        result = MessagesRepository.put_message(self.user_id, message_id, message)
        if result:
            statusCode = 200
            body ={
                "message": "success"
            }
        else:
            statusCode = 404
            body ={
                "message": "Not Found message_id: %s " % message_id
            }
        return statusCode, body
        

def lambda_handler(event, context):
    valid_rules = {
        "body":{
            "message_id" : {
                "type" : "String"
            },
            "message" : {
                "type" : "String",
                "rule" : {
                    "length" : {
                        "upper" : 100,
                        "lower" : 1
                    }
                }
            }
        }
    }
    ah = ApiHandler()
    return ah.handler(event, valid_rules)
