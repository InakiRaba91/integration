from manimlib import *

class IntegratingSlope(Scene):
    def add_interval(self, xt, dx, axes_func, func, axes_deriv, graph_deriv, label_x):
        epsilon = 1e-3
        # Progress line
        progress_line_xt_dx = DashedLine(axes_deriv.c2p(xt+dx, 0), axes_func.c2p(xt+dx, func(xt+dx)), color=WHITE)
        self.add(progress_line_xt_dx)
        if label_x is None:
            label_x = Tex(f"x").set_color(WHITE).scale(0.75).next_to(axes_deriv.c2p(xt+dx, 0), DOWN)
            self.add(label_x)
        else:
            self.play(label_x.animate.shift(axes_func.c2p(dx, 0) - axes_func.c2p(0, 0)))

        # Rectangle
        rectangles = axes_deriv.get_riemann_rectangles(graph_deriv, x_range=(xt, xt+dx-epsilon), dx=dx, stroke_background=False, fill_opacity=0.5, colors=(PURPLE, PURPLE))
        self.play(ShowCreation(rectangles))
        self.wait(1)

        # Slope
        f_xt, f_xt_dx = func(xt), func(xt+dx)
        pos_arrow = Arrow(axes_func.c2p(xt, 0), axes_func.c2p(xt, f_xt), buff=0, max_tip_length_to_length_ratio=0.08).set_color(RED)
        neg_arrow = Arrow(axes_func.c2p(xt+dx, 0), axes_func.c2p(xt+dx, f_xt_dx), buff=0, max_tip_length_to_length_ratio=0.08).set_color(GREEN)
        self.play(GrowArrow(pos_arrow), GrowArrow(neg_arrow))
        slope = Line(axes_func.c2p(xt, f_xt), axes_func.c2p(xt+dx, f_xt_dx)).set_color(BLUE)
        slope_x = Line(axes_func.c2p(xt, f_xt), axes_func.c2p(xt+dx, f_xt)).set_color(BLUE)
        slope_y = Line(axes_func.c2p(xt+dx, f_xt), axes_func.c2p(xt+dx, f_xt_dx)).set_color(BLUE)
        slope_group = VGroup(slope_x, slope_y, slope)
        # Animate the rotation and shift of the arrow
        self.play(Rotate(pos_arrow, angle=PI, about_point=pos_arrow.get_center()))
        pos_arrow_rotated = Arrow(axes_func.c2p(xt, f_xt), axes_func.c2p(xt, 0), buff=0, max_tip_length_to_length_ratio=0.08).set_color(RED)
        self.remove(pos_arrow)
        self.play(pos_arrow_rotated.animate.shift(axes_func.c2p(dx, 0) - axes_func.c2p(0, 0)))
        self.play(ShowCreation(slope_group))
        self.wait(1)
        return label_x

    def construct(self):
        # Define the function
        def func(x):
            return 2 * x + 0.5 * np.sin(2 * x)
        
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
        graph_func = axes_func.get_graph(func, color=YELLOW)
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
        # Starting line
        x0 = 2/3
        dx = 1/3
        progress_line_x0 = DashedLine(axes_deriv.c2p(x0, 0), axes_func.c2p(x0, func(x0)), color=WHITE)
        label_x0 = Tex(f"x_0").set_color(WHITE).scale(0.75).next_to(axes_deriv.c2p(x0, 0), DOWN)
        self.add(progress_line_x0, label_x0)
        xt = x0
        n = 5
        label_x = None
        for _ in range(n):
            label_x = self.add_interval(xt=xt, dx=dx, axes_func=axes_func, func=func, axes_deriv=axes_deriv, graph_deriv=graph_deriv, label_x=label_x)
            xt += dx

        # Final arrows
        nef_arrow = Arrow(axes_func.c2p(x0+dx, func(x0)), axes_func.c2p(x0+dx, 0), buff=0, thickness=7).set_color(RED)
        pos_arrow = Arrow(axes_func.c2p(x0+n*dx, 0), axes_func.c2p(x0+n*dx, func(x0+n*dx)), buff=0, thickness=7).set_color(GREEN)
        self.play(GrowArrow(nef_arrow), GrowArrow(pos_arrow))

        final_text = Tex(r"\int_{x_0}^{x} s(y) \, dy = f(x) - f(x_0)").set_color(BLUE).scale(0.65).to_edge(5*DOWN+7.7*RIGHT)
        background_color = rgba_to_color(self.camera.background_rgba)
        final_rect = SurroundingRectangle(final_text, color=BLUE, fill_opacity=1, fill_color=background_color)
        self.play(ShowCreation(final_rect), Write(final_text))

        self.wait(1)

# To render the scene, run the following command in your terminal:
# poetry run manimql integrating_slope.py IntegratingSlope