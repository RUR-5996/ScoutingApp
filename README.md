# **FRC Scouting App**

App for scouting FRC teams using BlueAlliance. Built by [Filip Martinek](https://github.com/FilipMartinek/), [M. Filip](https://github.com/mfilip123), [R.U.R. 5996](https://www.team5996.eu/).

## Run/TODO

 - [x] Get raw data from api:
```
python get_raw_data.py 
```
 - [x] Get individual team data (from raw data):
```
python get_team_data.py 
```
 - [x] Calculate average stats of teams at event
```
python get_team_avg.py
```
 - [x] Rank teams based on custom criteria
 ```
python rank_teams.py
```
 - [x] Rank teams based on pit scouting (make sure to provide data/pit_data.csv)
```
python rank_teams_pits.py
```
 - [ ] Train ML model
```
python train.py 
```

## Dependencies

 - Python 3.6+ (tested on Python 3.14.3)

 - Install Libraries:
 ```
 python -m pip install -r requirements.txt
 ```
