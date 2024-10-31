# Best practices against Path Traversal

* The most effective strategy for preventing path traversal vulnerabilities is to avoid using user-entered data to access or include system files. There are several functions within applications that, although originally designed to operate under this scheme, can be modified to provide equivalent functionality in a secure manner.
* In situations where file inclusion based on user input is essential, it is critical to implement the following security measures.

## Normalize user input

* Before applying any security measures, it is important to ensure that the user input is in a consistent and secure encoding, such as `UTF-8`. This helps to mitigate risks associated with misinterpretation of characters.

## Implementing a whitelist

* Creating and maintaining a whitelist is an essential step. If the user's input does not match the items on this list, the request must be rejected immediately.
  * In cases where it is not feasible to create a whitelist, it is critical to ensure that the user's input contains only items that are explicitly allowed by the application. For example, restrict input to alphanumeric characters.

> :older_man: A whitelist is a set of items that are explicitly allowed for a particular operation or process.

## Restricting file extension control

* It is important to prevent users from determining the file extension. For example, if the application needs to load an image, the extension should be added automatically by code.
  * In situations where the inclusion of multiple extensions is essential, it is necessary to compare the file extensions provided by the user with a list of allowed extensions (png, pdf, etc.).

## Path validation and normalization

* After validating the user input, it is crucial to define the base directory containing the files to be accessed or sent to the client. Then you need to normalize the path to verify where it points to.
  * Most programming languages provide a native function called `normalize()` that makes it easy to obtain the absolute path to the desired file. This function is essential for removing relative references such as `../`, so you can confirm that the resulting path starts with the base directory set for the files.
  