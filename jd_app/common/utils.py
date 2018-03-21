#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/17 上午2:14
import decimal


def format_app_num(num, f=2, is_separate=True):
    if isinstance(num, int) or isinstance(num, long):
        return '{:,}'.format(num) if is_separate else '{:}'.format(num)
    elif num is None:
        return "0"
    elif num is '':
        return "0"
    num = fmt_two_amount(num, f)
    if is_separate:
        result = '{:,}'.format(num)
    else:
        result = '{:}'.format(num)
    return result


def fmt_two_amount(value, f=2):
    if "," in str(value):
        value = value.replace(",", "")
    places = decimal.Decimal(10)**-f
    return decimal.Decimal(value).quantize(places, rounding=decimal.ROUND_DOWN)
