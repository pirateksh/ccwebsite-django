[TOC]

This tutorial is the continuation of the **plugin development part 1**, we recommend to do the previous parts before this one.

## Tutorial objectives

In this tutorial we will see how we can add events to our plugin to bind an action on user click.

## Plugin events

To add events to the plugin we have to do a few things:

- Add the event to the plugin manifest.
- Dispatch the event from the plugin code.
- Test the event by binding an action in the json configuration.

### The manifest

In this tutorial we will add an event to handle the user's click on our rectangle. To do that we need to add an `events` object that will define the events name associated by default to a `null` action. The manifest now looks like this with a new `onClick` event.

```js
{
    "uid": "org.forgejs.myplugin",

    "options":
    {
        "background": "blue"
    },

    "events":
    {
        "onClick": null
    },

    "sources":
    [
        "src/main.js"
    ],

    "constructor": "ForgePlugins.MyPlugin"
}
```

!!! This is not mandatory but we prefix our events by the `on` keyword, that's why why called our event `onClick`.

### Dispatch the event

Once we have declared our event in the manifest json file, we need to dispatch the event from the code. In our example we need to catch a pointer onClick event and re-dispatch it from the plugin events module. Below is the full commented code of the plugin.

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

        // Enable the pointer module of the displayObject
        this._displayObject.pointer.enabled = true;

        // Set the cursor to pointer
        this._displayObject.pointer.cursor = "pointer";

        // Listen to the onClick event with the pointer module
        // and redirect the event to our handler _onClickHandler
        this._displayObject.pointer.onClick.add(this._onClickHandler, this);

        // Add the displayObject to the plugin container
        this.plugin.container.addChild(this._displayObject);
    },

    /**
     * _onClickHandler will handle the dispatch of the plugin event in response
     * to the user's click on the displayObject
     */
    _onClickHandler: function(event)
    {
        this.plugin.events.onClick.dispatch();
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

Since part 1 of this tutorials series we've added a few lines of code:

- We enabled the pointer module of the displayObject to catch the click event from the user.
- We set a different cursor for the displayObject that'll tell the user our displayObject is clickable.
- We added an event handler to the onClick event of the pointer module of the displayObject.
- Declared the event handler function `_onClickHandler` that will dispatch our plugin `onClick` custom event.

## Bind actions to the event

Now that our event is dispatched by the `events` module of our plugin, we can bind actions to it from our main json configuration! If you don't know what actions are, we recommend you read the actions related tutorials.

To add an action and bind it to our `onClick` event we need two add a few things to the json configuration:

- Add `actions` array to the json configuration.
- Add an `action` object to the `actions` array.
- Add the `events` object to our plugin instance.
- Bind our `action` to the `onClick` event of the plugin instance.

```js
{
    "story": { ... },

    "actions":
    [
        {
            "uid": "action-0",
            "target": "viewer.camera",
            "method":
            {
                "name": "lookAt",
                "args": [0, 90, 0, null, 1500, true]
            }
        }
    ],

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
                },

                "events":
                {
                    "onClick": ["action-0"]
                }
            }
        ]
    }
}
```

So, we've added an action identified by `action-0`. This action will call the `lookAt` method of the camera to animate it to pitch 90 over 1500 milliseconds. Then we add the `events` object to the plugin instance configuration and bind the `action-0` to our `onClick` event.

That's it! Now if you click on the rectangle, the camera will move to pitch 90! Of course you are free to bind any action you want to your events. And you can dispatch any events you want from your plugin as long as you've declared them in the manifest.