__doc__ = """"""
import os
import bs4 as bs
import pprint
from subprocess import Popen, PIPE
import logging

from fossmerge.exceptions import DocumentError, PandocGenerationError

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


def reset():
    """"""
    global AVAILABLE_TABLES
    logger.warning("Reset AVAILABLE_TABLES")
    for table in AVAILABLE_TABLES.keys():
        AVAILABLE_TABLES[table]["ROWS"] = list()


def convert_to_html(filename: str):
    """[Convert docx-file to html]
    :param filename: [Path to input (docx) File.]
    :type filename: str
    :return: [content of the with pandoc generated html file.]
    :rtype: [bytestring]
    """
    cmd = ["pandoc", filename, "-f", "docx+styles", "-o", "_report.html"]
    process = Popen(cmd, stdout=PIPE)
    message = f"Execute {cmd} in pid {process.pid}"
    logger.debug(message)
    out, err = process.communicate()
    exit_code = process.poll()
    message = (
        f"Execute {cmd} in pid {process.pid} Returned {exit_code} in {os.getcwd()}"
    )
    if exit_code != 0:
        fatal_message = f"Error generating html for {filename} : message {message}: stdout: {out} stderr: {err}"
        logger.fatal(fatal_message)
        raise PandocGenerationError(fatal_message)
    else:
        logger.debug(message)
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
    reset()  # Clear AVAILABE_TABLES Data
    return analyse(html_string)


