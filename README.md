This program outputs a plot which displays the sentiment scores of the US states.</br>
The sentiments scores are based on an analysis of the tweets coming from each US state.</br>
</br>
In order to download live tweets one has to manually supply some credentials in the file twitterKeys.txt.</br>
To obtain the Twitter credentials do the following:</br>
</br>
* Create a twitter account if you do not already have one.
* Go to https://dev.twitter.com/apps and log in with your twitter credentials.
* Click "create an application"
* Fill out the form and agree to the terms. Put in a dummy website if you don't have one you want to use.
* On the next page, scroll down and click "Create my access token"
* Copy your "Consumer key" and your "Consumer secret" into twitterKeys.txt
* Click "Create my access token."
* Copy your "Access token" and your "Access secret" into twitterKeys.txt

After the credentials are se in twitterKeys.txt the program can be run by running the shell get_sentiment.sh (open a terminal and enter "sh get_sentiment.sh").</br>
A sentiment plot of the US states will be shown and saved as "sentiment_plot.png".

TODO:

[-] Not only select tweets based on the 'place' field but also the geolocation in the 'coordinates' field (see https://dev.twitter.com/docs/platform-objects/tweets)

