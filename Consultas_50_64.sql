USE gymsql;

select gender as Género, 
		count(*) as Total,
        ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users_data WHERE age >= 50 AND age <= 64)), 2) AS Porcentaje
from users_data
where age >=50 and age <=64
group by gender
order by Porcentaje DESC;

select user_location as Localizacion, 
		count(*) as Total,
        ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users_data WHERE age >= 50 AND age <= 64)), 2) AS Porcentaje
from users_data
where age >=50 and age <=64
group by user_location
order by Porcentaje DESC;


select subscription_plan, 
		count(*) as Total,
        ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users_data WHERE age >= 50 AND age <= 64)), 2) AS Porcentaje
from users_data
where age >=50 and age <=64
group by subscription_plan
order by Porcentaje DESC;

SELECT gym_type, COUNT(*) AS Total 
FROM gym_locations_data 
GROUP BY gym_type;

SELECT workout_type, SUM(calories_burned) AS Total_Calories 
FROM checkin_checkout_history_updated
GROUP BY workout_type
ORDER BY Total_Calories 

select user_id, AVG(TIMESTAMPDIFF(MINUTE, checkin_time, checkout_time)) AS Avg_Workout_Time 
FROM checkin_checkout_history_updated
GROUP BY user_id;

SELECT user_id, COUNT(*) AS Total_Visits 
FROM checkin_checkout_history_updated
GROUP BY user_id;

