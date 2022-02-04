import threading
from time import sleep
from parse_table import main
from create_xml import create_xml
from bottle import route, run, static_file, get
import os


@route('/')
def server_static():
    return static_file(filename='output.xml', root='.')

@get('/src/<folder>/<filename>')
def get_photo(folder, filename):
    return static_file(filename=filename, root=f'src/{folder}/')

def create_file():
    while True:
        print('='*100,'\n','XML CREATE','\n')
        create_xml(main())
        sleep(1200)


# run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
# run(host='localhost', port=8080)
p_bottle = threading.Thread(target=run, kwargs=dict(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug='True'))
# p_bottle.daemon = True
# p_bottle = threading.Thread(target=run, kwargs=dict(host='localhost', port=8080, debug='True'))
# p_bottle.daemon = True
p_bottle.start()

create = threading.Thread(target=create_file)
create.start()