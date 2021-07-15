# Some imports
import _scene_types
import pyglet
from pyglet.gl import *
import string
import time
import os
from math import cos, sin, pi

# https://gist.github.com/davidejones/0ba54a9402c5f374564e#file-pyglet_triangle-py-L2
from ctypes import create_string_buffer, cast, sizeof, c_int, c_char, pointer, byref, POINTER
# end

# No more evil global variables!
_data = _scene_types._Namespace()
_data.touch         = None
_data.stroke_weight = 0
_data.SIZE_IPHONE   = (320, 480)
_data.SIZE_IPHONE4  = (320, 480)
_data.SIZE_IPHONE5  = (320, 568)

_data.SIZE_IPAD3    = (748, 1024)
_data.DEFSIZE       = (320, 568)#_data.SIZE_IPAD3[::-1]
_data.letters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

_data.BG_COLOUR     = (0., 0., 0., 1.)
_data.STROKE_COLOUR = (1., 1., 1., 1.)
_data.FILL_COLOUR   = (1., 1., 1., 1.)
_data.TINT_COLOUR   = (1., 1., 1., 1.)

_data.LOADED_IMGS   = {}

"""
BEGIN DRAWING FUNCTIONS
"""

def hex2rgb(h):
    # color is in format #xxxxxx
    h = h[1:] # discard '#'
    r = h[:2] ; h = h[2:] # move first two chars to r
    g = h[:2] ; h = h[2:] # move first two chars to g
    b = h[:2]             # move first two chars to b
    r = int(r,16) ; g = int(g,16) ; b = int(b,16)
    return (r/255,g/255,b/255)

def compileShaderCode(shader, code):

    # hacky way to avoid use of OpenGL ES feature
    code = code.replace("precision", "//precision")

    shader_code_b = bytes(code, 'ascii')
    # https://gist.github.com/davidejones/0ba54a9402c5f374564e#file-pyglet_triangle-py-L2
    src_buffer = create_string_buffer(shader_code_b)
    buf_pointer = cast(pointer(pointer(src_buffer)), POINTER(POINTER(c_char)))
    length = c_int(len(shader_code_b) + 1)
    glShaderSource(shader, 1, buf_pointer, byref(length))
    # end 
    glCompileShader(shader)

# Using GL functions, create a vertex/fragment pair
# and return the compiled and linked shader program
# (the vertex shader is always a default one built
# to mimic the pythonista vertex shader)
def createVFShaderProgram(source):

    # create the CG program to return
    prog = glCreateProgram()

    # create the two shaders
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    frag_shader = glCreateShader(GL_FRAGMENT_SHADER)

    # compile vertex shader from inline source
    compileShaderCode(vertex_shader, '''
        #version 120
        varying vec2 v_tex_coord;
        void main(void) {
            v_tex_coord = gl_MultiTexCoord0.xy;
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }
    ''')

    # compile fragment shader from user-supplied source
    compileShaderCode(frag_shader, source)

    # link shaders to program
    glAttachShader(prog, vertex_shader)
    glAttachShader(prog, frag_shader)
    
    glLinkProgram(prog)

    return prog

def uniformFromName(prog, name):
    return glGetUniformLocation(prog, cast(pointer(create_string_buffer(bytes(name, 'ascii'))), POINTER(c_char)))


def stroke_weight(weight):
    _data.stroke_weight = weight

def no_stroke():
    _data.STROKE_COLOUR = None

def no_fill():
    _data.FILL_COLOUR = None

def no_tint():
    _data.TINT_COLOUR = None

def get_image_path(image_name):
    path = os.path.join(os.path.dirname(__file__), "Media", "Images", image_name.replace(":", os.sep) + "@2x.png")
    if os.path.isfile(path):
        return path
    return None

def load_image_file(path, name=None):
    if path in _data.LOADED_IMGS.keys():
        unload_image(path)
    img = pyglet.image.load(path)
    
    if name != None:
        iid = name
    else:
        iid = _data.new_image_id(_data.LOADED_IMGS.keys(), _data.letters)
    _data.LOADED_IMGS[iid] = img
    return iid

def load_image(name):
    path = get_image_path(name)
    if not path:
        raise IOError("built-in image: %s is not found" % name)
    load_image_file(path, name)

def image(name, x, y, w=0, h=0):
    if not name in _data.LOADED_IMGS.keys():
        load_image(name)
    _img = _data.LOADED_IMGS[name]

    glColor4f(*_data.TINT_COLOUR)

    texture = _img.get_texture()
    tex_coords = texture.tex_coords

    glEnable(texture.target)
    glBindTexture(texture.target, texture.id)

    glBegin(GL_QUADS)
    glTexCoord3f(tex_coords[0], tex_coords[1], tex_coords[2])
    glVertex2f(x, y)
    glTexCoord3f(tex_coords[3], tex_coords[4], tex_coords[5])
    glVertex2f(x+w, y)
    glTexCoord3f(tex_coords[6], tex_coords[7], tex_coords[8])
    glVertex2f(x+w, y+h)
    glTexCoord3f(tex_coords[9], tex_coords[10], tex_coords[11])
    glVertex2f(x, y+h)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

