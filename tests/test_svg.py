from bit_pu_rq_1d_decor import *
from print_support import *
from browser import svg, document as doc, window
from browser import timer
q = 1
q1 = 1
d = doc["panel"]
t = None
x = CanvasDraw()

def anim2(e):
    global q1
    global t1
    if (q1 % 10) >= 5:
        color = "white"
    else:
        color = "yellow"
    d.html = ""
    q1 = q1 + 1
    for c in range(1, 10):
        circle = svg.circle(cx=c*100, cy=120, r=30, stroke="black",stroke_width="2", fill=color)
        title = svg.text('Title', x=c*100, y=130, font_size=20,text_anchor="middle")
        d <= circle
        d <= title
    if (q1 == 500):
        timer.cancel_animation_frame(t1)
    else:
        t1 = timer.request_animation_frame(anim2)

def anim(e):
    global q
    global t
    if (q % 10) <= 5:
        color = "white"
    else:
        color = "yellow"
    q = q + 1
    x.fill_color(color)
    x.fill_rect(10,10, 30, 30)
    if (q >= 500):
        timer.cancel_animation_frame(t)
    else:
        t = timer.request_animation_frame(anim)

t = timer.request_animation_frame(anim)
t1 = timer.request_animation_frame(anim2)


