__doc__ = """"""
import logging
import os
import pprint
import sys
from logging.handlers import RotatingFileHandler
from .analyze_docx_file import RESULT_DIR, AVAILABLE_TABLES, convert_and_analyze_docx
from .analyze_clixml_file import convert_clixml_to_xmldict, check_xmldict, diff_xmldict
import click

# logger = logging.getLogger(__name__)
logger = logging.getLogger("fossmerge")
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

FOSS_LOGGING_MAP = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
MAX_SIZE_OF_LOGFILE = 200000
MAX_NUMBER_OF_LOGFILES = 5


def make_list_of_dicts(rows: list, columns: list):
    """"""
    list_of_dicts = list()
    for row in rows:
        assert len(row) == len(columns)
        d = dict()
        for i in range(len(row)):
            d[columns[i]] = row[i]
        list_of_dicts.append(d)
    return list_of_dicts


@click.group()
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Increase verbosity level (e.g. -v -vv). Default is 0.",
)
@click.option(
    "--log_to_console/--no_log_to_console",
    is_flag=True,
    default=True,  # print logging events >= WARNING by default on console
    help="Send logging output to console. Default is --log_to_console.",
)
@click.option(
    "--log_to_file/--no_log_to_file",
    is_flag=True,
    default=False,
    help="Send logging output to File. Default is --no_log_to_file.",
)
@click.option(
    "--log_file_name",
    default=".fossreport.log",
    help="Specify log File Name if log is sent to file.  Default is .fossreport.log.",
)
@click.pass_context
def cli(ctx, verbose, log_to_console, log_to_file, log_file_name):
    """The fossreport cmdline client analyzing docx/clixml files and merging them.  """
    # group_commands = ["Log", "CreateFolder", "CreateGroup"]  # noqa: F841
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    if log_to_file:
        logfile_handler = RotatingFileHandler(
            log_file_name,
            maxBytes=MAX_SIZE_OF_LOGFILE,
            backupCount=MAX_NUMBER_OF_LOGFILES,
        )
        logfile_handler.setFormatter(formatter)
        logger.addHandler(logfile_handler)
    logger.setLevel(FOSS_LOGGING_MAP.get(verbose, logging.DEBUG))
    ctx.obj["VERBOSE"] = verbose


@cli.command("Log")
@click.option(
    "--log_level", default=0, help="Set the log_level of the message [0,1,2]."
)
@click.option("--message_text", default="log message", help="Text of the log message.")
@click.pass_context
def Log(ctx, log_level, message_text):
    """Add a Log Message to the log.  If a log message is printed to the log depends
       on  the verbosity defined starting the foss_cli (default level 0 /-v level 1/-vv level 2).
       Beeing on global verbosity level 0 only messages of --log_level 2 will be printed.
       Beeing on global verbosity level 1  messages of --log_level 1 and 2 will be printed.
       Beeing on global verbosity level 2 messages of --log_level 0,1,2 will be printed.
       Where the log messages are printed depends on the global configuration for --log_to_console,
       --log_to_file and --log_file_name.
    """

    if log_level == 0:
        logger.debug(message_text)
    elif log_level == 1:
        logger.info(message_text)
    elif log_level == 2:
        logger.warning(message_text)
    else:
        error_text = "Impossible Log Level in Log command."
        logger.fatal(error_text)
        raise click.UsageError(error_text, ctx=ctx)


@cli.command("analyze_report")
@click.option("--report_file_name", help="The name of the Report (docx) File.")
@click.option("--report_table_name", help="The Name of the Table.")
@click.pass_context
def analyze_report(ctx, report_file_name, report_table_name):
    """Extract Table data from docx File."""
    logger.debug(
        f"analyze_report called with file_name {report_file_name} table_name {report_table_name} "
    )

    if report_table_name not in AVAILABLE_TABLES.keys():
        logger.fatal(f"{report_table_name} not a valid report Table name")
        sys.exit(2)
    ctx.obj["FILE_NAME"] = report_file_name
    ctx.obj["TABLE_NAME"] = report_table_name
    ctx.obj["AVAILABLE_TABLES"] = convert_and_analyze_docx(report_file_name)

    # if report_table_name:
    #    logger.debug(pprint.pformat(f'{ctx.obj["AVAILABLE_TABLES"][table_name]}'))
    # else:
    #    logger.debug(pprint.pformat(f'{ctx.obj["AVAILABLE_TABLES"]}'))
    logger.debug(f"FIN: analyze_report ")


