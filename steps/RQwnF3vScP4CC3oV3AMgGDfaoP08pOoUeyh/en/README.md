# File type validation using frameworks in Node.js

## Images

* Malicious content can be embedded in images, such as scripts in metadata.
* To mitigate this, image rewriting techniques can be used to strip out any potentially harmful content. This often involves re-encoding the image, which removes any embedded malicious data.

### Randomization by adding noise to images

* To enhance security, you can introduce random noise into images. This can make some attacks less predictable and harder to execute. Below is a breakdown of how this can be achieved.

#### Introduce random noise

* Loop over all the pixels in the image.
* For each pixel, consider the three RGB intensity values.
* Randomly choose to either:
  * Add 1 to the intensity value.
  * Subtract 1 from the intensity value.
  * Leave the intensity value unchanged.

#### Minimal visual impact

* The introduced noise is minor and should not be noticeable to viewers.
* The slight alteration helps in maintaining the image quality while adding a layer of unpredictability.

#### Potential security benefits

* This heuristic approach can make it harder for attackers to predict the exact outcome of the transformation.
* It can complement other security measures, adding an extra layer of defense.

#### Heuristic nature

* This method is not guaranteed to be effective on its own.
* It should be used in conjunction with other security strategies as part of a defense-in-depth approach.

## Microsoft Documents

* For Microsoft documents, libraries like **mammoth**, **docx**, **officegen** can be used to validate the content. They provide APIs to manipulate various file formats based on Office Open XML standards.
* These libraries help us to read and parse the content of microscoft documents.

## ZIP Files

* ZIP files are not recommended for upload as they can contain multiple file types, increasing the complexity of validation and the risk of various attack vectors like zip bombs, malicious executables, etc.
* Only allow specific, safe file types within ZIP archives.
* Set maximum size limits for both the ZIP file itself and the individual files it contains.

## PDF Files

* These are the common type of files that are circulated over the internet. To be safe against these files, check for and enforce security features like disabling JavaScript execution within the PDF and verifying digital signatures if applicable.

## Library for validating images in Nodejs

* Here, we will use **sharp** library. **sharp** is a high-performance image processing library in Node.js. Here's how you can use it to remove metadata from an image:

* Start by installing the other required libraries along with **sharp**.

```javascript
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
```

* Read the image in **inputPath**, filter it and add it to **outputPath**. Here, we are removing the metadata of the file

```javascript
const inputPath = path.join(__dirname, 'input.jpg');
const outputPath = path.join(__dirname, 'output.jpg');

fs.readFile(inputPath, (err, data) => {
  if (err) throw err;

  // Process the image with sharp
  sharp(data)
    .withMetadata({ remove: true }) // Remove metadata
    .toFile(outputPath, (err, info) => {
      if (err) throw err;
      console.log('Image processed and metadata removed:', info);
    });
});

```

* It can also be used to perform randomization. Create a function to add random noise to the image.

```javascript
async function addRandomNoise(inputPath, outputPath) {
  const { data, info } = await sharp(inputPath).raw().toBuffer({ resolveWithObject: true });
  const noisyData = data.map((value, index) => {
    const randomChange = Math.floor(Math.random() * 3) - 1; // -1, 0, or +1
    return Math.min(255, Math.max(0, value + randomChange)); // Ensure value stays within 0-255
  });

  await sharp(noisyData, { raw: { width: info.width, height: info.height, channels: info.channels } })
    .toFile(outputPath);
}
```

* Add the random noise to the file in the **inputPath**. If it fails then the file is vulnerable.

```javascript
const inputPath = path.join(__dirname, 'input.jpg');
const outputPath = path.join(__dirname, 'output.jpg');

// Process the image
addRandomNoise(inputPath, outputPath)
  .then(() => console.log('Image processed with random noise added.'))
  .catch(err => console.error('Error processing image:', err));
```

## Library for validating Microscoft document in Nodejs

* Install the below initialized libraries and specially the **mammoth** library.

