//Create the namespace if it doesn't already exist
var ForgePlugins = ForgePlugins || {};

//Constructor
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
     * _onClickHandler will handler the dispatch of the plugin event in response
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