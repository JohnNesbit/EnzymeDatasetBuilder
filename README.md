# EnzymeDatasetBuilder
This repository contains code for a web scraper that builds a dataset of enzyme's amino acid sequences and SMILEs of their substrates and products.

## 1. EC and Amino acid getter
This file accesses the Uniprot database to find enzymes and their names. The program then searches the MetaCyC database for the same enzyme for future use.
This file saves the uniprot and MetaCyC links for future use.

## 2. Chem url getter
This file loops through the MetaCyc links produced by the EC and Amino Acid getter and creates links to the chemical pages for each enzyme. Sadly, the file runs using pyautogui to
navigate through the website.

## 3. Chem getter
This file loops through the chemical page links and retrives the SMILE encodings from MetaCyC. It then saves them the csv files accesable through numpy.

## Format of ran dataset
With all of the files run sequentially they will produce 4 different directories. Each directory has a file for each enzyme found. One of these directories is significant: "chem" 
contains numpy csvs for each enzyme containing their subtrate's and product's SMILE encodings and the enzyme's aa encoding. Each enzyme's aa sequence is encoded into numbers via
simply assigning thier respective letter with a number. It is in this format to enable easy future one hot encoding.
