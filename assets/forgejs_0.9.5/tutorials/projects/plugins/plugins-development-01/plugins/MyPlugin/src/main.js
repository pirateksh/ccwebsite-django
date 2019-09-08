//Create the namespace if doesn't already exist
var ForgePlugins = ForgePlugins || {};

//Constructor
ForgePlugins.MyPlugin = function()
{
    this._displayObject = null;
};

ForgePlugins.MyPlugin.prototype =
{
    /**
     * The boot function
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
     * Destroy the text field
     */
    destroy: function()
    {
        this._displayObject = null;
    }
};