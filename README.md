This repository contains a plugin for [hangouts-bot](https://github.com/hangoutsbot/hangoutsbot). Simply put the python script ```event.py``` in the plugins folder which is located in the hangupsbot directory. Last but not least, add ```event``` to the config file of your bot and restart the bot to enable the plugin.

# Event-plugin

All the commands below are shown with the **!** prefix to trigger the bot and keep the examples short. When not having this prefix enabled for your hangoutsbot you probably have to trigger the events with **/bot**. 

### Actions for **event**

```! event <name>``` create event

```! event rename <number> <name>```

```! event <number>``` list participants of event

```! event <number> --id``` list the user id of the participants

```! event leave <number>``` 

```! event remove <number>``` remove entire event

```! event kick <number> <user_id>``` 

```! event hangout <number>``` **[Available in next update]** start a hangout with all participants


### Get a list of available events in your hangout


```! events``` Get a list of all available events and list the id's per event

### Join an event



```! join``` join latest created event

```! join <number>```

### Help

For more help, type ```! help <command>``` to get help for the specified command from the bot.


