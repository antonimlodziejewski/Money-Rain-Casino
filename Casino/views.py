from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .form import PlayerRegistrationForm, PlayerBalanceForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from .models import Player, Bet, GameResult, Deposit, Achievement
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.db.models import Q


class CasinoView(View):
    """View for rendering the main casino page."""
    def get(self, request):
        return render(request, 'base.html')


class PlayerRegistrationView(CreateView):
    """View for player registration."""
    model = Player
    form_class = PlayerRegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    """Custom login view with redirection for authenticated users."""
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('home')
        else:
            return reverse_lazy('login')


class CustomLogoutView(LogoutView):
    """Custom logout view with redirection to the home page."""
    next_page = reverse_lazy('home')


class PlayerBalanceUpdateView(UpdateView):
    """View for updating player's balance and handling achievements."""
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

        deposit_amount = new_balance
        Deposit.objects.create(player=player, amount=deposit_amount)

        existing_achievements = player.achievement_set.values_list('name', flat=True)

        if 10000 <= deposit_amount <= 99999 and 'VIP Achievement' not in existing_achievements:
            Achievement.objects.create(
                player=player,
                name="VIP Achievement",
                description="You've paid between $10,000 and $99,999 at once and unlocked the VIP achievement!",
            )
        elif deposit_amount >= 100000 and 'SUPERVIP Achievement' not in existing_achievements:
            Achievement.objects.create(
                player=player,
                name='SUPERVIP Achievement',
                description="Congratulations! You've paid $100,000 or more at once and unlocked the SUPERVIP achievement!",
            )

        return super().form_valid(form)


MAX_LINES = 3
MAX_BET = 300
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
    """View for the slot machine game."""
    template_name = 'slot_machine.html'

    def get(self, request):
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
            'MAX_LINES': MAX_LINES,
            'MIN_BET': MIN_BET,
            'MAX_BET': MAX_BET,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        balance = request.user.balance if request.user.is_authenticated else 0
        bet = int(request.POST.get('bet', 0))
        lines = int(request.POST.get('lines', 0))

        total_bet = bet * lines
        if total_bet > balance:
            message = "You can't bet more than u have!"
            winnings = 0
            winning_lines = []
        else:
            slots = self.get_slot_spin(ROWS, COLS, symbol_count)
            winnings, winning_lines = self.check_winnings(slots, lines, bet, symbol_value)
            message = f'You won {winnings}$!'

            balance += winnings - total_bet

            if request.user.is_authenticated:
                request.user.balance = balance
                request.user.save()

                game_result = GameResult.objects.create(
                    player=request.user,
                    winnings=winnings,
                    lines=lines,
                    bet_per_line=bet,
                    spin_results=slots
                )
                game_result.save()

                Bet.objects.create(player=request.user, amount=total_bet)

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
            'MAX_LINES': MAX_LINES,
            'MIN_BET': MIN_BET,
            'MAX_BET': MAX_BET,
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


@login_required
def deposit_history(request):
    """View for displaying deposit history of the logged-in player."""
    deposits = Deposit.objects.filter(player=request.user).order_by('-deposit_date')
    return render(request, 'deposit_history.html', {'deposits': deposits})


@login_required
def bet_history(request):
    """View for displaying bet history of the logged-in player."""
    bets = Bet.objects.filter(player=request.user).order_by('-bet_date')
    return render(request, 'bet_history.html', {'bets': bets})


@login_required
def winnings_history(request):
    """View for displaying winnings history of the logged-in player."""
    winnings = GameResult.objects.filter(
        Q(player=request.user) & Q(winnings__gt=0)
    ).order_by('-created_at')
    return render(request, 'winnings_history.html', {'winnings': winnings})


class PlayerDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting the player's account."""
    model = Player
    template_name = 'user_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_to_delete'] = self.request.user
        return context


@login_required
def achievements(request):
    """View for displaying the achievements of the logged-in player."""
    player_achievements = Achievement.objects.filter(player=request.user).order_by('-unlocked_date')
    return render(request, 'achievements.html', {'player_achievements': player_achievements})
