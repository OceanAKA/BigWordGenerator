from pickle import EMPTY_LIST
from typing import List
from flask import Flask, request, render_template, jsonify, redirect, url_for
import requests
import json
import string

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['u']
    text = text.translate(str.maketrans('','', string.punctuation))
    letters = text.split()
    finalSentence = ""
    ind = 0
    # args = request.args
    # sentence = args.get('name')


    for i in letters:
        word = letters[ind]
        api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(word)
        response = requests.get(api_url, headers={'X-Api-Key': 'jBFDd3xtpTwDCWOxX2rw0Q==sAXGrKHnaGAUefcz'})
        if response.status_code == requests.codes.ok:
            JSONStr = response.text
            synonyms = json.loads(JSONStr)
            for key, value in synonyms.items():
                if key == "synonyms":
                    if not value or len(word) < 3:
                        finalSentence += letters[ind] + " "
                    else:
                        if '_' in max(value,key=len):
                            while '_' in max(value, key=len):
                                del value[value.index(max(value, key=len))]
                            if len(max(value, key=len)) <= len(letters[ind]):
                                finalSentence += letters[ind] + " "
                            else:    
                                finalSentence += " " + max(value, key=len) + " "
                                print(finalSentence)          
                            # finalSentence += " " + sorted(value, key=len).lower() + " "
                        else:    
                            finalSentence += " " + max(value, key=len) + " "
                            print(finalSentence)                        
                    ind += 1
    else:
        print("Error:", response.status_code, response.text)  
    
    finalSentence = finalSentence.replace('_',' ')
    return render_template('index.html', sentenceOut=finalSentence)


if __name__ == "__main__":
    app.run(debug=True, port=8000)