def analyse(html_string: str):
    """[summary]

    :param html_string: [html string of report document.]
    :type html_string: str
    :return: [(AVAILABLE_TABLES, ld list of dictionaries having the content of the tables.)]
    :rtype: [(dict,dict)]

    We parse  "html_string" - and set what is needed. 
    All tables and "id" elements are on the same hierarchy-level of the document -
    a found <table> is correlated with the <id=...>  immediately found before. 
    The implementation of the parser  - sets an table-id based on the id 
    attribute of a h2/h3 tag. Maybe there comes a real table afterwards - in 
    that case we use the before given table-id to store the tables data 
    in the global  AVAILABLE_TABLES[table_id][ROWS] list.

    For debugging/tracing purposes we store the information (as list/dict)
    in the RESULT_DIR.

    NOTE:

        lxml's analysis of the html document behaves different on some plattforms.
        The  first tables data-nodes are returned as triple (on ubuntu) and  as 
        1,2,3-tuple on darwin. 
        That extra work is done in the FIRST tabel section.
    """
    soup = bs.BeautifulSoup(html_string, "lxml")
    if not os.path.isdir(RESULT_DIR):
        os.mkdir(RESULT_DIR)
    current_table_name = "FIRST"
    amount_tables = 0
    ld = {}
    for tag in soup.find_all(True):
        if tag.name == "h2" or tag.name == "h3":
            current_table_name = tag.attrs["id"]
        if tag.name == "table":
            amount_tables += 1
            rows_in_table = tag.find_all("tr")
            logger.debug(
                f"Table {amount_tables} Found - \
                using id {current_table_name} - \
                {len(rows_in_table)} rows. "
            )
            # Add the table data to AVAILABLE_TABLES[]["ROWS"]
            for row_number in range(len(rows_in_table)):
                tds = rows_in_table[row_number].find_all("td")
                row = [td.text.strip() for td in tds]
                AVAILABLE_TABLES[current_table_name]["ROWS"].append(row)
            (
                f' {current_table_name} has {len(AVAILABLE_TABLES[current_table_name]["ROWS"])} rows'
            )
            # generate each table as list of dict ==> eases debugging ....
            if True:
                ld[current_table_name] = []
                # for row in range(len(AVAILABLE_TABLES[current_table_name]["ROWS"])):
                for index, row in enumerate(
                    AVAILABLE_TABLES[current_table_name]["ROWS"]
                ):
                    d = {}
                    if current_table_name == "FIRST":
                        undefined_value = ""
                        length = len(
                            AVAILABLE_TABLES[current_table_name]["ROWS"][index]
                        )
                        if length == 0:
                            # XXX maybe remove the element ?? error came first with big document
                            d["Key"] = undefined_value
                            d["Value"] = undefined_value
                            d["Comment"] = undefined_value
                            logger.warning(
                                "FIRST TABLE:row{index} had a row without data (row_len is 0) inserted {d} "
                            )
                        elif length == 1:
                            d["Key"] = AVAILABLE_TABLES[current_table_name]["ROWS"][
                                index
                            ][0]
                            d["Value"] = undefined_value
                            d["Comment"] = undefined_value
                        elif length == 2:
                            d["Key"] = AVAILABLE_TABLES[current_table_name]["ROWS"][
                                index
                            ][1]
                            d["Key"] = undefined_value
                            d["Value"] = AVAILABLE_TABLES[current_table_name]["ROWS"][
                                index
                            ][0]
                            # d["Comment"] = undefined_value
                            d["Comment"] = AVAILABLE_TABLES[current_table_name]["ROWS"][
                                index
                            ][1]
                        elif length == 3:
                            d["Key"] = AVAILABLE_TABLES[current_table_name]["ROWS"][
                                index
                            ][0]
                            d["Value"] = AVAILABLE_TABLES[current_table_name]["ROWS"][
                                index
                            ][1]
                            d["Comment"] = AVAILABLE_TABLES[current_table_name]["ROWS"][
                                index
                            ][2]
                        else:
                            message = f'IMPOSSIBLE Data: FIRST table index:{index} has more than three ({length}) columns : \
                                data: {pprint.pformat(AVAILABLE_TABLES[current_table_name]["ROWS"][index])}'
                            logger.fatal(message)
                            raise DocumentError(message)

                        # Fix the rows, as on different oses different rows are returned with lxml
                        # XXX Fix lxml Usage
                        def fix_documents_row(index, row, new_row, message):
                            """"""
                            logger.warning(
                                f" table {current_table_name}:{index} has wrong len. {message}Fix it:  {row} becomes {new_row}"
                            )
                            AVAILABLE_TABLES[current_table_name]["ROWS"][
                                index
                            ] = new_row

                        if index == 0:
                            message = f"{index}: OSS Component Clearing report"
                            if len(row) == 1:
                                new_row = [row[0], "", ""]
                                fix_documents_row(index, row, new_row, message)
                        elif index == 1:
                            message = "{index}: Clearing Info , Department, GENERIC"
                            # ROW OK
                        elif index == 2:
                            message = f" Clearing Info , Prepared by , GENERIC"
                            if len(row) == 2:
                                new_row = ["", row[0], row[1]]
                                fix_documents_row(index, row, new_row, message)
                        elif index == 3:
                            message = f"{index}: Clearing Info , Reviewed  by , GENERIC"
                            if len(row) == 2:
                                new_row = ["", row[0], row[1]]
                                fix_documents_row(index, row, new_row, message)
                        elif index == 4:
                            message = (
                                "{index}: Clearing Info , Report Release date , GENERIC"
                            )
                            if len(row) == 2:
                                new_row = ["", row[0], row[1]]
                                fix_documents_row(index, row, new_row, message)
                        elif index == 5:
                            message = "{index}: Component Info , Community , GENERIC"
                            print(pprint.pformat(row))
                            # ROW OK
                        elif index == 6:
                            message = f"{index}: Component Info , Component, GENERIC"
                            if len(row) == 2:
                                new_row = ["", row[0], row[1]]
                                fix_documents_row(index, row, new_row, message)
                        elif index == 7:
                            message = f"{index}: Component Info , Version, GENERIC"
                            if len(row) == 2:
                                new_row = ["", row[0], row[1]]
                                fix_documents_row(index, row, new_row, message)
                        elif index == 8:
                            message = f"{index}: Component Info , hash, GENERIC"
                            if len(row) == 2:
                                new_row = ["", row[0], row[1]]
                                fix_documents_row(index, row, new_row, message)
                        elif index == 9:
                            message = (
                                f"{index}: Component Info , release_date , GENERIC"
                            )
                            if len(row) == 2:
                                new_row = ["", row[0], row[1]]
                                fix_documents_row(index, row, new_row, message)
                        elif index == 10:
                            messge = f"{index}: Component Info , main license, GENERIC"
                            if len(row) == 2:
                                new_row = ["", row[0], row[1]]
                                fix_documents_row(index, row, new_row, message)
                        elif index == 11:
                            message = (
                                f"{index}: Component Info , Other license, GENERIC"
                            )
                            # ROW OK
                        elif index == 12:
                            message = f"{index}: Component Info ,Fossology Upload/Package Link , GENERIC"
                            # ROW OK
                        elif index == 13:
                            message = (
                                "{index}: Component Info ,SW 360 Portal Link , GENERIC"
                            )
                            # ROW OK
                        elif index == 14:
                            message = f"{index}: Component Info ,Result of License Scan , GENERIC"
                            # ROW OK
                        else:
                            message = (
                                f"{index}: Impossible Index in  {current_table_name}"
                            )
                            logger.fatal(message)
                            raise DocumentError(message)

                    else:  # All tables beside FIRST
                        if current_table_name not in AVAILABLE_TABLES.keys():
                            message = f"{current_table_name}: Impossible Table Name. Update AVAILABLE_TABLES."
                            logger.fatal(message)
                            raise DocumentError(message)

                        if len(row) == 0:
                            logger.warning(
                                f'skip row {current_table_name}:{index} it is empty.  data: {row} - maybe it should be deleted from AVAILABLE_TABLES[{current_table_name}]["ROWS"]? '
                            )
                            continue

                        # Given the description in the tables COLUMN_CONTENT we are able to map each row
                        # to its given description.
                        for row_description_index, name in enumerate(
                            AVAILABLE_TABLES[current_table_name]["COLUMN_CONTENT"]
                        ):
                            d[name] = AVAILABLE_TABLES[current_table_name]["ROWS"][
                                index
                            ][row_description_index]
                        logger.debug(
                            f"Table {current_table_name}: ADDED dict {d} from row {row} at table offset: {index}"
                        )
                    ld[current_table_name].append(d)

                # if ctx.obj["DEBUG"]:
                #     print(f"START:  Current Table {current_table_name}")
                #     print(pprint.pformat(ld[current_table_name]))
                #     print(f"START:  Current Table {current_table_name}")

            # Save the list of the table
            with open(f"{RESULT_DIR}/{current_table_name}", "w") as fp:
                fp.write(pprint.pformat(AVAILABLE_TABLES[current_table_name]["ROWS"]))
            # Save the dict of the table
            with open(f"{RESULT_DIR}/{current_table_name}_d", "w") as fp:
                fp.write(pprint.pformat(ld))
    return AVAILABLE_TABLES, ld
