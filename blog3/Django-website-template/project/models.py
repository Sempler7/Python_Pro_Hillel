from django.db import models

class TripProfile(models.Model):
    destination_type = models.CharField(
        max_length=50,
        choices=[
            ('пляж', 'Пляж'),
            ('гори', 'Гори'),
            ('місто', 'Місто'),
            ('бізнес', 'Бізнес-поїздка'),
        ]
    )
    season = models.CharField(
        max_length=50,
        choices=[
            ('літо', 'Літо'),
            ('зима', 'Зима'),
            ('дощ', 'Дощовий сезон'),
        ]
    )
    duration = models.CharField(
        max_length=50,
        choices=[
            ('коротка', 'Коротка поїздка'),
            ('тиждень', 'Тиждень'),
            ('місяць', 'Місяць'),
        ]
    )
    with_children = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.destination_type} - {self.season}"
