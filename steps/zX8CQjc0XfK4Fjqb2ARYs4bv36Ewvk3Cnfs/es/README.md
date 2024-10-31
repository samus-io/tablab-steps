# Directivas de la cabecera Referrer-Policy

* La siguiente tabla define las diferentes directivas de la cabecera `Referrer-Policy`:
  |Directiva|Descripción|Resultado de la cabecera Referer|
  |:--:|:--:|:--:|
  |no-referrer|Cuando la cabecera `Referrer-Policy` tiene como directiva `no-referrer` esta evita que se envíe la cabecera `Referer`, previniendo toda fuga de información sensible.|No se envía cabecera `Referer`.|
  |no-referrer-when-downgrade|Esta directiva evita que no se emita la cabecera `Referer` a orígenes sin HTTPS. Esta cabecera no es muy recomendable, ya que no previene que se envíe información sensible a orígenes HTTPS.|`https://domain.tbl/user?name=User`|
  |origin|Con esta directiva la cabecera `Referer` solo contiene el origen desde la cual se origina la petición.|`https://domain.tbl/user/`|
  |origin-when-cross-origin|Esta directiva también es útil para evitar la filtración de información, ya que únicamente envía el origen cuando la petición se realiza a otro origen. En caso que la petición este destinada al mismo origen, se enviará toda la cabecera `Referer`. |`https://domain.tbl`|
  |same-origin|La directiva `same-origin` solamente se envía la cabecera `Referer` en las peticiones del mismo origen, es parecida a la directiva anterior pero con la diferencia que solo envía el origen en caso que la petición se realize al mismo origen.|No se envía cabecera `Referer`.|
  |strict-origin|Cuando se implementa esta directiva únicamente se envía el origen en la cabecera `Referer` en caso de que el protocolo de seguridad sea el mismo (`HTTP` a `HTTP` o `HTTPS` a `HTTPS`), de otra forma no se envía la cabecera. La directiva `strict-origin` es parecida a la directiva `same-origin` pero a diferencia de esta, es necesario que el protocolo de seguridad sea el mismo.|`https://domain.tbl`|
  |strict-origin-when-cross-origin|La directiva `strict-origin-when-cross-origin` solo envía el origen a peticiones hacia otros orígenes siempre y cuando el protocolo de seguridad sea el mismo (`HTTP` a `HTTP` o `HTTPS` a `HTTPS`). Esta directiva es parecida a `origin-when-cross-origin` pero con la diferencia que el protocolo de seguridad tiene que ser el mismo.|`https://domain.tbl`|
  |unsafe-url|Por último, `unsafe-url` es la directiva por defecto cuando no se define la cabecera `Referrer-Policy`, esta directiva adjunta a la cabecera `Referer` el origen, la ruta y los parámetros. Es importante no utilizar esta directiva ya que es considerada insegura.|`https://domain.tbl/user?name=User`|
  
## Recomendaciones de la cabecera Referrer Policy

* Hay que tener en cuenta que servicios de análisis web, como Google Analytics, utilizan la cabecera `Referrer` para recopilar información sobre que página fué desde la que accedió el usuario. Según la política que apliquemos, podría afectar a la recopilación de esta información.
* En el caso que se utilice un servició de análisis de datos, es recomendable utilizar las directivas `same-origin`, `origin-when-cross-origin` o `strict-origin-when-cross-origin`, para evitar errores en su funcionamiento.
* En caso que no se utilice ningún servicio de análisis web, las directivas mas recomendables son `strict-origin` `origin` y `no-referrer`.
