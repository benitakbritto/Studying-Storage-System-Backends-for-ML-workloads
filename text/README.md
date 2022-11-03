# Clean Dataset

`-c skips the character which are not in the charset`

iconv -c --from-code=UTF-8 --to-code=UTF-8 twitter_sentiment_dataset.csv > twitter_new.csv