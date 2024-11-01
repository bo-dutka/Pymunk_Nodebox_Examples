#encoding: utf-8
from __future__ import division

from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util
import random
from math import sin, cos, pi, atan2
space = pymunk.Space()
space.gravity = 0,-981


BULLET_LIFESPAN=1.0

def create_moto():
    cbody = pymunk.Body()
    cbody.position = 200,400
    circle=pymunk.Circle(cbody,20)
    circle.mass = 100
    circle.friction = 1000
    space.add(cbody, circle)
    cbody2 = pymunk.Body()
    cbody2.position = 300,400
    circle2=pymunk.Circle(cbody2,20)
    circle2.mass = 100
    circle2.friction = 1000
    circle.elasticity=0.3
    circle2.elasticity=0.3
    c = pymunk.PinJoint(cbody, cbody2, (0, 0), (0, 0))
    space.add(cbody2, circle2, c)
    pbody = pymunk.Body()
    pbody.position = 250,450
    poly=pymunk.Circle(pbody,20)
    poly.mass = 10
    poly.friction = 1
    c2 = pymunk.PinJoint(cbody, pbody, (0, 0), (0, 0))
    c3 = pymunk.DampedSpring(cbody2, pbody, (0, 0), (0, 0), 50, 5000, 300)
    space.add(pbody, poly, c2, c3)
    return pbody, cbody, cbody2

pbody, cbody, cbody2 = create_moto()

#Земля
body2 = pymunk.Body(body_type = pymunk.Body.STATIC)
body3 = pymunk.Body(body_type = pymunk.Body.STATIC)
body2.position = (0, 0)
body3.position = (650, 0)
l1 = pymunk.Segment(body2, (0, 0), (900, 0), 10)#Земля
l2 = pymunk.Segment(body2, (0, 900), (0, 0), 1)#ЛІВА СТІНКА
l3 = pymunk.Segment(body3, (0, 900), (0, 0), 1)#ПРАВА СТІНКА
l1.friction = 1
l1.collision_type = 3
l2.collision_type = 3
l3.collision_type = 3
l1.color = (0, 200, 0, 255)
l2.color = (255, 255, 255, 255)
l3.color = (255, 255, 255, 255)
space.add(body2, body3, l3, l1, l2)

draw_options = pymunk.pyglet_util.DrawOptions()

POLY_TYPE=1
BULLET_TYPE=2
bullets =[]

def create_poly(x, y):
    body = pymunk.Body()
    body.position = x, y
    body.velocity = 0, -0.01
    poly = pymunk.Poly.create_box(body, size=(20, 50))
    poly.mass = 1111
    poly.friction = 1
    poly.elasticity = 0.1
    poly.color = (255, 0, 0, 255)
    poly.collision_type = POLY_TYPE
    space.add(body, poly)

def create_poly2(x, y, x1, y1):
    body = pymunk.Body()
    body.position = x, y
    body.velocity = x1, y1
    poly = pymunk.Circle(body, 5)
    poly.mass = 100
    poly.friction = 1
    poly.elasticity = 0.1
    poly.color = (0, 0, 0, 255)
    poly.collision_type = BULLET_TYPE
    space.add(body, poly)
    bullets.append({'body': body, 'shape': poly, 'elapsed_time': 0})
    return poly

def collision_handler(arbiter, space, data):
    global score
    for shape in arbiter.shapes:
        if shape.collision_type == POLY_TYPE:
            space.remove(shape.body, shape)
            score+=1
    return True
score=0

handler = space.add_collision_handler(POLY_TYPE, BULLET_TYPE)
handler.begin = collision_handler

def draw(canvas):
    global score
    pbody.angle=atan2(canvas.mouse.y-pbody.position[1], canvas.mouse.x-pbody.position[0])

    background(1)
    space.step(0.02)
    if canvas.keys.char=="a": #Щоб їхати вліво натисніть 'a'
        cbody.angular_velocity= 15
        cbody2.angular_velocity= 15
    space.debug_draw(draw_options)

    if canvas.keys.char=="d":#Щоб їхати вправо натисніть 'd'
        cbody.angular_velocity= -15
        cbody2.angular_velocity= -15

    space.debug_draw(draw_options)

    if canvas.mouse.button==LEFT:
        create_poly2(pbody.position[0], pbody.position[1], 1000 * cos(pbody.angle), 1000 * sin(pbody.angle))

    # Видаляє снаряди
    for bullet in list(bullets):
        bullet['elapsed_time'] += 0.02
        if bullet['elapsed_time'] > BULLET_LIFESPAN:
            space.remove(bullet['body'], bullet['shape'])
            bullets.remove(bullet)

    if canvas.frame%100==0:
        x_position = random.randint(0, 500)
        create_poly(x_position, 500)

    text("Score: " + str(score), 300, 300)#Виводить рахунок

canvas.size = 500, 500
canvas.run(draw)