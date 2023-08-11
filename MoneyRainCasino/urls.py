"""
URL configuration for MoneyRainCasino project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Casino.views import CasinoView, PlayerRegistrationView, CustomLoginView, CustomLogoutView, PlayerBalanceUpdateView, \
    SlotMachineGameView, deposit_history, bet_history, winnings_history, PlayerDeleteView, achievements

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CasinoView.as_view(), name='home'),
    path('registration/', PlayerRegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('add_balance/', PlayerBalanceUpdateView.as_view(), name='balance'),
    path('slot_machine/', SlotMachineGameView.as_view(), name='slot_machine_game'),
    path('deposit_history/', deposit_history, name='deposit-history'),
    path('bet_history/', bet_history, name='bet-history'),
    path('winnings_history/', winnings_history, name='win-history'),
    path('delete_account', PlayerDeleteView.as_view(), name='player-delete'),
    path('achievements', achievements, name='achievements'),
]
