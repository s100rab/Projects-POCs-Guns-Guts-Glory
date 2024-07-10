CREATE DATABASE ecommerce;
USE ecommerce;
SELECT * FROM ecommerce.user;
SELECT * FROM ecommerce.user LIMIT 100;
SELECT COUNT(DISTINCT(COUNTRY)) FROM ecommerce.user;
SELECT COUNT(DISTINCT(LANGUAGE)) FROM ecommerce.user;
SELECT COUNT(1) FROM ecommerce.user WHERE gender = 'M';
SELECT COUNT(1) FROM ecommerce.user WHERE gender = 'F';
SELECT COUNT(1) FROM ecommerce.user WHERE hasProfilePicture = 'True';
SELECT COUNT(1) FROM ecommerce.user WHERE hasAnyApp = 'True';
SELECT COUNT(1) FROM ecommerce.user WHERE hasAndroidApp= 'True';
SELECT COUNT(1) FROM ecommerce.user WHERE hasIosApp = 'True';
SELECT COUNT(*) as count_user_Bought,country FROM ecommerce.user where productsBought >= 1
GROUP BY country order by count_user_Bought DESC;
SELECT COUNT(*) as count_user_sold,country FROM ecommerce.user where productsSold >= 1
GROUP BY country order by count_user_sold ;
SELECT productsPassRate,country FROM ecommerce.user 
GROUP BY country order by productsPassRate DESC LIMIT 10;
SELECT count(*) as count_user,language FROM ecommerce.user group by language;

SELECT * FROM ecommerce.user where gender = 'F' and socialProductsLiked >= 1
union
SELECT * FROM ecommerce.user where gender = 'F' and productsWished >= 1;

SELECT * FROM ecommerce.user where gender = 'M' and productsSold >= 1
union
SELECT * FROM ecommerce.user where gender = 'M' and productsBought >= 1;

SELECT count(1),country FROM ecommerce.user where productsbought >=1 group by country limit 1 ;

SELECT country FROM ecommerce.user where productsSold =0 limit 10;
SELECT distinct(type) FROM ecommerce.user;
SELECT * FROM ecommerce.user order by daysSinceLastLogin asc limit 110;

SELECT count(*) as count_female_users FROM ecommerce.user where gender = 'F' and daysSinceLastLogin >100;
SELECT count(*) as count_female_users,country FROM ecommerce.user where gender = 'F' group by country;
SELECT count(*) as count_male_users,country FROM ecommerce.user where gender = 'M' group by country;

SELECT COUNTRY,GENDER,AVG(productsSold) AS avg_products_sold,AVG(productsBought) AS avg_products_bought 
FROM ecommerce.user where gender = 'M' group by country,GENDER;
SELECT * FROM ecommerce.user;
SELECT * FROM ecommerce.user;