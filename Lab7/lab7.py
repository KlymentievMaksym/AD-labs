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

from sentinelhub import SHConfig

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

import datetime
import os

import matplotlib.pyplot as plt
import numpy as np

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
)

# The following is not a package. It is a file utils.py which should be in the same folder as this notebook.
# from utils import plot_image

def get_tiff_file(coords_x_1, coords_y_1, coords_x_2, coords_y_2, resolution=60):
    kiyv_coords_wgs84 = (coords_x_1, coords_y_1, coords_x_2, coords_y_2)
    
    # kiev_coords = np.array([29.073321247506765, 49.845775018245774, 31.986007792928522, 49.845775018245774, 31.986007792928522, 51.278667808079206, 29.073321247506765, 51.278667808079206,29.073321247506765, 49.845775018245774])
    # betsiboka_coords_wgs84 = (31.56, 31.55, 32.51, 32.58)
    
    kiyv_bbox = BBox(bbox=kiyv_coords_wgs84, crs=CRS.WGS84)
    
    betsiboka_size = bbox_to_dimensions(kiyv_bbox, resolution=resolution)
    
    print(f"Image shape at {resolution} m resolution: {betsiboka_size} pixels")
    
    evalscript_true_color = """
        //VERSION=3
    
        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"]
                }],
                output: {
                    bands: 3
                }
            };
        }
    
        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """
    
    request_true_color = SentinelHubRequest(
        evalscript=evalscript_true_color,
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
    
    true_color_imgs = request_true_color.get_data()
    
    # print(f"Returned data is of type = {type(true_color_imgs)} and length {len(true_color_imgs)}.")
    # print(f"Single element in the list is of type {type(true_color_imgs[-1])} and has shape {true_color_imgs[-1].shape}")
    
    image = true_color_imgs[0]
    # print(f"Image type: {image.dtype}")
    
    # plot function
    # factor 1/255 to scale between 0-1
    # factor 3.5 to increase brightness
    plot_image(image, factor=3.5 / 255, clip_range=(0, 1))
    
    request_true_color.save_data()
    print(
        "The output directory has been created and a tiff file with all bands was saved into the following structure:\n"
    )
    
    for folder, _, filenames in os.walk(request_true_color.data_folder):
        for filename in filenames:
            print(os.path.join(folder, filename))
            
get_tiff_file(29.907532,50.076532, 30.797424,50.511680)
get_tiff_file(30.797424,50.511680, 30.332565,50.600455)
get_tiff_file(30.797424, 50.511680, 31.475830,50.224367)
# get_tiff_file(29.907532,50.076532, 30.797424,50.511680)