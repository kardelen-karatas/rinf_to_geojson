from collections import namedtuple
import xml.etree.ElementTree as ET
import json
import geojson
from geojson import LineString, GeometryCollection
tree = ET.parse('RINFsol_lux_mal_nor.xml')

section_of_lines = tree.findall('.//SectionOfLine')
operational_points = tree.findall('.//OperationalPoint')

SectionOfLine = namedtuple('SectionOfLine', ['start', 'end'])

section_of_lines_aggr = {}
line_strings = []

for section in section_of_lines:
    
    sol = SectionOfLine(
        start={'id': section.find('SOLOPStart').get('Value')},
        end={'id': section.find('SOLOPEnd').get('Value')}
    )
    start_op_point = tree.find('.//OperationalPoint/UniqueOPID[@Value="%s"]/...' % sol.start['id'])
    end_op_point = tree.find('.//OperationalPoint/UniqueOPID[@Value="%s"]/...' % sol.end['id'])
    if start_op_point == None or end_op_point == None:
        print('no start or end op point for section of line: %s' % sol)
        continue

    start_op_point_coords = start_op_point.find('OPGeographicLocation')
    end_op_point_coords = start_op_point.find('OPGeographicLocation')

    sol.start['coords'] = (float(start_op_point_coords.get('Longitude').replace(',', '.')), float(start_op_point_coords.get('Latitude').replace(',', '.')))
    sol.end['coords'] = (float(end_op_point_coords.get('Longitude').replace(',', '.')), float(end_op_point_coords.get('Latitude').replace(',', '.')))
    line_strings.append(LineString([sol.start['coords'], sol.end['coords']]))

geometry_collection = GeometryCollection(line_strings)
print(geojson.dumps(geometry_collection))
