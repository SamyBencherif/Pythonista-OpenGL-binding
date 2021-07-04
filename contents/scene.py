# A bit modified scene.py from Pythonista's std lib

import _scene
import math, numbers
from _scene_types import *

# to prevent default unused import from failing:
Action = None

from collections.abc import Iterable

from _scene import stroke_weight, no_stroke, no_fill, no_tint, load_image, image
from _scene import background, rect, ellipse, fill, stroke, tint, get_image_path
from _scene import load_image_file, line, unload_image, image_quad, text
from _scene import triangle_strip
#size = _scene.size
#push_matrix = _scene.push_matrix
#pop_matrix = _scene.pop_matrix
#rotate = _scene.rotate
#translate = _scene.translate
#scale = _scene.scale
#blend_mode = _scene.blend_mode
#get_screen_scale = _scene.get_screen_scale

DEFAULT_ORIENTATION = 0
PORTRAIT = 1
LANDSCAPE = 2

BLEND_NORMAL = 0
BLEND_ADD = 1
BLEND_MULTIPLY = 2

# fragment shader
class Shader:
    def __init__(self, source):
        self.program = _scene.createVFShaderProgram(source)

    def get_uniform(self, name):
        
        raise Exception("Not Yet Implemented")

    def set_uniform(self, name, value):

        uniform = _scene.uniformFromName(self.program, name)

        # texture/sampler2D
        if type(value) == _scene.pyglet.image.ImageData:
            texture = value.get_texture()
            _scene.glUniform1i(uniform, texture.id)

        # float
        if type(value) in (float, int):
            _scene.glUniform1f(uniform, value)

        # 2/3/4 component vector
        if isinstance(value,Iterable):
            if len(value) == 3:
                _scene.glUniform3f(uniform, *value)
            if len(value) == 2:
                _scene.glUniform2f(uniform, *value)


def use_shader(shaderProgram):
    if shaderProgram == None:
        _scene.glUseProgram(0)
    else:
        _scene.glUseProgram(shaderProgram.program)

def load_pil_image(image):
    mode = image.mode
    if mode != 'RGBA':
        raise ValueError('Only RGBA images are supported')
    w, h = image.size
    return _scene.load_raw_image_data(image.tostring(), mode, w, h)

def run(scene_to_run, orientation=0, frame_interval=1, anti_alias=False, show_fps=False):
    """Run a scene (an object that inherits from Scene) in a fullscreen view.
    Running a scene first calls its setup() method (if defined),
    afterwards, the draw() method is repeatedly called (at 60 fps)."""
    if not isinstance(scene_to_run, Scene):
        raise TypeError('No valid Scene object')
    _scene.run(scene_to_run, orientation, frame_interval, anti_alias)

def gravity():
    """Return the current gravity as a Vector3 object that can be used to
    determine the device's orientation"""
    g = _scene.gravity()
    return Vector3(*g)

def render_text(txt, font_name='Helvetica', font_size=16.0):
    image_name, w, h = _scene.render_text(txt, font_name, font_size)
    return image_name, Size(w, h)

def curve_sinodial(x):
    y = 0.5 * math.sin(math.pi * x - 0.5 * math.pi) + 0.5
    return y
def curve_linear(x):
    return x
def curve_ease_in(x):
    return x ** 3
def curve_ease_out(x):
    return (x-1)**3 + 1
def curve_ease_in_out(x):
    if x / 0.5 < 1.0:
        x /= 0.5
        return 0.5 * (x ** 3)
    x /= 0.5
    x -= 2
    return 0.5 * (x ** 3 + 2)
def curve_elastic_out(x):
    c = d = 1.0
    b = 0.0
    t = x
    s = 1.70158
    p = 0
    a = c
    if not t: return b
    if ((t / d) == 1): return b + c
    if p == 0: p = d * 0.3
    if a < abs(c):
        a = c
        s = p / 4.0
    else:
        s = p / (2 * math.pi) * math.asin(c / a)
    return a * 2 ** (-10*t) * math.sin((t * d - s) * (2 * math.pi)/p) + c + b
