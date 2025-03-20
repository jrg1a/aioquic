def generate_large_file(filename="large_file.bin", size_mb=100):
    with open(filename, "wb") as f:
        f.write(b"\x00" * (size_mb * 1024 * 1024))  # Fyll filen med nullbytes

generate_large_file()
