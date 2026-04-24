
from .definitions import definitions
import sys

help_message = """
oante -- literal toki pona translator
     To use this, simply type `oante` followed by
  whatever text you wish to translate, in
  quotes.
  
  Example:
   $ oante "toki a, ma o!"
   > hello emphasis, world hey!

     This tool is a little smart, looking at the
  surrounding words to determine if a specific
  term should be a modifier or not.

     Punctuation is preserved, spaces are not.
"""

toki_pona_letters = list("aeiouptklmnswj")
go_to_primary = [
     "li",
     "e",
     "en",
     "anu",
     "la"
]
singles = [
     "mi",
     "sina"
]

def split_punct(word):
     just_word = ""
     punct = ""

     for i, char in enumerate(word):
          if char.lower() not in toki_pona_letters:
               punct = word[i:]
               break
          just_word += char.lower()

     return (just_word, punct)

def translate(words):

     # what should be translated
     # primary and modifier
     translate_primary = True

     # the final result
     res = ""

     # have you already done the mi/sina thing
     done_special_subject = False

     # go through the words
     for word in words:

          # split punctuation
          w, p = split_punct(word)

          # get the literal translation of a word
          lit = definitions.get(w)
          if lit == None:
               res += w + p + " "
               continue

          # the correct word to use
          final = lit[1]
          if translate_primary:
               final = lit[0]
               translate_primary = False

          # reset translating primiary
          if w in go_to_primary:
               translate_primary = True
          elif w in singles and not done_special_subject:
               translate_primary = True
               done_special_subject = True

          # reset sentences
          if p.isspace():
               done_special_subject = False
               translate_primary = True

          # get the base translation
          res += final + p + " "

     return res

def main():

     # print out the help message if you wish to have it
     if len(sys.argv) == 2 and sys.argv[1] == "-h":
          print(help_message)
          return

     # error with too few arguments
     if len(sys.argv) == 1:
          print(" >> You need to provide the text to translate! << ")
          return

     # make sure all the words are fine
     words = " ".join(sys.argv[1:]).split(" ")

     # finally, translate the whole thing
     res = translate(words)
     print(res)

