"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all


class InexpensiveProductList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games with their average rating, order them, and limit to 5
            db_cursor.execute("""
            SELECT  
                p.id,
                p.name, 
                p.price,
                s.name store_name
            FROM bangazon_api_product p
            JOIN bangazon_api_store s ON p.store_id = s.id
            WHERE p.price < 1000
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the games_by_user list:
            #
            # [
            #   {
            #     "id",
            #     "title",
            #     "number_of_players"
            #   },
            # ]

            inexpensive_products = []

            for row in dataset:
                inexpensive_products.append({
                    "id": row["id"],
                    "name": row["name"],
                    "price": row["price"],
                    "store_name": row["store_name"],
                })
                

        # The template string must match the file name of the html template
        template = 'products/inexpensive_products.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "inexpensive_product_list": inexpensive_products
        }

        return render(request, template, context)