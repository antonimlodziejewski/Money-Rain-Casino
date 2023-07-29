from django.db import models
from django.contrib.auth.models import AbstractUser, User

STATUS = (
    (1, 'Basic'),
    (2, 'Silver'),
    (3, 'Gold'),
    (4, 'Platinum')
)


class Player(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_winnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_losses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.IntegerField(choices=STATUS, default=1)
    experience_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username


class Bet(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bet_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} - {self.amount}"


