def init(type: str):

    if type == "RP2040":
        from .rp2040_dll import HIDDevice
    elif type == "RP2040_HOST":
        from .rp2040_host_dll import HIDDevice
    elif type == "ARDUINO":
        from .arduino_dll import HIDDevice
    else:
        HIDDevice = None
    return HIDDevice
