#!/usr/bin/python

import csv
import sys

class FSM_chat:
    __State = "Initial_State"
    _Input = "Initial_Input"
    _Content = '_Contents.csv'
    _Message = "Initial_Message"
    Error = False

    def __init__(self,Init_Input) -> None:
        self._initialize_Content(Init_Input)
        self.Process(Init_Input)
    
    def _initialize_Content(self, Init_Input):
        CsvRead = csv_file = csv.reader(open(self._Content, "r"), delimiter=",")
        for row in CsvRead:
            if Init_Input == row[1]:
                self._State = row[2]
                self._Content = row[3]
                self._Message == row[4]

    def Process(self,Input):
        self._Input = Input
        self.MainBody(True)

    def GiveMessage(self):
        return self._Message

    def MainBody(self,start):
        CsvRead = csv.reader(open(self._Content, "r"), delimiter=",")
        while True:
            start = (yield start)
            Found = False
            CsvRead.seek(0)
            for row in CsvRead:    
                if self._State == row[1]:
                    if self._Input == row[2]:
                        self._State == row[3]
                        self._Message == row[4]
                        Found = True
                        break
            if not Found:
                self.Error = True

    
