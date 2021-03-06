from typing import List

from .model import MLModel


class ModelRegistry:
    """
    Model registry interface, inspired in NVIDIA Triton's `model-repository`
    extension.
    """

    def __init__(self):
        self._models = {}

    def index(self):
        pass

    def load(self, model_name: str, model: MLModel):
        model.load()
        self._models[model_name] = model

    def unload(self):
        pass

    def get_model(self, model_name: str) -> MLModel:
        # TODO: Check if model exists
        # TODO: Handle model version
        return self._models[model_name]

    def get_models(self) -> List[MLModel]:
        return self._models.values()
