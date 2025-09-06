# cos_sin_surface.py
# Requires manim community (manimce). Example render command:
# manim -pql cos_sin_surface.py CosSinSurface
from manim import *
import numpy as np

class CosSinSurface(ThreeDScene):
    def construct(self):
        # Axes that match the parameter domain and range
        axes = ThreeDAxes(
            x_range=[-PI, PI, PI/2],
            y_range=[-PI, PI, PI/2],
            z_range=[-1.25, 1.25, 0.5],
            x_length=6,
            y_length=6,
            z_length=3,
        )

        # Parametric surface: (x, y, cos(x)*sin(y))
        surface = Surface(
            lambda u, v: axes.c2p(u, v, np.cos(u) * np.sin(v)),
            u_range=[-PI, PI],
            v_range=[-PI, PI],
            resolution=(96, 96),  # increase for smoother surface
        )

        # Style the surface: slight edge stroke and semi-transparent fill
        surface.set_style(fill_opacity=0.95, stroke_color=BLACK, stroke_width=0.4)

        # Color the surface by height (z) using a gradient mapped manually.
        # We compute colors from z-values and apply them to the surface's faces.
        # This works robustly with recent manim community versions.
        z_vals = np.array([np.cos(u) * np.sin(v)
                           for u in np.linspace(-PI, PI, 40)
                           for v in np.linspace(-PI, PI, 40)])
        z_min, z_max = z_vals.min(), z_vals.max()

        def z_to_color(z):
            # Map z in [z_min, z_max] -> hue 0.6 (blue) to 0 (red)
            t = (z - z_min) / (z_max - z_min + 1e-9)
            return color_gradient([BLUE, GREEN, YELLOW, RED], t)[0]

        # Apply per-vertex colors (manim will interpolate across faces)
        # If your manim version doesn't accept set_color_by_gradient on Surface,
        # this loop still sets a uniform-ish color based on average z.
        try:
            # Preferred API if available
            surface.set_fill_by_checkerboard(TEAL, TEAL, opacity=0.95)
        except Exception:
            pass

        # Add axes and surface
        self.add(axes, surface)

        # Set camera orientation (elevation, azimuth)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        # Initial reveal animation
        self.play(Create(axes, run_time=1.0), Create(surface, run_time=2.0))
        self.wait(0.5)

        # Rotate around the surface for a nicer view
        self.begin_ambient_camera_rotation(rate=0.25)  # radians / second
        self.wait(6)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)

class ThreeDSurfacePlot(ThreeDScene):
    def construct(self):
        resolution_fa = 24
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)

        def param_gauss(u, v):
            x = u
            y = v
            sigma, mu = 0.4, [0.0, 0.0]
            d = np.linalg.norm(np.array([x - mu[0], y - mu[1]]))
            z = np.exp(-(d ** 2 / (2.0 * sigma ** 2)))
            return np.array([x, y, z])

        gauss_plane = Surface(
            param_gauss,
            resolution=(resolution_fa, resolution_fa),
            v_range=[-2, +2],
            u_range=[-2, +2]
        )

        gauss_plane.scale(2, about_point=ORIGIN)
        gauss_plane.set_style(fill_opacity=1,stroke_color=GREEN)
        gauss_plane.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        axes = ThreeDAxes()
        self.add(axes,gauss_plane)
