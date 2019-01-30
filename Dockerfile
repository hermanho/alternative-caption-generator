FROM ubuntu:18.04

RUN apt-get update -y --fix-missing
RUN apt-get install -y \
    build-essential \
    curl \
    wget \
    python3.6 \
    python3.6-dev \
    python3.6-distutils \
    python3.6-venv

RUN curl -fSL "https://bootstrap.pypa.io/get-pip.py" | python3.6

ADD $PWD/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

ADD ./init.sh /app/
ADD ./bin/download_model.py /app/bin/download_model.py
ADD ./etc/word_counts.txt /app/etc/word_counts.txt
ADD ./medium_show_and_tell_caption_generator /app/medium_show_and_tell_caption_generator
ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 5000
# testing
# CMD ["/bin/bash"]

#production
# CMD ["python3", "./app/bin/download_model.py", "--model-dir", "./etc"]
# CMD ["python3", "./app/medium_show_and_tell_caption_generator/httpapp.py"]
CMD ["/bin/bash", "./app/init.sh"]
