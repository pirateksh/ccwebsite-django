[TOC]

A single panorama can be sufficient for creating an immersive experience, but you may want to build more complex and interactive experiences.
For that you'll need to place content all around the scene, to display information or to have a clickable zone to navigate from one scene to another.
This is what is commonly called hotspots. These are 3D objects in your scene. The following sample demonstrates what hotspots are:

<iframe src="http://kenprivatebeta.kolor.com/releases/latest/samples/projects/hotspots/"></iframe>

In this first hotspot tutorial, we will see how to add a hotspot to your scene, to position and rotate it.

## Creation of a simple hotspot

To create a hotspot we need to declare it on the JSON configuration of your project.
The `scene` objects of your configuration can have a `hotspots` property that is an array of `hotspot` objects.
Hotspots can be added inside a scene. Each scene gets a `hotspots` property containing an array of `hotspot` object.

Here is what the simplest hotspot declaration you can add to one of your scenes looks like:

```js
"hotspots":
[
    {
        "uid": "hotspot-0",
        "material":
        {
            "image": "images/scene-0-hotspot-0.jpg"
        }
    }
]
```

- `uid` - The unique identifier of the hotspot.
- `material` - The object containing information about what to display on the hotspot 3D object.

For a complete definition of a hotspot, see the [associated reference section](/releases/latest/doc/json/#hotspot).

## Position, rotation and scale of a hotspot

Once the hotspot has been added to the scene, we want to tweak its placement in the scene. The `transform` property is here specify a few things like the `position`, the `rotation` and the `scale`.

```js
"hotspots":
[
    {
        "uid": "hotspot-0",
        "material":
        {
            "image": "images/scene-0-hotspot-0.jpg"
        },

        "transform":
        {
            "position": { "radius": 200, "theta": 90, "phi": 30 },
            "rotation": { "x": 0, "y": 0, "z": 0 },
            "scale": { "x": 1, "y": 1, "z": 1 }
        }
    }
]
```

`transform.position` - Defines the spherical coordinate of your hotspot expressed in degrees.
`transform.rotation` - Defines the rotation of the hotspot from its local referential expressed in degrees.
`transform.scale` - Defines its scale in proportion to its original size. Default is 1.

### Position

A scene can be seen as the interior of a sphere, with the interior painted with a panorama. So the simplest way to place objects in it is to use [spherical coordinates](https://en.wikipedia.org/wiki/Spherical_coordinate_system), with the origin being the standing point of the user. The chosen set of coordinates are:

- `radius` - Value between **0** and **10000**
- `theta` - Value between **-180°** and **180°**
- `phi` - Value between **-90°** and **90°**

This position is used as a referential for all further computations of the position, such as in animations.

### Rotation

You can also rotate the hotspot on itself, in any direction. The method uses [Euler angles](https://en.wikipedia.org/wiki/Euler_angles). The rotation will be applied in reference to the current position or the initial position at initialization.

### Scale

The scale of a hotspot is a factor that will be applied to its original size. You can set scale for the three axis x, y and z. It is always a positive value.

## Geometry

The hotspot will use a plane as the default geometry. There will be other geometries in future releases, but for now, the main interest of the geometry object is to set the size of your plane geometry.

```js
"hotspots":
[
    {
        "uid": "hotspot-0",
        "material":
        {
            "image": "images/scene-0-hotspot-0.jpg"
        },

        "transform":
        {
            "position": { "radius": 200, "theta": 90, "phi": 30 },
            "rotation": { "x": 0, "y": 0, "z": 0 },
            "scale": { "x": 1, "y": 1, "z": 1 }
        }

        "geometry":
        {
            "type": "plane",
            "options":
            {
                "width": 150,
                "height": 200
            }
        }
    }
]
```

This way you can change the size of your geometry. The definitive rendered size of your geometry will be affected by the scale. If your plane is 150 width and your scale x is 2, your final size will be width 300.

## Facing camera

Most of the time you need your hotspot to be oriented towards the camera.

If you set the hotspot `transform.position.theta` to a value around 90°, you'll see the edge of the hotspot when you'll try to look at it like if you see it in profile.

As it can quickly be annoying to compute the right rotation, the `facingCamera` property is here to help you let your hotspot face the camera. You can still apply rotation, but the referential will the facing position with the first rotation applied.

```js
"hotspots":
[
    {
        "uid": "hotspot-0",
        "material":
        {
            "image": "images/scene-0-hotspot-0.jpg"
        },

        "facingCamera": true,

        "transform":
        {
            "position": { "radius": 200, "theta": 90, "phi": 30 }
        }
    }
]
```
