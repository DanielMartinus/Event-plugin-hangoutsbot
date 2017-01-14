This repository contains a plugin for [hangouts-bot](https://github.com/hangoutsbot/hangoutsbot). Simply put the python script ```events.py``` in the plugins folder which is located in the hangupsbot directory. Last but not least, add ```events``` to the config file of your bot and restart the bot to enable the plugin.

# Event-plugin

All the commands below are shown with the **!** prefix to trigger the bot and keep the examples short. When not having this prefix enabled for your hangoutsbot you probably have to trigger the events with **/bot**.

### Actions for **event**

```! event <name>``` create event

```! event rename <event_number> <name>```

```! event join``` join latest created event

```! event join <id>``` join event with id

```! event list``` print list of all available events

```! event <event_number>``` list participants of event

```! event <event_number> --id``` list the user id of the participants

```! event leave <event_number>``` leave event by event id

```! event add <event_id> <user_id>``` add user by googleId

```! event remove <event_number>``` remove entire event

```! event kick <event_number> <user_id>```

```! event hangout <event_number>``` **[Available in next update]** start a hangout with all participants


### Get a list of available events in your hangout


```! events``` Get a list of all available events and list the id's per event

### Join an event



```! join``` join latest created event

```! join <number>```

### Help

For more help, type ```! help <command>``` to get help for the specified command from the bot.


### TO-DO

- Create hangout with all participants
- Let everyone automatically join the hangout after hangout is created and joining the event
- Turn of auto join to hangout by owner of the event
- Add guests (people who are not in the hangout)
- ~~Add a person manually via googleId to an event~~
