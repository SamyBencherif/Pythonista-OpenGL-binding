Pythonista OpenGL Binding
==========================

This is a fork of the original program by [JadedTuna](https://github.com/JadedTuna/pcista).

## Background

[Pythonista](http://omz-software.com/pythonista/) is a lovely iphone app that allows you to edit and run python programs directly from the mobile device. It even comes with a selection of special modules for real time graphics and other things. Unfortunately these modules (such as the scene module) are not available on other devices, so I am expanding on JadedTunas work to make a "desktop version" of the Pythonista modules.

I created this fork because I wanted to work on my 3d library [LIB3D](https://github.com/SamyBencherif/LIB3D) on both mobile and desktop. Unfornately I found that the `image_quad` function I wanted to use is not supported in [pcista]((https://github.com/JadedTuna/pcista))--in fact it is impossible to (efficiently) implement in pygame, so I switched to pyglet which exposes OpenGL functionality.

## Installation

Simply generate and use a virtual environment using the provided script:

Run this command in your bash terminal:
```bash
source make_env.sh
```

Now the "python" command for that terminal will have access to supported Pythonista modules.
Try "import scene" to test it out.

## Differences

This version seeks to include some features from the newest version of Pythonista (v3.3)

* This version is compatible and intended for Python 3
* `image_quad` has partial support (no "from" coordinates, yet)
* `Shader` object has been included
    * `set_uniform` implemented to same extent as Pythonista
    * `get_uniform` not yet implemented.
    * `use_shader` works just like in app
* Some measures have been taking to prevent valid Pythonista scripts from crashing over an unused import (usually this means ensuring some module is there, even if it is empty).

Since this layer is written using OpenGL calls it is conceivable that this program could be ported to additional platforms without excess trouble: WebGL, Android, iOS App Store.

That being said there are currently some losses involved with this rewrite. 

* `render_text` is not yet rewritten
* `stroke_weight` has a visible maximum of 10px, like OpenGL, one obvious solution would be to construct a primitive for the border if it's over 10 pixels... but I haven't done that yet.
* `stroke` corners do not have endcaps

## Goal

My main focus is graphics, so I will start by porting the scene module, then sound, and maybe some ui.

---

Port of some Python iOS specific modules to PC.<br>
See **[SUPPORTED][]** for supported modules and **[SUPPORTED PROGRAMS][]** for supported programs.

[SUPPORTED]: https://github.com/Vik2015/pcista/blob/master/SUPPORTED.md
[SUPPORTED PROGRAMS]: https://github.com/Vik2015/pcista/blob/master/SUPPORTED_PROGRAMS.md
