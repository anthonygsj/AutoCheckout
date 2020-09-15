from selenium import webdriver
from selenium.webdriver.support.ui import Select
from params import keys
import time

class AutoCheckout(object):

	def __init__(self, keys):
		self.keys = keys
		self.shop_url = 'https://www.supremenewyork.com/shop/all/'
		self.browser = webdriver.Chrome('./chromedriver')

		if self.keys['restock']:
			self.add_to_cart()
		else:
			self.await_drop()

	def await_drop(self):
		drop_time_hour_utc = 15

		while time.gmtime().tm_hour != drop_time_hour_utc:
			time.sleep(1)
			print('awaiting drop - 11AM EST')

		self.add_to_cart()

	def add_to_cart(self):
		self.browser.get('{}{}/'.format(self.shop_url, self.keys['category']))\

		product_element = None

		while not product_element:
			try:
				product_element = self.browser.find_element_by_xpath('//a[text() = \'{}\']'.format(self.keys['product-name']))
			except:
				print('Shop page is still loading, trying again..')
				time.sleep(0.5)
		product_element.click()

		time.sleep(0.5)

		color_element = None

		while not color_element:
			try:
				color_element = self.browser.find_element_by_xpath('//button[@data-style-name=\'{}\']'.format(self.keys['product-style']))
			except:
				print('Product page still loading, trying again..')
				time.sleep(0.5)

		color_element.click()

		time.sleep(0.3)

		try:
			Select(self.browser.find_element_by_xpath('//*[@id="s"]')).select_by_visible_text(self.keys['product-size'])
		except:
			print('Product has no size options or is selected size is not available: [{} - {} - {}]'.format(self.keys['product-name'],self.keys['product-style'], self.keys['product-size']))

		time.sleep(0.3)

		cart_element = None

		while not cart_element:
			try:
				cart_element = self.browser.find_element_by_xpath('//input[@value=\"add to cart\"]')
			except:
				print('Item is not currently available, checking for restock...')
				self.browser.refresh()
				time.sleep(3)

		cart_element.click()

		time.sleep(0.3)

		checkout_element = None
		while not checkout_element:
			try:
				checkout_element = self.browser.find_element_by_link_text('checkout now')
			except:
				print('checkout button not yet shown, trying again..')
				time.sleep(0.5)
		checkout_element.click()

		self.checkout()

	def checkout(self):
		namefield = None
		while not namefield:
			try:
				namefield = self.browser.find_element_by_xpath('//*[@id="order_billing_name"]')
			except:
				print('Checkout page not yet loaded, trying again..')
				time.sleep(0.5)
		namefield.send_keys(self.keys['name'])
		self.browser.find_element_by_xpath('//*[@id="order_email"]').send_keys(self.keys['email'])
		self.browser.find_element_by_xpath('//*[@id="order_tel"]').send_keys(self.keys['telephone'])
		self.browser.find_element_by_xpath('//*[@id="bo"]').send_keys(self.keys['billing_address'])
		self.browser.find_element_by_xpath('//*[@id="oba3"]').send_keys(self.keys['address_2'])
		self.browser.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(self.keys['zip'])
		self.browser.find_element_by_xpath('//*[@id="rnsnckrn"]').send_keys(self.keys['card_num'])
		self.browser.find_element_by_xpath('//*[@id="orcer"]').send_keys(self.keys['ccv'])
		Select(self.browser.find_element_by_xpath('//*[@id="credit_card_month"]')).select_by_index(self.keys['month'] - 1)
		Select(self.browser.find_element_by_xpath('//*[@id="credit_card_year"]')).select_by_visible_text(str(self.keys['year']))
		self.browser.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label/div/ins').click()
		self.browser.find_element_by_xpath('//*[@id="pay"]/input').click()



if __name__ == '__main__':
	session = AutoCheckout(keys)
