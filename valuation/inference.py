import torch
from torch import Tensor
import torch.nn.functional as F

from model.mapfaster import MAPFASTER

config = {
    "encoder_se_reduction": 2,
    "encoder_body_channels": 4,
    "encoder_head_channels": 2,
    "encoder_dropout": 0,
    "block0_se_reduction": 4,
    "block0_body_in_channels": 8,
    "block0_body_out_channels": 16,
    "block0_head_channels": 8,
    "block0_dropout": 0,
    "predictor0_dropout": 0,
    "predictor0_linear_channels": 512,
}


def load_model(model_path: str) -> torch.nn.Module:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = MAPFASTER.init_from_config(config)

    state = torch.load(model_path, map_location=device)
    if isinstance(state, dict) and "model" in state:
        state = state["model"]

    model.load_state_dict(state)
    model.eval()
    model.to(device)

    return model


model = load_model("../_dummy-aDE5AJTbKk5nkDyHjk5JD9_6.pth")


def infer(tensor: Tensor):
    device = next(model.parameters()).device
    x = tensor.to(device)

    with torch.inference_mode():
        return model(x)
        #return F.softmax(model(x)) # for softmaxing if wanted
