from itertools import product, cycle

from ttyfb import *  # noqa
from ttyfb import Matrix4x4, Vec3

PHI = (1 + 5**.5) / 2
TAU = 6.283185307179586


def dodecahedron():
    vs = []
    for a, b, c in product([1, -1], repeat=3):
        vs.append(Vec3(a, b, c))

    for a, b in product([1, -1], repeat=2):
        vs.extend([
            Vec3(0, a * PHI, b / PHI),
            Vec3(a / PHI, 0, b * PHI),
            Vec3(a * PHI, b / PHI, 0),
        ])

    return [
        (vs[0], vs[8]), (vs[0], vs[9]), (vs[0], vs[10]),
        (vs[1], vs[10]), (vs[1], vs[11]), (vs[1], vs[12]),
        (vs[2], vs[9]), (vs[2], vs[13]), (vs[2], vs[14]),
        (vs[3], vs[12]), (vs[3], vs[13]), (vs[3], vs[17]),
        (vs[4], vs[8]), (vs[4], vs[15]), (vs[4], vs[16]),
        (vs[5], vs[11]), (vs[5], vs[16]), (vs[5], vs[18]),
        (vs[6], vs[14]), (vs[6], vs[15]), (vs[6], vs[19]),
        (vs[7], vs[17]), (vs[7], vs[18]), (vs[7], vs[19]),
        (vs[8], vs[11]), (vs[9], vs[15]), (vs[10], vs[13]),
        (vs[12], vs[18]), (vs[14], vs[17]), (vs[16], vs[19]),
    ]


def faces(o):
    m = Matrix4x4.perspective(TAU / 16, 1, 0.1, 10)
    r = Matrix4x4.rotation(o, 1, 0, 1)

    def project(v):
        v = r.map_vec3(v) + Vec3(0, 0, 3)
        c = lerp(255, 0, (v.z - 1.25) / 3.45)
        v = m.map_vec3(v)
        v = v * h / 10 + Vec3(w / 2, h / 2, 0)
        return v, c

    for a, b in dodecahedron():
        p, c_p = project(a)
        q, c_q = project(b)
        line((p.x, p.y), (q.x, q.y), (c_p, c_p, c_p), (c_q, c_q, c_q))


if __name__ == '__main__':
    with no_cursor():
        for o in cycle(range(360)):
            clear()
            faces(o)
            render(to_stdout)
