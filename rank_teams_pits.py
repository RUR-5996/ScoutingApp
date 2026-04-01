import pandas as pd 
import os
import get_team_avg

def sort_teams(criteria=(), requirements=()) -> None: # tuple in format ((Column: str, weight: float ∈ [0, 1]))
    try:
        event_df: pd.DataFrame = pd.read_csv("data/pit_data.csv")
    except:
        raise Exception("Pit data not provided")



    passes_requirements: list[bool] = [True for _ in range(len(event_df))]
    for requirement in requirements:
        for i in range(len(event_df)):
            if requirement[1] == "==":
                if event_df.loc[i, requirement[0]] != requirement[2]:
                    passes_requirements[i] = False
            elif requirement[1] == ">":
                if event_df.loc[i, requirement[0]] <= requirement[2]:
                    passes_requirements[i] = False
            elif requirement[1] == "<":
                if event_df.loc[i, requirement[0]] >= requirement[2]:
                    passes_requirements[i] = False

    for criterium, weight in criteria:
        event_df[criterium] = event_df[criterium].astype(float)
        weight: float = float(weight)
        event_df: pd.DataFrame = event_df.sort_values(by=criterium, ascending=False)
        top_row: pd.DataFrame = event_df.iloc[0]
        best: float = top_row[criterium]
        event_df[f"{criterium}Percent"] = event_df[criterium]
        for index in range(len(event_df)):
            if passes_requirements[index]:
                event_df.loc[index, f"{criterium}Percent"] /= best
                event_df.loc[index, f"{criterium}Percent"] *= weight
            else:
                event_df.loc[index, f"{criterium}Percent"] = float('-inf')

    event_df["sum"] = event_df[[f"{crit[0]}Percent" for crit in criteria]].sum(axis=1)
    event_df = event_df.sort_values(by="sum", ascending=False)
    
    event_df = event_df.round(3)
    print(event_df)
    event_df.to_csv("data/ranked_teams_pits.csv")
        

def main() -> None:

    sort_teams(
        (("Climbing", 0.8), ("CycleTime", -0.6)), 
        (("Score", ">", 100), ("DriveTrain", "==", 1)) # 1=SWERVE
    ) 


if __name__ == "__main__":
    main()
