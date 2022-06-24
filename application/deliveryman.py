from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.sql import text

deliveryman = """
    SELECT dm.deliveryman_id,
           avg(d.delivery_time - pick_time) AS avg_delivery_time,
           round(avg(r.delivery_tips), 2) AS avg_delivery_tips
    FROM deliveryman dm LEFT JOIN delivery d ON dm.deliveryman_id = d.deliveryman_id
                        LEFT JOIN reservation r ON d.reservation_id = r.reservation_id
    WHERE {criteria1} LIKE {value1}
          AND {criteria2} >= {value2}
          AND {criteria3} <= {value3}
    GROUP BY dm.deliveryman_id;
"""

def fetch_deliveryman(args):
    c1 = "CAST(dm.deliveryman_id AS varchar)"
    c2 = "r.order_time"
    c3 = "r.order_time"
    v1 = ":deliveryman_id"
    v2 = ":start_time"
    v3 = ":end_time"
    if 'deliveryman_id' in args and len(str(args['deliveryman_id'])) > 0:
        did = str(args['deliveryman_id'])
    else:
        did = '%'
    if 'consult_from' in args and len(args['consult_from']) > 0:   
        st = args['consult_from'].replace("T", " ")
    else:
        st = '2000-01-01 00:00:00'
    if 'consult_to' in args and len(args['consult_to']) > 0:
        et = args['consult_to'].replace("T", " ")
    else:
        et = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    query = deliveryman
    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3,
                         value1 = v1, value2 = v2, value3 = v3)
    query = text(query)
    return [query, did, st, et]
