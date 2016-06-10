# Use the Anaconda distribution of Python 2.7
FROM continuumio/anaconda:latest

# Update conda installer and all packages
RUN conda update conda --yes
RUN conda update --all --yes

# Install new packages here
RUN conda install numpy --yes
RUN conda install scikit-learn --yes
RUN pip install docopt==0.6.2

# Create 'pypackages.txt' which has the library of packages
RUN touch pypackages.txt
RUN pip freeze > echo >> pypackages.txt

CMD ["/bin/bash"]