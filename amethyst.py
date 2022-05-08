"""
Copyright (C) 2022 NikZapp
Copyright (C) 2022 LEHAtupointow

This program is free software: you can redistribute it and/or modify it under the terms of the GNU 
General Public License as published by the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see 
<https://www.gnu.org/licenses/>.

"""

import os
import sys
import asyncio

def handle_plugin_event(event_path, event_args):
    event_args["amethyst"] = amethyst
    for plugin in amethyst["plugins"]:
        handle_local_event(
            amethyst["plugins"][plugin], event_path.copy(), event_args.copy()
        )


def handle_local_event(plugin, event_path, event_args):
    # Get to the full path of the event
    if amethyst["debug"]:
        print(f"Handling event in {plugin}, path:{event_path}, args:{event_args}")
    events = plugin.events
    for event_group in event_path:
        if event_group in events:
            events = events[event_group]
        else:
            if amethyst["debug"]:
                print(f"Event {event_path} did not reach the plugin {plugin}")
            break
    if callable(events):
        try:
            if asyncio.iscoroutinefunction(events):
                coroutine = events(event_args)
                asyncio.run_coroutine_threadsafe(coroutine, amethyst["asyncio_loop"])
            else:
                events(event_args)
        except Exception as e:
            if amethyst["debug"]:
                print(
                    f'Exception in plugin {plugin.name} during event {".".join(event_path)}: {e}'
                )
    elif type(events) == list:
        for event in events:
            try:
                if asyncio.iscoroutinefunction(event):
                    coroutine = event(event_args)
                    asyncio.run_coroutine_threadsafe(
                        coroutine, amethyst["asyncio_loop"]
                    )
                else:
                    event(event_args)
            except Exception as e:
                if amethyst["debug"]:
                    print(
                        f'Exception in plugin {plugin.name} during multi-event {".".join(event_path)}: {e}'
                    )
    else:
        pass  # print('Unknown:', type(events))


try:
    from conf import config
except:
    if __name__ == "__main__": print("conf.py import failed. Using default settings.")
    config = dict(
        path_to_plugins="plugins",
        debug=True,
        event=handle_plugin_event,
        local_event=handle_local_event,
        asyncio_loop=asyncio.get_event_loop(),
    )

amethyst = config

def main():
    if not os.path.exists(amethyst["path_to_plugins"]):
        os.makedirs(amethyst["path_to_plugins"])
    # Step 1: Load all plugins
    amethyst["plugins"] = {}
    sys.path.insert(1, amethyst["path_to_plugins"])
    for short_path in os.listdir(amethyst["path_to_plugins"]):
        try:
            print(f"Importing {short_path}")
            plugin = __import__(short_path).Plugin
        except AttributeError:
            print(f"No plugin class found in {short_path}")
            print()
            continue
        finally:
            print(f"Checking compatibility for {short_path}")
            if not hasattr(plugin, "name"):
                print("WARNING: Name not defined.")
            if not hasattr(plugin, "author"):
                print("WARNING: Author not defined")
            if not hasattr(plugin, "events"):
                print("ERROR: Plugin has no event table!")
                print("Plugin is not compatible")
                print()
                continue
            print("Plugin is compatible")
        amethyst["plugins"][plugin.name] = plugin
        print(f"Loaded {short_path} as {plugin.name}")
        print()

    print("Running the setup event")
    handle_plugin_event(["amethyst", "setup"], {})
    print("Amethyst active.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping the plugins")
        handle_plugin_event(["amethyst", "stop"], {})
    print("Amethyst terminated.")
    quit()


if __name__ == "__main__":
    main()
