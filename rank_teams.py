import pandas as pd 
import os
import get_team_avg

def sort_teams(criteria) -> None: # tuplet in format ((Column: str, weight: int ∈ [0, 1]))
    event_df = pd.read_csv("data/event_avg.csv")
    for criterium, weight in criteria:
        event_df: pd.DataFrame = event_df.sort_values(by=criterium, ascending=False)
        top_row: pd.DataFrame = event_df.iloc[0]
        best: double = top_row[criterium]
        event_df[f"{criterium}percent"] = event_df[criterium]
        for index in range(len(event_df)):
            event_df.loc[index, f"{criterium}percent"] /= best
            event_df.loc[index, f"{criterium}percent"] *= weight

    event_df["sum"] = event_df[[f"{crit[0]}percent" for crit in criteria]].sum(axis=1)
    event_df = event_df.sort_values(by="sum", ascending=False)
    print(event_df)
    
    event_df.to_csv("data/ranked_teams.csv")
        
        

    

def main() -> None:
    # If data doesn't exist, generate it
    if not os.path.exists("data/event_avg.csv"):
        get_team_avg.main()
        

    sort_teams((("Score", 0.8), ("Totalautopoints", 0.6)))


if __name__ == "__main__":
    main()
