def init(type: str):

    if type == "RP2040_HOST":
        from .rp2040_host_dll import HIDDevice
    else:
        HIDDevice = None
    return HIDDevice
