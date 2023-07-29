from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .form import PlayerRegistrationForm, PlayerBalanceForm
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
import random
from .models import Player
from django.contrib.auth.views import LoginView, LogoutView


class CasinoView(View):
    def get(self, request):
        return render(request, 'base.html')


class PlayerRegistrationView(CreateView):
    model = Player
    form_class = PlayerRegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('home')
        else:
            return reverse_lazy('login')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class PlayerBalanceUpdateView(UpdateView):
    model = Player
    form_class = PlayerBalanceForm
    template_name = 'player_balance_update.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        player = form.instance
        previous_balance = Player.objects.get(pk=player.pk).balance
        new_balance = form.cleaned_data['balance']
        updated_balance = previous_balance + new_balance
        player.balance = updated_balance
        player.save()

        return super().form_valid(form)


