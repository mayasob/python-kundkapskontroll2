import pandas as pd
import sqlite3

# Anslut till SQLite-databasen
con = sqlite3.connect('friends.db')

# Läs in CSV-filen till en pandas DataFrame
df = pd.read_csv('archive/friends_episodes_v3.csv')

# Visa de första raderna för att kontrollera att data har laddats korrekt
df.head()

# Omvandla 'Season'-kolumnen till heltal
df['Season'] = df['Season'].astype(int)

# Konvertera episodeti till små bokstäver
df['Episode_Title'] = df['Episode_Title'].str.lower()

print(df.columns)

# Skriv DataFrame till SQLite-databasen
df.to_sql('episodes', con, if_exists='replace', index=False)

# Visa de 5 bästa avsnitten baserat på antal röster (Votes)
top_5_votes = df.nlargest(5, 'Votes')

# Visa de 5 sämsta avsnitten baserat på antal röster (Votes)
bottom_5_votes = df.nsmallest(5, 'Votes')

print("De fem bästa avsnitten baserat på antal röster:")
print(top_5_votes[['Episode_Title', 'Votes']])

print("\nDe fem sämsta avsnitten baserat på antal röster:")
print(bottom_5_votes[['Episode_Title', 'Votes']])

# Visa de 5 bästa avsnitten baserat på antal stjärnor (Stars)
top_5_stars = df.nlargest(5, 'Stars')

# Visa de 5 sämsta avsnitten baserat på antal stjärnor (Stars)
bottom_5_stars = df.nsmallest(5, 'Stars')

print("De fem bästa avsnitten baserat på antal stjärnor:")
print(top_5_stars[['Episode_Title', 'Stars']])

print("\nDe fem sämsta avsnitten baserat på antal stjärnor:")
print(bottom_5_stars[['Episode_Title', 'Stars']])

import logging

# Konfigurera loggfilen
logging.basicConfig(filename='process_log.log', level=logging.INFO)

try:
    # Skriv DataFrame till SQLite-databasen
    df.to_sql('episodes', con, if_exists='replace', index=False)
    logging.info("Data har sparats till databasen framgångsrikt.")
except Exception as e:
    logging.error(f"Ett fel uppstod: {e}")
    

import unittest

class TestDataProcessing(unittest.TestCase):
    def test_column_existence(self):
        df = pd.read_csv('archive/friends_episodes_v3.csv')
        self.assertIn('Episode_Title', df.columns)
        self.assertIn('Votes', df.columns)
        self.assertIn('Stars', df.columns)

# Kör testerna manuellt
suite = unittest.TestLoader().loadTestsFromTestCase(TestDataProcessing)
unittest.TextTestRunner().run(suite)
