import sqlite3 as sql
import os

from optparse import OptionParser
from PIL import Image



def present_images(img_dir, dataset, conn, cur):
  imgs = os.listdir(img_dir)
  if len(imgs) == 0: 
    print 'ERR: IMAGE DIR EMPTY dir:'+img_dir
    
  for img_file in imgs:
    if row_exists(cur, img_file): 
      print 'INFO: image already processed: ' + img_file
      continue
    img_path = os.path.join(img_dir, img_file)
    print img_path
    img = Image.open(img_path)
    img.show()
    num_plots = return_default_if_empty(raw_input('Approx num graphics (def 2)?'), 2)
    plots = return_default_if_empty(raw_input('Are there plots? (default:yes)'), 1)
    if plots:
      x_ax = return_default_if_empty(raw_input('Plot has x-axis? (default:yes)'), 1)
      y_ax = return_default_if_empty(raw_input('Plat has y-axis? (default:yes)'), 1)
    else:
      x_ax = 0 
      y_ax = 0
    has_img = return_default_if_empty(raw_input('Contains any images (default:yes=1)?'), 1) 
    has_diag = return_default_if_empty(raw_input('Contains any diagrams (default:yes=1)?'), 1) 
    has_color = return_default_if_empty(raw_input('Has color in the plot (default:yes=1)?'), 1)

    print img_file, dataset, has_img, num_plots, has_color, has_diag
    cur.execute("INSERT INTO img_labels VALUES('{0}', '{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8})".format(img_file, dataset, num_plots, has_img, plots, x_ax, y_ax, has_color, has_diag))
    conn.commit()

def return_default_if_empty(val, default_val):
  if val == None or val.strip() == '':
    return default_val
  if val == 'y' or val == 'Y': return 1
  if val == 'n' or val == 'N': return 0
  return val
  
def get_db_cursor():
  conn = sql.connect('../data/image_labels.db')
  cur = conn.cursor()
  # Create the db with cols:            
  cur.execute("""CREATE TABLE IF NOT EXISTS img_labels (file_name text, dataset text, 
              num_graphics integer, has_image integer, has_plot integer, 
              has_x_axis integer, has_y_axis integer, has_color integer, 
              has_diagram integer) """)
  return conn, cur

def row_exists(cur, path):
  cur.execute("SELECT * FROM img_labels WHERE file_name= '" + path + "';")
  return cur.fetchone() != None 
  


if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-d', '--dir', default='',
                    help='The directory to open images from. e.g.  ../scrape_figures/dump/full/')
  parser.add_option('-c', '--dataset', default='',
                    help='The dataset the images are from. e.g. nature-adsorption')
  (options, args) = parser.parse_args()
  if options.dir == '':
    print 'ERR: please provide a directory with -d <img dir>'
    quit()
  conn, cur = get_db_cursor()
  present_images(options.dir, options.dataset, conn, cur)
