import asyncio
import os
import logging
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived

# Konfigurasjon
OUTPUT_FOLDER = "received_files"
CHUNK_SIZE = 4096  # Juster pakningsstørrelse ved behov

# Sørg for at lagringsmappen eksisterer
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Sett opp logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class FileTransferServer(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files = {}

    def quic_event_received(self, event: QuicEvent):
        """Håndter mottatte data på en stream"""
        if isinstance(event, StreamDataReceived):
            stream_id = event.stream_id
            data_length = len(event.data)

            if stream_id not in self.files:
                # Ny filoverføring starter
                filename = f"{OUTPUT_FOLDER}/received_file_{stream_id}.bin"
                self.files[stream_id] = open(filename, "wb")
                logging.info(f"Startet mottak av fil: {filename}")

            # Skriv til fil
            self.files[stream_id].write(event.data)
            logging.info(f"Mottatt {data_length} bytes på stream {stream_id}")

            # Hvis stream er ferdig, lukk filen
            if event.end_stream:
                self.files[stream_id].close()
                logging.info(f"Fil mottatt og lagret som: {filename}")
                del self.files[stream_id]


async def run_server(host="0.0.0.0", port=4433):
    configuration = QuicConfiguration(is_client=False)
    server = await serve(host, port, configuration=configuration, create_protocol=FileTransferServer)

    logging.info(f"Server kjører på {host}:{port}...")
    try:
        await asyncio.Event().wait()  # Hold serveren kjørende
    except KeyboardInterrupt:
        logging.info("Serveren avsluttes...")
    finally:
        server.close()
        await server.wait_closed()


# Start serveren
asyncio.run(run_server())
