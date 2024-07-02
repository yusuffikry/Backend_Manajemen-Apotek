-- Kueri pertama: Menentukan 10 genre film dengan profit tertinggi di kedua toko
(SELECT
  c.name AS Kategori,
  s.store_id AS Toko,
  NULL AS JumlahDVD,
  NULL AS Status
FROM
  category c
  JOIN film_category fc ON c.category_id = fc.category_id
  JOIN film f ON fc.film_id = f.film_id
  JOIN inventory i ON f.film_id = i.film_id
  JOIN rental r ON i.inventory_id = r.inventory_id
  JOIN payment p ON r.rental_id = p.rental_id
  JOIN store s ON i.store_id = s.store_id
GROUP BY
  c.name, s.store_id
ORDER BY
  amount DESC
LIMIT 10)

UNION

-- Kueri kedua: Menentukan jumlah stok DVD dari setiap kategori di kedua toko
(SELECT
  c.name AS Kategori,
  s.store_id AS Toko,
  COUNT(i.inventory_id) AS JumlahDVD,
  CASE
    WHEN (COUNT(i.inventory_id) & (COUNT(i.inventory_id) - 1)) = 0 THEN 'Nice'
    ELSE 'Not Nice'
  END AS Status
FROM
  category c
  JOIN film_category fc ON c.category_id = fc.category_id
  JOIN film f ON fc.film_id = f.film_id
  JOIN inventory i ON f.film_id = i.film_id
  JOIN store s ON i.store_id = s.store_id
GROUP BY
  c.name, s.store_id
);


-- --
(SELECT
  c.name AS Kategori,
  "Toko 1" AS Toko,
  COUNT(i.inventory_id) AS JumlahDVD,
  CASE
    WHEN (COUNT(i.inventory_id) & (COUNT(i.inventory_id) - 1)) = 0 THEN 'Nice'
    ELSE 'Not Nice'
  END AS Status
FROM
  (SELECT SUM(p.amount)
   FROM payment p
   JOIN rental r ON p.rental_id = r.rental_id
   JOIN inventory i ON r.inventory_id = i.inventory_id
   JOIN film f ON i.film_id = f.film_id
   JOIN film_category fc ON i.film_id = fc.film_id
   JOIN category c USING (category_id)
   WHERE fc.category_id = c.category_id
     AND s.store_id = 1 
	  GROUP BY c.name, s.store_id
ORDER BY Toko, JumlahDVD DESC
LIMIT 10)
)


(SELECT
  c.name AS Kategori,
  "Toko 1" AS Toko,
  COUNT(i.inventory_id) AS JumlahDVD,
  CASE
    WHEN (COUNT(i.inventory_id) & (COUNT(i.inventory_id) - 1)) = 0 THEN 'Nice'
    ELSE 'Not Nice'
  END AS Status
FROM
  category c
  JOIN film_category fc ON c.category_id = fc.category_id
  JOIN film f ON fc.film_id = f.film_id
  JOIN inventory i ON f.film_id = i.film_id
  JOIN store s ON i.store_id = s.store_id
GROUP BY
  c.name, s.store_id
  ORDER BY toko DESC
LIMIT 10)


UNION 

(SELECT c.name AS Kategori, "Toko 2" AS Toko, COUNT(i.inventory_id) AS JumlahDVD, CASE
WHEN (COUNT(i.inventory_id) & (COUNT(i.inventory_id) - 1)) = 0 THEN 'Nice'
ELSE 'Not Nice'
END AS Status
FROM  category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN film f ON fc.film_id = f.film_id
JOIN inventory i ON f.film_id = i.film_id
JOIN store s ON i.store_id = s.store_id
WHERE s.store_id = 2
GROUP BY c.name, s.store_id
ORDER BY Toko, JumlahDVD DESC
LIMIT 10)



-- M2
SELECT CONCAT(c.first_name, " ", c.last_name) AS 'namaPelanggan', (SELECT COUNT(rental_id) FROM rental r WHERE r.customer_id = c.customer_id) AS 'jumlahRental', co.country AS 'negara'
FROM customer c
JOIN address a ON c.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
WHERE(
        SELECT COUNT(rental_id)
        FROM rental r
        WHERE r.customer_id = c.customer_id) = ( SELECT MAX(total_rentals) FROM (
		  																								SELECT c.customer_id, co.country, COUNT(rental_id) AS total_rentals
																						            FROM customer c
																						            JOIN rental r ON c.customer_id = r.customer_id
																						            JOIN address a ON c.address_id = a.address_id
																						            JOIN city ci ON a.city_id = ci.city_id
																						            JOIN country co ON ci.country_id = co.country_id
																						            GROUP BY c.customer_id, co.country
																						        		) AS customer_rentals
																						        		WHERE co.country = customer_rentals.country
);
