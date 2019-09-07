[TOC]

If you followed the previous tutorial on how to embed a ForgeJS viewer in your web page, you ended up with a viewer that just displays a black background because it has no configuration at all. So, now you'll want to add content. ForgeJS is meant to display 360° media. We will see how to configure the ForgeJS viewer to make the following project:

<iframe src="http://kenprivatebeta.kolor.com/releases/latest/samples/projects/simple-project/"></iframe>

Two steps to achieve this:
1. Create a json configuration file.
2. Give the configuration to the ForgeJS viewer.

## The json configuration

To customize the experience through a configuration, we will create a file that we named `config.json`. Many things can be declared in this configuration, but for the first one we will just add a scene with a 360° media to the project.

```js
{
    "story":
    {
        "scenes":
        [
            {
                "uid": "scene-0",
                "name": "My first scene",
                "slug": "my-first-scene",
                "description": "This is my first scene",

                "media":
                {
                    "uid": "media-0",
                    "type": "image",

                    "source":
                    {
                        "format": "equi",
                        "url": "path/to/equirectangular.jpg"
                    }
                }
            }
        ]
    }
}
```

The configuration has a `story` object that contains an array called `scenes` with `scene` objects inside.

### The scene object

- `uid` - The unique identifier of the scene.
- `name` - The name of the scene.
- `slug` - The name of the scene that will be displayed in the url.
- `description` - The description of the scene.
- `media` - The media object that will be displayed on the scene.

### The media object

The media object describes the 360° media that will be displayed on the scene background.

- `uid` - The unique identifier of the media.
- `type` - The type of media used by the scene.
- `source` - The source object that describes the file to load by the scene media.

### The media source

The media source is the file description that will be loaded by the media.

- `format` - The format of the file. In this tutorial we use an equirectangular image, so the type is "equi".
- `url` - The url of the file to load.

## Loading the configuration

To load the project configuration, you have to give the url of the json configuration file to the `FORGE.Viewer` constructor as the second argument.
Now the javascript viewer creation will looks like this:

```js
var viewer = new FORGE.Viewer("container", "config.json");
```