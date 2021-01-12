library("readxl")
library(tseries)
library(reshape2)

#Importa datos
lima_series <- read_excel("RScripts/data/serie_san isidro.xlsx")

#Mejor lo leemos como ts y data.frame (posible bug pa otra serie)
df <- ts(data.frame(precios=lima_series[0:79,]$Precio_por_m2), start=c(1998,1), frequency=4)

#Percentual change in data

#Ploteamos la serie
plot(df)


#Boxplot para cada quarter.
boxplot(df_pct ~ cycle(df))

#Decomposition of the series: In Observerd = Trend + Seasonal + random.
#There is no trend.
df.desc = decompose(df)
plot(df, xlab='Quarter')


#Unit-root tests...
#Aumented Dickey Fuller:
adf.test(df) #La serie es estacionaria.
#Phillips-Perron test:
PP.test(df) #La serie no tiene raiz unitaria (estacionaria)
#KPSS test
library(tseries)
kpss.test(df) #H0: La data es estacionaria.

#Hasta ahora tenemos que la data es estacionaria dado los tres métodos.

par(mfrow=c(1,2))
#ACF function:
acf(df)$acf #1

pacf(df)$acf #2

#Test de ruido blanco:

Box.test(df, type="Ljung-Box") #H0: El modelo no presenta falta de fit
#H1: El modelo presenta falta de fit.
#a 10% el modelo no presenta falta de fit en la serie.

#Prediccion. ARIMA(0,0,1)
fit <- arima(df,c(0,1,1), seasonal= list(order=c(0,1,1),period=4)) #AIC: -241.57

acf(residuals(fit), main="Residuals of acf")

pacf(residuals(fit),main = "Residuals of PACF")
#Evaluamos los residuos:

Box.test(residuals(fit),lag = 2, type = "Ljung") #Los residuos son independientes de los datos

#Forecasting:
pred <- predict(fit, n.ahead=2*4)

par(mfrow=c(1,1))

ts.plot(df, pred$pred,
        col=c('blue','red'), xlab='Años',ylab='Values', main='Forecast Lima Series')

ts.plot(ts(data.frame(precios=lima_series$Precio_por_m2), start=c(1998,1), frequency=4))