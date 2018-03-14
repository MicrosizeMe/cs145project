import codecs
from lxml import etree
from glob import glob
from unicodecsv import DictWriter
from multiprocessing import Pool

def main():
    # Sorted list of all xml file names
    xml_file_list = sorted(glob('./data/wdvc16_*_*.xml') + 
                           glob('./data/validation/wdvc16_*_*.xml') + 
                           glob('./data/test/wdvc16_*_*.xml'))

    p=Pool(4)
    p.map(parse_file, xml_file_list)

def parse_file(xml_file):
    print 'converting %s to csv' % xml_file
    # csv file name
    new_file_path = xml_file.replace('wdvc16', 'converted_wdvc16').replace('.xml', '.csv')
    print 'writing to %s' % new_file_path

    # page by page generator of the xml file
    xml_file_by_pages = page_stream_generator(xml_file)

    # columns
    columns = [u'page_title', u'page_ns', u'page_id',
               u'revision_id', u'revision_timestamp', u'revision_comment',
               u'revision_model', u'revision_format', u'revision_count',
               u'username', u'user_id', u'ip_address']

    with open(new_file_path, 'w') as csv_file:
        writer = DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()

        for xml_page in xml_file_by_pages:
            revisions_in_page = parse_page(xml_page)
            for page in revisions_in_page:
                writer.writerow(page)

# generator that walks through filename and yields each page
# as a space-separated string
def page_stream_generator(filename):
    with codecs.open(filename, 'r', 'utf8') as xml_file:
        page_contents = []

        # walk through xml
        for line in xml_file:
            line = line.strip()
            if line == '<page>': # new page; overwrite
                page_contents = [line]
            elif line == '</page>': # end of page; yield
                page_contents.append(line)
                yield ' '.join(page_contents)
            else: # inside page; keep going
                page_contents.append(line)

# takes an xml page and returns a list of dictionaries representing revisions in the page
def parse_page(page):
    root = etree.fromstring(page)

    #get page attributes
    page_dict = {}
    page_dict['page_title'] = none_handler(root.find('title'))
    page_dict['page_ns'] = none_handler(root.find('ns'))
    page_dict['page_id'] = none_handler(root.find('id'))

    revisions = root.findall('revision')
    page_dict['revision_count'] = len(revisions)

    all_revisions_in_page = []

    # need a new dictionary for each revision in the page
    for revision in revisions:
        # get revision attributes
        revision_dict = dict(page_dict)
        revision_dict['revision_id']=none_handler(revision.find('id'))
        revision_dict['revision_timestamp']=none_handler(revision.find('timestamp'))
        revision_dict['revision_comment']=none_handler(revision.find('comment'))
        revision_dict['revision_model']=none_handler(revision.find('model'))
        revision_dict['revision_format']=none_handler(revision.find('format'))

        # get contributor attributes
        contributor = revision.find('contributor')
        username = contributor.find('username')

        if username is not None:
            revision_dict['username'] = username.text
            revision_dict['user_id'] = none_handler(contributor.find('id'))
            revision_dict['ip_address'] = None
        else:
            revision_dict['username'] = None
            revision_dict['user_id'] = None
            revision_dict['ip_address'] = none_handler(contributor.find('ip'))

        all_revisions_in_page.append(revision_dict)

    return all_revisions_in_page
        

# handles case when etree doesn't contain a tag
def none_handler(element):
    if element is not None:
        return element.text
    else:
        return None

if __name__ == '__main__':
    main()
