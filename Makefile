# Beispiel1:
# Sections to compare
CLI_FILE1 = tests/files/2019-10-16_CLIXML_zlib_1--1.2.11.dfsg-1-debian10-combined.tar.bz2_2019-10-16_06_29_02.xml
REPORT_FILE1 = tests/files/2019-10-16_zlib_1--1.2.11.dfsg-1-debian10-combined.tar.bz2_clearing_report_Wed_Oct_16_10_2019_06_28_46.docx 
#===================================== ===============  ======================================  
# 1. General Assessment                SECTION1/TABLE1  
#- 6.1 Notes on individual files       SECTION2/TABLE2  # only exists in report docx
#- 17. Irrelevant Files                SECTION3/TABLE3  DONE
#- 17.1 Comment for Irrelevant Files   SECTION4/TABLE4  # only exists in report (docx)
#===================================== ===============  ======================================  

CLIXML_SECTION_1 = 
REPORT_TABLE_1 = 
CLIXML_SECTION_2 = 
REPORT_TABLE_2 = 
CLIXML_SECTION_3 = IrrelevantFiles
REPORT_TABLE_3 = irrelevant-files
# ??????????????????????????????????????????????
CLIXML_SECTION_4 = ?????     ==>>  Does not exist
# ??????????????????????????????????????????????
REPORT_TABLE_4 = comment-for-irrelevant-files
VERBOSE  = -vv 

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	/bin/rm -fR docs
	/bin/rm -fR docs-source/-autosummary

black:
	poetry run  black tests
	poetry run  black fossmerge

doc:
	poetry run sphinx-build -b html docs-source docs/

test1: black
	poetry run  coverage run  --source=fossmerge -m pytest $(VERBOSE)  tests/test_analyze_report_file.py

test: black
	#poetry run  coverage run  --source=fossmerge -m pytest $(VERBOSE)  tests/test_analyze_report_file.py::test_that_the_state_xml_file_is_analyzed_as_expected_for_the_FIRST_values
	#poetry run  coverage run  --source=fossmerge -m pytest $(VERBOSE)  tests/test_analyze_report_file.py::test_that_the_state_xml_file_is_analyzed_as_expected_for_the_NON_FIRST_values
	#poetry run  coverage run  --source=fossmerge -m pytest $(VERBOSE)  tests/test_analyze_report_file.py
	poetry run  coverage run  --source=fossmerge -m pytest $(VERBOSE)  tests/test_fossmerge_big_files.py
	#poetry run  coverage run  --source=fossmerge -m pytest $(VERBOSE)  

# - 17. Comparing Irrelevant Files
run: black
	#Hinterläßt in fossmerge/fossmerge_cli.py:147   ctx.obj["CLIXML_FILE_NAME"] = clixml_file_name
	# einen ctx Eintrag in dem die Datei als  dict steht. 
	#poetry run python -m fossmerge  $(VERBOSE) analyze_clixml --clixml_file_name $(CLI_FILE1) # --clixml_section ALL
	# Hinterlaesst in  fossmerge/fossmerge_cli.py:126 ctx.obj["AVAILABLE_TABLES"] = convert_and_analyze_docx(report_file_name) 
	# einen ctx Eintrag: in dem der das report-xml dokument als dict drinn steht
	#poetry run python -m fossmerge $(VERBOSE)  analyze_report --report_file_name $(REPORT_FILE1)  --report_table_name ALL
	# Verbinde nun die vorigen Kommandos (clixml und report stehen als lokale dictionaries zur Verfügung)
	# und schaue wie man aktualisieren kann
	poetry run python -m fossmerge $(VERBOSE)   merge_report \
		--clixml_file_name $(CLI_FILE1) \
		--clixml_section $(CLIXML_SECTION_3) \
		--report_file_name $(REPORT_FILE1)\
		 --report_table_name  $(REPORT_TABLE_3)








	
