import sys
import os

def hex_to_ip_from_file(input_file, output_file):
    try:
        # Clean shellcode
        with open(input_file, 'r') as file:
            cleaned_shellcode = file.read().strip().replace("\\x", "")

        # Convert shellcode to bytes
        shellcode_bytes = bytes.fromhex(cleaned_shellcode)

        # Pad shellcode to ensure IP address like octets.
        padding_needed = (4 - len(shellcode_bytes) % 4) % 4
        shellcode_bytes += b'\x00' * padding_needed

        # Convert to IP addresses.
        ip_addresses = [
            f"{shellcode_bytes[i]}.{shellcode_bytes[i + 1]}.{shellcode_bytes[i + 2]}.{shellcode_bytes[i + 3]}"
            for i in range(0, len(shellcode_bytes), 4)
        ]

        # Write IP addresses to file.
        with open(output_file, 'w') as file:
            file.write(",".join(ip_addresses))

        print(f"IP addresses have been written to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def ip_to_hex_from_file(input_file, output_file):
    try:
        # Process IP addresses
        with open(input_file, 'r') as file:
            ip_addresses = file.read().strip().split(',')

        # Convert addresses to shellcode.
        shellcode_hex = ''.join(
            f"\\x{int(octet):02x}" for ip in ip_addresses for octet in ip.split('.')
        )

        # Write shellcode to file.
        with open(output_file, 'w') as file:
            file.write(shellcode_hex)

        print(f"Hexadecimal shellcode has been written to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) not in [2, 4]:
        print("Usage: python script.py <S2A|A2S> [<input_file> <output_file>]")
        sys.exit(1)

    operation = sys.argv[1]

    if operation == "S2A":
        input_file = sys.argv[2] if len(sys.argv) > 2 else "shellcode-in.dat"
        output_file = sys.argv[3] if len(sys.argv) > 3 else "address-out.dat"
        hex_to_ip_from_file(input_file, output_file)
    elif operation == "A2S":
        input_file = sys.argv[2] if len(sys.argv) > 2 else "address-in.dat"
        output_file = sys.argv[3] if len(sys.argv) > 3 else "shellcode-out.dat"
        ip_to_hex_from_file(input_file, output_file)
    else:
        print("Invalid operation. Use 'S2A' for shellcode to IP conversion or 'A2S' for IP to shellcode conversion.")
        sys.exit(1)
