FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    make \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY native_parser/ /build/native_parser/
RUN cd /build/native_parser && make clean && make

FROM python:3.11-slim AS runner

RUN groupadd -g 10001 cloudvault && \
    useradd -u 10001 -g cloudvault -s /bin/bash -m cloudvault

WORKDIR /app

COPY --from=builder /root/.local /home/cloudvault/.local
COPY --from=builder /build/native_parser/libparser_secure.so /app/native_parser/libparser_secure.so
COPY --from=builder /build/native_parser/parser_secure /app/native_parser/parser_secure

COPY app/ /app/app/
COPY run.py /app/
COPY native_parser/parser_wrapper.py /app/native_parser/

RUN chown -R cloudvault:cloudvault /app /home/cloudvault

ENV PATH=/home/cloudvault/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER cloudvault

EXPOSE 5000

ENTRYPOINT ["python", "run.py", "--mode", "secure", "--port", "5000", "--host", "0.0.0.0"]
