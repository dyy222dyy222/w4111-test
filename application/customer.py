popular_restaurant = """
    SELECT rt.restaurant_name,
           count(r.reservation_id) AS number_of_reservations,
           round(avg(base_amount), 2) AS avg_base_amount
    FROM restaurant rt LEFT JOIN reservation r ON rt.restaurant_id = r.restaurant_id
    WHERE {criteria2} >= {value2}
          AND {criteria3} <= {value3}
    GROUP BY rt.restaurant_id,
             rt.restaurant_name
    ORDER BY number_of_reservations DESC;
"""

def fetch_popular_restaurant(args):
    if 'consult_from' in args and len(args['consult_from']) > 0:
        c2 = "r.order_time"
        v2 = args["consult_from"]
        v2 = "'" + v2.replace("T", " ") + ":00" + "'"
    else:
        c2 = 1
        v2 = 1
    if 'consult_to' in args and len(args['consult_to']) > 0:
        c3 = "r.order_time"
        v3 = args["consult_to"]
        v3 = "'" + v3.replace("T", " ") + ":00" + "'"
    else:
        c3 = 1
        v3 = 1
 
    query = popular_restaurant
    query = query.format(criteria2 = c2, criteria3 = c3,
                         value2 = v2, value3 = v3)
    return query



popular_dish = """
    SELECT i.item_name,
           count(r.reservation_id) AS number_of_orders
    FROM item i LEFT JOIN reservation_item ri ON i.item_id = ri.item_id
                JOIN reservation r ON ri.reservation_id = r.reservation_id
                LEFT JOIN restaurant rt ON r.restaurant_id = rt.restaurant_id
    WHERE {criteria1} = {value1}
          AND {criteria2} >= {value2}
          AND {criteria3} <= {value3}
    GROUP BY i.item_id,
             i.item_name
    ORDER BY number_of_orders DESC;
"""

def fetch_popular_dish(args):
    if 'restaurant_name' in args and len(args['restaurant_name']) > 0:
        c1 = "rt.restaurant_name"
        v1 = "'" + args["restaurant_name"] + "'"
    else:
        c1 = 1
        v1 = 1
    if 'consult_from' in args and len(args['consult_from']) > 0:
        c2 = "r.order_time"
        v2 = args["consult_from"]
        v2 = "'" + v2.replace("T", " ") + ":00" + "'"
    else:
        c2 = 1
        v2 = 1
    if 'consult_to' in args and len(args['consult_to']) > 0:
        c3 = "r.order_time"
        v3 = args["consult_to"]
        v3 = "'" + v3.replace("T", " ") + ":00" + "'"
    else:
        c3 = 1
        v3 = 1
 
    query = popular_dish
    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3,
                         value1 = v1, value2 = v2, value3 = v3)
    return query
