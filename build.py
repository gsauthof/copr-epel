#!/usr/bin/env python3

# Download and verify .spec file sources - e.g. in the COPR environment.
#
# 2018, Georg Sauthoff <mail@gms.tf>, GPLv3+

import glob
import hashlib
import os
import subprocess
import sys
import tempfile

def print_git():
    changeset = open('../.git/refs/heads/master').read().strip()
    print('Git repo at: {}'.format(changeset))

def download(url):
    print('Fetching {} ... '.format(url), end='')
    filename = url[url.rindex('/')+1:]
    just_https = ([ '--proto-redir', '=https' ] if url.startswith('https://')
        else [])
    subprocess.run(['curl'] + just_https + ['--silent', '--show-error',
        '--fail', '-L', '-o', filename, url], check=True)
    print('done.')
    return filename


def yield_urls(output):
    for line in output.splitlines():
        if line.startswith('Source') or line.startswith('Patch'):
            x = line.split()
            x[0] = x[0].strip(':')
            yield x

def spectool_yield_urls(specfile):
    xs = subprocess.check_output(['spectool', specfile],
            universal_newlines=True)
    yield from yield_urls(xs)

def rpmbuild_yield_urls(specfile):
    with tempfile.TemporaryDirectory() as td, open(specfile) as f:
        with open(td + '/pkg.spec', 'w') as g:
            sources = []
            for line in f:
                g.write(line)
                if line.startswith('%prep'):
                    print('cat << %EOF%', file=g)
                    for source in sources:
                        g.write(source)
                    print('%EOF%', file=g)
                    break
                elif line.startswith('Source') or line.startswith('Patch'):
                    sources.append(line)
        xs = subprocess.check_output(['rpmbuild']
                + sum((['--define', '_{}dir {}'.format(x, td) ]
                    for x in ('top', 'source', 'build', 'srcrpm', 'rpm')), [])
                + [ '--nodeps', '-bp', td + '/pkg.spec'],
                stderr=subprocess.DEVNULL, universal_newlines=True)
        yield from yield_urls(xs)

def rpmspec_yield_urls(specfile):
    xs = subprocess.check_output(['rpmspec', '-P', specfile],
            universal_newlines=True)
    yield from yield_urls(xs)

def get_checksums(specfile):
    d = {}
    with open(specfile) as f:
        for line in f:
            if line.startswith('#sha256('):
                i = line.index('(')
                j = line.index(')')
                k = line.index('=')
                key = line[i+1:j]
                checksum = line[k+1:].strip()
                d[key] = checksum
    return d

# cf. https://stackoverflow.com/a/44873382/427158
def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def verify_sources(urls, checksums):
    for key, url in urls:
        if '://' not in url:
            continue
        filename = download(url)
        checksum = sha256sum(filename)
        if checksum != checksums[key]:
            raise RuntimeError(('sha256 checksum of {} ({}) {} '
                'does NOT match the recorded one: {}').format(filename, key,
                    checksum, checksums[key]))

def build_srpm(specdir, outdir, specfile):
    subprocess.run(['rpmbuild', '--define', '_sourcedir {}'.format(specdir),
        '--define', '_specdir {}'.format(specdir),
        '--define', '_rpmdir {}'.format(outdir),
        '--define', '_srcrpmdir {}'.format(outdir),
        '-bs', specfile], check=True)

def main():
    # specdir equals $PWD
    outdir = sys.argv[1]
    # specdir = sys.argv[2]
    specdir = os.getcwd()
    specfile = glob.glob('*.spec')[0]
    print_git()
    urls = rpmspec_yield_urls(specfile)
    checksums = get_checksums(specfile)
    verify_sources(urls, checksums)
    build_srpm(specdir, outdir, specfile)

if __name__ == '__main__':
    sys.exit(main())

