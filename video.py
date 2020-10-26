import cv2
import numpy as np 
import cairo as cr
import colorsys as cs
from ball import Ball
from sys import stdout

ball = Ball(400, 200)

directionSpeed = np.pi / 16
angleSpeed = np.pi / 10
colorSpeed = np.pi / 36
direction = 0
rgb = 0.6, 0.2, 0.75
hls = list(cs.rgb_to_hls(*rgb))
radiusRange = 4, 12
lightnessRange = 0.7, 0.3

fps = 30
t = 0
dt = 1 / fps 
size = 1080, 1080  
video = cv2.VideoWriter('1.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, size)
surface = cr.ImageSurface(cr.FORMAT_ARGB32, *size)
ctx = cr.Context(surface)
while t + dt < 30:
  direction += directionSpeed * dt 
  angle = angleSpeed * dt
  hls[0] += colorSpeed * dt 
  if hls[0] > np.pi * 2: hls[0] = 0
  
  ball.rotate(direction, angle)
  ctx.set_source_rgb(1, 1, 1)
  ctx.rectangle(0, 0, *size)
  ctx.fill()
  points = list(np.asarray(ball.points()))
  points.sort(key = lambda a: a[0])
  radius = ball.radius 
  w, h = size  
  for x, y, z in points:
    y += w / 2
    z += h / 2
    dep = (x + radius) / (2 * radius)
    r1, r2 = radiusRange
    r = dep * (r2 - r1) + r1
    l1, l2 = lightnessRange 
    hls[1] = dep * (l2 - l1) + l1
    rgb = cs.hls_to_rgb(*hls) 
    ctx.set_source_rgb(*rgb)
    ctx.arc(y, z, r, 0, np.pi * 2)
    ctx.fill()
  a = np.ndarray(size, np.uint32, surface.get_data())
  def op(bits):
    b = np.bitwise_and(a, 0xff << bits)
    b = np.right_shift(b, bits)
    b = np.expand_dims(b, -1)
    return b
  r = op(16)
  g = op(8)
  b = op(0)
  bgr = np.concatenate((b, g, r), 2)
  bgr = bgr.astype(np.uint8)
  video.write(bgr)
  print('\rtime: %.2f'%t, end = '')
  stdout.flush()
  t += dt

video.release()
