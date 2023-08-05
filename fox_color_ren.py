# Copyright 2023 Elizabeth Paige Harper
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# From: https://github.com/Foxcapades/renpy-util-colors

from fox_hex_utils_ren import fox_hex_to_ubytes, fox_ubytes_to_hex
from fox_requirement_ren import fox_require_str

"""renpy
init -2 python:
"""


################################################################################
#
#   Base Classes
#
################################################################################


class FoxColor(object):
    """
    Base type for color classes.

    This type should not be instantiated directly, and attempting to do so will
    raise an exception.
    """

    def __init__(self, alpha: float):
        if self.__class__.__name__ == 'FoxColor':
            raise Exception('FoxColor cannot be constructed directly.')

        self._a: float = self._require_percent('alpha', alpha)

    #  RGB  ####################################################################

    @property
    def rgb(self) -> tuple[int, int, int]:
        """
        :return: Tuple of this color's red, gree, and blue channel values.
        """
        raise Exception("RGB property is not implemented")

    @property
    def rgba(self) -> tuple[int, int, int, float]:
        """
        :return: Tuple of this color's red, green, blue, and alpha channel
        values.
        """
        raise Exception("RGBA property is not implemented")

    #  HSL  ####################################################################

    @property
    def hsl(self) -> tuple[int, float, float]:
        """
        :return: Tuple of this color's hue, saturation, and lightness.
        """
        raise Exception("HSL property is not implemented")

    @property
    def hsla(self) -> tuple[int, float, float, float]:
        """
        :return: Tuple of this color's hue, saturation, lightness, and alpha
        channel values.
        """
        raise Exception("HSLA property is not implemented")

    #  HSV  ####################################################################

    @property
    def hsv(self) -> tuple[int, float, float]:
        """
        :return: Tuple of this color's hue, saturation, and value.
        """
        raise Exception("HSV property is not implemented")

    @property
    def hsva(self) -> tuple[int, float, float, float]:
        """
        :return: Tuple of this color's hue, saturation, value, and alpha channel
        values.
        """
        raise Exception("HSVA property is not implemented")

    #  HEX  ####################################################################

    @property
    def hex(self, include_alpha: bool = True) -> str:
        """
        Returns a hex value of 6 or 8 characters depending on whether this color
        has an alpha channel and the value of the `include_alpha` argument.

        If this color has an alpha value and `include_alpha` is `True` the
        returned hex value will be 8 characters (plus the '#' prefix).

        If this color has no alpha value or `include_alpha` is `False` the
        returned hex value will be 6 characters (plus the '#' prefix).

        :param include_alpha: Whether to include the alpha channel (when
        relevant).

        :return: A hex color string representation of this color.
        """
        if self._a >= 1.0 or not include_alpha:
            return fox_ubytes_to_hex(self.rgb, '#')
        else:
            r, g, b, a = self.rgba
            return fox_ubytes_to_hex((r, g, b, int(a * 255)), '#')

    #  ALPHA  ##################################################################

    @property
    def alpha(self):
        """
        :return: This color's alpha channel as a percent value between `0.0` and
        `1.0` (inclusive).
        """
        return self._a

    def set_alpha(self, alpha: float):
        """
        Updates this FoxColor's alpha value to the given alpha value.

        :param alpha: New alpha value for this FoxColor instance.
        """
        self._require_percent('alpha', alpha)
        self._a = alpha

    # Conversion Methods #######################################################

    def to_rgb(self) -> 'FoxRGB':
        """
        Converts the current color to a FoxRGB instance.  If the color was
        already a FoxRGB instance, that instance will be returned.

        :return: A FoxRGB instance converted from this color.
        """
        raise Exception('to_rgb not yet implemented')

    def to_hsl(self) -> 'FoxHSL':
        """
        Converts the current color to a FoxHSL instance.  If the color was
        already a FoxHSL instance, that instance will be returned.

        :return: A FoxHSL instance converted from this color.
        """
        raise Exception('to_hsl not yet implemented')

    def to_hsv(self) -> 'FoxHSV':
        """
        Converts the current color to a FoxHSV instance.  If the color was
        already a FoxHSV instance, that instance will be returned.
        :return:
        """
        raise Exception('to_hsv not yet implemented')

    #  INTERNALS  ##############################################################

    @staticmethod
    def _require_numeric(name: str, value: int | float):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise Exception(f'{name} must be a numeric value')

    def _require_percent(self, name: str, percent: float) -> float:
        self._require_numeric(name, percent)
        if 0.0 <= percent <= 1.0:
            return percent
        else:
            raise Exception(
                f'{name} must be a percent value between 0.0 and 1.0'
                ' (inclusive)'
            )


