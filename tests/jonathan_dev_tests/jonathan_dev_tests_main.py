"""

"""
from mydevtools import project_settings, function_timer as ft
from mydevtools.testing import mytestmethods
from lxml import etree
import rainbow as rb
from rainbow.agilent import ext_seq_metadata
import os


def jonathan_dev_tests_main(filepath: str):
    tests = [
        (test_extract_sequence_metadata, filepath),
        (test_chemstation_single_file,),
        (test_chemstation_library,),
    ]
    mytestmethods.test_report(tests)
    return None


def test_extract_sequence_metadata(filepath):
    seq_metadata_dict = ext_seq_metadata.extract_sequence_metadata(filepath)
    assert seq_metadata_dict, "seq_metadata_dict empty"

    xpath_dict = ext_seq_metadata.get_xpath_dict()
    
    lowered_keys_list = [key for key in xpath_dict.keys()]

    for key in lowered_keys_list:
        assert (
            key in seq_metadata_dict.keys()
        ), f"expected {key} to be in returned seq_metadata_dict"

    print(seq_metadata_dict)

    for description, metadata in seq_metadata_dict.items():
        assert metadata, f"{description}"


def test_chemstation_single_file():
    filepath = "/Users/jonathan/0_jono_data/raw_uv/2023-02-22_KOERNER-NELLUCIO-02-21.D"
    datadir = rb.read(filepath)
    uv_file = datadir.get_file("DAD1.UV")
    metadata = {**datadir.metadata, **uv_file.metadata}
    print(metadata)
   
    
def test_chemstation_library():
    libpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_lib_descs")
    for file in os.listdir(libpath):
        print("")
        filepath = os.path.join(libpath, file)
        datadir = rb.read(filepath)
        uv_file = datadir.get_file("DAD1.UV")
        metadata = {**datadir.metadata, **uv_file.metadata}
        print(metadata)
        


def main():
    filepath = (
        "/Users/jonathan/0_jono_data/mres_data_library/cuprac/138.D/sequence.acam_"
    )

    jonathan_dev_tests_main(filepath=filepath)
    return None


if __name__ == "__main__":
    main()
