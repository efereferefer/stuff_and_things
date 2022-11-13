#!/usr/bin/python

import csv
import sys
import asyncio

class FSM_chat:
    _State = "Initial_State"
    _Input = "Initial_Input"
    _Content = 'contents.csv'
    _Message = "Initial_Message"
    _MainBody = None
    Error = False

    def __init__(self,Init_Input) -> None:
        self._initialize_Content(Init_Input)
        self.Process(Init_Input)
    
    def _initialize_Content(self, Init_Input):
        self._MainBody = self.MainBody()
        CsvRead = csv.reader(open(self._Content, "r"), delimiter=",")
        for row in CsvRead:
            if Init_Input == row[0]:
                self._State = row[1]
                self._Content = row[2]
                self._Message = row[3]
                
                

    def Process(self,Input):
        self._Input = Input
        self._MainBody.send(None)
        

    def GiveMessage(self):
        if self.Error == True:
            return "Error"
        if self._Message == "echo":
            return self._Input
        return self._Message

    async def MainBody(self):
        CsvRaw = open(self._Content, "r")
        while True:
            await asyncio.sleep(0)
            CsvRaw.seek(0)
            Found = False
            CsvRead = csv.reader(open(self._Content, "r"), delimiter=",")
            for row in CsvRead:    
                print(row)
                if self._State == row[0]:
                    if self._Input == row[1] or row[1] == "any":
                        self._State = row[2]
                        self._Message = row[3]
                        Found = True
                        break
            if not Found:
                self.Error = True

    