################################################################################
#
#   HSL Class
#
################################################################################


class FoxHSL(FoxColor):
    """
    Represents a color stored as hue, saturation, and lightness values.
    """

    def __init__(
        self,
        hue: int,
        saturation: float,
        lightness: float,
        alpha: float = 1.0
    ) -> None:
        """
        Initializes the new FoxHSL instance with the given arguments.

        :param hue: Hue value as an int between 0 and 360 (inclusive).  If the
        given value falls outside of that range it will be 'corrected' to a
        value in that range to allow for negative rotations or over rotations.

        Correction should keep the target hue.

        :param saturation: Saturation value as a percent float between 0.0 and
        1.0 (inclusive).  If this value falls outside of that range an exception
        will be raised.

        :param lightness: Lightness value as a percent float between 0.0 and 1.0
        (inclusive).  If this value falls outside of that range, an exception
        will be raised.

        :param alpha: Alpha value as a percent float between 0.0 and 1.0
        (inclusive).  If this value falls outside of that range, an exception
        will be raised.

        Default = 1.0
        """
        super().__init__(alpha)
        self._h = self._fix_hue(hue)
        self._s = self._require_percent('saturation', saturation)
        self._l = self._require_percent('lightness', lightness)

    def __eq__(self, other) -> bool:
        return (isinstance(other, FoxHSL)
            and other._h == self._h
            and other._s == self._s
            and other._l == self._l
            and other._a == self._a)

    # Hue ######################################################################

    @property
    def hue(self) -> int:
        """
        :return: The hue value.
        """
        return self._h

    def set_hue(self, hue: int):
        """
        Updates this FoxHSL's hue to the given value.

        This value should be between 0 and 360 (inclusive).  If it falls outside
        of that range, the hue will be rotated to be in that range again,
        keeping the correct selection.

        :param hue: New hue value to set on this FoxHSL instance.
        """
        self._h = self._fix_hue(hue)

    # Saturation ###############################################################

    @property
    def saturation(self) -> float:
        """
        :return: The saturation value.
        """
        return self._s

    def set_saturation(self, saturation: float):
        """
        Updates this FoxHSL's saturation the given value.

        :param saturation: New saturation value to set on this FoxHSL instance.
        """
        self._s = self._require_percent('saturation', saturation)

    # Lightness ################################################################

    @property
    def lightness(self) -> float:
        """
        :return: The lightness value.
        """
        return self._l

    def set_lightness(self, lightness: float):
        """
        Updates this FoxHSL's lightness the given value.

        :param lightness: New lightness value to set on this FoxHSL instance.
        """
        self._l = self._require_percent('lightness', lightness)

    # HSL ######################################################################

    @property
    def hsl(self) -> tuple[int, float, float]:
        return self._h, self._s, self._l

    @property
    def hsla(self) -> tuple[int, float, float, float]:
        return self._h, self._s, self._l, self._a

    # HSV ######################################################################

    @property
    def hsv(self) -> tuple[int, float, float]:
        return self._to_hsv()

    @property
    def hsva(self) -> tuple[int, float, float, float]:
        h, s, v = self._to_hsv()
        return h, s, v, self._a

    # RGB ######################################################################

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self._to_rgb()

    @property
    def rgba(self) -> tuple[int, int, int, float]:
        r, g, b = self._to_rgb()
        return r, g, b, self._a

    # Conversion Overrides #####################################################

    def to_rgb(self) -> 'FoxRGB':
        r, g, b = self._to_rgb()
        return FoxRGB(r, g, b, self._a)

    def to_hsl(self) -> 'FoxHSL':
        return self

    def to_hsv(self) -> 'FoxHSV':
        h, s, v = self._to_hsv()
        return FoxHSV(h, s, v, self._a)

    # Creation Methods #########################################################

    def with_hue(self, hue: int) -> 'FoxHSL':
        """
        Creates a new FoxHSL value with the given hue.

        The new value will have the same saturation, lightness, and alpha values
        as the current FoxHSL instance.

        :param hue: Hue value for the new FoxHSL value.

        :return: A new FoxHSL value with the given hue.
        """
        return FoxHSL(hue, self._s, self._l, self._a)

    def with_saturation(self, saturation: float) -> 'FoxHSL':
        """
        Creates a new FoxHSL value with the given saturation.

        The new value will have the same hue, lightness, and alpha values as the
        current FoxHSL instance.

        :param saturation: Saturation value for the new FoxHSL value.

        :return: A new FoxHSL value with the given saturation.
        """
        return FoxHSL(self._h, saturation, self._l, self._a)

    def with_lightness(self, lightness: float) -> 'FoxHSL':
        """
        Creates a new FoxHSL value with the given lightness.

        The new value will have the same hue, saturation, and alpha values as
        the current FoxHSL instance.

        :param lightness: Lightness value for the new FoxHSL value.

        :return: A new FoxHSL value with the given lightness.
        """
        return FoxHSL(self._h, self._s, lightness, self._a)

    def with_alpha(self, alpha: float) -> 'FoxHSL':
        """
        Creates a new FoxHSL value with the given alpha.

        The new value will have the same hue, saturation, and lightness values
        as the current FoxHSL instance.

        :param alpha: Alpha value for the new FoxHSL value.

        :return: A new FoxHSL value with the given alpha.
        """
        return FoxHSL(self._h, self._s, self._l, alpha)

    def with_values(
        self,
        hue: int = None,
        saturation: float = None,
        lightness: float = None,
        alpha: float = None
    ) -> 'FoxHSL':
        """
        Creates a new FoxHSL value with the given hue, saturation, lightness,
        and/or alpha value(s).

        Any values that are not set, or are set to None will be defaulted to
        this FoxHSL instance's value for that field.

        :param hue: Optional hue override for the new FoxHSL instance.  If unset
        or set to None, the new FoxHSL will have this instance's hue value.

        :param saturation: Optional saturation override for the new FoxHSL
        instance.  If unset, or set to None, the new FoxHSL will have this
        instance's saturation value.

        :param lightness: Optional lightness override for the new FoxHSL
        instance.  If unset, or set to None, the new FoxHSL will have this
        instance's lightness value.

        :param alpha: Optional alpha override for the new FoxHSL instance.  If
        unset, or set to None, the new FoxHSL will have this instance's alpha
        value.

        :return: A new FoxHSL instance with the set values or the values from
        the current instance depending on the given arguments.
        """
        h = hue if hue is not None else self._h
        s = saturation if saturation is not None else self._s
        l = lightness if lightness is not None else self._l
        a = alpha if alpha is not None else self._a
        return FoxHSL(h, s, l, a)

    # INTERNALS ################################################################

    def _to_hsv(self):
        v = self._s * min(self._l, 1 - self._l) + self._l
        return self._h, 2 - 2 * self._l / v if v else 0.0, v

    def _to_rgb(self):
        if self._s == 0:
            tmp = int(self._l * 255)
            return tmp, tmp, tmp
        else:
            c = (1 - abs(2 * self._l - 1)) * self._s
            x = c * (1 - abs(((self._h / 60) % 2) - 1))
            m = self._l - c/2

            r = 0.0
            g = 0.0
            b = 0.0

            if self._h < 60:
                r = c
                g = x
                b = 0
            elif self._h < 120:
                r = x
                g = c
                b = 0.0
            elif self._h < 180:
                r = 0.0
                g = c
                b = x
            elif self._h < 240:
                r = 0.0
                g = x
                b = c
            elif self._h < 300:
                r = x
                g = 0.0
                b = c
            elif self._h < 360:
                r = c
                g = 0.0
                b = x

            r = int(round((r + m) * 255))
            g = int(round((g + m) * 255))
            b = int(round((b + m) * 255))

        return r, g, b

    def _fix_hue(self, hue: int) -> int:
        self._require_numeric('hue', hue)

        while hue < 0:
            hue += 360

        while hue > 360:
            hue -= 360

        if hue == 360:
            hue = 0

        return int(hue)


