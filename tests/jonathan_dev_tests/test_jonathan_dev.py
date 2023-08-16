"""
pytest version of my tests. As of 2023-08-15 10:47:00 the old tests at "tests/jonathan_dev_tests/jonathan_dev_tests_main.p"y will need to be converted to pytest format.
"""

import pytest
from rainbow.agilent import ext_seq_metadata
import logging
from lxml import etree
import os
import rainbow as rb

logger = logging.getLogger(__name__)
import pandas as pd
from glob import glob

pd.options.display.width = None
pd.options.display.show_dimensions = True
pd.options.display.max_colwidth = 100
pd.options.display.max_rows = 100
pd.options.display.max_columns = 15
pd.options.display.colheader_justify = "left"


class DataDir:
    def __init__(self, path):
        assert os.path.isdir(path), path
        self.name = os.path.basename(path)
        self.path = path
        self.parent = os.path.dirname(path)
        self.contents = os.listdir(path)
        self.paths = {name: os.path.join(self.path, name) for name in self.contents}


class SamplePool:
    def __init__(self, path):
        self.path = path
        self.contents = glob(path + "**/*.D")
        self.paths = {
            os.path.basename(path): path
            for path in self.contents
            if path.endswith(".D")
        }
        self.dds = {name: DataDir(path) for name, path in self.paths.items()}
@pytest.fixture
def sp():
    sp = SamplePool("/Users/jonathan/uni/0_jono_data/mres_data_library/")
    return sp

def test_datadir():
    dd = DataDir("tests/jonathan_dev_tests/test_lib_descs/116.D")
    print(dd.paths)


def test_samplepool():
    sp = SamplePool("tests/jonathan_dev_tests/test_lib_descs/")
    print(sp.contents)
    print(sp.paths)
    print(sp.dds.items())


def test_xpath():
    """
    test whether the given xpath can return a value. if that value is a list, check if all are full.
    """
    results = []
    sp = SamplePool("/Users/jonathan/uni/0_jono_data/mres_data_library/")
    # sp = SamplePool("tests/jonathan_dev_tests/test_lib_descs/")
    for fname, DD in sp.dds.items():
        acq_macaml = DD.paths["acq.macaml"]
        # 116 xpath
        val_raw_xpath_116 = "   Section[1]/Section[3]/Section[4]/Parameter[2]/Value"
        name_raw_xpath_116 = "/MethodConfiguration/MethodDescription/Section[1]/Section[3]/Section[4]/Parameter[2]/Name"
        # this is the 094 path
        val_raw_xpath_094 = "/MethodConfiguration/MethodDescription/Section/Section[1]/Section[2]/Parameter[2]/Value"
        name_raw_xpath_094 = "/MethodConfiguration/MethodDescription/Section/Section[1]/Section[2]/Parameter[2]/Name"
        tree = etree.parse(acq_macaml)
        root = tree.getroot()
        namespace = root.tag.split("}")[0].strip("{")
        ns = {"acaml": namespace}
        name_xpath_116 = ext_seq_metadata.xpath_factory(name_raw_xpath_116)
        val_xpath_116 = ext_seq_metadata.xpath_factory(val_raw_xpath_116)
        val = root.xpath(val_xpath_116, namespaces=ns)
        name = root.xpath(name_xpath_116, namespaces=ns)
        if val:
            results.append(
                dict(
                    fname=fname,
                    path=acq_macaml,
                    name=name[0].text,
                    val=val[0].text,
                    xpath="116",
                )
            )
        if not val:
            val_xpath_094 = ext_seq_metadata.xpath_factory(val_raw_xpath_094)
            name_xpath_094 = ext_seq_metadata.xpath_factory(name_raw_xpath_094)
            val = root.xpath(val_xpath_094, namespaces=ns)
            name = root.xpath(name_xpath_094, namespaces=ns)
            results.append(
                dict(
                    fname=fname,
                    path=acq_macaml,
                    name=name[0].text,
                    val=val[0].text,
                    xpath="094",
                )
            )
    result_df = pd.DataFrame(results)

    result_df = result_df.loc[:, "name"].value_counts()
    print(f"\n{result_df}")
    # for child in result[0].iterchildren():
    #     print(etree.tostring(child, pretty_print=True).decode())
    # # print(result[0].text)
    # assert result


def test_findall():
    sp = SamplePool("/Users/jonathan/uni/0_jono_data/mres_data_library/")
    from lxml import etree

    def find_parameter_values(filepath, target_names: list):
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
                
    results = []
    for name, DD in sp.dds.items():
        output = find_parameter_values(DD.paths['acq.macaml'], target_names=["Injection Volume",])
        output['name'] = name
        results.append(output)

    print(f"\n{df}")
        


def test_acq_macaml(sp):
    """
    test extraction of acq.macaml data. Primarily a print test, not sophisticated enough to validate pot. contents
    """
    results = []
    for name, DD in sp.dds.items():
        assert os.path.isfile(DD.paths['acq.macaml'])
        metadata = ext_seq_metadata.extract_acq_metadata(DD.paths['acq.macaml'])
        assert metadata
        metadata['name']=name
        print(metadata)
        results.append(metadata)
        for key, val in metadata.items():
            assert val, key
            
    df = pd.DataFrame(results).set_index('name')
    print(df)


def test_seq_acam_(seq_acam_):
    """
    test extraction of seq.acam_ data. Primarily a print test, not sophisticated enough to validate pot. contents
    """
    print(f"filepath: {seq_acam_}")
    metadata = ext_seq_metadata.extract_sequence_metadata(seq_acam_)
    sample_metadata = {
        "seq_name": "2023-04-04_WINES_2023-04-04_12-01-53",
        "seq_desc": None,
        "vialnum": "Vial 1",
        "originalfilepath": (
            "C:\\CHEM32\\1\\DATA\\0_JONO_DATA\\2023-04-04_WINES_2023-04-04_12-01-53"
        ),
        "id": "1c8ddfe0-e0c2-41d3-a20d-530454cf0f3f",
        "desc": "21 le macchiole bolgheri rosso",
    }

    assert metadata == sample_metadata


@pytest.fixture
def chemstation_metadata():
    return {
        "vendor": "Agilent",
        "date": "04-Apr-23, 12:03:16",
        "inj_vol_ul": "10.00",
        "seq_name": "2023-04-04_WINES_2023-04-04_12-01-53",
        "seq_desc": None,
        "vialnum": "Vial 1",
        "originalfilepath": (
            "C:\\CHEM32\\1\\DATA\\0_JONO_DATA\\2023-04-04_WINES_2023-04-04_12-01-53"
        ),
        "id": "1c8ddfe0-e0c2-41d3-a20d-530454cf0f3f",
        "desc": "21 le macchiole bolgheri rosso",
        "notebook": "94",
        "method": "AVANTOR100X4_6C18-H2O-MEOH-2_5.M",
        "unit": "mAU",
        "signal": "DAD1I, DAD: Spectrum",
    }


def test_rainbow_metadata(sp, chemstation_metadata):
    """
    test whether the metadata generated by rb.read + .get_file().metadata equals a predefined dict of metadata.
    
    Need to add assertion tests here, atm just viz test, cant spend too much time on this
    """
    results = []
    for dd in sp.dds.keys():
        datadir = rb.read(sp.dds[dd].path)
        uv_file = datadir.get_file("DAD1.UV")
        metadata = {**datadir.metadata, **uv_file.metadata}
        print(metadata)
        #assert metadata == chemstation_metadata
        results.append(metadata)
    
    df = pd.DataFrame(results)
    print(df)
