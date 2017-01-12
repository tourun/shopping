#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import items

CATEGORY_CHN2ENG = {
    '电子': 'Electronics',
    '食品': 'Foods',
    '日用品': 'Commodity',
    '酒类': 'Wine'
}


if __name__ == '__main__':
    cart = items.ShoppingCart()
    discount_map = dict()
    coupon = None
    submit_date = None
    print "输入ctrl-D退出"
    while True:
        try:
            raw = raw_input()
            raw = raw.strip()
            if not raw:
                continue
            if '|' in raw:
                expired_date, discount, han = raw.split('|')
                category = CATEGORY_CHN2ENG[han]
                discount = items.Discount(expired_date,
                                          float(discount),
                                          category)
                discount_map[category] = discount
            elif '*' in raw:
                cnt, product = raw.split('*')
                name, price = product.split(':')
                obj = items.new_goods(name, price, cnt)
                if obj:
                    if obj.category in discount_map:
                        obj.discount = discount_map[obj.category]
                    cart.add(obj)
            elif ' ' in raw:
                expired_date, top, sub = raw.split()
                obj = items.Coupon(expired_date, int(top), int(sub))
                if not coupon:
                    coupon = obj
                    cart.coupon = coupon
            else:
                submit_date = items.format_date(raw)

        except EOFError as e:
            print str(e)
            break
        except Exception as e:
            print traceback.format_exc()

    cart.submit(submit_date)
