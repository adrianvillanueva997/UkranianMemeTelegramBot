import telegramBot.src.config as config
import markovify


class Wikired():

    def insertTweetQuery(self, tweet):
        """Inserts tweet in database
            Parameters
            ----------
            args : String
                tweet
            Returns
            -------
            None

            """
        try:
            with config.engine.connect() as con:
                tweet.replace('\'', '\'\'')
                tweet.replace('%', '%%')
                tweet.replace('\"', '\"\"')
                con.execute('INSERT INTO TwitterBot.Wikired_Query (Wikired_Query.TWEET) values (\"' + tweet + '\")')
                print('tweet insertado: ' + tweet)
        except Exception as e:
            print(e)

    def wiki_red(self):
        """Especial thanks to RedMSR for giving me his tweets. Using markov chains, this function makes a new tweet based on his tweets
            Parameters
            ----------
            args : None

            Returns
            -------
            String
                Tweet

            """
        try:
            con = config.engine.connect()
            tweets = con.execute('SELECT Text FROM Wikired_Data')
            tweet_list = []
            for tweet in tweets:
                tweet_list.append(str(tweet['Text']))
            text_model = markovify.NewlineText(tweet_list, state_size=3)
            model_json = text_model.to_json()
            reconstituted_model = markovify.NewlineText.from_json(model_json)
            tweet = reconstituted_model.make_short_sentence(280)
            # print(tweet)
            self.insertTweetQuery(tweet)
            return tweet
        except Exception as e:
            print(e)

    def wiki_bab(self):
        """Especial thanks to Wikibab for giving me his tweets. Using markov chains, this function makes a new tweet based on his tweets
             Parameters
             ----------
             args : None

             Returns
             -------
             String
                 Tweet

             """
        try:
            con = config.engine.connect()
            tweets = con.execute('SELECT Text FROM Wikibab_Data')
            tweet_list = []
            for tweet in tweets:
                tweet_list.append(str(tweet['Text']))
            text_model = markovify.NewlineText(tweet_list, state_size=2)
            model_json = text_model.to_json()
            reconstituted_model = markovify.NewlineText.from_json(model_json)
            tweet = reconstituted_model.make_short_sentence(280)
            print(tweet)
            while tweet == None:
				tweet = reconstituted_model.make_short_sentence(280)

            self.insertTweetQuery(tweet)
            return tweet


        except Exception as e:
            print('excepcion')
            print(e)
