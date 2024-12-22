from asyncio import run

from source import KS


async def main():
    async with KS() as app:
        await app.run()


if __name__ == '__main__':
    run(main(), )
