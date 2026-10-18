import asyncio
import httpx
import time

PROTECTED_URL = "http://127.0.0.1:8000/agents/api/auth/login/"
UNPROTECTED_URL = "http://127.0.0.1:8000/agents/api/health/"
SAMPLES = 50

async def measure_latency(url, label):
    latencies = []
    async with httpx.AsyncClient() as client:
        for i in range(SAMPLES):
            start = time.perf_counter()
            await client.get(url) if "health" in url else await client.post(url, json={"username":"test", "password":"wrong"})
            end = time.perf_counter()
            latencies.append((end - start) * 1000) # Convert to ms
    
    avg = sum(latencies) / SAMPLES
    print(f"📊 {label}: Avg = {avg:.2f}ms | Min = {min(latencies):.2f}ms | Max = {max(latencies):.2f}ms")
    return avg

async def main():
    print(f"⏱️ Starting Latency Analysis ({SAMPLES} samples per route)...")
    
    # Measure Unprotected (Control)
    health_avg = await measure_latency(UNPROTECTED_URL, "Unprotected (Health)")
    
    # Measure Protected (Experiment)
    login_avg = await measure_latency(PROTECTED_URL, "Protected (Login)")
    
    tax = login_avg - health_avg
    print(f"\n--- FINAL ANALYSIS ---")
    print(f"The 'Security Tax' (Axes Overhead) is: {tax:.2f}ms")

if __name__ == "__main__":
    asyncio.run(main())