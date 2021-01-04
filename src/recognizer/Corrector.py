# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 21:38:03 2019

@author: fabie
"""

from spellchecker import SpellChecker

class Corrector():
    
    def __init__(self,text):
        
        self.text = text
        self.wordList = None
        self.wordIndex = []
    
    def arrayConverter(self):
        
        wordStart = 0
        wordEnd = 0
        index = 0
        wordList = []
        
        for browser in self.text :
            index += 1
            if browser == ' ' :
                wordEnd = index
                wordList.append(self.text[wordStart:wordEnd-1])
                self.wordIndex.append((wordStart,wordEnd))
                wordStart = wordEnd
                         
        self.wordList = wordList
        
    def correct(self) :
        
        correctedText = ""
        self.arrayConverter()
        index = 0
        
        for word in self.wordList :
            
            if len(word) <= 2 :
                spell = SpellChecker(language='fr',distance=0) 
            
            elif 2 <= len(word) and len(word) < 5 :
                spell = SpellChecker(language='fr',distance=1)  
                
            elif 5 <= len(word) and len(word) < 8 :
                spell = SpellChecker(language='fr',distance=2)  
                
            elif 8 <= len(word) and len(word) < 15 :
                spell = SpellChecker(language='fr',distance=3)
                 
            misspelle = spell.unknown([word])
            
            if misspelle == set() or word == "caracteres":
                correctedText+=word+" "
                
            elif word != "caracteres" : 
                correctedText+=str(spell.correction(word))+" "
               
            index+=1

        return correctedText

        



 