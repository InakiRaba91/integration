from manimlib import *

class IntegralApproximation(Scene):
    def construct(self):
        # Define the function
        def func(x):
            return 2+0.5*x*(x-1)*(x-2)
        integral_x_range = (0.5, 3)

        # Create axes
        axes = Axes(x_range=(-1, 4), y_range=(0, 5), axis_config={"color": BLUE}, width=12, height=6)

        # Create the graph of the function
        graph = axes.get_graph(func, color=YELLOW)

        # Create labels for the axes
        labels = axes.get_axis_labels(x_label_tex="x", y_label_tex="f(x)")
        [label.set_color(YELLOW) for label in labels]

        # Add axes, graph, and labels to the scene
        self.add(axes, graph, labels)

        # Add limits to the integral
        for x, x_alias in zip(integral_x_range, ("a", "b")):
            limit = DashedLine(
                start=axes.c2p(x, 0),
                end=axes.c2p(x, func(x)),
                dash_length=0.1,
                color=RED,
                stroke_width=7,
            )
            self.add(limit)
            # Add labels below the x-axis
            label = Tex(f"x={x_alias}").set_color(RED).scale(0.75).next_to(axes.c2p(x, 0), DOWN)
            self.add(label)
        
        # Add text label indicating the area under the curve is the integral of f(x)
        integral_text = Tex(r"A(x) = \int_{a}^{b} f(x) \, dx")
        integral_text.set_color(GREEN)
        integral_text.scale(0.75)
        integral_text.to_edge(6*UP)
        self.add(integral_text)

        # Initial dx value
        dx = 0.5

        # Animate the rectangles with decreasing dx
        for _ in range(5):
            rectangles = axes.get_riemann_rectangles(
                graph,
                x_range=integral_x_range,
                dx=dx,
                stroke_width=2,
                stroke_color=GREEN,
                stroke_background=False
            )
            self.play(ShowCreation(rectangles))
            self.wait(1)
            self.remove(rectangles)
            dx /= 2  # Decrease dx

        # Show final approximation
        final_rectangles = axes.get_riemann_rectangles(
            graph,
            x_range=integral_x_range,
            dx=dx,
            stroke_width=0.1,
            stroke_color=WHITE,
            stroke_background=False
        )
        self.play(ShowCreation(final_rectangles))
        self.wait(2)

# To render the scene, run the following command in your terminal:
# poetry run manimql integral.py IntegralApproximation