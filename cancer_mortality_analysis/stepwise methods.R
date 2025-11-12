head(merged_data_clean)
library(MASS)

res.full = lm(target_deathrate ~ ., data=merged_data_clean)
res.null = lm(target_deathrate ~ 1, data=merged_data_clean)

forward = step(res.null, 
               scope=list(upper=res.full),
               direction="forward",
               test = "F")

backward = step(res.full, 
                scope=list(lower=res.null),
                direction="backward",
                test = "F")

both = step(res.null, 
            scope=list(upper=res.full),
            direction="both",
            test = "F")

summary(forward)
summary(backward)
summary(both)