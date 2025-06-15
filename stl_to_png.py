import os
import trimesh
import pyrender
import numpy as np
from PIL import Image

def convert_stl_to_png(directory):
    print(f"Starting STL to PNG conversion from root: {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.stl'):
                stl_path = os.path.join(root, file)
                png_path = os.path.splitext(stl_path)[0] + '.png'

                # Skip if PNG already exists
                if os.path.exists(png_path):
                    print(f"Skipping: {png_path} (already exists)")
                    continue

                try:
                    # Load mesh
                    mesh = trimesh.load(stl_path)

                    # Handle Scenes (multiple geometries)
                    if isinstance(mesh, trimesh.Scene):
                        geometries = list(mesh.geometry.values())
                        if not geometries:
                            print(f"Skipping: {stl_path} (no geometry found)")
                            continue
                        combined = trimesh.util.concatenate(geometries)
                    else:
                        combined = mesh

                    # Ensure mesh has faces
                    if not combined.is_watertight:
                        print(f"Skipping: {stl_path} (mesh is not watertight)")
                        continue

                    # Create Pyrender mesh
                    pr_mesh = pyrender.Mesh.from_trimesh(combined)

                    # Create scene and add mesh
                    scene = pyrender.Scene()
                    scene.add(pr_mesh)

                    # Camera setup
                    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)
                    camera_pose = np.eye(4)
                    center = combined.centroid
                    max_dim = np.max(combined.extents)
                    distance = max_dim * 2
                    camera_pose[:3, 3] = [0, 0, distance]
                    scene.add(camera, pose=camera_pose)

                    # Light setup
                    light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=2.0)
                    scene.add(light, pose=camera_pose)

                    # Renderer
                    renderer = pyrender.OffscreenRenderer(viewport_width=800, viewport_height=600)
                    color, _ = renderer.render(scene)
                    renderer.delete()

                    # Save image
                    image = Image.fromarray(color)
                    image.save(png_path)
                    print(f"Saved: {png_path}")

                except Exception as e:
                    print(f"Error converting {stl_path}: {str(e)}")

if __name__ == "__main__":
    start_directory = "."  # Change this if needed
    convert_stl_to_png(start_directory)