INSERT_ORDER_MAIN = '''
INSERT INTO rabbit.order_main
(bill_amount, status, created_time, updated_time) VALUES 
(%s, %s, current_timestamp(), current_timestamp());
'''

INSERT_ORDER_DETAIL = '''
INSERT INTO rabbit.order_detail
(order_id, product_id, price, quantity, created_time, updated_time)
VALUES (%s, %s, 10, %s, current_timestamp(), current_timestamp())
'''