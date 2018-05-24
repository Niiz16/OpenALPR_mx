# OpenALPR_mx
Reconocimiento de placas de méxico con la librería de OpenALPR.

# OpenALPR
Es una librería open source de reconocimiento de placas automático, escrita con C++ con interconexiones(bindings) en C#, Java, Node.js, Go y Python. La librería analiza imágenes y transmisiones de vídeo para identificar las placas. La salida es la representación en texto de los caracteres de la placa.

Puedes leerlo directamente desde su GitHub [OpenALPR] (Está en inglés/ It's in English), para obtener más información. 

# Instalación
En mi caso, tuve que instalar el tesseract-3.05 que a su vez ocupa Leptonica 1.74 o mayor (Así que tambien hay que descargarlo).

Pueden checar la documentación de la instalación de OpenALPR en [GitHub].

### LEPTONICA
Descargar [Leptonica]
``` sh
    $ cd /usr/local/src/openalpr/leptonica-1.74/
    $ sudo ./configure [–prefix=/usr/local]
    $ sudo make
    $ sudo make install
```
### Instalación TESSERACT
Descargar [Tesseract]
```sh
    $ cd /usr/local/src/openalpr/tesseract-3.05.01
    $ sudo ./autogen.sh
    $ sudo ./configure
```
Configuration is done.
You can now build and install tesseract by running:
```sh
		$ make
		$ sudo make install
```

Training tools can be build and installed (after building of tesseract) with:
```sh
    $ make training
    $ sudo make training-install
    $ sudo make
    $ sudo make install
    $ sudo ldconfig
    $ sudo make training
    $ sudo make training-install
```
  Tuve el error de que faltaban unos archivos, es el mismo error que se puede ver en esta [branch].
  Así que hice lo que comentaron, en el siguiente [pull request].

### OpenALPR
  Instalé OpenALPR , siguiendo las instrucciones del GitHub de [OpenALPR].
```sh
    $ sudo apt-get update && sudo apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev
```
### OpenCV
  Instalar OpenCV 3.4 ya no fue necesario, ya que yo lo tenía instalado.
  Pero se puede instalar desde este [enlace].

[enlace]: <https://opencv.org/opencv-3-4.html>
[GitHub]: <https://github.com/openalpr/openalpr/wiki/Compilation-instructions-(Ubuntu-Linux)>
[Leptonica]: <http://www.leptonica.com/download.html>
[Tesseract]: <https://github.com/tesseract-ocr/tesseract/releases/tag/3.05.01sudo>
[branch]: <https://github.com/tesseract-ocr/tesseract/issues/1000>
[pull request]: <https://github.com/tesseract-ocr/tesseract/pull/1003/commits/4ccef1087122edb8a7044b673a23e4265865bf91>
[OpenALPR]: <https://github.com/openalpr/openalpr>


