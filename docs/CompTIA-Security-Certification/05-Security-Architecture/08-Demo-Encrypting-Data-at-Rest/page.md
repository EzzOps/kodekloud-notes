# Demo Encrypting Data at Rest

Source: https://notes.kodekloud.com/docs/CompTIA-Security-Certification/Security-Architecture/Demo-Encrypting-Data-at-Rest/page

This demo explains how to secure data at rest by configuring full-disk encryption on a Linux host.

Welcome to this demo from the KodeKloud [CompTIA Security+ Certification Preparation Course](https://learn.kodekloud.com/user/courses/comptia-security-certification). In this guide, we explain how to secure data at rest by configuring full-disk encryption on a Linux host. Full-disk encryption is essential for protecting confidential data and preventing unauthorized access in scenarios such as server theft, compromise, or repurposing.

Below, you will find a step-by-step process to set up an encrypted disk, create an XFS file system on the encrypted device, close the device mapping, and format another device with LUKS encryption.

***

## Step 1: Setting Up an Encrypted Disk Using Plain Encryption

Begin by setting up an encrypted disk with plain encryption. In this example, the mapped device is named "secretdisk". Run the following command:

```bash theme={null}
sudo cryptsetup open --type plain /dev/vdb secretdisk
```

Enter the passphrase when prompted (for example, "s3" or the one specified in your lab instructions).

***

## Step 2: Creating an XFS File System on the Mapped Device

With the encrypted device activated, create an XFS file system on it by executing:

```bash theme={null}
sudo mkfs.xfs /dev/mapper/secretdisk
```

This command outputs confirmation details, including metadata such as block size and inode size.

***

## Step 3: Closing the Mapped Device

After verifying that the file system has been created successfully, remove the encryption mapping to secure your configuration with:

```bash theme={null}
sudo cryptsetup close secretdisk
```

This action finalizes the plain encryption setup for the device.

***

## Step 4: Formatting a Device with LUKS Encryption

Next, transition to formatting a device using LUKS encryption, which offers enhanced security features. The process involves the following steps:

1. Open and initialize the encrypted device with plain encryption.
2. Create the XFS file system.
3. Close the mapped device.
4. Format the target device with LUKS encryption.

Execute the combined commands below:

```bash theme={null}
