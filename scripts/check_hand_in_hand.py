from fractions import Fraction as Q
from math import atan2, degrees
import json
from pathlib import Path


def add(a, b): return tuple(x + y for x, y in zip(a, b))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def mul(k, a): return tuple(k * x for x in a)
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def det(a, b): return a[0] * b[1] - a[1] * b[0]
def norm2(a): return dot(a, a)
def dist2(a, b): return norm2(sub(a, b))
def ccw(a): return (-a[1], a[0])
def cw(a): return (a[1], -a[0])
def turn(center, p, rotation): return add(center, rotation(sub(p, center)))
def angle(a, v, b):
    x, y = sub(a, v), sub(b, v)
    return degrees(atan2(abs(float(det(x, y))), float(dot(x, y))))


checks = {}
count = 0
for s in [Q(1), Q(4), Q(7, 2)]:
    A, B, C = (Q(0), s), (Q(0), Q(0)), (s, Q(0))
    for D in [(Q(-1), Q(1)), (Q(-2, 5), s / 3),
              (s / 5, s / 2), (Q(-3), -s / 4), (s * 2, s / 3)]:
        E, F = turn(A, D, ccw), mul(-1, D)
        G1, G2 = (Q(0), -s), (-s, Q(0))
        assert turn(C, A, ccw) == G1
        assert turn(C, E, ccw) == F
        assert turn(A, C, cw) == G2
        assert turn(A, E, cw) == D
        assert dist2(C, E) == dist2(C, F) == dist2(D, G2)
        assert dot(sub(E, C), sub(F, C)) == 0
        assert det(sub(D, G2), sub(F, C)) == 0
        count += 1
checks['example_1_exact_cases'] = count
A, B, C, D, E, F = (0, 4), (0, 0), (4, 0), (-1, 1), (3, 3), (1, -1)
assert dist2(C, E) == dist2(C, F) == 10
G = (-4, 0)
assert abs(angle(E, C, A) + angle(B, C, F) - 45) < 1e-10
checks['example_1_sample_squared_length'] = 10

count, special = 0, []
for a in [Q(1), Q(2), Q(3)]:
    for d in [a * Q(5, 4), a * Q(8, 5), a * 2, a * 3, a * 10]:
        B, A, C, D = (Q(0), Q(0)), (a, a), (2 * a, Q(0)), (d, d)
        E = turn(D, C, cw)
        F, G = sub(mul(2, D), E), mul(2, A)
        P = sub(mul(2, D), G)
        assert E == (Q(0), 2 * (d - a))
        assert turn(C, B, cw) == G and turn(C, E, cw) == F
        assert dist2(B, E) == dist2(G, F) == dist2(E, P)
        assert P == (2 * (d - a), 2 * (d - a))
        assert P[0] > 0
        assert det(sub(P, E), sub(F, G)) == 0
        assert dot(sub(E, B), sub(C, B)) == 0
        assert dist2(B, C) == 2 * dist2(A, C)
        assert dist2(E, C) == 2 * dist2(D, C)
        assert abs(angle(A, C, D) - angle(B, C, E)) < 1e-10
        alpha = angle(E, B, P)
        assert abs(alpha - 45) < 1e-10
        assert abs(angle(C, G, F) - (135 - alpha)) < 1e-10
        if D == G:
            assert P == D
            special.append('D = G and P = D: point reflection remains valid')
        count += 1
checks['example_2_exact_cases'] = count
checks['example_2_coincident_cases'] = len(special)
A, B, C, D, E = (2, 2), (0, 0), (4, 0), (3, 3), (0, 2)
assert dist2(B, E) == 4 and dist2(B, C) == 16
assert dist2(A, C) == 8 and dist2(D, C) == 10 and dist2(E, C) == 20
checks['example_2_sample'] = {'BE': 2, 'BC': 4, 'AC_squared': 8,
                              'DC_squared': 10, 'EC_squared': 20}
E_mirror = turn(D, C, ccw)
assert dot(sub(E_mirror, B), sub(C, B)) != 0
checks['opposite_orientation_counterexample'] = {'E': list(E_mirror), 'BE_perpendicular_BC': False}
out = Path(__file__).resolve().parents[1] / 'tmp' / 'hand-in-hand-math-checks.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(checks, ensure_ascii=False, indent=2))
