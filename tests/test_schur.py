from schur_cert.verifier import verify, coloring_valid

def test_schur_s3_certificate():
    r = verify()
    assert r["status"] == "PASS"
    assert r["n13_avoider_found"] is True
    assert coloring_valid(r["n13_avoider_coloring"])
    assert r["n14_avoider_found"] is False
