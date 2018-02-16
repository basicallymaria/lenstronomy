__author__ = 'sibirrer'

import numpy as np
import numpy.testing as npt
import pytest
from lenstronomy.LensModel.Solver.lens_equation_solver import LensEquationSolver
from lenstronomy.LensModel.Solver.solver import Solver
from lenstronomy.LensModel.lens_model import LensModel


class TestSolver4Point(object):

    def setup(self):
        """

        :return:
        """
        pass

    def test_constraint_lensmodel(self):
        lens_model_list = ['SPEP', 'SIS']
        lensModel = LensModel(lens_model_list)
        solver = Solver(solver_type='PROFILE', lensModel=lensModel, num_images=4)

        lensEquationSolver = LensEquationSolver(lensModel)
        sourcePos_x = 0.1
        sourcePos_y = -0.1
        deltapix = 0.05
        numPix = 150
        gamma = 1.9
        kwargs_lens = [{'theta_E': 1., 'gamma': gamma,'q': 0.8, 'phi_G': 0.5, 'center_x': 0.1, 'center_y': -0.1},
                       {'theta_E': 0.1, 'center_x': 0.5, 'center_y': 0}]
        x_pos, y_pos = lensEquationSolver.findBrightImage(sourcePos_x, sourcePos_y, kwargs_lens, numImages=4, min_distance=deltapix, search_window=numPix*deltapix)
        kwargs_lens_init = [{'theta_E': 1.3, 'gamma': gamma,'q': 0.9, 'phi_G': 1.5, 'center_x': 0., 'center_y': 0}, {'theta_E': 0.1, 'center_x': 0.5, 'center_y': 0}]
        kwargs_lens_new, accuracy = solver.constraint_lensmodel(x_pos, y_pos, kwargs_lens_init)

        npt.assert_almost_equal(kwargs_lens_new[0]['theta_E'], kwargs_lens[0]['theta_E'], decimal=3)
        npt.assert_almost_equal(kwargs_lens_new[0]['q'], kwargs_lens[0]['q'], decimal=3)
        npt.assert_almost_equal(kwargs_lens_new[0]['phi_G'], kwargs_lens[0]['phi_G'], decimal=3)
        npt.assert_almost_equal(kwargs_lens_new[0]['center_x'], kwargs_lens[0]['center_x'], decimal=3)
        npt.assert_almost_equal(kwargs_lens_new[0]['center_y'], kwargs_lens[0]['center_y'], decimal=3)

        npt.assert_almost_equal(kwargs_lens_new[0]['theta_E'], 1., decimal=3)
        lensModel = LensModel(lens_model_list=lens_model_list)
        x_source_new, y_source_new = lensModel.ray_shooting(x_pos, y_pos, kwargs_lens_new)
        dist = np.sqrt((x_source_new - x_source_new[0]) ** 2 + (y_source_new - y_source_new[0]) ** 2)
        assert np.max(dist) < 0.000001
        kwargs_ps4 = [{'ra_image': x_pos, 'dec_image': y_pos}]
        kwargs_lens_new = solver.update_solver(kwargs_lens_init, kwargs_ps4)
        npt.assert_almost_equal(kwargs_lens_new[0]['theta_E'], kwargs_lens[0]['theta_E'], decimal=3)
        npt.assert_almost_equal(kwargs_lens_new[0]['q'], kwargs_lens[0]['q'], decimal=3)
        npt.assert_almost_equal(kwargs_lens_new[0]['phi_G'], kwargs_lens[0]['phi_G'], decimal=3)
        npt.assert_almost_equal(kwargs_lens_new[0]['center_x'], kwargs_lens[0]['center_x'], decimal=3)
        npt.assert_almost_equal(kwargs_lens_new[0]['center_y'], kwargs_lens[0]['center_y'], decimal=3)

    def test_add_fixed_lens(self):
        lens_model_list = ['SPEP', 'SHEAR']
        lensModel = LensModel(lens_model_list)

        kwargs_lens_init = [{'theta_E': 1., 'gamma': 2,'q': 0.8, 'phi_G': 0.5, 'center_x': 0.1, 'center_y': -0.1},
                       {'e1': 0.1, 'e2': 0.5}]
        kwargs_fixed_lens_list = [{}, {}]
        solver = Solver(solver_type='PROFILE', lensModel=lensModel, num_images=4)
        kwargs_fixed_lens = solver.add_fixed_lens(kwargs_fixed_lens_list, kwargs_lens_init)
        assert kwargs_fixed_lens[0]['theta_E'] == kwargs_lens_init[0]['theta_E']

        solver = Solver(solver_type='CENTER', lensModel=lensModel, num_images=2)
        kwargs_fixed_lens = solver.add_fixed_lens(kwargs_fixed_lens_list, kwargs_lens_init)
        assert kwargs_fixed_lens[0]['center_x'] == kwargs_lens_init[0]['center_x']

        solver = Solver(solver_type='ELLIPSE', lensModel=lensModel, num_images=2)
        kwargs_fixed_lens = solver.add_fixed_lens(kwargs_fixed_lens_list, kwargs_lens_init)
        assert kwargs_fixed_lens[0]['q'] == kwargs_lens_init[0]['q']

        solver = Solver(solver_type='PROFILE_SHEAR', lensModel=lensModel, num_images=4)
        kwargs_fixed_lens = solver.add_fixed_lens(kwargs_fixed_lens_list, kwargs_lens_init)
        assert kwargs_fixed_lens[0]['center_x'] == kwargs_lens_init[0]['center_x']


if __name__ == '__main__':
    pytest.main()
