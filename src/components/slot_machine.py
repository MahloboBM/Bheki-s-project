import random
import streamlit as st
import time

def get_slot_symbols():
    """Get random slot machine symbols"""
    symbols = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣", "🎰"]
    return random.choices(symbols, k=3)

def animate_spin():
    """Animate the slot machine spinning"""
    animation_frames = 5  # Number of animation frames
    animation_symbols = ["🎰", "💎", "7️⃣", "🍒", "🍊", "🍋", "🍇"]
    
    for _ in range(animation_frames):
        # Generate random symbols for animation frame
        st.session_state.last_symbols = random.choices(animation_symbols, k=3)
        time.sleep(0.2)  # Delay between frames
        st.rerun()

def display_slot_machine(money, credit_used, losing_streak, win_probability, max_bet, 
                        allow_borrowing, credit_limit, last_win, game_over, game_won):
    """Display the slot machine interface"""
    st.markdown("<div class='slot-machine'>", unsafe_allow_html=True)
    
    # Display current money and credit
    st.markdown(f"<div class='slot-display'>Balance: ${money:.2f}</div>", unsafe_allow_html=True)
    if allow_borrowing and credit_used > 0:
        st.markdown(f"<div class='slot-display'>Credit Used: ${credit_used:.2f}</div>", unsafe_allow_html=True)
    
    # Calculate current bet
    if losing_streak == 0:
        base_bet = 1
    else:
        base_bet = 1 * (1/win_probability) ** losing_streak
    
    current_bet = min(base_bet, max_bet)
    
    if allow_borrowing:
        available_funds = money + (credit_limit - credit_used)
    else:
        available_funds = money
        
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
    if last_win is not None:
        if last_win:
            st.markdown("<div class='slot-display win'>WIN!</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='slot-display lose'>LOSE</div>", unsafe_allow_html=True)
    
    # Game over message
    if game_over:
        if game_won:
            st.markdown("<div class='slot-display win'>GOAL REACHED! 🎉</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='slot-display lose'>BANKRUPT! 💸</div>", unsafe_allow_html=True)
    
    # Spin button
    spin_disabled = game_over or (not allow_borrowing and money <= 0) or \
                   (allow_borrowing and money + credit_limit - credit_used <= 0)
    
    return st.button("SPIN", key="spin_button", use_container_width=True, disabled=spin_disabled) 