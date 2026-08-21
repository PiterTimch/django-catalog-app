FROM python:3.14-rc-slim AS build
WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .

RUN uv sync --frozen --no-dev

ARG SECRET_KEY=build-dummy-secret-key
RUN .venv/bin/python manage.py collectstatic --noinput


FROM python:3.14-rc-slim
WORKDIR /app

COPY --from=build /app /app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
