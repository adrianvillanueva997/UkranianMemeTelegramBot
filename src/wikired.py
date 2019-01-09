import json
import os
import markovify
from gtts import gTTS
import src.config as config


class Wikired:

    def text_to_speech(self):
        tweet = self.wiki_red()
        tts = gTTS(text=tweet, lang='es')
        tts.save('ukranian_audio.mp3')
        os.system("ukranian_audio.mp3")
        return tweet

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
        """Special thanks to RedMSR for giving me his tweets. Using markov chains, this function makes a new tweet based on his tweets
            Parameters
            ----------
            args : None

            Returns
            -------
            String
                Tweet

            """
        try:
            model_json = self.read_json(r'src/models/model_wikired.json')
            reconstituted_model = markovify.NewlineText.from_json(model_json)
            tweet = reconstituted_model.make_short_sentence(280)
            if tweet == None:
                return "try again later :)"
            else:
                self.insertTweetQuery(tweet)
                return tweet
        except Exception as e:
            print(e)

    def ukrania_today(self):
        """Special thanks to antena3 for giving me their tweets. Using markov chains, this function makes a new tweet based on his tweets
            Parameters
            ----------
            args : None

            Returns
            -------
            String
                Tweet

            """
        try:
            model_json = self.read_json(r'src/models/model_antena3.json')
            reconstituted_model = markovify.NewlineText.from_json(model_json)
            tweet = reconstituted_model.make_short_sentence(280)
            if tweet == None:
                return "try again later :)"
            else:
                return tweet
        except Exception as e:
            print(e)

    def ukranian(self):
        """Special thanks to Ukranian kalvos for giving me their chats. Using markov chains, this function makes a new tweet based on his tweets
            Parameters
            ----------
            args : None

            Returns
            -------
            String
                Tweet

            """
        try:
            model_json = self.read_json(r'src/models/model_ukranian.json')
            reconstituted_model = markovify.NewlineText.from_json(model_json)
            tweet = reconstituted_model.make_short_sentence(280)
            if tweet is None:
                return "try again later :)"
            else:
                return tweet
        except Exception as e:
            print(e)

    def wiki_bab(self):
        """Special thanks to Wikibab for giving me his tweets. Using markov chains, this function makes a new tweet based on his tweets
             Parameters
             ----------
             args : None

             Returns
             -------
             String
                 Tweet

             """
        try:
            model_json = self.read_json(r'/home/Xiao/telegrambot/telegramBot/src/models/model_wikibab.json')
            reconstituted_model = markovify.NewlineText.from_json(model_json)
            tweet = reconstituted_model.make_short_sentence(280)
            print(tweet)
            if tweet == None:
                return "try again later :)"
            else:
                self.insertTweetQuery(tweet)
                return str(tweet)
        except Exception as e:
            print(e)

    def tts(self, string):
        try:
            tts = gTTS(text=str(string), lang='es')
            tts.save('ukranian_audio.mp3')
            os.system("ukranian_audio.mp3")
        except Exception as e:
            print(e)

    def read_json(self, json_file):
        try:
            with open(json_file) as file:
                data = json.loads(file.read())
                print('reading json!')
                return data
        except Exception as e:
            print(e)
