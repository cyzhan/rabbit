INSERT_ORDER_MAIN = '''
INSERT INTO rabbit.order_main
(user_id, bill_amount, status, created_time, updated_time) VALUES 
(%s ,%s, %s, current_timestamp(), current_timestamp());
'''

INSERT_ORDER_DETAIL = '''
INSERT INTO rabbit.order_detail
(order_id, product_id, price, quantity, created_time, updated_time)
VALUES (%s, %s, %s, %s, current_timestamp(), current_timestamp())
'''