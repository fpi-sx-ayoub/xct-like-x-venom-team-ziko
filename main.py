import os
import sys
import json
import time
import base64
import binascii
import logging
import asyncio
import threading
import warnings
import types
from datetime import datetime, timedelta

import requests
import aiohttp
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib3.exceptions import InsecureRequestWarning

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

warnings.simplefilter('ignore', InsecureRequestWarning)


_sym_db = _symbol_database.Default()


def _build_pb2(module_name: str, serialized_file: bytes) -> types.ModuleType:
    """Recreate a *_pb2 module from its serialized FileDescriptorProto bytes."""
    mod = types.ModuleType(module_name)
    mod_globals = mod.__dict__
    descriptor = _descriptor_pool.Default().AddSerializedFile(serialized_file)
    mod_globals['DESCRIPTOR'] = descriptor
    _builder.BuildMessageAndEnumDescriptors(descriptor, mod_globals)
    _builder.BuildTopDescriptorsAndMessages(descriptor, module_name, mod_globals)
    
    sys.modules[module_name] = mod
    return mod


like_pb2 = _build_pb2(
    'like_pb2',
    b'\n\nlike.proto\"#\n\x04like\x12\x0b\n\x03uid\x18\x01 \x01(\x03\x12\x0e\n\x06region\x18\x02 \x01(\tb\x06proto3'
)

like_count_pb2 = _build_pb2(
    'like_count_pb2',
    b'\n\x10like_count.proto\"?\n\tBasicInfo\x12\x0b\n\x03UID\x18\x01 \x01(\x03\x12\x16\n\x0ePlayerNickname\x18\x03 \x01(\t\x12\r\n\x05Likes\x18\x15 \x01(\x03\"\'\n\x04Info\x12\x1f\n\x0b\x41\x63\x63ountInfo\x18\x01 \x01(\x0b\x32\n.BasicInfob\x06proto3'
)

uid_generator_pb2 = _build_pb2(
    'uid_generator_pb2',
    b'\n\x13uid_generator.proto\"0\n\ruid_generator\x12\x0f\n\x07saturn_\x18\x01 \x01(\x03\x12\x0e\n\x06garena\x18\x02 \x01(\x03\x62\x06proto3'
)

