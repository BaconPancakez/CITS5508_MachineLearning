# CITS5508 Machine Learning

This repository contains coursework material for CITS5508, including weekly labs, assignments, DataCamp notebooks, and a small Flappy Bird game project.

## Repository structure

- `lab1` to `lab7`: Jupyter notebooks, datasets, and lab sheet resources for weekly lab activities.
- `asst_1`, `asst_2`: Assignment notebooks and related datasets/documents.
- `datacamp`: Practice notebooks and datasets for DataCamp-style ML tasks.
- `game`: A standalone Pygame Flappy Bird implementation and assets.
- `cits5508-2026.yml`: Conda environment specification used for the course tooling.

## Environment setup

Create and activate the Conda environment from the provided file:

```bash
conda env create -f cits5508-2026.yml
conda activate cits5508
```

The environment includes core ML and notebook tooling such as Python 3.11, NumPy, pandas, SciPy, scikit-learn, matplotlib, JupyterLab, and Graphviz-related packages.

## Working with notebooks

Launch JupyterLab from the repository root:

```bash
jupyter lab
```

Then open any notebook under `lab*`, `asst_*`, or `datacamp`.

## Running the Flappy Bird game

From the `game` directory:

```bash
python flappybird.py
```

Ensure the environment has `pygame` installed if it is not already available in your local setup.