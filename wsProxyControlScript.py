#!/usr/bin/env python3

import logging
import argparse
import sys
import asyncio
import websockets

log = logging.getLogger()

def logger_setup():
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler = logging.FileHandler('/share/ctrl.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
logger_setup()

RECONNECT_DELAY = 5  # seconds between reconnect attempts

async def read_stdin_and_send(ws):
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        log.info("Sending to ws: "+ line)
        await ws.send(line.strip())

async def read_ws_and_print(ws):
    async for message in ws:
        log.info("Sending to stdout: " + message)
        sys.stdout.write(message)
        sys.stdout.write('\n')
        sys.stdout.flush()

async def websocket_loop(uri: str):
    while True:
        try:
            print(f"Connecting to {uri}...", file=sys.stderr)
            async with websockets.connect(uri) as ws:
                print(f"Connected to {uri}", file=sys.stderr)
                await asyncio.gather(
                    read_stdin_and_send(ws),
                    read_ws_and_print(ws)
                )
        except (ConnectionRefusedError, websockets.exceptions.InvalidURI,
                websockets.exceptions.InvalidHandshake, OSError) as e:
            print(f"Connection failed: {e}", file=sys.stderr)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}", file=sys.stderr)

        print(f"Retrying in {RECONNECT_DELAY} seconds...", file=sys.stderr)
        await asyncio.sleep(RECONNECT_DELAY)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    args, unknown = parser.parse_known_args()
    # HOST will have the port in it too.
    asyncio.run(websocket_loop("ws://"+args.host))



