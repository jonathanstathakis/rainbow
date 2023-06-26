"""

"""
from mydevtools import project_settings, function_timer as ft
from mydevtools.testing import mytestmethods
from lxml import etree
import rainbow as rb
from rainbow.agilent.chemstation import extract_sequence_metadata


def jonathan_dev_tests_main(filepath: str):
    xpath_dict = {
        "Name": "/SampleContextParams/IdentParam/Name",
        "VialNumber": "/SampleParams/AcqParam/VialNumber",
        "OriginalFilePath": "/Injections/MeasData/BinaryData/DirItem/OriginalFilePath",
    }
    tests = [
        (test_extract_sequence_metadata, filepath, xpath_dict),
        (test_chemstation,),
    ]
    mytestmethods.test_report(tests)
    return None


def test_extract_sequence_metadata(filepath, xpath_dict):
    seq_metadata_dict = extract_sequence_metadata(filepath, xpath_dict)
    assert seq_metadata_dict
    assert seq_metadata_dict.keys() == xpath_dict.keys()

    # print(seq_metadata_dict)

    for description, metadata in seq_metadata_dict.items():
        assert metadata, f"{description}"


def test_chemstation():
    filepath = "/Users/jonathan/0_jono_data/cuprac/116.D"
    uv_file = rb.read(filepath).get_file("DAD1.UV")
    assert uv_file
    assert "OriginalFilePath" in uv_file.metadata.keys()


def main():
    filepath = (
        "/Users/jonathan/0_jono_data/mres_data_library/cuprac/138.D/sequence.acam_"
    )

    jonathan_dev_tests_main(filepath=filepath)
    return None


if __name__ == "__main__":
    main()
