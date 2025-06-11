import os
import re

def split_scenes_grouped_fixed(input_file, output_base="Scenes"):
    os.makedirs(output_base, exist_ok=True)

    # Regex to capture: <!-- Scene 10.1 --> or <!-- Scene 10.1 JSON -->
    scene_pattern = re.compile(r'<!--\s*Scene\s+([0-9.]+)(?:\s+(json))?\s*-->', re.IGNORECASE)

    current_scene = None
    current_type = None
    buffer = []

    def save_scene(scene_name, scene_type, content):
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
                # If a previous block exists, save it
                if current_scene and buffer:
                    save_scene(current_scene, current_type, buffer)
                    buffer = []

                current_scene = match.group(1)
                current_type = match.group(2).lower() if match.group(2) else "xml"
            elif current_scene:
                buffer.append(line)

        # Save the final buffer
        if current_scene and buffer:
            save_scene(current_scene, current_type, buffer)

    print(f"Scenes correctly saved into '{output_base}' with XML and JSON split per scene.")

# Example usage
split_scenes_grouped_fixed("scenes_input.txt")
