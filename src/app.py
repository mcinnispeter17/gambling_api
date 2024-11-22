from fastapi import FastAPI
import pandas as pd
import main as main


app = FastAPI()

class InputData():
    api_key: str
    region: str
    mkt: str
    sports: str
    max_date: str


@app.get("/")
async def read_root():
    return {"health_check": "OK", "model_version": 1}

@app.get("/get_football_games")
async def get_football_games(max_date:str):

        game_list=main.get_football_games(max_date)
        return {"Game List ": game_list}

@app.get("/get_touchdown_scorers")
async def get_touchdown_scorers(max_date:str,max_odds:int):

        tocuhdown_scorer_list=main.get_touchdown_scorers(max_date,max_odds)
        return {"TouchDown List ": tocuhdown_scorer_list.to_string()}
        

#cd src 
#python -m uvicorn app:app --reload (I was in a env?)