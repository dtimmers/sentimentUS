#!/bin/hash

while true; do
    echo "Do you want to download new Tweets?(y/n)";
    read -p "(If tweets.txt does not exists yet you have to answer y)" yn;
    case $yn in
        [Nn]* ) 
		echo "We will now visualize the sentiments of the US states";break;;
        [Yy]* ) 
		echo "We will download fresh Twitter data which takes 20 minutes.";
  		echo "This will gives us a decent sample.";
		echo "Have a little break while we are downloading the tweets";
		python twitterstream.py tweets.txt;
		echo "Download completed";
		echo "We will now visualize the sentiments of the US states";
		break;;
        * ) 
		echo "Please answer y or n.";;
    esac
done

python state_sentiment.py AFINN-111.txt tweets.txt;
R CMD BATCH plotUS.R;
xdg-open sentiment_plot.png;


