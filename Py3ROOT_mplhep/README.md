# Py3ROOT Macros

## Status - 8th September 2021
The best incarnation of any plotting macro is to use Python3 in accordance with ROOT.

Python3.7 works well with non-ROOT modules: mplhep, uproot, boost-histogram, hist etc.

Current deployment of ROOT on local machine only works with Python3.6 therefore requires some compromises. Plotting macros less simple.

Therefore current options are:
* Design a plotting macro in Python3.6 which relies only minimally on mplhep. ROOT usage also in Python3.6
* Design a plotting macro in Python3.7, having converted ROOT histograms into pythonic objects beforehand. This can probably accomplishped by some PyHEP means but likely only in Python3.7
* Built ROOT for Python3.7. Fundamentally the only thing gained is the hep.histplot command 

Uproot version continues unrelated.