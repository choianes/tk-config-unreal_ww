import maya.cmds as cmds
import os

def export_fbx(output_path):
    # FBX export 설정
    cmds.loadPlugin("fbxmaya", quiet=True)
    cmds.file(rename=output_path)
    cmds.file(force=True, options="v=0", type="FBX export", exportAll=True)
    print(f"Exported FBX to {output_path}")