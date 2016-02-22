data1 <- read.csv('csv_output/second_first.csv')
data2 <- read.csv('csv_output/third_first.csv')
data3 <- read.csv('csv_output/third_second.csv')

data  <- data.frame(id = 1:(nrow(data1) + nrow(data2) + nrow(data3)))

for (name in names(data1)) 
    if (name != 'nodeid') {
    tmp <- c(data1[[name]], data2[[name]], data3[[name]])
    data[name] <- tmp
}
names(data) <- c("id", "nbPegonets", "nodesize", "nbInstances", "nbInstancesHavingType", "nbInstancesRedirected", "infoboxLength")

lm.r = lm(nbPegonets ~ (nbInstances + nbInstancesHavingType + nbInstancesRedirected + infoboxLength)^2, data = data)
summary(lm.r)
