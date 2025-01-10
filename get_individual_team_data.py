import pandas as pd

# Function to split the data into rows for each team and retain all relevant columns
def split_data_for_teams(match_data_df):
    # Create an empty list to store the new rows
    team_data = []

    # Get all columns in the DataFrame
    all_columns = match_data_df.columns.tolist()

    # Identify columns related to Autolinerobot and Endgamerobot
    autolinerobot_columns = [col for col in all_columns if 'Autolinerobot' in col]
    endgamerobot_columns = [col for col in all_columns if 'Endgamerobot' in col]

    # Loop through each row in the original DataFrame
    for _, row in match_data_df.iterrows():
        for i in range(1, 4):  # Iterate over Team1, Team2, Team3 (i = 1, 2, 3)
            team_name = row[f'Team{i}']
            
            if pd.notna(team_name):  # Skip if team name is NaN
                # Prepare the corresponding Autolinerobot and Endgamerobot columns for the current team
                team_entry = {
                    "Team": team_name,
                    "Autolinerobot": row[f'Autolinerobot{i}'],
                    "Endgamerobot": row[f'Endgamerobot{i}'],
                }

                # Add all other columns (excluding Autolinerobot and Endgamerobot) for the current row
                for column in all_columns:
                    if column not in autolinerobot_columns and column not in endgamerobot_columns and column not in ['Team1', 'Team2', 'Team3']:
                        team_entry[column] = row[column]

                # Append the team entry to the list
                team_data.append(team_entry)

    # Convert the list of dictionaries to a DataFrame
    team_data_df = pd.DataFrame(team_data)

    # Sort the data by the 'Team' column
    return team_data_df.sort_values(by="Team")

# Main function to run the program
def main():
    # Load the match data from the CSV file
    match_data_df = pd.read_csv("data/all_match_data.csv")
    
    # Split the data into rows for each team and sort by team
    team_data_df = split_data_for_teams(match_data_df)
    
    # Save the result to a new CSV file
    team_data_df.to_csv("data/team_split_data.csv", index=False)
    print("\nTeam split data with all stats saved to 'data/team_split_data.csv'")

if __name__ == "__main__":
    main()
