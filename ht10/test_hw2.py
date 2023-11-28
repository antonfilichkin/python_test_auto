from hw2 import Order, morning_discount, elder_discount


def test_order_no_discount():
    order = Order(100)
    assert order.final_price() == 100


def test_order_morning_discount():
    order_1 = Order(100, morning_discount)
    assert order_1.final_price() == 50


def test_order_elder_discount():
    order_2 = Order(100, elder_discount)
    assert order_2.final_price() == 10
