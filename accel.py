import math
from typing import Tuple

def multMatrix(x, y, z, dt=0.06):
  # change matrix: a = -x
  sindt = math.sin(dt)
  cosdt = math.cos(dt)
  a, b, c = 1, dt, dt*dt/2
  d, e, f = 0, 1, dt
  g, h, i = 0, 0, 1
  return (a*x+b*y+c*z, d*x+e*y+f*z, g*x+h*y+i*z)
def multMatrix1(x, y, z, dt=0.06):
  # change matrix: a = -x
  sindt = math.sin(dt)
  cosdt = math.cos(dt)
  a, b, c = 1, sindt, 1-cosdt
  d, e, f = 0, cosdt, sindt
  g, h, i = 0, -sindt, cosdt
  return (a*x+b*y+c*z, d*x+e*y+f*z, g*x+h*y+i*z)
def multMatrix2(x, y, z, dt=0.06):
  hsin = math.sinh(dt)
  hcos = math.cosh(dt)
  a, b, c = 1, hsin, hcos-1
  d, e, f = 0, hcos, hsin
  g, h, i = 0, hsin, hcos
  return (a*x+b*y+c*z, d*x+e*y+f*z, g*x+h*y+i*z)

def mult(m1, m2):
  return (m1[0]*m2[0]+m1[1]*m2[3]+m1[2]*m2[6], m1[0]*m2[1]+m1[1]*m2[4]+m1[2]*m2[7], m1[0]*m2[2]+m1[1]*m2[5]+m1[2]*m2[8], 
          m1[3]*m2[0]+m1[4]*m2[3]+m1[5]*m2[6], m1[3]*m2[1]+m1[4]*m2[4]+m1[5]*m2[7], m1[3]*m2[2]+m1[4]*m2[5]+m1[5]*m2[8], 
          m1[6]*m2[0]+m1[7]*m2[3]+m1[8]*m2[6], m1[6]*m2[1]+m1[7]*m2[4]+m1[8]*m2[7], m1[6]*m2[2]+m1[7]*m2[5]+m1[8]*m2[8])
def mult2(m1, v1):
  return (m1[0]*v1[0]+m1[1]*v1[1]+m1[2]*v1[2], m1[3]*v1[0]+m1[4]*v1[1]+m1[5]*v1[2], m1[6]*v1[0]+m1[7]*v1[1]+m1[8]*v1[2])

def changeMatrix(diff):
  def multRet(retv, dt=1):
    retMatrix = (1, 0, 0, 0, 1, 0, 0, 0, 1)
    change = tuple(dt*q for q in diff)
    lastMatrix = change
    retMatrix = tuple(q + r for (q, r) in zip(retMatrix, lastMatrix))
    iterexp = 8 + abs(int(dt)*4)
    for fact in range(2, iterexp):
      lastMatrix = mult(lastMatrix, change)
      lastMatrix = tuple(q/fact for q in lastMatrix)
      retMatrix = tuple(q + r for (q, r) in zip(retMatrix, lastMatrix))
    return mult2(retMatrix, retv)
  return multRet

def changeMatrix2(diff, dtu=0.002):
  ident = (1, 0, 0, 0, 1, 0, 0, 0, 1)
  unitMatrix = (1, 0, 0, 0, 1, 0, 0, 0, 1)
  change = tuple(dtu*q for q in diff)
  lastMatrix = change
  unitMatrix = tuple(q + r for (q, r) in zip(unitMatrix, lastMatrix))
  for fact in range(2, 50): # 
    lastMatrix = mult(lastMatrix, change)
    lastMatrix = tuple(q/fact for q in lastMatrix)
    unitMatrix = tuple(q + r for (q, r) in zip(unitMatrix, lastMatrix))
  
  m2_cache = list()
  m2_cache.append(unitMatrix)
  def gen_m2(b2: int): #b2 must be >0
    while len(m2_cache) <= b2:
      m2_cache.append(mult(m2_cache[-1], m2_cache[-1]))
    return m2_cache[b2]
  
  def gen_bits(b2: int):
    while b2 > 0:
      b2, y = b2>>1, b2 & 1
      yield y == 1
  def iter_count():
    it = 0
    while True:
      yield it
      it = it + 1
  
  def multRet(retv: tuple, dt=1):
    udiv, umod = divmod(dt / dtu, 1)
    for chk, bit in zip(gen_bits(int(udiv)), iter_count()):
      if chk:
        retv = mult2(gen_m2(bit), retv)
    tween = mult2(unitMatrix, retv)
    return tuple(q*umod+r*(1-umod) for q, r in zip(tween, retv))
  return multRet

print(multMatrix1(4, 3, 2, dt = 100))
multMatrix3 = changeMatrix((0, 1, 0, 0, 0, 1, 0, -1, 0))
print(multMatrix3((4, 3, 2), dt = 100))
multMatrix5 = changeMatrix2((0, 1, 0, 0, 0, 1, 0, -1, 0), dtu=0.005)
print(multMatrix5((4, 3, 2), dt = 100))
multMatrix6 = changeMatrix2((0, 1, 0, 0, 0, 1, 0, -1, 0), dtu=0.002)
print(multMatrix6((4, 3, 2), dt = 100))
print(multMatrix2(4, 3, 2, dt = 10))
multMatrix4 = changeMatrix((0, 1, 0, 0, 0, 1, 0, 1, 0))
print(multMatrix4((4, 3, 2), dt = 10))
varc = (4, 3, 2)
for _ in range(10000):
  varc = multMatrix5(varc, dt = 0.01)
print(varc)
print(multMatrix5((4, 3, 2), dt=100))

