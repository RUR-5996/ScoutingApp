import requests
import pandas as pd

# Function to get all events for a given year
def get_events(year, api_key):
    url = f"https://www.thebluealliance.com/api/v3/events/{year}"
    headers = {"X-TBA-Auth-Key": api_key}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching events:", response.status_code, response.text)
        return []

# Function to get all matches for a given event key
def get_matches(event_key, api_key):
    url = f"https://www.thebluealliance.com/api/v3/event/{event_key}/matches"
    headers = {"X-TBA-Auth-Key": api_key}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching matches:", response.status_code, response.text)
        return []

# Function to collect match data into a DataFrame
def collect_match_data(matches):
    data = []
    for match in matches:
        for alliance, details in match['alliances'].items():
            teams = details['team_keys']
            entry = {
                "Match Key": match['key'],
                "Match Name": match['comp_level'].capitalize() + str(match.get('match_number', '')),
                "Match Type": match['comp_level'].capitalize(),
                "Match Number": match.get('match_number', 'N/A'),
                "Alliance": alliance.capitalize(),
                "Team1": teams[0] if len(teams) > 0 else None,
                "Team2": teams[1] if len(teams) > 1 else None,
                "Team3": teams[2] if len(teams) > 2 else None,
                "Score": details['score']
            }
            
            # Add detailed scoring breakdown if available
            if 'score_breakdown' in match and match['score_breakdown']:
                breakdown = match['score_breakdown'].get(alliance, {})
                for key, value in breakdown.items():
                    entry[key.replace('_', ' ').capitalize()] = value
            
            data.append(entry)
    
    return pd.DataFrame(data)

# Main function to run the program
def main():
    api_key = "q8wGrrZZ08eBPpXMMzAuK8fYY0o2lQkAo10Td9eUr7XbihVojdWYFaU7yfvdKSry"
    year = input("Enter the competition year: ")
    
    events = get_events(year, api_key)
    
    if not events:
        print("No events found.")
        return
    
    all_matches_data = pd.DataFrame()
    
    for event in events:
        print(f"Fetching matches for event: {event['name']} ({event['key']})")
        matches = get_matches(event['key'], api_key)
        
        if matches:
            match_df = collect_match_data(matches)
            all_matches_data = pd.concat([all_matches_data, match_df], ignore_index=True)
    
    if not all_matches_data.empty:
        # Save all matches data to a single CSV file
        data_filedir = "data/all_match_data.csv"
        all_matches_data.to_csv(data_filedir, index=False)
        print(f"\nAll match data saved to '{data_filedir}'")
    else:
        print("No match data found for any event.")

if __name__ == "__main__":
    main()
