#!/usr/bin/env python
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import click
from cairosvg import svg2png
from matplotlib import colormaps

from pattern_generators import random_pattern
from shape import Hexagon, Shape, Triangle

here = Path(__file__).parent
sys.path.insert(0, str(here))

_name_to_shape = {s.__name__: s for s in (Hexagon, Triangle)}

# locations for output files
out_svg = here / 'cover_image.svg'
out_png = here / 'cover_image.png'


# basic static result properties
colormap = colormaps.get_cmap('viridis')


def get_color(x):
    if not (0 <= x <= 1):
        raise ValueError('can only convert values in [0, 1] to colors')
    color_bytes = colormap(x, bytes=True)[:3]
    return f'rgb{color_bytes}'


@click.command()
@click.option(
    '--shape',
    type=click.Choice(tuple(_name_to_shape), case_sensitive=False),
    default='Hexagon'
)
@click.option('--scale', type=float, default=10)
@click.option('--padding_factor', type=float, default=1.1)
@click.option('--width', type=int, default=1128)
@click.option('--height', type=int, default=191)
def main(shape, scale, padding_factor, width, height):
    shape_cls = _name_to_shape[shape]
    shape = shape_cls(scale, padding_factor, width, height)
    _main(shape)


def _main(shape: Shape):
    # Initialize a blank canvas of the right size.
    svg_root = ET.Element(
        'svg',
        attrib={
            'viewBox': f'0 0 {shape.out_width} {shape.out_height}',
            'version': '1.1'
        }
    )
    svg_image = ET.ElementTree(element=svg_root)

    # Add a black background.
    ET.SubElement(
        svg_root,
        'rect',
        attrib={
            'width': '100%',
            'height': '100%',
            'fill': 'black'
        }
    )

    # A pattern defines a mapping from s, t coordinates to [0, 1]
    pattern = random_pattern

    # Add a grid of hexagons.
    for vertices in shape():
        ET.SubElement(
            svg_root,
            'polygon',
            attrib={
                'points': ' '.join(f'{x},{y}' for x, y in vertices),
                'fill': get_color(pattern(*vertices[0]))
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
