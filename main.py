from flask import Flask, request
import pickle
from preprocessing import preprocess

app = Flask(__name__)

positive_model = pickle.load(open("models/positive.pkl", "rb"))
negative_model = pickle.load(open("models/negative.pkl", "rb"))


def analyze(tweets: list[str]):
    input = preprocess(tweets)

    pos_score = positive_model.predict_proba(input)[:, 1]
    neg_score = negative_model.predict_proba(input)[:, 1]

    final_score = [
        (
            round(pos_score[i], 2)
            if pos_score[i] > neg_score[i]
            else round(-1 * neg_score[i], 2)
        )
        for i in range(len(pos_score))
    ]

    return dict(zip(tweets, final_score))


@app.post("/analyze")
def sentiment_analysis():
    tweets = request.json

    if not tweets:
        return {"message": "You must provide at least one tweet"}, 400

    if not isinstance(tweets, list):
        return {"message": "You must provide a list of strings"}, 400

    return analyze(tweets)
