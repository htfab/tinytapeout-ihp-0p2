# Build Tiny Tapeout with OpenLane 2

## Environment setup

```bash
export OPENLANE2_ROOT=~/openlane2
```

Then install OpenLane 2 with Nix, as explained [here](https://openlane2.readthedocs.io/en/latest/getting_started/nix_installation/index.html), taking care of the following:

1. Look at the value of `OPENLANE_TAG` in [.github/config/openlane.txt](.github/config/openlane.txt) to find the exact OpenLane 2 commit you need to check out. Installing a different version will likely not work, as OpenLane 2 is still in beta and the API is not very stable.

2. Clone OpenLane 2 to ~/openlane2 (or change the value of the `OPENLANE2_ROOT` environment variable).

## Repository setup

First, make sure that you have checked out the submodules:

```bash
git submodule update --init
```

Then install all the Python dependencies. You may want to use a virtual enviroment (venv or similar).

```bash
pip install -r tt-multiplexer/py/requirements.txt -r tt/requirements.txt
```

## Fetching the projects

Run the following commands to generate the configuration for building Tiny Tapeout:

```bash
python tt/configure.py --update-shuttle
```

## Harden

```bash
nix-shell ${OPENLANE2_ROOT}/shell.nix --run "cd tt/rom && python build.ihp-sg13g2.py"
nix-shell ${OPENLANE2_ROOT}/shell.nix --run "cd tt-multiplexer/ol2/tt_ctrl && python build.py"
nix-shell ${OPENLANE2_ROOT}/shell.nix --run "cd tt-multiplexer/ol2/tt_mux && python build.py"
python tt/configure.py --copy-macros
nix-shell ${OPENLANE2_ROOT}/shell.nix --run "cd tt-multiplexer/ol2/tt_top && python build.py"
```

You'll find the final GDS in `tt-multiplexer/ol2/tt_top/runs/RUN_*/final/gds/openframe_project_wrapper.gds`. To copy it (along with the lef, gl verilog, and spef files), run:

```bash
python tt/configure.py --copy-final-results
```