```javascript
const express = require('express');
const multer = require('multer');
const mammoth = require('mammoth');
const fs = require('fs');
const path = require('path');
const uuid = require('uuid');

const app = express();
const port = 3000;

// Set up Multer storage configuration
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, '<desired location>'); 
  },
  filename: (req, file, cb) => {
    const fileName = `${uuid.v4()}`; // Naming the file using UUID V4 only
    cb(null, fileName);
  }
});

const upload = multer({ storage: storage });
```

* Create a function to validate the content of a `.docx` file.

```javascript
async function validateDocxContent(filePath) {
  try {
    const result = await mammoth.extractRawText({ path: filePath });
    const text = result.value; // Extracted plain text from the .docx file

    // Perform your validation logic here
    // Example: Check if the document contains the word "example"
    if (text.includes('example')) {
      return { isValid: true };
    } else {
      return { isValid: false, message: 'The document does not contain the required word: example' };
    }
  } catch (error) {
    throw new Error(`Failed to extract text from the document: ${error.message}`);
  }
}
```

* Call the **validateDocxContent** function. If it is valid then store it.

```javascript
  validateDocxContent(filePath)
    .then((validationResult) => {
      if (validationResult.isValid) {
        // Store the file
        upload.single('file')
      } else {
        // Reject the request
      }
    })
    .catch((error) => {
      // Reject the request
    });

```

## Library for validating ZIP files in nodejs

* For ZIP file validation in Node.js, you can use the `adm-zip` library to extract the contents of the ZIP file and perform validation based on the extracted files.

* Initialize the dependences.

```javascript
const AdmZip = require("adm-zip");
const fs = require("fs");
```

* Create a function to validate the ZIP file.

```javascript
function validateZipFile(filePath) {
    return new Promise((resolve, reject) => {
        const zip = new AdmZip(filePath);
        const zipEntries = zip.getEntries();
        
        // Validate each entry in the ZIP file
        zipEntries.forEach((zipEntry) => {
            // Perform validation logic for each entry (e.g., check file types, sizes, etc.)
            if (!zipEntry.isDirectory) {
                if (!isValidFileType(zipEntry.entryName)) {
                    reject(new Error(`Invalid file type: ${zipEntry.entryName}`));
                    return;
                }
                if (zipEntry.entryName.length > 100) { // Example: Check file name length
                    reject(new Error(`File name too long: ${zipEntry.entryName}`));
                    return;
                }
                // Additional validation checks...
            }
        });
        
        resolve("Validation successful");
    });
}

// Example function to check if a file type is valid
function isValidFileType(fileName) {
    // Implement your own logic to validate file types
    // For example, check file extensions or MIME types
    return fileName.endsWith(".txt") || fileName.endsWith(".jpg");
}
```

* Test the logic you implemented for ZIP file validation. If it valid then you handle the storing of this file.

```javascript
// Example usage
const filePath = "path/to/your/archive.zip";

validateZipFile(filePath)
    .then((output) => {
        console.log(output);
        //Store the file (e.g. using multer here)
    })
    .catch((error) => {
        console.error("Validation failed:", error);
    });

```

## Library for validating PDF files in nodejs

* For PDF file validation, you can use the `pdf-parse` library to extract text and other information from the PDF file and perform validation based on the extracted content.

* Initialize the dependences.

```javascript
const pdfParse = require("pdf-parse");
const fs = require("fs");
```

* Create a function to validate the PDF file.

```javascript
function validatePdfFile(filePath) {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, (err, data) => {
            if (err) {
                reject(err);
            } else {
                pdfParse(data).then((pdfData) => {
                    const text = pdfData.text;
                    // Perform validation logic based on extracted text
                    if (text.includes("some validation criteria")) {
                        resolve("Validation successful");
                    } else {
                        reject(new Error("Validation failed"));
                    }
                }).catch((error) => {
                    reject(error);
                });
            }
        });
    });
}
```

* Test the logic you implemented for PDF file validation. If it valid then you handle the storing of this file.

```javascript
// Example usage
const filePath = "path/to/your/document.pdf";

validatePdfFile(filePath)
    .then((output) => {
        console.log(output);
        //store the file (e.g. using multer here)
    })
    .catch((error) => {
        console.error("Validation failed:", error);
    });
```
