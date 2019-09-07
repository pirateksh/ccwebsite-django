[TOC]

The director module allows you to get a guided navigation inside a 360° media, be it a video or an image. The director module can play defined tracks and move the camera automatically according to a track. Tracks are a list of keyframes that will tell the director module how to navigate in the 360° over time like in the following example.

<iframe src="http://kenprivatebeta.kolor.com/releases/latest/samples/projects/directors-cut/"></iframe>

## Configuration

Each scene of your project can have a director object. This director object contains different options and a set of tracks to use for the animation.

```js
{
    "story":
    {
        "scenes":
        [
            {
                "uid": "scene-0",

                "media": { ... },

                "director":
                {
                    "animation":
                    {
                        "enabled": true,

                        "random": false,
                        "loop": false,
                        "delay": 2000,

                        "stoppable": false,
                        "idleTime": 3000

                        "tracks": [ "director-track-0", "director-track-1" ]
                    }
                }
            }
        ]
    }
}
```

### The animation object

- `enabled` - Global switch for enabling the director on the scene.
- `random` - Determines if the tracks are played randomly or in the array order.
- `loop` - Determines if the list of tracks is looped.
- `delay` - The time to wait before the animation starts.
- `stoppable` - Is the user allowed to stop the director animation with their controller?
- `idleTime` - Time to wait before resuming the director animation after the user stopped it.
- `tracks` - This is an array of director tracks to play for the animation.

## Director tracks

Each scene can declare a director animation that will play director tracks identified by their unique identifier.
Director tracks are declared at the root of the json configuration file in a `director` object, with some options and a `tracks` property containing an array of tracks. Each `track` object is made of a few things identifying it, and a list of `keyframes`.

```js
{
    "story": { ... },

    "director":
    {
        "tracks":
        [
            {
                "uid": "director-track-0",
                "name": "The track name",
                "description": "Director's track description",
                "smooth": true,
                "cancelRoll": true,

                "easing":
                {
                    "default": "LINEAR",
                    "start": 2000
                },

                "keyframes": [ ... ]
            }
        ]
    }
}
```

- `uid` - The unique identifier of the track.
- `name` - The name of the track.
- `description` - The description of the track.
- `smooth` - Determines if the track is smoothed during the interpolation between each keyframe.
- `cancelRoll` - Cancels the roll of the camera as there can be one when interpolating, it will also cancel any specified roll in keyframes.
- `easing` - The easing object describes how the interpolation will be made between each keyframe.
- `keyframes` - The array of keyframes for the animation.

### The easing object

```js
"easing":
{
    "default": "LINEAR",
    "start": 2000
}
```

`default` - The default easing formula used for interpolations between keyframes. (The list of formula names are available below).
`start` - The time in milliseconds needed to reach the first keyframe position. If the time is zero the camera wiil jump directly to the first keyframe's position.

#### Available easing formulas

Easing are functions that change the way the camera will interpolate between keyframes. The available formulas are listed below.

- `LINEAR`
- `SINE_IN`
- `SINE_IN_OUT`
- `SINE_OUT`
- `QUAD_IN`
- `QUAD_IN_OUT`
- `QUAD_OUT`
- `CUBIC_IN`
- `CUBIC_IN_OUT`
- `CUBIC_OUT`
- `BOUNCE_OUT`
- `BOUNCE_IN`

### The keyframes

The `keyframes` object is an array of keyframes. A keyframe is a `data` object associated to a `time`. For the director's keyframes we need to associate a time with a camera rotation and a field of view.

```js
"keyframes":
[
    {
        "time": 0,
        "data": { "yaw": 100,  "pitch": 20, "fov": 90 }
    },
    {
        "time": 3000,
        "data": { "pitch": 30 }
    },
    {
        "time": 6000,
        "data": { "yaw": 20, "pitch": 10 }
    },
    {
        "time": 8000,
        "data": { "yaw": 20 }
    },
    {
        "time": 15000,
        "data": { "yaw": 60, "pitch": -20,  "fov": 120 }
    }
]
```

`time` - The time of the keyframe. The camera position will be reached at this time.
`data.yaw` - The yaw of the camera to reach at this time.
`data.pitch` - The pitch of the camera to reach at this time.
`data.roll` - The roll of the camera to reach at this time. Note that if you have `cancelRoll` to `true` in your track this value will be ignored.
`data.fov` - The field of view of the camera to reach at this time.

**What will happen to the camera with this example?**

#### yaw
- The yaw value will interpolate between 100 and 20 from time 0 to time 6000.
- The yaw value will remain at 20 between time 6000 and time 8000.
- The yaw value will interpolate between 20 and 60 from time 8000 to time 15000.

#### pitch
- The pitch value will interpolate between 20 and 30 from time 0 to time 3000.
- The pitch value will interpolate between 30 and 10 from time 3000 to time 6000.
- The pitch value will interpolate between 10 and -20 from time 6000 to time 15000.

#### roll
- The roll of the camera will not be interpolated, there are no roll values in those keyframes. In our case the `cancelRoll` is set to `true` so any roll values would be ignored.

#### fov
- The fov (field of view) value will interpolate between 90 and 120 from time 0 to time 15000 during the whole animation.

