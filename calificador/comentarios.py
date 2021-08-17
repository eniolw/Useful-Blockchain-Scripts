import re
import sys
from legibilidad import legibilidad


palabras_ignorables = (
    'hola',  'saludo', 'noche', 'bienvenid', 'hello',
    'felicidades', 'felicitaciones', 'gracias',
    'gustó', 'excelente', 'disculp'
)


def calificar_comentario(texto):

    #Extraer lineas y omitir citas:
    lineas = texto.split("\n")
    texto = "\n".join(l for l in lineas if not l.startswith(">"))

    #Seleccionar caracteres significativos (omitiendo emojies, etc.):
    texto = "".join([t for t in texto if re.search('[A-Za-z0-9áéíóúÁÉÍÓÚñÑÜü.,;:?@()%\s-]', t)])

    #Extraer palabras:
    palabras = [p.lower() for p in texto.split() if re.search("[a-z0-9áéíóúüñ]+", p)]

    #Omitir palabras con onomatopeya de risa:
    palabras = [p for p in palabras if not re.search('(jeje|jaja|haha)+', p)]

    #Omitir palabras que sean arroba-menciones:
    palabras = [p for p in palabras if not re.search('@.+', p)]

    print('Palabras:', palabras)

    #Verificar si hay palabras validas:
    if len(palabras) == 0: return 0

    #Verificar si el texto posee palabras que descalifiquen el comentario 
    #(saludos, felicitaciones, etc):
    las_palabras = " ".join(palabras)
    for p in palabras_ignorables:
        if re.search(p, las_palabras): return 0

    puntuacion = 0

    # Calculando puntuacion si es una pregunta de al menos 5 palabras 
    # o es un comentario de al menos 10 palabras:
    if (len(palabras) >= 5 and any([p for p in palabras if p.endswith("?")])) or \
       (len(palabras) >= 10):

        #Calificacion en funcion del numero de palabras:
        a = min(len(palabras) / 50, 1)

        #Calificacion en funcion del indice de perspicuidad de Szigriszt-Pazos:
        b = (100 - legibilidad.szigriszt_pazos(texto)) / 100
        # print(a, b)
        puntuacion = a + b

    return puntuacion


def main(argv):
    entrada = " ".join(argv[1:])
    calificacion = calificar_comentario(entrada)
    print(calificacion)


if __name__ == '__main__':
    argv = sys.argv
    main(argv)
