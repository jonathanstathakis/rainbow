"""

"""
from mydevtools import project_settings, function_timer as ft
from mydevtools.testing import mytestmethods
from lxml import etree


def jonathan_dev_tests_main(filepath: str):
    tests = [(test_extract_sequence_metadata, filepath, xpath_dict)]
    mytestmethods.test_report(tests)
    return None


def xpath_factory(rel_path: str):
    namespace_inj = "/acaml:"
    path_root = "./"
    common_path = "/Doc/Content"
    path = common_path + rel_path
    path = path.replace("/", namespace_inj)
    xpath_exp = path_root + path

    return xpath_exp


xpath_dict = {
    "Name": "/SampleContextParams/IdentParam/Name",
    "VialNumber": "/SampleParams/AcqParam/VialNumber",
    "OriginalFilePath": "/Injections/MeasData/BinaryData/DirItem/OriginalFilePath",
}


def extract_sequence_metadata(filepath: str, xpath_dict: dict):
    """
    For a given .xml file "filepath" and dictionary of relative xpaths starting from
    "/Doc/Content", return a dictonary of extracted metadata.
    """
    print("")
    seq_metadata = {
        key: None for key in xpath_dict.keys()
    }  # setup the results container

    tree = etree.parse(filepath)  # create the etree object
    root = tree.getroot()

    namespace = root.tag.split("}")[0].strip(
        "{"
    )  # get the namespace for the file from the root tag
    ns = {"acaml": namespace}

    for description, rel_path in xpath_dict.items():
        try:
            # construct xpaths using the defined namespace
            xpath_exp = xpath_factory(rel_path)
            # get the result of the xpath exp as a list
            result = root.xpath(xpath_exp, namespaces=ns)
            # extract the item text from results list
            string_list = [item.text for item in result]
            # assign the results string list to return dict
            seq_metadata[description] = string_list
        except Exception as e:
            print(e)

    return seq_metadata


def test_extract_sequence_metadata(filepath, xpath_dict):
    seq_metadata_dict = extract_sequence_metadata(filepath, xpath_dict)
    assert seq_metadata_dict
    assert seq_metadata_dict.keys() == xpath_dict.keys()

    print(seq_metadata_dict)

    # for description, metadata in seq_metadata_dict.items():
    #     assert metadata, f"{description}"


def main():
    filepath = (
        "/Users/jonathan/0_jono_data/mres_data_library/cuprac/138.D/sequence.acam_"
    )

    jonathan_dev_tests_main(filepath=filepath)
    return None


if __name__ == "__main__":
    main()
