from collections import namedtuple
from .shortcuts import simath


def raycast(geometry, position, direction):
    geometry = geometry.ActivePrimitive.Geometry
    p = simath.CreateVector3(position)
    d = simath.CreateVector3(direction)

    # convert to geometry space
    space = geometry.Parent.Parent3DObject.Kinematics.Global.Transform
    p = simath.MapWorldPositionToObjectSpace(space, p).Get2()
    d = simath.MapWorldOrientationToObjectSpace(space, d).Get2()

    # raycast
    location = geometry.GetRaycastIntersections(p, d)
    pos = zip(*geometry.EvaluatePositions(location))[0]
    pos = simath.CreateVector3(pos)
    normal = zip(*geometry.EvaluateNormals(location, 1))[0]
    normal = simath.CreateVector3(normal)

    # convert to world space and return a namedtuple
    pos = simath.MapObjectPositionToWorldSpace(space, pos).Get2()
    normal = simath.MapObjectOrientationToWorldSpace(space, normal).Get2()
    return namedtuple("raycast", ["position", "normal"])(pos, normal)


def direction_to_rotation(direction, up_vector):
    x = simath.CreateVector3(direction)
    y = simath.CreateVector3(up_vector)
    z = simath.CreateVector3()
    z.Cross(x, y)
    y.Cross(x, z)
    rotation = simath.CreateRotation()
    rotation.SetFromXYZAxes(x, y, z)
    return rotation
