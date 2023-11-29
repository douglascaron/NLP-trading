from colorama import init, Fore
from openbb_terminal.sdk import openbb
openbb.login(token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoX3Rva2VuIjoicFl6TzVTVWNBZndyQURTYWxHSkRNZDhDSUpFQ0ZUdlBaalFyQUgxcCIsImV4cCI6MTczMjg3ODk1Mn0.eV0vwO20G_x7JBYCiixLepGoTgKTfqLqHY-defBqOMk", silent=True)

openbb.keys.finnhub(key= "cljhsnhr01qok8f3hqggcljhsnhr01qok8f3hqh0", persist=True, show_output=False)
openbb.keys.fmp(key= "060dbe078f74965df9ad070d16ffde5f", persist=True, show_output=False)
openbb.keys.news(key= "917a6589d0634bbf8082710cd995e240", persist=True, show_output=False)

# print(openbb.stocks.quote("SPY"))

