import random

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