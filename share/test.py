import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = './test.txt'

def visual_vector(axes, loc, vector, color = "red"):
    axes.quiver(loc[0], loc[1],
              vector[0], vector[1], color = color,
              angles = 'xy', scale_units = 'xy', scale = 1)

if __name__ == "__main__":
    with open(DATA_PATH) as f:
        lst = f.readlines()
    data = []
    for row in lst:
        row = row.split()
        data.append([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
    
    df = pd.DataFrame(data, columns=['x_pos', 'y_pos', 'x_vec', 'y_vec'])

    fig, ax = plt.subplots(figsize=(45, 45))
    ax.set_xlabel('$X$', fontsize=15)
    ax.set_ylabel('$Y$', rotation=0, fontsize=15)
    q = plt.quiver(df['x_pos'], df['y_pos'], df['x_vec'], df['y_vec'], angles='xy', scale_units='xy', scale=1)
    plt.show()