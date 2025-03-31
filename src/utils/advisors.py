import random
from .simulation import gamblers_ruin_simulation

def get_angel_message(money, initial_money, goal_money, win_probability, losing_streak, credit_used, allow_borrowing):
    messages = []
    
    # Basic probability explanation
    if st.session_state.total_bets == 0:
        messages.append(f"With a win probability of {win_probability:.1%} per bet, your expected value per $1 bet is ${win_probability*2-1:.2f}. This means on average, you'll lose ${1-win_probability*2:.2f} per dollar bet.")
    
    # Losing streak advice
    if losing_streak >= 3:
        messages.append(f"You're on a {losing_streak} bet losing streak. The probability of this happening by chance is about {(1-win_probability)**losing_streak:.2%}. Many gamblers fall into the trap of increasing bets to 'recover' losses, but this increases your risk.")
    
    # Credit warning
    if allow_borrowing and credit_used > 0:
        messages.append(f"You're currently using ${credit_used:.2f} of credit. Statistically, borrowing to continue gambling typically leads to deeper losses.")
    
    # Overall position
    if money < initial_money:
        win_prob, _ = gamblers_ruin_simulation(money, goal_money, win_probability, 2, credit_limit, max_bet, 1000, allow_borrowing)
        messages.append(f"You're down ${initial_money-money:.2f} from your starting amount. Based on simulations, your probability of reaching your goal from here is about {win_prob:.1%}.")
    elif money > initial_money:
        messages.append(f"You're up ${money-initial_money:.2f} from your starting amount. Many successful gamblers would consider walking away with a profit.")
    
    # Random educational insights
    if st.session_state.total_bets % 5 == 0 and st.session_state.total_bets > 0:
        insights = [
            "The Gambler's Ruin problem shows that with enough bets, a player with finite resources against an opponent with infinite resources will eventually go broke.",
            f"With your current win probability of {win_probability:.1%}, the house has a mathematical edge. Over time, this edge guarantees the casino's profit.",
            "Betting systems like Martingale (doubling after losses) don't change the expected value - they just trade frequent small wins for rare catastrophic losses.",
            "The longer you play, the more likely your results will approach the mathematical expectation, which favors the house."
        ]
        messages.append(random.choice(insights))
    
    return random.choice(messages) if messages else "Watch your bankroll and set clear limits for yourself."

def get_dealer_message(money, initial_money, goal_money, win_probability, losing_streak, last_win):
    messages = []
    
    # Encouraging continued play
    if money > initial_money:
        messages.append("You're on a hot streak! The big win could be just around the corner.")
        messages.append("You've got the touch today! Why stop when you're winning?")
    
    # After a win
    if last_win:
        messages.append("Nice win! That's how it starts - feeling lucky today?")
        messages.append("Winner! I can feel it - you're due for an even bigger win next!")
    
    # After a loss or losing streak
    if losing_streak >= 2:
        messages.append(f"Don't worry about that {losing_streak}-loss streak. Your luck is bound to turn around!")
        messages.append("The machine is just warming up. The longer it doesn't pay, the bigger the payout coming!")
    
    # When close to goal
    if money > goal_money * 0.8:
        messages.append(f"You're so close to your ${goal_money} goal! Just a few more spins!")
    
    # When using credit
    if money == 0:
        messages.append("That's what our credit line is for - the comeback is always bigger than the setback!")
    
    # Generic encouragement
    generic = [
        "One more spin - I've got a good feeling about this one!",
        "The big jackpot always hits when you least expect it.",
        "I've seen players turn $1 into thousands in just a few spins!",
        "The machine feels hot today, don't miss out!",
        "Players who stick with it are the ones who hit the big wins!"
    ]
    messages.extend(generic)
    
    return random.choice(messages) 