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
    Name = __name__
    Description = 'description'

    def __str__(self):
        return CarMake


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    Name = __name__
    DealerID = id
    Type = ['Sedan', 'SUV', 'Wagon']
    Year = datetime.date

    def __str__(self):
        return CarModel


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