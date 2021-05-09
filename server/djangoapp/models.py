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
class CarDealer(models.Model):
    Name = __name__
    DealerID = id

    def __str__(self):
        return CarDealer

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    Rate = [1, 2, 3, 4, 5]
    Comment = "Text"

    def __str__(self):
        return DealerReview
