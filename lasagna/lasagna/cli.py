import click

import lasagna.app as app


@click.command()
@click.option(
    '--host', default='0.0.0.0',
    help='host on which the application will be served'
)
@click.option(
    '--port', default=5000,
    help='port on which the application will be served'
)
@click.option(
    '--debug', is_flag=True, default=True,
    help='start the application in debug mode'
)
@click.option(
    '--reloader', is_flag=True, default=True,
    help='reload the application when the '
)
def main(host, port, debug, reloader):
    app.create_app().run(host=host, port=port, debug=debug,
                         use_reloader=reloader)
