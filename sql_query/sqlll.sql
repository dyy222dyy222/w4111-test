*peak_hour_for_pick_up*
SELECT rt.restaurant_name,
       EXTRACT(HOUR FROM rn.order_time) AS order_hour,
       COUNT(*) AS total_orders_per_hour
FROM reservation rn JOIN restaurant rt ON rn.restaurant_id = rt.restaurant_id
                    JOIN pickup pu ON rn.reservation_id = pu.reservation_id
WHERE restaurant_name = 'Oda House'
GROUP BY rt.restaurant_name,
         order_hour
ORDER BY total_orders_per_hour DESC;


*menu_design
SELECT i.item_name AS item_name,
       COUNT(*) AS order_times
FROM item i JOIN reservation_item ri ON i.item_id = ri.item_id 
     JOIN reservation r ON ri.reservation_id = r.reservation_id
     JOIN restaurant rt ON r.restaurant_id = rt.restaurant_id
WHERE restaurant_name = 'Oda House'
GROUP BY i.item_name
ORDER BY item_name DESC;

*churn_rate
WITH second_mouth AS (
     SELECT DISTINCT customer_id
     FROM reservation r JOIN restaurant rt ON r.restaurant_id = rt.restaurant_id
     WHERE restaurant_name = 
           AND r.order_time >= 
           AND r.order_time <=
),
WITH first_mouth AS (
     SELECT DISTINCT customer_id
     FROM reservation r JOIN restaurant rt ON r.restaurant_id = rt.restaurant_id
     WHERE restaurant_name = 
           AND r.order_time >= 
           AND r.order_time <=
)
SELECT 

