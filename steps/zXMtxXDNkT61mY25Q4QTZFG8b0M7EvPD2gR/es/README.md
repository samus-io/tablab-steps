# Prácticas recomendadas contra el Path Traversal

* La estrategia más eficaz para prevenir vulnerabilidades de Path Traversal consiste en evitar la utilización de datos introducidos por el usuario para el acceso o inclusión de archivos del sistema. Existen diversas funciones dentro de las aplicaciones que, aunque inicialmente diseñadas para operar bajo este esquema, pueden ser modificadas para ofrecer funcionalidades equivalentes de manera segura.
* En situaciones donde la inclusión de archivos basada en la entrada del usuario resulte imprescindible, es crucial implementar las siguientes medidas de seguridad.

## Normalización del input del usuario

* Antes de aplicar cualquier medida de seguridad, es primordial asegurar que la entrada proporcionada por el usuario se encuentre en una codificación uniforme y segura. Esto ayuda a mitigar riesgos asociados con la interpretación errónea de los caracteres.

## Implementación de una lista de valores permitidos (whitelist)

* Crear y mantener una whitelist es un paso esencial. Si la entrada proporcionada por el usuario no coincide con los elementos de esta lista, la petición debe ser rechazada de inmediato.
  * En casos donde la creación de una lista de valores permitidos no sea viable, es crucial asegurar que la entrada del usuario contenga únicamente elementos que sean explícitamente permitidos por la aplicación. Por ejemplo, restringir la entrada a caracteres alfanuméricos.

> :older_man: Una lista de valores permitidos, o whitelist, es un conjunto de elementos autorizados expresamente para cierta operación o proceso.

## Restricción sobre el control de la extensión de archivo

* Es fundamental evitar que los usuarios determinen la extensión de los archivos. Por ejemplo, si la aplicación necesita cargar una imagen, la extensión del archivo debería ser añadida automáticamente mediante código.
  * En situaciones donde la inclusión de múltiples extensiones sea indispensable, es necesario comparar las extensiones de archivos proporcionadas por el usuario con una lista de extensiones permitidas (png, pdf, etc.).

## Validación y normalización de la ruta de acceso

* Tras la validación del input del usuario, es crucial definir el directorio base que contiene los archivos destinados a ser accedidos o enviados al cliente. Posteriormente, se debe proceder con la normalización de la ruta de acceso para verificar hacia dónde apunta.
  * La mayoría de los lenguajes de programación ofrecen una función nativa denominada `normalize()`, la cual facilita la obtención de la ruta absoluta al archivo deseado. Esta función es esencial para eliminar referencias relativas como `../`, permitiendo así confirmar que la ruta resultante inicie con el directorio base establecido para los archivos.
