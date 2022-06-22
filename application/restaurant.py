from datetime import datetime

peak_hours_pu = """
    SELECT rt.restaurant_name,
           EXTRACT(HOUR FROM rn.order_time) AS order_hour,
           COUNT(*) AS total_orders_per_hour
    FROM reservation rn JOIN restaurant rt ON rn.restaurant_id = rt.restaurant_id
                        JOIN pickup pu ON rn.reservation_id = pu.reservation_id
    WHERE {criteria1} = {value1}
          AND {criteria2} >= {value2}
          AND {criteria3} <= {value3}
    GROUP BY rt.restaurant_name,
             order_hour
    ORDER BY total_orders_per_hour DESC;
"""

peak_hours_de = """
    SELECT rt.restaurant_name,
           EXTRACT(HOUR FROM rn.order_time) AS order_hour,
           COUNT(*) AS total_orders_per_hour
    FROM reservation rn JOIN restaurant rt ON rn.restaurant_id = rt.restaurant_id
                        JOIN delivery de ON rn.reservation_id = de.reservation_id
    WHERE {criteria1} = {value1}
          AND {criteria2} >= {value2}
          AND {criteria3} <= {value3}
    GROUP BY rt.restaurant_name,
             order_hour
    ORDER BY total_orders_per_hour DESC;
"""


def fetch_peak_hours(args):

    if 'restaurant_name' in args and len(args['restaurant_name']) > 0:
        c1 = "rt.restaurant_name"
        v1 = "'" + args["restaurant_name"] + "'"
    else:
        c1 = 1
        v1 = 1
    if 'consult_from' in args and len(args['consult_from']) > 0:
        c2 = "rn.order_time"
        v2 = args["consult_from"]
        v2 = "'" + v2.replace("T", " ") + ":00" + "'"
    else:
        c2 = 1
        v2 = 1
    if 'consult_to' in args and len(args['consult_to']) > 0:
        c3 = "rn.order_time"
        v3 = args["consult_to"]
        v3 = "'" + v3.replace("T", " ") + ":00" + "'"
    else:
        c3 = 1
        v3 = 1
 
    if args['delivery_type'] == 'pickup':
        query = peak_hours_pu
    else:
        query = peak_hours_de

    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3,
                         value1 = v1, value2 = v2, value3 = v3)
    return query


menu_design = """
    SELECT i.item_name AS item_name,
           COUNT(*) AS order_times
    FROM item i LEFT JOIN reservation_item ri ON i.item_id = ri.item_id 
                LEFT JOIN reservation r ON ri.reservation_id = r.reservation_id
                LEFT JOIN restaurant rt ON r.restaurant_id = rt.restaurant_id
    WHERE {criteria1} = {value1}
          AND {criteria2} >= {value2}
          AND {criteria3} <= {value3}
    GROUP BY i.item_name
    ORDER BY order_times
"""


def fetch_menu_design(args):
    if 'restaurant_name' in args and len(args['restaurant_name']) > 0 and args['restaurant_name'] != 'ALL':
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

    if args['popular/unpopular'] == 'popular':
        query = menu_design + " DESC;"
    else:
        query = menu_design + ";"

    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3,
                         value1 = v1, value2 = v2, value3 = v3)
    return query

churn_rate = """
    WITH second_month AS (
     SELECT DISTINCT customer_id
     FROM reservation r JOIN restaurant rt ON r.restaurant_id = rt.restaurant_id
     WHERE {criteria1} = {value1}
           AND {criteria2} >= {value2}
           AND {criteria3} <= {value3}
    ),
    first_month AS (
        SELECT DISTINCT customer_id
        FROM reservation r JOIN restaurant rt ON r.restaurant_id = rt.restaurant_id
        WHERE {criteria1} = {value1}
              AND {criteria4} >= {value4}
              AND {criteria2} <= {value2}
    )
    SELECT {value1} AS restaurant_name,
           CASE
                WHEN COUNT(f.customer_id) = 0 THEN 999
           ELSE ROUND((COUNT(f.customer_id) - COUNT(s.customer_id))/COUNT(f.customer_id),2)
           END AS churn_rate
    FROM first_month f LEFT JOIN second_month s ON f.customer_id = s.customer_id
"""



def fetch_churn_rate(args):
    if 'restaurant_name' in args and len(args['restaurant_name']) > 0 and args['restaurant_name'] != 'ALL':
        c1 = "rt.restaurant_name"
        v1 = "'" + args["restaurant_name"] + "'"
    else:
        c1 = 1
        v1 = 1
    if 'consult_from' in args and len(args['consult_from']) > 0:
        c2 = "r.order_time"
        c3 = "r.order_time"
        c4 = "r.order_time"
        v3 = args["consult_from"]
        v3 = datetime.strptime(v3, "%Y-%m-%dT%H:%M")
        v2 = v3 - datetime.timedelta(months=1)
        v4 = "'" + datetime.strftime((v2 - datetime.timedelta(months=1)), "%Y-%m-%d %H:%M:%S") + "'"
        v3 = "'" + datetime.strftime(v3, "%Y-%m-%d %H:%M:%S") + "'"
        v2 = "'" + datetime.strftime(v2, "%Y-%m-%d %H:%M:%S") + "'"
    
    else:
        c2 = 1
        c3 = 1
        c4 = 1
        v2 = 1
        v3 = 1
        v4 = 1
    
    query = churn_rate
    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3, criteria4 = c4,
                         value1 = v1, value2 = v2, value3 = v3, value4 = v4)
    return query


avg_reservation = """
    WITH reservation_number AS (
        SELECT c.customer_id AS customer_id,
               count(rn.reservation_id) AS number_of_reservation
        FROM customer c LEFT JOIN reservation rn ON c.customer_id = rn. customer_id
                        JOIN restaurant rt ON rn.restaurant_id = rt. restaurant_id
        WHERE {criteria1} = {value1}
              AND {criteria2} >= {value2}
              AND {criteria3} <= {value3}
        GROUP BY c.customer_id
    )
    SELECT customer_id,
           number_of_reservation,
           CASE
                WHEN number_of_reservation >= (
                    SELECT avg(number_of_reservation)
                    FROM reservation_number
                ) THEN 'YES'
                ELSE 'NO'
           END AS whether_more_than_avg
    FROM reservation_number
"""



def fetch_avg_res(args):
    if 'restaurant_name' in args and len(args['restaurant_name']) > 0:
        c1 = "rt.restaurant_name"
        v1 = "'" + args["restaurant_name"] + "'"
    else:
        c1 = 1
        v1 = 1
    if 'consult_from' in args and len(args['consult_from']) > 0:
        c2 = "rn.order_time"
        v2 = args["consult_from"]
        v2 = "'" + v2.replace("T", " ") + ":00" + "'"
    else:
        c2 = 1
        v2 = 1
    if 'consult_to' in args and len(args['consult_to']) > 0:
        c3 = "rn.order_time"
        v3 = args["consult_to"]
        v3 = "'" + v3.replace("T", " ") + ":00" + "'"
    else:
        c3 = 1
        v3 = 1
 
    query = avg_reservation
    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3,
                         value1 = v1, value2 = v2, value3 = v3)
    return query

