from calendar import c
from ctypes import c_ubyte
from manimlib import *

class Ambiguity(Scene):
    def construct(self):
        # Define the function
        def func(x, c):
            return 2 * x + 0.5 * np.sin(2 * x) + c
        
        # Define the derivative of the function
        def derivative(x):
            return 2 + np.cos(2 * x)
        
        a, b = -1, 3

        # Create axes
        axes_func = Axes(x_range=(a, b), y_range=(0, 5), axis_config={"color": BLUE}, width=12, height=3)
        axes_deriv = Axes(x_range=(a, b), y_range=(-1, 5), axis_config={"color": BLUE}, width=12, height=3)

        # Position the graphs on top of each other
        graphs = VGroup(axes_func, axes_deriv).arrange(DOWN, buff=1).stretch_to_fit_width(12)

        # Create axes function graph
        graph_func = axes_func.get_graph(lambda x: func(x, 0), color=YELLOW)

        c_init, c_lower, c_upper = 0, -1, 1
        c_tracker = ValueTracker(c_init)
        graph_func = always_redraw(lambda: axes_func.get_graph(lambda x: func(x, c_tracker.get_value()), color=YELLOW))
        labels_func = axes_func.get_axis_labels(x_label_tex="x", y_label_tex="f(x)").set_color(YELLOW) 

        # Create derivative graph
        graph_deriv = axes_deriv.get_graph(derivative, color=PINK)
        labels_deriv = axes_deriv.get_axis_labels(x_label_tex="x", y_label_tex="s(x)").set_color(PINK)

        # Group the axes and graphs together
        func_group = VGroup(graph_func, labels_func)
        deriv_group = VGroup(graph_deriv, labels_deriv)

        # Add the groups to the scene
        self.add(graphs, func_group, deriv_group)

        # Evolving part
        self.play(c_tracker.animate.set_value(c_upper), run_time=1, rate_func=linear)
        self.play(c_tracker.animate.set_value(c_lower), run_time=2, rate_func=linear)
        self.play(c_tracker.animate.set_value(c_init), run_time=1, rate_func=linear)
        self.wait(1)

# To render the scene, run the following command in your terminal:
# poetry run manimql integrating_slope.py IntegratingSlope