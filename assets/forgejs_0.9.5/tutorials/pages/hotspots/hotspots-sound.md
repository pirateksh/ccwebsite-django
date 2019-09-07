[TOC]

A hotspot can be a visual 3D object in the scene but it can also play a sound. The sound can be played at a constant volume or ajust its volume depending on the camera direction. In this case the volume will decrease in function of the distance between the location you're looking at and the hotspot. We call it the sound range. When you are off range the volume is set to the minimum.

<iframe src="http://kenprivatebeta.kolor.com/releases/latest/samples/projects/hotspots-sounds/"></iframe>

```js
"hotspots":
[
    {
        "uid": "hotspot-0",
        "material":
        {
            "image": "hotspot-0.jpg"
        },
        "sound":
        {
            "uid" : "sound-0",
            "source":
            {
                "url" : "sound-0.mp3"
            },
            "options":
            {
                "volume" : { "min": 0.2, "max": 0.6 },
                "loop" : true,
                "autoPlay": true,
                "startTime" : 0,
                "range" : 180
            }
        }
    }
]
```

- `uid` - The unique identifier of the sound.
- `source.url` - The url of the sound.
- `options.volume` - Can be an object with min and max volume or a number for the max volume (the min volume is **0** by default).
- `options.loop` - Does the sound loop?
- `options.autoPlay` - Does the sound auto play at start.
- `options.startTime` - The start time of the sound (in milliseconds).
- `options.range` - The range of the sound, if undefined the range will be at **360** so the volume will be the same wherever you look.
