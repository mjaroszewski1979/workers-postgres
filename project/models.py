from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class WorkerManager(models.Manager):
    
    def get_average_age(self):
        self.results = {}
        professions = list(self.values_list('profession', flat=True).distinct())
        for prof in professions:
            nums = list(self.filter(profession=prof).values_list('age', flat=True))
            self.results[prof] = int(sum(nums) / len(nums))
            self.average = self.results.items()
        try:
            return self.average
        except AttributeError:
            return None

class Worker(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(200)])
    image = models.ImageField(upload_to ='uploads/', null=True, blank=True)
    objects = WorkerManager()

    class Meta:
        ordering = ['surname']

    def __str__(self):
        return self.name



