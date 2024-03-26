"""
Script for validating trained OCR models.
"""

import pathlib

import click
from torch.utils.data import DataLoader

from fast_plate_ocr import utils
from fast_plate_ocr.config import load_config_from_yaml

# Custom metris / losses
from fast_plate_ocr.dataset import LicensePlateDataset


@click.command(context_settings={"max_content_width": 140})
@click.option(
    "-m",
    "--model",
    "model_path",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=pathlib.Path),
    help="Path to the saved .keras model.",
)
@click.option(
    "--config-file",
    default="./config/arg_plates.yaml",
    show_default=True,
    type=click.Path(exists=True, file_okay=True, path_type=pathlib.Path),
    help="Path pointing to the model license plate OCR config.",
)
@click.option(
    "-a",
    "--annotations",
    default="assets/benchmark/annotations.csv",
    show_default=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=pathlib.Path),
    help="Annotations file used for validation.",
)
@click.option(
    "-b",
    "--batch-size",
    default=1,
    show_default=True,
    type=int,
    help="Batch size.",
)
def valid(
    model_path: pathlib.Path,
    config_file: pathlib.Path,
    annotations: pathlib.Path,
    batch_size: int,
) -> None:
    """Validate a model for a given annotated data."""
    config = load_config_from_yaml(config_file)
    model = utils.load_keras_model(
        model_path, vocab_size=config.vocabulary_size, max_plate_slots=config.max_plate_slots
    )
    val_torch_dataset = LicensePlateDataset(annotations_file=annotations, config=config)
    val_dataloader = DataLoader(val_torch_dataset, batch_size=batch_size, shuffle=False)
    model.evaluate(val_dataloader)


if __name__ == "__main__":
    valid()
