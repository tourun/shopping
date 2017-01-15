#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ShoppingCart(object):
    """
    购物车类
    """
    def __init__(self):
        self._shopping_basket = []
        self._coupon = None

    def set_coupon(self, coupon):
        self._coupon = coupon

    def get_coupon(self):
        return self._coupon

    coupon = property(get_coupon, set_coupon)

    def add(self, item):
        self._shopping_basket.append(item)

    def remove(self, item):
        if item in self._shopping_basket:
            self._shopping_basket.remove(item)

    def submit(self, date):
        total = 0.0
        print '购买清单如下:'
        for item in self._shopping_basket:
            x = item.cal_price(date)
            total += x
            msg = "%s, 单价%s, 已购买%s件" % (item.name, item.price, item.cnt)
            if item.discount:
                msg += ", 享受%s折优惠" % int((item.discount.percent*10))
            print msg

        if self._coupon:
            if date < self._coupon.expired and total >= self._coupon.top:
                total -= self._coupon.sub

        print "总价为: %.2f" % total
        return total
