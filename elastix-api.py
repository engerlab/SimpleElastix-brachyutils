from SimpleITK import (
    ReadImage, WriteImage, ElastixImageFilter,
    GetParameterMap, GetDefaultParameterMap
    )
from pydantic import BaseModel

class Elastix_Inputs(BaseModel):
    r"""
    ### Purpose:
    - This class defines the inputs required for the Elastix registration API.
    ### Attributes:
    - `fixed_image`: Path to the fixed image.
    - `moving_image`: Path to the moving image.
    - `parameter_map`: Dictionary containing the parameter map for registration.
    """
    fixed_image: str
    moving_image: str
    parameter_map: dict     

def elastix_register(elastix_inputs: Elastix_Inputs):
    r"""
    ### Purpose:
    - This function performs image registration using the Elastix library.
    ### Parameters:
    - `elastix_inputs`: An instance of `Elastix_Inputs` containing the necessary inputs.
    ### Returns:
    - The result of the registration process.
    """

    fixed_image = ReadImage(elastix_inputs.fixed_image)
    moving_image = ReadImage(elastix_inputs.moving_image)
    parameter_map = GetParameterMap(elastix_inputs.parameter_map)
    
    ela_img_filter = elastixImageFilter() 
    ela_img_filter.SetFixedImage(elastix_inputs.fixed_image)
    ela_img_filter.SetMovingImage(elastix_inputs.moving_image)
    ela_img_filter.SetParameterMap(elastix_inputs.parameter_map)
    
    result = ela_img_filter.Execute()
    
    return result

def elastix_register():
    input_obj = Elastix_Inputs(
        fixed_image="temp_data/mr_case000000.seg.nrrd"
        moving_image="temp_data/us_case000000.seg.nrrd"
    )