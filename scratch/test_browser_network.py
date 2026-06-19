from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.set_capability('goog:loggingPrefs', {'browser': 'ALL', 'performance': 'ALL'})

driver = webdriver.Chrome(options=options)

try:
    url = "http://localhost:8000/index.html"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(3)
    
    print("\nReading performance logs...")
    perf_logs = driver.get_log('performance')
    print(f"Found {len(perf_logs)} performance log entries.")
    
    import json
    # Let's map request_id to URL and mimeType
    requests = {}
    for entry in perf_logs:
        log_data = json.loads(entry['message'])['message']
        method = log_data.get('method')
        if method == 'Network.responseReceived':
            params = log_data['params']
            request_id = params['requestId']
            response = params['response']
            requests[request_id] = {
                'url': response['url'],
                'mimeType': response['mimeType'],
                'status': response['status']
            }
            
    # Now print status and body for each local JS / HTML request
    for request_id, req in requests.items():
        resp_url = req['url']
        mime_type = req['mimeType']
        status = req['status']
        if 'localhost' in resp_url and (mime_type == 'text/html' or '.js' in resp_url):
            print(f"URL: {resp_url} | Status: {status} | MimeType: {mime_type}")
            try:
                body_data = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                body = body_data['body']
                print(f"  Body start: {repr(body[:150])}")
            except Exception as e:
                print(f"  Could not get body: {e}")
                    
finally:
    driver.quit()
