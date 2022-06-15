import base64
import json
import hmac
import hashlib

secret = "SSO-JWT-SECRET-KEY"
header = {
    "alg": "HS256",
    "typ": "JWT"
}
jwtString = ''


def base64encode(data):
    data_in = b'.'
    # encode data to ascii first
    if isinstance(data, bytes):
        data_in = data
    else:
        data_in = data.encode('ascii')

    data_encoded = base64.b64encode(data_in)
    # replace '+' with '-', '/' with '_'
    data_encoded = data_encoded.replace(
        b'+', b'-').replace(b'/', b'_')
    # strip '=' and return it
    return data_encoded.strip(b'=')


def base64decode(data):
    data_encoded = data.replace(
        b'-', b'+').replace(b'_', b'/')
    data_encoded = data_encoded + b'='*(len(data) % 4)
    return base64.b64decode(data_encoded)


def generateJWT(algo, header, payload, secret):
    header_encoded = base64encode(json.dumps(header))
    payload_encoded = base64encode(json.dumps(payload))
    data_encoded = header_encoded + b'.' + payload_encoded
    raw_signature = hmac.new(secret.encode(
        'ascii'), data_encoded, algo).digest()
    signature_encoded = base64encode(raw_signature)
    jwt_string = data_encoded + b'.' + signature_encoded
    return jwt_string


def verifyJWT(algo, jwt, secret):
    header_encoded, payload_encoded, signature_encoded = jwt.split(b'.')
    data_encoded = header_encoded + b'.' + payload_encoded
    signature = base64decode(signature_encoded)
    raw_signature = hmac.new(secret.encode(
        'ascii'), data_encoded, algo).digest()
    if (hmac.compare_digest(signature, raw_signature)):
        payload = json.loads(base64decode(payload_encoded))
        return payload
    else:
        return 'gagal'


def encodeJWT(payload):
    return generateJWT(hashlib.sha256, header, payload, secret)


def decodeJWT(jwt):
    return verifyJWT(hashlib.sha256, jwt, secret)
