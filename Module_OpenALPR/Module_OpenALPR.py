from openalpr import Alpr

COUNTRY_CODE = 'mx2' 
REGION_CODE = 'mx2' 
CONF_PATH = '/usr/share/openalpr/runtime_data/config/mx2.conf' 
RUNTIME_PATH = '/usr/share/openalpr/runtime_data/' 

def is_correct_plate(candidate):
    ''' Verifica que las placas coincidan con el archivo de patrones que configuramos.'''

    if candidate['matches_template']:
        return { 'plate': candidate['plate'].encode('utf-8'), 'confidence': candidate['confidence'] }


def get_candidates(plate):
    ''' Obtiene todos los patrones candidatos/posibles de la placa '''

    correct_plates = []
    for candidate in plate['candidates']:
        correct_plates.append(is_correct_plate(candidate))
    return filter(None, correct_plates)


def numplate(image_path, num_coincidence = 10):
    ''' Retorna los patrones encontrados en la imagen que se ingresa y que concuerdan con el archivo de patrones que configuramos anteriormente'''

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
    
    image_path = sys.argv[1]
   # result = numplate(image_path)
    print(image_path)
#    print(result)
