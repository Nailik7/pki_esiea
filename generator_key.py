from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

from cryptography import x509

from cryptography.x509.oid import NameOID

from cryptography.hazmat.primitives import hashes


def generator_private_key(filename: str, passphrase: str):

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())


    utf8_pass = passphrase.encode("utf-8")

    algorithm = serialization.BestAvailableEncryption(utf8_pass)


    with open(filename, "wb") as file:

        file.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.TraditionalOpenSSL,encryption_algorithm=algorithm,))


    return private_key

def generator_public_key(private_key, filename, tab: list):

    subject = x509.Name(

        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, tab[0:12][1]),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, tab[0:12][3]),
            x509.NameAttribute(NameOID.LOCALITY_NAME, tab[0:12][5]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, tab[0:12][7]),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, tab[0:12][9]),
            x509.NameAttribute(NameOID.COMMON_NAME, tab[0:12][11]),

        ]

    )




    valid_from = datetime.utcnow()

    valid_to = valid_from + timedelta(days=100)


    builder = (

        x509.CertificateBuilder()

        .subject_name(subject)

        .issuer_name(subject)

        .public_key(private_key.public_key())

        .serial_number(x509.random_serial_number())

        .not_valid_before(valid_from)

        .not_valid_after(valid_to)

        .add_extension(x509.BasicConstraints(ca=True,path_length=None), critical=True)

    )



    public_key = builder.sign(private_key, hashes.SHA256(), default_backend())


    with open(filename, "wb") as certfile:

        certfile.write(public_key.public_bytes(serialization.Encoding.PEM))


    return public_key



