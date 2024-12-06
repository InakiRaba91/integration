from manimlib import *

class DerivativeApproximation(Scene):
    def construct(self):
        # Define the function
        def func(x):
            return 2+0.5*x*(x-1)*(x-2)
        
        # Define the derivative approximation function
        def derivative_approx(x, dx):
            return (func(x + dx) - func(x)) / dx

        # Create axes
        axes = Axes(x_range=(-1, 4), y_range=(0, 5), axis_config={"color": BLUE}, width=12, height=6)

        # Create the graph of the function
        graph = axes.get_graph(func, color=YELLOW)

        # Create labels for the axes
        labels = axes.get_axis_labels(x_label_tex="x", y_label_tex="f(x)")
        [label.set_color(YELLOW) for label in labels]

        # Add axes, graph, and labels to the scene
        self.add(axes, graph, labels)

        # Add text label indicating the derivative approximation
        derivative_text = Tex(r"s(x) = \lim_{{\Delta x \to 0}} \frac{{f(x + \Delta x) - f(x)}}{{\Delta x}}")
        derivative_text.set_color(GREEN)
        derivative_text.scale(0.75)
        derivative_text.to_edge(5*UP)
        self.add(derivative_text)

        # Initial dx value
        dx = 1.
        x0 = 2.  # Point at which to approximate the derivative

        # Animate the derivative approximation with decreasing dx
        # Create points at f(x) and f(x + Δx)
        line_x0 = DashedLine(
            start=axes.c2p(x0, 0),
            end=axes.c2p(x0, func(x0)),
            dash_length=0.1,
            color=RED,
            stroke_width=5,
        )
        self.add(line_x0)

        # Add labels below the x-axis
        label_x0 = Tex(f"x=x_0")
        label_x0.set_color(RED).scale(0.75).next_to(axes.c2p(x0, 0), DOWN)
        self.add(label_x0)
        point_f_x = Dot(axes.c2p(x0, func(x0))).set_color(RED)
        label_f_x0 = Tex(f"f(x_0)").set_color(RED).scale(0.75).next_to(point_f_x, UP)
        self.add(label_f_x0)
        self.play(FadeIn(point_f_x))

        for _ in range(5):
            # Calculate the slope of the tangent line
            slope = derivative_approx(x0, dx)
            tangent_line = axes.get_graph(
                lambda x: func(x0) + slope * (x - x0),
                color=GREEN,
                x_range=[x0 - 1, x0 + 1]
            )

            # Create points at f(x + Δx)
            point_f_x_dx = Dot(axes.c2p(x0 + dx, func(x0 + dx))).set_color(BLUE)
            label_f_x0 = Tex(f"f(x_0+\Delta x)").set_color(BLUE).scale(0.75).next_to(point_f_x_dx, 0.5*DOWN + 0.5*RIGHT)
            line_x0_dx = DashedLine(
                start=axes.c2p(x0 + dx, 0),
                end=axes.c2p(x0 + dx, func(x0 + dx)),
                dash_length=0.1,
                color=BLUE,
                stroke_width=5,
            )

            # Add the tangent line and points to the scene
            self.play(ShowCreation(tangent_line), FadeIn(point_f_x_dx), FadeIn(label_f_x0), ShowCreation(line_x0_dx))
            self.wait(1)
            self.remove(tangent_line, point_f_x_dx, label_f_x0, line_x0_dx)
            dx /= 2  # Decrease dx

        # Show final approximation
        final_slope = derivative_approx(x0, dx)
        final_tangent_line = axes.get_graph(
            lambda x: func(x0) + final_slope * (x - x0),
            color=GREEN,
            x_range=[x0 - 1, x0 + 1]
        )
        final_point_f_x = Dot(axes.c2p(x0, func(x0))).set_color(RED)
        final_point_f_x_dx = Dot(axes.c2p(x0 + dx, func(x0 + dx))).set_color(BLUE)
        label_f_x0 = Tex(f"f(x_0+\Delta x)").set_color(BLUE).scale(0.75).next_to(point_f_x, 0.5*DOWN + 0.5*RIGHT)
        final_line_x0_dx = DashedLine(
            start=axes.c2p(x0 + dx, 0),
            end=axes.c2p(x0 + dx, func(x0 + dx)),
            dash_length=0.1,
            color=BLUE,
            stroke_width=5,
        )
        self.play(ShowCreation(final_tangent_line), FadeIn(final_point_f_x), FadeIn(final_point_f_x_dx), FadeIn(label_f_x0), ShowCreation(final_line_x0_dx))
        self.wait(2)

# To render the scene, run the following command in your terminal:
# poetry run manimql derivative.py DerivativeApproximation