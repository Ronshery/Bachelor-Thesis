FROM python:3.8-slim

RUN useradd -m perona

USER perona

WORKDIR /home/perona/benchmarking-operator

ENV PATH="/home/perona/.local/bin:${PATH}"

COPY --chown=perona:perona . .

RUN pip install --user -r requirements.txt

ENTRYPOINT ["python", "main.py"]