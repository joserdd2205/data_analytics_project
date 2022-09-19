#Miguel Angel Guijarro
#Gerardo Ramos
#Jose Rafael Delgado Dib
#install.packages("ltm")
library(ltm)
library(tidyverse)
library(car)
data <- read.csv("autos_seminuevos.csv")
seed(20)
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


#incluir todos para analisis exploratorio
reg_lineal <- lm(precio~.,data= data)
summary(reg_lineal)
#Al ver los resultados con la funcion summary podemos observar que
#el modelohr el y el enganche son estadisticamente significativos, sin embargo se intuye que 
#El valor del enganche pueda estar correlacionado con el precio
numerical <- c("precio", "año", "numero.de.puertas", "meses", "enganche", "mensualidad")
data[numerical]
cor(data[numerical])
#como puede observarse la correlacion entre el enganche, la mensualidad y el precio es 1, lo cual indica multicolinearidad
#es por ello que esta variable debe eliminarse del modelo
data1 <- subset(data, select = -c(enganche, mensualidad, modelo))

#dividir en training y testing (.70% y .30%) con reemplazo

muestra <- sample(c(TRUE, FALSE), nrow(data), replace=TRUE, prob=c(0.7,0.3))
train  <- data1[muestra, ]
test   <- data1[!muestra, ]
test

reg_lineal <- lm(precio~., data=train)
summary(reg_lineal)
#Ahora podemos observar que el modelo es significativo al 95% ya sin variables correlacionadas
#Ahora comprobamos con el testing set
predict(reg_lineal, test)
#Debido a que las modelos tienen nuevos niveles se quitaran estas del dataset