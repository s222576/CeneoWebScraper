from app import app
from flask import render_template, request, redirect, url_for
from googletrans import Translator
from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import author, extract, homepage, opinions, product_id, products

dest = "en"
src = "pl"
translator = Translator()

def get_element(parent, selector, attribute = None, return_list = False):
    try:
        if return_list:
            return ", ".join([item.text.strip() for item in parent.select(selector)])
        if attribute:
            return parent.select_one(selector)[attribute]
        return parent.select_one(selector).text.strip()
    except (AttributeError, TypeError):
        return None

def translate(text, src=src, dest=dest):
    try:
        return translator.translate(text, src=src, dest=dest).text
    except (AttributeError, TypeError):
        print("Error")
        return ""

opinion_elements = {
    "author":["span.user-post__author-name"],
    "rcmd": ["span.user-post__author-recomendation > em"],
    "score": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "posted_on": ["span.user-post__published > time:nth-child(1)", "datetime"],
    "bought_on": ["span.user-post__published > time:nth-child(2)", "datetime"],
    "useful_for": ["button.vote-yes > span"],
    "useless_for": ["button.vote-no > span"],
    "pros": ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
    "cons": ["div.review-feature__title--negatives ~ div.review-feature__item", None, True]
}
