__author__ = 'Shaun'

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for pageNumber, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True)):
        if pageNumber >= 2:
            interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

results = convert_pdf_to_txt('C:\Users\Shaun\Downloads\statement.pdf')
results2 = convert_pdf_to_txt('C:\Users\Shaun\Downloads\statement (1).pdf')
results_split = filter(None, results.split('\n'))
results_split2 = filter(None, results2.split('\n'))

results_list = filter(None, results.split('\n'))
results2_list = filter(None, results2.split('\n'))

split_test = results.split('New charges - transaction details')
split_test2 = results2.split('New charges - transaction details')

split_1 = filter(None, split_test[1].split('Total incl. GST($)'))
split_12 = filter(None, split_test2[1].split('Total incl. GST($)'))

split_2 = split_1[1].split('Total trips for tag 0914129799')
split_2_filtered = filter(None, split_2[0].split('\n'))

split_22 = split_12[1].split('Total trips for tag 0914129799')
split_22_filtered = filter(None, split_22[0].split('\n'))

split_3_docnum_date = filter(None, split_2[0].split('\n'))
split_3_docnum_date2 = filter(None, split_22[0].split('\n'))

list_length = split_3_docnum_date.__len__()
list_length2 = split_3_docnum_date2.__len__()

split_4 = split_2[1].split('Other fees, charges and adjustments')
split_42 = split_22[1].split('Other fees, charges and adjustments')

split_5_time = filter(None, split_4[0].split('\n'))
split_5_time2 = filter(None, split_42[0].split('\n'))

location = split_5_time[list_length:list_length*2]
location2 = split_5_time2[list_length:list_length*2]

split6 = split_4[1].split('Total other fees, charges and adjustments ')
split62 = split_42[1].split('Total other fees, charges and adjustments ')

split7_cost_list = filter(None, split6[1].split('\n'))
split7_cost_list2 = filter(None, split_42[0].split('\n'))

cost_list = split7_cost_list[0:list_length]
cost_list2 = split7_cost_list2[list_length2*2:list_length2*3]

final_list = []
count = 0
for i in split_3_docnum_date:
    final_list.append(i + ' ' + split_5_time[count] + ' ' + location[count] + ' ' + cost_list[count])
    count += 1
print ''

#            for m in xrange(0, len(i), 4):
#                new_log_lines.append(i[m+1]