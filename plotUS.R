# EnsurePackage(x) - Installs and loads a package if necessary
EnsurePackage<-function(x)
{
  x <- as.character(x);
  if (!require(x,character.only=TRUE))
  {
    install.packages(pkgs=x,repos="http://cran.r-project.org");
    require(x,character.only=TRUE);
  }
}

# PrepareMap() - Uses EnsurePackage() to load the necessary packages for plotting the US map
PrepareMap <- function()
{
  EnsurePackage("ggplot2");
  EnsurePackage("maps");
  EnsurePackage("RColorBrewer");
}

plotUSstates <- function()
{
  PrepareMaps();
  #load us map data
  states <- map_data("state");
  state.info <- data.frame(state.center, state.abb);
  state.info <- subset(state.info, !state.abb %in% c("AK", "HI"));
  #load the sentiment score per state
  sent_scores <- read.csv("sent_scores",stringsAsFactors=FALSE);
  #add sentiment scores to states
  states$score <- sent_scores$sentiment[match(states$region, sent_scores$state)];
  #cutting the state scores into bins
  states$bin <- cut(states$score, 5);
  states$bin <-factor(
    states$bin, labels=c('neg','neg/neutral','neutral','pos/neutral','pos'));
  #making sure the latitudes and longitudes do not show
  theme_opts <- list(theme(panel.grid.minor = element_blank(),
                           panel.grid.major = element_blank(),
                           panel.background = element_blank(),
                           plot.background = element_rect(fill="#e6e8ed"),
                           panel.border = element_blank(),
                           axis.line = element_blank(),
                           axis.text.x = element_blank(),
                           axis.text.y = element_blank(),
                           axis.ticks = element_blank(),
                           axis.title.x = element_blank(),
                           axis.title.y = element_blank(),
                           plot.title = element_text(size=22)));
  #plot all states with ggplot
  p <- ggplot(states, aes(x=long, y=lat));
  p <- p + 
    geom_polygon(aes(long, lat, group = group, fill=bin),colour="white" ) + 
    labs(title="Relative sentiment of the US states") + 
    guides(fill=guide_legend(title="scores")) +
    geom_text(data = state.info, aes(x = x, y = y, label = state.abb), colour = 'black',size=4);
  p + scale_fill_brewer(palette="Blues") + 
    theme_opts;
  ggsave("sentiment_plot.png",width=16.510,height=10.668,units="cm")
}

plotUSstates()
