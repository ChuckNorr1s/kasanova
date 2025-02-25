# Use an official Python slim image.
FROM python:3.10-slim

# Set working directory.
WORKDIR /app

# Copy and install pip dependencies from requirements.txt.
# (Ensure your requirements.txt contains the long list of packages.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install curl
RUN apt-get update && apt-get install --assume-yes curl

# Install Poetry using the official install script.
RUN curl -sSL https://install.python-poetry.org | python3 -
# Ensure Poetry is on the PATH (default install location is /root/.local/bin)
ENV PATH="/root/.local/bin:${PATH}"

# Configure Poetry to install dependencies globally (disable virtualenv creation)
RUN poetry config virtualenvs.create false

# Copy the poetry project directory and install its dependencies.
COPY poetry_dir /app/poetry_dir
RUN cd poetry_dir && poetry install

# Copy the rest of your application code.
COPY . /app

# Copy and set the entrypoint script.
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint.
ENTRYPOINT ["/app/entrypoint.sh"]