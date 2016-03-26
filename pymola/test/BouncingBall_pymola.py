
#############################################################################
# Automatically generated by pymola

from __future__ import print_function, division
import sympy
assert sympy.__version__ >= '0.7.6.1'
import sympy.physics.mechanics as mech
sympy.init_printing()
try:
    mech.init_vprinting()
except AttributeError:
    mech.mechanics_printing()
import scipy.integrate
import pylab as pl
from collections import OrderedDict

#pylint: disable=too-few-public-methods, too-many-locals, invalid-name, no-member

class Model(object):
    """
    Modelica Model.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.t = sympy.symbols('t')

        
        # symbols
        g, c = \
            sympy.symbols('g, c')
        

        # dynamic symbols
        height, velocity = \
            mech.dynamicsymbols('height, velocity')

        # parameters
        self.p_dict = OrderedDict({
            'g': 9.81,
            'c': 0.90,
        })

        # initial sate
        self.x0_dict = OrderedDict({
            'height': 10,
            'velocity': 0,
        })

        # state space
        self.x = sympy.Matrix([
            height, velocity
        ])

        # equations
        self.eqs = [
            height.diff(self.t) - velocity,
            velocity.diff(self.t) - -(g),
            ]


        # when equations



        self.x = sympy.Matrix(self.x)
        self.x_dot = self.x.diff(self.t)

        self.sol = sympy.solve(self.eqs, self.x_dot)

        self.f = sympy.Matrix([self.sol[xi] for xi in self.x_dot])
        print('x:', self.x)
        print('f:', self.f)

        self.p_vect = [locals()[key] for key in self.p_dict.keys()]

        print('p:', self.p_vect)

        self.f_lam = sympy.lambdify((self.t, self.x, self.p_vect), self.f)

    def get_p0(self):
        return [self.p_dict[key] for key in
            sorted(self.p_dict.keys())]

    def get_x0(self):
        return [self.x0_dict[key] for key in
            sorted(self.x0_dict.keys())]

    def simulate(self, tf=30, dt=0.001, show=False):
        """
        Simulation function.
        """

        p0 = self.get_p0()
        x0 = self.get_x0()

        print('p0', p0)
        print('x0', x0)

        sim = scipy.integrate.ode(self.f_lam)
        sim.set_initial_value(x0, 0)
        sim.set_f_params(p0)

        data = {
            'x': [],
            't': [],
        }

        while  sim.t < tf:
            sim.integrate(sim.t + dt)
            t = sim.t

            # TODO replace hardcoded when statement
            # below
            #velocity = sim.y[0]
            #height = sim.y[1]
            #c = self.p0[0]
            #if velocity < 0 and height < 0:
            #    velocity = -c*velocity
            #    height = 0
            #    sim.set_initial_value([velocity, height], t)

            # data['x'] += [[velocity, height]]
            data['x'] += [sim.y]
            data['t'] += [t]

        pl.plot(data['t'], data['x'])
        if show:
            pl.show()

        return data

if __name__ == "__main__":
    model = Model()
    model.simulate()

#############################################################################