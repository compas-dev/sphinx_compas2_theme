from compas.geometry import Circle, Frame
from compas.colors import Color
from compas_view2.app import App

primary = Color.from_hex("#0092d2")
secondary = Color.from_hls((primary.hls[0] * 360 + 30) / 360 % 1, primary.hls[1], primary.hls[2])

colors = [
    primary,
    secondary,
]

viewer = App()
viewer.view.show_grid = False
viewer.view.camera.position = [len(colors) / 2, -1, 10]
viewer.view.camera.look_at([len(colors) / 2, 0, 0])

for i, color in enumerate(colors):
    print(color)
    viewer.add(Circle(0.4, Frame([i, 0, 0])).to_polygon(n=100), facecolor=color)

viewer.run()
