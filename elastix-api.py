from SimpleITK import (
    ReadImage, WriteImage, ElastixImageFilter,
    GetDefaultParameterMap
    )
from pydantic import BaseModel
from fastapi import FastAPI

class Elastix_Inputs(BaseModel):
    r"""
    ### Purpose:
    - This class defines the inputs required for the Elastix registration API.
    ### Attributes:
    - `fixed_image`: Path to the fixed image.
    - `moving_image`: Path to the moving image.
    - `parameter_map`: Dictionary containing the parameter map for registration.
    """
    pth_fixed_image: str
    pth_moving_image: str
    parameter_map: str = "translation"
    pth_output_image: str = "temp_data/registered_image.nrrd"

app = FastAPI()

@app.post("/elastix_register")
def elastix_register(elastix_inputs: Elastix_Inputs):
    r"""
    ### Purpose:
    - This function performs image registration using the Elastix library.
    ### Parameters:
    - `elastix_inputs`: An instance of `Elastix_Inputs` containing the necessary inputs.
    ### Returns:
    - The result of the registration process.
    """

    fixed_image = ReadImage(elastix_inputs.pth_fixed_image)
    moving_image = ReadImage(elastix_inputs.pth_moving_image)
    parameter_map = GetDefaultParameterMap(elastix_inputs.parameter_map)

    ela_img_filter = ElastixImageFilter()
    ela_img_filter.SetFixedImage(fixed_image)
    ela_img_filter.SetMovingImage(moving_image)
    ela_img_filter.SetParameterMap(parameter_map)

    result = ela_img_filter.Execute()
    try:
        WriteImage(result, elastix_inputs.pth_output_image)
        return {
            "status": "success",
            "message": "Image registration completed successfully.",
            "output_image_path": elastix_inputs.pth_output_image
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to write output image: {str(e)}"
        }

def test_elastix_register():
    input_obj = Elastix_Inputs(
        pth_fixed_image="temp_data/mr_case000000.nrrd",
        pth_moving_image="temp_data/us_case000000.nrrd"
    )
    elastix_register(input_obj)

if __name__ == "__main__":
    test_elastix_register()
    print("Elastix registration test completed successfully.")