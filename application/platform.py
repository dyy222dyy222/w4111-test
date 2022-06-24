from datetime import datetime
from sqlalchemy.sql import text

coupon_used_pct = """
    SELECT CASE
               WHEN count(DISTINCT c.coupon_id) = 0 THEN 999   
               ELSE round((CAST(count(DISTINCT cu.coupon_id) as float)/cast(count(DISTINCT c.coupon_id) AS FLOAT))::numeric, 2) 
               END AS coupon_used_pct
    FROM coupon c LEFT JOIN coupon_used cu ON c.coupon_id = cu.coupon_id
    WHERE {criteria2} >= {value2}
          AND {criteria3} <= {value3};
"""

def fetch_pct_coupon(args):
    c2 = "c.issue_date"
    c3 = "c.expire_date"
    v2 = ":issue_time"
    v3 = ":expire_time"

    if 'consult_from' in args and len(args['consult_from']) > 0:   
        st = args['consult_from'].replace("T", " ")
    else:
        st = '2000-01-01 00:00:00'
    if 'consult_to' in args and len(args['consult_to']) > 0:
        et = args['consult_to'].replace("T", " ")
    else:
        et = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
 
    query = coupon_used_pct
    query = query.format(criteria2 = c2, criteria3 = c3,
                         value2 = v2, value3 = v3)
    query = text(query)
    return [query, st, et]



before_after = """
    WITH customer_stats AS (SELECT customer_id,
                                   (CASE 
                                        WHEN customer_id IN (SELECT customer_id
                                                            FROM coupon_used) THEN 'YES'
                                        ELSE 'NO'
                                    END) AS whether_use_coupon,
                                    count(reservation_id) AS total_order_number,
                                    avg(total_amount) AS avg_amount
                            FROM reservation
                            WHERE {criteria2} >= {value2}
                                  AND {criteria3} <= {value3}
                            GROUP BY customer_id)
    SELECT whether_use_coupon,
           round(avg(total_order_number),2) AS avg_order_number,
           round(avg(avg_amount),2) AS avg_amount
    FROM customer_stats
    GROUP BY whether_use_coupon;
"""

def fetch_before_after(args):
    c2 = "order_time"
    c3 = "order_time"
    v2 = ":start_time"
    v3 = ":end_time"

    if 'consult_from' in args and len(args['consult_from']) > 0:   
        st = args['consult_from'].replace("T", " ")
    else:
        st = '2000-01-01 00:00:00'
    if 'consult_to' in args and len(args['consult_to']) > 0:
        et = args['consult_to'].replace("T", " ")
    else:
        et = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
 
    query = before_after
    query = query.format(criteria2 = c2, criteria3 = c3,
                         value2 = v2, value3 = v3)
    query = text(query)
    return [query, st, et]

customer_distribution = """
    SELECT ca.city,
           count(r.reservation_id) AS number_of_orders
    FROM reservation r JOIN customer c ON r.customer_id = c.customer_id
                       LEFT JOIN customer_lives_in_address cl ON c.customer_id = cl.customer_id
                       LEFT JOIN customer_address ca ON cl.address_id = ca.address_id
    WHERE {criteria2} >= {value2}
          AND {criteria3} <= {value3}
    GROUP BY ca.city;

"""

def fetch_customer_distribution(args):
    c2 = "r.order_time"
    c3 = "r.order_time"
    v2 = ":start_time"
    v3 = ":end_time"

    if 'consult_from' in args and len(args['consult_from']) > 0:   
        st = args['consult_from'].replace("T", " ")
    else:
        st = '2000-01-01 00:00:00'
    if 'consult_to' in args and len(args['consult_to']) > 0:
        et = args['consult_to'].replace("T", " ")
    else:
        et = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
 
 
    query = customer_distribution
    query = query.format(criteria2 = c2, criteria3 = c3,
                         value2 = v2, value3 = v3)
    query = text(query)
    return [query, st, et]

