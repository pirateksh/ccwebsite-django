[TOC]

ForgeJS allows you to display different kind of media types and formats on the background of your scenes. Here is a little recap about the different kind of media declaration you can add in your json configuration at the time.

## Image

An image media have different formats. By format we mean that pixels are not organize the same way from a format to another for a same image ressource! ForgeJS handles two format at the moment which are **equirectangular** and **cubemap** images.

### Image equi

Here is what looks like an equirectangular image ressource:

![](https://cdn.forgejs.org/grav/images/tutorials/forest-equi.jpg)

The wikipedia definition of [equirectangular projection](https://en.wikipedia.org/wiki/Equirectangular_projection){.blank}.

```js
{
    "story":
    {
        "uid": "media-story",

        "scenes":
        [
            {
                "uid": "scene-image-equi",

                "media":
                {
                    "uid": "media-image-equi",
                    "type": "image",

                    "source":
                    {
                        "format": "equi",
                        "url": "forest-equi.jpg"
                    }
                }
            }
        ]
    }
}
```

- `uid` - The unique identifier of the media.
- `type` - The type of the media (image).
- `source.format` - The format of the source (equi).
- `source.url` - The url of the equi image.


### Image cubemap format

Here is what looks like a cubemap image ressource:

![](https://cdn.forgejs.org/grav/images/tutorials/forest-cubemap.jpg)

The wikipedia definition of [cube mapping](https://en.wikipedia.org/wiki/Cube_mapping){.blank}

```js
{
    "story":
    {
        "uid": "media-story",

        "scenes":
        [
            {
                "uid": "scene-image-cubemap",

                "media":
                {
                    "uid": "media-image-cubemap",
                    "type": "image",

                    "source":
                    {
                        "format": "cube",
                        "order": "RLUDFB",
                        "tile": 512,
                        "url": "forest-cubemap.jpg"
                    }
                }
            }
        ]
    }
}
```

- `uid` - The unique identifier of the media.
- `type` - The type of the media (image).
- `source.format` - The format of the source (cube).
- `source.order` - The order of the tiles from top left to bottom right.
- `source.tile` - The size of each tiles. All tiles must be squared so only one size is needed.
- `source.url` - The url of the equi image.

##### Order

Tiles are ordered from top left corner to bottom right corner of the ressource. We have six tiles in one image ressource. The `source.order` propoerty of the media json configuration explains how the tiles are ordered in the image ressource. In our case the order is **RLUDFB**, here is a little glossary to know what these letters means:

- `R` - The right tile.
- `L` - The left tile.
- `U` - The up tile.
- `D` - The down tile.
- `F` - The front tile.
- `B` - The back tile.

## Video

A video media can have different formats. By format we mean that pixels are not organize the same way from a format to another for a same video ressource! ForgeJS handles two format at the moment which are **equirectangular** and **cubemap** videos. We can also have diffrent video qualities for a same video.

### Video equi

Here is what looks like an equirectangular video ressource:

<video width="740" controls>
    <source src="https://cdn.forgejs.org/samples/common/videos/omni-highlights/source.02-720p_HD.mp4" type="video/mp4">
</video>

#### Mono quality

```js
{
    "story":
    {
        "uid": "media-story",

        "scenes":
        [
            {
                "uid": "scene-video-equi-mono-quality",

                "media":
                {
                    "uid": "media-video-equi-mono-quality",
                    "type": "video",

                    "source":
                    {
                        "format": "equi",
                        "url": "video-equi.mp4"
                    },

                    "options":
                    {
                        "autoPlay": true,
                        "loop": true,
                        "volume": 1
                    }
                }
            }
        ]
    }
}
```

- `uid` - The unique identifier of the media.
- `type` - The type of the media (video).
- `source.format` - The format of the source (equi).
- `source.url` - The url of the equi video.
- `options.autoPlay` - Does the video auto play at start? (Does not work on mobile)
- `options.loop` - Does the video loops?
- `options.volume` - The video volume you want to set.

#### Multi quality

ForgeJS have two ways to handle multi quality:

- The first one is to use several video files that represents differents quality of the same video. ForgeJS will try to play the best quality according to the user bandwidth.
- The second one is to use a [mpeg-dash](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP){.blank} video.

##### Multiple video files


```js
{
    "story":
    {
        "uid": "media-story",

        "scenes":
        [
            {
                "uid": "scene-video-equi-multi-quality",

                "media":
                {
                    "uid": "media-video-equi-multi-quality",
                    "type": "video",

                    "source":
                    {
                        "format": "equi",
                        "levels":
                        [
                            {"url": "video-equi-quality-0.mp4"},
                            {"url": "video-equi-quality-1.mp4"},
                            {"url": "video-equi-quality-2.mp4"},
                            {"url": "video-equi-quality-3.mp4"}
                        ]
                    }

                    "options":
                    {
                        "autoPlay": true,
                        "loop": true,
                        "volume": 1
                    }
                }
            }
        ]
    }
}
```

- `uid` - The unique identifier of the media.
- `type` - The type of the media (video).
- `source.format` - The format of the source (equi).
- `source.levels` - An array of objects containing the urls of the different levels of quality.
- `options.autoPlay` - Does the video auto play at start? (Does not work on mobile)
- `options.loop` - Does the video loops?
- `options.volume` - The video volume you want to set.

##### MPEG-DASH video

```js
{
    "story":
    {
        "uid": "media-story",

        "scenes":
        [
            {
                "uid": "scene-video-equi-mpeg-dash",

                "media":
                {
                    "uid": "media-video-equi-mpeg-dash",
                    "type": "video",

                    "source":
                    {
                        "format": "equi",
                        "streaming": "dash",
                        "url": "video-dash.mpd"
                    },

                    "options":
                    {
                        "autoPlay": true,
                        "loop": true,
                        "volume": 1
                    }
                }
            }
        ]
    }
}
```

- `uid` - The unique identifier of the media.
- `type` - The type of the media (video).
- `source.format` - The format of the source (equi).
- `source.streaming` - The streaming technique used for this video (dash).
- `source.url` - The url of the mpeag-dash media presentation description (MPD) file.
- `options.autoPlay` - Does the video auto play at start? (Does not work on mobile)
- `options.loop` - Does the video loops?
- `options.volume` - The video volume you want to set.

### Video cubemap

Here is what looks like a cubemap video ressource:

<video width="740" controls>
    <source src="https://cdn.forgejs.org/samples/common/videos/cubemap/omni_highlights.mp4" type="video/mp4">
</video>

#### Mono quality

```js
{
    "story":
    {
        "uid": "media-story",

        "scenes":
        [
            {
                "uid": "scene-video-cubemap-mono-quality",

                "media":
                {
                    "uid": "media-video-cubemap-mono-quality",
                    "type": "video",

                    "source":
                    {
                        "format": "cube",
                        "order": "RLUDFB",
                        "tile": 960,
                        "url": "video-cubemap.mp4"
                    }
                }
            }
        ]
    }
}
```

- `uid` - The unique identifier of the media.
- `type` - The type of the media (video).
- `source.format` - The format of the source (equi).
- `source.url` - The url of the equi video.
- `options.autoPlay` - Does the video auto play at start? (Does not work on mobile)
- `options.loop` - Does the video loops?
- `options.volume` - The video volume you want to set.

#### Multi quality

You can use the same muli quality features and syntax for a cubemap video as for the equi video.