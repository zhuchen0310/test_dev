#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/17 上午2:15
import redis

DB_URI = "mysql://zhuchen:zhuchen@118.24.159.168:3306/jingfen_dev"

SQLALCHEMY_DATABASE_URI = "mysql://zhuchen:zhuchen@118.24.159.168:3306/jingfen_dev"

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'TQ343dfsdf34+SDjjojlje343ET+?#$ODFDSFSD'

# REDIS
REDIS_HOST = "118.24.159.168"
REDIS_PORT = 6379
REDIS_DB = 10

# flask-session 使用参数
SESSION_TYPE = "redis"  # 利用redis 来保存session会话

#
SESSION_USE_SIGNER = True  # 为sesson_id进行签名
SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # redis 缓存设置

#
PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期 秒
