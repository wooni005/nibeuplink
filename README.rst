********************************
Nibe Uplink Communciation Module
********************************


Module
======


The module is an asyncio driven interface to nibe uplink public API. It is throttled to one http request every 4 seconds so
try to make the most of your requests by batching requests.

Info
____
Thanks to Joakim for the Nibe Uplink API module: https://github.com/elupus/nibeuplink

And thanks to David for the very good background information / howto page about how to use the Nibe Uplink API: 
https://www.marshflattsfarm.org.uk/wordpress/?page_id=3480

In this example where are also using his server for the callback URL, you can also put this script on your own server.


Here is a working code example: https://github.com/wooni005/nibeuplink/blob/master/example.py


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
