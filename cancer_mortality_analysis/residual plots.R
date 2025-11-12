#model
final = lm(target_deathrate ~ 
             incidencerate + 
             pcths18_24 + 
             pctmarriedhouseholds + 
             pcths25_over + 
             pctunemployed16_over +
             pctbachdeg18_24 + 
             percentmarried + 
             medianagemale +
             pctemployed16_over + 
             birthrate + 
             pctempprivcoverage +
             pctprivatecoverage + 
             pctblack + 
             pctwhite + 
             pctnohs18_24 +
             medianage, data = merged_data_clean)

par(mfrow=c(2,2))
plot(final)
par(mfrow=c(1,1))

plot(final, which = 1)
plot(final, which = 2)
plot(final, which = 3)
plot(final, which = 4)
plot(final, which = 5)

plot(final$fitted.values,resid(final),xlab="Fitted Values",ylab="Residuals")
qqnorm(resid(final))
qqline(resid(final))

