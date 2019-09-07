[TOC]

The ForgeJS framework allows you to build immersive experiences for web pages. In this hello world tutorial we will just see how to embed a ForgeJS viewer into your web page.

## Embedding into HTML

The following code shows how to create a ForgeJS viewer in full page.

```html
<!doctype html>
<html>
    <head>
        <title>ForgeJS tutorial</title>
        <meta charset="utf-8">
        <style>

            html, body {
                height: 100%;
                margin: 0;
                padding: 0;
            }

            #container {
                height: 100%;
            }

        </style>
    </head>
    <body>
        <div id="container"></div>

        <!-- Include the threejs custom build -->
        <script src="lib/three.custom.min.js"></script>

        <!-- Include the Hammer.js library -->
        <script src="lib/hammer.min.js"></script>

        <!-- Include the ForgeJS library -->
        <script src="lib/forge.min.js" ></script>

        <script>

            // Creation of the FORGE.Viewer
            var viewer = new FORGE.Viewer("container");

        </script>
    </body>
</html>
```

Basically all you have to do is to:

1. Create a container `<div></div>` html element where the viewer will be displayed and give it an `id` (in our example "container").

2. Load the ForgeJS framework and its dependencies by adding the `<script src=""></script>` html tags in your `<body></body>`.

3. In another `<script></script>`, create a variable and assign a `new FORGE.Viewer` to it and pass it the container id in first argument.

That's it! You've created your first ForgeJS viewer. For now it has no configuration at all, it just displays a black background. In the [next tutorial](/tutorials/basics/add-first-scene) we will see how to add a basic configuration to add a scene that displays 360° media.

!!! All the dependencies of ForgeJS that are a custom build of three.js, and hammer.js are included in our repository.


