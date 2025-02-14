
install-deps:
    pip install poetry
    projen

install-precommit:
    pre-commit install
    pre-commit install --hook-type commit-msg

update-precommit:
    pre-commit autoupdate

run-precommit:
    pre-commit run --all-files

make-commit-without-pre-commit:
    git commit --no-verify -m "Your commit message"
