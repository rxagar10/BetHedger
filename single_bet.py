import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_user_info():
    print('This will determine the optimal amount to wager: First we need some information: ')
    total_amt = input('Enter The Total Amount You Want to Wager: ')
    favorite_name = input('What/Who is the favorite for this bet: ')
    favorite_odds = input('Enter the Odds for the Favorite: ')
    upset_name = input('What/Who is the upset for this bet: ')
    upset_odds = input('Enter the Odds for the Upset: ')
    wants_spread = input('Do you want an image of possible spread of combinations? (Enter true or false): ')
    return total_amt, favorite_name, favorite_odds, upset_name, upset_odds, wants_spread

# Determines the Multiplier from a Given Odds
def conversionOdds(odds):
    if(odds < 0):
        return (100 / (odds * -1)) + 1
    else:
        return (odds / 100) + 1

# Returns a Dataframe that gets all of the combinations with the given Odds
def single_bet_payouts(favorite_odds, upset_odds, total_amt):
    favorite_multi = conversionOdds(favorite_odds)
    upset_multi = conversionOdds(upset_odds)
    risk_df = pd.DataFrame()
    risk_df['Risk for Favorite'] = np.arange(0, total_amt, 0.01)
    risk_df['Risk for Favorite'] = risk_df['Risk for Favorite'].round(decimals = 2)
    risk_df['Risk for Upset'] = risk_df.apply(lambda row: total_amt - row)
    risk_df['Risk for Upset'] = risk_df['Risk for Upset'].round(decimals = 2)
    risk_df['Favorite Payout'] = risk_df['Risk for Favorite'].apply(lambda row: favorite_multi*row)
    risk_df['Upset Payout'] = risk_df['Risk for Upset'].apply(lambda row: upset_multi*row)
    risk_df['Favorite Wins Balance'] = risk_df['Favorite Payout'] - total_amt
    risk_df['Upset Wins Balance'] = risk_df['Upset Payout'] - total_amt
    return risk_df

# Gets the combinations from the single bet combinations that results in a positive regardless of the result
def get_positive_combinations(df):
    positive_df = df.loc[df['Favorite Wins Balance'] > 0]
    positive_df = positive_df.loc[df['Upset Wins Balance'] > 0]
    return positive_df

# Displays a plot of the dataframe given
# Will show two bar graphs, one for the difference if the favorite wins given the risk
# and one for the diffference if the upset wins given the risk
def display_single_bet_payout_distribution(risk_df):
    X_axis = np.arange(len(risk_df['Risk for Upset']))
  
    plt.figure(figsize=(15,10))
    plt.bar(X_axis - 0.2, risk_df['Favorite Wins Balance'], 0.4, label = 'Balance if Favorite Wins')
    plt.bar(X_axis + 0.2, risk_df['Upset Wins Balance'], 0.4, label = 'Balance if Upset Wins')

    plt.xticks(X_axis, risk_df['Risk for Upset'])
    plt.xlabel("Risk for Upset")
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("Payout")
    plt.title("Hedging a Specific amount of Money")
    plt.legend()
    
    plt.show()


def main():
    # Gets the info of the bet from the user
    user_info = get_user_info()
    total_amt =  user_info[0]
    favorite_name =  user_info[1]
    favorite_odds = user_info[2]
    upset_name = user_info[3]
    upset_odds = user_info[4]
    wants_spread = user_info[5]
    df = single_bet_payouts(favorite_odds, upset_odds, total_amt)
    positive_df = get_positive_combinations(df)
    if(wants_spread):
        display_single_bet_payout_distribution(df)
        display_single_bet_payout_distribution(positive_df)
    
    

# Main function
if __name__ == "__main__":
    main()