################################################################################
#
#   HSV Classes
#
################################################################################


class FoxHSV(FoxColor):
    """
    Represents a color stored as hue, saturation, and value values.
    """

    def __init__(
        self,
        hue: int,
        saturation: float,
        value: float,
        alpha: float = 1.0,
    ) -> None:
        """
        Initializes the new FoxHSV instance with the given arguments.

        :param hue: Hue value as an int between 0 and 360 (inclusive).  If the
        given value falls outside of that range it will be 'corrected' to a
        value in that range to allow for negative rotations or over rotations.

        Correction should keep the target hue.

        :param saturation: Saturation value as a percent float between 0.0 and
        1.0 (inclusive).  If this value falls outside of that range, an
        exception will be raised.

        :param value: Color value as a percent float between 0.0 and 1.0
        (inclusive).  If this value falls outside of that range, an exception
        will be raised.

        :param alpha: Alpha value as a percent float between 0.0 and 1.0
        (inclusive).  If this value falls outside of that range, an exception
        will be raised.

        Default = 1.0
        """
        super().__init__(alpha)
        self._h = self._fix_hue(hue)
        self._s = self._require_percent('saturation', saturation)
        self._v = self._require_percent('value', value)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, FoxHSV)
            and other._h == self._h
            and other._s == self._s
            and other._v == self._v
            and other._a == self._a
        )

    # Hue ######################################################################

    @property
    def hue(self) -> int:
        """
        :return: The hue value.
        """
        return self._h

    def set_hue(self, hue: int):
        """
        Updates this FoxHSV's hue to the given value.

        This value should be between 0 and 360 (inclusive).  If it falls outside
        of that range, the hue will be rotated to be in that range again,
        keeping the correct selection.

        :param hue: New hue value to set on this FoxHSV instance.
        """
        self._h = self._fix_hue(hue)

    # Saturation ###############################################################

    @property
    def saturation(self) -> float:
        """
        :return: The saturation value.
        """
        return self._s

    def set_saturation(self, saturation: float):
        """
        Updates this FoxHSV's saturation to the given value.

        :param saturation: New saturation value to set on this FoxHSV instance.
        """
        self._s = self._require_percent('saturation', saturation)

    # Value ####################################################################

    @property
    def value(self) -> float:
        """
        :return: The color value.
        """
        return self._v

    def set_value(self, value: float):
        """
        Updates this FoxHSV's color value to the given value.

        :param value: New color value to set on this FoxHSV instance.
        """
        self._v = self._require_percent('value', value)

    # HSV ######################################################################

    @property
    def hsv(self) -> tuple[int, float, float]:
        return self._h, self._s, self._v

    @property
    def hsva(self) -> tuple[int, float, float, float]:
        return self._h, self._s, self._v, self._a

    # HSL ######################################################################

    @property
    def hsl(self) -> tuple[int, float, float]:
        return self._to_hsl()

    @property
    def hsla(self) -> tuple[int, float, float, float]:
        h, s, l = self._to_hsl()
        return h, s, l, self._a

    # RGB ######################################################################

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self._to_rgb()

    @property
    def rgba(self) -> tuple[int, int, int, float]:
        r, g, b = self._to_rgb()
        return r, g, b, self._a

    # Conversion Methods #######################################################

    def to_hsv(self) -> 'FoxHSV':
        return self

    def to_hsl(self) -> 'FoxHSL':
        h, s, l = self._to_hsl()
        return FoxHSL(h, s, l, self._a)

    def to_rgb(self) -> 'FoxRGB':
        r, g, b = self._to_rgb()
        return FoxRGB(r, g, b, self._a)

    # Copy Methods #############################################################

    def with_hue(self, hue: int) -> 'FoxHSV':
        """
        Creates a new FoxHSV value with the given hue.

        The new value will have the same saturation, value, and alpha values as
        the current FoxHSV instance.

        :param hue: Hue value for the new FoxHSV instance.

        :return: A new FoxHSV instance with the given hue.
        """
        return FoxHSV(hue, self._s, self._v, self._a)

    def with_saturation(self, saturation: float) -> 'FoxHSV':
        """
        Creates a new FoxHSV value with the given saturation.

        The new instance will have the same hue, value, and alpha values as the
        current FoxHSV instance.

        :param saturation: Saturation value for the new FoxHSV instance.

        :return: A new FoxHSV instance with the given saturation.
        """
        return FoxHSV(self._h, saturation, self._v, self._a)

    def with_value(self, value: float) -> 'FoxHSV':
        """
        Creates a new FoxHSV instance with the given color value.

        The new instance will have the same hue, saturation, and alpha values as
        the current FoxHSV instance.

        :param value: Color value for the new FoxHSV instance.

        :return: A new FoxHSV instance with the given color value.
        """
        return FoxHSV(self._h, self._s, value, self._a)

    def with_alpha(self, alpha: float) -> 'FoxHSV':
        """
        Creates a new FoxHSV instance with the given alpha.

        The new instance will have the same hue, saturation, and color value as
        the current FoxHSV instance.

        :param alpha: Alpha for the new FoxHSV instance.

        :return: A new FoxHSV instance with the given alpha.
        """
        return FoxHSV(self._h, self._s, self._v, alpha)

    def with_values(
        self,
        hue: int = None,
        saturation: float = None,
        value: float = None,
        alpha: float = None,
    ) -> 'FoxHSV':
        """
        Creates a new FoxHSV instance with the given hue, saturation, value
        and/or alpha.

        Any values that are not set, or are set to None will be defaulted to
        this FoxHSV instance's value for that field.

        :param hue: Optional hue override for the new FoxHSV instance.  If
        unset, or set to None, the new FoxHSV instance will have this instance's
        hue.

        :param saturation: Optional saturation override for the new FoxHSV
        instance.  If unset, or set to None, the new FoxHSV will have this
        instance's saturation.

        :param value: Optional value override for the new FoxHSV instance.  If
        unset, or set to None, the new FoxHSV will have this instance's value.

        :param alpha: Optional alpha override for the new FoxHSV instance.  If
        unset, or set to None, the new FoxHSV instance will have this instance's
        alpha.

        :return: A new FoxHSV instance with the set values or values from the
        current instance depending on the given arguments.
        """
        h = hue if hue is not None else self._h
        s = saturation if saturation is not None else self._s
        v = value if value is not None else self._v
        a = alpha if alpha is not None else self._a
        return FoxHSV(h, s, v, a)

    # Internals ################################################################

    def _to_hsl(self) -> tuple[int, float, float]:
        l = self._v - self._v * self._s / 2
        m = min(l, 1 - l)
        return self._h, (self._v - l) / m if m else 0.0, l

    def _to_rgb(self) -> tuple[int, int, int]:
        def f(n):
            k = (n + self._h / 60) % 6
            return int(round(255 * (self._v - self._v * self._s * max(0, min(k, 4 - k, 1)))))
        return f(5), f(3), f(1)

    def _fix_hue(self, hue: int) -> int:
        self._require_numeric('hue', hue)

        while hue < 0:
            hue += 360

        while hue > 360:
            hue -= 360

        if hue == 360:
            hue = 0

        return int(hue)


