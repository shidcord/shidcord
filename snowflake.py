"""
snowflake.py - snowflake helper functions

    These functions generate discord-like snowflakes
    that can be used to uniquely identify any object in litecord.
"""
import time
import hashlib
import os
import base64

# encoded in ms
EPOCH = 1420070400000

# internal state
_generated_ids = 0
PROCESS_ID = 1
WORKER_ID = 1

Snowflake = int


def get_invite_code() -> str:
    """Get a random invite code."""
    random_stuff = hashlib.sha512(os.urandom(1024)).digest()
    code = base64.urlsafe_b64encode(random_stuff).decode().replace('=', '5') \
        .replace('_', 'W').replace('-', 'm')
    return code[:6]


def _snowflake(timestamp: int) -> Snowflake:
    """Get a snowflake from a specific timestamp

    This function relies on modifying internal variables
    to generate unique snowflakes. Because of that every call
    to this function will generate a different snowflake,
    even with the same timestamp.

    Arguments
    ---------
    timestamp: int
        Timestamp to be feed in to the snowflake algorithm.
        This timestamp has to be an UNIX timestamp
         with millisecond precision.
    """
    global _generated_ids

    # bits 0-12 encode _generated_ids (size 12)
    genid_b = '{0:012b}'.format(_generated_ids)

    # bits 12-17 encode PROCESS_ID (size 5)
    procid_b = '{0:05b}'.format(PROCESS_ID)

    # bits 17-22 encode WORKER_ID (size 5)
    workid_b = '{0:05b}'.format(WORKER_ID)

    # bits 22-64 encode (timestamp - EPOCH) (size 42)
    epochized = timestamp - EPOCH
    epoch_b = '{0:042b}'.format(epochized)

    snowflake_b = f'{epoch_b}{workid_b}{procid_b}{genid_b}'
    _generated_ids += 1
    return int(snowflake_b, 2)


def snowflake_time(snowflake: Snowflake) -> float:
    """Get the UNIX timestamp(with millisecond precision, as a float)
    from a specific snowflake.
    """

    # the total size for a snowflake is 64 bits,
    # considering it is a string, position 0 to 42 will give us
    # the `epochized` variable
    snowflake_b = '{0:064b}'.format(snowflake)
    epochized_b = snowflake_b[:42]
    epochized = int(epochized_b, 2)

    # since epochized is the time *since* the EPOCH
    # the unix timestamp will be the time *plus* the EPOCH
    timestamp = epochized + EPOCH

    # convert it to seconds
    # since we don't want to break the entire
    # snowflake interface
    return timestamp / 1000


def get_snowflake():
    """Generate a snowflake"""
    return _snowflake(int(time.time() * 1000))
