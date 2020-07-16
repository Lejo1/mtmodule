protocol_id = b"\x4f\x45\x74\x03"
protocol_version_min = b"\x00\x25"
protocol_version_max = b"\x00\x27"
serialization_version = b"\x1c"
server_peer_id = b"\x00\x01"
seqnum_initial = 65500
seqnum_max = 65535

# major minor patch full(as std_string)
version = b"\x05" + b"\x02" + b"\x00" + b"\x00" + b"\x00\x0B5.2.0-mtbot"
#         major     minor     patch     reserved  version-string

tc = {
    "hello": b"\x00\x02",
    "auth_accept": b"\x00\x03",
    "accept_sudo_mode": b"\x00\x04",
    "deny_sudo_mode": b"\x00\x05",
    "access_denied": b"\x00\x0A",
    "blockdata": b"\x00\x20",
    "addnode": b"\x00\x21",
    "removenode": b"\x00\x22",
    "inventory": b"\x00\x27",
    "time_of_day": b"\x00\x29",
    "csm_restriction_flags": b"\x00\x2A",
    "player_speed": b"\x00\x2B",
    "chat_message": b"\x00\x2F",
    "active_object_remove_add": b"\x00\x31",
    "active_object_messages": b"\x00\x32",
    "hp": b"\x00\x33",
    "move_player": b"\x00\x34",
    "access_denied_legacy": b"\x00\x35",
    "fov": b"\x00\x36",
    "deathscreen": b"\x00\x37",
    "media": b"\x00\x38",
    "tooldef": b"\x00\x39",
    "nodedef": b"\x00\x3a",
    "craftitemdef": b"\x00\x3b",
    "announce_media": b"\x00\x3c",
    "itemdef": b"\x00\x3d",
    "play_sound": b"\x00\x3f",
    "stop_sound": b"\x00\x40",
    "privileges": b"\x00\x41",
    "inventory_formspec": b"\x00\x42",
    "detached_inventory": b"\x00\x43",
    "show_formspec": b"\x00\x44",
    "movement": b"\x00\x45",
    "spawn_particle": b"\x00\x46",
    "particlespawner": b"\x00\x47",
    "hudadd": b"\x00\x49",
    "hudrm": b"\x00\x4a",
    "hudchange": b"\x00\x4b",
    "hud_set_flags": b"\x00\x4c",
    "hud_set_param": b"\x00\x4d",
    "breath": b"\x00\x4e",
    "set_sky": b"\x00\x4f",
    "override_day_night_ratio": b"\x00\x50",
    "local_player_animations": b"\x00\x51",
    "eye_offset": b"\x00\x52",
    "delete_particlespawner": b"\x00\x53",
    "cloud_params": b"\x00\x54",
    "fade_sound": b"\x00\x55",
    "update_player_list": b"\x00\x56",
    "modchannel_msg": b"\x00\x57",
    "modchannel_signal": b"\x00\x58",
    "nodemeta_changed": b"\x00\x59",
    "srp_bytes_s_b": b"\x00\x60",
    "formspec_prepend": b"\x00\x61"
}

ts = {
    "get_peer": b"\x00\x00",
    "init": b"\x00\x02",
    "init2": b"\x00\x11",
    "modchannel_join": b"\x00\x17",
    "modchannel_leave": b"\x00\x18",
    "modchannel_msg": b"\x00\x19",
    "playerpos": b"\x00\x23",
    "gotblocks": b"\x00\x24",
    "deletedblocks": b"\x00\x25",
    "inventory_action": b"\x00\x31",
    "chat_message": b"\x00\x32",
    "damage": b"\x00\x35",
    "playeritem": b"\x00\x37",
    "respawn": b"\x00\x38",
    "interact": b"\x00\x39",
    "removed_sounds": b"\x00\x3a",
    "nodemeta_fields": b"\x00\x3b",
    "inventory_fields": b"\x00\x3c",
    "request_media": b"\x00\x40",
    "client_ready": b"\x00\x43",
    "first_srp": b"\x00\x50",
    "srp_bytes_a": b"\x00\x51",
    "srp_bytes_m": b"\x00\x52"
}

ts_commandspecs = {
    "get_peer": (0, True),
    "init": (1, False),
    "init2": (1, True),
    "modchannel_join": (0, True),
    "modchannel_leave": (0, True),
    "modchannel_msg": (0, True),
    "playerpos": (0, False),
    "gotblocks": (2, True),
    "deletedblocks": (2, True),
    "inventory_action": (0, True),
    "chat_message": (0, True),
    "damage": (0, True),
    "playeritem": (0, True),
    "respawn": (0, True),
    "interact": (0, True),
    "removed_sounds": (2, True),
    "nodemeta_fields": (0, True),
    "inventory_fields": (0, True),
    "request_media": (1, True),
    "client_ready": (1, True),
    "first_srp": (1, True),
    "srp_bytes_a": (1, True),
    "srp_bytes_m": (1, True)
}

accessDeniedStrings = [
    "Invalid password",
    "Your client sent something the server didn't expect.  Try reconnecting or updating your client",
    "The server is running in simple singleplayer mode.  You cannot connect.",
    "Your client's version is not supported.\nPlease contact server administrator.",
    "Player name contains disallowed characters.",
    "Player name not allowed.",
    "Too many users.",
    "Empty passwords are disallowed.  Set a password and try again.",
    "Another client is connected with this name.  If your client closed unexpectedly, try again in a minute.",
    "Server authentication failed.  This is likely a server error.",
    "",
    "Server shutting down.",
    "This server has experienced an internal error. You will now be disconnected."
]

packagetype = {
    "control": b"\x00",
    "original": b"\x01",
    "split": b"\x02",
    "reliable": b"\x03",
}

controltype = {
    "ack": b"\x00",
    "set_peer_id": b"\x01",
    "ping": b"\x02",
    "disco": b"\x03",
}

authmechanism = {
    "none": b"\x00\x00\x00\x00",
    "legacy": b"\x00\x00\x00\x01",
    "srp": b"\x00\x00\x00\x02",
    "first_srp": b"\x00\x00\x00\x04",
}

channel = [
    b"\x00",
    b"\x01",
    b"\x02"
]


def get(command):
    for name, com in tc.items():
        if command == com:
            return name
