[TOC]

Hotspots don't have to stay static, they can also move! A hotspot can have animations, that can be played at any time. The hotspot can play a list of `tracks` that define animation keyframes.

<iframe src="http://kenprivatebeta.kolor.com/releases/latest/samples/projects/hotspots-animation/"></iframe>

## Hotspot animation definition

In the **hotspot** property, we find an `animation` object, which consists of a list of flags and a list of tracks to play. The tracks are played in the order they are written in this array.

```js
"hotspots":
[
    {
        "uid": "hotspot-0",
        "material":
        {
            "image": "hotspot-0.jpg"
        },
        "animation":
        {
            "enabled": true,
            "loop": false,
            "random": false,
            "autoPlay": true,
            "tracks": [ "hotspot-0-track-0", "hotspot-0-track-1" ]
        }
    }
]
```

- `enabled` - Is the animation enabled?
- `loop` - Does the animation loop?
- `random` - Are the tracks played randomly?
- `autoPlay` - Does the animation auto play?
- `tracks` - The [list of tracks](#tracks) to play.

### Hotspot tracks definition

Tracks are a list of keyframes that describe the animation of a hotspot.
These tracks are defined at the root of your configuration JSON file in a global `hotspots` object. So it's possible to share tracks between different hotspots.

```js
"hotspots":
{
    "tracks":
    [
        {
            "uid": "hotspot-track-0",
            "name": "Track name",
            "description": "Track description",

            "keyframes":
            [
                {
                    "time": 2000,
                    "data":
                    {
                        "position": { "radius": 100, "theta": 0, "phi": 0 },
                        "rotation": { "x": 0, "y": 0, "z": 0 }
                    }
                },
                {
                    "time": 5000,
                    "data":
                    {
                        "position": { "radius": 200, "theta": 45, "phi": 20 },
                        "rotation": { "x": 40, "y": 180, "z": 180 }
                    }
                },
                {
                    "time": 8000,
                    "data":
                    {
                        "position": { "radius": 400, "theta": -20, "phi": 10 },
                        "rotation": { "x": -40, "y": -180, "z": -180 },
                        "scale": { "x": 1, "y": 1, "z": 1 }
                    }
                },
                {
                    "time": 12000,
                    "data":
                    {
                        "position": { "radius": 200, "theta": 0, "phi": 0 },
                        "rotation": { "x": 0, "y": 0, "z": 0 },
                        "scale": { "x": 2, "y": 2, "z": 2 }
                    }
                }
            ]
        }
    ]
}
```

### Track properties

- `uid` - The unique identifier of the track.
- `name` - The name of the track.
- `description` - The description of the track.
- `keyframes` - The keyframes used by the track for the animation.

### Keyframe properties

A keyframe is a `data` object associated to a `time`.

- `time` - Time of the keyframe (in milliseconds).
- `data.position` - The position where the hotspot will be at this given time.
- `data.rotation` - The rotation where the hotspot will be at this given time.
- `data.scale` - The scale where the hotspot will be at this given time.

Note that even if the transformation points are not in the correct order, the determining order will be the time of each point.
