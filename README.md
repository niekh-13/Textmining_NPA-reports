# Textmining_NPA-reports

## Summary

This repository provides all the code associated with the Master Thesis "Predicting cognitive tests scores for patients with primary braintumors by using sentence
embedding on neuropsychologists’reports", authored by Niek Huijsmans for the partial fulfillment of the requirements for the joint UvA-VU degree of Master of 
Science in Bioinformatics and Systems Biology. Both R code and Python3 code can be found. Results might differ a bit compared to those reported in the thesis, due
to updated packages.

## Usage
### Cleaning medical notes for uniformality
```
python3 cleaner.py
```
### Parsing of section in NPA reports
```
python3 Parser.py
```
### Datasplit for testing/training and validation (90%/10%)
```
python3 inclussion_data.py
```
### Sentence embedding
```
python3 SBERT.py
```
### t-SNE dimension reduction
```
python3 tSNE.py
```
### PLSR
```
python3 PLSR_socio+bert.py
```
or
```
python3 PLSR_socio+mpnet.py
```
### LARS
```
python3 LARS_socio+bert.py
```
or
```
python3 LARS_socio+mpnet.py
```
### Validation
```
python3 final_lars.py
```
## Patients inclussion
<img src="./figures/Minor 1.png">

*Fig 1. Flow chart of patient inclusion, allocation, analysis and validation.*

## Authors ##
### Authors: ###
- Niek Huijsmans
- Sander Boelders
- Karin Gehring

### Contributers: ###
- Sander Boelders

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**

