from SimpleITK import (
    ReadImage, WriteImage, ElastixImageFilter,
    GetDefaultParameterMap, WriteParameterFile,
    ReadParameterFile, TransformixImageFilter
    )
from pydantic import BaseModel
from fastapi import FastAPI
from pathlib import Path
from typing import List

class Register_Inputs(BaseModel):
    r"""
    ### Purpose:
    - This class defines the inputs required for the Elastix registration API.
    ### Attributes:
    - `fixed_image`: Path to the fixed image.
    - `moving_image`: Path to the moving image.
    - `parameter_map`: parameter map for the transformations.
    """
    pth_fixed_image: str
    pth_moving_image: str
    parameter_map: str = "translation"
    pth_output_image: str = "registered_image.nrrd"

    def __init__(self, **data):
        super().__init__(**data)
        dir_temp_data = Path(__file__).parent.joinpath("temp_data")
        self.pth_fixed_image=  str(dir_temp_data.joinpath(self.pth_fixed_image))
        self.pth_moving_image= str(dir_temp_data.joinpath(self.pth_moving_image))
        self.pth_output_image= str(dir_temp_data.joinpath(self.pth_output_image))

app = FastAPI()

@app.post("/elastix_register")
def elastix_register(elastix_inputs: Register_Inputs):
    r"""
    ### Purpose:
    - This function performs image registration using the Elastix library.
    ### Parameters:
    - `elastix_inputs`: An instance of `Register_Inputs` containing the necessary inputs.
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
        transform_maps = ela_img_filter.GetTransformParameterMap()
        for i, transform_map in enumerate(transform_maps):
            WriteParameterFile(
                transform_map,
                str(
                    Path(elastix_inputs.pth_output_image).parent.joinpath(f"transform_parameter_{i}.txt"))
            )

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

class Warp_Inputs(BaseModel):
    r"""
    ### Purpose:
    - This class defines the inputs required for the Elastix warping API.
    The warp operation applies a transformation to an input image.
    ### Attributes:
    """
    pth_input: str
    pth_output: str
    pth_transform_maps: List[str]   

    def __init__(self, **data):
        super().__init__(**data)
        dir_temp_data = Path(__file__).parent.joinpath("temp_data")
        self.pth_input = str(dir_temp_data.joinpath(self.pth_input))
        self.pth_output = str(dir_temp_data.joinpath(self.pth_output))
        self.pth_transform_maps = [
            str(dir_temp_data.joinpath(pth)) for pth in self.pth_transform_maps
            ]

@app.post("/elastix_warp")
def elastix_warp(warp_inputs: Warp_Inputs):
    r"""
    ### Purpose:
    - This function performs image warping using the Elastix library.
    ### Parameters:
    - `warp_inputs`: An instance of `Warp_Inputs` containing the necessary inputs.
    ### Returns:
    - The result of the warping process.
    """

    input_image = ReadImage(warp_inputs.pth_input)
    transform_map_list = []
    for transform_map_path in warp_inputs.pth_transform_maps:
        if not Path(transform_map_path).exists():
            return {
                "status": "error",
                "message": f"Transform map file {transform_map_path} does not exist."
            }
        transform_map_list.append(ReadParameterFile(transform_map_path))

    transformix_filter = TransformixImageFilter()
    transformix_filter.SetMovingImage(input_image)
    transformix_filter.SetTransformParameterMap(transform_map_list)

    result = transformix_filter.Execute()

    try:
        WriteImage(result, warp_inputs.pth_output)
        return {
            "status": "success",
            "message": "Image warping completed successfully.",
            "output_image_path": warp_inputs.pth_output
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to write output image: {str(e)}"
        }

def test_elastix_register():
    input_obj = Register_Inputs(
        pth_fixed_image="mr_case000000.nrrd",
        pth_moving_image="us_case000000.nrrd"
    )
    elastix_register(input_obj)

def test_elastix_warp():
    input_obj = Warp_Inputs(
        pth_input="us_case000000.nrrd",
        pth_output="warped_image.nrrd",
        pth_transform_maps=["transform_parameter_0.txt"]
    )
    elastix_warp(input_obj)

if __name__ == "__main__":
    test_elastix_register()
    # print("Elastix registration test completed successfully.")
    test_elastix_warp()
    print("Elastix warping test completed successfully.")
    