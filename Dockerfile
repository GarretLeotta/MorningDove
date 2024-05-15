# using ubuntu LTS version
FROM ubuntu:24.04 AS builder

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends -y python3.12 python3.12-dev python3.12-venv python3-pip python3-wheel build-essential && \
	apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3.12 -m venv /home/morningdove/venv
ENV PATH="/home/morningdove/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

FROM ubuntu:24.04 AS runner
RUN apt-get update && \
    apt-get install --no-install-recommends -y python3.12 python3-venv && \
	apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --create-home morningdove
COPY --from=builder /home/morningdove/venv /home/morningdove/venv

USER morningdove
RUN mkdir /home/morningdove/app
WORKDIR /home/morningdove/app
COPY . .

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/morningdove/venv
ENV PATH="/home/morningdove/venv/bin:$PATH"

WORKDIR /home/morningdove/app/src
CMD ["python", "main.py"]