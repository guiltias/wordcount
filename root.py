#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect

from Levenshtein import distance

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

def canonize(source, stop_symbols, stop_words):
  stop_symbols += '\n\r'
#'.,!?:;-\n\r()'
  return ([x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words.split())] )


def calc_distance(comments, sample):
    for item in comments:
        if distance(sample, item) < 5:
            return item

def substring(string1,string2):
    for char in string2:
	string1 = string1.replace(char, "")
    return string1


app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/compute", methods = ['GET', 'POST'])
def compute():
    if request.method!="POST":
        return render_template("result.html", result=[])
    elif request.method=="POST":
	original_text = request.form["text"]
        #text = canonize(original_text, request.form["stop_symbols"], request.form["stop_words"])
        text = original_text.split() 
 	words = request.form["words"].split()
	l = int(request.form["lev"])
	print "dist: ", l
	marked_text = ""
	
	# remove duplicates
	words = list(set(words))
	# prepare counts
	result = dict()

	for i in range(0, l + 1):
		result[i] = dict()
		for word in words:
			result[i][word] = 0
	for word in text:
 		tmp_word = word
		word = word.lower()
		for sample in words:
			sample = sample.lower()
			stripped_word = substring(word, request.form["stop_symbols"])
			d = distance(sample, stripped_word)
			diff = len(substring(stripped_word, sample))
			if d<=l and len(stripped_word) - diff >= 2:
				#print "escape: " + (substring(word,sample)).encode('utf-8') + " " + word.encode('utf-8') + " "+ sample.encode('utf-8') + " " + str(diff)
				result[d][sample] += 1
				tmp_word = "<b>" + tmp_word + " ("+sample+", d=" + str(d)+")</b> "
		marked_text += tmp_word+" "
        return render_template("result.html", result=result, overview=marked_text)

app.run(host='0.0.0.0', port=8080)



#http_server = HTTPServer(WSGIContainer(app))
#http_server.listen(8080)
#IOLoop.instance().start()

