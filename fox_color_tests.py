import unittest
from fox_color_ren import *


################################################################################
#
#    Unit Tests
#
################################################################################


class FoxColorTests(unittest.TestCase):

    def _tuples_equal(self, expect, actual):
        self.assertEqual(len(expect), len(actual), msg="expected tuple length did not match actual")

        for i in range(len(expect)):
            self.assertAlmostEqual(expect[i], actual[i], delta=0.01)

    def test_init(self):
        failed = False
        try:
            FoxColor(1.0)
        except Exception:
            failed = True

        self.assertTrue(failed)


class FoxHSLTests(FoxColorTests):

    def test_init_fixes_hue(self):
        target = FoxHSL(720, 1.0, 1.0)
        self.assertEqual(target.hue, 0)
        target = FoxHSL(-359, 1.0, 1.0)
        self.assertEqual(target.hue, 1)

    def test_eq(self):
        target = FoxHSL(0, 1.0, 0.5)
        self.assertEqual(target, FoxHSL(0, 1.0, 0.5))
        self.assertNotEqual(target, FoxHSL(1, 1.0, 0.5))
        self.assertNotEqual(target, FoxHSL(0, 0.0, 0.5))
        self.assertNotEqual(target, FoxHSL(0, 1.0, 1.0))

    def test_init_rejects_non_int_hue(self):
        self.assertRaises(Exception, FoxHSL.__init__, 'apple', 1.0, 1.0)

    def test_init_rejects_non_percent_saturation(self):
        # Non-float value
        self.assertRaises(Exception, FoxHSL.__init__, 13, 'apple', 1.0)
        # Too low
        self.assertRaises(Exception, FoxHSL.__init__, 13, -1.0, 1.0)
        # Too high
        self.assertRaises(Exception, FoxHSL.__init__, 13, 1.1, 1.0)

    def test_init_rejects_non_percent_lightness(self):
        # Non-float value
        self.assertRaises(Exception, FoxHSL.__init__, 13, 0.0, 'apple')
        # Too low
        self.assertRaises(Exception, FoxHSL.__init__, 13, 0.0, -1.0)
        # Too high
        self.assertRaises(Exception, FoxHSL.__init__, 13, 0.0, 1.1)

    def test_init_rejects_non_percent_alpha(self):
        # Non-float value
        self.assertRaises(Exception, FoxHSL.__init__, 13, 0.0, 0.0, 'orange')
        # Too low
        self.assertRaises(Exception, FoxHSL.__init__, 13, 0.0, 0.0, -1.0)
        # Too high
        self.assertRaises(Exception, FoxHSL.__init__, 13, 0.0, 0.0, 10.0)

    def test_hsl_props(self):
        target = FoxHSL(93, 0.14, 0.44, 0.55)
        self.assertEqual(target.hue, 93)
        self.assertEqual(target.saturation, 0.14)
        self.assertEqual(target.lightness, 0.44)
        self.assertEqual(target.alpha, 0.55)

    def test_hsl_setters(self):
        target = FoxHSL(93, 0.14, 0.44, 0.55)
        target.set_hue(99)
        self.assertEqual(target.hue, 99)
        target.set_saturation(0.55)
        self.assertEqual(target.saturation, 0.55)
        target.set_lightness(0.66)
        self.assertEqual(target.lightness, 0.66)
        target.set_alpha(0.77)
        self.assertEqual(target.alpha, 0.77)

    def test_set_hue_fixes_hue(self):
        target = FoxHSL(23, 1.0, 1.0)
        target.set_hue(400)
        self.assertEqual(target.hue, 40)

    def test_set_hue_rejects_non_numeric_inputs(self):
        target = FoxHSL(23, 1.0, 0.0)
        self.assertRaises(Exception, target.set_hue, 'apple')

    def test_set_saturation_rejects_non_percent_values(self):
        target = FoxHSL(23, 1.0, 0.0)
        # non-numeric
        self.assertRaises(Exception, target.set_saturation, 'banana')
        # too low
        self.assertRaises(Exception, target.set_saturation, -0.1)
        # too high
        self.assertRaises(Exception, target.set_saturation, 1.1)

    def test_set_lightness_rejects_non_percent_values(self):
        target = FoxHSL(23, 1.0, 0.0)
        # non-numeric
        self.assertRaises(Exception, target.set_lightness, 'grape')
        # too low
        self.assertRaises(Exception, target.set_lightness, -0.1)
        # too high
        self.assertRaises(Exception, target.set_lightness, 1.1)

    def test_set_alpha_rejects_non_percent_values(self):
        target = FoxHSL(23, 1.0, 0.0)
        # non-numeric
        self.assertRaises(Exception, target.set_alpha, 'potato')
        # too low
        self.assertRaises(Exception, target.set_alpha, -0.1)
        # too high
        self.assertRaises(Exception, target.set_alpha, 1.1)

    def test_rgb_prop(self):
        """
        This method does multiple tests to attempt to hit all the branches in
        the _to_rgb method.
        """
        # < 60
        target = FoxHSL(55, 1.0, 0.5)
        self._tuples_equal((255, 234, 0), target.rgb)

        # < 120
        target = FoxHSL(75, 0.52, 0.19)
        self._tuples_equal((61, 74, 23), target.rgb)

        # < 180
        target = FoxHSL(175, 0.75, 0.5)
        self._tuples_equal((32, 223, 207), target.rgb)

        # < 240
        target = FoxHSL(235, 0.75, 0.5)
        self._tuples_equal((32, 48, 223), target.rgb)

        # < 300
        target = FoxHSL(299, 0.75, 0.5)
        self._tuples_equal((220, 32, 223), target.rgb)

        # < 360
        target = FoxHSL(359, 0.75, 0.5)
        self._tuples_equal((223, 32, 35), target.rgb)

        # Sat == 0
        target = FoxHSL(320, 0, 0.5)
        self._tuples_equal((127, 127, 127), target.rgb)

    def test_rgba_prop(self):
        # Color: #6DAFD0
        target = FoxHSL(200, 0.51, 0.62, 0.33)
        expect = (109, 175, 208, 0.33)
        actual = target.rgba
        self._tuples_equal(expect, actual)

    def test_hsl_prop(self):
        # Color: #92BDB6
        target = FoxHSL(169, 0.25, 0.66)
        expect = (169, 0.25, 0.66)
        actual = target.hsl
        self._tuples_equal(expect, actual)

    def test_hsla_prop(self):
        # Color: #4d4d65
        target = FoxHSL(240, 0.13, 0.35, 0.66)
        expect = (240, 0.13, 0.35, 0.66)
        actual = target.hsla
        self._tuples_equal(expect, actual)

    def test_hsv_prop(self):
        # Color: #A742B6
        target = FoxHSL(292, 0.46, 0.48)
        expect = (292, 0.63, 0.70)
        actual = target.hsv
        self._tuples_equal(expect, actual)

    def test_hsva_prop(self):
        # Color: #6DB540
        target = FoxHSL(97, 0.48, 0.48, 0.5)
        expect = (97, 0.646, 0.71, 0.5)
        actual = target.hsva
        self._tuples_equal(expect, actual)

    def test_to_rgb(self):
        # Color: #9D9001
        target = FoxHSL(55, 0.987, 0.31)
        actual = target.to_rgb()
        self.assertEqual(actual.red, 157)
        self.assertEqual(actual.green, 144)
        self.assertEqual(actual.blue, 1)

    def test_to_hsl(self):
        # Color: #343B29
        target = FoxHSL(83, 0.18, 0.196)
        actual = target.to_hsl()
        self.assertEqual(target.hue, actual.hue)
        self.assertEqual(target.saturation, actual.saturation)
        self.assertEqual(target.lightness, actual.lightness)
        self.assertEqual(target.alpha, actual.alpha)

    def test_to_hsv(self):
        # Color: #3E5F8A
        target = FoxHSL(214, 0.38, 0.392)
        actual = target.to_hsv()
        self.assertEqual(actual.hue, 214)
        self.assertAlmostEqual(actual.saturation, 0.55, delta=0.01)
        self.assertAlmostEqual(actual.value, 0.54, delta=0.01)

    def test_with_hue(self):
        # Color: #C35831
        target = FoxHSL(16, 0.598, 0.478, 0.5)
        actual = target.with_hue(32)
        self.assertEqual(target.hue, 16)
        self.assertEqual(actual.hue, 32)
        self.assertEqual(actual.saturation, 0.598)
        self.assertEqual(actual.lightness, 0.478)
        self.assertEqual(actual.alpha, 0.5)

    def test_with_saturation(self):
        # Color: #C35831
        target = FoxHSL(16, 0.598, 0.478, 0.6)
        actual = target.with_saturation(0.666)
        self.assertEqual(actual.hue, 16)
        self.assertEqual(target.saturation, 0.598)
        self.assertEqual(actual.saturation, 0.666)
        self.assertEqual(actual.lightness, 0.478)
        self.assertEqual(actual.alpha, 0.6)

    def test_with_lightness(self):
        # Color: #C35831
        target = FoxHSL(16, 0.598, 0.478, 0.75)
        actual = target.with_lightness(0.666)
        self.assertEqual(actual.hue, 16)
        self.assertEqual(actual.saturation, 0.598)
        self.assertEqual(target.lightness, 0.478)
        self.assertEqual(actual.lightness, 0.666)
        self.assertEqual(actual.alpha, 0.75)

    def test_with_alpha(self):
        # Color: #C35831
        target = FoxHSL(16, 0.598, 0.478, 0.25)
        actual = target.with_alpha(0.666)
        self.assertEqual(actual.hue, 16)
        self.assertEqual(actual.saturation, 0.598)
        self.assertEqual(actual.lightness, 0.478)
        self.assertEqual(target.alpha, 0.25)
        self.assertEqual(actual.alpha, 0.666)

    def test_with_values(self):
        # Color: #C35831
        target = FoxHSL(16, 0.598, 0.478, 0.25)
        actual = target.with_values(hue=32)
        self.assertEqual(target.hue, 16)
        self.assertEqual(actual.hue, 32)
        actual = target.with_values(saturation=0.666)
        self.assertEqual(target.saturation, 0.598)
        self.assertEqual(actual.saturation, 0.666)
        actual = target.with_values(lightness=0.666)
        self.assertEqual(target.lightness, 0.478)
        self.assertEqual(actual.lightness, 0.666)
        actual = target.with_values(alpha=0.666)
        self.assertEqual(target.alpha, 0.25)
        self.assertEqual(actual.alpha, 0.666)

    def test_hex_prop_no_alpha(self):
        # Color: #AA58C4
        target = FoxHSL(285, 0.49, 0.56)
        self.assertEqual('#aa58c6', target.hex)

    def test_hex_prop_with_alpha(self):
        # Color: #55A752
        target = FoxHSL(118, 0.34, 0.49, 0.5)
        self.assertEqual('#55a7527f', target.hex)

    def test_set_hue(self):
        target = FoxHSL(118, 0.25, 0.5, 0.75)
        target.set_hue(100)
        self.assertEqual(100, target.hue)

        target.set_hue(361)
        self.assertEqual(1, target.hue)

    def test_set_saturation(self):
        target = FoxHSL(118, 0.25, 0.5, 0.75)
        target.set_saturation(1.0)
        self.assertEqual(1.0, target.saturation)

        self.assertRaises(Exception, target.set_saturation, -0.1)
        self.assertRaises(Exception, target.set_saturation, 1.1)

    def test_set_lightness(self):
        target = FoxHSL(118, 0.25, 0.5, 0.75)
        target.set_lightness(1.0)
        self.assertEqual(1.0, target.lightness)

        self.assertRaises(Exception, target.set_lightness, -0.1)
        self.assertRaises(Exception, target.set_lightness, 1.1)

    def test_set_alpha(self):
        target = FoxHSL(118, 0.25, 0.5, 0.75)
        target.set_alpha(1.0)
        self.assertEqual(1.0, target.alpha)

        self.assertRaises(Exception, target.set_alpha, -0.1)
        self.assertRaises(Exception, target.set_alpha, 1.1)