my_pb2 = _build_pb2(
    'my_pb2',
    b'\n\x08my.proto\"\xae\t\n\x08GameData\x12\x11\n\ttimestamp\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x14\n\x0cgame_version\x18\x05 \x01(\x05\x12\x14\n\x0cversion_code\x18\x07 \x01(\t\x12\x0f\n\x07os_info\x18\x08 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\t \x01(\t\x12\x18\n\x10network_provider\x18\n \x01(\t\x12\x17\n\x0f\x63onnection_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\x05\x12\x15\n\rscreen_height\x18\r \x01(\x05\x12\x0b\n\x03\x64pi\x18\x0e \x01(\t\x12\x10\n\x08\x63pu_info\x18\x0f \x01(\t\x12\x11\n\ttotal_ram\x18\x10 \x01(\x05\x12\x10\n\x08gpu_name\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x0f\n\x07user_id\x18\x13 \x01(\t\x12\x12\n\nip_address\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x15\n\rplatform_type\x18\x17 \x01(\x05\x12\x1a\n\x12\x64\x65vice_form_factor\x18\x18 \x01(\t\x12\x14\n\x0c\x64\x65vice_model\x18\x19 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x18\n\x10unknown_field_30\x18\x1e \x01(\x05\x12\"\n\x1asecondary_network_provider\x18) \x01(\t\x12!\n\x19secondary_connection_type\x18* \x01(\t\x12\x11\n\tunique_id\x18\x39 \x01(\t\x12\x10\n\x08\x66ield_60\x18< \x01(\x05\x12\x10\n\x08\x66ield_61\x18= \x01(\x05\x12\x10\n\x08\x66ield_62\x18> \x01(\x05\x12\x10\n\x08\x66ield_63\x18? \x01(\x05\x12\x10\n\x08\x66ield_64\x18@ \x01(\x05\x12\x10\n\x08\x66ield_65\x18\x41 \x01(\x05\x12\x10\n\x08\x66ield_66\x18\x42 \x01(\x05\x12\x10\n\x08\x66ield_67\x18\x43 \x01(\x05\x12\x10\n\x08\x66ield_70\x18\x46 \x01(\x05\x12\x10\n\x08\x66ield_73\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x10\n\x08\x66ield_76\x18L \x01(\x05\x12\x10\n\x08\x61pk_info\x18M \x01(\t\x12\x10\n\x08\x66ield_78\x18N \x01(\x05\x12\x10\n\x08\x66ield_79\x18O \x01(\x05\x12\x17\n\x0fos_architecture\x18Q \x01(\t\x12\x14\n\x0c\x62uild_number\x18S \x01(\t\x12\x10\n\x08\x66ield_85\x18U \x01(\x05\x12\x18\n\x10graphics_backend\x18V \x01(\t\x12\x19\n\x11max_texture_units\x18W \x01(\x05\x12\x15\n\rrendering_api\x18X \x01(\x05\x12\x18\n\x10\x65ncoded_field_89\x18Y \x01(\t\x12\x10\n\x08\x66ield_92\x18\\ \x01(\x05\x12\x13\n\x0bmarketplace\x18] \x01(\t\x12\x16\n\x0e\x65ncryption_key\x18^ \x01(\t\x12\x15\n\rtotal_storage\x18_ \x01(\x05\x12\x10\n\x08\x66ield_97\x18\x61 \x01(\x05\x12\x10\n\x08\x66ield_98\x18\x62 \x01(\x05\x12\x10\n\x08\x66ield_99\x18\x63 \x01(\t\x12\x11\n\tfield_100\x18\x64 \x01(\tb\x06proto3'
)

output_pb2 = _build_pb2(
    'output_pb2',
    b'\n\x13jwt_generator.proto\"\xd2\x02\n\nGarena_420\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05place\x18\x03 \x01(\t\x12\x10\n\x08location\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\n\n\x02id\x18\t \x01(\x05\x12\x0b\n\x03\x61pi\x18\n \x01(\t\x12\x0e\n\x06number\x18\x0c \x01(\x05\x12\x1e\n\tGarena420\x18\x0f \x01(\x0b\x32\x0b.Garena_420\x12\x0c\n\x04\x61rea\x18\x10 \x01(\t\x12\x11\n\tmain_area\x18\x12 \x01(\t\x12\x0c\n\x04\x63ity\x18\x13 \x01(\t\x12\x0c\n\x04name\x18\x14 \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0e\n\x06\x62inary\x18\x16 \x01(\x0c\x12\x13\n\x0b\x62inary_data\x18\x17 \x01(\x0c\x1a\"\n\x12\x44\x65\x63rypted_Payloads\x12\x0c\n\x04type\x18\x01 \x01(\x05\x62\x06proto3'
)

_protobuf_pkg = types.ModuleType('protobuf')
_protobuf_pkg.my_pb2 = my_pb2
_protobuf_pkg.output_pb2 = output_pb2
sys.modules['protobuf'] = _protobuf_pkg
sys.modules['protobuf.my_pb2'] = my_pb2
sys.modules['protobuf.output_pb2'] = output_pb2

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

PORT = int(os.environ.get("PORT", 3086))
STORAGE_PATH = "."  

ACCOUNTS_FILE = os.path.join(STORAGE_PATH, "accounts.txt")
TOKEN_FILE = os.path.join(STORAGE_PATH, "token_me.json")

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'
TOKEN_REFRESH_INTERVAL_HOURS = 0.1666  
MAX_WORKERS = 10

scheduler_started = False

REMOTE_CONFIG_URL = "https://redzedupdater.vercel.app/"
# [xCTx Modified] FALLBACK_TOKEN_API removed - now using local Garena API directly (no external dependency)
remote_config = None
remote_config_last_fetch = 0
REMOTE_CONFIG_TTL = 3600


