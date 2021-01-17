#!/usr/bin/env python
from math import sin, cos, pi, sqrt
from pathlib import Path

from cairosvg import svg2png
from matplotlib.cm import get_cmap
import numpy as np
import xml.etree.ElementTree as ET


# locations for output files
here = Path(__file__).parent
out_svg = here / 'cover_image.svg'
out_png = here / 'cover_image.png'


# basic static result properties
colormap = get_cmap('viridis')
out_width = 1128
out_height = 191
scale = 10
padding_factor = 1.1


def get_color(x):
    if not (0 <= x <= 1):
        raise ValueError('can only convert values in [0, 1] to colors')
    color_bytes = colormap(x, bytes=True)[:3]
    return f'rgb{color_bytes}'


def get_hexagon(s, t):
    rot_60 = np.array([[cos(pi/3), -sin(pi/3)],
                       [sin(pi/3),  cos(pi/3)]])

    placement_wrt_s = np.array([2*scale*padding_factor, 0])
    placement_wrt_t = rot_60 @ placement_wrt_s

    base_point = placement_wrt_s*s + placement_wrt_t*t

    offset = np.array([scale, scale/sqrt(3)])
    vertices = []
    for _ in range(6):
        vertices.append(base_point + offset)
        offset = rot_60 @ offset

    return ' '.join(f'{x},{y}' for x, y in vertices)


def main():
    # Initialize a blank canvas of the right size.
    svg_root = ET.Element(
        tag='svg',
        attrib={
            'viewBox': f'0 0 {out_width} {out_height}',
            'version': '1.1'
        }
    )
    svg_image = ET.ElementTree(element=svg_root)

    # Add a black background.
    background = ET.SubElement(
        parent=svg_root,
        tag='rect',
        attrib={
            'width': '100%',
            'height': '100%',
            'fill': 'black'
        }
    )

    # Add a grid of hexagons.
    for s in range(-5, 52):
        for t in range(11):
            hexagon = ET.SubElement(
                parent=svg_root,
                tag='polygon',
                attrib={
                    'points': get_hexagon(s, t),
                    'fill': get_color(np.random.rand())
                }
            )

    # Write the result files.
    svg_image.write(
        out_svg,
        encoding='UTF-8',
        xml_declaration=True,
    )
    svg2png(url=str(out_svg), write_to=str(out_png))


if __name__ == '__main__':
    main()
