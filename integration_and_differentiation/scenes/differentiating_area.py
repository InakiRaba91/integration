from manimlib import *

class DifferentiatingArea(Scene):
    def construct(self):
        # Define the function
        def func(x):
            return 2+0.5*x*(x-1)*(x-2)
        a = 0.5
        x = 3

        # Create axes
        axes = Axes(x_range=(-1, 4), y_range=(0, 5), axis_config={"color": BLUE}, width=12, height=6)

        # Create the graph of the function
        graph = axes.get_graph(func, color=YELLOW)
        f_text = Tex(r"f(x)").set_color(YELLOW).scale(0.75).to_edge(7*UP+7.5*LEFT)

        # Add axes, graph, and labels to the scene
        self.add(axes, graph, f_text)
        limit = DashedLine(
            start=axes.c2p(a, 0),
            end=axes.c2p(a, func(a)),
            dash_length=0.1,
            color=RED,
            stroke_width=7,
        )
        self.add(limit)
        
        # Add labels below the x-axis
        label = Tex(f"a").set_color(RED).scale(0.75).next_to(axes.c2p(a, 0), DOWN)
        self.add(label)
                
        # Draw Riemann rectangles
        dx = 0.1

        # Animate the rectangles with decreasing dx
        bs = [x, x + dx]
        label_bs = ["x", "x + \Delta x"]
        pos_labels = [1.3*DOWN, DOWN+0.2*RIGHT]
        colors_bs = [(TEAL, GREEN), (RED, ORANGE)]
        fill_opacity_bs = [1, 0.5]
        pos_bs = [2.2*UP+7.8*RIGHT, UP+3*RIGHT]
        for b, label_b, pos_label, colors, fill_opacity, pos in zip(bs, label_bs, pos_labels, colors_bs, fill_opacity_bs, pos_bs):
            # Add text label indicating the area under the curve is the integral of f(x)
            limit = DashedLine(
                start=axes.c2p(b, 0),
                end=axes.c2p(b, func(b)),
                dash_length=0.1,
                color=colors[1],
                stroke_width=7,
            )
            self.add(limit)
            # Add labels below the x-axis
            label = Tex(f"{label_b}").set_color(colors[1]).scale(0.6).next_to(axes.c2p(b, 0), pos_label)
            self.add(label)

            rectangles = axes.get_riemann_rectangles(
                graph,
                x_range=(a, b),
                dx=dx,
                colors=colors,
                fill_opacity=fill_opacity,
                stroke_background=False
            )
            integral_text = Tex(f"A({label_b})").set_color(colors[1]).scale(0.75).to_edge(pos)
            self.play(ShowCreation(rectangles), Write(integral_text))
            self.wait(2)
        # Highlight difference
        rectangles = axes.get_riemann_rectangles(
            graph,
            x_range=(x, x),
            dx=dx,
            colors=(PURPLE, PURPLE),
            stroke_background=False
        )
        integral_text = Tex(r"A(x+\Delta x)-A(x)=\frac{f(x)}{\Delta x}").set_color(PURPLE).scale(0.5).to_edge(8*DOWN+0.4*RIGHT)
        self.play(ShowCreation(rectangles), Write(integral_text))
        self.wait(1)

        # Add final text inside a blue rectangle
        final_text = Tex(r"A'(x) = \frac{\Delta A}{\Delta x}=f(x)").set_color(BLUE).scale(0.65).to_edge(4.5*DOWN+0.5*RIGHT)
        final_rect = SurroundingRectangle(final_text, color=BLUE)
        self.play(Write(final_text), ShowCreation(final_rect))
        self.wait(2)


# To render the scene, run the following command in your terminal:
# poetry run manimql differentiating_area.py DifferentiatingArea