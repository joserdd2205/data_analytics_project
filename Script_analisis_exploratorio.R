#Miguel Angel Guijarro
#Gerardo Ramos
#Jose Rafael Delgado Dib
#install.packages("ltm")
library(ltm)
library(tidyverse)
library(car)
library(ggplot2)
data <- read.csv("autos_seminuevos.csv")
set.seed(20)
data$mensualidad <-as.numeric(data$mensualidad)

summary(data)
data$marca <- as.factor(data$marca)
data$modelo <- as.factor(data$modelo)
summary(data)
data$transmision <- as.factor(data$transmision)
summary(data)
data$combustible <- as.factor(data$combustible)
data$año<-as.numeric(data$año)

summary(data)
data$ubicacion <- as.factor(data$ubicacion)
summary(data)
data <- na.omit(data)
summary(data)




#comprobar correlacion
numerical <- c("precio", "año", "numero.de.puertas", "enganche", "mensualidad")
data[numerical]
cor(data[numerical])
#como puede observarse la correlacion entre el enganche, la mensualidad y el precio es 1, lo cual indica multicolinearidad
#ademas la variable meses debe ser eliminada ya que tiene una desviacion estandar de 0
data1 <- subset(data, select = -c(enganche, mensualidad, meses))
summary(data1)
#graficar la relación de las variables con la variable precio
plot(precio~., data1, las=2 )


#Utilizar ggplot para analizar tres variables al mismo tiempo
ggplot(data1, aes(kilometraje, precio, colour = transmision)) + 
  geom_point()