def fetch_remote_config():
    global remote_config, remote_config_last_fetch
    try:
        r = requests.get(REMOTE_CONFIG_URL, timeout=10)
        if r.status_code == 200:
            remote_config = r.json()
            remote_config_last_fetch = time.time()
            app.logger.info(f"Remote config loaded: version {remote_config.get('current_version')}")
            return True
    except Exception as e:
        app.logger.error(f"Failed to fetch remote config: {e}")
    return False


def get_client_url():
    global remote_config
    if not remote_config or (time.time() - remote_config_last_fetch > REMOTE_CONFIG_TTL):
        fetch_remote_config()
    if remote_config and "client_url" in remote_config:
        return remote_config["client_url"].get("etc", "https://clientbp.ggpolarbear.com/")
    return "https://clientbp.ggpolarbear.com/"


def get_server_url():
    global remote_config
    if not remote_config or (time.time() - remote_config_last_fetch > REMOTE_CONFIG_TTL):
        fetch_remote_config()
    if remote_config and "server_url" in remote_config:
        return remote_config["server_url"].rstrip('/')
    return "https://loginbp.ggpolarbear.com"


def get_release_version():
    global remote_config
    if not remote_config or (time.time() - remote_config_last_fetch > REMOTE_CONFIG_TTL):
        fetch_remote_config()
    if remote_config and "latest_release_version" in remote_config:
        return remote_config["latest_release_version"]
    return "OB53"


def decode_jwt_payload(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except:
        return None


def is_token_expired(token):
    try:
        payload = decode_jwt_payload(token)
        if not payload:
            return True
        exp = payload.get('exp')
        if not exp:
            iat = payload.get('iat')
            ttl = payload.get('ttl', 7200)
            if iat:
                exp = iat + ttl
            else:
                return True
        current_time = int(time.time())
        return current_time >= exp
    except:
        return True


def get_token_remaining_time(token):
    try:
        payload = decode_jwt_payload(token)
        if not payload:
            return 0
        exp = payload.get('exp')
        if not exp:
            iat = payload.get('iat')
            ttl = payload.get('ttl', 7200)
            if iat:
                exp = iat + ttl
            else:
                return 0
        remaining = exp - int(time.time())
        return max(0, remaining)
    except:
        return 0


# [xCTx Modified] External fallback API removed completely.
# Token generation now relies exclusively on the local Garena OAuth endpoint.
# This mirrors the logic of the original `app.py` from `api jwt.zip` so the bot
# is fully self-contained and does NOT depend on any external token service.

def get_oauth_token(password, uid):
    """Get OAuth token directly from Garena (no external API).

    This is the merged-in logic from `api jwt.zip / app.py`.
    """

    app.logger.info(f"[LOCAL JWT] Requesting Garena OAuth token for UID {uid}...")
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"

    # Headers identical to the standalone api_jwt app.py for maximum compatibility
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }

    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }

    try:
        r = requests.post(url, headers=headers, data=data, timeout=30, verify=False)
        if r.status_code != 200:
            app.logger.error(f"[LOCAL JWT] Garena returned HTTP {r.status_code} for UID {uid}")
            return None

        try:
            j = r.json()
        except Exception as e:
            app.logger.error(f"[LOCAL JWT] Failed to parse Garena JSON for UID {uid}: {e}")
            return None

        token = (
            j.get("access_token")
            or j.get("token")
            or j.get("session_key")
            or j.get("jwt")
            or (j.get("data") or {}).get("token")
        )

        if not token:
            app.logger.warning(f"[LOCAL JWT] No access_token in Garena response for UID {uid}: {j}")
            return None

        j["access_token"] = token
        app.logger.info(f"[LOCAL JWT] Garena OAuth success for UID {uid}")
        return {
            "access_token": j.get("access_token"),
            "open_id": j.get("open_id", ""),
            "uid": j.get("uid", uid),
            "raw": j,
            "source": "garena_local"
        }
    except Exception as e:
        app.logger.error(f"[LOCAL JWT] Garena OAuth request failed for UID {uid}: {e}")
        return None


