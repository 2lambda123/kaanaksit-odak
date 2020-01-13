import plyfile
from plyfile import PlyData, PlyElement
from odak import np
from .transformation import rotate_point

def read_PLY(fn,offset=[0,0,0],angles=[0.,0.,0.],mode='XYZ'):
    """
    Definition to read a PLY file and extract meshes from a given PLY file. Note that rotation is always with respect to 0,0,0.

    Parameters
    ----------
    fn           : string
                   Filename of a PLY file.
    offset       : ndarray
                   Offset in X,Y,Z.
    angles       : list
                   Rotation angles in degrees.
    mode         : str
                   Rotation mode determines ordering of the rotations at each axis. There are XYZ,YXZ,ZXY and ZYX modes.                  

    Returns
    ----------
    triangles   : ndarray
                  Triangles from a given PLY file. Note that the triangles coming out of this function isn't always structured in the right order and with the size of (MxN)x3. You can use numpy's reshape to restructure it to mxnx3 if you know what you are doing.
    """
    with open(fn,'rb') as f:
        plydata = PlyData.read(f)
    triangle_ids = np.vstack(plydata['face'].data['vertex_indices'])
    triangles    = []
    for vertex_ids in triangle_ids:
        triangle     = [
                        rotate_point(plydata['vertex'][int(vertex_ids[0])].tolist(),angles=angles)[0],
                        rotate_point(plydata['vertex'][int(vertex_ids[1])].tolist(),angles=angles)[0],
                        rotate_point(plydata['vertex'][int(vertex_ids[2])].tolist(),angles=angles)[0]
                       ]
        triangle     = np.asarray(triangle)
        triangle[0] += np.asarray(offset)
        triangle[1] += np.asarray(offset)
        triangle[2] += np.asarray(offset)
        triangles.append(triangle)
    triangles = np.array(triangles)
    return triangles

def write_PLY(triangles,savefn='output.ply'):
    """
    Definition to generate a PLY file from given points.

    Parameters
    ----------
    triangles   : ndarray
                  List of triangles with the size of Mx3x3.
    savefn      : string
                  Filename for a PLY file.
    """
    tris  = []
    pnts  = []
    color = [255,255,255]
    for tri_id in range(triangles.shape[0]):
       tris.append(
                   (
                    [3*tri_id,3*tri_id+1,3*tri_id+2], 
                    color[0],
                    color[1],
                    color[2]
                   )
                  )
       for i in range(0,3):
           pnts.append(
                       (
                        float(triangles[tri_id][i][0]),
                        float(triangles[tri_id][i][1]),
                        float(triangles[tri_id][i][2])
                       )
                      )
    if np.__name__ == 'cupy':
        import numpy as np_cpu
        tris   = np_cpu.asarray(tris, dtype=[('vertex_indices', 'i4', (3,)),('red', 'u1'), ('green', 'u1'),('blue', 'u1')])
        pnts   = np_cpu.asarray(pnts, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    else:
        tris   = np.asarray(tris, dtype=[('vertex_indices', 'i4', (3,)),('red', 'u1'), ('green', 'u1'),('blue', 'u1')])
        pnts   = np.asarray(pnts, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    # Save mesh.
    el1       = PlyElement.describe(pnts, 'vertex', comments=['Vertex data'])
    el2       = PlyElement.describe(tris, 'face', comments=['Face data'])
    PlyData([el1,el2],text="True").write(savefn)

def write_PLY_from_points(points,savefn='output.ply'):
    """
    Definition to generate a PLY file from given points.

    Parameters
    ----------
    points      : ndarray
                  List of points with the size of MxNx3.
    savefn      : string
                  Filename for a PLY file.

    """
    # Generate equation
    roi     = np.zeros((2,points.shape[0],points.shape[1]))
    roi[0]  = np.copy(points[:,:,0])
    roi[1]  = np.copy(points[:,:,1])
    zz      = np.copy(points[:,:,2])
    samples = [points.shape[0],points.shape[1]]
    # Generate vertices.
    pnts   = []
    tris   = []
    for idx in range(0,samples[0]):
        for idy in range(0,samples[1]):
            pnt  = (roi[0][idx][idy]    , roi[1][idx][idy]    , zz[idx][idy])
            pnts.append(pnt)
    m = samples[0]*samples[1]
    color = [255,255,255]
    for idx in range(0,samples[0]-1):
        for idy in range(0,samples[1]-1):
            tris.append(([idy+(idx+1)*samples[0], idy+idx*samples[0]  , idy+1+idx*samples[0]], color[0], color[1], color[2]))
            tris.append(([idy+(idx+1)*samples[0], idy+1+idx*samples[0], idy+1+(idx+1)*samples[0]], color[0], color[1], color[2]))
    tris   = np.asarray(tris, dtype=[('vertex_indices', 'i4', (3,)),('red', 'u1'), ('green', 'u1'),('blue', 'u1')])
    pnts   = np.asarray(pnts, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    # Save mesh.
    el1       = PlyElement.describe(pnts, 'vertex', comments=['Vertex data'])
    el2       = PlyElement.describe(tris, 'face', comments=['Face data'])
    PlyData([el1,el2],text="True").write(savefn)
