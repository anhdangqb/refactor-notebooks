"""This is the demo pipeline, that collect all scripts and combine with config file to run the pipeline."""
import os

import hydra
import pandas as pd
from hydra.utils import to_absolute_path as abspath
from omegaconf import DictConfig

from src.ingest import process_data  # Import steps from ingest


@hydra.main(config_path="../config", config_name="pipeline")
def run_pipeline(config: DictConfig):
    """This is the demo pipeline, that collect all scripts and combine with config file to run the pipeline.
    TO use:
    - Modify the config file in config/pipeline.yaml
    - Run the pipeline with command: python src/pipeline.py
    - This file is supposed run as script, not import to other scripts
    """
    raw_data_path = abspath(config.raw.path)
    processed_data_path = abspath(config.processed.path)
    process_config = config.processed.config

    print(f"Loading raw data from: {raw_data_path}")
    df = process_data(
        pd.read_excel(raw_data_path),
        process_config.null_cols,
        process_config.outlier_policies,
    )

    # If not exist, create
    if not os.path.exists(os.path.dirname(processed_data_path)):
        os.makedirs(os.path.dirname(processed_data_path))

    # Write output
    df.to_csv(processed_data_path, index=False)
    print(f"Write output data to: {processed_data_path}")


# This is the block to make sure that this file is run as a script
# rather than import to other scripts
if __name__ == "__main__":
    run_pipeline()
