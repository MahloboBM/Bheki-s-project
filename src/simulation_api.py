from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Add the parent directory to the Python path so we can import the simulation module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.simulation import gamblers_ruin_simulation

app = FastAPI(title="Gambler's Ruin API")

class SimulationRequest(BaseModel):
    initial_money: float
    goal_money: float
    win_probability: float
    payout: float
    credit_limit: float
    max_bet: float
    num_simulations: int
    allow_borrowing: bool = True

@app.post("/simulate")
async def simulate(request: SimulationRequest):
    """Simulate the gambler's ruin problem

    Args:
        request (SimulationRequest): The request object containing the simulation parameters

    Raises:
        HTTPException: If the simulation fails

    Returns:
        dict: The result of the simulation
    """
    try:
        win_prob, loss_prob = gamblers_ruin_simulation(
            initial_money=request.initial_money,
            goal_money=request.goal_money,
            win_probability=request.win_probability,
            payout=request.payout,
            credit_limit=request.credit_limit,
            max_bet=request.max_bet,
            num_simulations=request.num_simulations,
            allow_borrowing=request.allow_borrowing
        )
        return {
            "win_probability": win_prob,
            "loss_probability": loss_prob
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 