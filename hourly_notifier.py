import requests
from datetime import datetime

# Replace this with your actual Discord webhook URL
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1362204460507729940/QY6vR1P6WinPNbS5VWBwu0AaIq8UsKo-etlQpt7-bCHeXszxV0zwafAM4YGJzC4t9MTg'

# Generate a timestamp
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Prepare the message payload
data = {
    "content": f"✅ Cron job ran at {now}"
}

# Send the POST request to Discord
response = requests.post(WEBHOOK_URL, json=data)

# Optional: print status for logging
if response.status_code == 204:
    print(f"Success: Sent at {now}")
else:
    print(f"Failed: Status code {response.status_code}")
