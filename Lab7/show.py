import rasterio
from matplotlib import pyplot as plt
import os
import numpy as np

for folder, _, filenames in os.walk('results/'):
    for filename in filenames:
        print(os.path.join(folder, filename))
        if '.json' not in filename:
            dataset = rasterio.open(os.path.join(folder, filename))
            print(dataset.shape)
            f, (ax1, ax2, ax3, ax4) = plt.subplots(1,4)
            band1 = dataset.read(1)
            band2 = dataset.read(2)
            band3 = dataset.read(3)
            band4 = dataset.read(4)
            
            ax1.imshow(band1)
            ax2.imshow(band2)
            ax3.imshow(band3)
            ax4.imshow(band4)
            plt.show()