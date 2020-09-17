library(readxl)
require(vcd)
require(MASS)
data <- read_excel("interarrival_times-Assn3-2020.xls",)
View(data)

day1 = as.vector(data$'Day1')
View(day1)

arrival_mean = mean(day1)
print(arrival_mean)

fit1 <- fitdistr(day1, "exponential")
ks.test(day1, "pexp", fit1$estimate)
