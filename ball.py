import numpy as np
from numpy import linalg

def rotate(a, b, ang):
  a1 = np.dot(a, b) / np.dot(b, b) * b
  a2 = a - a1
  w = np.cross(a2, b)
  d = np.cos(ang) * a2 / linalg.norm(a2) + np.sin(ang) * w / linalg.norm(w)
  a3 = linalg.norm(a2) * d
  return a1 + a3

def generate(r, n):
  points = []
  k = (np.sqrt(5) - 1) / 2
  for i in range(1, n + 1):
    z = (2 * i - 1) / n - 1
    p = np.sqrt(1 - z**2)
    ang = 2 * np.pi * i * k
    x = p * np.cos(ang)
    y = p * np.sin(ang)
    points.append([x, y, z])
  return np.array(points) * r


class Ball:
  def __init__(self, r, n):
    self.radius = r
    self.A = np.identity(3)
    xVectors = generate(r, n)
    self.X = np.matrix(xVectors.T)

  def rotate(self, direction, angle):
    dirVector = np.array([0, np.cos(direction), np.sin(direction)])
    for i in range(3):
      self.A[:,i] = rotate(self.A[:,i], dirVector, angle)

  def points(self):
    return (self.A * self.X).T

if __name__ == '__main__':
  b = Ball(10, 10)
  b.rotate(1, 1)
  print(b.points())

