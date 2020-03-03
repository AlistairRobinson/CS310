from secure_scan.actors import Station, AccessPoint

def test_station_constructor():
    a = Station()
    b = Station()
    assert a != b

def test_ap_constructor():
    a = AccessPoint()
    b = AccessPoint()
    assert a != b

def test_beacon():
    ap = AccessPoint()
    _ = ap.send_beacon()

def test_probe_request():
    ap = AccessPoint()
    st = Station()
    beacon = ap.send_beacon()
    _ = st.send_probe_request(beacon)

def test_invalid_probe_response():
    ap = AccessPoint()
    st = Station()
    beacon = ap.send_beacon()
    probe_request = st.send_probe_request(beacon)
    probe_response = ap.send_probe_response(probe_request)
    assert not st.verify_probe_response(probe_response)

def test_valid_probe_response():
    ap = AccessPoint()
    st = Station()
    st.save_ap(ap)
    beacon = ap.send_beacon()
    probe_request = st.send_probe_request(beacon)
    probe_response = ap.send_probe_response(probe_request)
    assert st.verify_probe_response(probe_response)

def test_karma():
    adversary = AccessPoint()
    ap = AccessPoint()
    st = Station()
    st.save_ap(ap)
    beacon = ap.send_beacon()
    probe_request = st.send_probe_request(beacon)
    try:
        probe_response = adversary.send_probe_response(probe_request)
        assert not st.verify_probe_response(probe_response)
    except ValueError:
        return True

def test_reverse_karma():
    ap = AccessPoint()
    st = Station()
    st.save_ap(ap)
    beacon = ap.send_beacon()
    probe_request = st.send_probe_request(beacon)
    assert not ap.ssid in str(probe_request.contents)