################################################################################
#
#   RGB Class
#
################################################################################


class FoxRGB(FoxColor):
    """
    Represents a color stored as red, green, and blue channel values.
    """

    def __init__(
        self,
        red: int,
        green: int,
        blue: int,
        alpha: float = 1.0,
    ) -> None:
        """
        Initializes the new FoxRGB instance with the given arguments.

        :param red: Red value as an int between 0 and 255 (inclusive).  If the
        given value falls outside of that range, an exception will be raised.

        :param green: Green value as an int between 0 and 255 (inclusive).  If
        the given value falls outside of that range, an exception will be
        raised.

        :param blue: Blue value as an int between 0 and 255 (inclusive).  If the
        given value falls outside of that range, an exceptions will be raised.

        :param alpha: Alpha value as a percent float between 0.0 and 1.0
        (inclusive).  If this value falls outside of that range, an exception
        will be raised.
        """
        super().__init__(alpha)
        self._r: int = self._require_rgb('red', red)
        self._g: int = self._require_rgb('green', green)
        self._b: int = self._require_rgb('blue', blue)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, FoxRGB)
            and other._r == self._r
            and other._g == self._g
            and other._b == self._b
            and other._a == self._a
        )

    # Red ######################################################################

    @property
    def red(self) -> int:
        """
        :return: The red channel value.
        """
        return self._r

    def set_red(self, red: int):
        """
        Updates this FoxRGB's red channel to the given value.

        :param red: The new red channel value to set on this FoxRGB instance.
        """
        self._r = self._require_rgb('red', red)

    # Green ####################################################################

    @property
    def green(self) -> int:
        """
        :return: The green channel value.
        """
        return self._g

    def set_green(self, green: int):
        """
        Updates this FoxRGB's green channel to the given value.

        :param green: The new green channel value to set on this FoxRGB
        instance.
        """
        self._g = self._require_rgb('green', green)

    # Blue #####################################################################

    @property
    def blue(self) -> int:
        """
        :return: The blue channel value.
        """
        return self._b

    def set_blue(self, blue: int):
        """
        Updates this FoxRGB's blue channel to the given value.

        :param blue: The new blue channel value to set on this FoxRGB instance.
        """
        self._b = self._require_rgb('blue', blue)

    # RGB ######################################################################

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self._r, self._g, self._b

    @property
    def rgba(self) -> tuple[int, int, int, float]:
        return self._r, self._g, self._b, self._a

    # HSL ######################################################################

    @property
    def hsl(self) -> tuple[int, float, float]:
        return self._to_hsl()

    @property
    def hsla(self) -> tuple[int, float, float, float]:
        h, s, l = self._to_hsl()
        return h, s, l, self._a

    # HSV ######################################################################

    @property
    def hsv(self) -> tuple[int, float, float]:
        return self._to_hsv()

    @property
    def hsva(self) -> tuple[int, float, float, float]:
        h, s, v = self._to_hsv()
        return h, s, v, self._a

    # Type Conversions #########################################################

    def to_rgb(self) -> 'FoxRGB':
        return self

    def to_hsl(self) -> FoxHSL:
        h, s, l = self._to_hsl()
        return FoxHSL(h, s, l, self._a)

    def to_hsv(self) -> FoxHSV:
        h, s, v = self._to_hsv()
        return FoxHSV(h, s, v, self._a)

    # Creation Methods #########################################################

    def with_red(self, red: int) -> 'FoxRGB':
        """
        Creates a new FoxRGB instance with the given red value.

        The new value will have the same green, blue, and alpha values as the
        current FoxRGB instance.

        :param red: Red value for the new FoxRGB instance.

        :return: A new FoxRGB instance with the given red value.
        """
        return FoxRGB(red, self._g, self._b, self._a)

    def with_green(self, green: int) -> 'FoxRGB':
        """
        Creates a new FoxRGB instance with the given green value.

        The new value will have the same red, blue, and alpha values as the
        current FoxRGB instance.

        :param green: Green value for the new FoxRGB instance.

        :return: A new FoxRGB instance with the given green value.
        """
        return FoxRGB(self._r, green, self._b, self._a)

    def with_blue(self, blue: int) -> 'FoxRGB':
        """
        Creates a new FoxRGB instance with the given blue value.

        The new value will have the same red, green, and alpha values as the
        current FoxRGB instance.

        :param blue: Blue value for the new FoxRGB instance.

        :return: A new FoxRGB instance with the given blue value.
        """
        return FoxRGB(self._r, self._g, blue, self._a)

    def with_alpha(self, alpha: float) -> 'FoxRGB':
        """
        Creates a new FoxRGB instance with the given alpha value.

        The new value will have the same red, green, and blue values as the
        current FoxRGB instance.

        :param alpha: Alpha value for the new FoxRGB instance.

        :return: A new FoxRGB instance with the given alpha value.
        """
        return FoxRGB(self._r, self._g, self._b, alpha)

    def with_values(
        self,
        red: int = None,
        green: int = None,
        blue: int = None,
        alpha: float = None
    ) -> 'FoxRGB':
        """
        Creates a new FoxRGB instance with the given red, green, blue, and/or
        alpha value(s).

        Any values that are not set, or are set to None will be defaulted to
        this FoxRGB instance's value for that field.

        :param red: Optional red value override for the new FoxRGB instance.  If
        unset, or set None, the new FoxRGB instance will have this instance's
        red value.

        :param green: Optional green value override for the new FoxRGB instance.
        If unset, or set to None, the new FoxRGB instance will have this
        instance's green value.

        :param blue: Optional blue value override for the new FoxRGB instance.
        If unset, or set to None, the new FoxRGB instance will have this
        instance's blue value.

        :param alpha: Optional alpha override for the new FoxRGB instance.  If
        unset, or set to None, the new FoxRGB instance will have this instance's
        alpha value.

        :return: A new FoxRGB instance with the set values or values from the
        current instance depending on the given arguments.
        """
        r = red if red is not None else self._r
        g = green if green is not None else self._g
        b = blue if blue is not None else self._b
        a = alpha if alpha is not None else self._a
        return FoxRGB(r, g, b, a)

    # Internal Methods #########################################################

    def _to_hsv(self) -> tuple[int, float, float]:
        r = self._r / 255
        g = self._g / 255
        b = self._b / 255

        v = max(r, g, b)
        c = v - min(r, g, b)

        if c == 0:
            h = 0
        elif v == r:
            h = (g - b) / c
        elif v == g:
            h = 2 + (b - r) / c
        elif v == b:
            h = 4 + (r - g) / c
        else:
            raise Exception('illegal state')

        h = 60 * ((h + 6) if h < 0 else h)
        s = c / v if v != 0 else 0

        return int(round(h)), s, v

    def _to_hsl(self) -> tuple[int, float, float]:
        r = self._r / 255
        g = self._g / 255
        b = self._b / 255

        a = max(r, g, b)
        i = min(r, g, b)

        l = (a + i) / 2
        d = a - i

        s = 0.0
        if d != 0:
            s = d / (1 - abs(2 * l - 1))

        h = 0.0
        if d > 0:
            if a == r:
                h = ((g - b) / d) % 6
            elif a == g:
                h = 2 + (b - r) / d
            elif a == b:
                h = 4 + (r - g) / d
            else:
                raise Exception("illegal state")
        h *= 60

        return int(round(h)), s, l

    def _require_rgb(self, name: str, color: int) -> int:
        self._require_numeric(name, color)
        if color < 0:
            raise Exception(f'rgb color value {name} was less than 0')
        elif color > 255:
            raise Exception(f'rgb color value {name} was greater than 255')
        else:
            return int(color)


