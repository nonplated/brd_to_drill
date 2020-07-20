import collections
import xml.etree.ElementTree as ET
from geomath import calculate_azimuth, calculate_point_by_azimuth, calculate_length


class Drill():
    Hole = collections.namedtuple(
        'Hole', ['type', 'x', 'y', 'drill', 'extent'])
    Tool = collections.namedtuple(
        'Tool', ['nr', 'drill', 'is_route', 'comment'])
    Element = collections.namedtuple(
        'Element', ['package', 'x', 'y', 'rot'])

    # all values will be saved here in MM (milimeters)
    # but can be exported as INCH (inches)
    available_units = ('INCH', 'MM')
    _default_units = self.available_units[0]
    _holes_mm = []

    def count_all_holes(self):
        return len(self._holes_mm)

    def import_from_xml(self, xml_filename):
        self._holes_mm = []  # reset list
        elements = []

        tree = ET.parse(xml_filename)
        root = tree.getroot()

        for child in root.iter('element'):
            element = self.Element(
                package=child.attrib.get('package'),
                x=float(child.attrib.get('x')),
                y=float(child.attrib.get('y')),
                rot=child.attrib.get('rot')
            )
            elements.append(element)

        for child in root.iter('via'):
            attr = child.attrib
            hole = self.Hole(
                type='via',
                x=float(attr.get('x')),
                y=float(attr.get('y')),
                drill=attr.get('drill'),
                extent=attr.get('extent')
            )
            self._holes_mm.append(hole)

        for child in root.iter('hole'):
            attr = child.attrib
            hole = self.Hole(
                type='hole',
                x=float(attr.get('x')),
                y=float(attr.get('y')),
                drill=attr.get('drill'),
                extent=attr.get('extent')
            )
            self._holes_mm.append(hole)

        for e in elements:
            for pad in root.findall('.//package[@name="'+e.package+'"]/pad'):
                attr = pad.attrib
                if attr.get('drill'):
                    if e.rot:  # if rotation is needed
                        az = calculate_azimuth(
                            e.x,
                            e.y,
                            e.x + float(attr.get('x')),
                            e.y + float(attr.get('y'))
                        )
                        lg = calculate_length(
                            e.x,
                            e.y,
                            e.x + float(attr.get('x')),
                            e.y + float(attr.get('y'))
                        )
                        rotation_degrees = int(e.rot[1:])
                        if e.rot[0] == 'R':  # left rotation!
                            rotation_grads = - rotation_degrees / 0.9
                        else:
                            rotation_grads = rotation_degrees / 0.9

                        new_az = az + rotation_grads
                        new_x, new_y = calculate_point_by_azimuth(
                            e.x, e.y, az + rotation_grads, lg
                        )
                    else:
                        new_x = e.x
                        new_y = e.y

                    hole = self.Hole(
                        type='pad',
                        x=new_x,
                        y=new_y,
                        drill=attr.get('drill'),
                        extent=attr.get('extent')
                    )
                    self._holes_mm.append(hole)

        return True

    def get_excellon_format(self, units_header=self._default_units, units_body=self._default_units):
        self._check_units(units_header)
        self._check_units(units_body)
        tools_list, is_success = self._get_tools_list(units_header)
        if not is_success:
            return tools_list, False
        body_list, is_success = self._get_body_list(units_body)
        if not is_success:
            return body_list, False
        excellon_output = \
            '\n'.join(self._get_header_list()) + \
            '\n' + \
            '\n'.join(tools_list) + \
            '\n%\n' + \
            '\n'.join(body_list) + \
            '\nM30\n'
        return excellon_output

    def _get_header_list(self, units='INCH'):
        units = units.upper()
        header = []
        header.append(('M71', 'M72')[units == 'INCH'])
        header.append('M48')
        return header

    def _get_tools(self, hole_type=[], hole_extent=[]):
        # get tool sizes from holes info
        tools_sizes = [hole.drill for hole in self._holes_mm]
        # make it unique
        tools_sizes = list(set(tools_sizes))
        # sort ascending
        tools_sizes = sorted(tools_sizes)
        return tools_sizes

    def _get_tools_table(self):
        tools_table = []
        tools_sizes = self._get_tools()
        for id, tool in enumerate(tools_sizes):
            tool = self.Tool(nr=(id+1), drill=tool, is_route=False, comment='')
            tools_table.append(tool)
        return tools_table

    def _check_units(self, units):
        if units.upper() not in self.available_units:
            raise Exception('[ ERROR ] --- Not recognized units! Please select one from: {}'.format(
                self.available_units))
        return True

    def _get_tools_list(self, units=self._default_units):
        self._check_units(units)
        tools_table = self._get_tools_table()
        output = []
        try:
            for tool in tools_table:
                output.append('T{:>02}C{:0.4}'.format(
                    tool.nr,
                    (float(tool.drill), float(tool.drill)/25.4)[units == 'INCH'])
                )
        except ValueError:
            return '[ ERROR ] --- Some value is not float.', False
        except:
            return '[ ERROR ] --- Cannot export tools table.', False
        return output, True

    def _get_body_list(self, units=self._default_units):
        self._check_units(units)
        tools_table = self._get_tools_table()
        output = []
        for tool in tools_table:
            holes = [hole
                     for hole in self._holes_mm
                     if hole.drill == tool.drill]
            output.append('T{:02d}'.format(int(tool.nr)))
            for h in holes:
                if units.upper() == 'INCH':
                    output.append(
                        self._get_formatted_coords(
                            h.x/25.4, h.y/25.4, 2, 4)
                        )
                else:
                    output.append(
                        self._get_formatted_coords(
                            h.x, h.y, 4, 2)
                        )
        return output, True

    def _get_formatted_value(self, value, leading_zeros, trailing_zeros):
        # in real you dont need the bigger values than {:0=13.6f}
        v = '{:0=18.10f}'.format(float(value)).partition('.')
        a = v[0][-leading_zeros:]
        b = v[2][:trailing_zeros]
        if float(value) < 0:
            a = '-'+a
        # this is important check, we dont cut leading number
        c = int(a)
        d = int(v[0])
        assert c == d
        return '{:s}{:s}'.format(a, b)

    def _get_formatted_coords(self, x, y, leading_zeros, trailing_zeros):
        new_coords = 'X{}Y{}'.format(
            self._get_formatted_value(x, leading_zeros, trailing_zeros),
            self._get_formatted_value(y, leading_zeros, trailing_zeros)
        )
        return new_coords


if __name__ == "__main__":
    print('This is a module only. Run the main program.')
