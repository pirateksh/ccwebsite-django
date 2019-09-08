[TOC]

This tutorial is the continuation of the **plugin development part 2**, we recommend to do the previous parts before this one.

## Tutorial objectives

In this tutorial we will see that we have access to the main loop of ForgeJS through the update method. We will add an update method to move the rectangle around. This example may not be the most useful feature but it demonstrate that we have access to the update loop!

## The update method

The `FORGE.PluginManager` will call every frame the update method of each plugins if this method exists. In the code sample below, we add an update method with a few lines of code that will move the rectangle around the screen and make it bounce on the screen borders.

```js
// Create the namespace if it doesn't already exist
var ForgePlugins = ForgePlugins || {};

// Constructor
ForgePlugins.MyPlugin = function()
{
    this._displayObject = null;
    this._speedX = 5;
    this._speedY = 4;
};

ForgePlugins.MyPlugin.prototype =
{
    /**
     * Boot function
     */
    boot: function()
    {
        this._displayObject = this.plugin.create.displayObject();
        this.plugin.container.addChild(this._displayObject);

        // ... See previous tutorials for full source of this method
    },

    /**
     * Update function
     */
    update: function(event)
    {
        // Check if the rectangle is leaving the plugin container from the left or right border.
        if(this._displayObject.x >= this.plugin.container.pixelWidth - this._displayObject.pixelWidth
            || this._displayObject.x < 0)
        {
            // Revert the speed of the X axis.
            this._speedX *= -1;
        }

        // Check if the rectangle is leaving the plugin container from the top or bottom border.
        if(this._displayObject.y >= this.plugin.container.pixelHeight - this._displayObject.pixelHeight
            || this._displayObject.y < 0)
        {
            // Revert the speed of the Y axis.
            this._speedY *= -1;
        }

        this._displayObject.x += this._speedX;
        this._displayObject.y += this._speedY;
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
