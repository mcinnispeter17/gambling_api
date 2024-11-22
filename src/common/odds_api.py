
import requests


class odds_api():
    def __init__(self,api_key:str,sport:str,region:str,mkt:str):
        self._api_key=api_key
        self._sport=sport
        self._region=region
        self._mkt=mkt
        self._h2h_odds_api_url=f"https://api.the-odds-api.com/v3/odds/?apiKey={api_key}&sport={sport}&region={region}&mkt={mkt}"
        self.events_api_url=f"https://api.the-odds-api.com/v4/sports/{sport}/events?apiKey={api_key}"
        #self._nfl_player_prop_api_url=f"https://api.the-odds-api.com/v4/sports/{sport}/events/{eventId}/odds?apiKey={apiKey}&regions={regions}&markets={markets}&oddsFormat=american"

    def get_nfl_events(self):
        response = requests.get(self.events_api_url)
        if response.status_code != 200:
            print(f"Error: Request for {self._sport} returned status code {response.status_code}.")
            return 
        print('Remaining requests', response.headers['x-requests-remaining'])
        print('Used requests', response.headers['x-requests-used'])
        data = response.json()
        
        return data
    
    def get_odds(self) -> str:
        response = requests.get(self._odds_api_url)

        if response.status_code != 200:
            print(f"Error: Request for {self._sport} returned status code {response.status_code}.")
            return 

        data = response.json()

        if 'data' not in data:
            print(f"No data found for {self._sport}.")
            return 'None'
        
        return data
    
    def get_touchdown_odds(self, game_info) -> str:
        event_touchdown_api_url=f"https://api.the-odds-api.com/v4/sports/{self._sport}/events/{game_info.get('game_id')}/odds?apiKey={self._api_key}&regions={self._region}&markets={self._mkt}&oddsFormat=american"

        response = requests.get(event_touchdown_api_url)

        if response.status_code != 200:
            print(f"Error: Request for {game_info.get('matchup')} returned status code {response.status_code}.")
            return 

        data = response.json()

        return data