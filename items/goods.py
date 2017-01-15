#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import format_date, CATEGORY_CHN2ENG


class Descriptor(object):
    """
    描述符基类
    """
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self

        return instance.__dict__[self.name]

    def __set__(self):
        pass


class Date(Descriptor):
    """
    日期描述符，校验日期格式
    """
    def __set__(self, instance, value):
        if instance is None:
            return self

        date = format_date(value)
        instance.__dict__[self.name] = date


class Price(Descriptor):
    """
    价格描述符，校验价格
    """
    def __set__(self, instance, value):
        if instance is None:
            return self

        # if '.' in value and all([x.isdigit() for x in value.split('.')]) \
        #     or value.isdigit():
        #     setattr(instance, self.name, float(value))
        try:
            v = float(value)
        except:
            raise TypeError("价格类型输入[%s]有误，请输入浮点数" % value)

        if v <= 0.0:
            raise ValueError("价格[%s]不能为负数" % value)

        instance.__dict__[self.name] = v


class Percent(Descriptor):
    """
    折扣描述符，校验折扣
    """
    def __set__(self, instance, value):
        if instance is None:
            return self

        try:
            v = float(value)
        except:
            raise TypeError("折扣输入[%s]有误，请输入浮点数" % value)

        if not 0.0 < v <= 1.0:
            raise ValueError("折扣值[%s]区间为(0, 1]" % value)

        instance.__dict__[self.name] = v


class Positive(Descriptor):
    """
    自然数描述符，校验商品个数
    """
    def __set__(self, instance, value):
        if instance is None:
            return self

        if not value.isdigit():
            raise TypeError("商品數量[%s]输入有误，请输入自然数" % value)
        if int(value) < 0:
            raise ValueError("商品个数[%s]要求为自然数" % value)

        instance.__dict__[self.name] = int(value)


class Category(Descriptor):
    """
    商品类别描述符，校验商品类别
    """
    def __set__(self, instance, value):
        if instance is None:
            return self

        if value not in CATEGORY_CHN2ENG:
            raise ValueError("产品类别输入有误[%s]" % value)

        instance.__dict__[self.name] = CATEGORY_CHN2ENG[value]


class Discount(object):
    """
    折扣类
    """
    expired = Date("date")
    percent = Percent("percent")
    category = Category("category")

    def __init__(self, expired, percent, category):
        self.expired = expired
        self.percent = percent
        self.category = category

    def __hash__(self):
        return hash(self.category)

    def __eq__(self, other):
        return self.category == other.category


class Coupon(object):
    """
    优惠券类 top表示消费价格 sub表示优惠价格
    """
    top = Price("top")
    sub = Price("sub")
    expired = Date("expired")

    def __init__(self, expired, top, sub):
        self.expired = expired
        self.top, self.sub = top, sub


class Goods(object):
    """
    商品基类
    """
    category = None
    price = Price("price")
    cnt = Positive("positive")

    def __init__(self, name, price, cnt=1):
        self.name = name
        self.price = price
        self.cnt = cnt
        self._discount = None

    def __eq__(self, rhs):
        return self.name == rhs.name

    def set_discount(self, discount):
        self._discount = discount

    def get_discount(self):
        return self._discount

    discount = property(get_discount, set_discount)

    def cal_price(self, date):
        x = self.price * self.cnt
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

