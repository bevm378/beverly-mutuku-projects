# =================================================================== #
#                         Modeling & Diagnostics                      #
# =================================================================== #

library(car)
library(MASS)

load("merged_clean.RDATA")

# --------------------- full model and null model ---------------------

res.full <- lm(target_deathrate ~ ., data=dat) 
res.null <- lm(target_deathrate ~ 1, data=dat) 

# ------------------------ stepwise selection -------------------------

forward <- step(res.null, 
                scope=list(upper=res.full),
                direction="forward",
                test = "F")

backward <- step(res.full, 
                 scope=list(lower=res.null),
                 direction="backward",
                 test = "F")

both <- step(res.null, 
             scope=list(upper=res.full),
             direction="both",
             test = "F")

summary(forward)
summary(backward)
summary(both)

# ------------ final model (chosen using stepwise results) ------------

final <- backward
summary(final)

# ------------------------- diagnostic plots --------------------------

par(mfrow=c(2,2))
plot(final)
par(mfrow=c(1,1))
plot(final)

# ----------------------------- residuals -----------------------------

err      <- resid(final)         # raw residuals 
err.rstu <- rstudent(final)      # studentized residuals (for outliers)

# check normality of residuals
hist(err, 
     breaks = 20, 
     main = "Histogram of Residuals",
     xlab = "Residuals")

qqnorm(err)
qqline(err)

which(abs(err.rstu)>3)           # outlier obs     

# ----------------------------- leverage -----------------------------

hat <- hatvalues(final)
round(summary(hat), 3)

p = length(coef(final))            
n = length(err)

lev.cut = 2*(p+1)/n         
which(hat > lev.cut)                             # high-leverage points

# -------------------------- Cook's Distance --------------------------

cd <- cooks.distance(final)

plot(cd, type="h", 
     main = "Cook's Distance",
     ylab = "Cook's D")

cd.cut = 1                
abline(h=cd.cut, col="red", lty=2)   
which(cd>cd.cut)                         # overall influence points obs
# ------------------------------- DFFITS ------------------------------

dff <- dffits(final)
dff.cut = 2*sqrt(p/n)                  

which(abs(dff)>dff.cut)                    # influence on fitted values

# ------------------------------- DFBETAS -----------------------------

dfb <- dfbetas(final)
dfb.cut = 2/sqrt(n)                         

which(abs(dfb)>dfb.cut)                     # influence on coefficients

# ------------------------- multicollinearity -------------------------

vif(final)                                  # VIF for multicollinearity

# ------------------------ train/test validation ----------------------

set.seed(304)
n.all   <- nrow(dat)
n.train <- round(0.8*n.all)

train.id  <- sample(1:n.all, n.train)
dat.train <- dat[train.id,]
dat.test  <- dat[-train.id,]

final.form <- formula(final)
res.train  <- lm(final.form, data=dat.train)

pred.test <- predict(res.train, newdata=dat.test)

r.test  <- cor(pred.test, dat.test$target_deathrate)
R2.test <- r.test^2

r.test
R2.test
