# Input validation en Node.js

* `VineJS` es una librería de validación de datos de formularios para Node.js. Se puede utilitzar para validar el cuerpo de una petición HTTP en aplicaciones de backend:
  ```javascript
  import vine from '@vinejs/vine'

  const schema = vine.object({
    sku: vine.string(),
    price: vine.number().positive(),
    variants: vine.array(
      vine.object({
        name: vine.string(),
        type: vine.enum(['size', 'color']),
        value: vine.string(),
      })
    )
  })

  const data = getDataToValidate()
  await vine.validate({ schema, data })
  ```
* :writing_hand: El siguiente código debe ser actualizado aplicando técnicas de Input Validation utilizando la librería VineJS para protegerlo de Inyecciones SQL:
  @@ExerciseBox@@