#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import items


def show_usage():
    msg = """
    输入格式如下：
        1 促销信息：
            日期 | 折扣 | 产品品类，可有多个，每个一行，如果没有则保留一个空行，如
            2013.11.11 | 0.7 | 电子
        2 所购产品：
            数量 * 商品: 单价，如
            1 * pad: 2399.00
            1 * 显示器: 1799.00
            12 * 啤酒: 25.00
            5 * 面包: 9.00
        3 结算日期:
            2013.11.11
        4 促销信息:
            到期时间 满多少元 减多少元，2014年3月2日到期，满1000减200，如
            2014.3.2 1000 2000
    输入ctrl-D退出
    """
    print msg


if __name__ == '__main__':
    show_usage()

    cart = items.ShoppingCart()
    discount_map = dict()
    coupon = None
    submit_date = None

    print "请输入:"
    while True:
        try:
            raw = raw_input()
            raw = raw.strip()
            if not raw:
                continue
            if '|' in raw:
                expired_date, discount, han = \
                    [_.strip() for _ in raw.split('|')]
                discount = items.Discount(expired_date,
                                          discount,
                                          han)
                discount_map[discount.category] = discount
            elif '*' in raw:
                cnt, product = [_.strip() for _ in raw.split('*')]
                name, price = [_.strip() for _ in product.split(':')]
                obj = items.new_goods(name, price, cnt)
                if obj:
                    if obj.category in discount_map:
                        obj.discount = discount_map[obj.category]
                    cart.add(obj)
            elif ' ' in raw:
                expired_date, top, sub = [_.strip() for _ in raw.split()]
                obj = items.Coupon(expired_date, top, sub)
                if not coupon:
                    coupon = obj
                    cart.coupon = coupon
            else:
                submit_date = items.format_date(raw)

        except EOFError as e:
            break
        except Exception as e:
            print str(e)
            print "请重新输入"

    cart.submit(submit_date)
