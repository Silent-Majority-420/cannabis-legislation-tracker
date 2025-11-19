#!/usr/bin/env python3
"""
Cannabis Legislation Tracker Scraper
Fetches federal cannabis bills from LegiScan API and generates JSON data for the tracker.
"""

import os
import json
import requests
from datetime import datetime

# LegiScan API configuration
LEGISCAN_API_KEY = os.environ.get('LEGISCAN_API_KEY')
LEGISCAN_BASE_URL = 'https://api.legiscan.com/?key={}&op={}'

def fetch_cannabis_bills():
    """Fetch cannabis-related bills from LegiScan API"""
    
    if not LEGISCAN_API_KEY:
        print("Error: LEGISCAN_API_KEY environment variable not set")
        return []
    
    # Search for cannabis-related bills at federal level
    search_url = LEGISCAN_BASE_URL.format(LEGISCAN_API_KEY, 'getSearch')
    search_params = {
        'state': 'US',  # US for federal bills
        'query': 'cannabis OR marijuana',
        'year': 2
    }
    
    response = requests.get(search_url, params=search_params)
    
    if response.status_code != 200:
        print(f"Error fetching bills: {response.status_code}")
        return []
    
    data = response.json()
    
    if data.get('status') != 'OK':
        print(f"API Error: {data.get('alert', {}).get('message', 'Unknown error')}")
        return []
    
    search_results = data.get('searchresult', {})
    
    bills = []
    for bill_id, bill_data in search_results.items():
        if bill_id == 'summary':
            continue
            
        # Get detailed bill information
        bill_url = LEGISCAN_BASE_URL.format(LEGISCAN_API_KEY, 'getBill')
        bill_params = {'id': bill_data.get('bill_id')}
        
        bill_response = requests.get(bill_url, params=bill_params)
        
        if bill_response.status_code == 200:
            bill_detail = bill_response.json()
            
            if bill_detail.get('status') == 'OK':
                bill_info = bill_detail.get('bill', {})
                
                # Extract key information
                bill = {
                    'id': bill_info.get('bill_id'),
                    'bill_number': bill_info.get('bill_number'),
                    'title': bill_info.get('title'),
                    'description': bill_info.get('description'),
                    'status': bill_info.get('status_desc'),
                    'status_date': bill_info.get('status_date'),
                    'url': bill_info.get('url'),
                    'last_action': bill_info.get('last_action'),
                    'last_action_date': bill_info.get('last_action_date'),
                    'sponsors': [],
                    'analysis_url': None  # Placeholder for custom analysis URLs
                }
                
                # Extract sponsors
                for sponsor in bill_info.get('sponsors', []):
                    bill['sponsors'].append({
                        'name': sponsor.get('name'),
                        'party': sponsor.get('party'),
                        'role': sponsor.get('role')
                    })
                
                bills.append(bill)
    
    return bills

def save_bills_data(bills):
    """Save bills data to JSON file"""
    
    output_data = {
        'last_updated': datetime.now().isoformat(),
        'total_bills': len(bills),
        'bills': bills
    }
    
    with open('bills.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Successfully saved {len(bills)} bills to bills.json")
    print(f"Last updated: {output_data['last_updated']}")

def main():
    """Main function to fetch and save cannabis bills"""
    
    print("Fetching federal cannabis legislation from LegiScan...")
    bills = fetch_cannabis_bills()
    
    if bills:
        save_bills_data(bills)
        print("\n📝 Next Steps:")
        print("1. Review bills.json to identify significant bills for analysis")
        print("2. Create analysis articles on silentmajority420.com")
        print("3. Add analysis URLs to the 'analysis_url' field in bills.json")
        print("4. Commit and push the updated bills.json to your repository")
    else:
        print("No bills found or error occurred")

if __name__ == '__main__':
    main()
