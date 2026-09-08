"""Build, inspect and install both artifacts without publishing or using checkout imports."""
import argparse
import email
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import venv
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd=ROOT):
    subprocess.run([str(arg) for arg in args], cwd=cwd, check=True)


def check_metadata(raw):
    metadata = email.message_from_bytes(raw)
    assert metadata['Name'] == 'python-slugify'
    assert metadata['Version'] == '9.0.0'
    assert metadata['Requires-Python'] == '>=3.10'
    assert metadata['License-Expression'] == 'MIT'
    assert set(metadata.get_all('Provides-Extra')) == {'unidecode', 'anyascii'}
    requirements = metadata.get_all('Requires-Dist')
    assert any(value.startswith('text-unidecode>=1.3') for value in requirements)
    assert any('unidecode' in value.lower() and 'extra ==' in value for value in requirements)
    assert any('anyascii' in value and 'extra ==' in value for value in requirements)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outdir', type=Path, help='Retain artifacts in a new, empty directory')
    args = parser.parse_args()
    if args.outdir is not None:
        args.outdir = args.outdir.resolve()
        if args.outdir.exists() and any(args.outdir.iterdir()):
            parser.error('--outdir must be absent or empty; existing artifacts are not overwritten')
    with tempfile.TemporaryDirectory(prefix='slugify-release9-') as temporary:
        scratch = Path(temporary)
        dist = args.outdir if args.outdir is not None else scratch / 'dist'
        run(sys.executable, '-m', 'build', '--outdir', dist)
        artifacts = sorted(dist.iterdir())
        assert len(artifacts) == 2
        run(sys.executable, '-m', 'twine', 'check', '--strict', *artifacts)
        for artifact in artifacts:
            if artifact.suffix == '.whl':
                assert artifact.name.endswith('-py3-none-any.whl')
                with zipfile.ZipFile(artifact) as archive:
                    names = archive.namelist()
                    assert 'slugify/py.typed' in names
                    assert any(name.endswith('/licenses/LICENSE') for name in names)
                    check_metadata(archive.read(next(name for name in names if name.endswith('/METADATA'))))
                    entry = archive.read(next(name for name in names if name.endswith('/entry_points.txt')))
                    assert b'slugify = slugify.__main__:main' in entry
            else:
                with tarfile.open(artifact) as archive:
                    names = archive.getnames()
                    for required in ('LICENSE', 'test.py', 'test_release.py', 'pyproject.toml', 'slugify/py.typed',
                                     'docs/release-9/migration.md', 'tools/check_dist.py',
                                     'tools/check_algorithms.py', 'tools/legacy_reference.py'):
                        assert any(name.endswith('/' + required) for name in names), required
                    assert not any(name.endswith('evidence.json') for name in names)
                    metadata = archive.extractfile(next(name for name in names if name.endswith('/PKG-INFO')))
                    assert metadata is not None
                    check_metadata(metadata.read())
            assert not any('__pycache__' in name or name.endswith(('.pyc', '.pyo')) for name in names)
            env = scratch / ('wheel-env' if artifact.suffix == '.whl' else 'sdist-env')
            venv.EnvBuilder(with_pip=True).create(env)
            bin_dir = env / ('Scripts' if os.name == 'nt' else 'bin')
            python = bin_dir / ('python.exe' if os.name == 'nt' else 'python')
            command = bin_dir / ('slugify.exe' if os.name == 'nt' else 'slugify')
            run(python, '-m', 'pip', 'install', '--disable-pip-version-check', artifact, cwd=scratch)
            run(python, '-m', 'pip', 'check', cwd=scratch)
            run(python, '-c', "import slugify; from importlib.metadata import version; "
                "assert version('python-slugify') == slugify.__version__ == '9.0.0'; "
                "assert slugify.slugify('影師嗎', backend='text-unidecode') == 'ying-shi-ma'; "
                "print(slugify.__file__)", cwd=scratch)
            # Execute copied API checks outside the checkout, importing only installed code.
            checks = scratch / 'check_algorithms.py'
            checks.write_text((ROOT / 'tools/check_algorithms.py').read_text())
            run(python, checks, cwd=scratch)
            for invocation in ([command], [python, '-m', 'slugify']):
                args = [str(arg) for arg in invocation]
                args.extend(['--regex-pattern', '[^-a-z0-9_]+', '___Test___'])
                output = subprocess.check_output(args, cwd=scratch, text=True)
                assert output == '___test___\n'
                for algorithm, expected in ((None, 'ab'), ('legacy', 'ab'), ('modern', 'a-b')):
                    options = ['--algorithm', algorithm] if algorithm else []
                    output = subprocess.check_output([*map(str, invocation), *options, 'a&#39;b'],
                                                     cwd=scratch, text=True)
                    assert output == expected + '\n'
                invalid = subprocess.run([*map(str, invocation), '--algorithm', 'invalid', 'a'],
                                         cwd=scratch, capture_output=True, text=True)
                assert invalid.returncode == 2 and 'invalid choice' in invalid.stderr
                run(*invocation, '--help', cwd=scratch)
            # Prove Unicode-only runtime needs no transliteration dependency.
            run(python, '-m', 'pip', 'uninstall', '-y', 'text-unidecode', cwd=scratch)
            run(python, '-c', "from slugify import slugify; "
                "assert slugify('影師嗎', allow_unicode=True) == '影師嗎'", cwd=scratch)
            print(f'PASS: {artifact.name}: metadata, contents, installation, CLI, Unicode-only runtime')
        print('PASS: wheel and sdist validation; no upload or tag operations performed')


if __name__ == '__main__':
    main()
