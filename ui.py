import bpy
import bmesh
import math
from bpy.props import *
from . import functions

result = None
mesh = None
    
def initSceneProperties():
    bpy.types.Scene.polygonNum = IntProperty(
        name = "n", 
        description = "何角形を探索すればいいか教えてください",
        default = 3,
        min = 3,
        soft_max = 100)
    
    bpy.types.Scene.angleThreshold = IntProperty(
        name = "deg",
        description = "何度までの曲がりを直線とみなしますか？",
        default = 170,
        min = 0,
        max = 180)
    
    def printResult(self, context):
        if len(result) > context.scene.resultNum - 1:
            functions.printPath(result[context.scene.resultNum - 1])
    
    bpy.types.Scene.resultNum = IntProperty(
        name = "No.", 
        description = "何番目の多角形を表示しますか？",
        default = 1,
        min = 1,
        update = printResult)

class calcButton(bpy.types.Operator):
    bl_idname = "test.calc_button"
    bl_label = "数える"
  
    def execute(self, context):
        global result
        global mesh
        mesh = bmesh.from_edit_mesh(bpy.context.object.data)
        angle_threshold = context.scene.angleThreshold / 180 * math.pi
        result = functions.getPolygons(mesh, context.scene.polygonNum, angle_threshold)
        self.report({"INFO"}, "%d個の%d角形が見つかりました" % (len(result), context.scene.polygonNum))
        return{"FINISHED"}

class VIEW3D_PT_CustomMenu(bpy.types.Panel):
    bl_label = "多角形の数を数える"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "多角形の数を数える"
    bl_context = "mesh_edit"
  
    @classmethod
    def poll(cls, context):
        return True
  
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="PLUGIN")
  
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        
        col = layout.column(align=True)
        
        col.label(text="何角形？:")
        col.prop(scn, "polygonNum", icon="BLENDER", toggle=True)
        col.label(text="直線とみなす最大の角度:")
        col.prop(scn, "angleThreshold", icon="BLENDER", toggle=True)
        
        col.separator();
        
        col.label(text="実行:")
        col.operator("test.calc_button")
        
        col.separator();
        
        col.label(text="結果の表示:")
        col.prop(scn, "resultNum", icon="BLENDER", toggle=True)
