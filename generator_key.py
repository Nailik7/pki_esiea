from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

from cryptography import x509

from cryptography.x509.oid import NameOID

from cryptography.hazmat.primitives import hashes


def generate_private_key(filename: str, passphrase: str):

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())


    utf8_pass = passphrase.encode("utf-8")

    algorithm = serialization.BestAvailableEncryption(utf8_pass)


    with open(filename, "wb") as file:

        file.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.TraditionalOpenSSL,encryption_algorithm=algorithm,))


    return private_key

def generate_public_key(private_key, filename, **kwargs):

    subject = x509.Name(

        [

            x509.NameAttribute(NameOID.COUNTRY_NAME, kwargs["country"]),

            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, kwargs["state"]),

            x509.NameAttribute(NameOID.LOCALITY_NAME, kwargs["locality"]),

            x509.NameAttribute(NameOID.ORGANIZATION_NAME, kwargs["org"]),

            x509.NameAttribute(NameOID.COMMON_NAME, kwargs["hostname"]),

        ]

    )


    # Because this is self signed, the issuer is always the subject

    #issuer = subject


    

    valid_from = datetime.utcnow()

    valid_to = valid_from + timedelta(days=100)


    # Used to build the certificate

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


    # Sign the certificate with the private key

    public_key = builder.sign(

        private_key, hashes.SHA256(), default_backend()

    )


    with open(filename, "wb") as certfile:

        certfile.write(public_key.public_bytes(serialization.Encoding.PEM))


    return public_key



