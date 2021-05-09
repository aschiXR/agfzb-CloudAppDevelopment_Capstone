from django.db import models
from django.utils.timezone import now
from datetime  import datetime, time


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=50)
    year = models.DateField()

    SUV = 'suv'
    SEDAN = 'sedan'
    WAGON = 'wagon'
    VAN = 'van'
    PICKUP = 'hatchaback'

    TYPES = [
        (SUV, 'suv'),
        (SEDAN, 'sedan'),
        (WAGON, 'wagon'),
        (VAN, 'van'),
        (PICKUP, 'hatchaback'),
    ]

    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPES,
        default=SEDAN
    )

    def __str__(self):
        return self.make.name + " " + \
               self.name + ", " + \
               str(self.year.year) + "(" + \
               "DealerID: " + str(self.dealer_id) + ")"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id_val, lat, long_val, state, st, zip_val):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id_val
        # Location lat
        self.lat = lat
        # Location long
        self.long = long_val
        # Dealer short name
        self.state = state
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip_val
    def __str__(self):
        return "Dealer name: " + self.full_name + \
                ", City: " + self.city + \
                ", State: " + self.state + \
                ", st: " + self.st

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id_review, dealership, name, \
            purchase, review, purchase_date=None, car_make=None, \
            car_model=None, car_year=None, sentiment=None):
        # Review id
        self.id = id_review
        # Dealership id
        self.dealership = dealership
        # Reviewer name
        self.name = name
        # Reviewer has purchased
        self.purchase = purchase
        # Reviewer review
        self.review = review
        # Reviewer purchase date
        self.purchase_date = purchase_date
        # Car Make
        self.car_make = car_make
        # Car Model
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # Reviewer sentiment
        self.sentiment = sentiment
    def __str__(self):
        return "Reviewer name: " + self.name + \
                ", Dealership: " + str(self.dealership) + \
                ", Review: " + self.review + \
                ", Purchase: " + str(self.purchase) + \
                ", Sentiment: " + str(self.sentiment) + \
                ", Car Make: " + str(self.car_make) + \
                ", Car Model: " + str(self.car_model)
