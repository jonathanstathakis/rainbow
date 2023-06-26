"""

"""
from mydevtools import project_settings, function_timer as ft
from mydevtools.testing import mytestmethods
from lxml import etree


def jonathan_dev_tests_main(filepath: str):
    tests = [(testing_etree, filepath)]
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


def testing_etree(filepath: str):
    # in the ElementTree API, Element class is the main container object created here:
    print("")
    tree = etree.parse(filepath)
    root = tree.getroot()
    ns = {"acaml": "urn:schemas-agilent-com:acaml14"}
    for description, rel_path in xpath_dict.items():
        xpath_exp = xpath_factory(rel_path)
        # result = root.xpath(xpath_exp)
        result = root.xpath(xpath_exp, namespaces=ns)
        print("xpath length is:", len(result))
        for item in result:
            print(description, ":", item.text)


def main():
    filepath = (
        "/Users/jonathan/0_jono_data/mres_data_library/cuprac/138.D/sequence.acam_"
    )

    jonathan_dev_tests_main(filepath=filepath)
    return None


if __name__ == "__main__":
    main()
