dat.ff=read.csv("cancer_reg.csv") 
dat.ff2=read.csv("avg-household-size.csv")

names(dat.ff)
names(dat.ff2)

merged_data = merge(dat.ff, dat.ff2, by = "geography")

str(merged_data)
summary(merged_data)

merged_data_clean = subset(merged_data, select = -c(geography, 
                                                    binnedinc,
                                                    pctotherrace,
                                                    pctpubliccoveragealone,
                                                    pctprivatecoveragealone,
                                                    studypercap,
                                                    statefips, 
                                                    countyfips))
merged_data_clean = na.omit(merged_data_clean)