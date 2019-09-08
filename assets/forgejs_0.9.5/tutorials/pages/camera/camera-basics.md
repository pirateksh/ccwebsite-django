[TOC]

ForgeJS is built on top of three.js 3D engine, that means that all object are in a 3D scene and at the center of the scene you have the camera that is the user point of view. You can customize the camera object in the json configuration of your project.

## Global configuration

At the root of your json configuration you can define a global `camera` object that will set the camera options for every scenes of your story.

Here is a basic configuration of the camera:

```js
{
    "story": { ... },

    "camera":
    {
        "parallax": 0,
        "yaw": { "default" : 0, "min": -100, "max": 100 },
        "pitch": { "default" : 0, "min": -90, "max": 180 },
        "roll": { "default" : 0, "min": 0, "max": 0 },
        "fov": { "default" : 90, "min": 70, "max": 110 }
    }
}
```

- `parallax` - The parallax factor of the camera. 0 means no parallax.
- `yaw` - The yaw configuration of the camera.
- `pitch` - The pitch configuration of the camera.
- `roll` - The roll configuration of the camera.
- `fov` - The field of view configuration of the camera.

The `yaw`, `pitch`, `roll` and `fov` options are objects that defines the default value, the minimum and maximum values.
The default values will be used as default for the camera rotation and field of view for each scene load complete.
By specifying these `min` and `max` option, you can limit the camera movement to a part of your scene and limit the field of view (fov).

## Scene configuration

If you want to give a different configuration on your scenes than the global one, you can add a `camera` object to your `scene` object to override the global camera configuration like this:

```js
{
    "story":
    {
        "scenes":
        [
            {
                "uid": "scene-0",

                "media": { ... },

                "camera":
                {
                    "parallax": 0,
                    "yaw": { "default" : 20, "min": -100, "max": 100 },
                    "pitch": { "default" : 10, "min": -90, "max": 180 },
                    "roll": { "default" : 0, "min": 0, "max": 0 },
                    "fov": { "default" : 90, "min": 70, "max": 110 }
                }
            }
        ]
    }
}
```

