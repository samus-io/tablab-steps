# What are the Alternate Data Streams (ADS)?

* **Alternate Data Streams (ADS)** are a feature of the NTFS file system that allows data to be stored in a file outside the main data stream. This means a single file can have multiple streams of data associated with it, which can be used for various purposes such as storing additional metadata (like author, title, or comments).
* For example, if the **Main File** is `document.txt`, then `document.txt:metadata` is the ADS of it.

* The **New Technology File System (NTFS)** is a file system developed by **Microsoft** for **Windows operating systems**. NTFS provides several advanced features compared to older file systems like FAT32:
  * **Metadata Support**: NTFS supports rich metadata, allowing for enhanced file organization and search capabilities.
  * **Security**: it includes file-level security, permissions, and encryption.
  * **File compression**: NTFS supports on-the-fly file compression.
  * **Large File and Volume Support**: it can handle very large files and volumes efficiently.
  * **Journaling**: NTFS uses a transaction log to help recover from errors quickly.

* Malware authors exploit ADS to hide their malicious payloads within legitimate files, making detection by antivirus software more challenging. Here's how it works:
  * **Hiding Payloads**: a malicious payload can be hidden within an innocent-looking file using ADS. For example, an image file (`image.jpg`) could have a hidden data stream containing malicious code (`image.jpg:malicious.exe`).
  * **Execution without detection**: when the image file is opened, the operating system can execute the hidden payload without the user’s knowledge.

* Cybersecurity professionals use several tools and techniques to detect the presence of ADS:
  * **Windows Explorer**: ADS can be detected by appending a colon and a stream name to the file name. For example, `image.jpg:hidden.txt`
  * **CMD Prompt**: use the `dir /r` command to list ADS on a file.
  * **Forensic Tools**: **Encase**, **FTK Imager**, and **Autopsy** are powerful tools that can view and analyze ADS.
  * **Python Libraries**: libraries like **PyADS** and **pyntfs** allow for the manipulation and extraction of ADS data programmatically.

* Creating an alternate data stream is straightforward and can be done using the command line:

## Command

```bash
echo "hidden data" > file.txt:hidden.txt
```

* This command creates an alternate data stream named `hidden.txt` in the file `file.txt` with the content **hidden data**.
* Tools to Work with NTFS Streams:
  * **Echo and more**: basic command-line utilities.
  * **Sysinternals streams utility**: a powerful tool for working with ADS.
  * **Dir Command with /R option**: lists ADS associated with files.
  * **PowerShell 3.0**: includes six cmdlets for directly manipulating ADS content.

## How is ADS used to bypass filters?

* Alternate Data Streams (ADS) in NTFS file systems can be exploited by attackers to bypass security filters and hide malicious payloads.
* The following explains how this can happen in key points.

### Evading Antivirus detection

* Attackers can hide malicious code within an ADS of a legitimate file. Most antivirus programs scan the main data stream of files but may overlook data in ADS.
* For example, a malicious script  can be hidden within an image file’s ADS (`image.jpg:script.ps1`). When the image is scanned by antivirus software, it appears clean because the primary content of the image does not contain malicious code. The malicious script remains undetected in the ADS.

### Bypassing file type restrictions

* Some systems enforce file type restrictions by examining file extensions or content. By placing the malicious payload in an ADS, attackers can bypass these restrictions.
* For example, an attacker can be restricted from uploading `.exe` files but can upload image files. They upload an image (`photo.jpg`) with an ADS containing an executable (`photo.jpg:malware.exe`). The server sees only a harmless image file, while the actual payload is stored in the ADS.

### Circumventing content inspection

* Standard content inspection tools often look at the primary data stream. ADS can be used to store additional data that bypasses these inspections.
* For example, a malicious payload can be split into two parts. The main part is embedded within a text file, and the remaining part is stored in an ADS (`document.txt:hidden`). When the file is inspected, the primary content appears safe, but the hidden stream completes the malicious payload.

### Persistence mechanisms

* Attackers can store configuration files or scripts in ADS to maintain persistence on a compromised system.
* For example, a backdoor script can be hidden within the ADS of a system file (`system.dll:backdoor.ps1`). Security tools that check for unauthorized changes to system files may not detect the hidden ADS, allowing the attacker to maintain access to the system.

### Tools and Commands to work with ADS

#### Creating ADS

* **Command**: `echo "hidden data" > file.txt:hidden.txt`
* This creates an alternate data stream named `hidden.txt` in the file `file.txt`.

#### Listing ADS

* **CMD Prompt**: `dir /r`
* This command lists all files along with their ADS.

#### Viewing ADS

  ```powershell
  Get-Item -Path .\file.txt -Stream *
  ```

* This command lists all ADS associated with `file.txt`.

#### Deleting ADS

  ```powershell
  Remove-Item -Path .\file.txt -Stream hidden.txt
  ```

* This command deletes the ADS named `hidden.txt` in `file.txt`.
