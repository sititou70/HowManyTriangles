import bpy
import bmesh
from . import mesh_utils
import time

def isEqualPaths(path1, path2):
    return len(set(path1) ^ set(path2)) is 0

def isInArrayWithComp(it, array, comp):
    for item in array:
        if comp(it, item):
            return True
    
    return False

def removeDuplicate(array, comp):
    array_uniq = []
    
    for item in array:
        if not isInArrayWithComp(item, array_uniq, comp):
            array_uniq.append(item)
    
    return array_uniq

def printPath(path):
    mesh_utils.unselectMesh(bmesh.from_edit_mesh(bpy.context.object.data))
    
    for item in path:
        item.select = True
    
    bpy.context.scene.objects.active = bpy.context.scene.objects.active

def calcTurningNum(path, angle_threshold):
    turning_num = 0
    
    if len(path) <= 3:
        return turning_num
    
    for i in map(lambda x : x + 1, range(0, len(path) - 4, 2)):
        if mesh_utils.calcEdgesAngle(path[i], path[i + 2]) < angle_threshold:
            turning_num += 1
    
    if path[0] is path[-1]:
        if mesh_utils.calcEdgesAngle(path[1], path[-2]) < angle_threshold:
            turning_num += 1
    
    return turning_num

def turningLimitedDFS(data):
    if calcTurningNum(data["track"], data["angle_threshold"]) > data["polygonNum"]:
        data["track"].pop()
        data["track"].pop()
        return data
    
    if len(data["track"]) >= 3 and data["track"][-1] is data["track"][0]:
        if calcTurningNum(data["track"], data["angle_threshold"]) is data["polygonNum"]:
            data["paths"].append(data["track"][:])
        data["track"].pop()
        data["track"].pop()
        return data
    
    for edge in data["track"][-1].link_edges:
        next_vertex = list(set(edge.verts) - set([data["track"][-1]]))[0]
        if next_vertex is data["track"][0] or next_vertex not in data["track"]:
            data["track"].append(edge)
            data["track"].append(next_vertex)
            data = turningLimitedDFS(data)
    
    if len(data["track"]) >= 3:
        data["track"].pop()
        data["track"].pop()
    return data

def getPolygons(mesh, n, angle_threshold):
    paths = []
    
    for vertex in mesh.verts:
        paths += turningLimitedDFS({"track": [vertex], "polygonNum": n, "paths": [], "angle_threshold": angle_threshold})["paths"]
    
    return removeDuplicate(paths, isEqualPaths)
