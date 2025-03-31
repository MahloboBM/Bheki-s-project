import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
import time
from PIL import Image  # If you need image processing

st.set_page_config(page_title="Bheki's project", layout="wide")

# Custom CSS to style the app
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #FF9900;
        text-align: center;
        margin-bottom: 1rem;
    }
    .slot-machine {
        background-color: #333;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .slot-display {
        background-color: #222;
        border-radius: 5px;
        padding: 10px;
        color: white;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 10px;
    }
    .win {
        color: #00FF00;
        font-weight: bold;
    }
    .lose {
        color: #FF0000;
        font-weight: bold;
    }
    .angel {
        background-color: #e6f7ff;
        border-left: 5px solid #1890ff;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .dealer {
        background-color: #ffe6e6;
        border-left: 5px solid #ff4d4f;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    @keyframes spin {
        0% { transform: translateY(0); }
        100% { transform: translateY(-50px); }
    }
    
    .spinning {
        animation: spin 0.2s linear infinite;
    }
    
    .slot-symbol {
        display: inline-block;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>🎰 Gambler's Ruin Simulator 🎰</h1>", unsafe_allow_html=True)

# Define the simulation functions
def gamblers_ruin_simulation(initial_money, goal_money, win_probability, payout,
                            credit_limit, max_bet, num_simulations, allow_borrowing=True):
    """
    Simulate the gambler's ruin problem
    """
    wins = 0
    losses = 0
    
    for _ in range(num_simulations):
        money = initial_money
        credit_used = 0
        losing_streak = 0
        
        while (allow_borrowing and money + credit_limit - credit_used > 0 and money < goal_money) or \
              (not allow_borrowing and money > 0 and money < goal_money):
            # Calculate bet size based on losing streak
            if losing_streak == 0:
                base_bet = 1  # Start with minimum bet
            else:
                # Increase bet by factor 1/p for each level of losing streak
                base_bet = 1 * (1/win_probability) ** losing_streak

            # Apply maximum bet limit
            current_bet = min(base_bet, max_bet)
            
            # Make sure we don't bet more than we have
            if allow_borrowing:
                available_funds = money + (credit_limit - credit_used)
            else:
                available_funds = money

            current_bet = min(current_bet, available_funds)
            
            # If we need to use credit for this bet
            if allow_borrowing and current_bet > money:
                credit_needed = current_bet - money
                credit_used += credit_needed
                money = 0
            
            # Determine if the gambler wins or loses
            if random.random() < win_probability:
                # Win: add payout times the bet
                winnings = current_bet * (payout - 1)
                money += winnings
                
                # Pay back credit if we have any
                if allow_borrowing and credit_used > 0:
                    payback = min(money, credit_used)
                    money -= payback
                    credit_used -= payback
                
                # Reset losing streak
                losing_streak = 0
            else:
                # Lose: lose the bet amount
                money -= current_bet
                # Increase losing streak
                losing_streak += 1
        
        if money >= goal_money:
            wins += 1
        else:
            losses += 1
    
    win_probability = wins / num_simulations
    loss_probability = losses / num_simulations
    
    return win_probability, loss_probability

def run_single_bet(money, credit_used, losing_streak, win_probability, payout, credit_limit, max_bet, allow_borrowing=True):
    """Run a single bet and return the updated state"""
    # Calculate bet size based on losing streak
    if losing_streak == 0:
        base_bet = 1
    else:
        base_bet = 1 * (1/win_probability) ** losing_streak
    
    # Apply maximum bet limit
    current_bet = min(base_bet, max_bet)
    
    # Make sure we don't bet more than we have
    if allow_borrowing:
        available_funds = money + (credit_limit - credit_used)
    else:
        available_funds = money
        
    current_bet = min(current_bet, available_funds)
    
    # If we need to use credit for this bet
    if allow_borrowing and current_bet > money:
        credit_needed = current_bet - money
        credit_used += credit_needed
        money = 0
    
    # Determine if the gambler wins or loses
    win = random.random() < win_probability
    
    if win:
        # Win
        winnings = current_bet * (payout - 1)
        money += winnings
        
        # Pay back credit if we have any
        if allow_borrowing and credit_used > 0:
            payback = min(money, credit_used)
            money -= payback
            credit_used -= payback
        
        # Reset losing streak
        losing_streak = 0
    else:
        # Lose
        money -= current_bet
        # Increase losing streak
        losing_streak += 1
    
    return money, credit_used, losing_streak, current_bet, win

# Create slot machine symbols
def get_slot_symbols():
    symbols = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣", "🎰"]
    return random.choices(symbols, k=3)

# Add the animation function here
def animate_spin():
    """Animate the slot machine spinning"""
    animation_frames = 5  # Number of animation frames
    animation_symbols = ["🎰", "💎", "7️⃣", "🍒", "🍊", "🍋", "🍇"]
    
    for _ in range(animation_frames):
        # Generate random symbols for animation frame
        st.session_state.last_symbols = random.choices(animation_symbols, k=3)
        time.sleep(0.2)  # Delay between frames
        st.rerun()

# Angel advisor messages
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

# Dealer messages
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

# Sidebar for simulation parameters
st.sidebar.header("Game Settings")

initial_money = st.sidebar.slider("Starting Amount ($)", 1, 100, 10)
goal_money = st.sidebar.slider("Goal Amount ($)", initial_money + 10, 500, 50)
win_probability = st.sidebar.slider("Win Probability", 0.1, 0.9, 0.45, 0.05)
payout = st.sidebar.slider("Payout Multiplier", 1.1, 5.0, 2.0, 0.1)
allow_borrowing = st.sidebar.checkbox("Allow Borrowing", True)
credit_limit = st.sidebar.slider("Credit Limit ($)", 0, 100, 20, disabled=not allow_borrowing)
max_bet = st.sidebar.slider("Maximum Bet ($)", 1, 50, 10)

# Run simulation for statistics
if 'simulation_results' not in st.session_state or st.sidebar.button("Calculate Odds"):
    with st.spinner("Calculating probabilities..."):
        win_prob, loss_prob = gamblers_ruin_simulation(
            initial_money, 
            goal_money, 
            win_probability, 
            payout, 
            credit_limit, 
            max_bet, 
            5000,
            allow_borrowing
        )
        st.session_state.simulation_results = (win_prob, loss_prob)
        st.sidebar.success(f"Probability of reaching ${goal_money} goal: {win_prob:.1%}")
        st.sidebar.error(f"Probability of going broke: {loss_prob:.1%}")

# Main content area
col1, col2 = st.columns([3, 2])

# Initialize session state if not already done
if 'money' not in st.session_state:
    st.session_state.money = initial_money
    st.session_state.credit_used = 0
    st.session_state.losing_streak = 0
    st.session_state.history = [initial_money]
    st.session_state.total_bets = 0
    st.session_state.total_wins = 0
    st.session_state.total_losses = 0
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.allow_borrowing = allow_borrowing
    st.session_state.last_win = None

# Check if borrowing setting changed
if st.session_state.allow_borrowing != allow_borrowing:
    st.session_state.allow_borrowing = allow_borrowing
    # Reset game if borrowing setting changed
    st.session_state.money = initial_money
    st.session_state.credit_used = 0
    st.session_state.losing_streak = 0
    st.session_state.history = [initial_money]
    st.session_state.total_bets = 0
    st.session_state.total_wins = 0
    st.session_state.total_losses = 0
    st.session_state.game_over = False
    st.session_state.game_won = False

# Reset button
if st.sidebar.button("Reset Game"):
    st.session_state.money = initial_money
    st.session_state.credit_used = 0
    st.session_state.losing_streak = 0
    st.session_state.history = [initial_money]
    st.session_state.total_bets = 0
    st.session_state.total_wins = 0
    st.session_state.total_losses = 0
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.allow_borrowing = allow_borrowing
    st.session_state.last_win = None

# Slot machine display in the left column
with col1:
    st.markdown("<div class='slot-machine'>", unsafe_allow_html=True)
    
    # Display current money and credit
    st.markdown(f"<div class='slot-display'>Balance: ${st.session_state.money:.2f}</div>", unsafe_allow_html=True)
    if allow_borrowing and st.session_state.credit_used > 0:
        st.markdown(f"<div class='slot-display'>Credit Used: ${st.session_state.credit_used:.2f}</div>", unsafe_allow_html=True)
    
    # Calculate current bet
    if st.session_state.losing_streak == 0:
        base_bet = 1
    else:
        base_bet = 1 * (1/win_probability) ** st.session_state.losing_streak
    
    current_bet = min(base_bet, max_bet)
    
    if allow_borrowing:
        available_funds = st.session_state.money + (credit_limit - st.session_state.credit_used)
    else:
        available_funds = st.session_state.money
        
    current_bet = min(current_bet, available_funds)
    
    # Display current bet
    st.markdown(f"<div class='slot-display'>Current Bet: ${current_bet:.2f}</div>", unsafe_allow_html=True)
    
    # Borrowing status
    borrowing_status = "Enabled" if allow_borrowing else "Disabled"
    st.markdown(f"<div class='slot-display' style='font-size: 1rem;'>Borrowing: {borrowing_status}</div>", unsafe_allow_html=True)
    
    # Slot symbols display
    if 'last_symbols' not in st.session_state:
        st.session_state.last_symbols = ["🎰", "🎰", "🎰"]
    
    symbols_display = " ".join([
        f"<span class='slot-symbol {('spinning' if getattr(st.session_state, 'is_spinning', False) else '')}' style='font-size: 3.5rem;'>{s}</span>" 
        for s in st.session_state.last_symbols
    ])
    st.markdown(f"<div style='text-align: center; margin: 20px 0;'>{symbols_display}</div>", unsafe_allow_html=True)
    
    # Win/lose message
    if st.session_state.last_win is not None:
        if st.session_state.last_win:
            st.markdown("<div class='slot-display win'>WIN!</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='slot-display lose'>LOSE</div>", unsafe_allow_html=True)
    
    # Game over message
    if st.session_state.game_over:
        if st.session_state.game_won:
            st.markdown("<div class='slot-display win'>GOAL REACHED! 🎉</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='slot-display lose'>BANKRUPT! 💸</div>", unsafe_allow_html=True)
    
    # Spin button
    spin_disabled = st.session_state.game_over or (not allow_borrowing and st.session_state.money <= 0) or \
                   (allow_borrowing and st.session_state.money + credit_limit - st.session_state.credit_used <= 0)
    
    if st.button("SPIN", key="spin_button", use_container_width=True, disabled=spin_disabled):
        # Set spinning state
        if 'is_spinning' not in st.session_state:
            st.session_state.is_spinning = True
            animate_spin()
        
        # Run a single bet
        money, credit_used, losing_streak, bet, win = run_single_bet(
            st.session_state.money, 
            st.session_state.credit_used,
            st.session_state.losing_streak,
            win_probability,
            payout,
            credit_limit,
            max_bet,
            allow_borrowing
        )
        
        # Update session state
        st.session_state.money = money
        st.session_state.credit_used = credit_used
        st.session_state.losing_streak = losing_streak
        st.session_state.history.append(money)
        st.session_state.total_bets += 1
        
        if win:
            st.session_state.total_wins += 1
            st.session_state.last_symbols = ["7️⃣", "7️⃣", "7️⃣"]
        else:
            st.session_state.total_losses += 1
            st.session_state.last_symbols = get_slot_symbols()
        
        st.session_state.last_win = win
        st.session_state.is_spinning = False
        
        # Check if game is over
        if money >= goal_money:
            st.session_state.game_over = True
            st.session_state.game_won = True
        elif (not allow_borrowing and money <= 0) or (allow_borrowing and money + credit_limit - credit_used <= 0):
            st.session_state.game_over = True
            st.session_state.game_won = False

        st.rerun()

# Add this to display advisor messages in col2
with col2:
    st.markdown("### Advisors")
    
    # Angel's advice
    st.markdown("<div class='angel'>", unsafe_allow_html=True)
    st.markdown("👼 **Guardian Angel Says:**", unsafe_allow_html=True)
    angel_message = get_angel_message(
        st.session_state.money,
        initial_money,
        goal_money,
        win_probability,
        st.session_state.losing_streak,
        st.session_state.credit_used,
        allow_borrowing
    )
    st.markdown(f"_{angel_message}_", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Dealer's message
    st.markdown("<div class='dealer'>", unsafe_allow_html=True)
    st.markdown("😈 **Casino Dealer Says:**", unsafe_allow_html=True)
    dealer_message = get_dealer_message(
        st.session_state.money,
        initial_money,
        goal_money,
        win_probability,
        st.session_state.losing_streak,
        st.session_state.last_win
    )
    st.markdown(f"_{dealer_message}_", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add some statistics
    st.markdown("### Statistics")
    st.markdown(f"Total Bets: {st.session_state.total_bets}")
    st.markdown(f"Wins: {st.session_state.total_wins}")
    st.markdown(f"Losses: {st.session_state.total_losses}")
    if st.session_state.total_bets > 0:
        win_rate = st.session_state.total_wins / st.session_state.total_bets
        st.markdown(f"Win Rate: {win_rate:.1%}")
