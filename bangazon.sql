SELECT u.id user_id,
        u.first_name || " " || u.last_name customer_name,
    s.name store_name
FROM auth_user u
JOIN bangazon_api_favorite f ON f.customer_id = user_id
JOIN bangazon_api_store s ON f.store_id = s.id
