def write_notification(email: str, mensagem: str):
    """Write notification."""
    with open("log.txt", mode="w") as file:
        conteudo = f"Email: {email} - msg: {mensagem}\n"
        file.write(conteudo)
