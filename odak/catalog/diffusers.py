from odak import np
import odak.catalog
from odak.raytracing.primitives import define_plane,bring_plane_to_origin
from odak.raytracing.boundary import intersect_w_surface
from odak.wave.parameters import wavenumber
from odak.tools.sample import circular_sample
from odak.tools.transformation import rotate_points,tilt_towards
from odak.raytracing.ray import create_ray_from_two_points

class thin_diffuser():
    """
    A class to represent a thin diffuser. This is generally useful for raytracing and wave calculations.
    """
    def __init__(self,phase=None,shape=[10.,10.],center=[0.,0.,0.],angles=[0.,0.,0.],diffusion_angle=5.,diffusion_no=[3,3]):
        """
        Class to represent a simple planar detector.

        Parameters
        ----------
        phase            : ndarray
                           Initial phase to be loaded. If non provided, it will start with a random phase.
        shape            : list
                           Shape of the detector.
        center           : list
                           Center of the detector.
        angles           : list
                           Rotation angles of the detector.
        diffusion angles : list
                           Full angle of diffusion along two axes.
        diffusion_no     : list
                           Number of rays to be generated along two axes at each diffusion.
        """
        self.settings           = {
                                   'center'                   : center,
                                   'angles'                   : angles,
                                   'rotation mode'            : 'XYZ',
                                   'shape'                    : shape,
                                   'diffusion angle'          : diffusion_angle,
                                   'number of diffusion rays' : diffusion_no
                                  }
        self.plane              = define_plane(
                                               self.settings['center'],
                                               angles=self.settings['angles']
                                              )
        self.k                  = wavenumber(0.05)
        self.diffusion_points   = circular_sample(
                                                  no=self.settings["number of diffusion rays"],
                                                  radius=np.cos(np.radians(self.settings["diffusion angle"]/2.)),
                                                  center=[0.,0.,1.]
                                                 )
        
    def raytrace(self,ray):
        """

        """
        if len(ray.shape) == 2:
            ray = ray.reshape((1,ray.shape[0],ray.shape[1]))
        normal,distance        = intersect_w_surface(ray,self.plane)
        ########################################################################
        # This is the bottleneck for has to be replaced for better performance #
        ########################################################################
        new_rays               = np.empty((0,2,3))
        for point_id in range(0,normal.shape[0]):
            tilt_angles   = tilt_towards(ray[point_id,0],normal[point_id,0])  
            tilted_points = rotate_points(
                                          self.diffusion_points,
                                          angles=tilt_angles,
                                          offset=normal[point_id,0]
                                         )
            new_rays      = np.vstack((new_rays,create_ray_from_two_points(normal[point_id,0],tilted_points)))
        new_rays = np.asarray(new_rays)
        return new_rays,normal,distance