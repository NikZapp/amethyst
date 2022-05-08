"""
This is an example of a sample conf.py.
"""

from amethyst import handle_plugin_event, handle_local_event
import asyncio
config = {
    "path_to_plugins":"plugins",
    "debug":True,
    "event":handle_plugin_event,
    "local_event":handle_local_event,
    "asyncio_loop":asyncio.get_event_loop(),
}
