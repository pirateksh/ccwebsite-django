[TOC]

If you do not find an existing plugin that fits your needs, you can develop your own plugin and eventually share it with the community.

To develop and test a plugin you will need to:

- Create a folder that will contain all the plugin's files.
- Create a **manifest.json** file that describes your plugin.
- Create javascript file(s) that will contain the code of your plugin.
- Create an instance of the plugin in a ForgeJS project json configuration to test it.

## Tutorial objectives

In this tutorial we will develop a very simple plugin which we will name "MyPlugin" and instantiate it on a basic test project.
The plugin will just display a colored rectangle at the top left of the screen. The background color of the rectangle should be customizable through options.
This project will be extended in other tutorials.

## Project hierarchy

As a reminder of the "Plugins basics" tutorial, here's how it looks like in our project file hierarchy:

```
project/
|
├── plugins/
|   |
│   └── MyPlugin/
|       |
|       └── src/
|       |   |
|       |   └── main.js
|       |
|       └── manifest.json
|
├── index.html
└── config.json
```

We have the main **plugins** folder for all plugins that will be used in our project.
In this main **plugins** folder we have to create a folder for our plugin that will contain all the plugin's files. We name it **MyPlugin**.

At the root of **MyPlugin** folder we will have:

- The **manifest.json** file that will describe our plugin.
- A **src** folder that will contain our javascipt file **main.js**

## The manifest

We will write a minimalist manifest.json file with only the mandatory fields.
A unique identifier (`uid`), the source related fields (`sources` and `constructor`) and the `options` object for customization.
Save this file as "manifest.json" at the root of "MyPlugin" folder.


```js
{
    "uid": "org.forgejs.myplugin",

    "options":
    {
        "background": "blue"
    },

    "sources":
    [
        "src/main.js"
    ],

    "constructor": "ForgePlugins.MyPlugin"
}
```

## The sources

The sources of this plugin are all located in the **src/main.js** file. It is not mandatory but we recommend you to have a namespace for your plugins. Here we will use `ForgePlugins` as a namespace but you are free to choose your own.

A plugin must have two mandatory methods that are `boot` and `destroy`.

Here is the complete code of our **main.js** plugin code:

```js
// Create the namespace if it doesn't already exist
var ForgePlugins = ForgePlugins || {};

// Constructor
ForgePlugins.MyPlugin = function()
{
    this._displayObject = null;
};

ForgePlugins.MyPlugin.prototype =
{
    /**
     * Boot function
     */
    boot: function()
    {
        // Create a display object with the factory
        this._displayObject = this.plugin.create.displayObject();

        // Assign options to the displayObject
        this._displayObject.background = this.plugin.options.background;
        this._displayObject.width = 100;
        this._displayObject.height = 50;

        // Add the displayObject to the plugin container
        this.plugin.container.addChild(this._displayObject);
    },

    /**
     * Destroy function
     */
    destroy: function()
    {
        this._displayObject = null;
    }
};
```

### The boot method

The boot method is the first method the plugin will call. This method does the following things:

- Create a `displayObject` through the plugin object factory.
- Assign the background color of the displayObject from the option object.
- Give the displayObject a size of 100x50.
- Add the displayObject to the plugin container.

### The destroy method

The destroy method is the last method called by the plugin manager when the instance is destroyed. The only thing we do in this method is to nullify the reference of the displayObject.

### The this object in plugin code

The `this` object is a reference to your plugin instance but the plugin manager automatically adds some useful references to it:

- `this.viewer` - You always have access to the main `viewer` object through `this.viewer`.
- `this.plugin` - Your instance is contained in a `FORGE.Plugin` object, you have access to it through `this.plugin`.
- `this.plugin.create` - This is the reference to the object factory handled by the `FORGE.Plugin`.
- `this.plugin.container` - This is the reference to the container created by the `FORGE.Plugin`. You can add your graphic objects to it either by using a ForgeJS.DisplayObject and use addChild to add it the `this.plugin.container` or add a classic dom object using the appendChild of the `this.plugin.container.dom` that is a HTML `<div></div>` element.

!! You should never try to override the `this.viewer` or the `this.plugin` reference in your plugin code.

!!! Objects that are created through the object factory (accessible via `plugin.create`) are automatically released from the memory by the ForgeJS framework when the instance is destroyed. That is why we use the factory and the displayObject to create a `<div></div>` element, but you are free to code whatever you want and use your own  components.


## Test the plugin

To test the plugin we have to instantiate it on a simple project to see the result. Here is a basic project configuration with the declaration of the plugin engine and an instance of this engine.

```js
{
    "story":
    {
        "scenes":
        [
            {
                "uid": "scene-0",

                "media":
                {
                    "uid": "media-0",
                    "type": "image",

                    "source":
                    {
                        "format": "equi",
                        "url": "path/to/panorama.png"
                    }
                }
            }
        ]
    },

    "plugins":
    {
        "engines":
        [
            {
                "uid": "org.forgejs.myplugin",
                "url": "MyPlugin/"
            }
        ],

        "instances":
        [
            {
                "uid": "myplugin-instance-0",
                "engine": "org.forgejs.myplugin"
            }
        ]
    }
}
```

In this project we have a single scene and an instance of "MyPlugin". If you run the project in your web browser, you should see a blue rectangle at the top left of your container.

## Customization with options

We add the possibility to customize the rectangle background color. Let see if we can change the background color of the rectangle.
In the following configuration example, we just add the `options` object to override the default blue color to green.

```js
{
    "story": { ... },

    "plugins":
    {
        "engines":
        [
            {
                "uid": "org.forgejs.myplugin",
                "url": "MyPlugin/"
            }
        ],

        "instances":
        [
            {
                "uid": "myplugin-instance-0",
                "engine": "org.forgejs.myplugin",

                "options":
                {
                    "background": "green"
                }
            }
        ]
    }
}
```

You can enhance the customizable aspect of your plugin by adding many options of your choice.
For example you can add options to set the size (that is actually hardcoded in the boot function to 100x50), the position and whatever you want to make customizable.









