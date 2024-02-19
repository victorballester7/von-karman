import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib import colormaps as cm
from matplotlib.ticker import LinearLocator
import os
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.axes import Axes
from matplotlib.text import Text
from typing import cast
import sys
import time
from read_data import read_data_file
from matplotlib.patches import Circle, Rectangle


# DEFAULTS
X_LABEL = 'x'
Y_LABEL = 'y'
Z_LABEL = 'z'
FONTSIZE_TIME = 10
y_pos_text = 1.03
y_pos_title = y_pos_text + 0.14
color = cm['inferno']
colorbar_args = {'shrink': 0.5, 'aspect': 10, 'location': 'left'}
duration = 10  # duration of the animation in seconds


def animate(filename: str, save=False):
    # Create a figure
    fig, ax = plt.subplots()

    # Read data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Replace with the actual file path
    file_path = script_dir + '/../' + filename
    headers, data_blocks = read_data_file(file_path)

    num_frames = len(data_blocks)
    FPS = int(num_frames / duration) + 1  # +1 to ensure positivity
    interval = 1000 / FPS  # interval between frames in milliseconds

    # Print some information
    print("Length of data: ", len(data_blocks))
    print("Number of frames: ", num_frames)
    print("Interval: ", interval)
    print("Expected duration: ", duration)

    # Create data
    nx = data_blocks.shape[1]
    ny = data_blocks.shape[2]

    dx = Lx / nx
    dy = Ly / ny

    X = np.linspace(dx / 2, Lx - dx / 2, nx)
    Y = np.linspace(dy / 2, Ly - dy / 2, ny)
    X, Y = np.meshgrid(X, Y, indexing='xy')

    # transpose the data and reverse
    old_data_blocks = data_blocks
    data_blocks = np.zeros((len(old_data_blocks), ny, nx))
    for i in range(len(old_data_blocks)):
        data_blocks[i] = old_data_blocks[i].T[::-1]

    Z = data_blocks[0]
    Z_MAX = np.max(data_blocks)
    Z_MIN = 0
    plot_args = {
        'cmap': color,
        'extent': [
            0,
            Lx,
            0,
            Ly],
        'vmin': Z_MIN,
        'vmax': Z_MAX,
        'interpolation': 'none'}
    # 'interpolation': 'spline16'}
    text_args = {'x': 0.5, 'y': y_pos_text, 's': '', 'transform': ax.transAxes,
                 'fontsize': FONTSIZE_TIME, 'horizontalalignment': 'center'}
    time_text = ax.text(**text_args)

    # Axes
    ax.set_xlabel(X_LABEL)
    ax.set_ylabel(Y_LABEL)

    # plot a circle
    if object != "":
        if object == 'circle':
            obstacle = Circle((x0, y0), radius, color='r', fill=False)
        elif object == 'rectangle':
            obstacle = Rectangle(
                (x0, y0), width, height, color='r', fill=False)
        # Add the circle to the plot
        ax.add_artist(obstacle)

    # Create plot
    plot = [ax.imshow(Z, **plot_args)]

    # Add a color bar which maps values to colors.
    fig.colorbar(plot[0], **colorbar_args)

    # Animation update function
    def init():
        return plot[0], time_text

    def update(frame):
        # Clear the previous frame
        # ax.clear()
        plot[0].remove()

        real_frame = int(frame)

        # Update the arrays
        Z = data_blocks[real_frame]

        # Update the time text
        time_text.set_text('t = %.3f' % headers[real_frame])

        # Update the plot
        plot[0] = ax.imshow(Z, **plot_args)

        return plot[0], time_text

    # Create the animation
    ani = FuncAnimation(fig, update, frames=num_frames,
                        interval=interval, blit=False, init_func=init)

    end_time = time.time()
    print("Total time for animating: ", int(
        UNIT_TIME * (end_time - start_time)), LABEL_TIME)

    if save:
        # Save the animation
        ani.save('animation.mp4', writer='ffmpeg', fps=FPS)
    else:
        # Show the animation
        plt.show()


# count time
UNIT_TIME = 1000  # in seconds
LABEL_TIME = "ms"
start_time = time.time()

try:
    Lx = float(sys.argv[1])
    Ly = float(sys.argv[2])
except IndexError:
    Lx = np.nan
    Ly = np.nan
try:
    object = sys.argv[3]
except IndexError:
    object = ""

if object == 'circle':
    try:
        x0 = float(sys.argv[4])
        y0 = float(sys.argv[5])
        radius = float(sys.argv[6])
    except IndexError:
        x0 = np.nan
        y0 = np.nan
        radius = np.nan
elif object == 'rectangle':
    try:
        x0 = float(sys.argv[4])
        y0 = float(sys.argv[5])
        width = float(sys.argv[6])
        height = float(sys.argv[7])
    except IndexError:
        x0 = np.nan
        y0 = np.nan
        x1 = np.nan
        y1 = np.nan


sol_u = 'data/u_solution.txt'

animate(sol_u)
