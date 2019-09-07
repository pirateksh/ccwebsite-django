[TOC]

Actions are a way to declare a property change or a method call from our json configuration. After declaring an action you can bind it to an event by its unique identifier. This way you can for example tell that a specific action will be triggered when the user clicks on a specific hotspot.

Actions are declared gloabally at the root of the json configuration. It is an array of `action` objects. A single action can be bound to many events in the json configuration. Here is a first example of an action object declaration.

```js
"actions":
[
    {
        "uid": "action-0",
        "target": "viewer.story",
        "method": { "name": "nextScene" }
    }
]
```

An action object is composed of four parts, here is a quick overview:

- `uid` - The unique identifier of the action **(required)**.
- `target` - The description of the target who owns the method to call or the property to change **(required)**.
- `method` - The description of the method to call.
- `property` - The description of a property to modify.

## Target

An action always has a target that owns the method to execute or the property to modify. It can be identified either with :
- A known unique identifier (uid) of another object of your json configuration.
- An `accessor` to describe the target by a string in pointed syntax from the **viewer** object.
- A combination of an `identifier` and an `accessor`.

Target can have multiple syntax depending on your needs, we will see that it can be a `string` or an `object`.

If you do not specify target, the target will be the `window` object and the framework will try to extecute a method or change a property declared on `window`.

### Using identifier (uid)

You know the unique identifier of the target, as it is declared in json configuration file. You can then specify it using one of the following syntaxes :

The `string` syntax:
```js
"target": "target-uid"
```

The `object` syntax:
```js
"target":
{
    "identifier": "target-uid"
}
```

In both exmaples "target-uid" is a unique identifier used by another object in your json configuration.

### Using accessor

An accessor is a `string` using pointed syntax that will make reference to an existing object. If your accessor starts with the keyword `viewer` the accessor will be resolved starting from the current viewer instance, this way you can target any submodule of the viewer like the camera (`viewer.camera`) or anything else accessible from the viewer. In any other case your accessor will look for your target starting from the window object.

The `string` syntax:
```js
"target": "viewer.camera"
```

The `object` syntax:
```js
"target":
{
    "accessor": "viewer.camera"
}
```

### Using both

You can have the special need to target a specific member of an object that have a unique identifier. In this case you can use the target `object` syntax with both `identifier` and `accessor`.

```js
"target":
{
    "identifier": "target-uid",
    "accessor": "target.member.accessor"
}
```

## Method

Once you get your target, you'll want to do something with it like executing one of its methods. For example if we target the `viewer.camera`, it is possible to execute the lookAt method with some arguments.

```js
"actions":
[
    {
        "uid": "action-camera-0",
        "target": "viewer.camera",
        "method":
        {
            "name": "lookAt",
            "args": [40, 20]
        }
    }
]
```

This action will execute the `lookAt` method of the `viewer.camera` using the array of arguments `[40, 20]`. If we execute this action the camera will look at yaw 40 and pitch 20 degrees!

- `name` - The public name of the method to execute on the target.
- `args` - The optional arguments to pass to the method.

## Property

In addition of methods, your target also has properties that you can change by setting another value or increment the current value if it's a number or anything else you may want to do with an object property.

```js
"actions":
[
    {
        "uid": "action-camera-0",
        "target": "viewer.camera",
        "property":
        {
            "name": "yaw",
            "value": 40,
            "operation": "set"
        }
    }
]
```

This action will set the camera yaw property to 40. Note that the `operation` is `set` by default so to set a value you just have to specify a `name` and a `value`.

- `name` - The public name of the property to affect on the target.
- `value` - The value used by the operation.
- `operation` - The optional operation to make with the property and the value.

### Operations

The operation specifies what to do with the property and the value. If your property is a number or a boolean, you may want to execute an arithmetic operation on it or toggling it from `true` to `false`. Specifying the operation is optional, the default operation is `set`.

Operation can be one of the following :

- `set` - Set the property to the value (default).
- `add` - Add the value to the property.
- `substract` - Substract the value from the property.
- `multiply` - Multiply the property by the value.
- `divide` - Divide the property by the value.
- `toggle` - Toggle the property to false if it was true, or the other way around (only works if the property is `boolean` type).