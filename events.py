import asyncio
import plugins
import string
import json

# Event plugin
# Have ideas or want to contribute you can find the source at
# https://github.com/DanielMartinus/Event-plugin-hangoutsbot

def _initialise(bot):
    plugins.register_user_command(["event", "events", "join"])


def clear(bot, event, *args):
    conv_event = {}
    bot.memory.set_by_path(['_event', event.conv_id], conv_event)
    yield from bot.coro_send_message(event.conv_id, 'Cleared')
    return


def join(bot, event, *args):
    """<br/><i><b>join</b> [<id>]</i><br />Join the event <id>. Omitting <id> will join the latest created event."""
    yield from _joinEvent(bot, event, list(args))


def events(bot, event, *args):
    """<br/><i><b>events</b></i><br />List all the events for this hangout"""
    yield from _printEventList(bot, event)

def event(bot, event, *args):
    """<br />[botalias] <i><b>event</b> <name></i><br />Create an event titled <name>.<br /><u>Usage</u><br />[botalias] <i><b>event</b> Beergress tonight!</i><br />---<br />[botalias] <i><b>event join</b> [<id>]</i><br />Join the event <id>. Omitting <id> will join the latest created event.<br /><u>Usage</u><br />[botalias] <i><b>event join</b> 3</i><br />---<br />[botalias] <i><b>event leave</b> <id></i><br />Leave event <id>.<br /><u>Usage</u><br />[botalias] <i><b>event leave</b> 3</i><br />---<br />[botalias] <i><b>event list</b></i><br />List all the events for this hangout<br /><u>Usage</u><br />[botalias] <i><b>event list</b></i><br />---<br />[botalias] <i><b>event</b> <id> [--id]</i><br />List those attending event <id>. Append --id to return the full G+ IDs of the attendees.<br /><u>Usage</u><br />[botalias] <i><b>event</b> 3 --id</i><br />---<br />[botalias] <i><b>event rename</b> <id> <new name></i><br />Rename event <id><br /><u>Usage</u><br />[botalias] <i><b>event rename</b> 3 Beergress tomorrow night!</i><br />---<br />[botalias] <i><b>event cancel</b> <id></i><br />Cancel event <id><br /><u>Usage</u><br />[botalias] <i><b>event cancel</b> 3</i><br />---<br />[botalias] <i><b>event add</b> <id> <G+ ID></i><br />Add user to event <id> by their G+ ID<br /><u>Usage</u><br />[botalias] <i><b>event add</b> 3 110350977702120778591</i><br />---<br />[botalias] <i><b>event kick</b> <id> <G+ ID></i><br />Kick user from event <id> by their G+ ID<br /><u>Usage</u><br />[botalias] <i><b>event kick</b> 3 110350977702120778591</i>"""
    parameters = list(args)

    if not bot.memory.exists(['_event']):
        bot.memory.set_by_path(['_event'], {})

    if not bot.memory.exists(['_event', event.conv_id]):
        bot.memory.set_by_path(['_event', event.conv_id], {})

    conv_event = bot.memory.get_by_path(['_event', event.conv_id])

    if len(parameters) > 0:
        if parameters[0] == "cancel":
            if not len(parameters) == 2:
                yield from bot.coro_send_message(event.conv_id, '[ID] missing of the event you want to remove. Use <b>/events</b> to list the id\'s')
                return
            if not parameters[1].isdigit():
                yield from bot.coro_send_message(event.conv_id, 'Not a valid event id. Use <b>/events</b> to list the id\'s')
                return

            _key = _getEventById(conv_event, parameters[1])
            conv_event.pop(_key)
            bot.memory.set_by_path(['_event', event.conv_id], conv_event)
            yield from bot.coro_send_message(event.conv_id, "Event removed")
        elif parameters[0] == "list":
            yield from _printEventList(bot, event)
        elif parameters[0] == "join":
            newArgs = list(args)
            # remove first argument which is not needed
            newArgs.pop(0)
            yield from _joinEvent(bot, event, newArgs)
        elif parameters[0] == "add":
            if not len(parameters) == 3:
                yield from bot.coro_send_message(event.conv_id, 'Parameters missing. Command should be <b>/bot event add <event_id> <user_id></b>')
                return
            if not parameters[1].isdigit():
                yield from bot.coro_send_message(event.conv_id, 'Not a valid event id')
                return
            if not parameters[2].isdigit():
                yield from bot.coro_send_message(event.conv_id, 'Not a valid user id')
                return

            _event = _getEventById(conv_event, parameters[1])
            if _event is None:
                yield from bot.coro_send_message(event.conv_id, 'Event id does not exists, try <b>/bot events</b> to see all event id\'s')
                return;

            _newParticipantId = parameters[2];

            _newParticipant = None
            for u in event.conv.users:
               if(_newParticipantId == u.id_.chat_id):
                  _newParticipant = u
                  break

            if _newParticipant is None:
               yield from bot.coro_send_message(event.conv_id, 'Can\'t find this user in this hangout')
            else:
               yield from _join(bot, event, conv_event, _event, _newParticipant)

        elif parameters[0] == "leave":
            if not len(parameters) == 2:
                yield from bot.coro_send_message(event.conv_id, '[ID] missing of the event you want to leave. Use <b>/events</b> to list the id\'s')
                return
            if not parameters[1].isdigit():
                yield from bot.coro_send_message(event.conv_id, 'Not a valid event id. Use <b>/events</b> to list the id\'s')
                return

            _key = _getEventById(conv_event, parameters[1])
            if _key == None:
                yield from bot.coro_send_message(event.conv_id, 'Not a valid event id. Use <b>/events</b> to list the id\'s')
                return

            participants = conv_event[_key]['participants']
            if not event.user.id_.chat_id in participants.keys():
                yield from bot.coro_send_message(event.conv_id, 'No changes made. You didn\'t join this event before.')
                return

            participants.pop(event.user.id_.chat_id)
            conv_event[_key]['participants'] = participants
            bot.memory.set_by_path(['_event', event.conv_id], conv_event)
            yield from bot.coro_send_message(event.conv_id, '<b>{}</b> will not participate with <b>{}</b>'.format(event.user.full_name, conv_event[_key]['title']))

        elif parameters[0] == "kick":
            if len(parameters) < 3:
                yield from bot.coro_send_message(event.conv_id, 'Insufficient parameters. Command usage: /event kick <event_id> <google_id_user>')
                return
            if not parameters[1].isdigit():
                yield from bot.coro_send_message(event.conv_id, 'Not a valid event id. Use <b>/events</b> to list the id\'s')
                return
            if not parameters[2].isdigit():
                yield from bot.coro_send_message(event.conv_id, 'Id not valid. Google user id expected. <b>/event <event_id> --id</b> will show the google user id per user')
                return

            key = _getEventById(conv_event, parameters[1])
            if key == None:
                yield from bot.coro_send_message(event.conv_id, 'Not a valid event id. Use <b>/events</b> to list the id\'s')
                return

            participants = conv_event[key]['participants']
            if parameters[2] in participants.keys():
                del participants[parameters[2]]
                conv_event[key]['participants'] = participants
                bot.memory.set_by_path(['_event', event.conv_id], conv_event)
                yield from bot.coro_send_message(event.conv_id, 'Succesfully kicked')
            else:
                yield from bot.coro_send_message(event.conv_id, 'Can\'t find the given userId to kick from the event')
        elif parameters[0] == "rename":
            if len(parameters) < 3:
                yield from bot.coro_send_message(event.conv_id, 'Insufficient parameters. Command usage: /event rename <event_id> <hangout_title>')
                return
            if not parameters[1].isdigit():
                yield from bot.coro_send_message(event.conv_id, 'Not a valid event id. Use <b>/events</b> to list the id\'s')
                return

            key = _getEventById(conv_event, parameters[1])
            if key == None:
                yield from bot.coro_send_message(event.conv_id, 'Not a valid event id. Use <b>/events</b> to list the id\'s')
                return

            del parameters[0:2]
            title = ' '.join(parameters).replace("'", "").replace('"', '')
            conv_event[key]['title'] = ' '.join(
                parameters).replace("'", "").replace('"', '')
            bot.memory.set_by_path(['_event', event.conv_id], conv_event)
            yield from bot.coro_send_message(event.conv_id, 'Event name Succesfully changed')
        elif parameters[0].isdigit():
            key = _getEventById(conv_event, parameters[0])
            if key == None:
                yield from bot.coro_send_message(event.conv_id, 'Not a valid event id. Use <b>/events</b> to list the id\'s')
                return

            _event = conv_event[key]
            participants = _event['participants']

            showId = False
            if len(parameters) > 1 and parameters[1] == '--id':
                showId = True

            _owner = _event['owner']

            html = []
            for num, key in enumerate(sorted(participants, key=str)):
                row = "<b>{}</b>. {}".format(str(num + 1), participants[key])
                if _owner == key:
                    row += ' (owner)'
                if showId:
                    row += ' <b>id:</b> {}'.format(key)
                html.append(row)

            # Generate the output list. Title first, then the participants
            html.insert(
                0, "Participants in <b>{}:</b>".format(_event['title']))
            message = _("<br />".join(html))

            yield from bot.coro_send_message(event.conv_id, message)
        else:
            title = ' '.join(parameters).replace("'", "").replace('"', '')
            body = {}
            body['hangout'] = 0
            body['title'] = title
            body['owner'] = event.user.id_.chat_id
            body['participants'] = {}
            key = "event:{}:{}".format(event.conv_id, title)
            conv_event[key] = body
            conv_event['_current'] = key
            bot.memory.set_by_path(['_event', event.conv_id], conv_event)
            yield from bot.coro_send_message(event.conv_id, "Event <b>{}</b> created. type /bot join to rsvp".format(title))

        return

    bot.memory.save()