@cli.command("analyze_clixml")
@click.option("--clixml_file_name", help="The name of the clixml() File.")
@click.pass_context
def analyze_clixml(ctx, clixml_file_name):
    """Extract  data from clixml File."""
    logger.debug(f"analyze_clixml called with file_name {clixml_file_name} ")
    ctx.obj["CLIXML_FILE_NAME"] = clixml_file_name
    ctx.obj["CLIXML_DICT"] = convert_clixml_to_xmldict(clixml_file_name)
    modified, ctx.obj["CLIXML_NORMALIZED_DICT"] = check_xmldict(ctx.obj["CLIXML_DICT"])
    if modified:
        logger.warning(f"analyze_clixml  {clixml_file_name} format hat to be changed ")
        diff_xmldict(ctx.obj["CLIXML_NORMALIZED_DICT"], ctx.obj["CLIXML_DICT"])
    else:
        logger.debug(f"analyze_clixml  {clixml_file_name} format was OK ")


@cli.command("merge_report")
@click.option("--clixml_file_name", help="The name of the clixml() File.")
@click.option(
    "--clixml_section", help="The name of the clixml section to check against."
)
@click.option("--report_file_name", help="The name of the Report (docx) File.")
@click.option("--report_table_name", help="The Name of the Table.")
@click.pass_context
def merge_report(
    ctx, clixml_file_name, report_file_name, report_table_name, clixml_section
):
    """Extract  data from clixml File."""
    logger.debug(
        f"merge_report called with clixml_file_name {clixml_file_name} \
          report_file_name {report_file_name} \
          report_table_name {report_table_name}  "
    )

    # Get report and CLIXML descriptions with the respective commands
    ctx.invoke(analyze_clixml, clixml_file_name=clixml_file_name)
    ctx.invoke(
        analyze_report,
        report_file_name=report_file_name,
        report_table_name=report_table_name,
    )

    #  Massage Report data so that we have a list of dicts
    # get the analysed data (a list of rows)
    report_table_rows = ctx.obj["AVAILABLE_TABLES"][report_table_name]["ROWS"]
    assert isinstance(report_table_rows, list)
    logger.debug(f"Report table {report_table_name} has {len(report_table_rows)} rows ")
    # get the structure of each row
    keys = AVAILABLE_TABLES[report_table_name]["COLUMN_CONTENT"]
    logger.debug(f"Report table {report_table_name} has the following keys {keys}")
    list_of_table_dicts = make_list_of_dicts(report_table_rows, keys)
    # double proof check
    for row in list_of_table_dicts:
        assert set(row.keys()) == set(keys)
    logger.info(
        f" Report Table {report_table_name} has the following elements {pprint.pformat(list_of_table_dicts)}"
    )

    #
    # Clixml data
    #
    clixml_dict = ctx.obj["CLIXML_NORMALIZED_DICT"]["ComponentLicenseInformation"]
    """odict_key_1 = [ "@component", "@creator", "@date", "@baseDoc", "@toolUsed", "@componentID",
    "@includesAcknowledgements", "@componentSHA1", "@Version", "License", "Obligation", "Copyright",
    "ExportRestrictions", "Patents", "IrrelevantFiles", ]
    """

    #
    # CURRENTLY ONLY IRRELEVANT FILES CAN BE ANALYZED
    #

    files_only_in_report = []
    files_only_in_clixml = []
    files_in_clixml_and_report = []

    if clixml_section == "IrrelevantFiles":
        logger.info(f"Analyzing clixml section {clixml_section}")

        def compactify(ld):
            ld2 = list()
            for row in ld:
                if row["Path"] == ".":
                    ld2.append(row["Files"])
                else:
                    ld2.append(row["Path"] + "/" + row["Files"])
            return ld2
        compactified_report_table_list = compactify(list_of_table_dicts)
        logger.info(
            f" Compactified Report Table {report_table_name} has the following \
                elements {pprint.pformat(compactified_report_table_list)}"
        )

        clixml_set=set(clixml_dict[clixml_section]["Files"])
        report_set=set(compactified_report_table_list)
        logger.info( f"report files {pprint.pformat(report_set)} ")
        logger.info( f"clixml files {pprint.pformat(clixml_set)} ")

        all_irrelevant_files = clixml_set  | report_set # union
        in_both =   clixml_set.intersection(report_set) 
        only_in_clixml = clixml_set.difference(report_set)
        only_in_report = report_set.difference(clixml_set)

        logger.info( f"All irrelevant Files {pprint.pformat(all_irrelevant_files)} ")
        if only_in_clixml == set() and only_in_clixml ==set():
           logger.info( f"All irrelevant Files are up to date ")
        else:
           logger.warning( f"irrelevant Files need update ")
           logger.warning( f"Files in both {pprint.pformat(in_both)} ")
           logger.warning( f"Files only in report  {pprint.pformat(only_in_report)} ")
           logger.warning( f"Files only in clixml {pprint.pformat(only_in_clixml)} ")
           sys.exit(2)




    else:
        logger.fatal(f"{clixml_section} currently not allowed to work on")
        raise


def main():
    cli(obj={})  # pragma: no cover


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
