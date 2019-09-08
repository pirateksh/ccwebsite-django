[TOC]

What about interactivity with our hotspots?
Hotspots have an event system to bind actions to specific events.
In the following example you can click on hotspots to go to another scene because an action is bound to the `onClick` event.

<iframe src="http://kenprivatebeta.kolor.com/releases/latest/samples/projects/hotspots-actions/"></iframe>

## Binding actions to hotspot events

If you don't know anything about `actions`, you should read the [action tutorial](#). We will not explain how to declare actions here, all you need to know is that actions describes what to do when you click a hotspot for example. It describe a behavior, and it has a unique identifier (uid).

To add actions on a hotspot event, you have to declare them in the **hotspot** configuration by associating an action uid to an event type.

```js
"hotspots":
[
    {
        "uid": "hotspot-0",
        "material":
        {
            "image": "hotspot-0.jpg"
        },
        "events":
        {
            "onClick": [ "action-1", "action-2" ],
            "onOver": "action-0",
            "onOut": "action-3"
        }
    }
]
```

You can associate a single action to an event or an array of actions that will be executed in the same order as the array order.

## Events type

### onClick

`onClick` event is triggered when the user clicks with their pointer device on the hotspot or taps the hotspot on a touch screen.

### onOver

`onOver` event is triggered when the pointer hovers over the hotspot.
!! This event will not be triggered on touch screen.

### onOut

`onOut` event is triggered when the pointer leaves the hotspot.
!! This event will not be triggered on touch screen.
