from collections import OrderedDict
from fossmerge import __version__, fossmerge_cli
import pprint
import xmltodict
import os
from fossmerge import analyze_docx_file


def test_current_report(runner, big_docx_report_file):
    """Test the CLI."""
    d = {}
    # XXX Currently the Github Ci does not hav sufficient XXX to run pandoc
    # with such big files - so skip them here.
    # The environment Variable SKIP_BIG_PANDOC_TESTS is set via 
    # the GitHub workflow file .github/workflows/fossmergetest.yml .
    skip_big_pandoc_tests = os.environ.get("SKIP_BIG_PANDOC_TESTS", "NO")
    if skip_big_pandoc_tests == "YES":
        return
    result = runner.invoke(
        fossmerge_cli.cli,
        [
            "-vv",
            "--no_log_to_console",
            "analyze_report",
            "--report_file_name",
            big_docx_report_file,
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


def test_current_state(runner, big_cli_xml_file):
    """Test the CLI."""
    d = {}
    result = runner.invoke(
        fossmerge_cli.cli,
        [
            "-v",
            "--no_log_to_console",
            "analyze_clixml",
            "--clixml_file_name",
            big_cli_xml_file,
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
