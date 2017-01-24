# Documentation example

FROM ubuntu
MAINTAINER "Kate Hodesdon" kate.hodesdon@sbgenomics.com

RUN apt-get update && apt-get install wget build-essential zlib1g-dev libncurses5-dev \
 && wget https://github.com/samtools/samtools/releases/download/1.2/samtools-1.2.tar.bz2 \
&& tar jxf samtools-1.2.tar.bz2 && cd samtools-1.2 && make && make install --force-yes
