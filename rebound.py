# Globals #


import os
import click
import utilities as util


# Helpers #


def display_results(search_results):
    for result in search_results:
        color = "green" if result["Answers"] != 0 else "white"

        click.echo(click.style("(" + str(result["Votes"]) + " Votes | " + str(result["Answers"]) + " Answers) ", fg=color) + click.style(result["Title"], bold=True))
        click.echo(result["Body"])
        click.echo(click.style("\n" + result["URL"], fg="blue"))
        click.echo(os.get_terminal_size().columns * "–") # Display divider


# Main #


@click.command()
@click.argument("command")
def rebound(command):
    output, error = util.execute(command) # Excutes the command and pipes output
    language = util.get_language(command) # Gets the language name
    #error_msg = util.get_error_message(error) # Prepares error message for search

    if error != None: # error_msg
        click.echo(os.get_terminal_size().columns * "–") # Display divider

        search_results, last_page, captcha = util.search_stackoverflow("Example error message", 1) # language + " " + error_msg
        if search_results != []:
            if click.confirm("\nDisplay Stack Overflow results?"):
                if captcha:
                    click.echo(click.style("\nSorry, Stack Overflow blocked our request. Try again in a minute.", fg="red"))
                else:
                    click.echo(click.style("\nResults for: " + "Example error message" + "\n", bold=True)) # (language + " " + error_msg)
                    display_results(search_results)

                    count = 1
                    while click.confirm("Display more results?") and not last_page:
                        search_results, last_page, captcha = util.search_stackoverflow("Example error message", count + 1) # language + " " + error_msg

                        if captcha:
                            click.echo(click.style("\nSorry, Stack Overflow blocked our request. Try again in a minute.", fg="red"))
                            break
                        else:
                            display_results(search_results)