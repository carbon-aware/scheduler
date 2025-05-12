import datetime

import httpx


async def main() -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://scheduler.carbonaware.dev/v0/schedule/",
            json={
                "windows": [
                    {
                        "start": datetime.datetime.now(datetime.UTC).isoformat(),
                        "end": (
                            datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
                        ).isoformat(),
                    }
                ],
                "duration": "PT3H",
                "zones": [
                    {
                        "provider": "aws",
                        "region": "us-west-1",
                    },
                    {
                        "provider": "aws",
                        "region": "us-east-1",
                    },
                    {
                        "provider": "aws",
                        "region": "eu-central-1",
                    },
                ],
                "num_options": 3,
            },
        )
        print(response.json())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
