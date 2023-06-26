"""

"""
from mydevtools import project_settings, function_timer as ft
from mydevtools.testing import mytestmethods
from lxml import etree


def jonathan_dev_tests_main(filepath: str):
    tests = [(testing_etree, filepath)]
    mytestmethods.test_report(tests)
    return None


def testing_etree(filepath: str):
    # Parse the XML file and get the root element
    tree = etree.parse(filepath)
    root = tree.getroot()

    print(f"Root tag: {root.tag}")  # print the root tag

    ns = {"acaml": "urn:schemas-agilent-com:acaml14"}
    xpath_exp = ".//acaml:Doc/acaml:Content/acaml:SampleContextParams/acaml:IdentParam/acaml:Name"
    result = root.xpath(xpath_exp, namespaces=ns)

    print("xpath length is:", len(result))
    for item in result:
        print(item.tag, item.attrib)


def testing_etree(filepath: str):
    # in the ElementTree API, Element class is the main container object created here:
    print("")
    tree = etree.parse(filepath)
    root = tree.getroot()

    ns = {"acaml": "urn:schemas-agilent-com:acaml15"}
    # xpath_exp = "./ACAML/Doc/Content/SampleContextParams/IdentParam/Name"
    xpath_exp = ".//acaml:Doc/acaml:Content/acaml:SampleContextParams/acaml:IdentParam/acaml:Name"
    result = root.xpath(xpath_exp, namespaces=ns)
    print("xpath length is:", len(result))
    for item in result:
        print(item.text)

    # name = etree.parse(filepath).find(xpath_exp)
    # print("")


#    print(name)

# assert name


def main():
    filepath = (
        "/Users/jonathan/mycode/python_code/rainbow/tests/inputs/red.D/sequence.acam_"
    )

    jonathan_dev_tests_main(filepath=filepath)
    return None


if __name__ == "__main__":
    main()
