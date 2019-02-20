# orcid-search
Python CLI for searching the ORCID public API

## Clone this repository to your machine

1. `git clone https://github.com/ORCID/orcid-search.git`

## Set up virtual environment 

1. `cd orcid-search`

2. `virtualenv venv`

3. `source ./venv/bin/activate` nix systesm `\venv\bin\activate` windows

4. `pip2 install -r requirements.txt` 

*Note: If you are running MacOS High Sierra, you may receive an error installing the packages in requirements.txt. To fix, install Xcode command line tools* `xcode-select --install`

## Run script

    python search_orcid.py --search=[affiliation organization name(s) to search] --file=[path to save results file]