# How to use Dockerfiles - Ubuntu++

# Start with a BASE IMAGE
# Here we will use the base image for ubuntu
FROM ubuntu:latest

# Let others know who maintains it
MAINTAINER "The CGC Team" cgc@sbgenomics.com

# Update ubuntu and install some necessary software
RUN apt-get update --yes \ 
	&& apt-get install wget build-essential zlib1g-dev libncurses5-dev vim --yes

# Now that we have our updated base image, let's install SamTools
# First we pull a specific version of SamTools from its repo and then install
RUN wget https://github.com/samtools/samtools/releases/download/1.2/samtools-1.2.tar.bz2 \
	&& tar jxf samtools-1.2.tar.bz2 \
	&& cd samtools-1.2 \
	&& make \ 
	&& make install

# Set a command that executes when you run the image
# In this case, open up a bash terminal 
CMD ["/bin/bash"]