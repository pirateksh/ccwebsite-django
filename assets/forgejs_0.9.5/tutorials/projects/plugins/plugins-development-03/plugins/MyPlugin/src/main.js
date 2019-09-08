//Create the namespace if it doesn't already exist
var ForgePlugins = ForgePlugins || {};

//Constructor
ForgePlugins.MyPlugin = function()
{
    this._displayObject = null;
    this._speedX = 5;
    this._speedY = 3;
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