################################################################################
#
#   Public Functions
#
################################################################################


def hex_to_fox_rgb(rgb_hex: str) -> FoxRGB:
    """
    Hex to FoxRGB.  Coverts the given rgb_hex value into a FoxRGB instance by
    parsing the hex code into red, green, blue, and optionally alpha channels.

    If the given hex string is not a valid color hex string value in one of the
    following valid formats, an exception will be raised.  Note for each of the
    valid formats below, the actual hex digits will be replaced with `r`, `g`,
    `b`, or an optional `a` character.  In practice, valid hex digits will be
    expected.

    Valid formats:

    * '#rgb'
    * '#rgba'
    * '#rrggbb'
    * '#rrggbbaa'

    :param rgb_hex: Hex color string to parse.

    :return: A FoxRGB instance parsed from the given hex color string.
    """
    fox_require_str('hex', rgb_hex)

    if not rgb_hex.startswith('#'):
        raise Exception(
            'given rgb_hex value was not a valid hex color string as it did not'
            ' start with a "#" character'
        )

    rgb_hex = rgb_hex[1:]

    l = len(rgb_hex)

    if l == 3 or l == 4:
        rgb_hex = __fox_expand_hex_color(rgb_hex)
    elif l == 6 or l == 8:
        pass
    else:
        raise Exception(
            'given rgb_hex value was not a valid hex color string as it was not'
            ' 3, 4, 6, or 8 hex characters'
        )

    bytes = fox_hex_to_ubytes(rgb_hex)

    l = len(bytes)

    if l == 3:
        return FoxRGB(bytes[0], bytes[1], bytes[2])
    elif l == 4:
        return FoxRGB(bytes[0], bytes[1], bytes[2], bytes[3] / 255)
    else:
        raise Exception('illegal state')


################################################################################
#
#   Internal Functions
#
################################################################################


def __fox_expand_hex_color(rgb_hex: str) -> str:
    out = ''

    for c in rgb_hex:
        out += c + c

    return out
