import os
import re

def split_scenes_grouped(input_file, output_base="Scenes"):
    os.makedirs(output_base, exist_ok=True)

    scene_pattern = re.compile(r'<!--\s*Scene\s+([^\s]+)(?:\s+(json))?\s*-->', re.IGNORECASE)

    current_scene = None
    current_type = None
    buffer = []

    def save_scene(scene_name, scene_type, content):
        # Extract the major number (e.g., 10 from 10.1)
        major_group = scene_name.split('.')[0]
        group_folder = os.path.join(output_base, f"Scene{major_group}")
        scene_folder = os.path.join(group_folder, f"Scene{scene_name}")
        os.makedirs(scene_folder, exist_ok=True)

        ext = "json" if scene_type == "json" else "xml"
        file_path = os.path.join(scene_folder, f"scene.{ext}")

        with open(file_path, "w") as f:
            f.writelines(content)

    with open(input_file, "r") as f:
        for line in f:
            match = scene_pattern.match(line.strip())
            if match:
                if current_scene and buffer:
                    save_scene(current_scene, current_type, buffer)
                    buffer = []

                current_scene = match.group(1)
                current_type = match.group(2)
            elif current_scene:
                buffer.append(line)

        if current_scene and buffer:
            save_scene(current_scene, current_type, buffer)

    print(f"Scenes organized by group folders under '{output_base}'")

# Example usage
split_scenes_grouped("scenes_input.txt")
