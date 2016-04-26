# do not edit, generated by pymola

from __future__ import print_function, division
import sympy
import scipy.integrate
import sympy.physics.mechanics as mech
import pylab as pl


class OdeModel(object):

    def __init__(self):
        self.t = sympy.symbols('t')
        self.x = sympy.Matrix([])
        self.u = sympy.Matrix([])
        self.y = sympy.Matrix([])
        self.p = sympy.Matrix([])
        self.c = sympy.Matrix([])
        self.v = sympy.Matrix([])
        self.x0 = {}
        self.u0 = {}
        self.p0 = {}
        self.c0 = {}
        self.eqs = []

    def compute_fg(self):
        fg_sol = sympy.solve(self.eqs, list(self.x.diff(self.t)) + list(self.y) +  list(self.v))
        self.f = self.x.diff(self.t).subs(fg_sol)
        assert(len(self.x) == len(self.f))
        self.g = self.y.subs(fg_sol)
        assert(len(self.g) == len(self.y))

    def linearize_symbolic(self):
        A = sympy.Matrix([])
        B = sympy.Matrix([])
        C = sympy.Matrix([])
        D = sympy.Matrix([])
        if len(self.x) > 0:
            if len(self.f) > 0:
                A = self.f.jacobian(self.x)
            if len(self.g) > 0:
                C = self.g.jacobian(self.x)
        if len(self.u) > 0:
            if len(self.f) > 0:
                B = self.f.jacobian(self.u)
            if len(self.g) > 0:
                D = self.g.jacobian(self.u)
        return (A, B, C, D)

    def linearize(self, x0=None, u0=None):
        ss = self.linearize_symbolic()
        ss_eval = []
        ss_subs = {}
        ss_subs.update(self.p0)
        ss_subs.update(self.c0)
        if x0 is None:
            x0 = self.x.subs(self.x0)[:]
        if u0 is None:
            u0 = self.x.subs(self.u0)[:]
        for i in range(len(ss)):
            ss_eval += [pl.matrix(ss[i].subs(ss_subs)).astype(float)]
        return ss_eval

    def simulate(self, x0=None, u0=None, t0=0, tf=10, dt=0.01):
        x_sym = sympy.DeferredVector('x')
        y_sym = sympy.DeferredVector('y')
        u_sym = sympy.DeferredVector('u')
        ss_subs = {self.x[i]: x_sym[i] for i in range(len(self.x))}
        ss_subs.update({self.u[i]: u_sym[i] for i in range(len(self.u))})
        ss_subs.update(self.p0)
        ss_subs.update(self.c0)

        # create f (dynamics) lambda function
        f_lam = sympy.lambdify((self.t, x_sym, u_sym), self.f.subs(ss_subs))
        res = pl.array(f_lam(0, pl.zeros(len(self.x)), pl.zeros(len(self.u))), dtype=float)
        if len(res) != len(self.x):
            raise IOError("f doesn't return correct size", res, self.x)

        # create jacobian lambda function
        if len(self.x) > 0 and len(self.f) > 0:
            jac_lam = sympy.lambdify((self.t, x_sym, u_sym), self.f.jacobian(self.x).subs(ss_subs))
            res = pl.array(jac_lam(0, pl.zeros(len(self.x)), pl.zeros(len(self.u))), dtype=float)
            if len(res.shape) == 2 and res.shape[1] != len(self.x):
                raise IOError("jacobian doesn't return correct size", res. self.f)
        else:
            jac_lam = None


        # create g (measurement) lambda function
        g_lam = sympy.lambdify((self.t, x_sym, u_sym), self.g.subs(ss_subs))
        res = pl.array(g_lam(0, pl.zeros(len(self.x)), pl.zeros(len(self.u))), dtype=float)
        if len(res.shape) == 2 and res.shape[1] != len(self.y):
            raise IOError("g doesn't return correct size", res, self.y)

        ode = scipy.integrate.ode(f_lam, jac_lam)
        ss_subs.update(self.x0)
        ss_subs.update(self.u0)
        if x0 is None:
            x0 = self.x.subs(self.x0)[:]
        if u0 is None:
            u0 = self.u.subs(self.u0)[:]
        print('x0', x0)
        ode.set_initial_value(x0, t0)
        y0 = g_lam(0, x0, u0)
        data = {
            't': [t0],
            'x': [x0],
            'y': [y0],
            'u': [u0],
        }
        while ode.t + dt <= tf:
            ode.set_f_params(u0)
            ode.set_jac_params(u0)
            if len(self.x) > 0:
                ode.integrate(ode.t + dt)
            else:
                ode.t += dt
            x = ode.y
            y = g_lam(ode.t, x, u0)
            data['t'] += [ode.t]
            data['x'] += [x]
            data['y'] += [y]
            data['u'] += [u0]
        data = {key: pl.array(data[key]) for key in data.keys()}
        return data

    def __repr__(self):
        return repr(self.__dict__)
