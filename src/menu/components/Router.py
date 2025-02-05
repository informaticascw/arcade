from util.constants import Constants

class Router:
	"""Menu pages routing module
	Creates a central control point for navigating through different menu pages

	Args:
		pages (list): List of pages that exist within the menu
		
	"""
	def __init__(self, pages:dict) -> None:
		self.pages:dict = pages

		nameSet = set(map(lambda x : x, self.pages))
		print(f"{Constants.CNSL_INFO}[ROUTER] Pages: {nameSet}{Constants.CNSL_RESET}")
  
		if "main" not in pages.keys():
			raise Exception('No "main" page found')

		self.mainPage: object = pages["main"]
		self.current: object = self.mainPage
		self.previous: object = None
		print(f"{Constants.CNSL_INFO}[ROUTER] Redirected to menu: [{self.current.name}]{Constants.CNSL_RESET}")
		
	def redirect(self, pageName:str) -> None:
		"""Redirect the user to a new menu screen

		Args:
			page (str): The page name to redirect the user to
		"""
		self.previous = self.current
		self.current = self.pages[pageName]
		
		print(f"{Constants.CNSL_INFO}[ROUTER] Redirected to menu: [{self.current.name}]{Constants.CNSL_RESET}")
		
	def previous(self) -> None:
		"""Redirect the user to the previous menu scnreen"""
		return self.redirect(self.previous)