class FoxHSVTests(FoxColorTests):

    def test_rgb_prop(self):
        # Color: #597564
        target = FoxHSV(144, 0.24, 0.46)
        expect = (89, 117, 100)
        actual = target.rgb
        self._tuples_equal(expect, actual)

    def test_rgba_props(self):
        target = FoxHSV(250, 0.75, 0.25, 0.5)
        self._tuples_equal((24, 16, 64, 0.5), target.rgba)

    def test_hsl_prop(self):
        target = FoxHSV(250, 0.75, 0.25)
        self._tuples_equal((250, 0.6, 0.16), target.hsl)

    def test_hsla_prop(self):
        target = FoxHSV(25, 1.0, 0.5, 0.75)
        self._tuples_equal((25, 1.0, 0.25, 0.75), target.hsla)

    def test_hsv_prop(self):
        target = FoxHSV(25, 1.0, 0.5, 0.75)
        self._tuples_equal((25, 1.0, 0.5), target.hsv)

    def test_hsva_prop(self):
        target = FoxHSV(25, 1.0, 0.5, 0.75)
        self._tuples_equal((25, 1.0, 0.5, 0.75), target.hsva)

    def test_to_hsl(self):
        target = FoxHSV(27, 1.0, 0.5, 0.75)
        actual = target.to_hsl()
        expect = FoxHSL(27, 1.0, 0.25, 0.75)
        self.assertEqual(expect, actual)

    def test_to_hsv(self):
        target = FoxHSV(28, 0.75, 0.5, 0.25)
        actual = target.to_hsv()
        self.assertEqual(target, actual)

    def test_to_rgb(self):
        target = FoxHSV(29, 0.75, 0.5, 0.25)
        actual = target.to_rgb()
        expect = FoxRGB(128, 78, 32, 0.25)
        self.assertEqual(expect, actual)

    def test_set_hue(self):
        target = FoxHSV(30, 0.75, 0.5, 0.25)
        target.set_hue(31)
        self.assertEqual(31, target.hue)
        target.set_hue(-1)
        self.assertEqual(359, target.hue)
        target.set_hue(361)
        self.assertEqual(1, target.hue)

    def test_set_saturation(self):
        target = FoxHSV(30, 0.75, 0.5, 0.25)
        target.set_saturation(0.76)
        self.assertEqual(0.76, target.saturation)
        self.assertRaises(Exception, target.set_saturation, -0.1)
        self.assertRaises(Exception, target.set_saturation, 1.1)

    def test_set_value(self):
        target = FoxHSV(30, 0.75, 0.5, 0.25)
        target.set_value(0.76)
        self.assertEqual(0.76, target.value)
        self.assertRaises(Exception, target.set_value, -0.1)
        self.assertRaises(Exception, target.set_value, 1.1)

    def test_with_hue(self):
        target = FoxHSV(22, 0.22, 0.22, 0.22)
        self.assertEqual(FoxHSV(23, 0.22, 0.22, 0.22), target.with_hue(23))

    def test_with_saturation(self):
        target = FoxHSV(22, 0.22, 0.22, 0.22)
        self.assertEqual(FoxHSV(22, 0.23, 0.22, 0.22), target.with_saturation(0.23))

    def test_with_value(self):
        target = FoxHSV(22, 0.22, 0.22, 0.22)
        self.assertEqual(FoxHSV(22, 0.22, 0.23, 0.22), target.with_value(0.23))

    def test_with_alpha(self):
        target = FoxHSV(22, 0.22, 0.22, 0.22)
        self.assertEqual(FoxHSV(22, 0.22, 0.22, 0.23), target.with_alpha(0.23))


