from core.rsa import sign, verify, gen_keys
from core.sha import sha64
from config import DATA_DIR
import flask, binascii, json, random, os

routes = flask.Blueprint('routes', __name__)

@routes.route('/api/generate', methods=['GET'])
def generate_keys():

    keys = gen_keys()
    # Retornar como strings para evitar perda de precisão no JavaScript (Number > 2^53-1)
    return {
        'n': str(keys[0]),
        'e': str(keys[1]),
        'd': str(keys[2])
    }

@routes.route('/api/sign', methods=['POST'])
def sign_message():
    if 'file' not in flask.request.files:
        return {'error': 'file field is required'}, 400
    file = flask.request.files['file']

    n_str = flask.request.form.get('n')
    d_str = flask.request.form.get('d')
    if n_str is None or d_str is None:
        return {'error': 'n and d are required'}, 400
    try:
        n = int(str(n_str).strip())
        d = int(str(d_str).strip())
    except (ValueError, TypeError):
        return {'error': 'Invalid key values (n/d must be integers as strings)'}, 400

    file_content = file.read()
    hash_bytes, salt = sha64(file_content)
    signature_int = sign(hash_bytes, d, n)

    signature_data = {
        'filename': file.filename,
        'hash': binascii.hexlify(hash_bytes).decode('utf-8'),
        'salt': binascii.hexlify(salt).decode('utf-8'),
        'signature': str(signature_int)
    }

    sig_file_path = os.path.join(DATA_DIR, f"{file.filename}_{random.getrandbits(16)}.sig")
    with open(sig_file_path, 'w') as sig_file:
        json.dump(signature_data, sig_file, indent=4)

    with open(sig_file_path, 'r') as sig_file:
        saved_signature_data = json.load(sig_file)

    return saved_signature_data

@routes.route('/api/verify', methods=['POST'])
def verify_signature():
    if 'file' not in flask.request.files:
        return {'error': 'file field is required'}, 400
    file = flask.request.files['file']

    sig_str = flask.request.form.get('signature')
    n_str = flask.request.form.get('n')
    e_str = flask.request.form.get('e')
    salt_hex = flask.request.form.get('salt')

    if sig_str is None or n_str is None or e_str is None or salt_hex is None:
        return {'error': 'signature, n, e, and salt are required'}, 400
    
    try:
        signature = int(str(sig_str).strip())
        n = int(str(n_str).strip())
        e = int(str(e_str).strip())
        salt = binascii.unhexlify(str(salt_hex).strip())
        
    except (ValueError, TypeError, binascii.Error):
        return {'error': 'Invalid values: signature/n/e must be integers; salt must be hex'}, 400

    # Recalcular hash do arquivo com o mesmo salt
    file_content = file.read()
    hash_bytes, salt = sha64(file_content, salt)

    # Verificar a assinatura
    is_valid = verify(signature, hash_bytes, e, n)

    return {
        'filename': file.filename,
        'hash': binascii.hexlify(hash_bytes).decode('utf-8'),
        'signature': str(signature),
        'valid': is_valid
    }