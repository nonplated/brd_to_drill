import unittest
import geomath
import random

class TestGeomath(unittest.TestCase):

	def test_calculate_azimuth(self):
		result = geomath.calculate_azimuth(0, 0, 1, 1)
		self.assertEqual( round(result,5), 50 )

		result = geomath.calculate_azimuth(0, 0, -999, 999)
		self.assertEqual( round(result,5), 350 )

		result = geomath.calculate_azimuth(-1000, -1000, 0, -1000)
		self.assertEqual( round(result,5), 100 )


	def test_cross(self):
		'''
			We will set return values from one function to another function,
			which should return our starting values with lost some accuracy.
		'''
		random.seed()

		max_loop_number = 10000
		max_range = 10 ** 3 # max_range > 10**3 will produce rounding accuracy errors
		accuracy_decimal = 0 # need to round some values to compare

		for ii in range(max_loop_number):
			# get random coords
			x1 = random.random() * max_range - max_range
			y1 = random.random() * max_range - max_range
			x2 = random.random() * max_range - max_range
			y2 = random.random() * max_range - max_range

			# calculate azimuth
			az = geomath.calculate_azimuth(x1, y1, x2, y2)

			# calculate length between points
			lg = geomath.calculate_length(x1, y1, x2, y2)

			# try to calcalute point x1,y1 from beginnings
			new_x1, new_y1 = geomath.calculate_point_by_azimuth(x2, y2, az+200, lg)
			self.assertEqual( round(new_x1, accuracy_decimal), round(x1, accuracy_decimal))
			self.assertEqual( round(new_y1, accuracy_decimal), round(y1, accuracy_decimal))

			# try to calcalute point x2,y2 from beginnings
			new_x2, new_y2 = geomath.calculate_point_by_azimuth(x1, y1, az, lg)
			self.assertEqual( round(new_x2, accuracy_decimal), round(x2, accuracy_decimal))
			self.assertEqual( round(new_y2, accuracy_decimal), round(y2, accuracy_decimal))


