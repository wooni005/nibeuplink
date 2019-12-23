#!/usr/bin/python3

import asyncio
import json

import nibeuplink

STORE = "nibeuplink.json"
DEFAULT_CLIENT_ID = "18965"

def token_read():
    try:
        with open(STORE, "r") as myfile:
            return json.load(myfile)
    except FileNotFoundError:
        return None


def token_write(token):
    with open(STORE, "w") as myfile:
        json.dump(token, myfile, indent=2)


async def run():

    scope = ["READSYSTEM"]

    async with nibeuplink.UplinkSession(
        client_id='9b1e683e2c904adfb52313b4a327b634', # NIBE Uplink API: Identifier
        client_secret='8YL79duUZWfQAgVdjQmuNZczAtaed5fawULKfhcPzQM=', # NIBE Uplink API: Secret
        redirect_uri='https://firm-ware.cz/oauth2callback/index.php', # NIBE Uplink API: Callback URL
        access_data=token_read(),
        access_data_write=token_write,
        scope=scope,
    ) as session:

        if not session.access_data:
            auth_uri = session.get_authorize_url()
            print(auth_uri)
            result = input("Enter full redirect url: ")
            await session.get_access_token(session.get_code_from_url(result))

        uplink = nibeuplink.Uplink(session)

        todo = []
        todo.extend( # Get outdoor temp
            [uplink.get_parameter(DEFAULT_CLIENT_ID, "40004")]
        )
        todo.extend( # Get compressor starts
            [uplink.get_parameter(DEFAULT_CLIENT_ID, "43416")]
        )

        if not len(todo):
            todo.extend([uplink.get_system(DEFAULT_CLIENT_ID)])

        res = await asyncio.gather(*todo)
        for a in res:
            try:
                print(json.dumps(a, indent=1))
            except TypeError:
                print(a)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
