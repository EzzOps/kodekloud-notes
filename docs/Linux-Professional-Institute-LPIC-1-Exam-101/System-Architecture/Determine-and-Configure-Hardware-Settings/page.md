# Determine and Configure Hardware Settings

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/System-Architecture/Determine-and-Configure-Hardware-Settings/page

This guide explains how to configure hardware settings, detect devices, manage kernel modules, and explore kernel information in Linux.

Modern hardware requires proper configuration before and after installing an operating system. In this guide, you’ll learn how to configure firmware settings (BIOS/UEFI), detect hardware in Linux, inspect devices on PCI and USB buses, manage kernel modules, and explore kernel information in `/proc` and `/sys`.

## 1. Firmware Configuration: BIOS vs UEFI

Computers use firmware interfaces to initialize hardware and start the boot process. Legacy systems rely on BIOS (Basic Input/Output System), while most modern machines use UEFI (Unified Extensible Firmware Interface).

| Feature                   | BIOS                                | UEFI                                                |
| ------------------------- | ----------------------------------- | --------------------------------------------------- |
| Initialization            | Legacy MBR boot                     | GPT support, faster boot                            |
| Configuration interface   | Text-based menu                     | Graphical menu, mouse support                       |
| Firmware updates          | Manufacturer-specific flasher tools | Built-in update utilities                           |
| Hardware testing & config | Basic POST (Power-On Self-Test)     | Extended diagnostics, secure boot, variable storage |

<Frame>
  ![The image is a diagram explaining the acronyms BIOS, UEFI, and POST, with their full forms: Basic Input/Output System, Unified Extensible Firmware Interface, and Power-On Self-Test.](https://kodekloud.com/kk-media/image/upload/v1752881459/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Determine-and-Configure-Hardware-Settings/bios-uefi-post-acronyms-diagram.jpg)
</Frame>

During POST, your firmware checks CPU, memory, and motherboard health. To enter the setup utility, press the key shown on-screen (often **F2**, **Delete**, or **F12**). Inside you can:

* Set the hardware clock’s date and time
* Enable/disable onboard peripherals (LAN, audio)
* Configure RAM error protection (ECC)
* Adjust IRQ and DMA channels
* Define boot device priority
* Enable performance features (XMP, virtualization)
* Disable unused hardware for security or power saving

<Callout icon="triangle-alert">
  Changing firmware settings can affect system stability. Always document original values before modifying.
</Callout>

## 2. Detecting Hardware in Linux

Once Linux boots, it discovers and initializes hardware. Missing devices usually indicate a faulty component or port; detected but non-functional devices often need the correct kernel module (driver).\
Here are the primary inspection tools:

| Tool    | Purpose                    | Example       |
| ------- | -------------------------- | ------------- |
| lspci   | List PCI/PCIe devices      | `sudo lspci`  |
| lsusb   | List USB devices           | `sudo lsusb`  |
| lsmod   | Show loaded kernel modules | `lsmod`       |
| modinfo | Display module details     | `modinfo snd` |

### 2.1 Inspecting PCI Devices with lspci

The `lspci` utility enumerates PCI/PCIe devices:

```bash theme={null}
sudo lspci
```

Sample output:

```text theme={null}
00:00.0 Host bridge: Intel Corporation 440FX - 82441FX PMC [Natoma] (rev 02)
00:03.0 Ethernet controller: Intel Corporation 82540EM Gigabit Ethernet Controller (rev 02)
00:0c.0 USB controller: Intel Corporation 7 Series/C210 Series Chipset Family USB xHCI
```

To get verbose details for a specific device (e.g., `00:03.0`):

```bash theme={null}
sudo lspci -s 00:03.0 -v
```

Show only kernel driver info:

```bash theme={null}
sudo lspci -s 00:03.0 -k
```

### 2.2 Inspecting USB Devices with lsusb

List all USB devices:

```bash theme={null}
sudo lsusb
```

For a tree-view with drivers and speeds:

```bash theme={null}
sudo lsusb -t
```

Query a specific device by bus and device number:

```bash theme={null}
sudo lsusb -s 01:20
```

## 3. Managing Kernel Modules

Kernel modules enable Linux to communicate with hardware.

```bash theme={null}
