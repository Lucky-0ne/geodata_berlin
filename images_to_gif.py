import os
import imageio.v2 as imageio

# Directory containing your images
directory = 'data/2022-2023_bikethefts/results/further_results/gifs/'

# Get a list of files in the directory (assuming all files are images)
files = sorted([os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.png')])

# Create a list to hold images
images = []
for file in files:
    images.append(imageio.imread(file))

# Save images as a GIF
output_file = 'data/2022-2023_bikethefts/results/further_results/gifs/bikethefts_heatmap.gif'
imageio.mimsave(output_file, images, format='GIF', fps=1)  # Set duration between frames (in seconds)
