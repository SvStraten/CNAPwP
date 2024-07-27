# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 13:53:07 2023

@author: Tamara Verbeek
"""
import pandas as pd
import numpy as np
import os
from Data import Data
from Utils.LogFile import LogFile
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

class Preprocess:
    def __init__(self, args):
        self.data = None
        self.args = args
        self.out_encoder = OneHotEncoder(sparse=False)
        self.one_encoder_event = OneHotEncoder(sparse=False)
        self.one_encoder_resource = OneHotEncoder(sparse=False)
        self.categories_event = None
        self.categories_resource = None
        self.k = args.prefix_length
        self.trace = 'case'
        self.contextdata = None
        
    def get_data(self):
        path = os.path.join(self.args.data_path, self.args.dataset)
        print(path)
        d = Data(self.args.dataset,
                 LogFile(filename=path, delim=",", header=0, rows=10000, time_attr="completeTime", trace_attr="case",
                         activity_attr='event', convert=False))
        d.logfile.keep_attributes(['event', 'completeTime'])
        listOfevents = [[value] for value in list(d.logfile.data['event'])]
        listOfevents.append(['0'])
        print('listOfevents')
        self.out_encoder.fit(listOfevents)
        self.one_encoder_event.fit(listOfevents)
        self.categories_event =  [1] * len(set([value for value in list(d.logfile.data['event'])])) #self.args.nrOfEvents
        print(len(self.categories_event))
        return d, len(self.categories_event)
    
    def sublists(self, my_dict):
        return list(map(list, zip(*my_dict.values())))

    def get_all_previous(self, contextdata):
        previous = {}
        for i in range(0, self.k):    
            print(np.array(self.contextdata['event_Prev'+str(i)]).reshape(-1,1))
            previous['prev'+str(i)] = list(self.one_encoder_event.transform(np.array(self.contextdata['event_Prev'+str(i)]).reshape(-1,1)))
        lists = self.sublists(previous)
        return lists

    def create_k_context(self):
        """
        Create the k-context from the current LogFile

        :return: None
        """
        print("Create k-context:", self.k)

        if self.k == 0:
            self.contextdata = self.get_data()

        if self.contextdata is None:
            result = map(self.create_k_context_trace, self.get_data()[0].logfile.data.groupby([self.trace], sort= False))
            self.contextdata = pd.concat(result, ignore_index=True)
        lists = self.get_all_previous(self.contextdata)
        
        targets = list(self.one_encoder_event.transform(np.array(self.contextdata['event']).reshape(-1,1)))
        return lists, self.get_data()[0].logfile.data, targets, len(self.categories_event)

    def create_k_context_trace(self, trace):
        contextdata = pd.DataFrame()

        trace_data = trace[1]
        shift_data = trace_data.shift().fillna('0')
        shift_data.at[shift_data.first_valid_index(), self.trace] = trace[0]
        joined_trace = shift_data.join(trace_data, lsuffix="_Prev0")
        for i in range(1, self.k):
            shift_data = shift_data.shift().fillna('0')
            shift_data.at[shift_data.first_valid_index(), self.trace] = trace[0]
            joined_trace = shift_data.join(joined_trace, lsuffix="_Prev%i" % i)
        contextdata = pd.concat([joined_trace, contextdata], ignore_index = True)
        contextdata = contextdata.astype("str", errors="ignore")
        return contextdata
