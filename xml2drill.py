import collections

class Drill():
    Hole = collections.namedtuple('Hole',['type','x','y','drill','extent'])
    Tool = collections.namedtuple('Tool',['nr','drill','is_route','comment'])

    # all values will be saved here in MM (milimeters)
    # but can be exported as INCH (inches)
    available_units = ('INCH', 'MM')
    holes_mm = []

    def import_from_xml(self, xml_content):
        self.holes_mm = [] # reset list
        # keep drill value as string type for a better comparing
        hole = self.Hole(type='via',x=200,y=220,drill='0.7',extent='1-16')
        self.holes_mm.append( hole )
        hole = self.Hole(type='via',x=100,y=110,drill='0.6',extent='1-16')
        self.holes_mm.append( hole )
        hole = self.Hole(type='via',x=300,y=330,drill='0.5',extent='1-16')
        self.holes_mm.append( hole )
        hole = self.Hole(type='via',x=300,y=330,drill='0.6',extent='1-16')
        self.holes_mm.append( hole )
        return True

    def get_header(self, units='INCH'):
        units = units.upper()
        header = []
        header.append(('M71', 'M72')[units == 'INCH'])
        return header

    def get_tools(self, hole_type=[], hole_extent=[]):
        # get tool sizes from holes info
        tools_sizes = [ hole.drill for hole in self.holes_mm ]
        # make it unique
        tools_sizes = list(set(tools_sizes))
        # sort ascending
        tools_sizes = sorted( tools_sizes )
        return tools_sizes

    def get_tools_table(self):
        tools_table = []
        tools_sizes = self.get_tools()
        for id,tool in enumerate(tools_sizes):
            tool = self.Tool(nr=(id+1), drill=tool, is_route=False, comment='')
            tools_table.append( tool )
        return tools_table

    def get_tools_text(self, units='INCH'):
        units = units.upper()
        if units not in self.available_units:
            raise Exception('ERROR: Not recognized units! Please select one from: {}'.format(
                self.available_units))
        tools_table = self.get_tools_table()
        text_output = []
        try:
            for tool in tools_table:
                text_output.append('T{:>02}C{:0.4}'.format(
                    tool.nr,
                    (float(tool.drill),float(tool.drill)/25.4)[units=='INCH'])
                )
        except ValueError:
            return 'ERROR: Some value is not float.', False
        except:
            return 'ERROR: Cannot export tools table.', False
        return text_output, True

    def get_body(self, units='INCH'):
        units = units.upper()
        if units not in self.available_units:
            raise Exception('ERROR: Not recognized units! Please select one from: {}'.format(
                self.available_units))
        return ['X01Y00', 'X02Y22'], True

    def get_body_text(self, units='INCH'):
        return ['X01Y00', 'X02Y22'], True

    def get_excellon_format(self, units='INCH'):
        units = units.upper()
        tools_text, is_success = self.get_tools_text(units)
        if not is_success:
            return tools_text, False
        body_text, is_success = self.get_body_text(units)
        if not is_success:
            return body_text, False
        excellon_output = \
            '\n'.join(self.get_header()) + \
            '\n' + \
            '\n'.join(tools_text) + \
            '\n%\n' + \
            '\n'.join(body_text) + \
            '\nM30\n'
        return excellon_output


if __name__ == "__main__":
    print('This is module only. Try a main program.')
