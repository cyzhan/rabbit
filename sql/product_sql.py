GET_PRODUCT_BY_IDS = '''
SELECT a.id, a.price, a.quantity 
FROM rabbit.product AS a
WHERE a.id IN ({}) AND a.active = 1
'''

SELECT_PRODUCT_FOR_UPDATE = '''
SELECT a.id, a.price, a.quantity 
FROM rabbit.product AS a 
WHERE a.id IN ({}) AND a.active = 1 FOR UPDATE
'''

UPDATE_PRODUCT_FOR_QUANTITY = '''
UPDATE rabbit.product AS a 
SET a.quantity = %s WHERE a.id = %s
'''


