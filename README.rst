The fossreport cmdline 
======================

POC: Analyzing docx/clixml files and merging them.

Currently the docx-file analysis is based on pandoc==>html==>bs4 ==> dict.


**Even if using the same bs4 parser engine (lxml) the parse results are different on mac/ubuntu.**





  Commands:

  ============== =====================================
  Log            Add a Log Message to the log.
  analyze_clixml Extract data from clixml File.
  analyze_report Extract Table data from docx File.
  merge_report   Extract data from clixml File.
  ============== =====================================



Test
----


*make test*


Doc
---


*make doc*