def encrypt_aes(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    return cipher.encrypt(padded_message)


def parse_major_login_response(response_content):
    response_dict = {}
    try:
        lines = response_content.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                response_dict[key.strip()] = value.strip().strip('"')
    except:
        pass
    return response_dict


def generate_jwt_token(uid, password):
    token_data = get_oauth_token(password, uid)
    if not token_data or not token_data.get("access_token"):
        app.logger.error(f"No access token for UID {uid} from any source")
        return None

    access_token = token_data["access_token"]
    open_id = token_data.get("open_id", "")
    release_version = get_release_version()
    server_url = get_server_url()
    token_source = token_data.get("source", "unknown")

    game_data = my_pb2.GameData()
    game_data.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    game_data.game_name = "free fire"
    game_data.game_version = 1
    game_data.version_code = "1.108.3"
    game_data.os_info = "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)"
    game_data.device_type = "Handheld"
    game_data.network_provider = "Verizon Wireless"
    game_data.connection_type = "WIFI"
    game_data.screen_width = 1280
    game_data.screen_height = 960
    game_data.dpi = "240"
    game_data.cpu_info = "ARMv7 VFPv3 NEON VMH | 2400 | 4"
    game_data.total_ram = 5951
    game_data.gpu_name = "Adreno (TM) 640"
    game_data.gpu_version = "OpenGL ES 3.0"
    game_data.user_id = f"Google|{uid}-{int(time.time())}"
    game_data.ip_address = "172.190.111.97"
    game_data.language = "en"
    game_data.open_id = open_id
    game_data.access_token = access_token
    game_data.platform_type = 4
    game_data.device_form_factor = "Handheld"
    game_data.device_model = "Asus ASUS_I005DA"
    game_data.field_60 = 32968
    game_data.field_61 = 29815
    game_data.field_62 = 2479
    game_data.field_63 = 914
    game_data.field_64 = 31213
    game_data.field_65 = 32968
    game_data.field_66 = 31213
    game_data.field_67 = 32968
    game_data.field_70 = 4
    game_data.field_73 = 2
    game_data.library_path = "/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/lib/arm"
    game_data.field_76 = 1
    game_data.apk_info = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/base.apk"
    game_data.field_78 = 6
    game_data.field_79 = 1
    game_data.os_architecture = "32"
    game_data.build_number = "2019117877"
    game_data.field_85 = 1
    game_data.graphics_backend = "OpenGLES2"
    game_data.max_texture_units = 16383
    game_data.rendering_api = 4
    game_data.encoded_field_89 = "\u0017T\u0011\u0017\u0002\b\u000eUMQ\bEZ\u0003@ZK;Z\u0002\u000eV\ri[QVi\u0003\ro\t\u0007e"
    game_data.field_92 = 9204
    game_data.marketplace = "3rd_party"
    game_data.encryption_key = "KqsHT2B4It60T/65PGR5PXwFxQkVjGNi+IMCK3CFBCBfrNpSUA1dZnjaT3HcYchlIFFL1ZJOg0cnulKCPGD3C3h1eFQ="
    game_data.total_storage = 111107
    game_data.field_97 = 1
    game_data.field_98 = 1
    game_data.field_99 = "4"
    game_data.field_100 = "4"

    serialized = game_data.SerializeToString()
    encrypted = encrypt_aes(AES_KEY, AES_IV, serialized)

    major_login_url = f"{server_url}/MajorLogin"

    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/octet-stream",
        'Expect': "100-continue",
        'X-GA': "v1 1",
        'X-Unity-Version': "2018.4.11f1",
        'ReleaseVersion': release_version
    }

    try:
        app.logger.info(f"MajorLogin for UID {uid} to {major_login_url}")
        response = requests.post(major_login_url, data=encrypted, headers=headers, verify=False, timeout=30)

        if response.status_code == 200:
            parsed = output_pb2.Garena_420()
            parsed.ParseFromString(response.content)
            result = parse_major_login_response(str(parsed))

            jwt_token = result.get("token")

            if jwt_token:
                app.logger.info(f"JWT generated for UID {uid} via {token_source}")
                return {
                    "uid": str(uid),
                    "token": jwt_token,
                    "region": "ME",
                    "status": "live",
                    "generated_at": int(time.time()),
                    "server_url": server_url,
                    "release_version": release_version,
                    "token_source": token_source
                }
            else:
                app.logger.error(f"No JWT in MajorLogin response for UID {uid}")
        else:
            app.logger.error(f"MajorLogin returned status {response.status_code} for UID {uid}")

        return None
    except Exception as e:
        app.logger.error(f"MajorLogin failed for {uid}: {e}")
        return None


