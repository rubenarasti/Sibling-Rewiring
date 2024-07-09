# TFG: Sibling-Rewiring2.0
Bienvenido a Sibling-Rewiring (SiRe). SiRe es una aplicación web desarrollada como trabajo final de grado en 2021. Esta es su segunda iteración.

SiRe se encarga de obtener la mejor organización de alumnos en un colegio para reducir al mínimo el riesgo de contagio.

## Funcionamiento
SiRe se basa en el concepto de los grupos burbuja, que consiste en aislar las aulas de estudiantes para minimizar su interacción con alumnos de otras aulas. Para que esta medida sea más efectiva, se debe considerar que algunas clases de distintos cursos están conectadas por hermanos que conviven en el mismo hogar.

Para minimizar el riesgo de contagio, se busca cambiar a los hermanos de grupo de manera que estas conexiones separen al máximo número de clases, intentando no perjudicar el riesgo de algunas clases sobre otras.

Para lograr esto, SiRe utiliza un criterio tri-objetivo para evaluar las distintas combinaciones en las que se asignan los hermanos a los grupos. Mediante un algoritmo genético, se encuentran múltiples soluciones óptimas a este problema con distintas evaluaciones, permitiendo al usuario elegir la solución que mejor se ajuste a sus necesidades.

## Resultados

![grafo.png](https://github.com/rubenarasti/Sibling-Rewiring/blob/main/Documentaci%C3%B3n/Imagenes%20documentacion/grafo_clases.png)

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