# this limited implementation of triangle_strip requires all parameters 
def triangle_strip(screen_coords, uvs, name):
    glColor4f(*_data.TINT_COLOUR)

    if not name in _data.LOADED_IMGS.keys():
        #print("loading image", name)
        load_image(name)

    _img = _data.LOADED_IMGS[name]

    texture = _img.get_texture()

    glEnable(texture.target)
    tex_coords = texture.tex_coords
    tex_coords[0] = uvs[0][0];
    tex_coords[1] = uvs[0][1];
    tex_coords[3] = uvs[1][0];
    tex_coords[4] = uvs[1][1];
    tex_coords[6] = uvs[2][0];
    tex_coords[7] = uvs[2][1];
    # everything except for Z values are overwritten

    glBindTexture(texture.target, texture.id)
    glBegin(GL_TRIANGLES)

    glTexCoord3f(tex_coords[0], tex_coords[1], tex_coords[2])
    glVertex2f(screen_coords[0], screen_coords[1])

    glTexCoord3f(tex_coords[3], tex_coords[4], tex_coords[5])
    glVertex2f(screen_coords[2], screen_coords[3])

    glTexCoord3f(tex_coords[6], tex_coords[7], tex_coords[8])
    glVertex2f(screen_coords[6], screen_coords[7])

    glEnd()
    glDisable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

def image_quad(name, *coords):
    assert len(coords) in (8,16)
    assert len(coords) == 8 # no support for "from" coordinates yet
    # idk I kind of wrote something for from coordinates but I
    # (1) don't know if I mapped it to the right space
    # (2) don't know if I access the texture size correctly

    # "to" coordinates
    screen_coords = coords[:8]
    glColor4f(*_data.TINT_COLOUR)

    if not name in _data.LOADED_IMGS.keys():
        #print("loading image", name)
        load_image(name)

    _img = _data.LOADED_IMGS[name]

    texture = _img.get_texture()
    tex_coords = texture.tex_coords

    if len(coords) > 8:
        # "from" coordinates
        for i in range(4):
            tex_coords[3*i] = coords[8+2*i] / _img.width
            tex_coords[3*i+1] = coords[8+2*i+1] / _img.height

    glEnable(texture.target)

    glBindTexture(texture.target, texture.id)
    glBegin(GL_QUADS)

    glTexCoord3f(tex_coords[0], tex_coords[1], tex_coords[2])
    glVertex2f(screen_coords[0], screen_coords[1])

    glTexCoord3f(tex_coords[3], tex_coords[4], tex_coords[5])
    glVertex2f(screen_coords[2], screen_coords[3])

    glTexCoord3f(tex_coords[6], tex_coords[7], tex_coords[8])
    glVertex2f(screen_coords[6], screen_coords[7])

    glTexCoord3f(tex_coords[9], tex_coords[10], tex_coords[11])
    glVertex2f(screen_coords[4], screen_coords[5])

    glEnd()
    glDisable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

def background(r, g=None, b=None, a=1.0):
    if g == None:
        r,g,b = hex2rgb(r)

    glClearColor(r,g,b,a)
    glClear(GL_COLOR_BUFFER_BIT)

def line(x1, y1, x2, y2):
    if _data.stroke_weight and _data.STROKE_COLOUR:
        x1, y1, x2, y2 = [int(i) for i in (x1, y1, x2, y2)]

        glLineWidth(_data.stroke_weight)
        glColor4f(*_data.STROKE_COLOUR)

        glBegin(GL_LINES)
        glVertex2f(x1,y1)
        glVertex2f(x2,y2)
        glEnd()

def rect(x, y, w, h):
    x, y, w, h = [int(i) for i in (x, y, w, h)]
    if _data.FILL_COLOUR:

        glColor4f(*_data.FILL_COLOUR)
        glBegin(GL_TRIANGLE_FAN)

        glVertex2f(x,y)
        glVertex2f(x+w,y)
        glVertex2f(x+w,y+h)
        glVertex2f(x,y+h)

        glEnd()

    if _data.stroke_weight and _data.STROKE_COLOUR:
        
        glColor4f(*_data.STROKE_COLOUR)
        glLineWidth(_data.stroke_weight)

        glBegin(GL_LINE_LOOP)

        glVertex2f(x,y)
        glVertex2f(x+w,y)
        glVertex2f(x+w,y+h)
        glVertex2f(x,y+h)

        glEnd()