class FoxRGBTests(FoxColorTests):

    def test_red_prop(self):
        target = FoxRGB(100, 50, 200)
        self.assertEqual(100, target.red)

    def test_set_red(self):
        target = FoxRGB(100, 50, 200)
        target.set_red(200)
        self.assertEqual(200, target.red)
        self.assertRaises(Exception, target.set_red, -1)
        self.assertRaises(Exception, target.set_red, 256)

    def test_green_prop(self):
        target = FoxRGB(100, 50, 200)
        self.assertEqual(50, target.green)

    def test_set_green(self):
        target = FoxRGB(100, 50, 200)
        target.set_green(100)
        self.assertEqual(100, target.green)
        self.assertRaises(Exception, target.set_green, -1)
        self.assertRaises(Exception, target.set_green, 256)

    def test_blue_prop(self):
        target = FoxRGB(100, 50, 200)
        self.assertEqual(200, target.blue)

    def test_set_blue(self):
        target = FoxRGB(100, 50, 200)
        target.set_blue(50)
        self.assertEqual(50, target.blue)
        self.assertRaises(Exception, target.set_blue, -1)
        self.assertRaises(Exception, target.set_blue, 256)

    def test_rgb_prop(self):
        target = FoxRGB(200, 100, 50)
        self._tuples_equal((200, 100, 50), target.rgb)

    def test_rgba_prop(self):
        target = FoxRGB(255, 155, 55, 0.75)
        self._tuples_equal((255, 155, 55, 0.75), target.rgba)

    def test_hsl_prop(self):
        target = FoxRGB(100, 150, 200)
        self._tuples_equal((210, 0.476, 0.588), target.hsl)

    def test_hsla_prop(self):
        target = FoxRGB(75, 100, 125, 0.75)
        self._tuples_equal((210, 0.25, 0.392, 0.75), target.hsla)

    def test_hsv_prop(self):
        target = FoxRGB(150, 250, 50)
        self._tuples_equal((90, 0.8, 0.98), target.hsv)

    def test_hsva_prop(self):
        target = FoxRGB(125, 225, 25, 0.25)
        self._tuples_equal((90, 0.889, 0.882, 0.25), target.hsva)

    def test_to_rgb(self):
        target = FoxRGB(125, 100, 75, 0.25)
        actual = target.to_rgb()
        self.assertEqual(target.red, actual.red)
        self.assertEqual(target.green, actual.green)
        self.assertEqual(target.blue, actual.blue)
        self.assertEqual(target.alpha, actual.alpha)

    def test_to_hsl(self):
        target = FoxRGB(125, 100, 75, 0.5)
        actual = target.to_hsl()
        self.assertEqual(30, actual.hue)
        self.assertAlmostEqual(0.25, actual.saturation, delta=0.01)
        self.assertAlmostEqual(0.392, actual.lightness, delta=0.01)
        self.assertEqual(0.5, actual.alpha)

    def test_to_hsv(self):
        target = FoxRGB(136, 236, 36, 0.36)
        actual = target.to_hsv()
        self.assertEqual(90, actual.hue)
        self.assertAlmostEqual(0.847, actual.saturation, delta=0.01)
        self.assertAlmostEqual(0.925, actual.value, delta=0.01)
        self.assertEqual(0.36, 0.36)

    def test_eq(self):
        target = FoxRGB(25, 26, 27, 0.25)
        self.assertEqual(target, FoxRGB(25, 26, 27, 0.25))
        self.assertNotEqual(target, FoxRGB(26, 26, 27, 0.25))
        self.assertNotEqual(target, FoxRGB(25, 27, 27, 0.25))
        self.assertNotEqual(target, FoxRGB(25, 26, 28, 0.25))
        self.assertNotEqual(target, FoxRGB(25, 26, 27, 0.24))


