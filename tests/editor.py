import sys
import time
import binascii

import tb as traceback
import javascript
#import pdb

from browser import document, window, alert, bind, html
import browser.widgets.dialog as dialog
from print_support import clear_queue

# set height of container to 75% of screen
_height = document.documentElement.clientHeight
_s = document['container']
_s.style.height = '%spx' % int(_height * 0.4)

has_ace = True
try:
    editor = window.ace.edit("editor")
    editor.setTheme("ace/theme/solarized_light")
    editor.session.setMode("ace/mode/python")
    editor.focus()

    editor.setOptions({
     'enableLiveAutocompletion': True,
     'highlightActiveLine': False,
     'highlightSelectedWord': True
    })
except:
    from browser import html
    editor = html.TEXTAREA(rows=20, cols=70)
    document["editor"] <= editor
    def get_value(): return editor.value
    def set_value(x): editor.value = x
    editor.getValue = get_value
    editor.setValue = set_value
    has_ace = False

if hasattr(window, 'localStorage'):
    from browser.local_storage import storage
else:
    storage = None

if 'set_debug' in document:
    __BRYTHON__.debug = int(document['set_debug'].checked)

def reload():
    if 'current_script' in globals() and current_script != None:
        _name = current_script + '?foo=%s' % time.time()
        editor.setValue(open(_name).read())
    editor.scrollToRow(0)
    editor.gotoLine(0)


def reset_src():
    if "code" in document.query:
        code = document.query.getlist("code")[0]
        editor.setValue(code)
    else:
        if storage is not None and "py_src" in storage:
            editor.setValue(storage["py_src"])
        else:
            editor.setValue('for i in range(10):\n\tprint(i)')
    editor.scrollToRow(0)
    editor.gotoLine(0)

def reset_src_area():
    if storage and "py_src" in storage:
        editor.value = storage["py_src"]
    else:
        editor.value = 'for i in range(10):\n\tprint(i)'


class cOutput:
    encoding = 'utf-8'

    def __init__(self):
        self.cons = document["console"]
        self.buf = ''

    def write(self, data):
        self.buf += str(data)

    def flush(self):
        self.cons.value += self.buf
        self.buf = ''

    def __len__(self):
        return len(self.buf)

if "console" in document:
    cOut = cOutput()
    sys.stdout = cOut
    sys.stderr = cOut


def to_str(xx):
    return str(xx)

info = sys.implementation.version
version = '%s.%s.%s' % (info.major, info.minor, info.micro)
if info.releaselevel == "rc":
    version += f"rc{info.serial}"
document['version'].text = version

output = ''

def show_console(ev):
    document["console"].value = output
    document["console"].cols = 60
    
def adjust_canvas(canvas_count):
    # modify doc according to canvas count
    #print("Canvas count:{}".format(_canvas_count))
    maindiv = document["maindiv"]
    ih = ""
    maindiv.innerHTML = ih
    for i in range(1, int(canvas_count)+1):
        ih += "<canvas class='canvas"+canvas_count+"' id='canvas"+str(i)+"'></canvas>"
    maindiv.innerHTML = ih
    for i in range(1, int(canvas_count)+1):
        canvas = document["canvas"+str(i)]
        canvas.attrs["width"] = canvas.offsetWidth
        canvas.attrs["height"] = canvas.offsetHeight

def load_script_low(name_and_canvas):
        vals = name_and_canvas.split(",")
        _name = vals[0]
        _canvas_count = vals[1]
        
        # adjust canvas
        adjust_canvas(_canvas_count)
        
        # show some status
        stat_div = document["status_top"]
        stat_div.innerHTML = _name

        # remeber selected test from index page
        clear_queue()
        window.STEPPING=0
        
        current_script=_name
        _name = _name + '?foo=%s' % time.time()
        editor.setValue(open(_name).read())
        
        # remeber selected test from index page
        select = document["files"]
        if storage is not None and select is not None:
            storage["selected_idx"]=str(select.selectedIndex)


# load a Python script and setup the screen for it
def load_script(evt):
    #print(evt.detail, evt.target, evt.target.value, evt.target.type)
    if not hasattr(evt.target, "type") or not hasattr(evt, "detail"):
        load_script_low(evt.target.value)
        

# run a script, in global namespace if in_globals is True
def run(*args):
    global output
    document["console"].value = ''
    src = editor.getValue()
    if storage is not None:
       storage["py_src"] = src

    t0 = time.perf_counter()
    try:
        ns = {'__name__':'__main__'}
        exec(src, ns)
        state = 1
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        state = 0
    sys.stdout.flush()
    output = document["console"].value

    #print('<completed in %6.2f ms>' % ((time.perf_counter() - t0) * 1000.0))
    return state

def show_js(ev):
    src = editor.getValue()
    document["console"].value = javascript.py2js(src, '__main__')

def share_code(ev):
    src = editor.getValue()
    if len(src) > 2048:
        d = dialog.InfoDialog("Copy url",
                              f"code length is {len(src)}, must be < 2048",
                              style={"zIndex": 10},
                              ok=True)
    else:
        href = window.location.href.rsplit("?", 1)[0]
        query = document.query
        query["code"] = src
        url = f"{href}{query}"
        url = url.replace("(", "%28").replace(")", "%29")
        d = dialog.Dialog("Copy url")
        area = html.TEXTAREA(rows=0, cols=0)
        d.panel <= area
        area.value = url
        # copy to clipboard
        area.focus()
        area.select()
        document.execCommand("copy")
        d.remove()
        d = dialog.Dialog("Copy url")
        d.panel <= html.DIV("url copied in the clipboard<br>Send it to share the code")
        buttons = html.DIV()
        ok = html.BUTTON("Ok")
        buttons <= html.DIV(ok, style={"text-align": "center"})
        d.panel <= html.BR() + buttons

        @bind(ok, "click")
        def click(evt):
            d.remove()

if has_ace:
    reset_src()
else:
    reset_src_area()
