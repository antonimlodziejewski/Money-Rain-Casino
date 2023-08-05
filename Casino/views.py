from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .form import PlayerRegistrationForm, PlayerBalanceForm
from django.views.generic.edit import CreateView, UpdateView
import random
from .models import Player, Bet, GameResult
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


MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    '$': 2,
    '!': 4,
    '#': 6,
    "@": 8
}

symbol_value = {
    '$': 14,
    '!': 12,
    '#': 8,
    "@": 6
}


class SlotMachineGameView(View):
    template_name = 'slot_machine.html'

    def get(self, request):
        # Default values
        balance = request.user.balance if request.user.is_authenticated else 0

        bet = 10
        lines = 1
        message = ''
        winning_lines = []
        show_winning_lines = False

        context = {
            'balance': balance,
            'bet': bet,
            'lines': lines,
            'message': message,
            'winning_lines': winning_lines,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        balance = request.user.balance if request.user.is_authenticated else 0
        bet = int(request.POST.get('bet', 0))
        lines = int(request.POST.get('lines', 0))

        total_bet = bet * lines
        if total_bet > balance:
            message = 'Nie możesz zbetować więcej niż masz!'
            winnings = 0
            winning_lines = []
        else:
            slots = self.get_slot_spin(ROWS, COLS, symbol_count)
            winnings, winning_lines = self.check_winnings(slots, lines, bet, symbol_value)
            message = f'Wygrałeś {winnings}$!'

            balance += winnings - total_bet

            if request.user.is_authenticated:
                request.user.balance = balance
                request.user.save()

        if winnings > 0:
            show_winning_lines = True
        else:
            show_winning_lines = False

        context = {
            'balance': balance,
            'bet': bet,
            'lines': lines,
            'message': message,
            'winning_lines': winning_lines,
        }
        return render(request, self.template_name, context)

    def get_slot_spin(self, rows, cols, symbols):
        all_symbols = []
        for symbol, symbol_count in symbols.items():
            for _ in range(symbol_count):
                all_symbols.append(symbol)

        columns = []
        for _ in range(cols):
            column = []
            current_symbols = all_symbols[:]
            for _ in range(rows):
                value = random.choice(current_symbols)
                current_symbols.remove(value)
                column.append(value)

            columns.append(column)

        return columns

    def check_winnings(self, columns, lines, total_bet, values):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * total_bet
                winning_lines.append(line + 1)
        return winnings, winning_lines
