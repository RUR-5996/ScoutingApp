import pandas as pd
import curses

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

# Function to calculate the team statistics summary
def calculate_team_summary(match_data, selected_match_id):
    # Filter data for the selected match ID
    match_data = match_data[match_data['Match Key'] == selected_match_id]

    # Convert all boolean columns to 1s and 0s
    bool_columns = match_data.select_dtypes(include=['bool']).columns
    match_data[bool_columns] = match_data[bool_columns].astype(int)

    # Convert "Yes"/"No" columns to 1s and 0s
    yes_no_columns = match_data.select_dtypes(include=['object']).apply(
        lambda col: col.isin(['Yes', 'No']).all()
    )
    yes_no_columns = yes_no_columns[yes_no_columns].index  # Get column names
    match_data[yes_no_columns] = match_data[yes_no_columns].replace({'Yes': 1, 'No': 0})

    # Calculate the mean for numeric columns (including converted columns)
    numeric_cols = match_data.select_dtypes(include=['number']).columns
    match_summary = match_data.groupby('Team')[numeric_cols].mean().reset_index()

    return match_summary

# Function to display the match selection menu
def select_match_id(matches):
    def menu(stdscr):
        curses.curs_set(0)
        current_row = 0

        # Get terminal size
        height, width = stdscr.getmaxyx()

        # Maximum rows we can display
        max_rows = height - 2  # Leave room for prompt and navigation

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Select a match (use arrow keys and Enter):")

            # Display matches, ensuring they fit within the terminal height
            for idx, match in enumerate(matches):
                if idx < current_row or idx >= current_row + max_rows:
                    continue  # Skip items outside the current view

                display_text = match if len(match) < width - 2 else match[:width - 5] + "..."
                row = idx - current_row + 1  # Adjust row index for scrolling
                if idx == current_row:
                    stdscr.addstr(row, 0, f"> {display_text}", curses.A_REVERSE)
                else:
                    stdscr.addstr(row, 0, f"  {display_text}")

            # Get user input
            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(matches) - 1:
                current_row += 1
            elif key == ord("\n"):
                return matches[current_row]

    return curses.wrapper(menu)

# Main function to run the program
def main():
    # Load the match data from the CSV file
    match_data_df = pd.read_csv("data/all_match_data.csv")

    # Split the data into rows for each team and sort by team
    team_data_df = split_data_for_teams(match_data_df)

    # Save the split data to a new CSV file
    team_data_df.to_csv("data/team_split_data.csv", index=False)
    print("\nTeam split data with all stats saved to 'data/team_split_data.csv'")

    # Get the list of unique Match IDs, sorted by most recent first
    match_ids = sorted(team_data_df['Match Key'].unique(), reverse=True)

    # Let the user select a match ID
    selected_match_id = select_match_id(match_ids)
    print(f"Selected Match ID: {selected_match_id}")

    # Calculate the summary statistics for the selected match
    summary_df = calculate_team_summary(team_data_df, selected_match_id)

    # Save the summary to a new CSV file
    summary_df.to_csv(f"data/team_summary_match_{selected_match_id}.csv", index=False)
    print(f"\nTeam summary for match {selected_match_id} saved to 'data/team_summary_match_{selected_match_id}.csv'")

if __name__ == "__main__":
    main()
