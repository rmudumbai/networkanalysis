import requests

url = "http://localhost:8000/analyze"
files = {'file': open('sample_syslog.log', 'rb')}

try:
    response = requests.post(url, files=files)
    if response.status_code == 200:
        data = response.json()
        print(f"Successfully analyzed {len(data)} lines.")
        print("First 5 lines:")
        for line in data[:5]:
            print(f"Type: {line['type']}, Content: {line['content'][:50]}...")
            
        # Count errors and warnings
        errors = sum(1 for line in data if line['type'] == 'error')
        warnings = sum(1 for line in data if line['type'] == 'warning')
        print(f"Total Errors: {errors}")
        print(f"Total Warnings: {warnings}")
    else:
        print(f"Error: {response.status_code}")
except Exception as e:
    print(f"Exception: {e}")
