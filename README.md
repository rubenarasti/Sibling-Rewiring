# TFG: Sibling-Rewiring2.0
Bienvenido a Sibling-Rewiring (SiRe). SiRe es una aplicación web que se desarrolló como trabajo final de grado en 2021. Esta es su segunda iteración.

Se encargará de obtener la mejor organización de alumnos en un colegio para reducir el riesgo de contagio al mínimo.

### Funcionamiento
SiRe, se basa en el concepto de los grupos burbuja, que son aislar las aulas de estudiantes para que tengan la mínima interacción posible con alumnos de otras aulas. Para que esta medida sea más efectiva, se debe tener en cuenta que algunas clases de distintos cursos están conectadas por hermanos que conviven en el mismo hogar.
Para minimizar el riesgo de contagio, se busca cambiar a los hermanos de grupo para que dichas conexiones aislen al máximo número de clases intentando no perjudicar el riesgo de algunas clases sobre otras.

Para conseguir esto, SiRe utiliza un criterio tri-objetivo para evaluar las distintas combinaciones en las que asignan los hermanos a los grupos. mediante un algoritmo genético, se ecuentran múltiples soluciones optimas (ESTO NO SE SI ESTÁ BIEN DICHO YA Q EL OPTIMO ES LO MEJOR POSIBLE) a este problema con distintas evaluaciones para que el usuario pueda elegir la solucion que más se ajuste a sus necesidades.


### Resultados

![graficas](https://github.com/rubenarasti/Sibling-Rewiring/blob/main/Documentaci%C3%B3n/Imagenes%20documentacion/grafo_clases.png)

## Características

## Web
La aplicación web se puede probar en el siguiente enlace: [Sibling-Rewiring2.0](https://sire-ddeac2c1782a.herokuapp.com/)

## Instalación
Si se quiere instalar la aplicación localmente toda la información necesaria se encuentra en el apartado D.3 de los [anexos](https://github.com/rubenarasti/Sibling-Rewiring/blob/main/Documentaci%C3%B3n/TFG-SiblingRewiring2.0-Anexos.pdf) 

##

# TFG: Sibling-Rewiring
Welcome to Sibling-Rewiring (SIRE). Sire is an app developed as TFG. 

The app will obtain the best placement of students in their classrooms, to reduce the risks of transmission to a minimum, taking into account sibling relationships.

### Abstract
Nowadays, we are experiencing a global pandemic, COVID-19 pandemic produced by SARS-CoV-2 virus. This fact has generated new needs changing people lifestyle.

This project emerges to respond to one of those needs, the grouping of children in school. Previously they had thought of siblings with same age, getting them into the same class, because they also be together at home. But what happens with siblings with different age?

Thanks to the help of simulated annealing and complex networks we have achieved a solution to the problem. We consider all siblings in school to generate a network, where links
are siblings and nodes classes of school. We mix that net looking for a similar one with a minimum risk of transmission.

Sire (Sibling-Rewiring) is therefore an application designed to minimize the risk of spread of any disease transmitted by air or close contact.

## Installation

