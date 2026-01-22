FROM python:3.13.11-slim
#Copy from another docker image - uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
#Set the working directory
WORKDIR /code
# Add virtual environment to PATH so we can use installed packages
ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./
#Install dependencies from the uv.lock file to mirror dependencies installed in our virtual environment for reproducibility
RUN uv sync --locked

#RUN pip install pandas pyarrow

#Copy from the host machine to the docker image
COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]