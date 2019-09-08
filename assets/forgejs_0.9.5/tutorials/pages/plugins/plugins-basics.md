[TOC]

## What is a plugin?

Plugins are external modules that are not part of the ForgeJS core. For any special feature need that is not included in the core you will have to find or develop a plugin that will extend the core features for your project and match your needs.

You can do anything you want with plugins, here are some use cases :

- Make user interface components for anything like video controls, navigation through scenes, geolocalization on a map...
- Make an analytics module to get statistics on how your project is viewed by users.
- Add 3D content to the scene that is not handled by the core like particle systems.

## Where to find plugins?

We release official ForgeJS team plugins on our GitHub repository dedicated to plugins. (Coming soon).
We also have a forum where users can share their creations.
If you develop useful plugins and you want to share them with the community, get in touch with users on the ForgeJS forum!

## How to use plugins?

You do not need to manually load the plugins' javascript source files into your web page, the ForgeJS framework handles the loading of the source files and assets needed by the plugins. Each plugin is bundled in a folder that contains a mandatory manifest file, the sources and the assets.

### Project hierarchy

To include a plugin to your project you will have to copy the entire folder of the plugin into the main plugin folder. By default, ForgeJS will look for a folder nammed `plugins` located at the root of your project.

```
project/
|
├── plugins/
|   |
│   └── MyPlugin/
|   |   |
|   |   └── src/
|   |   |   |
|   |   |   └── main.js
|   |   |
|   |   └── manifest.json
|   |
│   └── MyOtherPlugin/
|       |
|       └── src/
|       |   |
|       |   └── main.js
|       |
|       └── assets/
|       └── manifest.json
|
├── index.html
└── config.json
```

### Plugins configuration

The root of the json configuration has a global `plugins` object to declare which plugin engines to load and which plugin engines to instantiate for the whole project.

```js
{
    "story": { ... },

    "plugins":
    {
        "enabled": true,
        "prefix": "./plugins/",

        "engines":
        [
            {
                "uid": "org.forgejs.myplugin",
                "url": "MyPlugin/",
                "manifest": "manifest.json"
            }
        ]

        "instances":
        [
            {
                "uid": "org.forgejs.myplugin-0",
                "engine": "org.forgejs.myplugin",
                "options": {},
                "data": {},
                "index": 10
            }
        ]
    }
}
```

- `enabled` - The global switch to turn on or off all plugins of the project.
- `prefix` - The folder where ForgeJS will look for your plugins' engines' sources relative to the root of the project. Here you can change the default `./plugins` folder prefix.
- `engines` - The array of engines that ForgeJS will load.
- `instances` - The array of instances that ForgeJS will create for the whole project.

#### Engines

In the `plugins` json configuration, `engines` is an array that declares all plugins ressources that you will be able to instantiate on your project.


```js
{
    "story": { ... },

    "plugins":
    {
        "enabled": true,
        "prefix": "./plugins/",

        "engines":
        [
            {
                "uid": "org.forgejs.myplugin",
                "url": "MyPlugin/",
                "manifest": "manifest.json"
            },

            {
                "uid": "org.forgejs.myotherplugin",
                "prefix": "./customPluginsFolderLocation/"
                "url": "MyOtherPlugin/",
                "manifest": "manifest.json"
            }
        ]

        "instances": [ ... ]
    }
}
```

- `uid` - The unique identifier of the plugin engine.
- `prefix` - If the plugin is not located in the global plugins folder you can specify here another location for this particular plugin.
- `url` - The url of the plugin relative to the prefix folder.
- `manifest` - The name of the plugin manifest file. The default name is "manifest.json".

#### Instances

A plugin instance is an occurence of a plugin engine. You can have several plugin instances that use the same plugin engine.

```js
{
    "story": { ... },

    "plugins":
    {
        "enabled": true,
        "prefix": "./plugins/",

        "engines":
        [
            {
                "uid": "org.forgejs.myplugin",
                "url": "MyPlugin/",
                "manifest": "manifest.json"
            }
        ]

        "instances":
        [
            {
                "uid": "org.forgejs.myplugin-0",
                "enabled": true,
                "engine": "org.forgejs.myplugin",
                "scenes": ["scene-0", "scene-1"],
                "options": {},
                "data": {},
                "events": {},
                "keep": true,
                "index": 10
            }
        ]
    }
}
```

- `uid` - The unique identifier of the plugin instance.
- `enabled` - Enabled flag for the plugin instance.
- `engine` - The unique identifier of the plugin engine to instanciate.
- `scenes` - The array of scene unique identifiers
- `options` - The plugin's options object. The options are described in the plugin's manifest file.
- `data` - The plugin's data object. The data are described in the plugin's manifest file.
- `events` - The plugin's event object. The available events are described in the plugin's manifest file.
- `keep` - This flag specifies if the plugin is kept or not when the scene changes.
- `index` - If the plugin is a graphical one, it sets the index of the plugin container.

