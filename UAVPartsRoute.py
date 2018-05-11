#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
from flask_restful import Resource
from flask_restful import reqparse
from flask import Flask, request ,jsonify
from flask import Response,make_response
from UAVManagerDAO import PartsDao,UserDAO
from UAVManagerEntity import Parts

parser = reqparse.RequestParser()
parser.add_argument('parts_id', type=int, location='args')
parser.add_argument('parts_ver',type=str,location='args')
parser.add_argument('parts_type',type=str,location='args')
parser.add_argument('parts_fact',type=str,location='args')
parser.add_argument('parts_date',type=str,location='args')
parser.add_argument('user_team',type=str,location='args')
parser.add_argument('parts_status',type=str,location='args')
parser.add_argument('page_index',type=int,required=True,location='args')
parser.add_argument('page_size',type=int,required=True,location='args')

class UAVPartsList(Resource):
    def __init__(self):
        self.dao = PartsDao()
        self.userDao = UserDAO()

    def post(self):
        if (request.data != ""):
            data = json.loads(request.data)
            token = data['token']
            user = self.userDao.verify_token(token, '')
            if (not user):
                return make_response(jsonify({'error': 'Unauthorized access'}), 401)
            args = parser.parse_args()
            parts_status = args.get('parts_status')
            parts_type = args.get('parts_type')
            page_index = args.get('page_index')
            page_size = args.get('page_size')
            return self.dao.query_condition(user, None, None, parts_type, parts_status, page_index, page_size)
        else:
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)

    def get(self):
        return self.post()

class UAVPartsTypes(Resource):
    def __init__(self):
        self.dao = PartsDao()
        self.userDao = UserDAO()

    def post(self):
        if (request.data != ""):
            data = json.loads(request.data)
            token = data['token']
            user = self.userDao.verify_token(token, '')
            if (not user):
                 return make_response(jsonify({'error': 'Unauthorized access'}), 401)

            rs=self.dao.query_type()
            return rs
        else:
            return  make_response(jsonify({'error': 'Unauthorized access'}), 401)

    def get(self):
        return self.post()

class UAVPartsStatistic(Resource):
    def __init__(self):
        self.dao = PartsDao()
        self.userDao = UserDAO()

    def post(self,parts_status):
        if (request.data != ""):
            data = json.loads(request.data)
            token = data['token']
            user = self.userDao.verify_token(token, '')
            if (not user):
                 return make_response(jsonify({'error': 'Unauthorized access'}), 401)

            rs=self.dao.query_statistic(user,parts_status)
            if rs==-1:
                return make_response(jsonify({'error': 'Unauthorized access'}), 401)
            else:
                return rs
        else:
            return  make_response(jsonify({'error': 'Unauthorized access'}), 401)

    def get(self,parts_status):
        return self.post(parts_status)