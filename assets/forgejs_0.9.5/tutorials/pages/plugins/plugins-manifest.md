[TOC]

## The manifest file

Each plugin engine must have a manifest file, it's mandatory for each plugin. This manifest file descibes many aspects of a plugin:

- General information like name, description, version, author, licence etc...
- The compatibility of the plugin regarding the ForgeJS version or the device itself.
- Where are located the javascript sources, CSS, and what is the name of the constructor to instantiate.
- Which are the available options, events or actions.

If you use a plugin you should find a lot of useful information in its manifest file. If you are a plugin developper, this is the first file you will create to describe your plugin.

A manifest file looks like this:

```js
{
    "uid": "org.forgejs.myplugin",
    "name": "My awesome plugin",
    "shortName": "myPlugin",
    "description": "My plugin description",
    "version": "1.0.0",
    "url": "http://forgejs.org/plugins/myPlugin",

    "author":
    {
        "name": "ForgeJS Team",
        "url": "http://forgejs.org"
    },

    "licence":
    {
        "name": "Apache 2",
        "url": "https://www.apache.org/licenses/LICENSE-2.0"
    },

    "viewer":
    {
        "min": "1.0.0",
        "max": "1.5.2"
    },

    "device":
    {
        "mobile": true
    },

    "data":
    {
        "Any custom data required by the plugin"
    },

    "options":
    {
        "color": "blue",
        "size": 20
    },

    "events":
    {
        "onClick": null
    },

    "actions":
    [
        "show",
        "hide"
    ],

    "sources":
    [
        "src/main.js"
    ],

    "constructor": "ForgeJSPlugins.MyPlugin"
}
```

- `uid` - The unique identifier of the plugin engine.
- `name` - The name of the plugin.
- `shortName` - The short name of the plugin.
- `description` - The description of the plugin. Keep this description to fewer than 140 characters.
- `version`: The current version number of the plugin.
- `url` - The home page of the plugin, which might be on forgejs.org or on your own website. This must be unique to your plugin.
- `author.name` - The name of the plugin author.
- `author.url` - The author's website.
- `licence.name` - The name of the plugin's license (e.g. Apache 2, MIT).
- `licence.url` - The link to the license text (e.g. [https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)).
- `viewer.min` - The ForgeJS viewer minimum version which the plugin is compatible with.
- `viewer.max` - The ForgeJS viewer maximum version which the plugin is compatible with.
- `device` - The device limitations of the plugin.
- `data` - The data object is an object that provides data to the plugin engine.
- `options` - The default plugin's options.
- `events` - The list of events dispatched by the plugin.
- `actions` - An array of callable actions of the plugin.
- `sources` - An array of Javascript or CSS source files.
- `constructor` - The name of the plugin constructor (e.g. ForgePlugins.MyPlugin).

## Version restrictions

You can verify which version of forgeJS is compatible with a plugin or restrict the use of a plugin to a specific version of ForgeJS if you are a plugin developper. You can do that by using the `viewer` object of the manifest. In the previous example, the plugin is compatible with ForgeJS versions between 1.0.0 and 1.5.2

```js
"viewer":
{
    "min": "1.0.0",
    "max": "1.5.2"
}
```

## Device restrictions

Not every plugin is usable on every device. Sometimes a plugin needs a specific feature on the device or a specific kind of device in order to work properly. For example if your plugin needs a mobile device to be functional you will specify this in the `device` object of the manifest.

```js
"device":
{
    "mobile": true
}
```

The ForgeJS has a ForgeJS.Device class that will check many aspects of your device. The `device` manifest object needs to use the properties names of the `ForgeJS.Device` class to check the device. In this example you need the `mobile` property of the `ForgeJS.Device` to be `true`.

## Plugin options

The manifest has an `options` object that describes which are the plugins options and their default values. Here is an example of an `options` object:

```js
"options":
{
    "color": "blue",
    "size": 20
}
```

If you want to change these options, you can override the `options` object in your plugin instance declaration in the json configuration of your project.

Here what a plugin instance configuration with custom options may look like:

```js
{
    "uid": "org.forgejs.myplugin-0",
    "engine": "org.forgejs.myplugin",

    "options":
    {
        "color": "green"
    }
}
```

In this example the plugin instance identified by `org.forgejs.myplugin-0` will have its `color` option set to green. The `size` option will remain the same as the default value declared in the manifest file because no other value is set in the instance `options` object.

## Plugin events

Plugins can emit events. The available events are described in the `events` object of the manifest with a `null` value assigned. By convention all events names start by "on...", like `onClick`.

```js
"events":
{
    "onClick": null
}
```

It's up to you to decide what to do in response to a plugin event. For that you can set in your plugin instance configuration an array of actions to execute in response to an event. If you don't know what actions are, there is a tutorial available for you.

Here what a plugin instance configuration with actions binded to an event may look like:

```js
{
    "uid": "org.forgejs.myplugin-0",
    "engine": "org.forgejs.myplugin",

    "events":
    {
        "onClick": ["action-0", "action-1"]
    }
}
```

We assume that this plugin is a graphical one and if the user clicks on it the action manager will execute "action-0" then "action-1".

## Plugin actions

Plugin actions are methods that are exposed by the plugin instance. The array is here just to list these method names. In this example we know that the plugin engine has two exposed methods usable by actions.

```js
"actions":
[
    "show",
    "hide"
]
```

If we want to declare in the project json configuration an action that uses one of these plugin instance methods we can do it like this:

```js
"actions":
[
    {
        "uid": "action-hide",
        "target": "org.forgejs.myplugin-0",
        "method":
        {
            "name": "hide"
        }
    }
]
```