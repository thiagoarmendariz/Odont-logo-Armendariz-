# Página web para odontólogo

Sitio profesional, simple y responsive para un consultorio odontológico. Está hecho con HTML, CSS y JavaScript puro para que sea rápido, fácil de mantener y simple de subir a cualquier hosting.

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

## Cómo ejecutarlo

No necesita instalación. Podés abrir `index.html` directamente en el navegador.

Para verlo con un servidor local:

```bash
cd "/Users/thiago/Documents/Pagina Para Odontologo"
python3 -m http.server 5173
```

Después entrá a:

```text
http://localhost:5173
```

## Cómo subirlo a Vercel

Este proyecto ya está preparado como sitio estático. En Vercel no hace falta build.

Opción recomendada:

1. Subir esta carpeta a un repositorio de GitHub.
2. Entrar a Vercel y elegir `Add New Project`.
3. Importar el repositorio.
4. Framework preset: `Other`.
5. Build command: dejar vacío.
6. Output directory: dejar vacío o usar `.` si Vercel lo pide.
7. Deploy.

Archivos agregados para Vercel:

- `vercel.json`: configuración simple de sitio estático.
- `package.json`: scripts locales de desarrollo y chequeo.
- `.gitignore`: evita subir archivos temporales.
- `assets/img/favicon.svg`: ícono del sitio.

## Cómo modificar los datos

Editá el archivo `assets/js/data.js`. Ahí están centralizados:

- Nombre del odontólogo.
- Teléfono.
- WhatsApp.
- Email.
- Dirección.
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

El campo `whatsapp` debe quedar solo con código de país, código de área y número, sin `+`, espacios ni guiones. Si el número real de WhatsApp es celular argentino, probablemente haya que usar el formato `549...`.

## Cómo funciona WhatsApp

El formulario de turnos toma los datos del paciente y arma automáticamente un mensaje. Al enviar, abre:

```text
https://wa.me/NUMERO?text=MENSAJE
```

El número sale de `contact.whatsapp` en `assets/js/data.js`.

## Preparado para base de datos

En `assets/js/app.js`, la función `sendAppointmentRequest()` centraliza el envío del turno. Hoy abre WhatsApp y guarda un borrador temporal en `sessionStorage`. Más adelante se puede reemplazar o ampliar esa parte con:

- API propia.
- Base de datos.
- Panel para el odontólogo.
- Estados de turno: pendiente, confirmado o cancelado.
- Notificaciones por email o WhatsApp.
- Integración con Google Calendar.

## Datos que faltan antes de publicar

Antes de publicar la versión final, conviene juntar:

- Confirmar si el WhatsApp es exactamente `542914238463` o si debe llevar `549`.
- Foto profesional, si después quiere reemplazar el logo en la sección del profesional.
- Confirmar si quiere mantener solo Instagram o agregar otra red.
- Link exacto del pin de Google Maps, si existe uno mejor que la búsqueda por dirección.
