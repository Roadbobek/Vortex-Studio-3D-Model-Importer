import json
import trimesh
import numpy as np


def obj_to_block_json(
        obj_filepath,
        output_filepath,
        project_id,
        pitch=1.0,
        default_colour=(0.8, 0.8, 0.8, 1.0)
):
    # load obj mesh
    mesh = trimesh.load(obj_filepath, force='mesh')

    # convert mesh into voxels (pitch = size of each block)
    voxel_grid = mesh.voxelized(pitch=pitch)

    # get 3d coordinates of occupied voxel centers
    block_centers = voxel_grid.points

    parts = []

    for i, center in enumerate(block_centers):
        part = {
            "name": f"Part_{i}",
            "position": {
                "x": round(float(center[0]), 4),
                "y": round(float(center[1]), 4),
                "z": round(float(center[2]), 4)
            },
            "rotation": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "scale": {
                "x": float(pitch),
                "y": float(pitch),
                "z": float(pitch)
            },
            "color": {
                "r": default_colour[0],
                "g": default_colour[1],
                "b": default_colour[2],
                "a": default_colour[3]
            },
            "material": "Plastic",
            "group": None,
            "cast_shadow": True,
            "anchored": True,
            "can_collide": True,
            "spawn_location": False,
            "baseplate": False,
            "truss": False,
            "textures": []
        }
        parts.append(part)

    # default light in studio
    default_light = {
        "name": "Light",
        "position": {
            "x": 50.0,
            "y": 80.0,
            "z": 30.0
        },
        "rotation": {
            "x": -0.39447272,
            "y": 0.43916786,
            "z": 0.22334667,
            "w": 0.775654
        },
        "color": {
            "r": 0.99999994,
            "g": 0.99999994,
            "b": 0.99999994,
            "a": 1.0
        },
        "illuminance": 10000.0,
        "shadows_enabled": True
    }

    # construct final project file
    project_data = {
        "project_id": "imported_obj_project",
        "parts": parts,
        "lights": [default_light],
        "groups": []
    }

    with open(output_filepath, "w") as f:
        json.dump(project_data, f, indent=2)

    print(f"Successfully converted {len(parts)} blocks to {output_filepath}")


# usage: .obj file path, project output file path, project id from .json, pitch (export quality)
obj_to_block_json("model_samples\t34.obj", r"C:\Users\Roadb\Documents\Vortex Studio\obj_testing.json", "ba8fc01c0056996d375dedb7db02f973", 0.35)