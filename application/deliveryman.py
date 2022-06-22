deliveryman = """
    SELECT dm.deliveryman_id,
           avg(d.delivery_time - pick_time) AS avg_delivery_time,
           round(avg(r.delivery_tips), 2) AS avg_delivery_tips
    FROM deliveryman dm LEFT JOIN delivery d ON dm.deliveryman_id = d.deliveryman_id
                        LEFT JOIN reservation r ON d.reservation_id = r.reservation_id
    WHERE {criteria1} = {value1}
          AND {criteria2} >= {value2}
          AND {criteria3} <= {value3}
    GROUP BY dm.deliveryman_id;
"""

def fetch_deliveryman(args):
    if 'deliveryman_id' in args and len(str(args['deliveryman_id'])):
        c1 = 'dm.deliveryman_id'
        v1 = args['deliveryman_id']
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
    query = deliveryman
    query = query.format(criteria1 = c1, criteria2 = c2, criteria3 = c3,
                         value1 = v1, value2 = v2, value3 = v3)
    return query

args = {'deliveryman_id': 1,
        'consult_from': '2010-01-01T11:11',
        'consult_to': '2022-01-01T11:11'}

print(fetch_deliveryman(args))