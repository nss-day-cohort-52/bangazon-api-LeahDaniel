"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all


class CompleteOrderList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games with their average rating, order them, and limit to 5
            db_cursor.execute("""
            SELECT o.id,
                u.first_name || " " || u.last_name customer_name,
                SUM(p.price) total_cost,
                pt.merchant_name
            FROM bangazon_api_order o 
            JOIN auth_user u ON o.user_id = u.id
            JOIN bangazon_api_orderproduct op ON op.order_id = o.id
            JOIN bangazon_api_product p ON p.id = op.product_id
            JOIN bangazon_api_paymenttype pt ON o.payment_type_id = pt.id
            WHERE o.completed_on NOTNULL
            GROUP BY o.id
            ORDER BY o.created_on
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

            complete_orders = []

            for row in dataset:
                complete_orders.append({
                    "id": row["id"],
                    "customer_name": row["customer_name"],
                    "total_cost": row["total_cost"],
                    "merchant_name": row["merchant_name"],
                })
                

        # The template string must match the file name of the html template
        template = 'orders/complete_orders.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "complete_order_list": complete_orders
        }

        return render(request, template, context)