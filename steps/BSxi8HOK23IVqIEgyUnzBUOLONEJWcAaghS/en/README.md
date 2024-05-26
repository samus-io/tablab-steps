# Finding Insecure File Upload

## Challenges of securing file upload(common bypassing methods)

* The below topics, explain the challenges in securing file upload with some common bypassing methods for each challenge.

### Double Extension

* Attackers use double extensions to trick file validation systems. For example, a file named `image.jpg.php` might pass validation if the system only checks for `.jpg` extensions.
* There are various bypassing methods that belong to this category:
  * **Double Extensions:** use multiple or uppercase extensions to bypass simple checks. `file.png.php`, `file.png.Php5` are the examples that can bypass.
  * **Valid Before Execution:** add a safe extension before a dangerous one. For example, `file.png.php`.
  * **Special Characters:** inject special characters to confuse the server.  For example, `file.php%20`, `file.php/` and etc.
  * **Parser Tricks:** use null bytes or extra extensions to trick the file parser. For example,`file.php\x00.png`, `file.phpJunk123png`.
  * **Layered Extensions:** combine multiple extensions to bypass filters. For example, `file.png.jpg.php`.
  * **Misconfigured Parsing:** place the executable extension first.
  * **NTFS ADS:** use Windows-specific features to hide malicious content. For example, `file.asax:.jpg`.
  * **Filename Limits:** use long filenames to truncate safe extensions. For example, Linux max length is typically 255 bytes, so create a name `abc...abc.php.png`, `abc...abc` in a long string.

#### Key Points to Mitigate Double extension challenge

* Validate filenames to ensure they don’t contain multiple extensions.
* Strip or normalize file extensions before processing.

### Bypass Content-Type

* Attackers can manipulate the `Content-Type` header in HTTP requests to bypass validation that relies on this header to determine the file type.
* Attackers modify the `Content-Type` header in the upload request to match a safe file type, even if the actual file is malicious. For example, content-type as `image/jpeg` for an executable script.

#### Key Points to Mitigate Content-type heaer bypass

* Use server-side checks to determine file types, such as verifying file content or magic numbers instead of trusting the Content-Type header.

### Magic Numbers

* Magic numbers are unique sequences of bytes at the beginning of a file used to verify its type. Attackers might manipulate these to bypass checks.
* Attackers prepend correct magic numbers to malicious files to make them appear legitimate. For example, `\xFF\xD8\xFF` (JPEG file) and a php file after ther magic number.

#### Key Points to Mitigate Magic Numbers challenge

* Implement checks for magic numbers, but also validate the entire file content.
* Combine magic number checks with file extension and MIME type validations.

### Path Traversal

* Path traversal involves manipulating file paths to access files outside the intended directory.
* Attackers include sequences like `../` in filenames to traverse directories and store files in unintended locations. For example, `../../../../var/www/html/malicious.php` makes the file to be stored in the web root, and can be accessed and executed via a URL.

#### Key Points to Mitigate Path Traversal challenge

* Sanitize and validate file paths.
* Use safe methods for file path handling, avoiding direct concatenation of user inputs.
* Store uploaded files outside the web root and reference them securely.

## What are the Alternate Data Streams (ADS)?

* **Alternate Data Streams (ADS)** are a feature of the NTFS file system that allows data to be stored in a file outside the main data stream. This means a single file can have multiple streams of data associated with it, which can be used for various purposes such as storing additional metadata (like author, title, or comments).
* For example, if the **Main File** is `document.txt`, then **ADS** is `document.txt:metadata` the ADS of it.

* The **New Technology File System (NTFS)** is a file system developed by **Microsoft** for **Windows operating systems**. NTFS provides several advanced features compared to older file systems like FAT32:
  * **Metadata Support**: NTFS supports rich metadata, allowing for enhanced file organization and search capabilities.
  * **Security**: it includes file-level security, permissions, and encryption.
  * **File Compression**: NTFS supports on-the-fly file compression.
  * **Large File and Volume Support**: it can handle very large files and volumes efficiently.
  * **Journaling**: NTFS uses a transaction log to help recover from errors quickly.

* Malware authors exploit ADS to hide their malicious payloads within legitimate files, making detection by antivirus software more challenging. Here's how it works:
  * **Hiding Payloads**: a malicious payload can be hidden within an innocent-looking file using ADS. For example, an image file (`image.jpg`) could have a hidden data stream containing malicious code (`image.jpg:malicious.exe`).
  * **Execution Without Detection**: when the image file is opened, the operating system can execute the hidden payload without the user’s knowledge.

* Cybersecurity professionals use several tools and techniques to detect the presence of ADS:
  * **Windows Explorer**: ADS can be detected by appending a colon and a stream name to the file name. For example, `image.jpg:hidden.txt`
  * **CMD Prompt**: use the `dir /r` command to list ADS on a file.
  * **Forensic Tools**: **Encase**, **FTK Imager**, and **Autopsy** are powerful tools that can view and analyze ADS.
  * **Python Libraries**: Libraries like **PyADS** and **pyntfs** allow for the manipulation and extraction of ADS data programmatically.

* Creating an alternate data stream is straightforward and can be done using the command line:

### Command

```bash
echo "hidden data" > file.txt:hidden.txt
```

* This command creates an alternate data stream named `hidden.txt` in the file `file.txt` with the content **hidden data**.
* Tools to Work with NTFS Streams :
  * **Echo and More**: basic command-line utilities.
  * **Sysinternals Streams Utility**: a powerful tool for working with ADS.
  * **Dir Command with /R Option**: lists ADS associated with files.
  * **PowerShell 3.0**: includes six cmdlets for directly manipulating ADS content.

## How is ADS used to bypass filters?

* Alternate Data Streams (ADS) in NTFS file systems can be exploited by attackers to bypass security filters and hide malicious payloads. Here’s how this can happen, explained in several key points:

### Evading Antivirus Detection

* Attackers can hide malicious code within an ADS of a legitimate file. Most antivirus programs scan the main data stream of files but may overlook data in ADS.
* For example, a malicious script  can be hidden within an image file’s ADS (`image.jpg:script.ps1`). When the image is scanned by antivirus software, it appears clean because the primary content of the image does not contain malicious code. The malicious script remains undetected in the ADS.

### Bypassing File Type Restrictions

* Some systems enforce file type restrictions by examining file extensions or content. By placing the malicious payload in an ADS, attackers can bypass these restrictions.
* For example, an attacker can be restricted from uploading `.exe` files but can upload image files. They upload an image (`photo.jpg`) with an ADS containing an executable (`photo.jpg:malware.exe`). The server sees only a harmless image file, while the actual payload is stored in the ADS.

### Circumventing Content Inspection

* Standard content inspection tools often look at the primary data stream. ADS can be used to store additional data that bypasses these inspections.
* For example, a malicious payload can be split into two parts. The main part is embedded within a text file, and the remaining part is stored in an ADS (`document.txt:hidden`). When the file is inspected, the primary content appears safe, but the hidden stream completes the malicious payload.

### Persistence Mechanisms

* Attackers can store configuration files or scripts in ADS to maintain persistence on a compromised system.
* For example, a backdoor script can be hidden within the ADS of a system file (`system.dll:backdoor.ps1`). Security tools that check for unauthorized changes to system files may not detect the hidden ADS, allowing the attacker to maintain access to the system.

### Tools and Commands to Work with ADS

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
