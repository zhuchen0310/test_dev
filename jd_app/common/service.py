#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/17 上午2:55
import functools
import arrow
import copy
from flask_session import Session
from flask import jsonify, session
from .response_code import RET
from run import db, app


class Commons(object):
    def __init__(self):
        self.name = None

    def login_required(self, f):
        """
        验证用户登录的装饰器
        :param f:
        :return:
        """

        # functools让被装饰的函数名称不会改变
        @functools.wraps(f)
        def wrapper(*arges, **kwargs):
            # 从session中获取user_id
            user_id = session.get('user_id')
            if user_id is None:
                return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
            else:
                # 用户已经登录
                g.user_id = user_id
                return f(*arges, **kwargs)

        return wrapper

    @staticmethod
    def now(is_str=False, format="YYYY-MM-DD HH:mm:ss"):
        """
        获取当前时间
        :return:
        """
        now = arrow.now().datetime if not is_str else arrow.now().format(
            format)

        return now

    def str_to_datetime(self, time_str):
        if isinstance(time_str, str):
            datetime = arrow.get(time_str).datetime
        elif isinstance(time_str, int):
            datetime = arrow.get(str(time_str)[::10]).datetime
        else:
            return
        return datetime

    @staticmethod
    def save(obj):
        try:
            with app.app_context():
                db.session.add(obj)
                db.session.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            return obj

    def get_datetime_by_timestamp(self, data):
        """
        递归处理时间戳
        :param data:
        :return:
        """
        year = self.now().year
        data = copy.deepcopy(data)
        datetime = self.str_to_datetime(data)
        if datetime and datetime.year != year and len(data) > 0:
            data = data[:len(data) - 1:]
            datetime = self.get_datetime_by_timestamp(data)
        return datetime
