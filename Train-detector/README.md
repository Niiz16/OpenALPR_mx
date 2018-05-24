# Entrenamiento del Detector 
Todo lo siguiente fue tomado de [GitHub].

 El detector encontrará la localización de la imagen de una placa. Un detector puede soportar diferentes estilos de placas, mientras tengan la misma relación de aspecto.
  Por ejemplo, en EU, las placas son de 12 pies por 6 pies (una relación de 2:1).

  Para entrenar el detector de placas, necesitarás
     
    1. 3000+ imágenes claras de placas
    2. 40-60 horas de tiempo libre
  
  El siguiente repositorio contiene scripts que te ayudarán a entrenar el detector de placas para una región en particular.
  El detector de región entrenado puede ser usado en OpenALPR.

  El detector de región de placas usa el **algoritmo Local Binary Pattern (LBP)**, "Patrón binario local". Para entrenar el detector, necesitarás muchas imágenes positivas/negativas. 
  Este repositorio ya contiene una colección de imágenes negativas; necesitarás agregar tus propias imágenes positivas.

  Para empezar, necesitarás muchas imágenes de placas recortadas que contengan coincidencias positivas de placas. 
  Vea el directorio de imágenes positivas de "eu" que está en el repositorio para entender los tipos de imágenes requeridas. El programa de [imageclipper] será de ayuda para crear estas imágenes recortadas. Este se menciona en la [Documentación].
  
  En el repositorio de [Github] de OpenALPR  se menciona la herramienta  [Plate Tagger Utility] en vez de [imageclipper].
         La herramienta Plate Tagger es usada para anotar las locacion y números de las imágenes de las placas. Las anotaciones pueden ser usadas para entrenar el algoritmo de OpenALPR para la precisión del reconocimiento de las placas.
  
  
  Después de haber colectado muchas (cientos a miles) de imágenes positivas, el siguiente paso es entrenar el detector. 
  Primero tienes que configurar el script de entrenamiento para usar las dimensiones correctas. 
  
  Editamos el script ```prep.py``` y cambia las variables WIDTH (ancho), HEIGHT (alto) y COUNTRY (país) para hacer que coincida con el país con el que hiciste entrenamiento. 
  El ancho y el alto debe ser proporcional al tamaño de la placa (ligeramente mayor está bien). Una área de pixeles total alrededor de 650 parece trabajar mejor.
  También, ajustar el patrón si es necesario de las librerías OpenCV.

  Cuando estés listo para empezar el entrenamiento, ingrese los siguientes comandos:
``` sh
    $ rm ./out/* (Borrar el directorio "out" en caso de que contenga datos de ejecuciones anteriores
    $ ./prep.py neg
    $ ./prep.py pos
    $ ./prep.py train
      Copie la salida proveniente del comando anterior a la línea de comando. Ajuste "numStages" a un valor más pequeño (usualmente 12 etapas trabaja bien, pero dependerá de su entrada de imágenes). 
      También puede necesitar ajustar el valor de "numPos" a un número pequeño para completar el entrenamiento.
```
 Copie el archivo "`out/cascade.xml`" en el directorio `runtime` de su OpenALPR
   (`runtime_data/region/[countrycode].xml`). Debe estar ahora disponible el uso de detección de placas por región.

# Observaciones
Las **imágenes negativas**, solo son imagenes en "raw" que no tienen nada que ver con placas
Tarda un poco en clonar el repositorio

Hay que poner la dirección de OPENCV en el archivo de python
```sh
'BASE_DIR' = nombre del directorio donde estás trabajando
'raw-neg' = directorio de entrada de imágenes negativas
'country' = directorio de entrada de imágenes positivas de las placas
'negative' = directorio de salida de imágenes negativas
'positive' = directiorio de salida de imágenes positivas
'WIDTH', HEIGHT estan en cm
```
Para encontrar las direcciones usé el comando find en ubuntu

# numPos y numStages
Puse numPos = 300 y numStages = 6, pero depende del número de placas positivas que tengas.
De salida genera 2 archivos `.txt` y un `vecfile.vec`

Hay que tener en cuenta que el archivo `.conf` de nuestro país, el archivo `xml` que generamos es el que se especifica en el detector_file, como se muestra a continuación:   
```sh
ocr_language = lmx
detector_file = mx.xml
```
La ruta del archivo `.conf` normalmente es la siguiente `/usr/share/openalpr/runtime_data/config`


[GitHub]: <https://github.com/openalpr/train-detector>
[Documentación]: <http://doc.openalpr.com/opensource.html#training-the-detector>
[Plate Tagger Utility]: <https://github.com/openalpr/plate_tagger>
[imageclipper]: <https://github.com/openalpr/imageclipper>
