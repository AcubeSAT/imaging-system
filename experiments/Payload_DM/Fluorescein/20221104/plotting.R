# Load libraries
library(dplyr)
library(tidyverse)
library(ggplot2)
library(RColorBrewer)
library(wesanderson)

# Set paths
data_path <- 
data_filename <- 

# Set wd
setwd(data_path)

# Load data
data <- read.csv(file.path(data_path, file.path(data_filename, "csv", fsep = ".")), header = TRUE, stringsAsFactors = FALSE)

# Calculate statistics
data_summary <- function(data, varname, groupnames){
  require(plyr)
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm = TRUE),
      sd = sd(x[[col]], na.rm = TRUE))
  }
  data_sum<-ddply(data, groupnames, .fun = summary_func,
                  varname)
  data_sum <- rename(data_sum, c("mean" = varname))
  return(data_sum)
}

data_stats <- data_summary(data, varname = c("Mean"),
                                          groupnames = c("Concentration", "Area"))

# Choose color palettes
gp1 <- wes_palettes$Darjeeling1
gp2 <- wes_palettes$Darjeeling2

# Plotting
ggplot(data_stats, aes(x = as.numeric(Concentration), y = as.numeric(Mean)))+
    geom_point(color = "#87c487", size = 6) +
    # geom_smooth() +
    theme_bw(base_size = 20) +
    # geom_errorbar(aes(ymin=Mean-sd, ymax=Mean+sd), width=.2,
    # position=position_dodge(.01)) +  
    labs(x = "Concentration (uM)", y = "Brightness (a.u.)") +
    theme(strip.text = element_text(face = "bold",
                                  hjust = 0, size = 20),
        strip.background = element_rect(fill = "#FFFFFF"))


ggsave("20221104_CK_Fluorescein.pdf")