def get_css():
    """Return the CSS styles for the application"""
    return """
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
    """ 