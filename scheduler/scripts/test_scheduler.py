import datetime
import httpx


async def main():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8080/v0/schedule/", json={
            "windows": [
                {
                    "start": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "end": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).isoformat()
                }
            ],
            "duration": "PT1H",
            "zones": [
                {
                    "provider": "aws",
                    "region": "us-west-1",
                }
            ],
            "num_options": 1
        })
        print(response.json())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
