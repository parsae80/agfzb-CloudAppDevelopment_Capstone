from django.db import models
from django.utils.timezone import now



class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = [
        ("Sedan", "sedan"),
        ("SUV","SUV"),
        ("WAGON", "Wagon"),
    ]
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    dealerId = models.CharField(max_length = 50)
    carType = models.CharField(max_length = 50, choices=CAR_TYPES)
    year = models.DateField()

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# class CarDealer(models.Model):
     

# <HINT> Create a plain Python class `DealerReview` to hold review data
