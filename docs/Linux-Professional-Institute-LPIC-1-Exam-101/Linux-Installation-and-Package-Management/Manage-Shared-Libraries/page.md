# Example: Start the VM
virsh start TestMachine

# Verify running VMs
virsh list
```

> `reset` simulates pressing the reset button.\
> `destroy` cuts power immediately—like unplugging the VM.

***

## 5. Deleting a Domain

Remove the domain definition only:

```bash theme={null}
virsh undefine TestMachine
```

<Callout icon="triangle-alert">
  `--remove-all-storage` will also delete associated disk images:

  ```bash theme={null}
  virsh undefine TestMachine --remove-all-storage
  ```
</Callout>

***

## 6. Autostart Configuration

Enable the VM to start on host boot:

```bash theme={null}
virsh autostart TestMachine
```

Disable autostart:

```bash theme={null}
virsh autostart --disable TestMachine
```

***

## 7. Inspecting VM Details

Retrieve detailed VM information:

```bash theme={null}
virsh dominfo TestMachine
```

Sample output:

```text theme={null}
Id:             -
Name:           TestMachine
UUID:           01a57937-3fbb-4191-9cec-a73383456fa8
OS Type:        hvm
State:          shut off
CPU(s):         1
Max memory:     1048576 KiB
Used memory:    1048576 KiB
Persistent:     yes
Autostart:      disable
```

***

## 8. Modifying VM Resources

### Adjusting vCPUs

Increase maximum vCPUs:

```bash theme={null}
virsh setvcpus TestMachine 2 --config --maximum
```

Set vCPUs for next boot:

```bash theme={null}
virsh setvcpus TestMachine 2 --config
```

### Adjusting Memory

Set maximum memory:

```bash theme={null}
virsh setmaxmem TestMachine 2048M --config
```

Verify changes:

```bash theme={null}
virsh dominfo TestMachine
```

***

## 9. Starting and Verifying Changes

Start the VM with updated resources:

```bash theme={null}
virsh start TestMachine
```

Confirm the running state:

```bash theme={null}
virsh dominfo TestMachine
```

Expected fields:

```text theme={null}
State:        running
CPU(s):       2
Max memory:   2097152 KiB
Used memory:  2097152 KiB
```

***

## Quick Reference: Common `virsh` Commands

| Command                                                    | Description                |
| ---------------------------------------------------------- | -------------------------- |
| virsh define \<file>.xml                                   | Define a new VM domain     |
| virsh start \<domain>                                      | Start a VM                 |
| virsh shutdown \<domain>                                   | Graceful shutdown          |
| virsh destroy \<domain>                                    | Forced power off           |
| virsh reboot \<domain>                                     | Reboot VM                  |
| virsh reset \<domain>                                      | Forced reset               |
| virsh list \[--all]                                        | List VMs (active/inactive) |
| virsh undefine \<domain> \[--remove-all-storage]           | Remove VM definition       |
| virsh autostart \<domain> \[--disable]                     | Enable/disable autostart   |
| virsh dominfo \<domain>                                    | Show domain information    |
| virsh setvcpus \<domain> \<count> \[--config] \[--maximum] | Adjust vCPUs               |
| virsh setmaxmem \<domain> \<size> \[--config]              | Adjust max memory          |

***

## References

* [Libvirt Documentation](https://libvirt.org/docs.html)
* [QEMU Official Website](https://www.qemu.org/)
* [KVM on Linux](https://www.linux-kvm.org/)
* [Cloud Providers Comparison](https://aws.amazon.com/compare/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/6cd15bbf-73f8-4fee-9bfb-c6923d53698e" />
</CardGroup>


# Manage Shared Libraries

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Manage-Shared-Libraries/page

This article explores managing shared libraries on Linux, covering compilation, linking, library types, naming conventions, paths, linker configuration, and dependency inspection.

In this lesson, we explore how to manage shared libraries on Linux. You’ll learn about compilation vs. linking, static and dynamic libraries, naming conventions, library paths, dynamic linker configuration, and dependency inspection.

## 1. Compilation vs. Linking

Building an executable from source involves two key steps:

1. **Compilation**\
   The compiler (e.g., `gcc`) translates source files (`.c`, `.cpp`) into object files (`.o`).

2. **Linking**\
   The linker combines object files and connects them to libraries, producing the final executable.

Linking can be:

* **Static**: Library code is embedded into the executable.
* **Dynamic**: Executable references shared libraries at runtime.

<Frame>
  ![The image is an educational slide explaining software libraries, compilers, linkers, and the concept of linking, including static and dynamic linking.](https://kodekloud.com/kk-media/image/upload/v1752881442/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Manage-Shared-Libraries/software-libraries-compilers-linkers-linking.jpg)
</Frame>

## 2. Static Libraries vs. Shared Libraries

### Static Libraries (.a)

* Merged into the executable at link time.
* No runtime dependency on external files.
* Larger binary size, but fully self-contained.

<Callout icon="lightbulb">
  Static linking increases the size of the executable since all used library code is included.
</Callout>

### Shared (Dynamic) Libraries (.so)

* Executable holds references, not library code.
* Resolved by the dynamic linker at runtime.
* Multiple programs can share a single library instance in memory, saving disk and RAM.

<Frame>
  ![The image explains the difference between static and shared libraries. Static libraries are merged with the program at link time with no runtime dependencies, while shared libraries are not merged and must be available at runtime.](https://kodekloud.com/kk-media/image/upload/v1752881443/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Manage-Shared-Libraries/static-vs-shared-libraries-explained.jpg)
</Frame>

## 3. Shared Library Naming Conventions

Shared libraries follow the SONAME pattern:

```text theme={null}
lib{name}.so.{major}
```

* `lib`: prefix
* `.so`: shared object
* `{major}`: major version

Example:

```text theme={null}
libpthread.so.0
```

<Frame>
  ![The image shows a terminal interface with a section explaining naming conventions for shared libraries, including components like library name, shared object, and version number, with an example given as "libpthread.so.0".](https://kodekloud.com/kk-media/image/upload/v1752881444/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Manage-Shared-Libraries/terminal-naming-conventions-shared-libraries.jpg)
</Frame>

On Debian 9.9, the GNU C library’s SONAME is `libc.so.6`, typically a symlink to the full version. Static archives end with `.a`, for example `libpthread.a`.

## 4. Common Library Locations

Shared libraries are usually installed in these directories:

| Directory        | Description              |
| ---------------- | ------------------------ |
| `/lib`           | 32-bit system libraries  |
| `/lib32`         | 32-bit compatibility     |
| `/lib64`         | 64-bit system libraries  |
| `/usr/lib`       | Standard library path    |
| `/usr/local/lib` | Local (custom) libraries |

## 5. Dynamic Linker Configuration

The dynamic linker (`ld.so` or `ld-linux.so`) reads `/etc/ld.so.conf` to locate libraries:

```text theme={null}
include /etc/ld.so.conf.d/*.conf
```

Each file in `/etc/ld.so.conf.d/` lists absolute library directories, for example:

```text theme={null}
/usr/local/lib
```

After editing, rebuild the cache and create necessary symlinks:

```bash theme={null}
sudo ldconfig -v
```

Sample output:

```bash theme={null}
/usr/local/lib:
/lib/x86_64-linux-gnu:
    libfuse.so.2 -> libfuse.so.2.9.7
    libnss_myhostname.so.2 -> libnss_myhostname.so.2
    libidn.so.11 -> libidn.so.11.6.16
    ...
```

Query for a specific library:

```bash theme={null}
sudo ldconfig -p | grep libfuse
