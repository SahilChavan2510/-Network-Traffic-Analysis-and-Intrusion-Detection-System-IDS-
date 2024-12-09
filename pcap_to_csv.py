#pcap_to_csv.py
import pyshark
import csv

capture_file = '4.pcapng'  # Update with your file path

with open('network_traffic4.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([
        "Source IP", "Destination IP", "Protocol", "Length", "Time", 
        "SYN_Flag", "ACK_Flag", "FIN_Flag", "RST_Flag", "PSH_Flag", 
        "URG_Flag", "Source_Port", "Dest_Port", "TTL", "Window_Size", "Payload"
    ])

    try:
        capture = pyshark.FileCapture(capture_file)
    except FileNotFoundError:
        print(f"Error: File not found: {capture_file}")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit()

    packet_count = 0
    for packet in capture:
        try:
            # Skip non-IP packets
            if not hasattr(packet, 'ip'):
                continue

            # Extract IP addresses
            source_ip = getattr(packet.ip, 'src', None)
            dest_ip = getattr(packet.ip, 'dst', None)

            # Extract protocol
            protocol = getattr(packet, 'transport_layer', None)

            # Extract length
            length = getattr(packet, 'length', None)
            length = int(length) if length and length.isdigit() else None

            # Extract timestamp
            time = getattr(packet.sniff_time, 'isoformat', lambda: None)()

            # Extract TCP flags
            flags = {'SYN': 0, 'ACK': 0, 'FIN': 0, 'RST': 0, 'PSH': 0, 'URG': 0}
            if hasattr(packet, 'tcp'):
                for flag in flags.keys():
                    flag_value = getattr(packet.tcp, f'flags_{flag.lower()}', None)
                    flags[flag] = int(flag_value) if flag_value and flag_value.isdigit() else 0

            # Extract port numbers
            source_port = None
            dest_port = None
            if protocol and hasattr(packet, protocol.lower()):
                source_port = getattr(packet[protocol.lower()], 'srcport', None)
                dest_port = getattr(packet[protocol.lower()], 'dstport', None)
                source_port = int(source_port) if source_port and source_port.isdigit() else None
                dest_port = int(dest_port) if dest_port and dest_port.isdigit() else None

            # Extract TTL and Window Size
            ttl = getattr(packet.ip, 'ttl', None)
            ttl = int(ttl) if ttl and ttl.isdigit() else None

            window_size = getattr(packet.tcp, 'window_size', None) if hasattr(packet, 'tcp') else None
            window_size = int(window_size) if window_size and window_size.isdigit() else None

            # Extract payload
            payload = getattr(packet, 'highest_layer', None)

            # Write row to CSV
            writer.writerow([
                source_ip, dest_ip, protocol, length, time,
                flags['SYN'], flags['ACK'], flags['FIN'], flags['RST'], flags['PSH'], flags['URG'],
                source_port, dest_port, ttl, window_size, payload
            ])

            packet_count += 1
            if packet_count % 100 == 0:
                print(f"Processed {packet_count} packets...")

        except Exception as e:
            print(f"Error processing packet {packet_count}: {e}")
            continue

    capture.close()
    print(f"Finished processing {packet_count} packets.")
