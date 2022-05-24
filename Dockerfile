FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/wf-base:fbe8-main


RUN python3 -m pip install Cython &&\
    python setup. py install &&\
    python3 -m pip install Cython --install-option="--no-cython-compile"

# Or use managed library distributions through the container OS's package
# manager.
RUN apt-get update -y &&\
    apt-get install -y autoconf samtools

# Its easy to build binaries from source that you can later reference as
# subprocesses within your workflow.
# RUN git clone https://github.com/mills-lab/vapor.git &&\
#     cd vapor &&\
#     python setup.py install --user &&\
#     export PATH=$PATH:$HOME/.local/bin

# You can use local data to construct your workflow image.  Here we copy a
# pre-indexed reference to a path that our workflow can reference.
# COPY data /root/reference
# ENV BOWTIE2_INDEXES="reference"

COPY wf /root/wf

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
