#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.common.framework import LambdaApiFramework
from functions.repository.messages_repository import MessagesRepository


class ApiHandler(LambdaApiFramework):

    def __init__(self):
        super().__init__()

    def controller(self, query_strings=None, body=None, path_params=None):
        message_id = body.get("message_id")
        result = MessagesRepository.delete_message_by_message_id(self.user_id, message_id)
        if result:
            statusCode = 200
            body = {
                "message": "success"
            }
        else:
            statusCode = 204
            body = {
                "message": "No content message_id: %s " % message_id
            }
        return statusCode, body


def lambda_handler(event, context):
    valid_rules = {
        "body": {
            "message_id": {
                "required": True,
                "type": "String",
                "rule": {
                    "length": {
                        "upper": 100,
                        "lower": 1
                    }
                }
            }
        }
    }
    ah = ApiHandler()
    return ah.handler(event, valid_rules)
