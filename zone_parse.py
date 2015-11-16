#-*- coding: utf-8 -*-
import bs4
from bs4 import BeautifulSoup
import re
import os
import sys 
reload( sys ) 
sys.setdefaultencoding('utf-8')
def re_taotao(html):
	comment_c_re = re.compile(r':(.*?):(.*?):',re.S)
	comment_r_re = re.compile(r':(.*?):(/d.*?)',re.S)
	soup = BeautifulSoup(html,from_encoding="utf-8")
	items = soup.select('.feed')
	taotaos = []
	for item in items:
		taotao = item.select('pre')
		taotao_dic = {}
		content = ''
		zhuan = ''
		for i in taotao:
			for string in i.stripped_strings:
				if (string == None):
					continue
				content += string
		if(item.select('.rt_forward_btn')):
			zhuan = item.select('.rt_forward_btn')[0].string
		else:
			zhuan = 'None'
		zan = item.select('.qz_like_btn')[1].string
		taotao_dic['content'] = content
		taotao_dic['zhuan'] = zhuan
		taotao_dic['zan'] = zan
		comments = item.select('.comments_list')
		if(not comments):
			continue
		comments_c_r = []
		for comment in comments[0].ul:
			comment_c = ''
			spans = comment.select('.comments_content')[0].select('span')
			for span in spans:
				for string in span.stripped_strings:
					if(string != None and type(span.previous_sibling) != bs4.element.Tag and span.previous_sibling != None):
						if(span.previous_sibling.strip() == ':'):
							comment_c += string
			print comment_c
			comment_c_dic = {}
			comment_c_dic['nickname'] = comment.select('.comments_content')[0].select('.nickname')[0].string
			comment_c_dic['content'] = comment_c
			comment_c_dic['time'] = comment.select('.comments_content')[0].select('.ui_mr10')[0].string
			comments_r = comment.select('.mod_comments_sub')
			if(not comments_r):
				continue
			comments_rr = []
			if(comments_r[0].ol):
				for comment_r in comments_r[0].ol:
					comment_rr = ''
					spans = comment_r.select('.comments_content')[0].select('span')
					for span in spans:
						for string in span.stripped_strings:
							if(string != None and type(span.previous_sibling) != bs4.element.Tag and span.previous_sibling != None):
								if(span.previous_sibling.strip() == ':'):
									comment_rr += string
					comment_r_dic = {}
					comment_r_dic['nickname'] = comment_r.select('.comments_content')[0].select('.nickname')[0].string
					comment_r_dic['content'] = comment_rr
					comment_r_dic['time'] = comment_r.select('.comments_content')[0].select('.ui_mr10')[0].string
					comments_rr.append(comment_r_dic)
					print comment_rr.encode('GBK','ignore')
			else:
				for comment_r in comments_r[0].ul:
					comment_rr = ''
					spans = comment_r.select('.comments_content')[0].select('span')
					for span in spans:
						for string in span.stripped_strings:
							if(string != None and type(span.previous_sibling) != bs4.element.Tag and span.previous_sibling != None):
								if(span.previous_sibling.strip() == ':'):
									comment_rr += string
					comment_r_dic = {}
					comment_r_dic['nickname'] = comment_r.select('.comments_content')[0].select('.nickname')[0].string
					comment_r_dic['content'] = comment_rr
					comment_r_dic['time'] = comment_r.select('.comments_content')[0].select('.ui_mr10')[0].string
					comments_rr.append(comment_r_dic)
					print comment_rr.encode('GBK','ignore')
			comments_c_r.append([comment_c_dic,comments_rr])
		taotaos.append([taotao_dic,comments_c_r])
	return taotaos
#todo 用os模块写个遍历文件，自动解析qq空间
file = open(r'qq_zone.txt')#原qq空间的html
file2 = open(r'back_content.txt','w')#输出路径
try:
	html = file.read()
finally:
	file.close()
if(html != None):
	taotaos = re_taotao(html)
	for taotao in taotaos:
		file2.write('taotao:'.decode('UTF-8','ignore'))
		content = taotao[0]
		file2.write(content['content'].decode('UTF-8','ignore') + " 转:".decode('UTF-8','ignore') + content['zhuan'].decode('UTF-8','ignore') + "赞:".decode('UTF-8','ignore') + content['zan'].decode('UTF-8','ignore'))
		file2.write('\n'.decode('UTF-8','ignore'))
		for comment in taotao[1]:
			file2.write('comment:\n  '.decode('UTF-8','ignore'))
			file2.write(comment[0]['nickname'].decode('UTF-8','ignore') + ' : '.decode('UTF-8','ignore') + comment[0]['content'].decode('UTF-8','ignore') + ' 时间: '.decode('UTF-8','ignore') + comment[0]['time'].decode('UTF-8','ignore'))
			file2.write("\nre_comment:".decode('UTF-8','ignore'))
			for comment_r in comment[1]:
				file2.write('\n  '.decode('UTF-8','ignore'))
				file2.write(comment_r['nickname'].decode('UTF-8','ignore') + ' : '.decode('UTF-8','ignore') + comment_r['content'].decode('UTF-8','ignore') + ' 时间: '.decode('UTF-8','ignore') + comment_r['time'].decode('UTF-8','ignore'))
			file2.write('\n'.decode('UTF-8','ignore'))
	print 'success'
	file2.close()
else:
	print 'html为空'