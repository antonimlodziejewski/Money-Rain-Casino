from django.db import models
from django.contrib.auth.models import AbstractUser, User

STATUS = (
    (1, 'Basic'),
    (2, 'Silver'),
    (3, 'Gold'),
    (4, 'Platinum')
)


class Player(AbstractUser):
    """
    Custom User model representing a player in the casino application.
    """
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
    """
    Model representing a betting activity of a player.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bet_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} - {self.amount}"


class GameResult(models.Model):
    """
    Model representing the result of a casino game played by a player.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    winnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lines = models.IntegerField(default=1)
    bet_per_line = models.IntegerField(default=10)
    spin_results = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wynik gry: Gracz ID {self.player_id}, Wygrana: {self.winnings}$, Linie: {self.lines}, Zakład na linię: {self.bet_per_line}$"


class Deposit(models.Model):
    """
    Model representing a deposit made by a player.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deposit by {self.player.username} - {self.amount}$ at {self.deposit_date}"


class Achievement(models.Model):
    """
    Model representing an achievement unlocked by a player.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    unlocked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Unlocked by: {self.player.username}"
