from requests import Session
from bs4 import BeautifulSoup


login = 'velichko_ivan'
password = 'Asdq123455'
snippet_data = {
    "title": "Titlednbfjdbhdbfhdbf",
    "code": "Contentfjggjhjdngjdn contentosqosoqsoqsoqs contentjwnqimomsxxncjejeneend",
    "linenos": False,
    "language": "text",
    "style": "monokai"
}

session = Session()
response = session.get(url='http://31.31.203.230/api-auth/login/')
soup = BeautifulSoup(response.text, features="html.parser")
token = soup.find('input', {'name': 'csrfmiddlewaretoken'})

# Authorization
login_data = dict(username=login, password=password, csrfmiddlewaretoken=token.attrs['value'])
post_auth = session.post(url='http://31.31.203.230/api-auth/login/', data=login_data)

# Check authorization
assert post_auth.history[0].cookies['csrftoken'], 'You are not logged in...'

# Create snippet
post_snippet = session.post(url='http://31.31.203.230/snippets/', data=snippet_data,
                            headers={"X-CSRFTOKEN": post_auth.history[0].cookies['csrftoken']})
assert post_snippet.status_code == 201, 'Snippet not created...'

# Get snippet by url
snippet_json = post_snippet.json()
snippet_url = snippet_json['url']
get_snippet = session.get(url=snippet_url)
assert get_snippet.status_code == 200, 'Unable to get snippet...'

# Make sure it's yours
assert snippet_json['owner'] == login, 'You are not the owner...'

# Log out
get_logout = session.get(url='http://31.31.203.230/api-auth/logout/')
assert get_logout.status_code == 200, 'You have not logged out...'
