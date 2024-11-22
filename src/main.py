import requests
import pandas as pd
from common import odds_api as oa
import computation.surebet_computation as sc
import computation.implied_odds_computation as ioc
import common.parser as parser
import json

def american_to_decimal(american_odds):
    try:
        # Ensure the odds are numeric by converting strings to integers
        american_odds = int(american_odds)

        # Convert American odds to Decimal format
        if american_odds > 0:
            return (american_odds / 100) + 1
        else:
            return (100 / abs(american_odds)) + 1
    except ValueError:
        # If conversion to integer fails (for example if it's NaN or a non-numeric string)
        return None
    
def get_touchdown_scorers(max_date:str,max_odds:int):
    # Enable the table schema
    pd.set_option("display.notebook_repr_html", True)

    # Set some display options
    pd.set_option("display.max_columns", 15)
    pd.set_option("display.width", 1000)

    # Constants and API configuration
    api_key = "c3400b0bc5c50c231ca7707cb7a7aeb7"
    region = "us"
    mkt = "player_anytime_td"
    sports = "americanfootball_nfl"
   
    odds_api_driver = oa.odds_api(api_key=api_key,sport=sports,region=region,mkt=mkt)

    event_list=odds_api_driver.get_nfl_events()


    game_list=[]
    implied_games_df_list=[]
    for event in event_list:
        if event['commence_time']>max_date:
            continue

        game_id=event['id']
        home_team=event['home_team']
        away_team = event['away_team']
        game_match_up = f'{away_team} at {home_team}'
        game_list.append({'game_id':game_id,'matchup':game_match_up})


        print(game_match_up)

        touchdown_odds=odds_api_driver.get_touchdown_odds({'game_id':game_id,'matchup':game_match_up})

        implied_odds_df=parser.touchdown_bet_parser(touchdown_odds)

        game_implied_odds=ioc.retrieve_implied_odds(implied_odds_df,max_odds)
        implied_games_df_list.append(game_implied_odds)

    money_makers=pd.concat(implied_games_df_list).sort_values(by='Implied_Odds_Diff',ascending=False)

    return(money_makers)

def execute_test():
    # Enable the table schema
    pd.set_option("display.notebook_repr_html", True)

    # Set some display options
    pd.set_option("display.max_columns", 15)
    pd.set_option("display.width", 1000)

    # Constants and API configuration
    api_key = "c3400b0bc5c50c231ca7707cb7a7aeb7"
    region = "us"
    mkt = "player_anytime_td"
    sports = "americanfootball_nfl"
    max_date='2024-11-24T18:00:00Z'
    odds_api_driver = oa.odds_api(api_key=api_key,sport=sports,region=region,mkt=mkt)

    event_list=odds_api_driver.get_nfl_events()
    print(event_list)
    return(event_list)

def get_football_games(max_date):
    # Enable the table schema
    pd.set_option("display.notebook_repr_html", True)

    # Set some display options
    pd.set_option("display.max_columns", 15)
    pd.set_option("display.width", 1000)

    # Constants and API configuration
    api_key = "c3400b0bc5c50c231ca7707cb7a7aeb7"
    region = "us"
    mkt = "player_anytime_td"
    sports = "americanfootball_nfl"

    odds_api_driver = oa.odds_api(api_key=api_key,sport=sports,region=region,mkt=mkt)

    event_list=odds_api_driver.get_nfl_events()

    print(event_list)
    game_list=[]

    for event in event_list:
        if event['commence_time']>max_date:
            continue

        game_id=event['id']
        home_team=event['home_team']
        away_team = event['away_team']
        game_match_up = f'{away_team} at {home_team}'
        game_list.append({'game_id':game_id,'matchup':game_match_up})

    return game_list