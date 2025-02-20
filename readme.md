# Social Media Sentiment Analysis

## Group

    Thierry Pavone TCHOUAMOU PAYONG
    Paul-Henry NGANKAM NGOUNOU
    Oumou Khairy GUEYE
    Maxime Loïc NKWEMI NJIKI

## Description

This project is a web api that analyzes the sentiment of a given list of tweets.

## Installation

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Database

To quickly set up a mysql database and phpMyAdmin interface with docker compose, run the following command:

```bash
docker-compose up -d
```

## Training

To train the models, run the following commands:

```bash
python training/vectorizer_training.py
python training/positive_training.py
python training/negative_training.py
```

## Usage

To run the application, run the following command:

```bash
flask --app main run
```
