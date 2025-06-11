import os
import re

def split_scenes_with_offset(input_file, output_base="Scenes", offset=0):
    os.makedirs(output_base, exist_ok=True)

    scene_pattern = re.compile(r'<!--\s*Scene\s+([0-9]+)(?:\.([0-9]+))?(?:\s+(json))?\s*-->', re.IGNORECASE)

    current_scene = None
    current_type = None
    buffer = []

    def offset_scene_name(major_str, minor_str):
        major_num = int(major_str) + offset
        if minor_str:
            return f"{major_num}.{minor_str}"
        else:
            return str(major_num)

    def save_scene(scene_name, scene_type, content):
        # scene_name is offset version, e.g. "150.1"
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

                major_part = match.group(1)
                minor_part = match.group(2)
                current_type = match.group(3).lower() if match.group(3) else "xml"

                current_scene = offset_scene_name(major_part, minor_part)
            elif current_scene:
                buffer.append(line)

        if current_scene and buffer:
            save_scene(current_scene, current_type, buffer)

    print(f"Scenes saved with offset {offset} in '{output_base}'")

# Example usage
split_scenes_with_offset("scenes_input.txt")
