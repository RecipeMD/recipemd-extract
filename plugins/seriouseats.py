from recipemd.data import Recipe,Ingredient

def extract(url,soup):
	if not 'seriouseats.com' in url:
		return

	# title
	title = soup.find('h1',attrs={'class':'title recipe-title'}).text.strip()

	# summary
	summary=''

	summaryPars=soup.find('div',attrs={'class':'recipe-introduction-body'}).find_all('p')

	for par in summaryPars:
		if not 'caption' in par.attrs.get('class',[]):
			summary = summary + par.text + '\n\n'
	summary=summary.strip()

	# servings and tags
	servings=soup.find('span',attrs={'class':'info yield'}).text

	tags=[servings]

	for tag in soup.find_all('a',attrs={'class':'tag'}):
		tags.append(tag.text)

	# ingredients
	ingredients=[]

	for ingred in soup.find_all('li',attrs={'class':'ingredient'}):
		ingredients.append(Ingredient(name=ingred.text))

	# instructions
	instructions=''

	for step in soup.find_all('li',attrs={'class':'recipe-procedure'}):
		stepNumber = step.find('div',attrs={'class':'recipe-procedure-number'}).text.strip()
		stepInstr = step.find('div',attrs={'class':'recipe-procedure-text'}).text.strip()

		instructions = instructions + stepNumber + ' ' + stepInstr + '\n'
	instructions=instructions.strip()

	return Recipe(title=title,ingredients=ingredients,instructions=instructions,description=summary,tags=tags)
