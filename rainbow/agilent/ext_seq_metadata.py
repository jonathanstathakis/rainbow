"""
2023-06-27 09:41:20

Module containing core function extract_sequence_metadata and dependencies
"""
from lxml import etree


def extract_sequence_metadata(filepath: str) -> dict[str, str]:
    """
    Take a sequence.acam_ file and return a dictionary of extracted metadata.
    
    Elements are specified by a relative xpath starting from the branch at "/Doc/Content". Place the xpath in xpath_dict
    """
    
    xpath_dict = get_xpath_dict()
    
    seq_metadata = {
        key: None for key in xpath_dict.keys()
    }  # setup the results container

    tree = etree.parse(filepath)  # create the etree object
    root = tree.getroot()
    
    # get the namespace for the file from the root tag
    namespace = root.tag.split("}")[0].strip(
        "{"
    )
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
            if description == 'id':
                seq_metadata[description] = result[0].attrib['id']
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
            print(e)

    return seq_metadata


def get_xpath_dict():
    """
    In the .acam* files every metadata element lies on the /Doc/Content/ root,
    branching from that point. The necessary xpath is complicated, needing a namespace
    injection at every node, so for ease of use place a simple relative xpath here and
    the factory will do the rest.
    """
    xpath_dict = {
            "seq_name": "/SampleContextParams/IdentParam/Name",
            "seq_desc" : "/SampleContextParams/IdentParam/Description",
            "vialnum": "/SampleParams/AcqParam/VialNumber",
            "originalfilepath": "/Injections/MeasData/BinaryData/DirItem/OriginalFilePath",
            "id": "/SampleContexts/Setup",
            "desc": "/SampleParams/IdentParam/Description"
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