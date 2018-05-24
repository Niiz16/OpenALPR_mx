# Train-OCR
# Entrenamiento OCR
Todo lo siguiente fue tomado de [GitHub].

El entramiento de **OpenALPR OCR** es una manera rápida de mejorar la precisión para un país en particular. 
> Para hacer esto es necesario:
    1. Alrededor de 200 imágenes claras de las placas del país
    2. 16 horas de tiempo libre
  
**[OpenALPR]** usa la librería de *Tesseract OCR*. Muchos de los aspectos tediosos del entrenamiento de OCR han sido automatizados por medio de un script de Python. Como sea, la entrada de datos necesita un formato específico para satisfacer a Tesseract.
  
  Para obtener más información acerca del entranamiento usando Tesseract OCR, puede leer el siguiente **[Tutorial]**.
### Pasos 
1. Clonamos el repositorio [GitHub]
    En el folder de "eu/input" hay archivos tif y box. 
    Para cada fuente debemos tener al menos un archivo tif y un archivo box
    Para las placas de un país podemos tener muchas fuentes y cada una debe tener diferente nombre.

    >La convención es l[country_code].[fontname].exp[pagenumber].box
    
   > Por ejemplo:
      Para la fuente de las placas de alemanas (europa) deberá verse de la siguiente forma:
      leu.germany.exp0.box
    
    ### TIF
 En este archivo hay muchas letras y números similares. La mejor forma de generar esto es de imágenes de las placas actuales.

[OpenALPR] tiene algunas herramientas para generar estos archivos de entrada.
        
    1. Encontrar muchas imágenes de las placas
    2. Separarlas por fuente
    3. Dentro de una misma región, algunas veces las fuentes de las placas pueden variar (Ejemplo: nuevas y viejas, Placas digitales o estampadas, vehículos y bicicletas)
                  Cada fuente única debe estar en un archivo diferente para alcanzar una mayor precisión

2. Añadiendo un nuevo País
    Para entrenar OCR por un país completamente nuevo, necesitaremos configurar las dimensiones de la placa y los carácteres.
        
    *  Añadir un nuevo archivo en runtime_data/config/ con su código de país de 2 dígitos. Puedes copiar y pegar una sección de otro país. 
        >La ruta usualmente es: /usr/share/openalpr/runtime_data/config

     Necesitaremos modificar los siguientes valores
            
            plate_width_mm = [width of full plate in mm]
                             "Ancho de toda la placa en mm"

            plate_height_mm = [height of full plate in mm]
                              "Alto de toda la placa en mm"

            char_width_mm = [width of a single character in mm]
                            "Ancho de un único caracter en mm"

            char_height_mm = [height of a single character in mm]
                             "Altura de un único caracter en mm"

            char_whitespace_top_mm = [whitespace between the character and the top of the plate in mm]
                                     "Espacios en blanco entre cada caracter y la parte superior de la placa en mm"

            char_whitespace_bot_mm = [whitespace between the character and the bottom of the plate in mm]
                                     "Espacios en blanco entre caracter y la parte inferior de la placa en mm"

            template_max_width_px = [maximum width of the plate before processing. Should be proportional to the plate dimensions]
                                    "Ancho máximo de la placa antes del procesamiento. Debe ser proporcional a las dimensiones de la placa, px"

            template_max_height_px = [maximum height of the plate before processing. Should be proportional to the plate dimensions]
                                     "Altura máxima de la placa antes del procesamiento. Debe ser proporcional a las dimensiones de la placa, px"

            min_plate_size_width_px = [Minimum size of a plate region to consider it valid.]
                                      "Tamaño mínimo de la placa de una región para considerarla válida, Ancho"

            min_plate_size_height_px = [Minimum size of a plate region to consider it valid.]
                                       "Tamaño mínimo de la placa de una región para considerarla válida, Alto"

            ocr_language = [name of the OCR language -- typically just the letter l followed by your country code]
                           "Nombre del lenguanje del OCR, tipícamente la letra "l" seguida del código del país"

 	  **Para obtener esta información se utilizó la [Norma]:**
              NORMA Oficial Mexicana NOM-001-SCT-2-2016, Placas metálicas, calcomanías de identificación y tarjetas de circulación empleadas en automóviles, tractocamiones, autobuses, camiones, motocicletas, remolques, semirremolques, convertidores y grúas, matriculados en la República Mexicana

