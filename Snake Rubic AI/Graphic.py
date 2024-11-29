import matplotlib.pyplot as plt
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