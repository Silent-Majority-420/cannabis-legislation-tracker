def fetch_bills_for_state(state_code, state_name):
    """Fetch cannabis-related bills for a specific state"""
    
    print(f"Fetching bills for {state_name}...")
    
    # Use 2 years for all states (API limitation - doesn't support year=5)
    year_param = 2
    
    # Search for cannabis-related bills
    search_url = LEGISCAN_BASE_URL.format(LEGISCAN_API_KEY, 'getSearch')
    search_params = {
        'state': state_code,
        'query': 'cannabis OR marijuana',
        'year': year_param
    }
    
    try:
        response = requests.get(search_url, params=search_params)
        
        if response.status_code != 200:
            print(f"  ⚠ Error fetching {state_name}: HTTP {response.status_code}")
            return []
        
        data = response.json()
        
        if data.get('status') != 'OK':
            print(f"  ⚠ API Error for {state_name}: {data.get('alert', {}).get('message', 'Unknown')}")
            return []
        
        search_results = data.get('searchresult', {})
        
        if not search_results or search_results.get('summary', {}).get('count', 0) == 0:
            print(f"  ℹ No bills found for {state_name}")
            return []
        
        bills = []
        bill_count = 0
        filtered_count = 0
        
        for bill_id, bill_data in search_results.items():
            if bill_id == 'summary':
                continue
            
            bill_count += 1
            
            # Get detailed bill information
            bill_url = LEGISCAN_BASE_URL.format(LEGISCAN_API_KEY, 'getBill')
            bill_params = {'id': bill_data.get('bill_id')}
            
            try:
                bill_response = requests.get(bill_url, params=bill_params)
                
                if bill_response.status_code == 200:
                    bill_detail = bill_response.json()
                    
                    if bill_detail.get('status') == 'OK':
                        bill_info = bill_detail.get('bill', {})
                        
                        title = bill_info.get('title', '')
                        description = bill_info.get('description', '')
                        
                        # Filter out non-relevant bills
                        if not is_relevant_bill(title, description):
                            filtered_count += 1
                            continue
                        
                        # Extract key information
                        bill = {
                            'id': bill_info.get('bill_id'),
                            'state_code': state_code,
                            'state_name': state_name,
                            'bill_number': bill_info.get('bill_number'),
                            'title': title,
                            'description': description[:500],
                            'status': bill_info.get('status_desc'),
                            'status_date': bill_info.get('status_date'),
                            'url': bill_info.get('url'),
                            'last_action': bill_info.get('last_action'),
                            'last_action_date': bill_info.get('last_action_date'),
                            'sponsors': [],
                            'analysis_url': None
                        }
                        
                        # Extract sponsors (limit to first 5)
                        for sponsor in bill_info.get('sponsors', [])[:5]:
                            bill['sponsors'].append({
                                'name': sponsor.get('name'),
                                'party': sponsor.get('party', ''),
                                'role': sponsor.get('role', '')
                            })
                        
                        bills.append(bill)
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ⚠ Error fetching bill details: {e}")
                continue
        
        if filtered_count > 0:
            print(f"  ℹ Filtered out {filtered_count} non-policy bills")
        print(f"  ✓ Found {len(bills)} relevant bills for {state_name}")
        return bills
        
    except Exception as e:
        print(f"  ⚠ Error for {state_name}: {e}")
        return []
