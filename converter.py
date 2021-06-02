import argparse
import sys
import os
import shutil

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup


parser = argparse.ArgumentParser(description='Parse multiple html files and export them with layout as .blade files.')

parser.add_argument('--directory', metavar='directory', type=str, help='directory')
#parser.add_argument('--contentclass', metavar='contectclass', type=str, help='Content class of child tags')
parser.add_argument('--contentid', metavar='contectid', type=str, help='Content id of child tags')
parser.add_argument('--extra', metavar='extra', type=str, help='Extra content to be inserted to layout')
parser.add_argument('--ignore', metavar='ignore', nargs='+',  help='Ignore files. Just convert to blade')

layout = None

all_args = parser.parse_args()
directory = all_args.directory


# Cleanup old
for root, dirs, files in os.walk('./output/'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

for root, dirs, files in os.walk(directory):
	for f in files:
		
		if 'html' in f:
			with open(root + '/' + f, 'r') as current_html:
				filebasename = f.rsplit('.')[0]
				if all_args.ignore:
					if f in all_args.ignore:
						f = open('./output/{}.blade.php'.format(filebasename), 'a')
						f.write(current_html.read())
						f.close()
						continue
				all_content = BeautifulSoup(current_html.read(), 'html.parser')
				title = all_content.find('title').text
				if all_args.contentid:
					content = all_content.find("div", {"id": all_args.contentid})
					if content is None:
						content = all_content.find("div", {"class": all_args.contentid})
					divsoup = BeautifulSoup(str(content), 'html.parser')
					for elm in content.find_next_siblings():
					    elm.extract()
					content.extract()

					content = '''
		@extends('layouts.front')

		@section('title', '{}')

		@section('content')
		'''.format(title) + content.prettify() + ''' @endsection'''
					f = open('./output/' + filebasename + '.blade.php', 'a')
					f.write(content)
					f.close()
					

					# if not layout:
					# 	layout = all_content
					# 	body = layout.find('body')
					# 	body.append("@yield('content')")
					# 	layout_str = layout.prettify()
					
					# 	if all_args.extra:
					# 		pos = layout_str.find('</body>')
					# 		new_layout = layout_str[:pos] + all_args.extra + layout_str[pos:]
					# 		layout = new_layout

					# 		f = open("./output/front.blade", "a")
					# 		f.write(str(layout))
					# 		f.close()
