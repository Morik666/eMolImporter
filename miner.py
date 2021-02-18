from datetime import datetime
from glob import glob
from configs import *
from order import *

def read_order(path):
	from PyPDF2 import PdfFileReader
	f = open(path, 'rb')
	pdf = PdfFileReader(f)
	order = Order()
	item = Item()
	mode = ItemsReadingMode.Pasive
	msg = ''

	for i in range(pdf.getNumPages()):
		txt = pdf.getPage(i).extractText().split('\n')
		breakpoint()
		if not order.PO and txt[3] == 'Purchase Order #':
			order.PO = txt[4]
		
		for j, line in enumerate(txt):
			if line[:4] == 'ATTN' and len(order.Reciever) < 2:
				order.Reciever = line[6:-12].strip()
				order.Ref = txt[i+1]
				order.EndUser = txt[i+2]
				order.ShippingAddress += [line, txt[i+1], txt[i+2]]
				mode = ItemsReadingMode.ShippingAddress
			elif mode == ItemsReadingMode.ShippingAddress and line == 'Customer Name':
				mode = ItemsReadingMode.Pasive
			elif mode == ItemsReadingMode.ShippingAddress:
				order.ShippingAddress.append(line)
			elif mode == ItemsReadingMode.Pasive and line == 'Catalog ID':
				mode = ItemsReadingMode.CatalogID
			elif mode == ItemsReadingMode.CatalogID and line[:2] == 'EN':
				item.CatalogID = line
				mode = ItemsReadingMode.PackSize
			elif mode == ItemsReadingMode.PackSize and line[-2:] == 'mg':
				item.PackSize = line
				mode = ItemsReadingMode.Price
			elif mode == ItemsReadingMode.Price and line[:1] == '$':
				item.Price = line
				order.Items.append(item)
				item = Item()
				mode = ItemsReadingMode.CatalogID
			elif line == 'Total':
				break
	
	log = open(LOG_PATH, 'a+')
	if msg:
		log.write(f'{datetime.now()}|"{path}"|Error! {msg}\n')
	log.write(f'{datetime.now()}|"{path}"|{str(order)}\n')
	log.close()
	return order

def mine():
	files = glob(os.path.join(REACTOR_PATH, '*.pdf'))
	orders = []
	for file in files:
		orders.append(read_order(file))