def load_accounts():
    accounts = []
    if not os.path.exists(ACCOUNTS_FILE):
        app.logger.error(f"Accounts file not found: {ACCOUNTS_FILE}")
        return accounts

    with open(ACCOUNTS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                uid, pwd = line.split(":", 1)
                accounts.append({"uid": uid.strip(), "password": pwd.strip()})

    app.logger.info(f"Loaded {len(accounts)} accounts")
    return accounts


def load_tokens():
    if not os.path.exists(TOKEN_FILE):
        app.logger.warning(f"Token file not found: {TOKEN_FILE}")
        return None, 0, 0

    try:
        with open(TOKEN_FILE, "r") as f:
            tokens = json.load(f)

        if not isinstance(tokens, list):
            return None, 0, 0

        valid_tokens = []
        expired_count = 0

        for token_entry in tokens:
            token = token_entry.get("token", "")
            if not token:
                continue

            # Check if token is expired, but still add it for robustness in testing
            if is_token_expired(token):
                expired_count += 1
                # Even if expired, we add it to valid_tokens to try sending likes
                # This ensures the user's request for > 70 likes is met if the tokens still work
                token_entry["expires_in"] = 0
                valid_tokens.append(token_entry)
            else:
                remaining = get_token_remaining_time(token)
                token_entry["expires_in"] = remaining
                valid_tokens.append(token_entry)

        app.logger.info(f"Tokens: {len(valid_tokens)} valid (including expired for retry), {expired_count} expired, {len(tokens)} total")
        return valid_tokens, expired_count, len(tokens)

    except Exception as e:
        app.logger.error(f"Failed to load tokens: {e}")
        return None, 0, 0


def save_tokens(tokens):
    try:
        os.makedirs(os.path.dirname(TOKEN_FILE) if os.path.dirname(TOKEN_FILE) else '.', exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            json.dump(tokens, f, indent=2)
        app.logger.info(f"Saved {len(tokens)} tokens to {TOKEN_FILE}")
        return True
    except Exception as e:
        app.logger.error(f"Failed to save tokens: {e}")
        return False


def refresh_expired_tokens():
    app.logger.info("Refreshing expired tokens...")
    accounts = load_accounts()
    if not accounts:
        app.logger.error("No accounts found")
        return False

    current_tokens = []
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                current_tokens = json.load(f)
        except:
            current_tokens = []

    uid_to_account = {acc["uid"]: acc for acc in accounts}
    tokens_to_refresh = []

    for token_entry in current_tokens:
        uid = token_entry.get("uid")
        token = token_entry.get("token", "")
        if not token or is_token_expired(token):
            if uid in uid_to_account:
                tokens_to_refresh.append(uid_to_account[uid])

    existing_uids = {t.get("uid") for t in current_tokens}
    for acc in accounts:
        if acc["uid"] not in existing_uids:
            tokens_to_refresh.append(acc)

    if not tokens_to_refresh:
        app.logger.info("No tokens need refresh")
        return True

    app.logger.info(f"Refreshing {len(tokens_to_refresh)} tokens...")
    results = []
    threads = []

    def worker(acc):
        result = generate_jwt_token(acc['uid'], acc['password'])
        if result:
            results.append(result)
        time.sleep(0.3)

    for acc in tokens_to_refresh:
        t = threading.Thread(target=worker, args=(acc,))
        threads.append(t)

    for i in range(0, len(threads), MAX_WORKERS):
        batch = threads[i:i + MAX_WORKERS]
        for t in batch:
            t.start()
        for t in batch:
            t.join()

    if results:
        valid_existing = [t for t in current_tokens if not is_token_expired(t.get("token", ""))]
        uid_map = {t["uid"]: t for t in valid_existing}
        for new_token in results:
            uid_map[new_token["uid"]] = new_token
        merged = list(uid_map.values())
        return save_tokens(merged)

    return False


def refresh_all_tokens():
    app.logger.info("Starting full token refresh...")
    accounts = load_accounts()
    if not accounts:
        app.logger.error("No accounts to refresh")
        return

    results = []
    threads = []

    def worker(acc):
        result = generate_jwt_token(acc['uid'], acc['password'])
        if result:
            results.append(result)
        time.sleep(0.5)

    for acc in accounts:
        t = threading.Thread(target=worker, args=(acc,))
        threads.append(t)

    for i in range(0, len(threads), MAX_WORKERS):
        batch = threads[i:i + MAX_WORKERS]
        for t in batch:
            t.start()
        for t in batch:
            t.join()

    if results:
        existing = []
        if os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE, "r") as f:
                    existing = json.load(f)
            except:
                existing = []

        uid_map = {item["uid"]: item for item in existing}
        for new_item in results:
            uid_map[new_item["uid"]] = new_item

        merged = list(uid_map.values())
        save_tokens(merged)
        app.logger.info(f"Saved {len(merged)} tokens to {TOKEN_FILE}")
    else:
        app.logger.error("No tokens generated!")


def scheduled_refresh():
    while True:
        app.logger.info("Starting a new infinite loop cycle for token refresh...")
        refresh_all_tokens()
        app.logger.info("Cycle completed. Restarting infinite loop in 60 seconds...")
        
        time.sleep(60)


def start_scheduler():
    global scheduler_started
    if not scheduler_started:
        t = threading.Thread(target=scheduled_refresh, daemon=True)
        t.start()
        scheduler_started = True
        app.logger.info("Token scheduler started")


def encrypt_for_like(plaintext):
    try:
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        padded = pad(plaintext, AES.block_size)
        encrypted = cipher.encrypt(padded)
        return binascii.hexlify(encrypted).decode('utf-8')
    except:
        return None


def create_like_protobuf(uid, region):
    try:
        msg = like_pb2.like()
        msg.uid = int(uid)
        msg.region = region
        return msg.SerializeToString()
    except:
        return None


def create_uid_protobuf(uid):
    try:
        msg = uid_generator_pb2.uid_generator()
        msg.saturn_ = int(uid)
        msg.garena = 1
        return msg.SerializeToString()
    except:
        return None


def decode_player_info(binary_data):
    if not binary_data or len(binary_data) < 5:
        return None
    try:
        info = like_count_pb2.Info()
        info.ParseFromString(binary_data)
        if info.AccountInfo.UID != 0:
            return info
    except:
        pass
    try:
        basic = like_count_pb2.BasicInfo()
        basic.ParseFromString(binary_data)
        if basic.UID != 0:
            info = like_count_pb2.Info()
            info.AccountInfo.UID = basic.UID
            info.AccountInfo.PlayerNickname = basic.PlayerNickname
            info.AccountInfo.Likes = basic.Likes
            return info
    except:
        pass
    return None


def get_player_info(encrypted_uid, token):
    try:
        client_url = get_client_url()
        url = f"{client_url}GetPlayerPersonalShow"
        edata = bytes.fromhex(encrypted_uid)
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': get_release_version()
        }
        response = requests.post(url, data=edata, headers=headers, verify=False, timeout=15)
        if response.status_code == 401:
            return None, "EXPIRED"
        if response.status_code != 200:
            return None, f"HTTP_{response.status_code}"
        result = decode_player_info(response.content)
        return result, "OK"
    except Exception as e:
        return None, "ERROR"


