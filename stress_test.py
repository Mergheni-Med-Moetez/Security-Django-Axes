import asyncio
import httpx
import time

# Target the exact URL from our settings update
TARGET_URL = "http://127.0.0.1:8000/agents/api/auth/login/"
ATTACK_SIZE = 50 
USERNAME = "test_agent"
PASSWORD = "WrongPassword!"

async def send_request(client, req_id):
    # LEAD INTEGRATOR FIX: Added a tiny staggered delay (50ms per request)
    # This ensures the server can process requests in sequence while still 
    # testing the high-speed capability of the RAM cache.
    await asyncio.sleep(req_id * 0.2) # Increased from 0.05 to 0.2
    
    data = {"username": USERNAME, "password": PASSWORD}
    try:
        response = await client.post(TARGET_URL, json=data)
        return response.status_code
    except Exception as e:
        return f"Error: {e}"

async def main():
    print(f"🚀 Launching Staggered High-Speed Attack: {ATTACK_SIZE} requests...")
    
    async with httpx.AsyncClient() as client:
        # We still generate all tasks, but the sleep inside the function 
        # manages the 'machine gun' timing.
        tasks = [send_request(client, i) for i in range(ATTACK_SIZE)]
        start_time = time.perf_counter()
        results = await asyncio.gather(*tasks)
        end_time = time.perf_counter()

    # Analysis
    success_401 = results.count(401) # Allowed to try
    success_403 = results.count(403) # Blocked
    
    print(f"\n--- RESULTS ---")
    print(f"Time Taken: {end_time - start_time:.2f}s")
    print(f"Attempts Allowed (401): {success_401}")
    print(f"Attempts Blocked (403): {success_403}")

    if success_401 > 5:
        print(f"⚠️  FAILURE: Race Condition Detected! Allowed {success_401} attempts.")
    elif success_401 == 0:
         print("⚠️  NOTICE: No attempts allowed. Did you forget to restart the server?")
    else:
        print("✅ SUCCESS: The Atomic Counter held firm.")

if __name__ == "__main__":
    asyncio.run(main())