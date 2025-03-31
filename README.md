# Gambler's Ruin Simulator

An interactive web application that demonstrates the Gambler's Ruin problem through a slot machine simulation. Built with Streamlit and Python.

## Features

- Interactive slot machine interface
- Customizable game parameters
- Real-time probability calculations
- Guardian Angel advisor with mathematical insights
- Casino Dealer with typical gambling fallacies
- Visual statistics and tracking
- Credit system simulation

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Bheki-s-project.git
cd Bheki-s-project
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run main.py
```

## How to Use

1. Adjust the game settings in the sidebar:
   - Starting Amount: Your initial money
   - Goal Amount: The amount you want to reach
   - Win Probability: Chance of winning each bet
   - Payout Multiplier: How much you win on a successful bet
   - Borrowing Options: Enable/disable credit system
   - Maximum Bet: Cap on bet size

2. Click the "SPIN" button to play
3. Watch the advisors for different perspectives:
   - Guardian Angel: Provides mathematical insights and warnings
   - Casino Dealer: Demonstrates common gambling fallacies
4. Track your progress with the statistics panel

## Educational Purpose

This simulator is designed to demonstrate:
- The mathematics behind gambling
- Common gambling fallacies
- The impact of house edge
- Risk of borrowing while gambling
- Importance of responsible gambling

## License

MIT License