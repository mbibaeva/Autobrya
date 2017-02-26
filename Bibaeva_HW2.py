#английский, украинский, белорусский, русский, французский языки
#сначала берём текст, который будем разбирать
def take_text(filename):
    file = open(file_name, 'r', encoding = 'utf-8')
    text = file.read()
    return text

print('Подождите, пока соберутся статьи....')

#потом собираем тексты по языкам
import wikipedia
import re

def get_texts_for_lang(lang, n = 10): #я немного поправила функцию, чтобы если какие-то статьи пропускались, число текстов всё равно оставалось одинаковым
    wikipedia.set_lang(lang)
    wiki_content = []
    more_texts = n
    while more_texts > 0:
        page_name = wikipedia.random(1)
        try:
            page = wikipedia.page(page_name)
            more_texts -= 1
        except wikipedia.exceptions.WikipediaException:
            #print('Skipping page {}'.format(page_name))
            continue
        wiki_content.append('{}\n{}'.format(page.title, page.content.replace('==', '')))
    return wiki_content

langs = ['en', 'fr', 'de', 'ru', 'uk', 'be']        
wiki_texts = {}
for lang in langs:
    wiki_texts[lang] = get_texts_for_lang(lang, 5)
    print (lang, len(wiki_texts[lang]))
print('finish')

# Первый метод: частотный словарь
import codecs
import collections
import sys

def tokenize(text):
    words = text.split(' ')
    for word in words:
        word = word.strip('0123456789?\)\(\";:\.,«»')
    return words

def do_it(corpus):
    freqs = collections.defaultdict(lambda: 0)
    if type(corpus) is list:
        for article in corpus:
            for word in tokenize(article.replace('\n', '').lower()):
                freqs[word] += 1      
    elif type(corpus) is str:
        for word in tokenize(corpus.replace('\n', '').lower()):
            freqs[word] += 1      
    freqs = sorted(freqs, key=lambda w: freqs[w], reverse=True)[:50]
    return freqs

def method_1(text, wiki_text, langs):
    default = 0
    info = collections.defaultdict(lambda: 0)
    my_freqs = do_it(text)
    for lang in langs:
        corpus = wiki_texts[lang]
        freqs = do_it(corpus)
        for x in my_freqs:
            if x in freqs:
                info[lang] += 1
    val = info.values()
    for x in info:
        if info[x] == max(val):
            return x

# Второй метод: н-граммы

from itertools import islice, tee

def make_ngrams(text):
    N = 3 
    ngrams = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(text, N))))
    ngrams = [''.join(x) for x in ngrams]
    return ngrams

corpus = wiki_texts[lang]
def make_it(corpus):
    freqs = collections.defaultdict(lambda: 0)
    if type(corpus) is list:
        for article in corpus:
            for ngram in make_ngrams(article.replace('\n', '').lower()):
                freqs[ngram] += 1
    elif type(corpus) is str:
        for ngram in make_ngrams(article.replace('\n', '').lower()):
            freqs[ngram] += 1
    freqs = sorted(freqs, key=lambda n: freqs[n], reverse=True)[:50]
    return freqs

def method_2(text, wiki_texts, langs):
    default = 0
    info = collections.defaultdict(lambda: 0)
    my_freqs = do_it(text)
    for lang in langs:
        corpus = wiki_texts[lang]
        freqs = make_it(corpus)
        for x in my_freqs:
            if x in freqs:
                info[lang] += 1
    val = info.values()
    for x in info:
        if info[x] == max(val):
            return x

#выбор метода
def choose_method(text):        
    method = input('Если частотный словарь, введите 1. \n Если n-граммы, введите 2. \n Если оба, введите 3: ')
    if method == '1':
        print(method_1(text, wiki_texts, langs))
    elif method == '2':
        print(method_2(text, wiki_texts, langs))
    elif method == '3':
        print('По частотному словарю: ' + str(method_1(text, wiki_texts, langs)))
        print('По n-граммам: ' + str(method_2(text, wiki_texts, langs)))

file_name = str(input('Введите имя файла: '))
choose_method(take_text(file_name))
