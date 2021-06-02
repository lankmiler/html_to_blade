import argparse
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup


parser = argparse.ArgumentParser(description='Parse multiple html files and export them with layout as .blade files.')

parser.add_argument('--files', metavar='files', type=str, help='Files separator. Should be separated by comma.')
parser.add_argument('--layout', metavar='layout', type=str, help='layout file')
parser.add_argument('--contentclass', metavar='contectclass', type=str, help='Content class of child tags')
parser.add_argument('--contentid', metavar='contectid', type=str, help='Content id of child tags')
parser.add_argument('--output_dir', metavar='output_dir', type=str, help='output directory to save files')

layout = None

all_args = parser.parse_args()

files = all_args.files.split(',')

for item in files:
	with open(item, 'r') as html_file:
		soup = BeautifulSoup(html_file.read(), 'html.parser')
		if all_args.contentid:
			content = soup.find("div", {"id": all_args.contentclass})
			divsoup = BeautifulSoup(str(content), 'html.parser')
			print(divsoup.prettify())
			sys.exit(0)
		elif all_args.contentclass:
			content = soup.find("div", {"class": all_args.contentclass})
			divsoup = BeautifulSoup(str(content), 'html.parser')
			print(divsoup.prettify())
			sys.exit(0)
		else:
			print('No selector given!')
			sys.exit(0)
