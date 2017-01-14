This repository contains a plugin for [hangouts-bot](https://github.com/hangoutsbot/hangoutsbot). Simply put the python script ```events.py``` in the plugins folder which is located in the hangupsbot directory. Last but not least, add ```events``` to the config file of your bot and restart the bot to enable the plugin.

# Event-plugin

All the commands below are shown with the **!** prefix to trigger the bot and keep the examples short. When not having this prefix enabled for your hangoutsbot you probably have to trigger the events with **/bot**.

### Actions for **event**

```! event <name>``` Create an event titled <name>

```! event join <id>``` Join the event <id>. Omitting <id> will join the latest created event.

```! event leave <event_number>``` Leave event <id>.

```! event list``` List all the events for this hangout

```! event <id> [--id]``` List those attending event <id>. Append --id to return the full G+ IDs of the attendees.

```! event rename <id> <name>``` Rename event <id>

```! event cancel <event_number>``` Cancel event <id>

```! event add <id> <G+ ID>``` Add user to event <id> by their G+ ID

```! event kick <id> <G+ ID>``` Kick user from event <id> by their G+ ID


### Get a list of available events in your hangout


```! events``` List all the events for this hangout

### Join an event


```! join``` join latest created event

```! join <id>``` join the event <id>

### Help

For more help, type ```! help <command>``` to get help for the specified command from the bot.


### TO-DO

- Create hangout with all participants
- Let everyone automatically join the hangout after hangout is created and joining the event
- Turn of auto join to hangout by owner of the event
- Add guests (people who are not in the hangout)
- ~~Add a person manually via googleId to an event~~
