from bpy_extras.io_utils import (ExportHelper)
from bpy.props import (StringProperty)
import bpy

import os.path
import os

bl_info = {
    "name": "YouTube Markers",
    "author": "Luan Mattner Müller",
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "category": "Import-Export",
}


def ensure_folder_exist(foldername):
    if not os.access(foldername, os.R_OK | os.W_OK | os.X_OK):
        os.makedirs(foldername)


def ensure_extension(filepath, extension):
    if not filepath.lower().endswith(extension):
        filepath += extension

    return filepath


def save(operator, context, filepath=""):
    filepath = ensure_extension(filepath, ".txt")
    scene = bpy.context.scene
    fps = scene.render.fps / scene.render.fps_base

    markers = {}
    for _, v in scene.timeline_markers.items():
        frame = v.frame
        time = frame / fps

        hours, rem = divmod(time, 3600)
        minutes, seconds = divmod(rem, 60)

        markers[frame] = "{:0>2}:{:0>2}:{:0>2} - {}".format(
            int(hours), int(minutes), int(seconds), v.name)

    with open(filepath, 'w', encoding='utf-8') as f:
        for m in sorted(markers.keys()):
            f.write(markers[m] + "\n")

    return {"FINISHED"}


class ExportYouTubeMarkers(bpy.types.Operator, ExportHelper):
    """Save your markers as YouTube chapters list"""
    bl_idname = "chapters.txt"
    bl_label = "Export chapters"

    filter_glob = StringProperty(
        default="*.txt",
        options={'HIDDEN'},
    )

    check_extension = True

    filename_ext = ".txt"

    def execute(self, context):
        return save(self, context, **self.properties)


def menu_func_export(self, context):
    self.layout.operator(ExportYouTubeMarkers.bl_idname,
                         text="YouTube chapters list (.txt)")


def register():
    bpy.utils.register_class(ExportYouTubeMarkers)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportYouTubeMarkers)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
