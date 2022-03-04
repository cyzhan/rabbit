INSERT_ORDER_MAIN = '''
INSERT INTO rabbit.order_main
(bill_amount, status, created_time, updated_time) VALUES 
(%s, %s, current_timestamp(), current_timestamp());
'''