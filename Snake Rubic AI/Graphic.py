import matplotlib.pyplot as plt
import numpy as np

sample = {
    "coordinates": [
        [-5, 2, -6],
        [-5, 2, -5],
        [-5, 2, -4],
        [-4, 2, -4],
        [-3, 2, -4],
        [-3, 2, -3],
        [-3, 2, -2],
        [-2, 2, -2],
        [-1, 2, -2],
        [-1, 2, -1],
        [0, 2, -1],
        [0, 2, 0],
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [2, 0, 1],
        [3, 0, 1],
        [3, 0, 2],
        [3, 0, 3],
        [4, 0, 3],
        [4, 0, 4],
        [4, 0, 5],
        [5, 0, 5],
        [5, 0, 6],
        [6, 0, 6],
        [7, 0, 6],
    ],
    "sticky_cubes": [[5, 6], [12, 13], [14, 15], [15, 16], [18, 19]],
}


import numpy as np
import plotly.graph_objects as go

class Graphic:
    def __init__(self) -> None:
        pass

    def display(self, coordinates):
        # Initialize a 3D array for the voxel grid
        voxelarray = np.zeros([25, 25, 25], dtype=bool)

        # Populate the voxel grid
        for coor in coordinates:
            x, y, z = coor[0], coor[1], coor[2]
            x += 15
            y += 15
            z += 15
            voxelarray[x, y, z] = True

        # Get the indices of non-zero (True) elements
        x, y, z = np.where(voxelarray)

        # Create a 3D scatter plot using Plotly
        fig = go.Figure(data=go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            marker=dict(
                size=5,  # Set the size of the markers
                color=z,  # Optional: use color to represent the z-axis value
                colorscale='Viridis',  # Choose a colorscale
                opacity=0.8
            )
        ))

        # Update layout for better visualization
        fig.update_layout(
            scene=dict(
                xaxis=dict(nticks=10, range=[0, 25]),
                yaxis=dict(nticks=10, range=[0, 25]),
                zaxis=dict(nticks=10, range=[0, 25])
            ),
            title='3D Voxel Representation',
            margin=dict(r=10, l=10, b=10, t=50)
        )

        fig.show()

# graphic = Graphic()
#
# graphic.display(sample["coordinates"])