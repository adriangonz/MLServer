import pytest

from .models import SumModel


@pytest.mark.parametrize("ready", [True, False])
def test_ready(monkeypatch, data_plane, model_registry, ready):
    new_model = SumModel("sum-model-2", "1.2.3")
    model_registry.load(model_name=new_model.name, model=new_model)

    monkeypatch.setattr(new_model, "ready", ready)

    all_ready = data_plane.ready()

    assert all_ready == ready


@pytest.mark.parametrize("ready", [True, False])
def test_model_ready(monkeypatch, data_plane, sum_model, ready):
    monkeypatch.setattr(sum_model, "ready", ready)

    model_ready = data_plane.model_ready(sum_model.name)

    assert model_ready == ready


def test_infer(data_plane, sum_model, inference_request):
    prediction = data_plane.infer(sum_model.name, inference_request)

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == [21]