@asyncio.coroutine
def _join(bot, event, conv_event, _key, _user):
    _event = conv_event[_key]

    if _user is not None:
       _newUser = _user
    else:
       _newUser = event.user

    participants = _event['participants']
    participants[_newUser.id_.chat_id] = _newUser.full_name

    _event['participants'] = participants
    conv_event[_key] = _event

    bot.memory.set_by_path(['_event', event.conv_id], conv_event)
    yield from bot.coro_send_message(event.conv_id, '<b>{}</b> joined <b>{}</b>'.format(_newUser.full_name, conv_event[_key]['title']))

    return

@asyncio.coroutine
def _printEventList(bot, event):
    """List all available events of current hangout"""
    conv_event = bot.memory.get_by_path(['_event', event.conv_id])
    html = []
    for num, key in enumerate(sorted(conv_event, key=str)):
        segment = key.split(':')
        if segment[0] == "event":
            html.append("{}. <b>{}</b> [{} people]".format(str(num), conv_event[
                        key]['title'], len(conv_event[key]['participants'])))

    if len(html) == 0:
        yield from bot.coro_send_message(event.conv_id, '<i>No events available yet. Use <b>/event <eventname></b> to create your own event</i>')
        return
    # Generate the output list. Title first followed by the participants
    html.insert(0, _("<b>Current available events:</b>"))
    message = _("<br />".join(html))

    yield from bot.coro_send_message(event.conv_id, message)
    return

@asyncio.coroutine
def _joinEvent(bot, event, parameters):
    conv_event = bot.memory.get_by_path(['_event', event.conv_id])
    if len(parameters) == 0:
        if not '_current' in conv_event.keys():
            yield from bot.coro_send_message(event.conv_id, 'No event created yet.')
            return

        _key = conv_event['_current']
        conv_event = yield from _join(bot, event, conv_event, _key, None)
    else:
        id = parameters[0]
        if not id.isdigit():
            yield from bot.coro_send_message(event.conv_id, 'Please submit a valid event id. <b>/events</b> list the event id\'s')
            return
        found = False
        for num, key in enumerate(sorted(conv_event, key=str)):
            if (num) == int(id):
                # submit to hangout
                yield from _join(bot, event, conv_event, key, None)
                found = True
                break
        if found == False:
            yield from bot.coro_send_message(event.conv_id, 'Id doesn\'t exist. <b>/events</b> list the event id\'s')
            return

def _getEventById(conv_event, id):
    for num, key in enumerate(sorted(conv_event, key=str)):
        if (num) == int(id):
            # ignore other keys. Only return keys based on the event key format
            # event:conv_id:name_event
            if not key.split(':')[0] == 'event':
                return None
            return key
    return None
