#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.common.framework import LambdaApiFramework
from functions.repository.messages_repository import MessagesRepository


class ApiHandler(LambdaApiFramework):

    def __init__(self):
        super().__init__()

    def controller(self, query_strings=None, body=None, path_params=None):
        message = body.get("message")
        messages = MessagesRepository.get_message_by_user_id(self.user_id)
        if len(messages) > 10:
            statusCode = 200
            body = {
                "message": "reached the limit of messages, number of messages : limit = 10"
            }
        else:
            _ = MessagesRepository.post_message(self.user_id, message)
            statusCode = 201
            body = {
                "message": "created"
            }
        return statusCode, body


def lambda_handler(event, context):
    valid_rules = {
        "body": {
            "message": {
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