3. Entendiendo las placas de tu País
    La primera cosa que necesitas saber es cuántas fuentes de placas tiene tu país. En EU, por ejemplo, muchos estados usan muchas fuentes diferentes para sus placas. Algunos países sólo usan una fuente. 
    Cada fuente necesita ser entrenada separadamente. Usted no quiere combinar los carácteres de las fuentes, esto decrementará su precisión. Después de que cada fuente es entrenada, pueden ser combinadas dentro de un "dataset" (conjunto de datos) para su país entero.

4. Creando los moldes de carácteres
    Cuando estés listo para empezar el entramiento, necesitaremos crear una librería de moldes de los carácteres. Cada molde es un archivo de imagen pequeña que contiene el "black-and-white" (el negro y blanco) del caracter y es nombrado después.
    Necesitaremos varios de estos moldes por cada caracter y fuente. Los moldes de caracteres serán ligeramente diferentes, esto es necesario para que el entramiento de OCR pueda entender como detectar los carácteres.
    
5. Produciendo los moldes
    Hay dos formas de producir los moldes de carácteres
    **En México no se utilizan las letras I-Ñ-O-Q** 
      
      1. Usando imágenes actuales de las placas (Hay que tener en cuenta que las imágenes deben de ser de fondo claro y carácteres negros, porque tiene problemas al reconocerlas, así que se pueden someter a un tratamiento para invertir colores).   
      2. Usando una fuente TTF que luzca como la fuente de las placas.
         **Esta opción ya no está soportada en la versión más reciente de openalpr-utils (2.2.4-1build1)

### Produciendo moldes de placas actuales
Debemos recolectar una librería grande de imágenes de placas (al menos 100), asegurándonos que cada imagen tenga al menos 250px.
La relación de aspecto debe coincidir con la configuración de ancho/alto para las placas, y estas imágenes deberán estar recortadas alrededor de las placas.
 (El programa [Imageclipper], Repositorio separado es de ayuda para recortar un número grande de imágenes). Guarda las imágenes en formato png.
Cada archivo deberá ser nombrado con un identificador de 2carácteres por cada fuente/región. Por ejemplo, para las placas de Maryland, deberíamos nombrar el archivo: mdplate1.png  
        
**Crear un directorio vacío de salida**.
        
Para empezar a clasificar los carácteres, usamos la herramienta de **"classifychars"** que viene incluida en la instalación de [OpenALPR]
>Executando el comando.
    El archivo fuente está normalmente localizado en: 
```sh
    /usr/local/src/openalpr/tesseract-ocr/classify):
    openalpr-utils.classifychars 
```
**Comando:**
```
    $ openalpr-utils-classifychars [country(país)] [indirectory(directorio dónde están las imágenes)] [outdirectory(directorio de salida, dónde se guardarán las imágenes)]
``` 
**Ejemplo:**
```sh                
    $ openalpr-utils-classifychars eu ./pics/ ./out
```
Una GUI se abrirá y analizará cada imagen de las placas en su directorio de entrada. 
Para clasificar las placas debemos seguir los siguientes pasos:

1. Presionar "Espacio" para seleccionar una imagen del tablero, se pondrá en azul si es seleccionada. 
Para cada placa, hay buenos carácteres y malos carácteres. Querrá escoger los mejores carácteres, ya que las imperfecciones puede confundir el OCR.
2. Presionar "Enter"(intro) y escribir las letras o números de cada posición del selector de caracter. Si presionamos espacio, saltará ese caracter. 
**Si es el último caracter, no lo salta, yo recomiendo guardarlo con alguna letra en especifico para después poderlos eliminar o presionar escape. 
3. Presionar "s" para guardar cada caracter como un archivo separado en el directorio de salida.
4. Presionar "Espacio" para seleccionar otra imagen del tablero. 
5. Repetir los pasos hasta que se haya terminado, y presionar "n" para moverse a la siguiente placa y repetir los pasos para clasificar.
         
