# plot-drawing-tools

This is a collection of jupyter notebooks adn python scripts for drawing histograms created using [ntuple-tools](https://github.com/cerminar/ntuple-tools/).

## Browsing the notebooks

You can browse the actual notebook output clicking on the link:
[Notebook Viewer (NBViewer)](https://nbviewer.jupyter.org/github/cerminar/plot-drawing-tools/tree/v152/)Clone this repo in the `ntuple-tools` directory (see [ntuple-tools repository](https://github.com/cerminar/ntuple-tools)).

Install the `jupyter` packge in the venv you are using to run `ntuple-tools`:

`pip install plot-drawing-tools/requirements.txt`

Register the virtualeven as kernel:

`python kernel install --name "<venvname>" --user`

Start `jupyter notebook`:

`jupyter notebook`

or alternatively:

`root --notebook`

Select the kernel you just created to run the notebooks!

## Gettting started

An introduction to the functionality of the package can be found in the notebook

`notebooks/getting-started.ipynb`

## Automatically linking current branch to nbviewer

[nbviewer](https://nbviewer.org/) allows to display the notebook output from a github repository, including the javascript to display the ROOT plots correctly.

A `pre-commit` hook can be used to update the link in the `Browsing the notebooks` section of this README to point to the current branch.

To install the hook:

`cp python/pre-commit.py .git/hooks/pre-commit`