def curve_elastic_in(x):
    c = d = 1.0
    b = 0.0
    t = x
    s = 1.70158
    p = 0
    a = c
    if not t: return b
    if ((t / d) == 1): return b + c
    if p == 0: p = d * 0.3
    if a < abs(c):
        a = c
        s = p / 4.0
    else:
        s = p / (2 * math.pi) * math.asin(c / a)
    t -= 1
    return -(a*math.pow(2,10*(t)) * math.sin( (t*d-s)*(2*math.pi)/p )) + b
def curve_elastic_in_out(x):
    c = d = 1.0
    b = 0.0
    t = x
    s = 1.70158
    p = 0
    a = c
    if not t: return b
    t /= d/2
    if t == 2: return b + c
    if p == 0: p = d * (0.3 * 1.5)
    if a < abs(c):
        a = c
        s = p / 4.0
    else:
        s = p / (2 * math.pi) * math.asin(c / a)
    if t < 1:
        t -= 1
        return -0.5 * (a * math.pow(2, 10 * (t)) * math.sin((t * d - s) * (2 * math.pi) / p)) + b
    t -=1
    return a * math.pow(2, -10 * t) * math.sin((t * d - s) * (2 * math.pi) / p) * 0.5 + c + b
def curve_bounce_out(x):
    c = d = 1.0
    b = 0.0
    t = x
    if (t / d) < (1.0 / 2.75):
        return c * (7.5625*t*t) + b
    elif t < (2.0/2.75):
        t -= (1.5/2.75)
        return c * (7.5625 * t * t + 0.75) + b
    elif t < (2.5 / 2.75):
        t -= (2.25/2.75)
        return c * (7.5625 * t * t + 0.9375) + b
    else:
        t -= (2.625/2.75)
        return c * (7.5625 * t * t + 0.984375) + b
def curve_bounce_in(x):
    return 1.0 - curve_bounce_out(1.0 - x)
def curve_bounce_in_out(x):
    t = x
    d = 1.0
    if t < (d / 2.0):
        return curve_ease_in_bounce(x * 2) * 0.5
    return curve_ease_out_bounce(x * 2 - d) * 0.5 + 0.5

def curve_ease_back_in(x):
    s = 1.70158
    return x * x * ((s+1) * x - s)
def curve_ease_back_out(x):
    s = 1.70158
    t = x - 1
    return (t * t * ((s+1) * t + s) + 1)
def curve_ease_back_in_out(x):
    s = 1.70158
    t = x
    b = 0.0
    c = d = 1.0
    t /= d/2
    if (t < 1):
        s *= 1.525
        return c/2 * (t*t*((s+1)*t - s)) + b;
    t -= 2
    s *= 1.525
    return c/2 * (t*t*((s+1)*t + s) + 2) + b;

class Animation (object):
    """An Animation object can be attached to a Layer to alter some of its
    attributes smoothly. Animations can trigger a completion function when
    they are finished.
    Instead of creating an animation directly and setting
    all its attributes, it is often more convenient to use the animate()
    method of the Layer class."""
    def __init__(self):
        self.t = self.delay = 0.0
        self.repeat = 1
        self._repetitions = 0
        self.autoreverse = False
        self.value = self.from_value = self.to_value = None
        self.duration = 0.5
        self.curve = curve_sinodial
        self.finished = False
        self.attribute = self.completion = self.layer = None

    def update(self, dt):
        """Update the progress of an animation with a given time delta.
        This will automatically be called in each frame for animations
        that are attached to a Layer."""
        self.t += dt
        progress = 0.0
        if self.t < self.delay:
            self.value = self.from_value
            return
        else:
            progress = 1.0 if self.duration <= 0 else min(1.0, (self.t - self.delay) / self.duration)

        self.value = self.interpolate(progress)
        if self.attribute and isinstance(self.layer, Layer):
            setattr(self.layer, self.attribute, self.value)
        if progress >= 1.0 and not self.finished:
            self._repetitions += 1
            self.delay = 0.0
            if ((not self.autoreverse and self._repetitions >= self.repeat) or
                (self.autoreverse and self._repetitions >= self.repeat * 2)):
                self.finished = True
                if isinstance(self.layer, Layer):
                    self.layer.remove_animation(self)
                if callable(self.completion):
                    self.completion()
            else:
                self.t = 0.0
                if self.autoreverse:
                    self.to_value, self.from_value = self.from_value, self.to_value
                else:
                    self.value = self.from_value

    def interpolate(self, progress):
        p = self.curve(progress)
        from_v = self.from_value
        to_v = self.to_value
        if isinstance(from_v, numbers.Number) and isinstance(to_v, numbers.Number):
            return from_v + (to_v - from_v) * p
        elif isinstance(self.from_value, Rect) and isinstance(self.to_value, Rect):
            from_x = from_v.x
            from_y = from_v.y
            to_x = to_v.x
            to_y = to_v.y
            from_w = from_v.w
            from_h = from_v.h
            to_w = to_v.w
            to_h = to_v.h
            value = Rect(from_x + (to_x - from_x) * p, from_y + (to_y - from_y) * p, from_w + (to_w - from_w) * p, from_h + (to_h - from_h) * p)
            return value
        elif isinstance(self.from_value, Color) and isinstance(self.to_value, Color):
            value = Color()
            value.r = self.from_value.r + (self.to_value.r - self.from_value.r) * p
            value.g = self.from_value.g + (self.to_value.g - self.from_value.g) * p
            value.b = self.from_value.b + (self.to_value.b - self.from_value.b) * p
            value.a = self.from_value.a + (self.to_value.a - self.from_value.a) * p
            return value
        return 0.0

