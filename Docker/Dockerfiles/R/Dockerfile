# How to use Dockerfiles - R

# Start with a BASE IMAGE
# Here we will use the base image rocker/r-base
# For more information: see https://hub.docker.com/_/r-base/
FROM rocker/r-base:latest

# Update
RUN apt-get update --yes

# Use the Rscript command to install R packages here

# You can install packages by using RUN as so:
#RUN Rscript -e "install.packages('ggplot2')"
#RUN Rscript -e "install.packages('plyr')"
#RUN Rscript -e "install.packages('reshape2')"

# Or, you can chain Rscript commands:
#RUN Rscript -e "install.packages('ggplot2')" && \
#	Rscript -e "install.packages('plyr')" && \
#	Rscript -e "install.packages('reshape2')"

# Finally, you can chain commands inside R:
RUN Rscript -e "install.packages('ggplot2'); \
				install.packages('plyr'); \
				install.packages('reshape2')"
RUN Rscript -e "install.packages('devtools'); \
				library(devtools); \
				install_github("docopt/docopt.R")"

# By default, the CMD for rocker is "R"; you can change this to go to the terminal
CMD ["/bin/bash"]

# If you need to add more R packages to your container, you can simply add more lines such as:
# 	RUN Rscript -e "install.packages('<package>')"
# or modify any of the implementations above, then rebuild the container. Docker will detect changes and update accordingly.