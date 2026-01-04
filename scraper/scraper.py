from scrapling.fetchers import Fetcher
from urllib.parse import quote_plus
import json
import time

us_states = [
  { "name": "Alabama", "abbreviation": "AL", "capital": "Montgomery" },
  { "name": "Alaska", "abbreviation": "AK", "capital": "Juneau" },
  { "name": "Arizona", "abbreviation": "AZ", "capital": "Phoenix" },
  { "name": "Arkansas", "abbreviation": "AR", "capital": "Little Rock" },
  { "name": "California", "abbreviation": "CA", "capital": "Sacramento" },
  { "name": "Colorado", "abbreviation": "CO", "capital": "Denver" },
  { "name": "Connecticut", "abbreviation": "CT", "capital": "Hartford" },
  { "name": "Delaware", "abbreviation": "DE", "capital": "Dover" },
  { "name": "Florida", "abbreviation": "FL", "capital": "Tallahassee" },
  { "name": "Georgia", "abbreviation": "GA", "capital": "Atlanta" },
  { "name": "Hawaii", "abbreviation": "HI", "capital": "Honolulu" },
  { "name": "Idaho", "abbreviation": "ID", "capital": "Boise" },
  { "name": "Illinois", "abbreviation": "IL", "capital": "Springfield" },
  { "name": "Indiana", "abbreviation": "IN", "capital": "Indianapolis" },
  { "name": "Iowa", "abbreviation": "IA", "capital": "Des Moines" },
  { "name": "Kansas", "abbreviation": "KS", "capital": "Topeka" },
  { "name": "Kentucky", "abbreviation": "KY", "capital": "Frankfort" },
  { "name": "Louisiana", "abbreviation": "LA", "capital": "Baton Rouge" },
  { "name": "Maine", "abbreviation": "ME", "capital": "Augusta" },
  { "name": "Maryland", "abbreviation": "MD", "capital": "Annapolis" },
  { "name": "Massachusetts", "abbreviation": "MA", "capital": "Boston" },
  { "name": "Michigan", "abbreviation": "MI", "capital": "Lansing" },
  { "name": "Minnesota", "abbreviation": "MN", "capital": "St. Paul" },
  { "name": "Mississippi", "abbreviation": "MS", "capital": "Jackson" },
  { "name": "Missouri", "abbreviation": "MO", "capital": "Jefferson City" },
  { "name": "Montana", "abbreviation": "MT", "capital": "Helena" },
  { "name": "Nebraska", "abbreviation": "NE", "capital": "Lincoln" },
  { "name": "Nevada", "abbreviation": "NV", "capital": "Carson City" },
  { "name": "New Hampshire", "abbreviation": "NH", "capital": "Concord" },
  { "name": "New Jersey", "abbreviation": "NJ", "capital": "Trenton" },
  { "name": "New Mexico", "abbreviation": "NM", "capital": "Santa Fe" },
  { "name": "New York", "abbreviation": "NY", "capital": "Albany" },
  { "name": "North Carolina", "abbreviation": "NC", "capital": "Raleigh" },
  { "name": "North Dakota", "abbreviation": "ND", "capital": "Bismarck" },
  { "name": "Ohio", "abbreviation": "OH", "capital": "Columbus" },
  { "name": "Oklahoma", "abbreviation": "OK", "capital": "Oklahoma City" },
  { "name": "Oregon", "abbreviation": "OR", "capital": "Salem" },
  { "name": "Pennsylvania", "abbreviation": "PA", "capital": "Harrisburg" },
  { "name": "Rhode Island", "abbreviation": "RI", "capital": "Providence" },
  { "name": "South Carolina", "abbreviation": "SC", "capital": "Columbia" },
  { "name": "South Dakota", "abbreviation": "SD", "capital": "Pierre" },
  { "name": "Tennessee", "abbreviation": "TN", "capital": "Nashville" },
  { "name": "Texas", "abbreviation": "TX", "capital": "Austin" },
  { "name": "Utah", "abbreviation": "UT", "capital": "Salt Lake City" },
  { "name": "Vermont", "abbreviation": "VT", "capital": "Montpelier" },
  { "name": "Virginia", "abbreviation": "VA", "capital": "Richmond" },
  { "name": "Washington", "abbreviation": "WA", "capital": "Olympia" },
  { "name": "Oregon", "abbreviation": "OR", "capital": "Salem" },
  { "name": "Pennsylvania", "abbreviation": "PA", "capital": "Harrisburg" },
  { "name": "Rhode Island", "abbreviation": "RI", "capital": "Providence" },
  { "name": "South Carolina", "abbreviation": "SC", "capital": "Columbia" },
  { "name": "South Dakota", "abbreviation": "SD", "capital": "Pierre" },
  { "name": "Tennessee", "abbreviation": "TN", "capital": "Nashville" },
  { "name": "Texas", "abbreviation": "TX", "capital": "Austin" },
  { "name": "Utah", "abbreviation": "UT", "capital": "Salt Lake City" },
  { "name": "Vermont", "abbreviation": "VT", "capital": "Montpelier" },
  { "name": "Virginia", "abbreviation": "VA", "capital": "Richmond" },
  { "name": "Washington", "abbreviation": "WA", "capital": "Olympia" },
  { "name": "West Virginia", "abbreviation": "WV", "capital": "Charleston" },
  { "name": "Wisconsin", "abbreviation": "WI", "capital": "Madison" },
  { "name": "Wyoming", "abbreviation": "WY", "capital": "Cheyenne" }
]

def get_listings(state, maxpage):
    listing = []
    base_url = "https://www.zillow.com"
    location_encoded  = quote_plus(state["capital"] + ", " + state["abbreviation"])
    for page_num in range(1,maxpage+1):
        print(f"Fetching Page {page_num}")
        print(f"Fetching Url {base_url}")
        if page_num==1:
            url = f"{base_url}/{location_encoded}/"
        else:
            url = f"{base_url}/{location_encoded}/{page_num}_p"

        
        response = Fetcher.get(url)
        listing += extract_data(response)
        if page_num<maxpage:
            time.sleep(5)
    return listing
def extract_data(response):
    # 1. Try to find the hidden JSON data
    json_raw = response.css('#__NEXT_DATA__::text').get()
    # print("raw :",json_raw)
    if json_raw:
        try:
            data = json.loads(json_raw)
            # Debug: Save JSON to file once to inspect structure if needed

            # with open('debug_zillow.json', 'w') as f:
            #     json.dump(data, f, indent=2)

            # Modern Zillow JSON path search
            # We look for 'listResults' anywhere in the object
            def find_listings(obj):
                if isinstance(obj, dict):
                    if 'listResults' in obj:
                        return obj['listResults']
                    for v in obj.values():
                        result = find_listings(v)
                        if result: return result
                    
                elif isinstance(obj, list):
                    for item in obj:
                        result = find_listings(item)
                        if result: return result
                return None

            results = find_listings(data)
            if results:
                print(f"Found {len(results)} listings in JSON!")
                return results
        except Exception as e:
            print(f"JSON Parse Error: {e}")

    # 2. Fallback to CSS (Still only gets ~9)
    print("Falling back to CSS selectors (Limited results)")
    cards = response.css('article[data-test="property-card"]')
    return cards
def convert_json(data):
    return json.dumps(data,indent = 4)

picked_state = us_states[20]

listings = get_listings(picked_state ,2)

print(len(listings))

with open('data.json', 'r+') as f:
    f.write(str(convert_json(listings)))