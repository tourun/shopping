#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import format_date


class Discount(object):
    def __init__(self, expired, percent, category):
        self.expired = format_date(expired)
        if percent <= 0 or percent >= 1:
            raise ValueError('discount should in range (0, 1)')
        self.percent = percent
        self.category = category

    def __hash__(self):
        return hash(self.category)

    def __eq__(self, other):
        return self.category == other.category


class Goods(object):
    category = None

    def __init__(self, name, price, cnt=1):
        self._name = name
        self._price = price
        self._cnt = cnt
        self._discount = None

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def cnt(self):
        return self._cnt

    def set_discount(self, discount):
        self._discount = discount

    def get_discount(self):
        return self._discount

    discount = property(get_discount, set_discount)

    def cal_price(self, date):
        x = self._price * self._cnt
        if self._discount and date <= self._discount.expired:
            x *= self._discount.percent

        return x


class Electronics(Goods):
    category = 'Electronics'

    def __init__(self, name, price, cnt):
        super(Electronics, self).__init__(name, price, cnt)


class Foods(Goods):
    category = 'Foods'

    def __init__(self, name, price, cnt):
        super(Foods, self).__init__(name, price, cnt)


class Commodity(Goods):
    category = 'Commodity'

    def __init__(self, name, price, cnt):
        super(Commodity, self).__init__(name, price, cnt)


class Wine(Goods):
    category = 'Wine'

    def __init__(self, name, price, cnt):
        super(Wine, self).__init__(name, price, cnt)


class Coupon(object):
    def __init__(self, expired, top, sub):
        self.expired = format_date(expired)
        self.expired = expired
        if top < 0 or sub < 0:
            raise ValueError('top and sub should bigger than 0')

        self.top, self.sub = top, sub
