"""Transport regressions for gateways on routed networks."""

import asyncio
from unittest.mock import Mock, patch

import pytest
from mobilealerts import Gateway
from mobilealerts.gateway import BROADCAST_ADDR, FIND_GATEWAY, PORT

HOST = "192.0.2.81"
MAC = "001D8C0DF7E1"


def config_packet():
    packet = bytearray(186)
    packet[2:8] = bytes.fromhex(MAC)
    packet[8:10] = (186).to_bytes(2, "big")
    packet[11:15] = bytes([192, 0, 2, 81])
    packet[15] = 1
    return bytes(packet)


@pytest.mark.parametrize("host", [None, HOST])
def test_commands_and_config_use_selected_destination(host):
    gateway = Gateway(MAC, gateway_ip=host)
    assert asyncio.run(gateway.init(config_packet()))
    sock = Mock()
    with patch.object(Gateway, "prepare_socket", return_value=sock):
        asyncio.run(gateway.send_command(FIND_GATEWAY))
        gateway.set_config()
    assert [call.args[1] for call in sock.sendto.call_args_list] == [
        (host or BROADCAST_ADDR, PORT),
        (host or BROADCAST_ADDR, PORT),
    ]


@pytest.mark.parametrize(
    "host", ["not-an-ip", "::1", "255.255.255.255", "224.0.0.1", "0.0.0.0"]
)
def test_manual_host_rejects_non_unicast_ipv4(host):
    with pytest.raises(ValueError):
        Gateway(MAC, gateway_ip=host)


def test_unicast_discovery_preserves_transport_after_discovery():
    sock = Mock()
    replies = [config_packet(), asyncio.TimeoutError()]

    async def receive(*args):
        result = replies.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    async def exercise():
        loop = asyncio.get_running_loop()
        with patch.object(Gateway, "prepare_socket", return_value=sock), patch.object(
            loop, "sock_recv", side_effect=receive
        ):
            gateways = await Gateway.discover(gateway_ip=HOST)
            assert len(gateways) == 1
            assert gateways[0].gateway_id == MAC
            await gateways[0].send_command(FIND_GATEWAY)
        assert all(call.args[1] == (HOST, PORT) for call in sock.sendto.call_args_list)

    asyncio.run(exercise())


def test_socket_remains_nonblocking_for_asyncio():
    sock = Gateway.prepare_socket(2, "127.0.0.1")
    try:
        assert not sock.getblocking()
    finally:
        sock.close()


def test_real_unicast_roundtrip_on_loopback():
    import mobilealerts.gateway as transport

    class Responder(asyncio.DatagramProtocol):
        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, addr):
            self.transport.sendto(config_packet(), addr)

    async def exercise():
        loop = asyncio.get_running_loop()
        server, _ = await loop.create_datagram_endpoint(
            Responder, local_addr=("127.0.0.1", 0)
        )
        try:
            with patch.object(transport, "PORT", server.get_extra_info("sockname")[1]):
                gateways = await Gateway.discover("127.0.0.1", gateway_ip="127.0.0.1")
                assert len(gateways) == 1
                assert await gateways[0].init()
        finally:
            server.close()

    asyncio.run(exercise(), debug=True)
