import flet as ft
from typing import List

# Importar las funciones estadísticas
from formulas_estadísticas import (
    media, mediana, moda, media_agrupada, mediana_agrupada, moda_agrupada,
    cuartil, decil, percentil, rango_intercuartil, cuartil_agrupado,
    varianza, desviacion_estandar, rango, percentil_agrupado, decil_agrupado,
    coeficiente_variacion
)

def main(page: ft.Page):
    page.title = "Calculadora Estadística"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    title = ft.Text(
        value="Medidas de tendencia central, de posición y de dispersión",
        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        text_align=ft.TextAlign.CENTER
    )

    def parse_input(input_str: str) -> List[float]:
        """Convierte el string de entrada en una lista de números"""
        try:
            return [float(x.strip()) for x in input_str.split(',') if x.strip()]
        except ValueError:
            return []

    # Switch para tipo de datos
    data_type_switch = ft.Switch(
        label="Datos Agrupados",
        value=False,
        on_change=lambda e: update_input_hint(e)
    )

    # Inputs para valores y frecuencias
    values_input = ft.TextField(
        label="Ingrese límites inferiores de clase",
        width=420,
        hint_text="Ejemplo: 10,20,30,40,50",
        visible=False
    )
    frequencies_input = ft.TextField(
        label="Ingrese frecuencias",
        width=420,
        hint_text="Ejemplo: 1,2,3,4,5",
        visible=False
    )
    numbers_input = ft.TextField(
        label="Ingrese números",
        width=420,
        hint_text="Ejemplo: 1,2,3,4,5",
        visible=True
    )

    # Inputs para deciles y percentiles
    decile_input = ft.TextField(
        label="Posición Decil (1-9)",
        width=210,
        hint_text="Ejemplo: 3",
    )
    percentile_input = ft.TextField(
        label="Posición Percentil (1-99)",
        width=210,
        hint_text="Ejemplo: 85",
    )

    # Inputs para coeficiente de variacion
    media_input = ft.TextField(
        label="Valor de la media",
        width=210,
        hint_text="Ejemplo: 50.5",
    )

    desviacion_input = ft.TextField(
        label="Valor de desviacion",
        width=210,
        hint_text="Ejemplo: 25.7",
    )

    def update_input_hint(e):
        if data_type_switch.value:
            values_input.visible = True
            frequencies_input.visible = True
            numbers_input.visible = False
            coeficiente.visible = True
            tab.tabs.append(t_coeficiente_variacion)
        else:
            values_input.visible = False
            frequencies_input.visible = False
            numbers_input.visible = True
            coeficiente.visible = False
            if t_coeficiente_variacion in tab.tabs:
                tab.tabs.remove(t_coeficiente_variacion)
    
        mean_result.value = "Media: "
        median_result.value = "Mediana: "
        mode_result.value = "Moda: "
        q1_result.value = "Q1 (25%): "
        q2_result.value = "Q2 (50%): "
        q3_result.value = "Q3 (75%): "
        decile_result.value = "Decil: "
        percentile_result.value = "Percentil: "
        iqr_result.value = "Rango Intercuartil: "
        variance_result.value = "Varianza: "
        std_dev_result.value = "Desviación estándar: "
        range_result.value = "Rango: "
        decile_input.value = ""
        percentile_input.value = ""
        coeficiente.value = "Coeficiente de variación: "
        media_input.value = ""
        desviacion_input.value = ""
        coeficiente_result.value = "Coeficiente de variación: "

        page.update()

    # Resultados para tendencia central
    mean_result = ft.Text("Media: ")
    median_result = ft.Text("Mediana: ")
    mode_result = ft.Text("Moda: ")

    # Resultados para medidas de posición básicas
    q1_result = ft.Text("Q1 (25%): ")
    q2_result = ft.Text("Q2 (50%): ")
    q3_result = ft.Text("Q3 (75%): ")

    # Resultados para medidas de posición adicionales
    decile_result = ft.Text("Decil: ")
    percentile_result = ft.Text("Percentil: ")
    iqr_result = ft.Text("Rango Intercuartil: ")

    # Resultados para medidas de dispersión
    variance_result = ft.Text("Varianza: ")
    std_dev_result = ft.Text("Desviación estándar: ")
    range_result = ft.Text("Rango: ")
    coeficiente = ft.Text("Coeficiente de variación: ", visible=False)

    # Resultados para coeficiente de variacion
    coeficiente_result = ft.Text("Coeficiente de variación: ")

    def calcular_medidas_de_posición(e):
        try:
            if data_type_switch.value:  # Datos agrupados
                limites = parse_input(values_input.value)
                frecuencias = parse_input(frequencies_input.value)
                
                if not limites or not frecuencias or len(limites) != len(frecuencias):
                    raise ValueError("Datos inválidos o incompletos")

                # Calcular decil si se ingresó un valor
                if decile_input.value:
                    try:
                        pos_decil = int(decile_input.value)
                        if 1 <= pos_decil <= 9:
                            decil_val = decil_agrupado(pos_decil, limites, frecuencias)
                            decile_result.value = f"Decil {pos_decil}: {decil_val:.2f}"
                        else:
                            decile_result.value = "Error: Posición del decil debe estar entre 1 y 9"
                    except ValueError:
                        decile_result.value = "Error: Ingrese un número válido para el decil"

                # Calcular percentil si se ingresó un valor
                if percentile_input.value:
                    try:
                        pos_percentil = int(percentile_input.value)
                        if 1 <= pos_percentil <= 99:
                            percentil_val = percentil_agrupado(pos_percentil, limites, frecuencias)
                            percentile_result.value = f"Percentil {pos_percentil}: {percentil_val:.2f}"
                        else:
                            percentile_result.value = "Error: Posición del percentil debe estar entre 1 y 99"
                    except ValueError:
                        percentile_result.value = "Error: Ingrese un número válido para el percentil"

                # Calcular rango intercuartil para datos agrupados
                q1 = cuartil_agrupado(1, limites, frecuencias)
                q3 = cuartil_agrupado(3, limites, frecuencias)
                iqr = q3 - q1
                iqr_result.value = f"Rango Intercuartil: {iqr:.2f}"

            else:  # Datos individuales
                datos = parse_input(numbers_input.value)
                if not datos:
                    raise ValueError("Por favor ingrese datos válidos")

                # Calcular decil si se ingresó un valor
                if decile_input.value:
                    try:
                        pos_decil = int(decile_input.value)
                        if 1 <= pos_decil <= 9:
                            decil_val = decil(datos, pos_decil)
                            decile_result.value = f"Decil {pos_decil}: {decil_val:.2f}"
                        else:
                            decile_result.value = "Error: Posición del decil debe estar entre 1 y 9"
                    except ValueError:
                        decile_result.value = "Error: Ingrese un número válido para el decil"

                # Calcular percentil si se ingresó un valor
                if percentile_input.value:
                    try:
                        pos_percentil = int(percentile_input.value)
                        if 1 <= pos_percentil <= 99:
                            percentil_val = percentil(datos, pos_percentil)
                            percentile_result.value = f"Percentil {pos_percentil}: {percentil_val:.2f}"
                        else:
                            percentile_result.value = "Error: Posición del percentil debe estar entre 1 y 99"
                    except ValueError:
                        percentile_result.value = "Error: Ingrese un número válido para el percentil"

                # Calcular rango intercuartil
                iqr = rango_intercuartil(datos)
                iqr_result.value = f"Rango Intercuartil: {iqr:.2f}"

            page.update()

        except Exception as e:
            page.open(ft.SnackBar(content=ft.Text(f"Error: {str(e)}")))
            page.update()

    def calcular_medidas():
        try:
            if data_type_switch.value:  # Datos agrupados
                limites = parse_input(values_input.value)
                frecuencias = parse_input(frequencies_input.value)
                
                # Validación básica
                if not limites or not frecuencias or len(limites) != len(frecuencias):
                    raise ValueError("Datos inválidos o incompletos. El número de límites debe ser igual al número de frecuencias")

                # Calculamos el ancho de clase (asumiendo que es constante)
                ancho_clase = limites[1] - limites[0]
                
                # Calculamos las marcas de clase (punto medio de cada intervalo)
                marcas_clase = [li + (ancho_clase/2) for li in limites]
                
                # Medidas de tendencia central
                # Media
                mean_val = sum(m * f for m, f in zip(marcas_clase, frecuencias)) / sum(frecuencias)
                mean_result.value = f"Media: {mean_val:.2f}"
                
                # Mediana
                try:
                    median_val = mediana_agrupada(limites, frecuencias)
                    median_result.value = f"Mediana: {median_val:.2f}"
                except Exception as e:
                    median_result.value = "Mediana: Error en el cálculo"
                    print(f"Error en mediana: {str(e)}")

                # Moda
                try:
                    mode_val = moda_agrupada(limites, frecuencias)
                    mode_result.value = f"Moda: {mode_val:.2f}"
                except Exception as e:
                    mode_result.value = "Moda: Error en el cálculo"
                    print(f"Error en moda: {str(e)}")

                # Medidas de posición
                try:
                    q1 = cuartil_agrupado(1, limites, frecuencias)
                    q2 = cuartil_agrupado(2, limites, frecuencias)
                    q3 = cuartil_agrupado(3, limites, frecuencias)
                    
                    q1_result.value = f"Q1 (25%): {q1:.2f}"
                    q2_result.value = f"Q2 (50%): {q2:.2f}"
                    q3_result.value = f"Q3 (75%): {q3:.2f}"
                except Exception as e:
                    q1_result.value = "Q1: Error en el cálculo"
                    q2_result.value = "Q2: Error en el cálculo"
                    q3_result.value = "Q3: Error en el cálculo"
                    print(f"Error en cuartiles: {str(e)}")

                # Medidas de dispersión
                try:
                    # Varianza poblacional
                    var_p = sum(frecuencias[i] * (marcas_clase[i] - mean_val) ** 2 for i in range(len(frecuencias))) / sum(frecuencias)
                    # Varianza muestral
                    var_m = sum(frecuencias[i] * (marcas_clase[i] - mean_val) ** 2 for i in range(len(frecuencias))) / (sum(frecuencias) - 1)
                    # Desviación estándar
                    desv_est_p = var_p ** 0.5
                    desv_est_m = var_m ** 0.5
                    # Coeficiente de variacion
                    coeficiente_p = coeficiente_variacion(desv_est_p, mean_val)
                    coeficiente_m = coeficiente_variacion(desv_est_m, mean_val)
                    
                    variance_result.value = f"Varianza (Poblacional): {var_p:.2f}\nVarianza (Muestral): {var_m:.2f}"
                    std_dev_result.value = f"Desviación estándar (Poblacional): {desv_est_p:.2f}\nDesviación estándar (Muestral): {desv_est_m:.2f}"
                    range_result.value = f"Rango: {max(limites) - min(limites):.2f}"
                    coeficiente.value = f"Coeficiente de variación (Poblacional): {coeficiente_p:.2f}%\nCoeficiente de variación (Muestral): {coeficiente_m:.2f}%"
                except Exception as e:
                    variance_result.value = "Varianza: Error en el cálculo"
                    std_dev_result.value = "Desviación estándar: Error en el cálculo"
                    range_result.value = "Rango: Error en el cálculo"
                    print(f"Error en medidas de dispersión: {str(e)}")

                page.update()

            else:  # Datos individuales
                datos = parse_input(numbers_input.value)
                if not datos:
                    raise ValueError("Por favor ingrese datos válidos")

                # Medidas de tendencia central
                mean_val = media(datos)
                median_val = mediana(datos)
                mode_val = moda(datos)
                
                mean_result.value = f"Media: {mean_val:.2f}"
                median_result.value = f"Mediana: {median_val:.2f}"
                mode_result.value = f"Moda: {', '.join(map(str, mode_val)) if mode_val else 'No hay moda'}"

                # Medidas de posición básicas
                q1_val = cuartil(datos, 1)
                q2_val = cuartil(datos, 2)
                q3_val = cuartil(datos, 3)
                
                q1_result.value = f"Q1 (25%): {q1_val:.2f}"
                q2_result.value = f"Q2 (50%): {q2_val:.2f}"
                q3_result.value = f"Q3 (75%): {q3_val:.2f}"

                # Medidas de dispersión
                var_p = varianza(datos, "p")
                var_m = varianza(datos, "m")
                desv_est_p = desviacion_estandar(datos, "p")
                desv_est_m = desviacion_estandar(datos, "m")
                rango_val = rango(datos)
                
                variance_result.value = f"Varianza (Poblacional): {var_p:.2f}\nVarianza (Muestral): {var_m:.2f}"
                std_dev_result.value = f"Desviación estándar (Poblacional): {desv_est_p:.2f}\nDesviación estándar (Muestral): {desv_est_m:.2f}"
                range_result.value = f"Rango: {rango_val:.2f}"

            page.update()

        except Exception as e:
            page.open(ft.SnackBar(content=ft.Text(f"Error: {str(e)}")))
            page.update()
    
    def calcular_coeficiente(e):
        try:
            if not media_input.value or not desviacion_input.value:
                    raise ValueError("Ingrese valores para la media y desviacion estandar")
            
            try:
                media_v = float(media_input.value)
                desviacion_v = float(desviacion_input.value)

                coeficiente_valor = coeficiente_variacion(desviacion_v, media_v)
                estimacion = ""
                
                match coeficiente_valor:
                    case cv if cv <= 7:
                        estimacion = "precisas"
                    case cv if 8 <= cv <= 14:
                        estimacion = "aceptables"
                    case cv if 15 <= cv <= 20:
                        estimacion = "regulares"
                    case cv if cv > 20:
                        estimacion = "poco precisas"
                    case _:
                        estimacion = "Valor fuera de los rangos esperados"

                coeficiente_result.value = f"Coeficiente de variación: {coeficiente_valor:.2f}%\nLas estimaciones se consideran {estimacion}"
            except ValueError:
                coeficiente_result.value = "Error: Ingrese numeros validos"
        
            page.update()

        except Exception as e:
            page.open(ft.SnackBar(content=ft.Text(f"Error: {str(e)}")))
            page.update()

        page.update()

    calculate_button = ft.ElevatedButton("Calcular", on_click=lambda _: calcular_medidas())
    calculate_position_button = ft.ElevatedButton("Calcular Posiciones", on_click=calcular_medidas_de_posición)
    calcular_coeficiente_button = ft.ElevatedButton("Calcular Coeficiente", on_click=calcular_coeficiente)

    tab = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        indicator_color=ft.colors.GREEN_200,
        tabs=[
            ft.Tab(
                text="Tendencia Central",
                icon=ft.icons.CENTER_FOCUS_WEAK,
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            mean_result,
                            median_result,
                            mode_result,
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                ),
            ),
            ft.Tab(
                text="Posición",
                icon=ft.icons.POLICY_SHARP,
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            q1_result,
                            q2_result,
                            q3_result,
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                ),
            ),
            ft.Tab(
                text="Posición Adicional",
                icon=ft.icons.ANALYTICS_OUTLINED,
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    decile_input,
                                    percentile_input,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            calculate_position_button,
                            decile_result,
                            percentile_result,
                            iqr_result,
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                ),
            ),
            ft.Tab(
                text="Dispersión",
                icon=ft.icons.DEBLUR_SHARP,
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            variance_result,
                            std_dev_result,
                            range_result,
                            coeficiente,
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                ),
            ),
        ],
        expand=1,
    )

    # Pestaña coneficiene de variacion personalizado
    t_coeficiente_variacion = ft.Tab(
        text="Coeficiente de Variacion",
        icon=ft.icons.EQUALIZER,
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            media_input,
                            desviacion_input,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    calcular_coeficiente_button,
                    coeficiente_result,
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        ),
    )

    input_container = ft.Container(
        content=ft.Column(
            controls=[
                data_type_switch,
                values_input,
                frequencies_input,
                numbers_input,
                calculate_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=ft.padding.only(bottom=20),
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    title,
                    input_container,
                    tab,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )
    )

ft.app(main)