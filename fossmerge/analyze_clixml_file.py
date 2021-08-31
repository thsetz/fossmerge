__doc__ = """
"""
import os
import pprint
import logging
from deepdiff import DeepDiff


# logger = logging.getLogger(__name__)
logger = logging.getLogger("fossmerge")

import xmltodict

odict_keys_0 = ["ComponentLicenseInformation"]
odict_key_1 = [
    "@component",
    "@creator",
    "@date",
    "@baseDoc",
    "@toolUsed",
    "@componentID",
    "@includesAcknowledgements",
    "@componentSHA1",
    "@Version",
    "License",
    "Obligation",
    "Copyright",
    "ExportRestrictions",
    "Patents",
    "IrrelevantFiles",
]


def convert_clixml_to_xmldict(file_name: os.path):
    """[summary]

    :param file_name: [description]
    :type file_name: [os.path]
    :return: [description of the files content]
    :rtype: [type] ordered Dict
    """ """
    """
    logger.debug(f"convert_and_analyze_clixml called with file_name {file_name} ")
    doc = xmltodict.parse(open(file_name, "rb"), dict_constructor=dict)
    return doc


def check_xmldict(doc: dict):
    """[summary]
        A given a CLIXML-doc  xmltodict dict is analyzedi/normalized e.g missing wrong Attributes are added/modified.py

    :param doc: [xmltodict dict created with xmltodict.parse(...)]
    :type doc: dict
    :return: [bool indicating if document was modified, new (deepcopy) document.]
    :rtype: [bool, dict]
    """
    import copy

    new_doc = copy.deepcopy(doc)
    for key in new_doc["ComponentLicenseInformation"].keys():
        if key == "ExportRestrictions":
            for elem in new_doc["ComponentLicenseInformation"][key]:
                subelems = ["Content", "Files", "FileHash"]
                # https://stackoverflow.com/questions/34312674/why-are-the-values-of-an-ordereddict-not-equal
                assert list(subelems) == list(elem.keys())
        elif key == "License":
            i = 0
            for elem in new_doc["ComponentLicenseInformation"][key]:
                sub_elems = [
                    "@type",
                    "@name",
                    "@spdxidentifier",
                    "Content",
                    "Files",
                    "FileHash",
                    "Acknowledgements",
                ]
                sub_elems2 = [
                    "@type",
                    "@name",
                    "@spdxidentifier",
                    "Content",
                    "Files",
                    "FileHash",
                ]
                # Some have  Acknowledgement some not: Add Empy Ackknowledgement if no one is found
                try:
                    assert list(sub_elems) == list(elem.keys())
                except:
                    assert list(sub_elems2) == list(elem.keys())
                    elem["Acknowledgements"] = ""
                    assert list(sub_elems) == list(elem.keys())
                    logger.warning(
                        f"License: entry number {i} had no Acknowledgment Entry. Forcefully added one."
                    )
                i += 1
        elif key == "Obligation":
            for elem in new_doc["ComponentLicenseInformation"][key]:
                sub_elems = ["Topic", "Text", "Licenses"]
                assert list(sub_elems) == list(elem.keys())
        elif key == "Copyright":
            for elem in new_doc["ComponentLicenseInformation"][key]:
                sub_elems = ["Content", "Files", "FileHash"]
                assert list(sub_elems) == list(elem.keys())
        elif key == "Patents":
            i = 0
            for elem in new_doc["ComponentLicenseInformation"][key]:
                sub_elems = ["Content", "Files", "FileHash", "Comment"]
                sub_elems2 = ["Content", "Files", "FileHash"]
                # Some have  Comment some not: Add Empy Comment if no one is found
                try:
                    assert list(sub_elems) == list(elem.keys())
                except:
                    assert list(sub_elems2) == list(elem.keys())
                    elem["Comment"] = ""
                    logger.warning(
                        f"Patent: entry number {i} had no Comment Entry. Forcefully added one."
                    )
                    assert list(sub_elems) == list(elem.keys())
        elif key == "IrrelevantFiles":
            # Only One Entry a List
            if isinstance(doc["ComponentLicenseInformation"][key]["Files"], str):
                l = new_doc["ComponentLicenseInformation"][key]["Files"].split()
                logger.warning(f"Irrelevant Files is of type  str : Convert it to list")
                new_doc["ComponentLicenseInformation"][key]["Files"] = l
                logger.warning(
                    f"Modified Irrelevant Files: {new_doc['ComponentLicenseInformation'][key]['Files']}"
                )
            assert isinstance(
                new_doc["ComponentLicenseInformation"][key]["Files"], list
            )
        elif key.startswith("@"):
            logger.debug(f"{key}: {new_doc['ComponentLicenseInformation'][key]}")
        else:
            logger.fatal(f"IMPOSSIBLE Key in {file_name}")
            raise

    differences = DeepDiff(doc, new_doc)
    if differences == {}:
        modified = False
    else:
        logger.warning(pprint.pformat(differences))
        modified = True
    return modified, new_doc


def diff_xmldict(lhs: dict, rhs: dict):
    differences = DeepDiff(lhs, rhs)
    logger.info("diff_xmldict called")
    if differences == {}:
        logger.info("No diffs found")
    else:
        logger.warning(f"Diffs found {pprint.pformat(differences) }")
