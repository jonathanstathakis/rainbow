"""
2023-06-27 09:41:20

Module containing core function extract_sequence_metadata and dependencies.


"""
from lxml import etree
import os
import logging
logger = logging.getLogger(__name__)


def extract_sequence_metadata(filepath: str) -> dict[str, str]:
    """
    Take a sequence.acam_ file and return a dictionary of extracted metadata.

    Elements are specified by a relative xpath starting from the branch at
    "/Doc/Content". Currently the method of extracting new elements is to identify the
    xpath without namepsace relative to "/Doc/Content", place that string in
    get_seq_acam_xpath_dict and the xpath_factory will construct the xpath with
    namespace.
    
    Note - have been using the XML Tools VSCode plugin to generate xpaths at target
    elements, howevever it has been known to fail, if so will have to manually
    construct the path.
    """

    xpath_dict = get_seq_acam_xpath_dict()

    seq_metadata = {
        key: None for key in xpath_dict.keys()
    }  # setup the results container

    tree = etree.parse(filepath)  # create the etree object
    root = tree.getroot()

    # get the namespace for the file from the root tag
    namespace = root.tag.split("}")[0].strip("{")
    ns = {"acaml": namespace}

    # iterate through the xpath_dict trying to get each element
    for description, rel_path in xpath_dict.items():
        try:
            # construct xpaths using the defined namespace
            xpath_exp = xpath_factory(rel_path)

            # get the result of the xpath exp as a list

            result = root.xpath(xpath_exp, namespaces=ns)
            # extract the item text from results list
            # each item is <class 'lxml.etree._Element'>
            # ideally metadata is a flat dict, so if a result contains multiple items, assign them with incrementing keys
            if description == "id":
                seq_metadata[description] = result[0].attrib["id"]
            elif len(result) < 2:
                seq_metadata[description] = result[0].text
            else:
                # unpack the list into indexed keys
                for idx, item in enumerate(result):
                    # remove original unindexed key
                    seq_metadata.pop(description)
                    description_idx = description + "_" + idx
                    seq_metadata[description_idx] = item.text
        except Exception as e:
            logger.error(e)

    return seq_metadata


def extract_acq_metadata(filepath: str):
    """
    Get metadata from acq.macaml

    Elements are specified by a relative xpath starting from the branch at "/Doc/Content". Currently the method
    of extracting new elements is to identify the xpath without namepsace relative to "/Doc/Content", place
    that string in get_seq_acam_xpath_dict and the xpath_factory will construct the xpath with namespace
    
    2023-08-16 11:02:18 Jonathan - reason this is written as a wrapper is to obscure
    the choice of target names from the user (see find_parameter_values). Later
    changes can expose that to the user if desired, just remove the wrapper. Note:
    tests arnt fully automated, will need to add at later date (see test_jonathan_dev.py)
    """
    assert os.path.isfile(filepath)
    
    def find_parameter_values(filepath, target_names: list)-> dict:
        """
        For a given filepath (acq.macaml) extract values of parameters with names
        matching those listed in target_names. Returns dict of metadata with keys
        matching target_names.
        """
        rdict = {}
        # Parse the XML file
        tree = etree.parse(filepath)

        # Find all "Parameter" elements
        ns = {"acaml": "urn:schemas-agilent-com:acaml14"}
        sections = tree.findall(".//acaml:Section", namespaces=ns)

        # Iterate through the sections
        for section in sections:
            section_name = section.find("acaml:Name", namespaces=ns)  # Adjust as needed
            parameters = section.findall(".//acaml:Parameter", namespaces=ns)

            # Iterate through the "Parameter" elements in this section
            for parameter in parameters:
                parameter_name = parameter.find("acaml:Name", namespaces=ns)
                parameter_value = parameter.find("acaml:Value", namespaces=ns)

                for target in target_names:
                    if (
                        section_name is not None
                        and parameter_name is not None
                        and parameter_value is not None
                        and parameter_name.text == target
                    ):

                        rdict[target] = parameter_value.text
        return rdict

    acq_metadata = find_parameter_values(filepath, target_names=["Injection Volume",])

    return acq_metadata



def get_seq_acam_xpath_dict():
    """
    In the .acam* files every metadata element lies on the /Doc/Content/ root,
    branching from that point. The necessary xpath is complicated, needing a namespace
    injection at every node, so for ease of use place a simple relative xpath here and
    the factory will do the rest.
    """
    xpath_dict = {
        "seq_name": "/SampleContextParams/IdentParam/Name",
        "seq_desc": "/SampleContextParams/IdentParam/Description",
        "vialnum": "/SampleParams/AcqParam/VialNumber",
        "originalfilepath": "/Injections/MeasData/BinaryData/DirItem/OriginalFilePath",
        "id": "/SampleContexts/Setup",
        "desc": "/SampleParams/IdentParam/Description",
    }
    return xpath_dict


def xpath_factory(rel_path: str):
    """
    For the root path specified in extract_sequence_metadata and relative paths in
    xpath_dict, construct a full xpath expression with the necessary namspace.
    """
    namespace_inj = "/acaml:"
    path_root = "./"
    common_path = "/Doc/Content"
    path = common_path + rel_path
    path = path.replace("/", namespace_inj)
    xpath_exp = path_root + path

    return xpath_exp


def get_xml_vialnum(path):
    """
    Returns the VialNumber from an XML document, if it exists.

    Args:
        path (str): Path to the XML document.

    """
    tree = etree.parse(path)
    root = tree.getroot()
    for vialnum in root.xpath("//*[local-name()='VialNumber']"):
        if vialnum.text:
            return vialnum.text
    return None
