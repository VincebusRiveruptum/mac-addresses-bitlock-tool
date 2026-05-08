
"""
windows_hw_info.py

Retrieves MAC addresses for all installed network adapters and checks
BitLocker protection status on the Windows system drive.

Requirements (Windows only):
    pip install wmi
"""

import platform
import sys


def assert_windows() -> None:
    if platform.system() != "Windows":
        print("This script only runs on Windows.")
        sys.exit(0)


def get_network_adapters() -> None:
    import wmi

    c = wmi.WMI()
    print("Network Adapters")
    print("=" * 50)

    adapters = [a for a in c.Win32_NetworkAdapter() if a.MACAddress]

    if not adapters:
        print("  No adapters with a MAC address found.")
        return

    for adapter in adapters:
        # NetEnabled can be None for non-IP adapters (e.g. Bluetooth)
        status = (
            "Enabled" if adapter.NetEnabled
            else "Disabled" if adapter.NetEnabled is False
            else "N/A"
        )
        print(f"  Name    : {adapter.Name}")
        print(f"  MAC     : {adapter.MACAddress}")
        print(f"  Status  : {status}")
        print(f"  Type    : {adapter.AdapterType or 'Unknown'}")
        print()


def check_bitlocker() -> None:
    import wmi

    # BitLocker lives in a separate WMI namespace
    try:
        c = wmi.WMI(namespace="root/CIMV2/Security/MicrosoftVolumeEncryption")
    except wmi.x_wmi:
        print("BitLocker WMI namespace not available on this system.")
        return

    PROTECTION_STATUS = {
        0: "OFF  — Volume is unprotected",
        1: "ON   — Volume is protected",
        2: "UNKNOWN",
    }

    CONVERSION_STATUS = {
        0: "Fully Decrypted",
        1: "Fully Encrypted",
        2: "Encryption in Progress",
        3: "Decryption in Progress",
        4: "Encryption Paused",
        5: "Decryption Paused",
    }

    print("BitLocker Status")
    print("=" * 50)

    volumes = list(c.Win32_EncryptableVolume())
    if not volumes:
        print("  No encryptable volumes found.")
        return

    for vol in volumes:
        drive = vol.DriveLetter or "(no letter)"
        protection = PROTECTION_STATUS.get(vol.ProtectionStatus, "Unknown")
        conversion = CONVERSION_STATUS.get(vol.ConversionStatus, "Unknown")

        print(f"  Drive          : {drive}")
        print(f"  Protection     : {protection}")
        print(f"  Encryption     : {conversion}")
        print()


if __name__ == "__main__":
    assert_windows()
    get_network_adapters()
    check_bitlocker()