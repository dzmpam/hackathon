import strictyaml
import os
import shutil

SEED_FILE="/app/seed.yml"

def run_pipeline(name, app_dir, out_dir):
    os.system('docker run --rm -v {app_dir}:/app -e "APP_DIR={app_dir}" '\
              '-v /var/run/docker.sock:/var/run/docker.sock -e "PARENT_OUT_DIR={out_dir}" {name}'
              .format(app_dir = app_dir,
                      out_dir = out_dir,
                      name = name))

def main():
    with open(SEED_FILE, 'r') as file:
        seed = strictyaml.load(file.read())

    app_dir = os.environ['APP_DIR']
    parent_out_dir = os.environ.get('PARENT_OUT_DIR', '')
    out_dir = parent_out_dir + os.path.sep + 'ci'

    shutil.rmtree('/app/' + out_dir, ignore_errors=True)
    os.mkdir('/app/' + out_dir)

    run_pipeline(seed['pipeline'], app_dir, out_dir)

    open('/app/' + out_dir + '/seed.out', 'w+')
    print 'Seed finished'

if __name__ == '__main__':
    main()
