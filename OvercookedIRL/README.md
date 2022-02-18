# OvercookedIRL

## Setup Instructions

Create "overcooked" environment from environment.yml file (first time only):


    conda env create -f environment.yml
    conda activate overcooked
Make sure the active enivronment is using conda's version of pip, not the system's version of pip. That way, conda-env can automatically keep track of packages installed/removed with pip:

    conda install pip
Updating the environment.yml file after you add or remove packages:

    conda env export > environment.yml

Updating the conda environment from someone else's new environment.yml file:

    conda env update --prefix ./env --file environment.yml  --prune

## Running the Game
Run main.py:

    python main.py



