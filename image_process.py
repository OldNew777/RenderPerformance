def tonemapping_aces(x):
    a = 2.51
    b = 0.03
    c = 2.43
    d = 0.59
    e = 0.14
    return x * (a * x + b) / (x * (c * x + d) + e)


def tonemapping_uncharted2(x):
    def F(x):
        A = 0.22
        B = 0.30
        C = 0.10
        D = 0.20
        E = 0.01
        F = 0.30
        return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F
    WHITE = 11.2
    return F(1.6 * x) / F(WHITE)