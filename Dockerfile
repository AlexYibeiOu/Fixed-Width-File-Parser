# Dockerfile

FROM python:3.8

LABEL maintainer="Alex Ou" \
      name="Fixed_Width_File_Parser" \
      version="1.0"

RUN git clone https://github.com/AlexYibeiOu/Fixed-Width-File-Parser.git

WORKDIR /Fixed-Width-File-Parser/core