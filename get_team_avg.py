import pandas as pd
import os
import get_team_data

def get_avg_data(teams_in_event) -> None:

    team_data_df: pd.DataFrame = pd.read_csv("data/team_split_data.csv")

    # Calculate average data
    avg_df: pd.DataFrame = pd.DataFrame()
    for team in teams_in_event:
        filtered_data: pd.Series | pd.DataFrame = team_data_df[team_data_df["Team"] == ("frc" + str(team))]
        filtered_data = filtered_data.reset_index(drop=True)
        
        avg_data: dict[str, float] = {
            "Team": team,
            "Numberofmatches": len(filtered_data),
            "Score": 0,
            "Adjustpoints": 0,
            "Autotowerpoints": 0,
            "Endgametowerpoints": 0,
            "Foulpoints": 0,
            "Majorfoulcount": 0,
            "Minorfoulcount": 0,
            "Rp": 0,
            "Totalautopoints": 0,
            "Totalteleoppoints": 0,
            "Totaltowerpoints": 0,
        }
        if len(filtered_data) > 0:
            exclude_from_avg: tuple[str, str] = ("Team", "Numberofmatches")
            excluded = {k: v for k, v in avg_data.items() if not k in exclude_from_avg}.keys() # remove team N˚ & # of matches from iteration

        
            for index, match in filtered_data.iterrows():
                for key in excluded:
                    avg_data[key] += match[key]
         
            for key in excluded:
                avg_data[key] /= len(filtered_data)

        avg_df = pd.concat([avg_df, pd.DataFrame([avg_data])], ignore_index=True)

        
    avg_df = avg_df.round(3)
    avg_df.to_csv("data/event_avg.csv")

def main() -> None:
    # Read team numbers from txt file
    with open("data/teams.txt", "r") as teamfile:
        teams_in_event: list[int] = [int(team_num) for team_num in teamfile.read().splitlines()]

    # If data doesn't exist, generate it
    if not os.path.exists("data/team_split_data.csv"):
        get_team_data.main()

    get_avg_data(teams_in_event)
        

if __name__ == "__main__":
    main()
