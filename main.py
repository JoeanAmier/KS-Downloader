from asyncio import run
import argparse
from sys import argv
from source import KS
from asyncio.exceptions import CancelledError


def capture_exit(function):
    async def inner(*args, **kwargs):
        try:
            await function(*args, **kwargs)
        except (CancelledError, KeyboardInterrupt):
            exit()

    return inner


async def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode")

    server_parser = subparsers.add_parser(
        "server",
    )
    server_parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
    )
    server_parser.add_argument(
        "--port",
        type=int,
        default=5557,
    )
    if len(argv) == 1:
        await terminal()
    else:
        args, unknown = parser.parse_known_args()
        if unknown:
            print(
                f"Error: Unrecognized arguments: {unknown}. Please check your input."
            )
        if args.mode == "server":
            await server(args.host, args.port)
        else:
            print("Unsupported command-line parameters")

@capture_exit
async def terminal():
    async with KS() as app:
        await app.run()

@capture_exit
async def server(
    host="0.0.0.0",
    port=5557,
    log_level="info",
):
    async with KS() as app:
        await app.run_server(
            host,
            port,
            log_level,
        )


if __name__ == "__main__":
    run(
        main(),
    )
