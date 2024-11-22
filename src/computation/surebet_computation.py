def compute_surebet(odds_a, odds_b):
    implied_prob_a = 1 / odds_a
    implied_prob_b = 1 / odds_b
    total_implied_prob = implied_prob_a + implied_prob_b

    if total_implied_prob < 1:
        profit_percentage = (1 - total_implied_prob) * 100
        investment = 1000

        bet_a = (investment * implied_prob_a) / odds_a
        bet_b = (investment * implied_prob_b) / odds_b

        return profit_percentage, bet_a, bet_b
    else:
        return None, None, None
    

def fetch_surebets_h2h(data):

    # Calculate surebets
    surebets = []
    all_games = []

    for event in data["data"]:
            team_a, team_b = event["teams"]
            odds_list = []

            for site in event["sites"]:
                odds = site["odds"]["h2h"]
                odds_list.append((site["site_nice"], odds))

            for i in range(len(odds_list)):
                for j in range(i + 1, len(odds_list)):
                    site_a, odds_a = odds_list[i]
                    site_b, odds_b = odds_list[j]

                    profit, bet_a, bet_b = compute_surebet(odds_a[0], odds_b[0]) 

                    if profit:
                        surebets.append({
                            "Team A": team_a,
                            "Team B": team_b,
                            "Site A": site_a,
                            "Site B": site_b,
                            "Odds A": odds_a[0],
                            "Odds B": odds_b[0],
                            "Profit %": round(profit, 2),
                            "Bet A": round(bet_a, 2),
                            "Bet B": round(bet_b, 2),
                            "Timestamp": event.get("commence_time", None)
                        })

                all_games.append({
                    "Team A": team_a,
                    "Team B": team_b,
                    "Site": site_a,
                    "Odds A": odds_a[0],
                    "Odds B": odds_b[0],
                    "Timestamp": event.get("commence_time", None)
                })
    return all_games