from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes


def create_csr(private_key, filename, tab: list):

    subject = x509.Name([            
            x509.NameAttribute(NameOID.COUNTRY_NAME, tab[0:14][1]),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, tab[0:13][3]),
            x509.NameAttribute(NameOID.LOCALITY_NAME, tab[0:14][5]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, tab[0:14][7]),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, tab[0:14][9]),
            x509.NameAttribute(NameOID.COMMON_NAME, tab[0:14][13]),     
        ])
    # Generate any alternative dns names
    
    alt_names = []
    for name in tab[0:14][13]:

        alt_names.append(x509.DNSName(name))

    san = x509.SubjectAlternativeName(alt_names)


    builder = (x509.CertificateSigningRequestBuilder().subject_name(subject).add_extension(san, critical=False))
    csr = builder.sign(private_key, hashes.SHA256(), default_backend())

    with open(filename, "wb") as csrfile:

        csrfile.write(csr.public_bytes(serialization.Encoding.PEM))


    return csr


def sign_csr(csr, ca_public_key, ca_private_key, new_filename):

    valid_from = datetime.utcnow()

    valid_until = valid_from + timedelta(days=100)


    builder = (

        x509.CertificateBuilder()

        .subject_name(csr.subject)

        .issuer_name(ca_public_key.subject)

        .public_key(csr.public_key())

        .serial_number(x509.random_serial_number())

        .not_valid_before(valid_from)

        .not_valid_after(valid_until)

    )


    for extension in csr.extensions:

        builder = builder.add_extension(extension.value, extension.critical)


    public_key = builder.sign(private_key=ca_private_key,algorithm=hashes.SHA256(),backend=default_backend(),)


    with open(new_filename, "wb") as keyfile:

        keyfile.write(public_key.public_bytes(serialization.Encoding.PEM))