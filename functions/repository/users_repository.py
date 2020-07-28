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

TABLE_NAME = os.environ['env'] + '-' + os.environ['project'] + '-users'

DYNAMODB = boto3.resource('dynamodb', region_name=os.environ['region'])
TABLE_OBJECT = DYNAMODB.Table(TABLE_NAME)


class UsersRepository():

    @staticmethod
    def get_user(user_id):
        if user_id is None:
            return None

        response = TABLE_OBJECT.get_item(
            Key={'user_id': user_id}
        )
        item = response.get('Item')

        if item is None:
            return None
        else:
            return json.loads(json.dumps(item, cls=DecimalEncoder))

    @staticmethod
    def get_user_by_cognito_user_id(cognito_user_id):
        if cognito_user_id is None:
            return None

        response = TABLE_OBJECT.query(
            IndexName='cognito_user_id',
            KeyConditionExpression='cognito_user_id = :cui',
            ExpressionAttributeValues={':cui': cognito_user_id}
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
    def post_user_by_cognito_user_id(cognito_user_id, username, email):
        if cognito_user_id is None:
            return False
        if username is None:
            return False
        if email is None:
            return False

        salt = str(random.randint(1, 1000))
        seed = ".".join([cognito_user_id, email, username, salt])
        user_id = hashlib.sha256(seed.encode()).hexdigest()

        now = datetime.datetime.now(datetime.timezone.utc)
        regist_at = now.strftime("%Y-%m-%dT%H:%M:%S%z")

        try:
            response = TABLE_OBJECT.put_item(
                Item={
                    "user_id": user_id,
                    "cognito_user_id": cognito_user_id,
                    "username": username,
                    "email": email,
                    "updated_at": regist_at,
                    "created_at": regist_at
                })
            LOGGER.info(json.dumps(response, cls=DecimalEncoder))
        except Exception as ex:
            LOGGER.error(ex)
            return None

        return True

    @staticmethod
    def put_user(user_id, user_data):
        if user_id is None:
            return None
        if user_data is None:
            return None

        updated_item = UsersRepository.get_user(user_id)
        if updated_item is None:
            return False

        now = datetime.datetime.now(datetime.timezone.utc)
        updated_at = now.strftime("%Y-%m-%dT%H:%M:%S%z")

        updated_item['username'] = user_data.get('username')
        updated_item['email'] = user_data.get('email')
        updated_item['updated_at'] = updated_at

        try:
            response = TABLE_OBJECT.put_item(Item=updated_item)
            LOGGER.info(json.dumps(response, cls=DecimalEncoder))
        except Exception as ex:
            LOGGER.error(ex)
            return None

        return True

    @staticmethod
    def delete_user(user_id):
        if user_id is None:
            return None

        delete_item = UsersRepository.get_user(user_id)
        if delete_item is None:
            return False

        try:
            response = TABLE_OBJECT.delete_item(
                Key={
                    "user_id": user_id
                }
            )
            LOGGER.info(json.dumps(response, cls=DecimalEncoder))
        except Exception as ex:
            LOGGER.error(ex)
            return None

        return True
