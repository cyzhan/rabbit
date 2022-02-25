GET_PRODUCT_BY_IDS = '''
SELECT a.id, a.price, a.quantity 
FROM rabbit.product AS a
WHERE a.id IN ({}) AND a.active = 1
'''