class HexToRGBTests(unittest.TestCase):

    def test_invalid_input(self):
        self.assertRaises(Exception, hex_to_fox_rgb, 'hoopla')
        self.assertRaises(Exception, hex_to_fox_rgb, '#22')
        self.assertRaises(Exception, hex_to_fox_rgb, '#xxx')

    def test_full_without_alpha(self):
        target = hex_to_fox_rgb('#181040')
        self.assertEqual(24, target.red)
        self.assertEqual(16, target.green)
        self.assertEqual(64, target.blue)
        self.assertEqual(1.0, target.alpha)

    def test_full_with_alpha(self):
        target = hex_to_fox_rgb('#1810407F')
        self.assertEqual(24, target.red)
        self.assertEqual(16, target.green)
        self.assertEqual(64, target.blue)
        self.assertAlmostEqual(0.5, target.alpha, delta=0.01)

    def test_short_without_alpha(self):
        target = hex_to_fox_rgb('#edc')
        self.assertEqual(target.red, 238)
        self.assertEqual(target.green, 221)
        self.assertEqual(target.blue, 204)
        self.assertEqual(target.alpha, 1.0)

    def test_short_with_alpha(self):
        target = hex_to_fox_rgb('#edcb')
        self.assertEqual(target.red, 238)
        self.assertEqual(target.green, 221)
        self.assertEqual(target.blue, 204)
        self.assertAlmostEqual(target.alpha, 0.7333, delta=0.01)


if __name__ == '__main__':
    unittest.main()