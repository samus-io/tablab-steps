# Input validation in Node.js

* `VineJS` is a form data validation library for Node.js. You may use it to validate the HTTP request body in your backend applications:
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
* :writing_hand: Update the following code by appliying Input Validation techniques using the VineJS library to protect from SQL Injections:
  @@ExerciseBox@@