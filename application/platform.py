coupon_used_pct = """
    SELECT round(count(DISTINCT cu.coupon_id)/count(DISTINCT c.coupon_id), 2) AS coupon_used_pct
    FROM coupon c LEFT JOIN coupon_used cu ON c.coupon_id = cu.coupon_id
    WHERE {criteria2} >= {value2}
          AND {criteria3} <= {value3};
"""

def fetch_pct_coupon(args):
    if 'consult_from' in args and len(args['consult_from']) > 0:
        c2 = "c.issue_date"
        v2 = args["consult_from"]
        v2 = "'" + v2.replace("T", " ") + ":00" + "'"
    else:
        c2 = 1
        v2 = 1
    if 'consult_to' in args and len(args['consult_to']) > 0:
        c3 = "c.expire_date"
        v3 = args["consult_to"]
        v3 = "'" + v3.replace("T", " ") + ":00" + "'"
    else:
        c3 = 1
        v3 = 1
 
    query = coupon_used_pct
    query = query.format(criteria2 = c2, criteria3 = c3,
                         value2 = v2, value3 = v3)
    return query


before_after = """
WITH customer_stats AS (
    SELECT customer_id,
           (CASE 
                WHEN customer_id IN (SELECT r.customer_id
                                     FROM reservation r JOIN coupon_used cu ON r.reservation_id = cu.reservation_id
                                                        JOIN customer c ON r.customer_id = c.customer_id
                                     WHERE {criteria2} >= {value2}
                                            AND {criteria3} <= {value3}) THEN 'YES'
                ELSE 'NO'
                END) AS whether_use_coupon,
            count(reservation_id) AS total_order_number,
            avg(total_amount) AS avg_amount
    FROM reservation r
    WHERE {criteria2} >= {value2}
          AND {criteria3} <= {value3}
          GROUP BY customer_id)
SELECT whether_use_coupon,
       round(avg(total_order_number),2) AS avg_order_number,
       round(avg(avg_amount),2) AS avg_amount
FROM customer_stats
GROUP BY whether_use_coupon;"""



def fetch_before_after(args):
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
 
    query = before_after
    query = query.format(criteria2 = c2, criteria3 = c3,
                         value2 = v2, value3 = v3)
    return query



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
 
    query = customer_distribution
    query = query.format(criteria2 = c2, criteria3 = c3,
                         value2 = v2, value3 = v3)
    return query

