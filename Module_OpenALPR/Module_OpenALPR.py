''' Modulo pensado para recibir el path de una imagen y retornar los patrones posibles, hecho con OpenALPR '''

from openalpr import Alpr

COUNTRY_CODE = 'mx2' 
REGION_CODE = 'mx2' 
CONF_PATH = '/usr/share/openalpr/runtime_data/config/mx2.conf' 
RUNTIME_PATH = '/usr/share/openalpr/runtime_data/' 

def is_correct_plate(candidate):
    ''' Verifica que las placas coincidan con el archivo de patrones que configuramos anteriormente.
    
    Parameters
    ----------
    candidate:   
    Recibe un diccionario que confirma o no si la placa esta dentro de nuestro archivo de patrones del pais.

    Returns
    -------
    De salida nos entrega un diccionario con la placa y el porcentaje de coincidencia'''

    if candidate['matches_template']:
        return { 'plate': candidate['plate'].encode('utf-8'), 'confidence': candidate['confidence'] }


def get_candidates(plate):
    ''' Obtiene todos los patrones candidatos/posibles de la placa. 

    Parameters
    ----------
    plate:
    Recibe un diccionario que contiene los patrones candidatos.

    Returns
    -------
     De salida nos entrega una lista de diccionarios con los patrones posibles y su porcentaje de coincidencia
    '''

    correct_plates = []
    for candidate in plate['candidates']:
        correct_plates.append(is_correct_plate(candidate))
    return filter(None, correct_plates)


def numplate(image_path, num_coincidence = 10):
    ''' Retorna los patrones encontrados en la imagen que se ingresa y que concuerdan con el archivo de patrones que configuramos anteriormente.
    Parameters
    ----------
    image_path:
    Recibe el path de la imagen a procesar (obligatorio) 

    num_coincidence:
    El numero de patrones posibles que deseamos analizar (no es obligatorio, por default es 10)

    Returns
    -------
    De salida nos entrega una lista con diccionarios con los patrones posibles y su porcentaje de coincidencia
'''

    alpr = Alpr(COUNTRY_CODE, CONF_PATH, RUNTIME_PATH)
    if not alpr.is_loaded():
        print('Error cargando openALPR')
        sys.exit(1)

    alpr.set_top_n(num_coincidence)
    alpr.set_default_region(REGION_CODE)
    
    results = alpr.recognize_file(image_path)
    correct_plates = [] 
    for plate in results['results']:
        correct_plates = get_candidates(plate)
        
    alpr.unload()
    return correct_plates

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = numplate(image_path)
        print(result)

    else:
        print("Ejemplo de uso\n-------------- \n>> python Module_OpenALPR.py 1.jpg 10\n \nParameters\n----------\n image_path: \n Recibe el path de la imagen a procesar (obligatorio)\n\n num_coincidence:\n El numero de patrones posibles que deseamos analizar (no es obligatorio, por default es 10)\n\nReturns\n-------\n De salida nos entrega una lista con diccionarios con los patrones posibles y su porcentaje de coincidencia")
