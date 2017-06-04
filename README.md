# epi_pyscripts

## Requirements
* Python 2.7
* Virtualenv (recommended)

## Installation
```bash
# CLONE THE REPOSITORY FROM GITHUB
git clone https://github.com/zxqwerxz/epi_pyscripts.git

# CREATE A VIRTUALENV TO INSTALL REQUIRED PYTHON DEPENDENCIES
cd epi_pyscripts
virtualenv env
. env/bin/activate
pip install -r requirements.txt

# EVERY TIME YOU WANT TO RUN SOMETHING FROM THE PACKAGE, RUN:
. env/bin/activate

# EVERY TIME YOU ARE FINISHED WITH THE PACKAGE, RUN:
deactivate
```

I recommend making symlinks so you do not need to copy the python scripts
everywhere. Here is an example:
```bash
# LET'S ASSUME YOU HAVE YOUR DATA HERE
cd /home/jyzhou/data/project1

# CREATE A SYMLINK
ln -s /path/to/epipyscripts src

# NOW YOU CAN RUN THE SCRIPTS LIKE THIS:
python src/fetch_seq.py infile.csv human > outfile.fastq
```
