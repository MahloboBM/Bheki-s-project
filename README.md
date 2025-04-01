# Gambler's Ruin Simulation

This project simulates the gambler's ruin problem, exploring different betting strategies and their outcomes.

## Features

- Simulate gambler's ruin scenarios with various parameters
- Support for credit-based betting
- Configurable betting strategies
- Interactive visualization of results
- REST API for programmatic access

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gamblers-ruin
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Streamlit App

To run the interactive web interface:

```bash
streamlit run src/app.py
```

### Using the API

The project includes a REST API for programmatic access to the simulation. To run the API server:

```bash
python src/api/simulation_api.py
```

The API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.

#### Example API Request

Using curl:
```bash
curl -X POST "http://localhost:8000/simulate" \
     -H "Content-Type: application/json" \
     -d '{
           "initial_money": 100,
           "goal_money": 200,
           "win_probability": 0.5,
           "payout": 2.0,
           "credit_limit": 50,
           "max_bet": 20,
           "num_simulations": 1000,
           "allow_borrowing": true
         }'
```

The API will return a JSON response with:
- `win_probability`: Probability of reaching the goal
- `loss_probability`: Probability of losing all money

## Project Structure

```
gamblers-ruin/
├── src/
│   ├── app.py              # Streamlit web interface
│   ├── api/
│   │   └── simulation_api.py  # FastAPI server
│   └── utils/
│       └── simulation.py   # Core simulation logic
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.