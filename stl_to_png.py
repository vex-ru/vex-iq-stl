import os
import pyvista as pv

# Traverse all directories starting from the current directory
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.lower().endswith('.stl'):
            stl_path = os.path.join(root, file)
            png_path = os.path.splitext(stl_path)[0] + '.png'

            try:
                # Load the STL mesh
                mesh = pv.read(stl_path)

                # Create a plotter with off-screen rendering
                plotter = pv.Plotter(off_screen=True)

                # Add mesh with smooth shading and light blue color
                plotter.add_mesh(mesh, color='lightblue', smooth_shading=True)

                # Set isometric camera view to show 3 sides
                plotter.view_isometric()

                # Optional: Set background color
                plotter.background_color = 'white'

                # Adjust camera to ensure full object is visible
                plotter.reset_camera()

                # Save the screenshot as PNG
                plotter.screenshot(png_path)

                # Close plotter to free memory
                plotter.close()

                print(f"Generated: {png_path}")

            except Exception as e:
                print(f"Failed to process {stl_path}: {e}")