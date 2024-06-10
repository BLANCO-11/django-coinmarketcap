# Crypto Coin Data Extraction API

Welcome to the Crypto Coin Data Extraction API! This Django application is designed to scrape and provide data on various cryptocurrencies from CoinMarketCap. This API facilitates easy access to up-to-date information on a wide range of crypto coins.

## Features

- Extract and retrieve cryptocurrency data from CoinMarketCap.
- Utilize Celery for asynchronous task processing.
- Leverage Redis for message brokering.

## Prerequisites

Before running this application, ensure you have the following installed:

- Python 3.x
- Redis
- Django
- Celery
- Chrome WebDriver (if using Selenium for web scraping)

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/BLANCO-11/django-coinmarketcap.git
cd coinmarketcap_project
```

2. **Create a virtual environment:**

```bash
python -m venv venv
```

3. **Activate the virtual environment:**

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

4. **Install the dependencies:**

```bash
pip install -r requirements.txt
```

## Running the Application

Before starting the Django server, you need to start Celery and Redis. A batch file (`start_celery_with_redis.bat`) has been provided for convenience.

1. **Start Celery and Redis:**

   On Windows, run the batch file:

```bash
start_celery_with_redis.bat
```

2. **Run the Django server:**

```bash
python manage.py runserver
```

## Usage

Once the server is running, you can access the API at `http://127.0.0.1:8000/`.

### API Endpoints

- `/api/taskmanager/start_scraping` - [POST] Payload Input url which are names of the crypto coins (['bitcoin', 'cardano']) request is to be run for these coins parallely and returns back a job id.
- `/api/taskmanager/scraping_status/<job_id>` - [GET] From the job_id received in the previous API, we can query this API and it will return the currently scraped data for that job.

## Images

Below are some proof-of-working images of the application. Replace the URLs with your image paths.

1. ![Image 1](https://i.imgur.com/A1VdVdo.png)
2. ![Image 2](https://i.imgur.com/uih8Sze.png)
3. ![Image 3](https://i.imgur.com/U6T5q76.png)
4. ![Image 4](https://i.imgur.com/v78lYqK.png)
5. ![Image 5](https://i.imgur.com/C4J53Id.png)
6. ![Image 6](https://i.imgur.com/S1oVq1L.png)
7. ![Image 7](https://i.imgur.com/oWTHKDK.png)

