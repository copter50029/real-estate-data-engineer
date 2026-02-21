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

def get_listings(state, maxpage_limit):
    all_listings = []
    base_url = "https://www.zillow.com"
    location = state["name"]
    
    current_page = 1
    # We'll update this after the first request
    actual_total_pages = maxpage_limit 
    while current_page <= actual_total_pages and current_page <= maxpage_limit:
        print(f"Fetching Page {current_page} of {actual_total_pages}")
        
        url = f"{base_url}/{location}/" if current_page == 1 else f"{base_url}/{location}/{current_page}_p"
        response = Fetcher.get(url)
        
        page_listings, total_pages_found = extract_data(response)
        all_listings.extend(page_listings)
        
        # On page 1, we learn the real total pages available
        if current_page == 1:
            actual_total_pages = total_pages_found
            print(f"Site reports {actual_total_pages} pages available.")
        if current_page < actual_total_pages and current_page < maxpage_limit:
            time.sleep(5) # Respectful delay
            
        current_page += 1
            
    return all_listings
def find_search_data(obj):
    """Finds the dictionary that contains listings or search results."""
    if isinstance(obj, dict):
        # If we found the category container (cat1, etc) or the searchResults block
        if 'listResults' in obj or 'searchResults' in obj:
            return obj
        for v in obj.values():
            result = find_search_data(v)
            if result: return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_search_data(item)
            if result: return result
    return None

def extract_data(response):
    json_raw = response.css('#__NEXT_DATA__::text').get()
    if json_raw:
        try:
            data = json.loads(json_raw)
            search_data = find_search_data(data)
            
            if search_data:
                # 1. Extract Listings
                listings = search_data.get('listResults')
                if not listings and 'searchResults' in search_data:
                    listings = search_data['searchResults'].get('listResults')
                
                if listings is None: listings = []

                # 2. Extract Pagination (can be in search_data or search_data['searchList'])
                max_pages = search_data.get('totalPages')
                if not max_pages:
                    search_list = search_data.get('searchList', {})
                    if not isinstance(search_list, dict): search_list = {}
                    max_pages = search_list.get('totalPages')
                
                if not max_pages:
                    pagination = search_data.get('pagination') or search_data.get('searchList', {}).get('pagination', {})
                    if isinstance(pagination, dict):
                        max_pages = pagination.get('totalPages')

                # 3. Fallback to Result Count
                if not max_pages:
                    total = search_data.get('totalResultCount') or search_data.get('searchList', {}).get('totalResultCount', 0)
                    if total:
                        max_pages = (total // 40) + 1

                # Final Cleanup
                if not max_pages: max_pages = 1
                if max_pages > 20: max_pages = 20

                print(f"Found {len(listings)} listings. Total pages set to: {max_pages}")
                return listings, max_pages
            else:
                # Debug: if we found JSON but not the search block, save it to inspect
                with open('failed_structure.json', 'w') as f:
                    json.dump(data, f, indent=2)
                print("JSON found but 'listResults' container was missing. Saved to failed_structure.json")
        except Exception as e:
            print(f"JSON Parse Error: {e}")

    # Fallback to CSS - extract HTML strings so it's JSON serializable
    print("Falling back to CSS selectors (Limited results)")
    cards = response.css('article[data-test="property-card"]').getall()
    return (cards, 1) 
def convert_json(data):
    return json.dumps(data,indent = 4)


if __name__ == "__main__":
    picked_state = us_states[20]

    listings = get_listings(picked_state ,5)

    print(len(listings))

    with open('data.json', 'w') as f:
        f.write(str(convert_json(listings)))