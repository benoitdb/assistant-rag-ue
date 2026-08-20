# SDK Streamlit natif de Hugging Face Spaces déprécié depuis 2025-04-30
# (voir https://huggingface.co/docs/hub/en/spaces-changelog) — Dockerfile
# suivant le template officiel recommandé en remplacement (SDK Docker).

FROM python:3.11-slim

RUN useradd -m -u 1000 user

WORKDIR /app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .

USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

EXPOSE 7860

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
