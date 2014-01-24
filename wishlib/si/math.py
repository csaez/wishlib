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
