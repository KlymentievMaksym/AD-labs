# %reload_ext autoreload
# %autoreload 2
# %matplotlib inline

"""
Utilities used by example notebooks
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import os
# import command
import datetime
from sentinelhub import SHConfig

from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
        MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
    to_wgs84,
)

# The following is not a package. It is a file utils.py which should be in the same folder as this notebook.
# from utils import plot_image

def plot_image(
    image: np.ndarray, factor: float = 1.0, clip_range: tuple[float, float] | None = None, **kwargs: Any
) -> None:
    """Utility function for plotting RGB images."""
    _, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])

def get_tiff_file_from_sentinel(coords_x_1, coords_y_1, coords_x_2, coords_y_2, resolution=60):
    kiyv_coords_wgs84 = (coords_x_1, coords_y_1, coords_x_2, coords_y_2)
    # kiyv_coords_wgs84 = to_wgs84(51.415883589517534,30.12370823169888, 51.44399790803582,31.7020921271763, 50.45686117062749, 31.729300891794363, 50.42971299170202,30.183927395096326, 51.415883589517534,30.12370823169888)
    # kiev_coords = np.array([29.073321247506765, 49.845775018245774, 31.986007792928522, 49.845775018245774, 31.986007792928522, 51.278667808079206, 29.073321247506765, 51.278667808079206,29.073321247506765, 49.845775018245774])
    # betsiboka_coords_wgs84 = (31.56, 31.55, 32.51, 32.58)
    
    kiyv_bbox = BBox(bbox=kiyv_coords_wgs84, crs=CRS.WGS84)
    
    betsiboka_size = bbox_to_dimensions(kiyv_bbox, resolution=resolution)
    #S2A_MSIL2A_20190821T085601_N0213_R007_T36UUB_20190821T115206
    print(f"Image shape at {resolution} m resolution: {betsiboka_size} pixels")
    
    evalscript_bands = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B02","B03","B04","B08"],
            }],
            output: {
                bands: 4,
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B02,
                sample.B03,
                sample.B04,
                sample.B08,
                ];
    }
"""
    
    request_bands = SentinelHubRequest(
        evalscript=evalscript_bands,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=("2019-08-21", "2019-08-21"),
                mosaicking_order=MosaickingOrder.LEAST_CC,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=kiyv_bbox,
        size=betsiboka_size,
        config=config,
        data_folder="results//",
    )
    
    bands_response  = request_bands.get_data()
    
    # print(f"Returned data is of type = {type(true_color_imgs)} and length {len(true_color_imgs)}.")
    # print(f"Single element in the list is of type {type(true_color_imgs[-1])} and has shape {true_color_imgs[-1].shape}")
    
    image = bands_response[0]
    # print(f"Image type: {image.dtype}")
    
    # plot function
    # factor 1/255 to scale between 0-1
    # factor 3.5 to increase brightness
    plot_image(image, factor=3.5 / 255, clip_range=(0, 1))# , factor=3.5 / 1e4, clip_range=(0, 1)#, factor=3.5 / 1e4, vmax=1 #, factor=3.5 / 255, clip_range=(0, 1))
    
    request_bands.save_data(show_progress=True)
    print(
        "The output directory has been created and a tiff file with all bands was saved into the following structure:\n"
    )
    
    for folder, _, filenames in os.walk(request_bands.data_folder):
        for filename in filenames:
            print(os.path.join(folder, filename))

try:
    os.mkdir('Results\\')
except FileExistsError:
    pass

config = SHConfig()
config.sh_client_id="aa98480f-8d30-4c49-95ac-68d419d09457"
config.sh_client_secret="norshf6xP41NXVtrmUFlUOPK5gWlu0Jz"
# config.data_folder="results//"
config.save("my-profile")
config = SHConfig("my-profile")


if not config.sh_client_id or not config.sh_client_secret:
    print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")
    
# first try
#get_tiff_file_from_sentinel(30.279350,50.343489, 30.514870,50.465591)#(29.907532,50.076532, 30.797424,50.511680)
#get_tiff_file_from_sentinel(30.514870,50.465591, 30.279350,50.617885)#(30.797424,50.511680, 30.332565,50.600455)
#get_tiff_file_from_sentinel(30.514870,50.617885, 30.825920,50.329026)#(30.797424, 50.511680, 31.475830,50.224367)

# idk what it is but let it stay
# get_tiff_file_from_sentinel(29.907532,50.076532, 30.797424,50.511680)

# what I chose
get_tiff_file_from_sentinel(30.197983,50.595879, 30.571518,50.316970)
get_tiff_file_from_sentinel(30.571518,50.316970, 30.842056,50.595879) 

# # by indentificators
# get_tiff_file_from_sentinel(30.178667516417683,49.53173120782476, 31.752783043838747,50.545333158635955)
# get_tiff_file_from_sentinel(30.12370823169888,50.45686117062749, 31.729300891794363,51.44399790803582)

