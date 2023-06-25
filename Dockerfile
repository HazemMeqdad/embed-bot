FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install python-dotenv

ENV TOKEN="discord token"
ENV HOST="your host link"
ENV PUBLIC_KEY="your discord bot key"
ENV APPLICATION_ID="your discord bot it"
ENV PORT="your host port"

RUN if [ -f .env ]; then python -m dotenv .env; fi

RUN python register_commands.py

CMD ["python", "app.py"]
