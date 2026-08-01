FROM python:3.10-slim

WORKDIR /app


# Copy requirements or install dependencies directly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY db.py frontend.py modelmain.py entrypoint.sh /app/

RUN chmod +x entrypoint.sh

EXPOSE 8501

ENTRYPOINT ["./entrypoint.sh"]