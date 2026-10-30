import struct
from native_parser.parser_wrapper import MetadataParserWrapper

def test_secure_parser_rejects_missing_magic():
    wrapper = MetadataParserWrapper(mode="secure")
    bad_header = b"BADM" + struct.pack("<HHI", 1, 0, 10) + b"Alice\x00Title\x00"
    res = wrapper.parse_header(bad_header)
    assert not res["success"]
    assert res["error_code"] == -2

def test_secure_parser_rejects_oversized_payload():
    wrapper = MetadataParserWrapper(mode="secure")
    giant_payload = b"CVLT" + struct.pack("<HHI", 1, 0, 5000) + b"A" * 5000
    res = wrapper.parse_header(giant_payload)
    assert not res["success"]
    assert res["error_code"] == -4

def test_secure_parser_rejects_length_tampering():
    wrapper = MetadataParserWrapper(mode="secure")
    tampered_header = b"CVLT" + struct.pack("<HHI", 1, 0, 200) + b"ShortData\x00"
    res = wrapper.parse_header(tampered_header)
    assert not res["success"]
    assert res["error_code"] == -3

def test_secure_parser_bounded_string_copy():
    wrapper = MetadataParserWrapper(mode="secure")
    long_author = b"B" * 200
    valid_header = b"CVLT" + struct.pack("<HHI", 1, 0, len(long_author) + 10) + long_author + b"\x00Safe Title\x00"
    res = wrapper.parse_header(valid_header)
    assert res["success"]
    assert len(res["author"]) <= 63
    assert res["title"] == "Safe Title"
