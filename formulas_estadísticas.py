from collections import Counter
import math

# Medidas de tendencia central
# Datos individuales
# Media aritmetica
def media(numeros):
  return sum(numeros) / len(numeros)

def media_con_frecuencia(numeros, frecuencias):
  assert len(numeros) == len(frecuencias), "El numero de datos y el numero de frecuencias deben ser las mismas"
  return  sum([n * f for n, f in zip(numeros, frecuencias)]) / sum(frecuencias)

# Mediana
def _mediana_impar(numeros):
  return sorted(numeros)[len(numeros) // 2]

def _mediana_par(numeros):
  num_ordenados = sorted(numeros)
  punto_medio = len(numeros) // 2
  return (num_ordenados[punto_medio - 1] + num_ordenados[punto_medio]) / 2

def mediana(numeros):
  return _mediana_par(numeros) if len(numeros) % 2 == 0 else _mediana_impar(numeros)

# Moda
def moda(numeros):
  contador = Counter(numeros)
  max_count = max(contador.values())
  if max_count == 1:
    return []
  else:
    return [num for num, count in contador.items() if count == max_count]


# Datos Agrupados
# Media Aritmetica
def media_agrupada(marca_clase, frecuencias):
  if len(marca_clase) != len(frecuencias):
    raise ValueError("La lista de marca de clase y la lista de frecuencias deben tener la misma longitud.")
  
  return sum([c * f for c, f in zip(marca_clase, frecuencias)]) / sum(frecuencias)

# Mediana
def mediana_agrupada(lim_inferiores, frecuencias):
  if len(lim_inferiores) != len(frecuencias):
    raise ValueError("Las listas de límites inferiores y frecuencias deben tener la misma longitud.")
  intervalos = [(lim_inferiores[i], lim_inferiores[i + 1]) for i in range(len(lim_inferiores) - 1)]
  intervalos.append((lim_inferiores[-1], lim_inferiores[-1] + (lim_inferiores[-1] - lim_inferiores[-2])))
  
  N = sum(frecuencias)
  
  frecuencia_acumulada = 0
  clase_mediana = None
  for i, frecuencia in enumerate(frecuencias):
    frecuencia_acumulada += frecuencia
    if frecuencia_acumulada >= N / 2:
      clase_mediana = i
      break
    
  if clase_mediana is None:
    raise ValueError("No se pudo determinar la clase mediana.")
  
  L1 = intervalos[clase_mediana][0]  # Límite inferior de la clase mediana
  F1 = sum(frecuencias[:clase_mediana])  # Suma de frecuencias de las clases anteriores
  f_mediana = frecuencias[clase_mediana]  # Frecuencia de la clase mediana
  c = intervalos[clase_mediana][1] - intervalos[clase_mediana][0]  # Amplitud del intervalo
  
  mediana = L1 + ((N / 2 - F1) / f_mediana) * c
  return mediana

# Moda
def moda_agrupada(lim_inferiores, frecuencias):
  if len(lim_inferiores) != len(frecuencias):
    raise ValueError("Las listas de límites inferiores y frecuencias deben tener la misma longitud.")
  
  intervalos = [(lim_inferiores[i], lim_inferiores[i + 1]) for i in range(len(lim_inferiores) - 1)]
  intervalos.append((lim_inferiores[-1], lim_inferiores[-1] + (lim_inferiores[-1] - lim_inferiores[-2])))
  
  clase_modal = frecuencias.index(max(frecuencias))
  
  L1 = intervalos[clase_modal][0]  # Límite inferior de la clase modal
  f_modal = frecuencias[clase_modal]  # Frecuencia de la clase modal
  f_anterior = frecuencias[clase_modal - 1] if clase_modal > 0 else 0  # Frecuencia de la clase anterior
  f_siguiente = frecuencias[clase_modal + 1] if clase_modal < len(frecuencias) - 1 else 0  # Frecuencia de la clase siguiente
  c = intervalos[clase_modal][1] - intervalos[clase_modal][0]  # Amplitud del intervalo
  
  delta1 = f_modal - f_anterior
  delta2 = f_modal - f_siguiente
  moda = L1 + (delta1 / (delta1 + delta2)) * c
  return moda

# Medidas de posicion
# Datos Individuales
# Cuartiles
def cuartil(datos, posicion):
    if posicion not in [1, 2, 3]:
        raise ValueError("Para cuartiles, la posición debe ser 1, 2 o 3.")
    
    datos = sorted(datos)
    n = len(datos)
    
    k = (n - 1) * (posicion / 4)
    f = int(k)
    c = k - f

    if f + 1 < n:
        return datos[f] + c * (datos[f + 1] - datos[f])
    else:
        return datos[f]

# Deciles
def decil(datos, posicion):
    if not (1 <= posicion <= 9):
        raise ValueError("Para deciles, la posición debe estar entre 1 y 9.")
    
    datos = sorted(datos)
    n = len(datos)
    
    k = (n - 1) * (posicion / 10)
    f = int(k)
    c = k - f
    
    if f + 1 < n:
        return datos[f] + c * (datos[f + 1] - datos[f])
    else:
        return datos[f]

# Percentiles
def percentil(datos, posicion):
    datos = sorted(datos)
    n = len(datos)
    
    if not (0 <= posicion <= 100):
        raise ValueError("La posición debe estar entre 0 y 100 para percentiles.")
    
    k = (n - 1) * (posicion / 100)
    f = int(k)
    c = k - f
    
    if f + 1 < n:
        return datos[f] + c * (datos[f + 1] - datos[f])
    else:
        return datos[f]

# Rango intercuartil
def rango_intercuartil(datos):
  return cuartil(datos, 3) - cuartil(datos, 1)

# Datos Agrupados
# Cuartiles
def cuartil_agrupado(k, limites_inferiores, frecuencias):
    n = sum(frecuencias)
    
    pos_k = k * (n / 4)
    
    frecuencias_acumuladas = [sum(frecuencias[:i+1]) for i in range(len(frecuencias))]
    
    for i in range(len(frecuencias_acumuladas)):
        if pos_k <= frecuencias_acumuladas[i]:
            l_i = limites_inferiores[i]
            N_i_minus_1 = frecuencias_acumuladas[i-1] if i > 0 else 0
            n_i = frecuencias[i]
            
            if i < len(limites_inferiores) - 1:
                c = limites_inferiores[i+1] - limites_inferiores[i]
            else:
                c = limites_inferiores[i] - limites_inferiores[i-1]
            break
    
    cuartil = l_i + ((pos_k - N_i_minus_1) / n_i) * c
    
    return cuartil

# Deciles
def decil_agrupado(k, limites_inferiores, frecuencias):
    n = sum(frecuencias)
    
    pos_k = k * (n / 10)
    
    frecuencias_acumuladas = [sum(frecuencias[:i+1]) for i in range(len(frecuencias))]
    
    for i in range(len(frecuencias_acumuladas)):
        if pos_k <= frecuencias_acumuladas[i]:
            l_i = limites_inferiores[i]
            N_i_minus_1 = frecuencias_acumuladas[i-1] if i > 0 else 0
            n_i = frecuencias[i]
            
            if i < len(limites_inferiores) - 1:
                c = limites_inferiores[i+1] - limites_inferiores[i]
            else:
                c = limites_inferiores[i] - limites_inferiores[i-1]
            break
    
    decil = l_i + ((pos_k - N_i_minus_1) / n_i) * c
    
    return decil

# Percentiles
def percentil_agrupado(k, limites_inferiores, frecuencias):
    n = sum(frecuencias)
    
    pos_k = k * (n / 100)
    
    frecuencias_acumuladas = [sum(frecuencias[:i+1]) for i in range(len(frecuencias))]
    
    for i in range(len(frecuencias_acumuladas)):
        if pos_k <= frecuencias_acumuladas[i]:
            l_i = limites_inferiores[i]
            N_i_minus_1 = frecuencias_acumuladas[i-1] if i > 0 else 0
            n_i = frecuencias[i]
            
            if i < len(limites_inferiores) - 1:
                c = limites_inferiores[i+1] - limites_inferiores[i]
            else:
                c = limites_inferiores[i] - limites_inferiores[i-1]
            break
    
    percentil = l_i + ((pos_k - N_i_minus_1) / n_i) * c
    
    return percentil

# Medidas de Dispersion
# Datos individuales
# Rango
def rango(datos):
  return max(datos) - min(datos)

# Varianza
def varianza(datos, tipo="p"):
  if len(datos) < 2:
    raise ValueError("La lista de datos debe contener al menos dos elementos para calcular la varianza.")

  media = sum(datos) / len(datos)
  suma_cuadrados = sum((x - media) ** 2 for x in datos)

  if tipo == "p":
    return suma_cuadrados / len(datos)
  elif tipo == "m":
    return suma_cuadrados / (len(datos) - 1)
  else:
    raise ValueError("El parámetro 'tipo' debe ser 'p = poblacion' o 'm = muestra'.")

# Desviacion estandar
def desviacion_estandar(datos, tipo="p"):
  if tipo == "p":
    return math.sqrt(varianza(datos))
  elif tipo == "m":
    return math.sqrt(varianza(datos, tipo="m"))
  else:
    raise ValueError("El parámetro 'tipo' debe ser 'p = poblacion' o 'm = muestra'.")

# Datos agrupados
# Varianza
def varianza_poblacion_agrupada(marcas_clase, frecuencias, media):
    total_poblacion = sum(frecuencias)
    suma_xi_ni = sum((xi ** 2) * ni for xi, ni in zip(marcas_clase, frecuencias))
    varianza = (suma_xi_ni / total_poblacion) - (media ** 2)
    return varianza

def varianza_muestra_agrupada(marcas_clase, frecuencias, media_muestra):
    total_muestra = sum(frecuencias)
    if total_muestra <= 1:
        raise ValueError("El tamaño de la muestra debe ser mayor a 1 para calcular la varianza muestral.")
    
    suma_xi_ni = sum((xi ** 2) * ni for xi, ni in zip(marcas_clase, frecuencias))
    varianza = (suma_xi_ni / (total_muestra - 1)) - (media_muestra ** 2)
    return varianza


# Coeficiente de variacion
def coeficiente_variacion(desviacion_estandar, media):
    cv = (desviacion_estandar / media) * 100
    return cv