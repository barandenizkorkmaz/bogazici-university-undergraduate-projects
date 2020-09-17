library(readxl)
data <- read_excel("Assignment2-Interarrival_Data-S2020.xls")
View(data)

day1 = as.vector(data$'Day 1')
day2 = as.vector(data$'Day 2')

# TASK 1
ks.test(day1, "punif", 0, 400)
ks.test(day2, "punif", 0, 400)

# TASK 2
table1 = c(mean(day1),sd(day1),min(day1),max(day1))
table2 = c(mean(day2),sd(day2),min(day2),max(day2))
stats_view <- data.frame(table1, table2, row.names = c("Mean","Standard Deviation","Minimum","Maximum"))
colnames(stats_view) <- c("Day 1", "Day 2")
View(stats_view) #TASK 2: RESULTS

#TASK3
day1_diff = max(day1) - min(day1)
day2_diff = max(day2) - min(day2)

day1_5 = hist(day1, breaks = seq(min(day1), max(day1), length=(day1_diff/5)+1))
day1_5$density = day1_5$counts/sum(day1_5$counts)
day1_10 = hist(day1, breaks = seq(min(day1), max(day1), length=(day1_diff/10)+1))
day1_10$density = day1_10$counts/sum(day1_10$counts)
day1_20 = hist(day1, breaks = seq(min(day1), max(day1), length=(day1_diff/20)+1))
day1_20$density = day1_20$counts/sum(day1_20$counts)
par(mfrow=c(3,1))
plot(day1_5,freq=FALSE,ylab = "Relative Frequency", col='red', main = 'Day 1: Frequency Hist. for 5-sec intervals', xlab='Interarrival Times')
plot(day1_10,freq=FALSE,ylab = "Relative Frequency", col='red', main = 'Day 1: Frequency Hist. for 10-sec intervals',xlab='Interarrival Times')
plot(day1_20,freq=FALSE,ylab = "Relative Frequency", col='red', main = 'Day 1: Frequency Hist. for 20-sec intervals',xlab='Interarrival Times')

day2_5 = hist(day2, breaks = seq(min(day2), max(day2), length=(day2_diff/5)+1))
day2_5$density = day1_5$counts/sum(day1_5$counts)
day2_10 = hist(day2, breaks = seq(min(day2), max(day2), length=(day2_diff/10)+1))
day2_10$density = day2_10$counts/sum(day2_10$counts)
day2_20 = hist(day2, breaks = seq(min(day2), max(day2), length=(day2_diff/20)+1))
day2_20$density = day2_20$counts/sum(day2_20$counts)
par(mfrow=c(3,1))
plot(day2_5,freq=FALSE,ylab = "Relative Frequency", col='blue', main = 'Day 2: Frequency Hist. for 5-sec intervals',xlab='Interarrival Times')
plot(day2_10,freq=FALSE,ylab = "Relative Frequency", col='blue', main = 'Day 2: Frequency Hist. for 10-sec intervals',xlab='Interarrival Times')
plot(day2_20,freq=FALSE,ylab = "Relative Frequency", col='blue', main = 'Day 2: Frequency Hist. for 20-sec intervals',xlab='Interarrival Times')

#TASK 4
# Preprocess stage for day 1:
len = ceiling((max(day1) - min(day1)) / 10)
chisq_obs_1 <- vector(mode = "numeric", length = len)
chisq_int_1 <- vector(mode = "numeric", length = len)
for(i in 1:length(day1)){
  index = floor(day1[i]/10)
  chisq_obs_1[index] = chisq_obs_1[index] + 1
}

for(i in 1:len){
  chisq_int_1[i] = 10 * (i-1) + min(day1)
}

# Preprocess stage for day 2:
len = ceiling((max(day2) - min(day2)) / 10)
chisq_obs_2 <- vector(mode = "numeric", length = len)
chisq_int_2 <- vector(mode = "numeric", length = len)
for(i in 1:length(day2)){
  index = floor(day2[i]/10)
  chisq_obs_2[index] = chisq_obs_2[index] + 1
}

for(i in 1:len){
  chisq_int_2[i] = 10 * (i-1) + min(day2)
}

prob_exp_1 <- dexp(chisq_int_1, rate=1/mean(day1)) # prob for the exp dist. variable for the values
chisq.test(chisq_obs_1, p=prob_exp_1,rescale.p = TRUE)

prob_exp_2 <- dexp(chisq_int_2, rate=1/mean(day2)) # prob for the exp dist. variable for the values
chisq.test(chisq_obs_2, p=prob_exp_2,rescale.p = TRUE)

#TASK 5
par(mfrow=c(2,1))
QQ_day1 = qexp(ppoints(length(day1)))[order(order(day1))]
QQ_day2 = qexp(ppoints(length(day2)))[order(order(day2))]
plot(day1,QQ_day1, main = 'Day 1: Quantile-Quantile Plot', xlab='Sample Quantiles', ylab='Theoretical Quantiles')
plot(day2,QQ_day2, main = 'Day 2: Quantile-Quantile Plot', xlab='Sample Quantiles', ylab='Theoretical Quantiles')

#TASK 6

day1_obs_times <- numeric(length = length(day1))
day1_obs_times[1] = day1[1]
for (i in 2:length(day1)) {
  day1_obs_times[i] <- day1_obs_times[i-1] + day1[i]
}

day2_obs_times <- numeric(length = length(day2))
day2_obs_times[1] = day2[1]
for (i in 2:length(day2)) {
  day2_obs_times[i] = day2_obs_times[i-1] + day2[i]
}

par(mfrow=c(2,1))
plot(1:length(day1_obs_times), day1_obs_times, main='Observation Times: Day 1', ylab='Observation Time', xlab='Customer Number')
plot(1:length(day2_obs_times), day2_obs_times, main='Observation Times: Day 2', ylab='Observation Time', xlab='Customer Number')

#TASK 7

acf_day1 <- acf(day1_obs_times, lag.max = 2, plot=FALSE)
acf_day2 <- acf(day2_obs_times, lag.max = 2, plot=FALSE)

plot(acf_day1, main = "Autocorrelation Test: Day 1", xlab='Lag', ylab='Autocorrelation coefficient')
plot(acf_day2, main = "Autocorrelation Test: Day 2", xlab='Lag', ylab='Autocorrelation coefficient')

corr_day1 <- acf_day1$acf[2:length(acf_day1$acf)]
corr_day2 <- acf_day2$acf[2:length(acf_day2$acf)]

Lag1 <- c(acf_day1$acf[2],acf_day2$acf[2])
Lag2 <- c(acf_day1$acf[3],acf_day2$acf[3])

dat <- data.frame(Lag1, Lag2, row.names = c("Day 1","Day 2"))
colnames(dat) <- c("Lag 1", "Lag 2")
View(dat)
