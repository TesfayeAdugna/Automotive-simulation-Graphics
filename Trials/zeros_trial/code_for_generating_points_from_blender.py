import bpy
obdata = bpy.context.object.data

print("Vertixes")
vertexlist = []
for v in obdata.vertices:
    vertexlist.append("({}, {}, {})".format(v.co.x, v.co.y, v.co.z))

print("edges")
edgelist = []
for e in obdata.edges:
    print("({}, {})".format(e.vertices[0], e.vertices[1]))
    edgelist.append("({}, {})".format(e.vertices[0], e.vertices[1]))



print("faces")
for f in obdata.polygons:
     print("(", end="")
     for v in f.vertices:
         print("{},".format(v), end="")
     print("),\t", end = "")