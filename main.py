from typing import TextIO

import click
import tqdm
import time
import pandas as pd
from smtplib import SMTP_SSL as SMTP
import re
from dotenv import dotenv_values
from email.mime.text import MIMEText


# fmt: off
@click.command()
@click.option("--csv", type=click.Path(exists=True, dir_okay=False), help="path to the csv containing all people to send the mail to")
@click.option("--mail_column", type=str, help="the name of the column of the email address of the recipients")
@click.option("--template", type=click.File("r"), help="path to the text template for the mail \{*column name*\} will be swappend for the appropriate data from the csv")
@click.option("--subject", type=str, help="subject of the mail")
@click.option("--bcc", type=str, required=False, help="blind copy for the mail")
@click.option("--interval", type=int, default=3, help="pause between each sending of a mail in seconds")
# fmt: on
def send_mails(
    csv: str,
    mail_column: str,
    template: TextIO,
    subject: str,
    bcc: str | None,
    interval: int,
) -> None:
    config = dotenv_values(".env")
    table = pd.read_csv(csv)

    not_sent = []

    try:
        conn = SMTP(config["smtp_server"], port=465)
        conn.set_debuglevel(False)
        conn.login(config["username"], config["password"])
    except:
        print(f"could not establish connection to {config['smtp_server']}")
    else:
        text = template.read()
        for index, mail in tqdm.tqdm(
            zip(table.index, table[mail_column]), total=table.shape[0]
        ):
            subbed_text = re.sub(
                r"\{(.+)\}", lambda x: str(table.at[index, x.group(1)]), text
            )

            # compose mail
            msg = MIMEText(subbed_text, "plain")
            msg["Subject"] = subject
            msg["From"] = config["sender"]
            if bcc:
                msg["Bcc"] = bcc

            try:
                conn.sendmail(
                    config["sender"],
                    [mail, bcc] if bcc else mail,
                    msg.as_string(),
                )
            except:
                print(f"could not send message to {mail}")
                not_sent.append(mail)

            time.sleep(interval)

    conn.quit()

    if len(not_sent):
        print(f"{len(not_sent)} mails could not be sent")
        for mail in not_sent:
            print(mail)
    else:
        print("all mails sent successfully")


if __name__ == "__main__":
    send_mails()
