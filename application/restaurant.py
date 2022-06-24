from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.sql import text



peak_hours_pu = """
    SELECT rt.restaurant_name,
           EXTRACT(HOUR FROM rn.order_time) AS order_hour,
           COUNT(*) AS total_orders_per_hour
    FROM reservation rn JOIN restaurant rt ON rn.restaurant_id = rt.restaurant_id
                        JOIN pickup pu ON rn.reservation_id = pu.reservation_id
    WHERE {criteria1} LIKE {value1}
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
    WHERE {criteria1} LIKE {value1}
          AND {criteria2} >= {value2}
          AND {criteria3} <= {value3}
    GROUP BY rt.restaurant_name,
             order_hour
    ORDER BY total_orders_per_hour DESC;
"""


def fetch_peak_hours(args):
    c1 = "rt.restaurant_name"
    c2 = "rn.order_time"
    c3 = "rn.order_time"
    v1 = ":restaurant_name"
    v2 = ":start_time"
    v3 = ":end_time"
    if 'restaurant_name' in args and len(args['restaurant_name']) > 0:
        rn = args['restaurant_name']
    else:
        rn = '%'
    if 'consult_from' in args and len(args['consult_from']) > 0:   
        st = args['consult_from'].replace("T", " ")
    else:
        st = '2000-01-01 00:00:00'
    if 'consult_to' in args and len(args['consult_to']) > 0:
        et = args['consult_to'].replace("T", " ")
    else:
        et = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    if args['delivery_type'] == 'pickup':
        query = peak_hours_pu
    else:
        query = peak_hours_de

    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3,
                         value1 = v1, value2 = v2, value3 = v3)
    query = text(query)
    
    return [query, rn, st, et]



menu_design = """
    SELECT i.item_name AS item_name,
           COUNT(*) AS order_times
    FROM item i LEFT JOIN reservation_item ri ON i.item_id = ri.item_id 
                LEFT JOIN reservation r ON ri.reservation_id = r.reservation_id
                LEFT JOIN restaurant rt ON r.restaurant_id = rt.restaurant_id
    WHERE {criteria1} LIKE {value1}
          AND {criteria2} >= {value2}
          AND {criteria3} <= {value3}
    GROUP BY i.item_name
    ORDER BY order_times
"""


def fetch_menu_design(args):
    c1 = "rt.restaurant_name"
    c2 = "r.order_time"
    c3 = "r.order_time"
    v1 = ":restaurant_name"
    v2 = ":start_time"
    v3 = ":end_time"
    if 'restaurant_name' in args and len(args['restaurant_name']) > 0:
        rn = args['restaurant_name']
    else:
        rn = '%'
    if 'consult_from' in args and len(args['consult_from']) > 0:   
        st = args['consult_from'].replace("T", " ")
    else:
        st = '2000-01-01 00:00:00'
    if 'consult_to' in args and len(args['consult_to']) > 0:
        et = args['consult_to'].replace("T", " ")
    else:
        et = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    if args['popular/unpopular'] == 'popular':
        query = menu_design + " DESC;"
    else:
        query = menu_design + ";"

    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3,
                         value1 = v1, value2 = v2, value3 = v3)
    query = text(query)
        
    return [query, rn, st, et]




churn_rate = """
    WITH second_month AS (
     SELECT DISTINCT customer_id
     FROM reservation r JOIN restaurant rt ON r.restaurant_id = rt.restaurant_id
     WHERE {criteria1} LIKE {value1}
           AND {criteria2} >= {value2}
           AND {criteria3} <= {value3}
    ),
    first_month AS (
        SELECT DISTINCT customer_id
        FROM reservation r JOIN restaurant rt ON r.restaurant_id = rt.restaurant_id
        WHERE {criteria1} LIKE {value1}
              AND {criteria4} >= {value4}
              AND {criteria2} <= {value2}
    )
    SELECT CASE
                WHEN COUNT(f.customer_id) = 0 THEN 999
           ELSE ROUND((cast(COUNT(f.customer_id) - COUNT(s.customer_id)as float)/CAST(COUNT(f.customer_id) AS FLOAT))::numeric,2)
           END AS churn_rate
    FROM first_month f LEFT JOIN second_month s ON f.customer_id = s.customer_id
"""



def fetch_churn_rate(args):
    c1 = 'rt.restaurant_name'
    c2 = 'r.order_time'
    c3 = 'r.order_time'
    c4 = 'r.order_time'
    v1 = ':restaurant_name'
    v2 = ':minus1'
    v3 = ':end_time'
    v4 = ':minus2'
    if 'restaurant_name' in args and len(args['restaurant_name']) > 0:
        rn = args['restaurant_name']
    else:
        rn = '%'
    if 'consult_from' in args and len(args['consult_from']) > 0:   
        et = datetime.strptime(args["consult_from"], "%Y-%m-%dT%H:%M")
        et1 = et - relativedelta(months=1)
        et2 = et1 - relativedelta(months=1)
        et = datetime.strftime(et, "%Y-%m-%d %H:%M:%S")
        et1 = datetime.strftime(et1, "%Y-%m-%d %H:%M:%S")
        et2 = datetime.strftime(et2, "%Y-%m-%d %H:%M:%S")
    else:
        et = ''
        et1 = ''
        et2 = ''

   
    query = churn_rate
    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3, criteria4 = c4,
                         value1 = v1, value2 = v2, value3 = v3, value4 = v4)

    query = text(query)
    return [query, rn, et, et1, et2] 



avg_reservation = """
    WITH reservation_number AS (
        SELECT c.customer_id AS customer_id,
               count(rn.reservation_id) AS number_of_reservation
        FROM customer c LEFT JOIN reservation rn ON c.customer_id = rn. customer_id
                        JOIN restaurant rt ON rn.restaurant_id = rt. restaurant_id
        WHERE {criteria1} LIKE {value1}
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
    c1 = "rt.restaurant_name"
    c2 = "rn.order_time"
    c3 = "rn.order_time"
    v1 = ":restaurant_name"
    v2 = ":start_time"
    v3 = ":end_time"
    if 'restaurant_name' in args and len(args['restaurant_name']) > 0:
        rn = args['restaurant_name']
    else:
        rn = '%'
    if 'consult_from' in args and len(args['consult_from']) > 0:   
        st = args['consult_from'].replace("T", " ")
    else:
        st = '2000-01-01 00:00:00'
    if 'consult_to' in args and len(args['consult_to']) > 0:
        et = args['consult_to'].replace("T", " ")
    else:
        et = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
 
    query = avg_reservation
    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3,
                         value1 = v1, value2 = v2, value3 = v3)
    query = text(query)
    return [query, rn, st, et]

