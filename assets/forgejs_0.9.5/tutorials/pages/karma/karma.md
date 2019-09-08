
Good to know about writting KEN tests for Karma !
--------------------------------------------


#### Delay between test

If you resize the main DOM container you will have to wait before doing tests because the KEN.ScaleManager check the size every 10 frames. <br>
To achieve that, I'll use the "done" callback of jasmine to delay the next test.

```javascript
describe("my test", function()
{
    it("should resize the main container then wait 500ms", function(done)
    {
        //Reset container size
        div.style.width = "800px";
        div.style.height = "600px";

        //Wait before using the done callback !
        setTimeout(function(){ done(); }, 500);
    }); 

    it("should run this test 500ms later ...", function()
    {
        // .........
    });
});
```

This technique is also used to delay an asynchrone test, while loading a ressource for example !


#### The requestAnimationFrame / update issue

The browsers in which the test are executed are not focused by the user. This causes the requestAnimationFrame and timeout to pause ... To deal with this I recommend to have all browsers displayed on screen to avoid this "sleep".