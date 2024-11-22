
def retrieve_implied_odds(df,max_odds=500):

    result = df.groupby('Player').agg({'Price':'first','Implied_Odds': ['mean', 'min', 'max']}).reset_index()
    result['Implied_Odds_Diff'] = result['Implied_Odds']['max'].sub(result['Implied_Odds']['min'], axis = 0) 
    final_result=result[(result.Implied_Odds_Diff > 0.05) & (result['Price']['first']<max_odds)].sort_values(by='Implied_Odds_Diff',ascending=False)
    return final_result[['Player','Price','Implied_Odds_Diff']]