class Layer (object):
    """Represents a rectangular area that can be filled with a color and
    draw an image. The primary purpose of layers is to make basic animations
    very easy. The frame, scale_x, scale_y, rotation, tint, and
    background attributes of a layer can be animated, so that the values change
    smoothly over time. You can either create an Animation object and attach
    it to a layer with the add_animation() method, or you can use the layer's
    animate() method, which implicitly creates and attaches an animation.
    Animations can optionally call a completion function when they finish."""

    def __init__(self, rect=Rect()):
        self.frame = rect
        self.sublayers = []
        self.animations = {}
        self.scale_x = self.scale_y = self.alpha = 1.0
        self.rotation = 0.0
        self.image = self.superlayer = None
        self.background = self.stroke = Color(0, 0, 0, 0)
        self.stroke_weight = 0.0
        self.tint = Color(1, 1, 1, 1)
        self.ignores_touches = False

    def _hit_test(self, location):
        if self.ignores_touches or self.alpha <= 0:
            return None
        hit_layer = self if location in self.frame else None
        hit_sublayer = None
        for layer in self.sublayers:
            location_in_sublayer = Point(location.x - self.frame.x, location.y - self.frame.y)
            hit = layer._hit_test(location_in_sublayer)
            if hit: hit_sublayer = hit
        return hit_sublayer if hit_sublayer else hit_layer

    def convert_to_screen(self, location):
        tx, ty, _, _ = self.frame
        l = self
        ancestor = l.superlayer
        while ancestor:
            tx += ancestor.frame.x
            ty += ancestor.frame.y
            ancestor = ancestor.superlayer
        return Point(location.x + tx, location.y + ty)

    def convert_from_screen(self, location):
        tx, ty, _, _ = self.frame
        l = self
        ancestor = l.superlayer
        while ancestor:
            tx += ancestor.frame.x
            ty += ancestor.frame.y
            ancestor = ancestor.superlayer
        return Point(location.x - tx, location.y - ty)

    def update(self, dt):
        if self.animations:
            for animation_key in self.animations.keys():
                #Note: It's possible that animations remove each other while updating
                if self.animations.has_key(animation_key):
                    animation = self.animations[animation_key]
                    animation.update(dt)
        for s in self.sublayers:
            s.update(dt)

    def add_animation(self, animation, key):
        """Add an Animation to the layer that changes the value of key over time.
        key can be one of frame, scale_x, scale_y, rotation, background, tint, alpha."""
        if animation.from_value == animation.to_value:
            return
        animation.attribute = key
        animation.layer = self
        self.animations[key] = animation

    def remove_animation(self, animation):
        """Remove a given animation from the layer."""
        del self.animations[animation.attribute]

    def remove_all_animations(self):
        """Remove all animations from a layer."""
        self.animations = {}

    def add_layer(self, layer):
        """Add a layer as a sublayer of this layer.
        A sublayers frame is defined relative to its superlayer's frame.
        The alpha value of sublayers is blended with that of their superlayer."""
        if not isinstance(layer, Layer):
            raise TypeError('Invalid layer object')
        if layer != self:
            self.sublayers.append(layer)
            layer.superlayer = self

    def remove_layer(self, layer=None):
        """Remove a layer from this layer's sublayers.
        If layer is None, this layer is removed from its superlayer."""
        if layer:
            try:
                self.sublayers.remove(layer)
            except ValueError:
                pass
        elif self.superlayer:
            self.superlayer.remove_layer(self)

    def draw(self, a=1.0):
        a *= self.alpha
        if a <= 0: return

        push_matrix()
        x, y, w, h = self.frame
        s_x = self.scale_x
        s_y = self.scale_y
        rot = self.rotation

        translate(x + w/2, y + h/2)
        if s_x != 1 or s_y != 1:
            scale(s_x, s_y)
            pass  # what does this "pass" do?!?
        if rot != 0:
            rotate(rot)
            pass  # what does this "pass" do?!?

        """
        ^ The "pass"es above do not do anything. They are safe to remove.

        The reason they are there is likely they were being used as placeholders
        and someone forgot to delete them. (You can't have empty if statements in 
        Python).

        I am not deleting them, because I wanted to answer the question. If anyone
        sees this please delete it all.
        """

        translate(-w * 0.5, -h * 0.5)

        bg_r, bg_g, bg_b, bg_a = self.background
        strk_r, strk_g, strk_b, strk_a = self.stroke
        strk.a *= a
        fill(bg_r, bg_g, bg_b, bg_a * a)
        stroke(strk_r, strk_g, strk_b, strk_a)
        stroke_weight(self.stroke_weight)
        rect(0, 0, w, h)

        if self.image:
            tint_color = self.tint
            if tint_color:
                tint(tint_color.r, tint_color.g, tint_color.b, a)
            else:
                tint(1, 1, 1, a)
            image(self.image, 0, 0, w, h)

        for s in self.sublayers:
            s.draw(a)
        pop_matrix()

    def animate(self, attribute, to_value, duration=0.5, delay=0.0, curve=curve_sinodial,
                repeat=1, autoreverse=False, completion=None):
        """Animate an attribute of the layer smoothly to a new value.
        This implicitly creates an Animation object and attaches it to the layer.
        key can be one of frame, scale_x, scale_y, rotation, background, tint, alpha.
        to_value must have the proper type for the attribute (Rect for frame;
        float for scale_x, scale_y, rotation, alpha; Color for background, tint)."""
        animation = Animation()
        animation.from_value = getattr(self, attribute)
        animation.to_value = to_value
        animation.duration = duration
        animation.delay = delay
        animation.curve = curve
        animation.completion = completion
        animation.autoreverse = autoreverse
        animation.repeat = repeat
        self.add_animation(animation, attribute)

