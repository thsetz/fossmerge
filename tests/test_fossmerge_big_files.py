from collections import OrderedDict
from fossmerge import __version__, fossmerge_cli
import pprint
import xmltodict
from fossmerge import analyze_docx_file


def xest_current_report(runner, big_docx_report_file):
    """Test the CLI."""
    d = {}
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
