import bpy
import os
def load_image_as_3d(image_path, output_path):
    try:
        bpy.ops.object.select_all(action='DESELECT')  
        bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0)) 
        plane = bpy.context.object 
        print("Plane created successfully.")

        # Step 2: Create a new material and assign it to the plane
        mat = bpy.data.materials.new(name="ImageMaterial")  # Create a new material
        mat.use_nodes = True  # Enable nodes for the material
        plane.data.materials.append(mat)  # Assign material to the plane
        print("Material assigned successfully.")

        # Step 3: Add the image texture to the material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        tex_image = nodes.new("ShaderNodeTexImage")  # Add a texture image node
        tex_image.image = bpy.data.images.load(image_path)  # Load the image
        print(f"Image '{image_path}' loaded successfully.")
        bsdf = nodes.get("Principled BSDF")  # Get the Principled BSDF node
        links.new(bsdf.inputs["Base Color"], tex_image.outputs["Color"])  # Connect the image to the Base Color

        # Step 4: Add displacement mapping
        displace = nodes.new(type="ShaderNodeDisplacement")  # Create a displacement node
        links.new(displace.inputs["Height"], tex_image.outputs["Color"])  # Use the image for height data
        links.new(displace.outputs["Displacement"], mat.node_tree.nodes["Material Output"].inputs["Displacement"])  # Connect to displacement output
        print("Displacement mapping added successfully.")

        # Step 5: Subdivide the plane for more detail
        bpy.ops.object.mode_set(mode='EDIT')  # Enter edit mode
        bpy.ops.mesh.subdivide(number_cuts=50)  # Subdivide the plane with 50 cuts for high detail
        bpy.ops.object.mode_set(mode='OBJECT')  # Exit edit mode
        print("Plane subdivided successfully.")

        # Step 6: Add a Subdivision Surface Modifier
        subsurf = plane.modifiers.new(name="Subsurf", type="SUBSURF")
        subsurf.levels = 6  # Set levels of subdivision
        subsurf.render_levels = 6  # Set render levels of subdivision

        # Step 7: Enable Adaptive Subdivision
        if bpy.context.scene.render.engine == 'CYCLES':  # Check if using Cycles
            bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'  # Enable experimental features
            plane.modifiers["Subsurf"].subdivision_type = 'ADAPTIVE'
        print("Subdivision surface modifier added successfully.")

        # Step 8: Save the Blender file
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(output_path, "3d_image_scene.blend"))
        print(f"Blender scene saved at {os.path.join(output_path, '3d_image_scene.blend')}")

        # Step 9: Render and save the image
        bpy.context.scene.render.filepath = os.path.join(output_path, "rendered_image.png")
        bpy.ops.render.render(write_still=True)
        print(f"Rendered image saved at {os.path.join(output_path, 'rendered_image.png')}")

        print("Image successfully converted into a 3D object in Blender!")
    except Exception as e:
        print(f"Error converting image to 3D: {e}")

# Main execution
if __name__ == "__main__":
    # Specify the path to your generated image
    image_path = r"C:\Users\vskav\Downloads\proj\generated_image.png"  # Replace with your image path
    output_path = r"C:\Users\vskav\Downloads\proj"  # Replace with your desired output folder path

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Load the image as 3D and save outputs
    load_image_as_3d(image_path, output_path)
