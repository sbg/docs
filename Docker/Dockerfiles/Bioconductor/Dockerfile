# How to use Dockerfiles - Bioconductor

# Start with a BASE IMAGE
# Here we will use the release_base image for Bioconductor
FROM bioconductor/release_base:latest

# Update the container
RUN apt-get update --yes

# More instructions for installing new Bioconductor packages can be found here: https://www.bioconductor.org/install/
# To add more Bioconductor packages, insert that package in "" in the list below
RUN Rscript -e 'source("http://bioconductor.org/biocLite.R"); biocLite(c("DESeq2", "limma", "edgeR"))'

# Set CMD to start up a terminal
CMD ["/bin/bash"]
