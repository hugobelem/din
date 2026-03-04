from din.interface.cli import app
from din.shared.infra.db import init_db

def main() -> None:
    init_db()
    app()

if __name__ == '__main__':
    main()
