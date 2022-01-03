from datetime import date, datetime
from django.http.response import JsonResponse
from django.shortcuts import render
import random
import json
import torch
from main.models import ExpenseRecord
from nlp.model import NeuralNet
from nlp.nltk_utils import bag_of_words, tokenize

# Create your views here.
from django.http import HttpResponse


def predict(sentence):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open("./nlp/intents.json", "r") as f:
        intents = json.load(f)

    FILE = "./nlp/data.pth"

    data = torch.load(FILE)
    input_size = data["input_size"]
    output_size = data["output_size"]
    hidden_size = data["hidden_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)

    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.5:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return [intent["tag"], random.choice(intent["responses"])]


def action(request):
    data = {}
    command = str(request.GET["command"])
    output = predict(command)
    if output[0] == "ADD_EXPENSE":
        data["action"] = "ADD_EXPENSE"
        data["reply"] = output[1]
    elif output[0] == "SHOW_EXPENSES":
        data["action"] = "SHOW_EXPENSES"
        data["reply"] = output[1]
    else:
        data["action"] = "REPLY"
        data["reply"] = output[1]
    return JsonResponse(data)


def addRecord(request):
    item_name = request.GET["item_name"]
    item_cost = request.GET["item_cost"]
    username = request.GET["username"]
    new_expense = ExpenseRecord(username=username, amount=item_cost, currency="INR", date_time=datetime.now(
    ), date=date.today(), month=date.today().month, year=date.today().year, category="GENERAL", comments = item_name)
    new_expense.save()
    data = {}
    data["action"] = "REPLY"
    data["reply"] = "Hooray! Item added to your expense records."
    return JsonResponse(data)

MONTHS_INDEX={
    "JAN":1,
    "FEB":2,
    "MAR":3,
    "APR":4,
    "MAY":5,
    "JUN":6,
    "JUL":7,
    "AUG":8,
    "SEP":9,
    "OCT":10,
    "NOV":11,
    "DEC":12
}

def showRecords(request):
    username = request.GET["username"]
    month = request.GET["month"]
    month = predict(month)
    if len(month)==3:
        month = MONTHS_INDEX[month]
    records = ExpenseRecord.objects.filter(username = username, month=month)
    data = {}
    data["action"] = "LIST_EXPENSES"
    data["list"] = json.dumps(records)
    return JsonResponse(data)




