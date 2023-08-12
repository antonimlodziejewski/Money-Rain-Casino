import pytest
from Casino.models import Player
from django.urls import reverse


@pytest.mark.django_db
def test_CasinoView(client):
    """
    Tests whether the CasinoView (home page) is accessible and returns a status code of 200 (OK).
    """
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_CasinoView(client):
    """
    Tests whether the home page (view 'home') is accessible and returns a status code of 200 (OK).
    """
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_PlayerRegistrationView(client):
    """
    Tests whether the registration page (view 'registration') is accessible and returns a status code of 200 (OK).
    """
    response = client.get(reverse('registration'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_CustomLogoutView(client):
    """
    Tests whether logging out a user via a POST request (view 'logout') redirects to another page,
    which is expected behavior for an authenticated user.
    """
    response = client.post(reverse('logout'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_PlayerBalanceUpdateView(client, create_player):
    """
    Tests whether the player balance update page (view 'balance') is accessible and returns a status code of 200 (OK)
    after authenticating the player.
    """
    client.force_login(create_player)
    response = client.get(reverse('balance'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_SlotMachineGameView_get(client):
    """
    Tests whether the slot machine game page (view 'slot_machine_game') is accessible and returns a status code of 200 (OK)
    for a GET request.
    """
    response = client.get(reverse('slot_machine_game'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_SlotMachineGameView_post(client):
    """
    Tests whether the slot machine game page (view 'slot_machine_game') is accessible and returns a status code of 200 (OK)
    for a POST request.
    """
    response = client.post(reverse('slot_machine_game'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_deposit_history(client, create_player):
    """
    Tests whether the deposit history page (view 'deposit-history') is accessible and returns a status code of 200 (OK)
    after authenticating the player.
    """
    client.force_login(create_player)
    response = client.get(reverse('deposit-history'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_bet_history(client, create_player):
    """
    Tests whether the bet history page (view 'bet-history') is accessible and returns a status code of 200 (OK)
    after authenticating the player.
    """
    client.force_login(create_player)
    response = client.get(reverse('bet-history'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_winnings_history(client, create_player):
    """
    Tests whether the winnings history page (view 'win-history') is accessible and returns a status code of 200 (OK)
    after authenticating the player.
    """
    client.force_login(create_player)
    response = client.get(reverse('win-history'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_PlayerDeleteView(client, create_player):
    """
    Tests whether the player delete page (view 'player-delete') is accessible and returns a status code of 200 (OK)
    after authenticating the player.
    """
    client.force_login(create_player)
    response = client.get(reverse('player-delete'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_achievements(client, create_player):
    """
    Tests whether the player achievements page (view 'achievements') is accessible and returns a status code of 200 (OK)
    after authenticating the player.
    """
    client.force_login(create_player)
    response = client.get(reverse('achievements'))
    assert response.status_code == 200
