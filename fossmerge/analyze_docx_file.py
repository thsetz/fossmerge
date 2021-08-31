__doc__ = """"""
import os
import bs4 as bs
import pprint
from subprocess import Popen, PIPE
import logging

logger = logging.getLogger(__name__)


RESULT_DIR = ".foss_merge_resultfiles"
AVAILABLE_TABLES = {
    "FIRST": {
        "COLUMN_CONTENT": ("Key", "Value", "Comment"),
        "ROWS": [],
        "COMMENT": "First table in html - no id given.",
    },
    "assessment-summary": {
        "COLUMN_CONTENT": ("Key", "Value"),
        "ROWS": [],
        "COMMENT": " Second Table in html. No explicit columns defined.",
    },
    # id required-license-compliance-tasks: only id on h2 level :: NO Table
    "required-license-compliance-tasks": {
        "COLUMN_CONTENT": None,
        "ROWS": [],
        "COMMENT": "It is an id on h2 immedeately followed by a \
                    new Id (referencing common-obligations-restrictions-and-risks \
                    on a h3 tag: ==> not implemented  ",
    },
    "common-obligations-restrictions-and-risks": {
        "COLUMN_CONTENT": ("Key", "Value"),
        "ROWS": [],
        "COMMENT": "on h3",
    },
    "additional-obligations-restrictions-risks-beyond-common-rules": {
        "COLUMN_CONTENT": (
            "Obligation",
            "License",
            "License section reference and short Description",
        ),
        "ROWS": [],
        "COMMENT": "on h3;",
    },
    "acknowledgements": {
        "COLUMN_CONTENT": (
            "Reference to the license",
            "Text of acknowledgements",
            "File path",
        ),
        "ROWS": [],
        "COMMENT": "",
    },
    "export-restrictions": {
        "COLUMN_CONTENT": ("Statements", "Comments", "FilePath"),
        "ROWS": [],
        "COMMENT": "",
    },
    "intellectual-property": {
        "COLUMN_CONTENT": ("Statements", "Comments", "File path"),
        "ROWS": [],
        "COMMENT": "",
    },
    # id: notes: only id on h2 level :: NO Table
    "notes": {"TABLE_ID": "notes", "COLUMN_CONTENT": None, "ROWS": [], "COMMENT": ""},
    "notes-on-individual-files": {
        "COLUMN_CONTENT": ("License name", "Comment Entered", "File path"),
        "ROWS": [],
        "COMMENT": "",
    },
    "results-of-license-scan": {
        "COLUMN_CONTENT": ("Scanner count", "Concluded license count", "License name"),
        "ROWS": [],
        "COMMENT": "",
    },
    "main-licenses": {
        "COLUMN_CONTENT": ("License name", "License text", "File path"),
        "ROWS": [],
        "COMMENT": "",
    },
    "other-oss-licenses-red---do-not-use-licenses": {
        "COLUMN_CONTENT": ("License name", "License text", "File path"),
        "ROWS": [],
        "COMMENT": "",
    },
    "other-oss-licenses-yellow---additional-obligations-to-common-rules-e.g.-copyleft": {
        "COLUMN_CONTENT": ("License name", "License text", "File path"),
        "ROWS": [],
        "COMMENT": "",
    },
    "other-oss-licenses-white---only-common-rules": {
        "COLUMN_CONTENT": ("License name", "License text", "File path"),
        "ROWS": [],
        "COMMENT": "",
    },
    "overview-of-all-licenses-with-or-without-obligations": {
        "COLUMN_CONTENT": ("License ShortName", "Obligation"),
        "ROWS": [],
        "COMMENT": "",
    },
    "copyrights": {
        "COLUMN_CONTENT": ("Statements", "Comments", "File path"),
        "ROWS": [],
        "COMMENT": "",
    },
    "copyrights-user-findings": {
        "COLUMN_CONTENT": ("Statements", "Comments", "File path"),
        "ROWS": [],
        "COMMENT": "",
    },
    "bulk-findings": {
        "COLUMN_CONTENT": ("License name", "License text", "File path"),
        "ROWS": [],
        "COMMENT": "",
    },
    # id: non-functional-licenses : only id on h2 level :: NO Table
    "non-functional-licenses": {"COLUMN_CONTENT": None, "ROWS": [], "COMMENT": "",},
    "irrelevant-files": {
        "COLUMN_CONTENT": ("Path", "Files", "Licenses"),
        "ROWS": [],
        "COMMENT": "",
    },
    "comment-for-irrelevant-files": {
        "COLUMN_CONTENT": ("License name", "Comment Entered", "File path"),
        "ROWS": [],
        "COMMENT": "",
    },
    # ?? not available in all files
    "do-not-use-files": {"COLUMN_CONTENT": (), "ROWS": [], "COMMENT": ""},
    # ?? not available in all files
    "comment-for-do-not-use-files": {"COLUMN_CONTENT": (), "ROWS": [], "COMMENT": "",},
    "clearing-protocol-change-log": {
        "COLUMN_CONTENT": ("Last Update", "Responsible", "Comments"),
        "ROWS": [],
        "COMMENT": "",
    },
}


