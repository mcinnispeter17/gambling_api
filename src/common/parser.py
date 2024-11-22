import json
import pandas as pd
from pybettor import implied_prob

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
    
def touchdown_bet_parser(touchdown_json:str):
    events=[]
    event=touchdown_json
    #for event in json.loads(touchdown_json):

    event_id = event['id']
    sport_key = event['sport_key']
    sport_title = event['sport_title']
    commence_time = event['commence_time']
    home_team = event['home_team']
    away_team = event['away_team']

    for bookmaker in event['bookmakers']:
        bookmaker_key = bookmaker['key']
        bookmaker_title = bookmaker['title']

        for market in bookmaker['markets']:
            if market['key'] == 'player_anytime_td':
                for outcome in market['outcomes']:
                    player = outcome['description']
                    price = outcome['price']
                    price_dec = american_to_decimal(price)
                    implied_odds=implied_prob(price_dec,"dec")[0]

                    # Append each record to the events list
                    events.append([event_id, sport_key, sport_title, commence_time, home_team, away_team, 
                                bookmaker_key, bookmaker_title, player, price,price_dec,implied_odds])

    # Create a DataFrame from the events list
    columns = ['Event ID', 'Sport Key', 'Sport Title', 'Commence Time', 'Home Team', 'Away Team', 
            'Bookmaker Key', 'Bookmaker Title', 'Player', 'Price', 'Price_Decimal','Implied_Odds']
    df = pd.DataFrame(events, columns=columns)

    return df
