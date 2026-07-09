# Pagina web para odontologo

Sitio profesional, simple y responsive para un consultorio odontologico. Esta hecho con HTML, CSS y JavaScript puro para que sea rapido, facil de mantener y simple de subir a cualquier hosting.

## Estructura

```text
.
├── .gitignore
├── index.html
├── package.json
├── README.md
├── vercel.json
└── assets
    ├── css
    │   └── styles.css
    ├── img
    │   ├── consultorio-espera.jpg
    │   ├── consultorio-pasillo.jpg
    │   ├── consultorio-sillon.jpg
    │   ├── favicon.svg
    │   ├── logo-armendariz.png
    │   └── og-preview.svg
    └── js
        ├── app.js
        └── data.js
```

## Como ejecutarlo

No necesita instalacion. Podes abrir `index.html` directamente en el navegador.

Para verlo con un servidor local:

```bash
cd "/Users/thiago/Documents/Pagina Para Odontologo"
python3 -m http.server 5173
```

Despues entra a:

```text
http://localhost:5173
```

## Como subirlo a Vercel

Este proyecto ya esta preparado como sitio estatico. En Vercel no hace falta build.

Opcion recomendada:

1. Subir esta carpeta a un repositorio de GitHub.
2. Entrar a Vercel y elegir `Add New Project`.
3. Importar el repositorio.
4. Framework preset: `Other`.
5. Build command: dejar vacio.
6. Output directory: dejar vacio o usar `.` si Vercel lo pide.
7. Deploy.

Archivos agregados para Vercel:

- `vercel.json`: configuracion simple de sitio estatico.
- `package.json`: scripts locales de desarrollo y chequeo.
- `.gitignore`: evita subir archivos temporales.
- `assets/img/favicon.svg`: icono del sitio.

## Como modificar los datos

Edita el archivo `assets/js/data.js`. Ahi estan centralizados:

- Nombre del odontologo.
- Telefono.
- WhatsApp.
- Email.
- Direccion.
- Horarios.
- Medios de pago.
- Link de Google Maps.
- Servicios.
- Preguntas frecuentes.
- Redes sociales.
- Imagen principal y foto profesional.

Ejemplo importante:

```js
contact: {
  phone: "+542914238463",
  phoneDisplay: "291 423-8463",
  whatsapp: "542914238463",
  whatsappDisplay: "291 423-8463"
}
```

El campo `whatsapp` debe quedar solo con codigo de pais, codigo de area y numero, sin `+`, espacios ni guiones. Si el numero real de WhatsApp es celular argentino, probablemente haya que usar el formato `549...`.

## Como funciona WhatsApp

El formulario de turnos toma los datos del paciente y arma automaticamente un mensaje. Al enviar, abre:

```text
https://wa.me/NUMERO?text=MENSAJE
```

El numero sale de `contact.whatsapp` en `assets/js/data.js`.

## Preparado para base de datos

En `assets/js/app.js`, la funcion `sendAppointmentRequest()` centraliza el envio del turno. Hoy abre WhatsApp y guarda un borrador temporal en `sessionStorage`. Mas adelante se puede reemplazar o ampliar esa parte con:

- API propia.
- Base de datos.
- Panel para el odontologo.
- Estados de turno: pendiente, confirmado o cancelado.
- Notificaciones por email o WhatsApp.
- Integracion con Google Calendar.

## Datos que faltan antes de publicar

Antes de publicar la version final, conviene juntar:

- Confirmar si el WhatsApp es exactamente `542914238463` o si debe llevar `549`.
- Foto profesional, si despues quiere reemplazar el logo en la seccion del profesional.
- Confirmar si quiere mantener solo Instagram o agregar otra red.
- Link exacto del pin de Google Maps, si existe uno mejor que la busqueda por direccion.
