********************************
Nibe Uplink Communciation Module
********************************


Module
======


The module is an asyncio driven interface to nibe uplink public API. It is throttled to one http request every 4 seconds so
try to make the most of your requests by batching requests.

Status
______
.. image:: https://travis-ci.org/elupus/nibeuplink.svg?branch=master
    :target: https://travis-ci.org/elupus/nibeuplink

.. image:: https://coveralls.io/repos/github/elupus/nibeuplink/badge.svg?branch=master
    :target: https://coveralls.io/github/elupus/nibeuplink?branch=master

Thanks to David for the very good background information / howto page about how to use the Nibe Uplink API: 
https://www.marshflattsfarm.org.uk/wordpress/?page_id=3480

In this example where are also using his server for the callback URL, you can also put this script on your own server.

And thanks to Joakim for the Nibe Uplink API module:
https://github.com/elupus/nibeuplink



Code example
_______

.. code-block:: python


#!/usr/bin/python3

import asyncio
import json

import nibeuplink

STORE = "nibeuplink.json"
CLIENT_ID = "12345"

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
        client_id='XXX',     # NIBE Uplink API: Identifier
        client_secret='YYY', # NIBE Uplink API: Secret
        redirect_uri='ZZZ',  # NIBE Uplink API: Callback URL
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


Console
=======

The module contains a commandline utility to test and request data from Nibe Uplink called ``nibeuplink``, it will store token information in a file in the current directory called nibeuplink.json

Example
_______

Help for utility

.. code-block:: bash

    nibeuplink -h

Request all systems

.. code-block:: bash

    nibeuplink --client_id 'XXX' --client_secret 'YYY' --redirect_uri 'ZZZ'


Request data for specific system

.. code-block:: bash

    nibeuplink --client_id 'XXX' --client_secret 'YYY' --redirect_uri 'ZZZ' --system 12345

Request data for outside temp

.. code-block:: bash

    nibeuplink --client_id 'XXX' --client_secret 'YYY' --redirect_uri 'ZZZ' --system 12345 --parameter 40004