async def send_like_request(encrypted_uid, token):
    try:
        client_url = get_client_url()
        url = f"{client_url}LikeProfile"
        edata = bytes.fromhex(encrypted_uid)
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': get_release_version()
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=edata, headers=headers, timeout=10) as resp:
                return resp.status
    except:
        return None


async def send_multiple_likes(uid, tokens):
    try:
        proto_data = create_like_protobuf(uid, "ME")
        if not proto_data:
            return None
        encrypted = encrypt_for_like(proto_data)
        if not encrypted:
            return None
        tasks = []
        # Increased range to ensure more likes are delivered
        # Using min(len(tokens), 250) to use as many unique tokens as possible up to 250
        num_to_send = min(len(tokens), 300) 
        for i in range(num_to_send):
            token = tokens[i]["token"]
            tasks.append(send_like_request(encrypted, token))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    except:
        return None


@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "service": "Free Fire Like API - ME Server",
        "timestamp": datetime.now().isoformat(),
        "remote_config": remote_config.get("current_version") if remote_config else "not loaded"
    })


@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200


@app.route('/status', methods=['GET'])
def api_status():
    valid_tokens, expired_count, total_count = load_tokens()
    sample_expiry = None
    if valid_tokens and len(valid_tokens) > 0:
        remaining = get_token_remaining_time(valid_tokens[0].get("token", ""))
        sample_expiry = f"{remaining // 60} minutes"

    return jsonify({
        "status": "running",
        "server": "ME",
        "storage_path": STORAGE_PATH,
        "auto_refresh_hours": TOKEN_REFRESH_INTERVAL_HOURS,
        "total_tokens": total_count,
        "valid_tokens": len(valid_tokens) if valid_tokens else 0,
        "expired_tokens": expired_count,
        "sample_expires_in": sample_expiry,
        "remote_config_version": remote_config.get("current_version") if remote_config else "not loaded",
        "client_url": get_client_url(),
        "server_url": get_server_url()
    })


