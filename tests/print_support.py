# printing support module

DEBUG=False

draw_settings = {
   'circle_diameter':15,
   'start_x': 30,
   'start_y': 30,
   '2d_x': 20,
   '2d_y': 20,
   'box_size': 30,
   'default_line_width': 1,
   'highlight_line_width': 3,
   'default_color':'black',
   'highlight_color':'red',
   'default_font': "12px Arial",
   'big_font': "15px Arial"
}

from enum import Enum
from types import MethodType

class TreeType(Enum):
    """
        There are 2 types of trees how can BIT be displayed: either as Query tree or as Update tree.
    """
    NoTree = -1
    QueryTree = 0
    UpdateTree = 1

class Tools(object):
    """
        There are 2 types of trees how can BIT be displayed: either as Query tree or as Update tree.
    """
    def sleep(self):
        pass
        
    def my_print(self, text):
        print(text)

tools = Tools()


if ('__BRYTHON__' in globals()):
    from browser import document, html, aio, svg, window
    from browser.html import BR
    from browser import timer
    import sys
    import math
    
    queue = []
    started = False
    
    class CanvasDraw(object):
        def __init__(self, canvas):
            canvas = document[canvas]
            canvas.attrs["width"] = canvas.offsetWidth
            canvas.attrs["height"] = canvas.offsetHeight
            self.canvas = canvas
            self.ctx = self.canvas.getContext("2d")
            self.ctx.font = "12px Arial"
            self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height);
            self.tree_type = TreeType.NoTree
            
        def update_tree_type(self, newtype, pre) -> None:
            return
            """if pre and self.tree_type == TreeType.NoTree:
                return
            if self.tree_type != newtype :
                self.push_sleep(2)
            if not pre: 
                self.tree_type=newtype"""
            
        """ clear screen """
        def cls(self):
            self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height)

        """ clear screen for updatep """
        def cls_updatep(self):
            self.ctx.clearRect(0, 25, self.canvas.width, self.canvas.height)

        """ fill color """
        def fill_color(self, color):
            self.ctx.fillStyle = color
            
        """ stroke color """
        def stroke_color(self, color):
            self.ctx.strokeStyle = color
            
        """ fill rectangle """
        def fill_rect(self, start_x, start_y, end_x, end_y):
            self.ctx.fillRect(start_x, start_y, end_x, end_y);

        """ fill circle """
        def fill_circle(self, x, y, diameter):
            ctx = self.ctx
            ctx.beginPath()
            ctx.arc(x, y, diameter, 0, 2 * math.pi)
            ctx.fill()
            
        """ draw text at x, y """
        def text_left(self, draw_x, draw_y, text_to_draw):
            self.ctx.fillText(str(text_to_draw), draw_x, draw_y)

        """ draw text at x, y """
        def text_big(self, draw_x, draw_y, text_to_draw):
            self.ctx.font = draw_settings["big_font"]
            self.ctx.fillText(str(text_to_draw), draw_x, draw_y)
            self.ctx.font = draw_settings["default_font"]
            
        """ draw text at x, y """
        def text_center(self, draw_x, draw_y, text_to_draw):
            self.ctx.fillText(str(text_to_draw), draw_x - (self.ctx.measureText(text_to_draw).width / 2), draw_y)

        """ draw a circle centered at x, y """
        def text_in_circle(self, draw_x, draw_y, circle_diameter, text_to_draw, \
                width = draw_settings['default_line_width'], color = draw_settings['default_color']):
            ctx = self.ctx
            ctx.beginPath()
            ctx.arc(draw_x, draw_y, circle_diameter, 0, 2 * math.pi)
            ctx.lineWidth=width
            ctx.strokeStyle=color
            ctx.stroke()
            measures = ctx.measureText(text_to_draw)
            # print(dict(measures))
            ctx.fillText(str(text_to_draw), draw_x - measures.width/2, 
                draw_y + (measures.actualBoundingBoxAscent + measures.actualBoundingBoxDescent)/2)

        def text_in_circle_h(self, draw_x, draw_y, circle_diameter, text_to_draw, highlight = False):
            self.text_in_circle(draw_x, draw_y, circle_diameter, text_to_draw, 
                draw_settings['highlight_line_width'] if highlight else draw_settings['default_line_width'], 
                draw_settings['highlight_color'] if highlight else draw_settings['default_color'])


        """ draw a rectangle centered at x, y """
        def text_in_rect_center(self, draw_x, draw_y, box_size, text_to_draw):
            self.ctx.beginPath()
            self.ctx.rect(draw_x - box_size/2, draw_y - box_size/2, box_size, box_size)
            self.ctx.strokeStyle="black"
            self.ctx.stroke()
            measures = self.ctx.measureText(text_to_draw)
            # print(dict(measures))
            self.ctx.fillText(str(text_to_draw), draw_x - measures.width/2,
                draw_y + (measures.actualBoundingBoxAscent + measures.actualBoundingBoxDescent)/2)

        """ draw a rectangle with upper left corner at x, y with optional highlight """
        def cell_2d_hi(self, x1, y1, box_size, text_to_draw, highlight = False):
            self.ctx.beginPath()
            self.ctx.rect(x1, y1, box_size, box_size)
            self.ctx.strokeStyle=draw_settings['highlight_color'] if highlight else draw_settings['default_color']
            self.ctx.lineWidth=draw_settings['highlight_line_width'] if highlight else draw_settings['default_line_width']
            self.ctx.stroke()
            measures = self.ctx.measureText(text_to_draw)
            # print(dict(measures))
            self.ctx.fillText(str(text_to_draw), x1 + (box_size - measures.width)/2, 
                y1 + box_size - measures.actualBoundingBoxAscent - measures.actualBoundingBoxDescent)
                
        def cell_2d(self, draw_x, draw_y, box_size, text_to_draw):
            self.cell_2d_hi(draw_x, draw_y, box_size, text_to_draw)

            
        """ draw a vector from x1, y1 to x2,y2 with color and width """
        def vector_cw(self, x1, y1, x2, y2, color, width):
            self.ctx.beginPath()
            self.ctx.lineWidth=width
            self.ctx.strokeStyle=color
            self.ctx.moveTo(x1, y1)
            self.ctx.lineTo(x2, y2)
            self.ctx.stroke()

        """ draw a vector from x1, y1 to x2,y2 with default color and default width """
        def vector(self, x1, y1, x2, y2):
            self.vector_cw(x1, y1, x2, y2, draw_settings['default_color'], draw_settings['default_line_width'])
        
        """ draw a vector from x1, y1 to x2,y2 with default color and default width """
        def vector_hi(self, x1, y1, x2, y2):
            self.vector_cw(x1, y1, x2, y2, draw_settings['highlight_color'], draw_settings['highlight_line_width'])
            
        """ draw vector animation starting at x1, y1 to x2, y2 with 2 colors and percentage of highlight"""
        def vector_p(self, x1, y1, x2, y2, color1, color2, percent):
            #print('P:',percent)
            dx = (x2-x1)*(percent/100)
            dy = (y2-y1)*(percent/100)
            if (dx != 0 or dy != 0):
                self.vector_cw(x1, y1, x1+dx, y1+dy, color2, draw_settings['highlight_line_width'] )
            if (x1 + dx != x2 or y1 + dy != y2):
                self.vector_cw(x1+dx, y1+dy, x2, y2, color1, draw_settings['default_line_width'] )
                
        def push(self, object, tree_type, method, *args):
            global queue
            global started
            started = True
            cp = object.clone()
            elem = { 'obj':cp, 'm':method, 'a': args }
            self.update_tree_type(tree_type, True)
            queue.append(elem)
            self.update_tree_type(tree_type, False)
            # DEBUG
            if DEBUG:
                print("PUSH:", elem)
    
        def push_print(self, text):
            global queue
            global started
            started = True
            elem = { 'obj':tools, 'm':Tools.my_print, 'a': text } 
            queue.append(elem)
            # DEBUG
            #print("PUSH:", elem)
            
        def push_sleep(self, count):
            global queue
            global started
            started = True
            for i in range(0,count):
                elem = { 'obj':tools, 'm':Tools.sleep, 'a': () } 
                queue.append(elem)
                #print("PUSH:", elem)
            
            
    class AnimatedObj(object):
        def __init__(self, draw_support, animation_type = 'blink', speed = 2):
            self.draw_support = draw_support
            self.animation_start = None
            self.animation_last = None
            self.progress = 0 # percentage ?
            self.animation_type = animation_type # supported blink, progr
            self.speed = speed # 10 equals 20 msec
            self.run = True
            
        def pre_animate(self, time):
            if self.animation_start == None:
                self.animation_start = time
                
        def post_animate(self, time):
            if self.progress >= 100:
                self.run = False
            elif self.progress  < 100:
                self.progress = self.progress + self.speed
                self.animation_last = time
    
    class AnimatedLine(AnimatedObj):
        def __init__(self, draw_support, x1, y1, x2, y2):
            super().__init__(draw_support, animation_type='progr') 
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.color1 = draw_settings["default_color"]
            self.color2 = draw_settings["highlight_color"]
            
        def animate(self, time):
            if (not self.run):
                return
            super().pre_animate(time)
            self.draw_support.vector_p(self.x1, self.y1, self.x2, self.y2, self.color1, self.color2, self.progress)
            super().post_animate(time)
            
    class State1d(object):
        def __init__(self, type: TreeType = None ):
            self.vectors = []
            self.vertices = []
            self.type = type
            self.percent = 0
            self.current_vector = 0
            self.draw_support = CanvasDraw()
            self.vectors.append(AnimatedLine(self.draw_support,10,10,100,100))
            self.last_time = None
            
        def next_frame(self, time):
            """if self.last_time:
                if time - self.last_time < 100:
                    return"""
            self.last_time = time
            if self.percent < 100:
                self.percent = self.percent + 1
                
        def draw_frame(self, time):
            for v in self.vectors:
                if v.run:
                    v.animate(time)
         
    #global state
    #state = State1d(None)
    
    def pop_exec():
        global queue
        if len(queue) == 0:
            return
        pop = queue.pop(0)
        obj = pop['obj']
        method = pop['m']
        args = pop['a']
        # DEBUG
        if DEBUG:
            print('POP:',obj, method, args)
        m = MethodType(method, obj)
        if type(args) == tuple:
            m(*args)
        else:
            m(args)
            
    def exec_immediate():
        global queue
        if len(queue) == 0:
            return False
        if DEBUG:
            print('EI:',queue[0])
        return queue[0]['m'] == Tools.my_print

    def clear_queue():
        global queue
        queue = []
        
    def is_empty():
        return len(queue) == 0
        
    start = 0
    
    """ fetch next from queue and draw it in animation frame intervals """
    def animate(time):
        global start
        global started
        global queue
        
        #state.draw_frame(time)
        #state.next_frame(time)
        while exec_immediate():
            pop_exec()
            document.getElementById("console").scrollTop = document.getElementById("console").scrollHeight 

        if time - start > window.ANIM_SPEED or window.STEPPING==1:
            if window.ANIM_SPEED > 200:
                pass
                #window.beep()
            pop_exec()
            start = time
        if DEBUG:
            print("a:",af,time)
        if started and is_empty():
            timer.cancel_animation_frame(window.af)
            window.STEPPING=2 
        else:
            if window.STEPPING!=1:
                window.af = timer.request_animation_frame(animate)
    
else:

    class CanvasDraw(object):
        def __init__(self, canvas):
            pass
            
        def return_none(*args, **kwargs):
            return None
            
        def push(self, object, method, *args):
            pass
    
        def push_print(self, text):
            print(text)
            
        def push_sleep(self, count):
            pass
            
        def __getattr__(self,attr):
            return self.return_none

        def __get_global_handler(self, name):
            return self.return_none

        def __global_handler(self, *args, **kwargs):
            return self.return_none
            
