"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all


class UserFavoriteList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT u.id user_id,
                u.first_name || " " || u.last_name customer_name,
                s.name store_name
            FROM auth_user u
            JOIN bangazon_api_favorite f ON f.customer_id = user_id
            JOIN bangazon_api_store s ON f.store_id = s.id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each customer
            #
            # [
            #   {
            #     "user_id": 1,
            #     "customer_name": "foo",
            #     "favorites": [
            #       {
            #         "store_name": "bar"
            #       },
            #       {
            #         "store_name": "bar"
            #       },
            #     ]
            #   },
            # ]

            favorites_by_customer = []

            for row in dataset:
                favorite = {
                    "store_name": row["store_name"]
                }
                
                # This is using a generator comprehension to find the user_dict in the favorites_by_customer list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                
                user_dict = next(
                    (
                        favorite for favorite in favorites_by_customer
                        if favorite['user_id'] == row['user_id']
                    ),
                    None
                )
                
                if user_dict:
                    # If the user_dict is already in the favorites_by_customer list, append the favorite to the favorites list
                    user_dict['favorites'].append(favorite)
                else:
                    # If the user is not on the favorites_by_customer list, create and add the user to the list
                    favorites_by_customer.append({
                        "user_id": row["user_id"],
                        "customer_name": row['customer_name'],
                        "favorites": [favorite]
                    })
        
        # The template string must match the file name of the html template
        template = 'favorites/user_favorites.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "user_favorites_list": favorites_by_customer
        }

        return render(request, template, context)
