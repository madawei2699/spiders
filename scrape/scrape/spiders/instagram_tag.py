import json
import optparse
import os


def scrape(in_dir, out_file):
    with open(out_file, 'w') as out:
        out.write('tag|count\n')
        for file in os.listdir(in_dir):
            with open(os.path.join(in_dir, file), 'r') as f:
                try:
                    d = json.loads(f.read())
                    out.write('%s|%s\n' % (file, d['hashtags'][0]['hashtag']['media_count']))
                except Exception as e:
                    print 'Failed to parse json file: ', file
                    out.write('%s|\n' % file)


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option("-i", "--in_dir", dest="in_dir", default='',
                      help='Input directory containing all the json data files..')
    parser.add_option("-o", "--out_file", dest="out_file", default='',
                      help='File to output data.')

    (options, args) = parser.parse_args()

    assert options.in_dir != ''
    assert options.out_file != ''

    scrape(options.in_dir, options.out_file)
