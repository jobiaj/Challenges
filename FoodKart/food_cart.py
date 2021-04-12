#-*- coding: utf-8 -*-
__author__ = "Jobi A J"


from builtins import object


class FoodCart(object):
    RESTARANTS_CACHE = {}
    USERS_CACHE = {}
    ORDER_HISTORY_CACHE = {}

    def __init__(self):
        pass

    def register_restaurant(self, name, locations, item, price, remaining_count):
        # Register Restaurant method, for registration for the foodkart resturant need 
        # to provide resturant_name, locations, item available, price and remaining_count.
        # Keeping the information in the object's Resturant Cache .
        resturant = Restaurant(name, locations, item, price, remaining_count)
        self.RESTARANTS_CACHE[name] = resturant


    def register_user(self, username, phone_number, location):
        # Register user method, for registration for the foodkart user need 
        # Username, phone_number and location.
        # Keeping the information in the objects User cache.
        user_info = User(username, phone_number, location)
        self.USERS_CACHE[username] = user_info


    def place_order(self, user, resturant_name, count):
        resturant = self.RESTARANTS_CACHE[resturant_name]
        resturant.place_order(count)
        #record the order history
        if user in self.ORDER_HISTORY_CACHE.keys():
            if resturant_name not in self.ORDER_HISTORY_CACHE[user]: 
                self.ORDER_HISTORY_CACHE[user].append(resturant_name)
        else:
            self.ORDER_HISTORY_CACHE[user] = [resturant_name]


    def create_review(self, username, resturant_name, review):
        ORDER_HISTORY_CACHE = {"username": ["foodcort1", "foodcort2"]}
        if username in self.ORDER_HISTORY_CACHE.keys():
            if resturant_name in self.ORDER_HISTORY_CACHE[username]:
                resturant = self.RESTARANTS_CACHE[resturant_name]
                resturant.update_review(review)
            else:
                print("can’t post a review, without ordering")
        else:
            print("can’t post a review, without ordering")


    def show_restaurant(self, mode="items"):
        display_data = ""
        mode_factory = {
         "items": {"display": ['name', "item", "price"], 
                   "sorting_key": 'price',
                   "order": False},
         "rating": {"display": ['name', "item", "rating"], 
                   "sorting_key": 'rating',
                   "order": True},
        }
        display_fields = mode_factory[mode]
        resturants = []
        for resturant_name in self.RESTARANTS_CACHE.keys():
            resturants.append(self.RESTARANTS_CACHE[resturant_name])
        sorted_res = sorted(resturants, key=lambda x:getattr(x, display_fields['sorting_key']), reverse=display_fields['order'])   
        for resturant in sorted_res:
            #resturant = self.RESTARANTS_CACHE[resturant_name]
            display_field = display_fields["display"]
            item = "%s, %s, %s" %(getattr(resturant, display_field[0]), 
                getattr(resturant, display_field[1]),
                getattr(resturant, display_field[2]))
            item += '\n'
            display_data += item
        print(display_data)


    def update_quantity(self, resturant_name, count):
        if resturant_name not in self.RESTARANTS_CACHE:
            print("Given Restaurant not exist in the kart")
        else:
            resturant = self.RESTARANTS_CACHE[resturant_name]
            resturant.update_quantity(count)
            print(resturant)



class Restaurant(object):
    ITEMS_CACHE = {}

    def __init__(self, name, locations, item, price, remaining_count):
        self.name = name
        self.locations = locations
        self.item = item
        self.price = price
        self.remaining_count = remaining_count
        self.review = []


    def update_review(self, review):
        self.review.append(review)
        # if self.review == 'NA':
        #     self.review = review
        # else:
        #     self.review += review
    @property
    def rating(self):
        if self.review:
            return sum(self.review)/len(self.review)
        else:
            return 0



    def place_order(self, count):
        if self.remaining_count < count:
            print("Cannot place order")
        else:
            self.remaining_count -= count
            print("Order Placed Successfully.")


    def update_quantity(self, count):
        self.remaining_count += count


    def getattr(self, attribute):
        import pdb; pdb.set_trace()
        if attribute in self.__dict__.keys():
            return self.__dict__[attribute]
        return None


    def __repr__(self):
        display_data = "%s, %s %s - %s" % (self.name, self.locations, self.item, self.remaining_count)
        return display_data


class User(object):

    def __init__(self, username, phone_number, location):
        self.username = username
        self.phone_number = phone_number
        self.location = location


def run_tasks():
    food_cart = FoodCart()
    food_cart.register_user("Pralove", "phoneNumber-1", "HSR")
    food_cart.register_user("Nitesh", "phoneNumber-2", "BTM")
    food_cart.register_user("Vatsal",  "phoneNumber-3", "BTM")

    food_cart.register_restaurant("Food Court-1", ["BTM", "HSR"], "NI Thali", 100, 5)
    food_cart.register_restaurant("Food Court-2", "BTM", "Burger", 120, 3)
    food_cart.register_restaurant("Food Court-3", "HSR", "SI Thali", 150, 1)
    food_cart.register_restaurant("Food Court-4", "HSR", "SI Thali", 200, 1)
    food_cart.register_restaurant("Food Court-5", "HSR", "SI Thali", 400, 1)

    food_cart.show_restaurant("items")

    food_cart.place_order("Nitesh", "Food Court-1", 2)
    food_cart.place_order("Pralove", "Food Court-2", 2)
    food_cart.place_order("Pralove", "Food Court-2", 7)
    food_cart.update_quantity("Food Court-2", 7)
    print("Trying with Quantity")
    food_cart.place_order("Pralove123", "Food Court-2", 7)
    print("Trying with Quantity End")
    food_cart.update_quantity("Food Court-2", 1)


    food_cart.create_review("Nitesh", "Food Court-1", 3)
    food_cart.create_review("Pralove", "Food Court-2", 5)
    food_cart.create_review("Pralove", "Food Court-1", 5)
    food_cart.create_review("Pralove", "Food Court-1", 4)

    food_cart.show_restaurant("rating")
    food_cart.update_quantity("Food Court-2", 5)



if __name__ == "__main__":
    print("*****Running the predefined testcases for FoodKart****")
    run_tasks()
    print("****Test cases ran Successfully.****")