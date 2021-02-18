from enum import Enum

class Order:
	def __init__(self):
		self.PO = ''
		self.Ref = ''
		self.Reciever = ''
		self.ShippingAddress = []
		self.EndUser = ''
		
		self.Items = []
	
	def __str__(self):
		items = '['
		for item in self.Items:
			items += str(item)
		items += ']'
		return '{' + f'PO: {self.PO}, Ref: {self.Ref}, Reciever: {self.Reciever}, ShippingAddress: {self.ShippingAddress}, EndUser: {self.EndUser}, Items: {items}' + '}'

class ItemsReadingMode(Enum):
	Pasive = 0
	ShippingAddress = 1
	CatalogID = 2
	PackSize = 3
	Price = 4

class Item:
	def __init__(self):
		self.CatalogID = ''
		self.PackSize = ''
		self.Price = ''
	
	def __str__(self):
		return '{' + f'CatalogID: {self.CatalogID}, PackSize: {self.PackSize}, Price: {self.Price}' + '}'