def convert_to_html(filename: str):
    """[Convert docx-file to html]
    :param filename: [Path to input (docx) File.]
    :type filename: str
    :return: [content of the with pandoc generated html file.]
    :rtype: [type]
    """
    cmd = ["pandoc", filename, "-f", "docx+styles", "-o", "_report.html"]
    process = Popen(cmd, stdout=PIPE)
    message = f"Execute {cmd} in pid {process.pid}"
    logger.info(message)
    out, err = process.communicate()
    exit_code = process.poll()
    if exit_code != 0:
        logger.fatal(f"Fatal error: {out} / {error}")
        raise
    else:
        message = (
            f"Execute {cmd} in pid {process.pid} Returned {exit_code} in {os.getcwd()}"
        )
        logger.info(message)
        assert os.path.isfile("_report.html")
        return open("_report.html", "rb").read()


def convert_and_analyze_docx(filename: os.path):
    """[summaryi]
    :param filename: [Path to input File.]
    :type filename: str
    :return: [content of the with pandoc generated html file.]
    :rtype: [type]

    """

    html_string = convert_to_html(filename)
    return analyse(html_string)


def analyse(html_string: str):
    """[summary]

    :param html_string: [html string of report document.]
    :type html_string: str
    :return: [list of dictionaries having the content of the tables.]
    :rtype: [type]

    We parse  "html_string" - and set what is needed. 
    All tables and "id" elements are on the same hierarchy-level of the document -
    a found <table> is correlated with the <id=...>  immediately found before. 
    The implementation of the parser  - sets an table-id based on the id 
    attribute of a h2/h3 tag. Maybe there comes a real table afterwards - in 
    that case we use the before given table-id to store the tables data 
    in the global  AVAILABLE_TABLES[table_id][ROWS] list.

    For debugging/tracing purposes we store the information (as list/dict)
    in the RESULT_DIR.



    """
    soup = bs.BeautifulSoup(html_string, "lxml")
    if not os.path.isdir(RESULT_DIR):
        os.mkdir(RESULT_DIR)
    current_id = "FIRST"
    amount_tables = 0
    for tag in soup.find_all(True):
        if tag.name == "h2" or tag.name == "h3":
            current_id = tag.attrs["id"]
        if tag.name == "table":
            amount_tables += 1
            rows_in_table = tag.find_all("tr")
            logger.info(
                f"Table {amount_tables} Found - \
                using id {current_id} - \
                {len(rows_in_table)} rows. "
            )
            # Add the tabl data to AVAILABLE_TABLES[]["ROWS"]
            for row_number in range(len(rows_in_table)):
                tds = rows_in_table[row_number].find_all("td")
                row = [td.text.strip() for td in tds]
                AVAILABLE_TABLES[current_id]["ROWS"].append(row)

            # generate each table as list of dict ==> eases debugging ....
            ld = []
            for row in range(len(AVAILABLE_TABLES[current_id]["ROWS"])):
                d = {}
                if current_id == "FIRST":
                    # Currently the FIRST table has 1-3 columns - fix this here to
                    # Always three columns
                    # "COLUMN_CONTENT": ("Key","Value","Comment"),
                    if len(AVAILABLE_TABLES[current_id]["ROWS"][row]) == 1:
                        d["Key"] = AVAILABLE_TABLES[current_id]["ROWS"][row][0]
                        d["Value"] = None
                        d["Comment"] = None
                    elif len(AVAILABLE_TABLES[current_id]["ROWS"][row]) == 2:
                        d["Key"] = AVAILABLE_TABLES[current_id]["ROWS"][row][0]
                        d["Value"] = AVAILABLE_TABLES[current_id]["ROWS"][row][1]
                        d["Comment"] = None
                    elif len(AVAILABLE_TABLES[current_id]["ROWS"][row]) == 3:
                        d["Key"] = AVAILABLE_TABLES[current_id]["ROWS"][row][0]
                        d["Value"] = AVAILABLE_TABLES[current_id]["ROWS"][row][1]
                        d["Comment"] = AVAILABLE_TABLES[current_id]["ROWS"][row][2]
                    else:
                        logger.fatal(
                            "IMPOSSIBLE Data: FIRST table has more than three columns: "
                        )
                        raise
                else:
                    for elem in enumerate(
                        AVAILABLE_TABLES[current_id]["COLUMN_CONTENT"]
                    ):
                        # elems are e.g. (0, 'Statements') (1, 'Comments') (2, 'File path')
                        d[elem[1]] = AVAILABLE_TABLES[current_id]["ROWS"][row][elem[0]]

                    logger.debug(f'row: {AVAILABLE_TABLES[current_id]["ROWS"][row]}')
                    if len(d.keys()) != len(AVAILABLE_TABLES[current_id]["ROWS"][row]):
                        print(
                            f'table {current_id}:{row} \n d  {len(d.keys())} \n {len(AVAILABLE_TABLES[current_id]["ROWS"][row])}'
                        )
                ld.append(d)

            # Save the list of the table
            with open(f"{RESULT_DIR}/{current_id}", "w") as fp:
                fp.write(pprint.pformat(AVAILABLE_TABLES[current_id]["ROWS"]))
            # Save the dict of the table
            with open(f"{RESULT_DIR}/{current_id}_d", "w") as fp:
                fp.write(pprint.pformat(ld))
    return AVAILABLE_TABLES
