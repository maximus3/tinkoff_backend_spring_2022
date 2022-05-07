import requests
import asyncio
import async_timeout

from app.__main__ import app
from starlette.testclient import TestClient


async def sleep(n=10):
    await asyncio.sleep(n)


async def main():
    r = requests.get('http://localhost:8090/history/main')
    print(r.json())
    r = requests.post(
        'http://localhost:8090/login', json={'username': 'username'}
    )
    print(r.json())
    user_id = r.json()['id']
    with TestClient(app) as client, client.websocket_connect(f'/ws/main/{user_id}') as ws:
        ws.send_text('HELLO')

        try:
            async with async_timeout.timeout(5):
                received_message = ws.receive_text()
                print(received_message)
                assert received_message == f'username:HELLO'
        except asyncio.TimeoutError:
            print('timeout')
        else:
            print('success')

        ws.send_text('WORLD')

        try:
            async with async_timeout.timeout(5):
                received_message = ws.receive_text()
                print(received_message)
                assert received_message == f'username:WORLD'
        except asyncio.TimeoutError:
            print('timeout')
        else:
            print('success')
    print('Out of websocket and client')


if __name__ == '__main__':
    asyncio.run(main())
    print('Print out of asyncio.run', flush=True)
    asyncio.run(sleep())
    print('Print out of asyncio.run sleep', flush=True)
