# standard libraries
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable

# third party libraries
import click
import numpy as np
from cairosvg import svg2png
from matplotlib import colormaps

# cover image libraries
from cover_image.pattern_generators import (gaussian_process_pattern,
                                            random_pattern)
from cover_image.shape import Hexagon, Shape, Triangle

_name_to_shape = {s.__name__: s for s in (Hexagon, Triangle)}
_name_to_pattern = {"gaussian_process": gaussian_process_pattern, "random": random_pattern}

# locations for output files
here = Path()
out_svg = here / "cover_image.svg"
out_png = here / "cover_image.png"


# basic static result properties
colormap = colormaps.get_cmap("viridis")


def get_color(x):
    if not (0 <= x <= 1):
        raise ValueError("can only convert values in [0, 1] to colors")
    color_bytes = colormap(x, bytes=True)[:3]
    return f"rgb{color_bytes}"


@click.command()
@click.option("--shape", type=click.Choice(tuple(_name_to_shape), case_sensitive=False), default="Hexagon")
@click.option("--pattern", type=click.Choice(tuple(_name_to_pattern), case_sensitive=False), default="gaussian_process")
@click.option("--scale", type=float, default=10)
@click.option("--padding-factor", type=float, default=1.1)
@click.option("--width", type=int, default=1128)
@click.option("--height", type=int, default=191)
def main(shape, pattern, scale, padding_factor, width, height):
    shape_cls = _name_to_shape[shape]
    shape = shape_cls(scale, padding_factor, width, height)
    pattern = _name_to_pattern[pattern]
    _main(shape, pattern)


def _main(shape: Shape, pattern: Callable):
    # Initialize a blank canvas of the right size.
    svg_root = ET.Element("svg", attrib={"viewBox": f"0 0 {shape.out_width} {shape.out_height}", "version": "1.1"})
    svg_image = ET.ElementTree(element=svg_root)

    # Add a black background.
    ET.SubElement(svg_root, "rect", attrib={"width": "100%", "height": "100%", "fill": "black"})

    # Find a color for each shape.
    shapes = list(shape())
    sample_points = np.vstack([np.mean(s, axis=0) for s in shapes])
    colors = [get_color(v) for v in pattern(sample_points)]

    # Add the shapes.
    for vertices, color in zip(shapes, colors):
        ET.SubElement(
            svg_root,
            "polygon",
            attrib={"points": " ".join(f"{x},{y}" for x, y in vertices), "fill": color},
        )

    # Write the result files.
    svg_image.write(
        out_svg,
        encoding="UTF-8",
        xml_declaration=True,
    )
    svg2png(url=str(out_svg), write_to=str(out_png))


if __name__ == "__main__":
    main()
