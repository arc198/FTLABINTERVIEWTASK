from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import operator
import json

def index(request):
    return render(request, 'index.html', {})


word_count = {}
words = []
with open('word_search.tsv') as datafile:                   
    for row in datafile:
        word, frequency = row.split('\t')           
        word_count[word] = int(frequency.strip())   
        words.append(word)                          

# to find wether the word is existing or not

def search(letter):
    results = []
    for word in words:
        if letter in word:
            results.append(word)
    return results

# to find the mattched words containing letters entered by user
def sort(results, incomplete_word):
    word_length = [(result, result.find(incomplete_word), word_count[result], len(result)) for result in results]
    word_length.sort(key=operator.itemgetter(1))
    word_length.sort(key=operator.itemgetter(3))
    data = [word_length[0] for word_length in word_length][:25]
    return data


#Returns the autocomplete results while the user types in a letter.
def searchword(request):
    if request.is_ajax():
        query = request.GET.get('term','')
        results = sort(search(query.lower()), query.lower())
        data = json.dumps(results)
    else:
        data = 'fail'
    type = 'application/json'
    return HttpResponse(data, type)

# Returns a jsonresponse having the search results(25 words) containing the searched word(partial)
def Results(request):
    if request.method == 'GET':
        query = request.GET.get('term') # for example: query = 'hello'
        if query:
            data = sort(search(query.lower()), query.lower())
            if len(data) == 0:
                return JsonResponse({'output': "Word not found."})
            else:
                return JsonResponse({'output': data})
        else:
            return redirect('/')



