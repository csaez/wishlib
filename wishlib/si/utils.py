from collections import namedtuple

from .shortcuts import si, sidict, disp, simath
from .math import multiply_vector_matrix, rotate_vector


def siget(fullname=""):
    """Returns a softimage object given its fullname."""
    fullname = str(fullname)
    if not len(fullname):
        return None
    return sidict.GetObject(fullname, False)


def inside_softimage():
    """Returns a boolean indicating if the code is executed inside softimage."""
    try:
        disp('XSI.Application')
        return True
    except:
        return False


def cmd_wrapper(cmd_name, **kwds):
    """Wrap and execute a softimage command accepting named arguments"""
    cmd = si.Commands(cmd_name)
    if not cmd:
        raise Exception(cmd_name + " doesnt found!")
    for arg in cmd.Arguments:
        value = kwds.get(arg.Name)
        if value:
            arg.Value = value
    return cmd.Execute()


def raycast(geometry, position, direction):
    hit = False
    g = geometry.ActivePrimitive.Geometry
    p = simath.CreateVector3(position)
    d = simath.CreateVector3(direction)

    # convert to local space
    space = geometry.Kinematics.Global.Transform.Matrix4
    space.InvertInPlace()
    p = multiply_vector_matrix(p, space).Get2()
    tm = simath.CreateTransform()
    tm.SetMatrix4(space)
    d = rotate_vector(d, tm.Rotation).Get2()

    # raycast
    location = g.GetRaycastIntersections(p, d)
    pos = zip(*g.EvaluatePositions(location))[0]
    pos = simath.CreateVector3(pos)
    normal = zip(*g.EvaluateNormals(location, 1))[0]
    normal = simath.CreateVector3(normal)

    # convert to world space and return a namedtuple
    space = geometry.Kinematics.Global.Transform.Matrix4
    if pos.Get2() != (0, 0, 0):  # if hit
        hit = True
        pos = multiply_vector_matrix(pos, space)
    pos = pos.Get2()
    tm.SetMatrix4(space)
    normal = rotate_vector(normal, tm.Rotation).Get2()
    return namedtuple("raycast", ["hit", "position", "normal"])(hit, pos, normal)


def project_into_mesh(mesh, target, max_depth=2):
    # validate entries
    if mesh is None or target is None:
        return None
    # calculate direction
    cam = si.GetViewCamera(-1)
    position = cam.Kinematics.Global.Transform.Translation
    direction = simath.CreateVector3(*target)
    direction.SubInPlace(position)
    direction.NormalizeInPlace()
    position = position.Get2()
    direction = direction.Get2()
    # raycast
    results = list()
    for i in range(max_depth):
        r = raycast(mesh, position, direction)
        if r.hit:
            position = r.position
            results.append(position)
            position = [p + (direction[i] * 0.01)
                        for i, p in enumerate(position)]
    if len(results):
        # sum and return average
        return [sum(coord) / len(coord) for i, coord in enumerate(zip(*results))]
    return None
