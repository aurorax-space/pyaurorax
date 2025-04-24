from ..classes.fov import FOV


def create_map(cartopy_projection, fov_data):

    # Store the projection information and FOVData objects (if there is any) in an
    # FOV Object and return it
    if fov_data is not None:
        if isinstance(fov_data, list):
            return FOV(cartopy_projection=cartopy_projection, fov_data=fov_data)
        else:
            return FOV(cartopy_projection=cartopy_projection, fov_data=[fov_data])
    else:
        return FOV(cartopy_projection=cartopy_projection)
