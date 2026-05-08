
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
    header = "Network Adapters\n" + "=" * 50
    print(header)
    
    file_content = [header]

    adapters = [a for a in c.Win32_NetworkAdapter() if a.MACAddress]

    if not adapters:
        msg = "  No adapters with a MAC address found."
        print(msg)
        file_content.append(msg)
        with open("mac_addresses.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(file_content) + "\n")
        return

    for adapter in adapters:
        # NetEnabled can be None for non-IP adapters (e.g. Bluetooth)
        if adapter.NetEnabled:
            status = "Enabled"
            lines = [
                f"  Name    : {adapter.Name}",
                f"  MAC     : {adapter.MACAddress}",
                f"  Status  : {status}",
                f"  Type    : {adapter.AdapterType or 'Unknown'}",
                ""
            ]
            for line in lines:
                print(line)
            file_content.extend(lines)
            
    with open("mac_addresses.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(file_content) + "\n")


def check_bitlocker() -> None:
    import wmi

    # BitLocker lives in a separate WMI namespace
    try:
        c = wmi.WMI(namespace="root/CIMV2/Security/MicrosoftVolumeEncryption")
    except wmi.x_wmi:
        msg = "BitLocker WMI namespace not available on this system."
        print(msg)
        with open("mac_addresses.txt", "a", encoding="utf-8") as f:
            f.write("\n" + msg + "\n")
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

    header = "BitLocker Status\n" + "=" * 50
    print(header)
    file_content = ["", header]

    volumes = list(c.Win32_EncryptableVolume())
    if not volumes:
        msg = "  No encryptable volumes found."
        print(msg)
        file_content.append(msg)
        with open("mac_addresses.txt", "a", encoding="utf-8") as f:
            f.write("\n".join(file_content) + "\n")
        return

    for vol in volumes:
        drive = vol.DriveLetter or "(no letter)"
        protection = PROTECTION_STATUS.get(vol.ProtectionStatus, "Unknown")
        conversion = CONVERSION_STATUS.get(vol.ConversionStatus, "Unknown")

        lines = [
            f"  Drive          : {drive}",
            f"  Protection     : {protection}",
            f"  Encryption     : {conversion}",
            ""
        ]
        for line in lines:
            print(line)
        file_content.extend(lines)

    with open("mac_addresses.txt", "a", encoding="utf-8") as f:
        f.write("\n".join(file_content) + "\n")


if __name__ == "__main__":
    assert_windows()
    get_network_adapters()
    check_bitlocker()