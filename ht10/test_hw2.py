from hw2 import Order


def morning_discount(order):
    return order.price * 0.5


def elder_discount(order):
    return order.price * 0.1


def test_order_no_discount():
    order_2 = Order(100)
    assert order_2.final_price() == 100


def test_order_morning_discount():
    order_1 = Order(100, morning_discount)
    assert order_1.final_price() == 50


def test_order_elder_discount():
    order_2 = Order(100, elder_discount)
    assert order_2.final_price() == 10
