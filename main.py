import click
import tqdm
import time
import pandas as pd
from smtplib import SMTP_SSL as SMTP
import re
from dotenv import dotenv_values
from email.mime.text import MIMEText


@click.command()
@click.option("--csv", type=click.Path(exists=True, dir_okay=False))
@click.option("--template", type=click.Path(exists=True, dir_okay=False))
@click.option("--subject", type=str)
@click.option("--bcc", type=str, required=False)
def send_mails(csv: str, template: str, subject: str, bcc: str | None) -> None:
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
        for index, mail in tqdm.tqdm(
            zip(table.index, table[config["mail_column"]]), total=table.shape[0]
        ):
            with open(template) as t:
                text = t.read()
                subbed_text = re.sub(
                    r"\{(.+)\}", lambda x: str(table.at[index, x.group(1)]), text
                )

                # compose mail
                msg = MIMEText(subbed_text, "plain")
                msg["Subject"] = subject
                msg["From"] = config["sender"]
                if bcc is not None:
                    msg["Bcc"] = bcc

                try:
                    conn.sendmail(
                        config["sender"],
                        mail if bcc is None else [mail, bcc],
                        msg.as_string(),
                    )
                except:
                    print(f"could not send message to {mail}")
                    not_sent.append(mail)

                time.sleep(3)

    conn.quit()

    if len(not_sent):
        print(f"{len(not_sent)} mails could not be sent")
        for mail in not_sent:
            print(mail)
    else:
        print("all mails sent successfully")


if __name__ == "__main__":
    send_mails()
