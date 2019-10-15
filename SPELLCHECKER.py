#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
#########################################################################
####################    SPELLCHECKER         ############################
###################   USING NLTK LIBRARY     ############################
#########################################################################
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
	 
################ LIBRARY IMPORT ################
	 
import nltk
from nltk.util import ngrams
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
 
	 
############### PREPROCESSING #######################################
	   
def preprocessing():
    """Loading the data from 'NUCLEARCORPUS.TXT Returning the whole dictionary as data."""
data = []
with open('NUCLEARCORPUS.txt', 'r') as file:
    data = file.read().replace('\n', '')

 
############## TOKENIZATION OF DATA LOADED IN THE PROGRAM #############  
	 
from nltk.tokenize import sent_tokenize, word_tokenize
tokens = word_tokenize(data)
"""counter = 0
for w in tokens:
   counter+=1
   print(counter,".",w)
lenght = len(tokens)        
lenght"""
	 
tokens = [word.lower() for word in tokens]  ### converting the text to lower case
tokens = [word for word in tokens if word.isalpha()]  ### This cleans the unwanted characters from the tokens
print(tokens)
	 
 
################## UNIQUE FREQUENCY LIST OF TOKENS #########################
	 
import nltk
unig_freq = {}
unig_freq = nltk.FreqDist(tokens)
	 
################  BUILDING BIGRAMS AND MAKING FREQUENCY LIST   ################
	 
bigrams = list(nltk.bigrams(tokens)) # makes bigrams from tokens
   
bigram_freq = {}
length = len(tokens)
for i in range(length-1):
    bigram = (tokens[i], tokens[i+1])
    if bigram not in bigram_freq:
        bigram_freq[bigram] = 0
        bigram_freq[bigram] += 1
	   
bigrams_with_frequency_one = 0
bigrams_with_frequency_two = 0
for bigram in bigram_freq:
    if bigram_freq[bigram] == 1:
        bigrams_with_frequency_one += 1
    elif bigram_freq[bigram] == 2:
        bigrams_with_frequency_two += 1

############# Minimum edit distace == 2  #######################

from collections import Counter
import re


def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(data))
WORDS

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): return (e2 for e1 in edits1(word) for e2 in edits1(e1))
	 
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
#########################################################################
####################    SPELLCHECKER GUI     ############################
###################   USING TKINTER LIBRARY  ############################
#########################################################################
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
	 
###### IMPORTING THE LIBRARY tkinter FOR BUILDING GUI ###################
	 
from tkinter import *
import tkinter as tk
 
############## FIXING THE HEIGHT & WIDTH OF THE TAB #####################
 
HEIGHT = 500
WIDTH = 600
	 
	 
root = tk.Tk()
root.title('SPELL-CHECKER')  # Title for the spellchecker
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
	 
############  FIXING THE BACKGROUND IMAGE ###############################
	 
filename = tk.PhotoImage(file = 'landscape.png')
background_label = tk.Label(image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
canvas.pack()
 
##############     INPUT SENTENCE FRAME     #############################
	 
Real = []  # real words list
Error = [] # error words list
	 
def color_text(e, tag, word, fg_color='black', bg_color='white'):  # highlighting the error words
	    # add a space to the end of the word
	    word = word + " "
	    e.insert('end', word)
	    end_index = e.index('end')
	    begin_index = "%s-%sc" % (end_index, len(word) + 1)
	    e.tag_add(tag, begin_index, end_index)
	    e.tag_config(tag, foreground=fg_color, background=bg_color)
	 
def enter(): # defing the button for suggestions
    global e
    string = e.get('1.0', END)
    sstring = word_tokenize(e.get("1.0",'end-1c'))
   
	   
    for word in sstring:   # detecting Non-word
        if word in unig_freq:
            Real.append(word)
        if word in bigram_freq:
            Real.append(word)
        if word not in unig_freq:
            Error.append(word)
   
 
        print(string)
   
	 

for x in range(len(Error)):
    wrong = correction(Error[x])
    if (len(Error[x]) ==1) or (wrong[0] == Error[x]):
        continue
    else:
        wrong = correction(Error[x])
        sugesstion = known(edits2(Error[x]))
        
        

        #print(sugesstion)
        #print(wrong)

frame = tk.Frame(root, bg='#80c1ff', bd=2.5)
frame.place(relx=0.4, rely=0.05, relwidth=0.75, relheight=0.4, anchor='n')  
 
e = tk.Text(frame, wrap="word")
e.place(relwidth=0.75, relheight=1)
e.pack()    
e.focus_set()
 
	 
button = tk.Button(root, text="Enter", command= enter)
button.place(relx=0.8,rely=0.2, relheight=0.075, relwidth=0.1)
	 
def clear(): # clearing
    e.delete('1.0',END)
	 
button = tk.Button(root, text="Clear", command= clear)
button.place(relx=0.8,rely=0.3, relheight=0.075, relwidth=0.1)
 
############  WORD SUGGESTION FRAME     #######################
 
def sugess():
    for x in range(len(Error)):
        wrong = correction(Error[x])
        if (len(Error[x]) ==1) or (wrong[0] == Error[x]):
            continue
        else:
            wrong = correction(Error[x])
            sugesstion = known(edits2(Error[x]))
            print(sugesstion)
            print(wrong)
    
     ## highlight            
            string = e.get('1.0', END)
            sentenct_words = string.split()
            tags = ["tg" + str(k) for k in range(len(sentenct_words))]
            e.delete('1.0', END)
            for ix, word in enumerate(sentenct_words):
                if word[:len(word)] == word in Error:
                    color_text(e, tags[ix], word, 'blue', 'orange')
                else:
                    color_text(e, tags[ix], word) 
            
            for i in sugesstion:
                SGS.insert('end', i)
	   
#limit suggestions
def delete():
    Error.clear()
    Real.clear()
    SGS.delete(0, tk.END)  
	       
frame2 = tk.Frame(root, bg='chartreuse2', bd=2.25)
frame2.place(relx=0.4, rely=0.5, relwidth=0.75, relheight=0.3, anchor='n')
	 
SGS = tk.Listbox(frame2)
SGS.place(relwidth=0.99, relheight=1)
	 
suggestion_button = tk.Button(root, text="Suggestion", command = sugess)
suggestion_button.place(relx=0.8,rely=0.5, relheight=0.075, relwidth=0.12)
suggestion_delete = tk.Button(root, text="Clear", command = delete)
suggestion_delete.place(relx=0.8,rely=0.6, relheight=0.075, relwidth=0.1)
	 
	 
########### CORRECT WORD FRAME ################################
	 
new_words = []
def fix(): # correction
    CRCT.delete('1.0', END)
   
    
    sent_string = e.get('1.0', END)

    for s_word in Error:
        new_words.append(correction(s_word))
        sent_string = sent_string.replace(s_word,correction(s_word))
    

    CRCT.insert('end', sent_string)
    
  
frame3 = tk.Frame(root, bg='cyan2', bd=2.25)
frame3.place(relx=0.4, rely=0.85, relwidth=0.75, relheight=0.1, anchor='n')
CRCT= tk.Text(frame3)
CRCT.place(relwidth=0.99, relheight=1)
Correction_button = tk.Button(root, text="Correction", command = fix)
Correction_button.place(relx=0.8,rely=0.85, relheight=0.075, relwidth=0.12)

root.mainloop()