@app.route('/token_status', methods=['GET'])
def api_token_status():
    valid_tokens, expired_count, total_count = load_tokens()
    if valid_tokens is None:
        return jsonify({"error": "Token file not found"}), 404

    expiring_soon = []
    for t in (valid_tokens or [])[:5]:
        remaining = get_token_remaining_time(t.get("token", ""))
        expiring_soon.append({
            "uid": t.get("uid"),
            "region": t.get("region"),
            "expires_in_minutes": round(remaining / 60, 1)
        })

    return jsonify({
        "server": "ME",
        "total_tokens": total_count,
        "valid_tokens": len(valid_tokens) if valid_tokens else 0,
        "expired_tokens": expired_count,
        "sample_tokens": expiring_soon
    })


@app.route('/generate_token', methods=['GET'])
def api_generate_token():
    uid = request.args.get('uid')
    password = request.args.get('password')

    if not uid or not password:
        return jsonify({"error": "Missing uid or password"}), 400

    result = generate_jwt_token(uid, password)
    if result:
        payload = decode_jwt_payload(result['token'])
        if payload and payload.get('exp'):
            result['expires_at'] = datetime.fromtimestamp(payload['exp']).isoformat()
            result['expires_in_seconds'] = payload['exp'] - int(time.time())
        return jsonify({"status": "success", "data": result})
    return jsonify({"status": "error", "message": "Failed to generate token from all sources"}), 500


@app.route('/refresh_all_tokens', methods=['GET'])
def api_refresh_all():
    def run():
        refresh_all_tokens()
    threading.Thread(target=run).start()
    return jsonify({"status": "started", "message": "Full refresh in progress"})


@app.route('/refresh_expired', methods=['GET'])
def api_refresh_expired():
    def run():
        refresh_expired_tokens()
    threading.Thread(target=run).start()
    return jsonify({"status": "started", "server": "ME", "message": "Refreshing expired tokens"})


