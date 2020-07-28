#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import datetime
import json
import random
import hashlib
from pylibs import boto3
from pylibs.boto3.dynamodb.conditions import Key
from functions.common.decimal_encoder import DecimalEncoder

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

TABLE_NAME = os.environ['env'] + '-' + os.environ['project'] + '-messages'

DYNAMODB = boto3.resource('dynamodb', region_name=os.environ['region'])
TABLE_OBJECT = DYNAMODB.Table(TABLE_NAME)


class MessagesRepository():

    @staticmethod
    def get_message_by_user_id(user_id):
        if user_id is None:
            return None

        response = TABLE_OBJECT.query(
            KeyConditionExpression='user_id = :ui',
            ExpressionAttributeValues={':ui': user_id}
        )
        items = response.get('Items')

        if items is None:
            return None
        else:
            return json.loads(json.dumps(items, cls=DecimalEncoder))

    @staticmethod
    def get_message_by_message_id(user_id, message_id):
        if user_id is None:
            return None
        if message_id is None:
            return None

        response = TABLE_OBJECT.query(
            KeyConditionExpression='user_id = :ui and message_id = :mi',
            ExpressionAttributeValues={
                ':ui': user_id,
                ':mi': message_id,
                }
        )
        items = response.get('Items')
        if len(items) > 0:
            item = items[0]
        else:
            item = None

        if item is None:
            return None
        else:
            return json.loads(json.dumps(item, cls=DecimalEncoder))

    @staticmethod
    def post_message(cognito_user_id, message):
        if cognito_user_id is None:
            return None
        if message is None:
            return None

        salt = str(random.randint(1, 1000))
        seed = ".".join([cognito_user_id, message, salt])
        message_id = hashlib.sha256(seed.encode()).hexdigest()

        now = datetime.datetime.now(datetime.timezone.utc)
        created_at = now.strftime("%Y-%m-%dT%H:%M:%S%z")
        expired_at = int(now.timestamp())

        try:
            response = TABLE_OBJECT.put_item(
                Item={
                    "user_id": cognito_user_id,
                    "message_id": message_id,
                    "message": message,
                    "updated_at": created_at,
                    "created_at": created_at,
                    "expired_at": expired_at
                })
            LOGGER.info(json.dumps(response, cls=DecimalEncoder))
        except Exception as ex:
            LOGGER.error(ex)
            return None

        return True

    @staticmethod
    def put_message(cognito_user_id, message_id, message):
        if cognito_user_id is None:
            return None
        if message_id is None:
            return None
        if message is None:
            return None

        updated_item = MessagesRepository.get_message_by_message_id(cognito_user_id, message_id)
        if updated_item is None:
            return False

        now = datetime.datetime.now(datetime.timezone.utc)
        updated_at = now.strftime("%Y-%m-%dT%H:%M:%S%z")

        updated_item['message'] = message
        updated_item['updated_at'] = updated_at

        try:
            response = TABLE_OBJECT.put_item(Item=updated_item)
            LOGGER.info(json.dumps(response, cls=DecimalEncoder))
        except Exception as ex:
            LOGGER.error(ex)
            return None

        return True

    @staticmethod
    def delete_message_by_message_id(cognito_user_id, message_id):
        if message_id is None:
            return None

        delete_item = MessagesRepository.get_message_by_message_id(cognito_user_id, message_id)
        if delete_item is None:
            return False

        try:
            response = TABLE_OBJECT.delete_item(
                Key={
                    "user_id": cognito_user_id,
                    "message_id": message_id
                }
            )
            LOGGER.info(json.dumps(response, cls=DecimalEncoder))
        except Exception as ex:
            LOGGER.error(ex)
            return None

        return True
