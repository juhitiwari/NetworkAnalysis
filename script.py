#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 10:47:39 2018

@author: slytherin
"""

import pandas as pd
import networkx as nx
book1=pd.read_csv("data/asoiaf-book1-edges.csv")
G_book1=nx.Graph()
books=[G_book1]
book_fnames=["data/asoiaf-book2-edges.csv","data/asoiaf-book3-edges.csv","data/asoiaf-book4-edges.csv","data/asoiaf-book5-edges.csv"]
for book_fname in book_fnames:
    book=pd.read_csv(book_fname)
    G_book=nx.Graph()
    for _,edge in book.iterrows():
        G_book.add_edge(edge['Source'],edge['Target'],weight=edge['weight'])
    books.append(G_book)
    
#impt characters in 1 and 5
deg_cen_book1=nx.degree_centrality(books[0])
deg_cen_book5=nx.degree_centrality(books[4])
sorted_deg_cen_book1=sorted(deg_cen_book1.items(),key = lambda x : x[1], reverse = True)[0:10]
sorted_deg_cen_book5=sorted(deg_cen_book5.items(),key = lambda x : x[1], reverse = True)[0:10]

#evolution of characters
evol=[nx.degree_centrality(book) for book in books]
degree_evol_df=pd.DataFrame.from_records(evol)
degree_evol_df[['Eddard-Stark', 'Tyrion-Lannister', 'Jon-Snow']].plot()

#importance with betweeness centrality
evolbet=[nx.betweenness_centrality(book,weight='weight') for book in books]
bet_evol_df=pd.DataFrame.from_records(evolbet).fillna(0)
set_of_char = set()
for i in range(5):
    set_of_char |= set(list(bet_evol_df.T[i].sort_values(ascending=False)[0:4].index))
list_of_char = list(set_of_char)
bet_evol_df[list_of_char].plot(figsize=(13,7))

#importance with pagerank
evolpage=[nx.pagerank(book) for book in books]
page_evol_df=pd.DataFrame.from_records(evolpage)
set_of_char = set()
for i in range(5):
    set_of_char |= set(list(page_evol_df.T[i].sort_values(ascending=False)[0:4].index))
list_of_char = list(set_of_char)
page_evol_df[list_of_char].plot(figsize=(13,7))

#corelating the three
measures=[nx.pagerank(books[4]),nx.betweenness_centrality(books[4],weight='weight'),nx.degree_centrality(books[4])]
cor=pd.DataFrame.from_records(measures)
print(cor.T.corr())

p_rank,deg_rank,bet_rank=cor.idxmax(axis=1)
print(p_rank,deg_rank,bet_rank)

   
