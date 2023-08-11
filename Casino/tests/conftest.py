import pytest
from django.test import Client
from Casino.models import *


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def create_player():
    return Player.objects.create(username="testuser", balance=100)


@pytest.fixture
def create_bet(create_player):
    return Bet.objects.create(player=create_player, amount=50)


@pytest.fixture
def create_game_result(create_player):
    return GameResult.objects.create(player=create_player, winnings=25, lines=2, bet_per_line=5)


@pytest.fixture
def create_deposit(create_player):
    return Deposit.objects.create(player=create_player, amount=200)


@pytest.fixture
def create_achievement(create_player):
    return Achievement.objects.create(player=create_player, name="Test Achievement",
                                      description="Achievement description")