class TextLayer (Layer):
    def __init__(self, text, font, font_size):
        Layer.__init__(self)
        img, size = render_text(text, font, font_size)
        self.image = img
        self.frame = Rect(0, 0, size.w, size.h)

class Button (Layer):
    def __init__(self, frame, title=None):
        Layer.__init__(self, frame)
        self.background = Color(0.9, 0.9, 0.9)
        self.stroke_weight = 2
        self.stroke = Color(0.5, 0.5, 0.5)
        self.action = None
        if title:
            t = TextLayer(title, 'Helvetica-Bold', min(30, max(10, int(frame.h * 0.8))))
            t.ignores_touches = True
            t.tint = Color(0, 0, 0)
            t.frame.center(frame.center())
            t.frame.x = int(t.frame.x)
            t.frame.y = int(t.frame.y)
            self.add_layer(t)

    def touch_began(self, touch):
        self.background = Color(0.7, 0.7, 0.7)

    def touch_moved(self, touch):
        if self.superlayer.convert_from_screen(touch.location) in self.frame:
            self.background = Color(0.7, 0.7, 0.7)
        else:
            self.background = Color(0.9, 0.9, 0.9)

    def touch_ended(self, touch):
        self.background = Color(0.9, 0.9, 0.9)
        if self.superlayer.convert_from_screen(touch.location) in self.frame and callable(self.action):
            self.action()