def ellipse(x, y, w, h):
    x, y, w, h = [int(i) for i in (x, y, w, h)]

    if _data.FILL_COLOUR:

        glColor4f(*_data.FILL_COLOUR)
        glBegin(GL_TRIANGLE_FAN)

        glVertex2f(w/2+x,h/2+y)
        Iterations = 50
        for i in range(Iterations):
            glVertex2f(w/2 + x + w/2 * cos(i/(Iterations-1) * 2*pi), h/2 + y + h/2 * sin(i/(Iterations-1) * 2*pi))

        glEnd()

    if _data.stroke_weight and _data.STROKE_COLOUR:
        
        glColor4f(*_data.STROKE_COLOUR)
        glLineWidth(_data.stroke_weight)

        glBegin(GL_LINE_LOOP)

        Iterations = 50
        for i in range(Iterations):
            glVertex2f(w/2 + x + w/2 * cos(i/(Iterations-1) * 2*pi), h/2 + y + h/2 * sin(i/(Iterations-1) * 2*pi))

        glEnd()
    
def fill(r, g, b, a=1.0):
    if g == None:
        r,g,b = hex2rgb(r)

    _data.FILL_COLOUR = (r, g, b, a)

def stroke(r, g, b, a=1.0):
    if g == None:
        r,g,b = hex2rgb(r)

    _data.STROKE_COLOUR = (r, g, b, a)

def tint(r, g=None, b=None, a=1.0):
    if g == None:
        if type(r) == tuple:
            r,g,b,a = r
        else:
            r,g,b = hex2rgb(r)

    _data.TINT_COLOUR = (r, g, b, a)

def unload_image(name):
    del _data.LOADED_IMGS[name]

def load_raw_image_data(data, mode, w, h):
    img = pygame.image.fromstring(data, (w, h), mode).convert()
    iid = _data.new_image_id(_data.LOADED_IMGS.keys(), _data.letters)
    _data.LOADED_IMGS[iid] = img
    return iid

def text(txt, font_name='Helvetica', font_size=16.0, x=0.0, y=0.0, alignment=5):

    # anchor position opposes keypad position
    anchor = [
        ('right', 'top'), ('center', 'top'), ('left', 'top'),
        ('right', 'center'), ('center', 'center'), ('left', 'center'),
        ('right', 'bottom'), ('center', 'bottom'), ('left', 'bottom')
    ][alignment-1]

    """
    Using batches is more efficient if lots of text is being drawn, but
    it does not allow for arbitrary interlacing with OpenGL primitives.

    Currently, batching is disabled.
    """

    lbl = pyglet.text.Label(txt,
                      font_name,
                      font_size,
                      color=[int(x*255) for x in _data.TINT_COLOUR],
                      x=x, y=y,
                      anchor_x=anchor[0], anchor_y=anchor[1])#,
                      #batch= _data.screen)
    lbl.draw()

def render_text(txt, font_name, font_size):
    raise Exception("I did not implement this function.")

    """
    renderfont = pygame.font.SysFont(font_name, int(font_size))
    img = renderfont.render(txt, _data.anti_alias, _data.TINT_COLOUR)
    
    iid = _data.new_image_id(_data.LOADED_IMGS.keys(), _data.letters)
    _data.LOADED_IMGS[iid] = img
    
    sx, sy = img.get_size()
    return iid, sx, sy
    """

"""
END DRAWING FUNCTIONS
"""

def run(scene, orientation, frame_inverval, anti_alias):
    _run(scene, orientation, frame_inverval, anti_alias)
    scene._stop()

def _run(scene, orientation, frame_interval, anti_alias):
    if orientation == 2: # LANDSCAPE
        _data.DEFSIZE = _data.DEFSIZE[::-1]
    
    _data.DEFSIZE = getattr(scene,
                            "_pgwindowsize",
                            _data.DEFSIZE)

    window = pyglet.window.Window(
        width=_data.DEFSIZE[0],
        height=_data.DEFSIZE[1],
        caption="Pythonista Window",
        resizable=True
    )
    
    # enable transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    _data.anti_alias = anti_alias
    _data.FPS     = 60./frame_interval
    last_time     = time.time()
    
    scene._setup_scene(*_data.DEFSIZE)

    #@window.event
    def on_draw(*dt):
        window.clear()

        # buffer for high-level drawing operations
        _data.screen = pyglet.graphics.Batch()
        scene._draw(1/_data.FPS)
        _data.screen.draw()
    
    # run at double FPS for now, since we do not calculate frame deltas
    pyglet.clock.schedule_interval(on_draw, .5/_data.FPS) 

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        scene._touch_began(x,y,0)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        scene._touch_ended(x,y,0)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        scene._touch_moved(x,y,x-dx,y-dy,0)

    @window.event
    def on_resize(width, height):
        _data.DEFSIZE = (width, height)
        scene._set_size(width, height)

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED

    pyglet.app.run()
    scene._stop()
