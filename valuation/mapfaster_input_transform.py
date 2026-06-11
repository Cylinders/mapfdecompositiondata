from pathlib import Path

import cv2
import numpy as np
import numpy.typing as npt
import torch
from torch import Tensor

from structs import Grid, Agent, GridPath

FREE = np.array((255, 255, 255), dtype=np.uint8)  # white
OBSTACLE = np.array((255, 0, 0), dtype=np.uint8)  # red
START = np.array((0, 255, 0), dtype=np.uint8)  # green
GOAL = np.array((0, 0, 255), dtype=np.uint8)  # blue
PATH = np.array((0, 0, 0), dtype=np.uint8)  # black

Path("../dump").mkdir(exist_ok=True)


def encode_cuts(grid: Grid, paths: dict[Agent, GridPath], batch: list[list[list[Agent]]]) -> Tensor:
    h, w = grid.shape
    images: list[npt.NDArray[np.uint8]] = []

    for cut in batch:
        for group in cut:
            image = np.empty((h, w, 3), dtype=np.uint8)

            image[grid] = OBSTACLE
            image[~grid] = FREE

            for agent in group:
                for x, y in paths[agent]:
                    image[y, x] = PATH

            for agent in group:
                sx, sy = agent.start
                gx, gy = agent.goal

                image[sy, sx] = START
                image[gy, gx] = GOAL

            images.append(image)

    # debug imade dump
    for i, rgb in enumerate(images):
        cv2.imwrite(
            f"../dump/image_{i}.png",
            cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR),
        )

    rgb_batch = np.stack(images, axis=0)
    return preprocess_rgb_batch(rgb_batch)


IMAGE_SIZE = 320

IMAGENET_MEAN = torch.tensor([0.485, 0.456, 0.406])[:, None, None]
IMAGENET_STD = torch.tensor([0.229, 0.224, 0.225])[:, None, None]


def preprocess_rgb_one(rgb: npt.NDArray[np.uint8]) -> torch.Tensor:
    assert rgb.ndim == 3 and rgb.shape[2] == 3
    assert rgb.dtype == np.uint8

    h, w, _ = rgb.shape

    scale = IMAGE_SIZE / max(h, w)
    new_w = round(w * scale)
    new_h = round(h * scale)

    resized = cv2.resize(rgb, (new_w, new_h), interpolation=cv2.INTER_NEAREST)

    padded = np.zeros((IMAGE_SIZE, IMAGE_SIZE, 3), dtype=np.uint8)

    top = (IMAGE_SIZE - new_h) // 2
    left = (IMAGE_SIZE - new_w) // 2
    padded[top:top + new_h, left:left + new_w] = resized

    x = torch.from_numpy(padded).permute(2, 0, 1).float() / 255.0
    return (x - IMAGENET_MEAN) / IMAGENET_STD  # [3, 320, 320]


def preprocess_rgb_batch(batch: npt.NDArray[np.uint8]) -> torch.Tensor:
    assert batch.ndim == 4 and batch.shape[-1] == 3
    assert batch.dtype == np.uint8

    return torch.stack([preprocess_rgb_one(img) for img in batch], dim=0)
