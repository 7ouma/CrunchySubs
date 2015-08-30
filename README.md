# CrunchySubs
CrunchySubs es un script hecho en python que permite descargar subtítulos de Crunchyroll de forma premium y free.

Basado en CrunchySubs 1.3.3. CrunchySubs 1.4 (Nombre temporal) está re-escrito para mejorar la eficiencia. 

Al descargar los subtítulos hay varias formas de hacerlo. La primera, al ingresar el enlace de Crunchyroll, el script por defecto te mostrará la lista de idiomas disponibles. Al escoger uno o todos se descargará. Sin embargo, la primera vez que se inicia el script, se creará un archivo de configuraciones llamado Config.json. En él se podrá poner un lenguaje especifico para evitar que Crunchyroll nos pregunte cada vez el lenguaje que queremos. También, podemos poner un * (asterisco) para que crunchyroll descargue todos los idiomas disponibles automaticamente. Por defecto viene en "none" donde que como se menciona más arriba el script preguntará cada vez que vayas a descargar.

Otra de las configuraciones es el directorio de descarga, si está en default descargará los subtitulos en la carpeta del script creando una carpeta adicional llamada "Subs". Si quieren agregar una ruta distinta deben de tener en cuenta que si están en windows, en vez de poner "c:\subtitulos" deberán escapar los caracteres y poner "c:\\\\subtitulos"

Algo que hay que tener en cuenta es que por el momento no se permiten rutas que contengan caracteres especiales como áéíóúÑñ por problemas de codificación.

Ahora, entrando en las opciones del programa al iniciar, la primera es directamente para bajar un subtitulo de un enlace deseado.

La segunda es para bajar un paquete de varios subtitulos contenidos en el archivo enlaces.txt (Por el momento esta opción está deshabilitada por lo que si la selecionan les dará error.)

La tercera es de login. Más nada que decir.

La cuarta aún está en desarrollo y no funciona del todo bien por problemas de codificación, por lo que si quieren editar las configuraciones haganlo directo en el archivo json (con notepad o algún otro editor de texto). Así se evitarán errores.

Todas esas fallas y funciones desabilitadas temporalmente irán siendo reparadas/habilitadas en el transcurso de los días.


Autor original de la función para desencriptar: Desconocido para mí, si alguien sabe, favor dejar un comentario en el blog, por acá o mediante un correo a 7ouman@gmail.com.

Autor del resto del script: Touman (Miguel A.).
Más información del script en http://crunchysubs.blogspot.com/


