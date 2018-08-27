from recipemd.data import RecipeParser,Recipe,Ingredient

def extract(url,soup):
	if not 'chefkoch.de' in url:
		return

	# title
	title = soup.find('h1', attrs={'class': 'page-title'}).text
	if title == 'Fehler: Seite nicht gefunden' or title == 'Fehler: Rezept nicht gefunden':
		raise ValueError('No recipe found, check URL')
	# summary
	summary = soup.find('div', attrs={'class': 'summary'}).text
	# servings and tags
	servings= soup.find('input', attrs={'id':'divisor'}).attrs['value']
	tags=['{} Portion{}'.format(servings, 'en' if int(servings) > 1 else '')]

	tagcloud=soup.find('ul', attrs={'class':'tagcloud'})
	for tag in tagcloud.find_all('a'):
		tags.append(tag.text)
	# ingredients
	table = soup.find('table', attrs={'class': 'incredients'})
	rows = table.find_all('tr')

	ingreds=[]
	for row in rows:
		cols = row.find_all('td')
		cols = [s.text.strip() for s in cols]
		unit, amount = RecipeParser.parse_amount(cols[0])
		ingreds.append(Ingredient(name=cols[1],amount=amount,unit=unit))
	# instructions
	instruct = soup.find('div', attrs={'id': 'rezept-zubereitung'}).text  # only get text
	instruct = instruct.strip()  # remove leadin and ending whitespace
	# write to file
	return Recipe(title=title, ingredients=ingreds, instructions=instruct, description=summary, tags=tags)
