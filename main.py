import os
import sys


def handle_plugin_event(event_path, event_args):
    event_args['amethyst'] = amethyst
    for plugin in amethyst['plugins']:
        handle_local_event(plugin, event_path, event_args)


def handle_local_event(plugin, event_path, event_args):
    # Get to the full path of the event
    events = plugin.events
    for event_group in event_path:
        if event_group in events:
            events = events.event_group
        else:
            if amethyst['debug']: print(f'Event {event_path} did not reach the plugin {plugin}')
            break
    if callable(events):
        try:
            events(event_args)
        except Exception as e:
            if amethyst['debug']: print(f'Exception in plugin {plugin.name} during event {".".join(event_path)}: {e}')
    if type(events) == list:
        for event in events:
            try:
                event(event_args)
            except Exception as e:
                if amethyst['debug']: print(f'Exception in plugin {plugin.name} during multi-event {".".join(event_path)}: {e}')


amethyst = dict(path_to_plugins='./plugins',
                version='DEV_2.0',
                debug=False,
                event=handle_plugin_event,
                local_event=handle_local_event)


# Step 1: Load all plugins
amethyst['plugins'] = []
sys.path.insert(1, amethyst['path_to_plugins'])
for short_path in os.listdir(amethyst['path_to_plugins']):
    try:
        plugin = __import__(short_path).Plugin
    except ModuleNotFoundError:
        print(f'Cannot import plugin: {short_path}')
        print()
        continue
    except AttributeError:
        print(f'Incompatible plugin: {short_path}')
        print()
        continue
    finally:
        print(f'Checking compatibility for {short_path}')
        if not hasattr(plugin, 'name'):
            print('WARNING: Name not defined.')
        if not hasattr(plugin, 'author'):
            print('WARNING: Author not defined')
        if not hasattr(plugin, 'events'):
            print('ERROR: Plugin has no event table!')
            print('Plugin is not compatible')
            print()
            continue
        print('Plugin is compatible')
    amethyst['plugins'].append(plugin)
    print(f'Loaded {short_path} as {plugin.name}')
    print()

print('Running the setup event')
handle_plugin_event(['amethyst', 'setup'], {})
print('Done')

try:
    while True:
        pass
except KeyboardInterrupt:
    print('Stopping the plugins')
    handle_plugin_event(['amethyst', 'stop'], {})
    print('Done')
