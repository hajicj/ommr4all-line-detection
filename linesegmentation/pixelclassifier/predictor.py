from pagesegmentation.lib.predictor import Predictor, PredictSettings
from pagesegmentation.lib.dataset import DatasetLoader, SingleData
from linesegmentation.datatypes.datatypes import ImageData
import numpy as np
from typing import Generator, List
from scipy import misc


class PCPredictor:
    def __init__(self, settings: PredictSettings, height=20):
        self.height = height
        self.settings = settings
        self.predictor = Predictor(settings)

    def predict(self, images: List[ImageData]) -> Generator[np.array, None, None]:
        dataset_loader = DatasetLoader(self.height, prediction = True)
        data = dataset_loader.load_data(
            [SingleData(binary=i.image, image=i.image, line_height_px= i.height) for i in images]
        )
        for i, pred in enumerate(self.predictor.predict(data)):
            pred = misc.imresize(pred[0][pred[2].xpad:, pred[2].ypad:], pred[2].original_shape, interp="nearest")
            yield pred