@app.route('/like', methods=['GET'])
def handle_like():
    uid = request.args.get("uid")

    if not uid:
        return jsonify({"error": "Missing uid"}), 400

    server_name = "ME"

    try:
        valid_tokens, expired_count, total_count = load_tokens()

        if not valid_tokens or len(valid_tokens) == 0:
            app.logger.warning("No valid tokens, attempting refresh...")
            refresh_success = refresh_expired_tokens()

            if refresh_success:
                valid_tokens, _, _ = load_tokens()

            if not valid_tokens or len(valid_tokens) == 0:
                return jsonify({
                    "error": "No valid tokens available",
                    "message": "Token refresh attempted but failed",
                    "expired_count": expired_count,
                    "total_count": total_count
                }), 500

        check_token = valid_tokens[0]["token"]

        uid_proto = create_uid_protobuf(uid)
        if not uid_proto:
            return jsonify({"error": "UID protobuf failed"}), 500

        encrypted_uid = encrypt_for_like(uid_proto)
        if not encrypted_uid:
            return jsonify({"error": "Encryption failed"}), 500

        before_info, status = get_player_info(encrypted_uid, check_token)

        if status == "EXPIRED":
            app.logger.warning("Token expired during request, refreshing...")
            refresh_expired_tokens()
            valid_tokens, _, _ = load_tokens()

            if not valid_tokens:
                return jsonify({"error": "Token expired and refresh failed"}), 500

            check_token = valid_tokens[0]["token"]
            before_info, status = get_player_info(encrypted_uid, check_token)

        if before_info is None:
            return jsonify({
                "error": "Failed to retrieve player info",
                "token_status": status,
                "valid_tokens_available": len(valid_tokens)
            }), 500

        before_likes = int(before_info.AccountInfo.Likes)
        player_name = str(before_info.AccountInfo.PlayerNickname)
        player_uid = int(before_info.AccountInfo.UID)

        app.logger.info(f"Before: {player_name} has {before_likes} likes")
        
        # Split tokens into batches if needed, but for now we send all available
        # The user wants more than 70, and we have ~270 accounts.
        # We will use the first 150 tokens to ensure we hit the target without being too aggressive.
        target_tokens = valid_tokens[:200] 

        asyncio.run(send_multiple_likes(uid, target_tokens))

        # Increased wait time to allow server to process likes
        time.sleep(8)

        after_info, _ = get_player_info(encrypted_uid, check_token)

        if after_info is None:
            return jsonify({"error": "Failed to get final player info"}), 500

        after_likes = int(after_info.AccountInfo.Likes)
        likes_given = after_likes - before_likes

        return jsonify({
            "LikesAdded": likes_given,
            "LikesGivenByAPI": likes_given,
            "LikesafterCommand": after_likes,
            "LikesbeforeCommand": before_likes,
            "PlayerNickname": player_name,
            "UID": player_uid,
            "message": f"تمت إضافة {likes_given} إعجاب بنجاح" if likes_given > 0 else "فشل في إضافة الإعجابات",
            "status": 1 if likes_given > 0 else 2,
            "tokens_used": len(valid_tokens)
        })

    except Exception as e:
        app.logger.error(f"Like handler error: {e}")
        return jsonify({"error": str(e)}), 500


def init_app():
    fetch_remote_config()
    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH, exist_ok=True)

    source_accounts = os.path.abspath(os.path.join(os.path.dirname(__file__), "accounts.txt"))
    target_accounts = os.path.abspath(ACCOUNTS_FILE)

    if os.path.exists(source_accounts) and source_accounts != target_accounts:
        import shutil
        try:
            shutil.copy2(source_accounts, target_accounts)
            app.logger.info(f"Copied accounts.txt to {target_accounts}")
        except Exception as e:
            app.logger.error(f"Failed to copy accounts: {e}")
    elif not os.path.exists(target_accounts):
        with open(ACCOUNTS_FILE, 'w') as f:
            f.write("# Format: uid:password\n")
        app.logger.info(f"Created empty {ACCOUNTS_FILE}")

    start_scheduler()


init_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False, threaded=True)
