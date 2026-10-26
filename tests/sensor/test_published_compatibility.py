"""Keep the API expected by the integration's published 0.1.13 dependency."""

from mobilealerts import Sensor


def test_restored_measurement_can_set_prior_value():
    sensor = Sensor(None, "083F2CAA2B42")
    sensor.parse_packet(
        bytes.fromhex(
            "E161950AB225083F2CAA2B4203FF400900E095189BAD83E58C6AC515C3F3D642C41EC607C2AC00000000000000000000000000000000000000000000000000"
        )
    )
    measurement = sensor.measurements[0]
    measurement.prior_value = 12.3
    assert measurement.prior_value == 12.3


def test_sensor_without_reading_has_unknown_timestamp_and_battery():
    sensor = Sensor(None, "083F2CAA2B42")
    assert sensor.timestamp is None
    assert sensor.low_battery is None
