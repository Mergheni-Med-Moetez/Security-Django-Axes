import time

import requests

URL = 'http://127.0.0.1:8000/agents/api/auth/login/'
USERNAME = 'test_agent'
PASSWORD = 'WrongPassword!'
NUM_ATTEMPTS = 10
TIMEOUT = 5


def run_attack():
    print(f'Starting sequential brute-force simulation against {URL}')
    for attempt in range(1, NUM_ATTEMPTS + 1):
        try:
            response = requests.post(
                URL,
                json={'username': USERNAME, 'password': PASSWORD},
                timeout=TIMEOUT,
            )
            status_code = response.status_code
            expected = 401 if attempt <= 5 else 403
            outcome = 'ok' if status_code == expected else 'unexpected'
            print(f'Attempt {attempt}: HTTP {status_code} ({outcome}, expected {expected})')
        except requests.RequestException as exc:
            print(f'Attempt {attempt} failed: {exc}')
        time.sleep(0.4)


if __name__ == '__main__':
    run_attack()
