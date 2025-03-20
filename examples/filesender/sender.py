import asyncio
import logging
from aioquic.asyncio.client import connect
from aioquic.quic.configuration import QuicConfiguration

CHUNK_SIZE = 4096  # Samme som serveren

# Sett opp logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def send_file(host, port, filename):
    configuration = QuicConfiguration(is_client=True)

    logging.info(f"Kobler til {host}:{port} for å sende fil: {filename}")

    async with connect(host, port, configuration=configuration) as connection:
        stream_id = connection._quic.get_next_available_stream_id()

        with open(filename, "rb") as f:
            total_sent = 0
            while chunk := f.read(CHUNK_SIZE):
                connection.send_stream_data(stream_id, chunk)
                total_sent += len(chunk)
                logging.info(f"Sendt {len(chunk)} bytes (totalt: {total_sent} bytes)")

        logging.info(f"Fil {filename} sendt!")
        await connection.wait_closed()

# Kjør klienten
asyncio.run(send_file("localhost", 4433, "large_file.bin"))
