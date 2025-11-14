# ==================================================================== #
#                        Data Cleaning & Analysis                      #
# ==================================================================== #

library(car)

# ---------------------------- load raw data ---------------------------

dat1 <- read.csv("cancer_reg.csv")
dat2 <- read.csv("avg-household-size.csv")

# ----------------------------- merge data -----------------------------

merged_raw <- merge(dat1, dat2, by="geography")

summary(merged_raw)
names(merged_raw)
colSums(is.na(merged_raw))                    # missing values by column

# ------------------ remove ID and irrelevant columns ------------------

dat <- subset(merged_raw, select = -c(geography, 
                                      binnedinc,
                                      pctotherrace,
                                      pctpubliccoveragealone,
                                      pctprivatecoveragealone,
                                      studypercap,
                                      statefips, 
                                      countyfips))

dat <- dat[, sapply(dat, is.numeric)]    # keep numeric columns only
dat <- na.omit(dat)                      # drop rows with missing values

summary(dat)           
names(dat)             
round(cor(dat), 2)                       # correlation among variables

save(dat, file = "merged_clean.RDATA")
