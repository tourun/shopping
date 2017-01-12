#!/usr/bin/env python
# -*- coding: utf-8 -*-

import goods

all_products = {
    'Electronics': ['ipad', 'iphone', '显示器', '笔记本电脑', '键盘'],
    'Foods': ['面包', '饼干', '蛋糕', '牛肉', '鱼', '蔬菜'],
    'Commodity': ['餐巾纸', '收纳箱', '咖啡杯', '雨伞'],
    'Wine': ['啤酒', '白酒', '伏特加']
}


def format_date(string):
    date = string.split('.')
    if len(date) != 3:
        raise ValueError('date format error: %s' % string)
    return '%s.%02s.%02s' % (date[0], date[1], date[2])


def new_goods(name, price, cnt):
    for kind, products in all_products.iteritems():
        if name in products:
            cls = getattr(goods, kind, None)
            return cls(name, float(price), int(cnt)) if cls else None

    return None