class Scene (object):
    def setup(self):
        """You can override this method to set up your scene before the first
        frame is drawn. The size attribute of the scene will already be set to
        the screen size."""
        pass

    def _setup_scene(self, width, height):
        self.touches = dict()
        self.root_layer = None
        self.dt = self.t = 0.0
        self.delayed_invocations = []
        self._set_size(width, height)
        self.setup()

    def _set_size(self, width, height):
        self.size = Size(width, height)
        self.bounds = Rect(0, 0, width, height)
        self.did_change_size()

    def did_change_size(self):
        """
        Notifies user of window size change (or screen-rotation on mobile)
        """

    def should_rotate(self, orientation):
        return False

    def add_layer(self, layer):
        """Adds a layer to the root layer of the scene. The root layer is implicitly
        created when you call this for the first time."""
        if not self.root_layer:
            s = _scene._data.DEFSIZE
            self.root_layer = Layer(Rect(0, 0, *s))
        self.root_layer.add_layer(layer)

    def delay(self, dt, func):
        invocation = { 't': self.t + dt, 'f': func }
        self.delayed_invocations.append(invocation)

    def _draw(self, dt):
        self.dt = dt
        self.t += dt
        fired_invocations = []
        for invocation in self.delayed_invocations:
            if invocation['t'] <= self.t:
                invocation['f']()
                fired_invocations.append(invocation)
        for invocation in fired_invocations:
            self.delayed_invocations.remove(invocation)
        self.draw()
        self.update()

    def draw(self):
        """This method is called once for every frame (typically 60 times
        per second). It defines how the scene is rendered. The dt (time delta
        since last frame) attribute of the scene will be automatically updated
        before the draw method is called."""
        pass

    def update(self):
        """Called after draw"""
        pass

    def _stop(self):
        self.stop()

    def stop(self):
        """This method is called automatically when the scene is stopped.
        The default implementation does nothing."""
        pass

    def pause(self):
        """This method is called automatically when the app is paused (e.g. the home
        button is pressed). The default implementation does nothing."""
        pass

    def resume(self):
        """This method is automatically called when the app resumes from paused state
        (e.g. after reactivating from the home screen). The default implementation does
        nothing."""
        pass

    def _touch_began(self, x, y, touch_id):
        touch = Touch(x, y, x, y, touch_id)

        if self.root_layer:
            hit_layer = self.root_layer._hit_test(Point(x, y))
            touch.layer = hit_layer
            if hit_layer:
                if hasattr(hit_layer, 'touch_began') and callable(hit_layer.touch_began):
                    hit_layer.touch_began(touch)
        self.touches[touch_id] = touch
        self.touch_began(touch)

    def _touch_moved(self, x, y, prev_x, prev_y, touch_id):
        touch = Touch(x, y, prev_x, prev_y, touch_id)
        old_touch = self.touches.get(touch_id, None)
        if old_touch:
            touch.layer = old_touch.layer
            if touch.layer:
                if hasattr(touch.layer, 'touch_moved') and callable(touch.layer.touch_moved):
                    touch.layer.touch_moved(touch)
        self.touches[touch_id] = touch
        self.touch_moved(touch)

    def _touch_ended(self, x, y, touch_id):
        touch = Touch(x, y, x, y, touch_id)
        old_touch = self.touches.get(touch_id, None)
        if touch_id in self.touches.keys(): del self.touches[touch_id]
        if old_touch:
            touch.layer = old_touch.layer
            if touch.layer:
                if hasattr(touch.layer, 'touch_ended') and callable(touch.layer.touch_ended):
                    touch.layer.touch_ended(touch)
        self.touch_ended(touch)

    def touch_began(self, touch):
        """Override this method to be notified when a touch begins.
        For multi-touch events, this is called once for each touch."""
        pass

    def touch_moved(self, touch):
        """Override this method to be notified when a touch moves.
        For multi-touch events, this is called once for each touch."""
        pass

    def touch_ended(self, touch):
        """Override this method to be notified when a touch ends.
        For multi-touch events, this is called once for each touch."""
        pass
