# Ejecutar esto una sola vez para obtener el certificado
import ssl
import socket

hostname = 'api.bcra.gob.ar'
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        cert_der = ssock.getpeercert(binary_form=True)
        
import ssl
pem = ssl.DER_cert_to_PEM_cert(cert_der)
with open('cert.pem', 'w') as f:
    f.write(pem)
print("Certificado guardado")
