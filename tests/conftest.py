import os
import pytest

from click.testing import CliRunner
from fossmerge import analyze_docx_file


@pytest.fixture(scope="session")
def docx_report_file() -> str:
    testfile = "2019-10-16_zlib_1--1.2.11.dfsg-1-debian10-combined.tar.bz2_clearing_report_Wed_Oct_16_10_2019_06_28_46.docx"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", testfile)


@pytest.fixture(scope="session")
def big_docx_report_file() -> str:
    testfile = "2020-01-14_e2fsprogs_1.44.5-1-debian10-combined.tar.bz2_clearing_report_Mon_Jan_13_01_2020_07_27_52.docx"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", testfile)


@pytest.fixture(scope="session")
def cli_xml_file() -> str:
    testfile = "2019-10-16_CLIXML_zlib_1--1.2.11.dfsg-1-debian10-combined.tar.bz2_2019-10-16_06_29_02.xml"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", testfile)


@pytest.fixture(scope="session")
def big_cli_xml_file() -> str:
    testfile = "2020-05-04_CLIXML_linux_4.19.98-1-debian10-combined.tar.bz2_2020-05-03_17_44_47.xml"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", testfile)


# click runner
@pytest.fixture(scope="session")
def runner():
    the_runner = CliRunner()
    yield the_runner
    # cleanup
