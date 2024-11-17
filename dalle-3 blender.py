import os
import httpx
from openai import AzureOpenAI
from PIL import Image
import matplotlib.pyplot as plt
import bpy

# Azure OpenAI DALL-E 3 Configuration
deployment_name = "dall-e-3"
client = AzureOpenAI(
    api_version="2024-02-01",
    api_key="e31d5f754aae4f4a922646ab803149bavgarga6b",  # Replace with your Azure OpenAI API key
    azure_endpoint="https://kavinazureopenai.openai.azure.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01"
)

# Directory to save generated images
output_dir = r"C:\Users\vskav\Downloads\proj"  # Replace with your desired folder path
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

# Generate an image using Azure OpenAI DALL-E 3
def generate_image(prompt, output_file):
    try:
        # Generate image using DALL-E
        result = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1
        )
        
        # Get image URL from response
        image_url = result.data[0].url
        
        # Download and save the image
        response = httpx.get(image_url)
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        print(f"Image successfully saved to {output_file}")
        return output_file
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

# Load image into Blender
def load_image_in_blender(image_path):
    try:
        # Create a plane with the image as texture
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
        plane = bpy.context.object
        mat = bpy.data.materials.new(name="ImageMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        tex_image = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex_image.image = bpy.data.images.load(image_path)
        mat.node_tree.links.new(bsdf.inputs["Base Color"], tex_image.outputs["Color"])
        plane.data.materials.append(mat)
        print("Image successfully loaded into Blender")
    except Exception as e:
        print(f"Error loading image into Blender: {e}")

# Main script
if __name__ == "__main__":
    prompt = "A 3D realistic rendering of a futuristic city with flying cars and skyscrapers"  # Replace with your desired prompt
    output_file = os.path.join(output_dir, "generated_image.png")  # Define the path for the generated image
    
    # Generate the image
    image_path = generate_image(prompt, output_file)
    
    # Display the image (optional)
    if image_path:
        image = Image.open(image_path)
        plt.imshow(image)
        plt.axis("off")  # Turn off axis
        plt.show()
    
    # Load the image into Blender
    if image_path:
        load_image_in_blender(image_path)
