# The MIT License (MIT)

# Copyright (c) 2014 Cesar Saez

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import
from .shortcuts import simath


def direction_to_rotation(direction, up_vector):
    x = simath.CreateVector3(direction)
    y = simath.CreateVector3(up_vector)
    z = simath.CreateVector3()
    z.Cross(x, y)
    y.Cross(x, z)
    rotation = simath.CreateRotation()
    rotation.SetFromXYZAxes(x, y, z)
    return rotation


def multiply_vector_matrix(vector3, matrix4):
    tm = simath.CreateTransform()
    tm.SetTranslation(vector3)
    m = tm.Matrix4
    m.MulInPlace(matrix4)
    tm.SetMatrix4(m)
    return tm.Translation


def rotate_vector(vector3, rotation):
    tm1 = simath.CreateTransform()
    tm1.SetTranslation(vector3)
    m1 = tm1.Matrix4
    tm2 = simath.CreateTransform()
    tm2.SetRotation(rotation)
    m2 = tm2.Matrix4
    m1.MulInPlace(m2)
    tm1.SetMatrix4(m1)
    return tm1.Translation
