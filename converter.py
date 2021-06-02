import argparse
import sys
import re

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
parser.add_argument('--extra', metavar='extra', type=str, help='Extra content to be inserted to layout')


layout = None

all_args = parser.parse_args()

files = all_args.files.split(',')

for item in files:
	with open(item, 'r') as html_file:
		all_content = BeautifulSoup(html_file.read(), 'html.parser')
		if all_args.contentid:
			content = all_content.find("div", {"id": all_args.contentclass})
			divsoup = BeautifulSoup(str(content), 'html.parser')
			for elm in content.find_next_siblings():
			    elm.extract()
			content.extract()

			content = '''
@extends('layouts.front')

@section('title', '{}')

@section('content')
'''.format(title) + content.prettify() + ''' @endsection'''
			f = open('./output/' + item.split('.')[0] + '.blade.php', 'a')
			f.write(content)
			f.close()
			

			if not layout:
				layout = all_content
				body = layout.find('body')
				body.append("@yield('content')")
				layout_str = layout.prettify()
			
				if all_args.extra:
					pos = layout_str.find('</body>')
					new_layout = layout_str[:pos] + all_args.extra + layout_str[pos:]
					layout = new_layout

					f = open("layout.blade", "a")
					f.write(str(layout))
					f.close()

			sys.exit(0)
		elif all_args.contentclass:
			title = all_content.find('title').text
			content = all_content.find("div", {"class": all_args.contentclass})
			divsoup = BeautifulSoup(str(content), 'html.parser')
			for elm in content.find_next_siblings():
			    elm.extract()
			content.extract()

			content = '''
@extends('layouts.front')

@section('title', '{}')

@section('content')
'''.format(title) + content.prettify() + ''' @endsection'''
			f = open('./output/' + item.split('.')[0] + '.blade.php', 'a')
			f.write(content)
			f.close()			

			if not layout:
				layout = all_content
				body = layout.find('body')
				body.append("@yield('content')")
				layout_str = layout.prettify()
			
				if all_args.extra:
					pos = layout_str.find('</body>')
					new_layout = layout_str[:pos] + all_args.extra + layout_str[pos:]
					layout = new_layout

					f = open("./output/layout.blade.php", "a")
					f.write(str(layout))
					f.close()
				#print(str(body.encode(formatter='html5')))
			#sys.exit(0)
		else:
			print('No selector given!')
			sys.exit(0)