### Produciendo moldes desde un TTF Font (fuente TTF)
****Esta opción ya no me aparece soportada en la versión que tengo de openalpr-utils (2.2.4-1build1)**
        Necesitaremos agregar algunas distorsiones realistas para los carácteres. Esto es necesario para hacer robusto el detector OCR.
           
1. Conocer todos los carácteres que conforman las placas del país
2. Crear un documento de word con todos los carácteres. Asegurarse que hay un espaciado entre cada línea y caracter.
3. Copiar y pegar todos los carácteres a un archivo text, sin dejar espacios o saltos de línea.
4. Imprimir el documento de Word.  
5. Tomar algunas fotos (5 serán suficientes) del documento de Word con una cámara digital. Variando el ángulo/rotación ligeramente (de uno a dos grados) entre cada foto.
6. Guardar las fotos en un directorio (folder)
7. Correr el programa openalpr-utils-binarizefontsheet para producir los moldes de cada imagen. 
Proporcione al programa el archivo de texto del paso 3, así como cada archivo de imagen.
          
    ** Cuando tiene menos números de lo normal, a veces mete espacios a capturar
 ** El programa se cierra solo 
 ** Recomiendo revisar la carpeta de los moldes resultantes para ver si no hubo errores en las capturas
          

6. Construyendo una hoja de entrenamiento de Tesseract
     Una vez que haz clasificado todos los caracteres, puede ser una buena idea escanear el directorio para asegurarse de que las clasificaciones coincidan con las imágenes.
El nombre de cada imagen debe de llevar al inicio el caracter que representa. Después de esto, necesitarás crear una hoja de entrenamiento.
Hay una herramienta en OpenALPR "openalpr-utils-prepcharsfortraining" que creará la hoja de entramiento de Tesseract por ti. Ejecutamos el siguiente comando:
       openalpr-utils-prepcharsfortraining [Directorio de salida de los moldes]
     
     La salida tendremos:
       `combined.box`
       `combined.tif`
     
     Renombrar estos archivos ("`leu.germany.expo0.box`") para que coincida con el nombre que usa Tesseract

7. Terminando de entrenar OCR
     Por último, usaremos los archivos box/tif creados anteriormente para entrenar OCR con las placas del país. 
     Crea un nuevo directorio usando el codigo de país, después crea un directorio de entrada "(input)" dentro del directorio anterior. 
     Copie todos los archivos box/tif creados en los pasos anteriores dentro de este directorio.

     Ejecutamos el archivo `train.py`  Escriba su código de país. (Se tiene que cambiar el path de donde se encuentran ubicados algunos archivos)

     Path correcto en mi caso `train.py` me di una idea en el este [issue] de Github. 
     ```sh
         $ DIR = /usr/local/share/tessdata
         $ BIN = /usr/local/bin/tesseract
         $ TRAINDIR = /usr/local/bin
     ```

     Si todo sale bien, debe tener un nuevo archivo llamado l[código_del_país].traineddata. 
       Copie este archivo dentro de runtime_directory (runtime_data/ocr/tessdata/) y estará listo para usar con OpenALPR.

     Tesseract puede reportar problemas, lo más común es que se quejará de que no puede alinear los cuadros en la imagen proporcionada.
       Si recibes muchos warnings (advertencias), vuelve a correr la herramienta de openalpr-utils-prepcharsfortraining y agregue valores para -tile_width y -tile_height. Usando diferentes valores cambiará como Tesseract ve la imagen y esto pontenciará la mejora de resultados.




  [issue]: <https://github.com/openalpr/train-ocr/issues/21>
  [Norma]: <http://dof.gob.mx/nota_to_doc.php?codnota=5442476>
  [GitHub]: <https://github.com/openalpr/train-ocr>
  [Documentación]: <http://doc.openalpr.com/opensource.html#pattern-matching>
  [Imageclipper]: <https://github.com/openalpr/imageclipper>
  [OpenAlpr]: <https://github.com/openalpr>
  [Tutorial]: <https://code.google.com/p/tesseract-ocr/wiki/TrainingTesseract3>