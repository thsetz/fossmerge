from collections import OrderedDict
from fossmerge import __version__, fossmerge_cli
import pprint
import xmltodict


def test_version():
    assert __version__ == "0.1.0"


def test_current_report(runner, docx_report_file):
    """Test the CLI."""
    d = {}
    result = runner.invoke(
        fossmerge_cli.cli,
        [
            "-vv",
            "--no_log_to_console",
            "analyze_report",
            "--report_file_name",
            docx_report_file,
            "--report_table_name",
            "copyrights",
        ],
        obj=d,
        catch_exceptions=False,
    )
    assert d["VERBOSE"] == 2
    available_tables = d["AVAILABLE_TABLES"]
    assert isinstance(available_tables, dict)
    assert result.exit_code == 0


def test_current_state(runner, cli_xml_file):
    """Test the CLI."""
    d = {}
    result = runner.invoke(
        fossmerge_cli.cli,
        [
            "-v",
            "--no_log_to_console",
            "analyze_clixml",
            "--clixml_file_name",
            cli_xml_file,
        ],
        obj=d,
        catch_exceptions=False,
    )
    assert d["VERBOSE"] == 1
    doc = d["CLIXML_DICT"]
    assert isinstance(doc, OrderedDict)
    x = xmltodict.unparse(doc, pretty=True)
    print(x)
    assert result.exit_code == 0


def test_merge_report(runner, cli_xml_file, docx_report_file):
    """Test the merge_report CLI."""
    d = {}
    result = runner.invoke(
        fossmerge_cli.cli,
        [
            "-vv",
            "--no_log_to_console",
            "merge_report",
            "--clixml_file_name",
            cli_xml_file,
            "--report_file_name",
            docx_report_file,
            "--report_table_name",
            "irrelevant-files",
            "--clixml_section",
            "IrrelevantFiles",
        ],
        obj=d,
        catch_exceptions=False,
    )
    assert d["VERBOSE"] == 2
    doc = d["CLIXML_DICT"]
    assert isinstance(doc, OrderedDict)
    x = xmltodict.unparse(doc, pretty=True)
    assert result.exit_code == 0

    """
- 1. General Assessment ==> id=assessment-summary
- 6.1 Notes on individual files ==> id=notes-on-individual-files
- 17. Irrelevant Files  ==> id=irrelevant-files 
- 17.1 Comment for Irrelevant Files id=comment-for-irrelevant-files
    """
