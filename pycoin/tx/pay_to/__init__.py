
from ... import ecdsa
from ... import encoding

from .ScriptPayToAddress import ScriptPayToAddress
from .ScriptPayToPublicKey import ScriptPayToPublicKey
from .ScriptPayToScript import ScriptPayToScript
from .ScriptMultisig import ScriptMultisig
from .ScriptUnknown import ScriptUnknown
from .ScriptNulldata import ScriptNulldata

SUBCLASSES = [
    ScriptPayToAddress, ScriptPayToPublicKey, ScriptPayToScript,
    ScriptMultisig, ScriptNulldata, ScriptUnknown
]


def script_obj_from_script(script):
    for sc in SUBCLASSES:
        try:
            st = sc.from_script(script)
            return st
        except ValueError:
            pass
    return None


def build_hash160_lookup(secret_exponents):
    d = {}
    for secret_exponent in secret_exponents:
        public_pair = ecdsa.public_pair_for_secret_exponent(ecdsa.generator_secp256k1, secret_exponent)
        for compressed in (True, False):
            hash160 = encoding.public_pair_to_hash160_sec(public_pair, compressed=compressed)
            d[hash160] = (secret_exponent, public_pair, compressed)
    return d


def build_p2sh_lookup(scripts):
    return dict((encoding.hash160(s), s) for s in scripts)
