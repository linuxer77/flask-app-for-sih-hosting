import os
import json
import requests
from groq import Groq
from flask import Flask, render_template, jsonify, request, redirect, url_for
from app import app
from serpapi import GoogleSearch

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    client = Groq()

    def get_all_info():
        client = Groq()
        content_for_language = f"Tell me what language is this, country of origin and the country currency, separate them each by space. For language answer in two-letter language code. (e.g., en for English, es for Spanish, or fr for French, for country answer in a two-letter country code. (e.g., us for the United States, uk for United Kingdom, or fr for France) Head to the Google countries page for a full list of supported Google countries. And For the currency  Head to the Google Travel Currencies page for a full list of supported currency codes for ex- for dollar it's USD. Sample input query: 'जबलपुर में लोकप्रिय होटल' sample output: 'hi in INR', Don't give any other text just give tell me language, country of origin, country currency, and without any inverted commas or anything. My current query is: {query}"

        completion_language = client.chat.completions.create(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=[
                {
                    "role": "system",
                    "content": "best free hotel apis\n"
                },
                {
                    "role": "user",
                    "content": f"{content_for_language}"
                }
            ],
            temperature=0.5,
            max_tokens=1024,
            top_p=0.65,
            stream=True,
            stop=None,
        )

        detected_language = ""
        for text in completion_language:
            detected_language += text.choices[0].delta.content or ""
        
        return detected_language


    
    client = Groq()
    content = "You're an intelligent language translation model, you have to translate any give input into english and my current prompt is "

    completion = client.chat.completions.create(
        model="llama3-groq-70b-8192-tool-use-preview",
        messages=[
            {
                "role": "system",
                "content": "best free hotel apis\n"
            },
            {
                "role": "user",
                "content": f"{content} + '{query}' + and don't give any other response apart from translating the message, also don't add any "" or anything else in the output "
            }
        ],
        temperature=0.5,
        max_tokens=1024,
        top_p=0.65,
        stream=True,
        stop=None,
    )

    translated_query = ''
    for chunk in completion:
        translated_query += chunk.choices[0].delta.content or ""

    params = {
        "engine": "google_hotels",
        "q": f"{translated_query}",
        "check_in_date": "2024-09-18",
        "check_out_date": "2024-09-28",
        "adults": "1",
        "currency": f"{get_all_info()[6:]}", # Cuurency of the country
        "gl": f"{get_all_info()[3:5]}", # Country in the 2 word form
        "hl": f"{get_all_info()[:2]}", # Language in the 2 word form
        "api_key": "94d60742b92907667abcf9ebb2682c70c3c89bd7f974054e1e3a614b5d40dbd9" 
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return jsonify(results)
