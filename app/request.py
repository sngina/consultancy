import urllib.request, json
from  .models import Quotes  

def get_quotes():
    get_quotes_url = 'http://quotes.stormconsultancy.co.uk/random.json' 
    with urllib.request.urlopen(get_quotes_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)
        author = get_quotes_response.get('author')
        quote = get_quotes_response.get("quote")

        quote_object = Quotes(author , quote)
        return quote_object
