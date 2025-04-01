import streamlit as st
from utils.simulation import gamblers_ruin_simulation, run_single_bet
from utils.advisors import get_angel_message, get_dealer_message
from components.slot_machine import display_slot_machine, animate_spin, get_slot_symbols
from styles.styles import get_css

# Set page config
st.set_page_config(page_title="Bheki's project", layout="wide")

# Apply custom CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>🎰 Gambler's Ruin Simulator 🎰</h1>", unsafe_allow_html=True)

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
    spin_button = display_slot_machine(
        st.session_state.money,
        st.session_state.credit_used,
        st.session_state.losing_streak,
        win_probability,
        max_bet,
        allow_borrowing,
        credit_limit,
        st.session_state.last_win,
        st.session_state.game_over,
        st.session_state.game_won
    )
    
    if spin_button:
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